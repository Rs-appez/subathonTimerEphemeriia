from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpRequest
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Timer, TipGoal
from .serializers import TimerSerializer, TipGoalSerializer
from .utils import write_log
from django.conf import settings

import time
import threading


def index(request):
    timer = Timer.objects.last()
    tip_images = []
    tip_goals_values = []

    sub_images = []
    sub_goals_values = []

    if timer is None:
        time = "no timer"
    else:
        time = timer.display_time()
        started = timer.timer_active

        for goal in timer.get_tip_goal():
            tip_images.append(goal.get_image())
            tip_goals_values.append(goal.goal_amount)

        for goal in timer.get_sub_goal():
            sub_images.append(goal.get_image())
            sub_goals_values.append(goal.goal_amount)

    return render(
        request,
        "subathonTimer/index.html",
        {
            "time": time,
            "started": started,
            "tip_images": tip_images,
            "tip_goals_values": tip_goals_values,
            "total_tips": timer.timer_total_donations,
            "sub_images": sub_images,
            "sub_goals_values": sub_goals_values,
            "total_subs": timer.timer_total_subscriptions,
            "timer_paused": timer.timer_paused,
            "paused_time": timer.display_paused_time(),
        },
    )


def add_time(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/admin_django/login/?next=/timer/add_time")

        user = request.user

        req = HttpRequest()
        req.user = user
        req.method = "POST"
        req.data = {
            "time": request.POST["time"],
            "username": user.username,
        }

        tvs = TimerViewSet()

        res = tvs.add_time(req)

        return redirect(
            f"/add_time_success?message={res.data['message']}&status={res.data['status']}"
        )

    elif request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/admin_django/login/?next=/add_time/")
        timer = Timer.objects.last()
        return render(
            request,
            "subathonTimer/addTime.html",
            {"logs": __get_logs(), "timer_paused": timer.timer_paused},
        )


def add_time_success(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/timer/add_time/")
    timer = Timer.objects.last()
    return render(
        request,
        "subathonTimer/addTime.html",
        {
            "message": request.GET.get("message", ""),
            "status": request.GET.get("status"),
            "logs": __get_logs(),
            "timer_paused": timer.timer_paused,
        },
    )


def __get_logs():
    path = "/logs/log.txt" if not settings.DEBUG else "log.txt"
    with open(path, "r") as f:
        lines = f.readlines()
    return lines[::-1]


def start_timer(request):
    if request.method == "POST":
        timer = Timer.objects.last()
        timer.start_timer()
        return redirect("index")


def pause_timer(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/timer/add_time/")
    if request.method == "POST":

        req = HttpRequest()
        req.method = "POST"
        req.user = request.user

        tvs = TimerViewSet()
        if request.POST.get("pause") == "true":
            res = tvs.pause(req)

        else:
            res = tvs.resume(req)

        return redirect(
            f"/add_time_success?message={res.data['message']}&status={res.data['status']}"
        )


def tip_progress(request):
    timer = Timer.objects.last()
    last_goal = timer.get_last_tip_goal()

    return render(
        request,
        "subathonTimer/tipProgress.html",
        {"total_tips": timer.timer_total_donations, "last_goal": last_goal.goal_amount},
    )


class TimerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Timer.objects.all()
    serializer_class = TimerSerializer

    seen_ids = set()
    cache_lock = threading.Lock()

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def get_timer_info(self, request, pk=None):
        timer = Timer.objects.last()
        time = timer.display_time()
        return Response({"time": time})

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def sub(self, request, pk=None):
        timer = Timer.objects.last()

        tier = request.data["tier"]
        username = request.data["username"]
        id = request.data["id"]
        gifter = request.data["gifter"] if "gifter" in request.data else ""

        if gifter is None:
            gifter = ""

        bonus_time = 0

        if id in self.seen_ids:
            return Response({"message": "Already seen", "status": 400})

        self.seen_ids.add(id)

        try:
            tier = int(tier)

            if not timer.new_sub(tier):
                raise Exception

            with self.cache_lock:

                last_gifters = cache.get("last_gifter", [])

                last_gifter = [x for x in last_gifters if x[0] == gifter]
                last_gifter = last_gifter[0] if last_gifter else ("", 0, 0)

                if (
                    gifter != ""
                    and gifter == last_gifter[0]
                    and time.time() - last_gifter[2] < 20
                ):
                    update_gifter = (gifter, last_gifter[1] + 1, time.time())

                    if update_gifter[1] == 5:
                        bonus_time = timer.add_bonus_sub(tier, 5)

                    elif update_gifter[1] == 10:
                        bonus_time = timer.add_bonus_sub(tier, 15)
                        update_gifter = (gifter, 0, time.time())

                else:
                    update_gifter = (gifter, 1, time.time())

                if last_gifter in last_gifters and last_gifter[0] != "":
                    last_gifters[last_gifters.index(last_gifter)] = update_gifter
                else:
                    last_gifters.append(update_gifter)

                cache.set("last_gifter", last_gifters)

        except Exception as e:
            return Response({"message": "Invalid tier", "status": 400})

        timer.send_ticket()

        msg = f"New sub: {username} - {tier}"

        if gifter != "":
            msg += f" - offered by {gifter}"
        write_log(msg)

        if bonus_time > 0:
            write_log(f"Bonus time added for {gifter} - {bonus_time} seconds")

        return Response({"message": "Sub added", "status": 200})

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def bits(self, request, pk=None):
        timer = Timer.objects.last()

        bits = request.data["bits"]
        username = request.data["username"]
        id = request.data["id"]

        if id in self.seen_ids:
            return Response({"message": "Already seen", "status": 400})

        self.seen_ids.add(id)

        try:
            bits = int(bits)
            timer.new_bits(bits)

        except Exception:
            return Response({"message": "Invalid bits", "status": 400})

        timer.send_ticket()

        write_log(f"New bits: {username} - {bits}")

        return Response({"message": "Bits added", "status": 200})

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def donation(self, request, pk=None):
        timer = Timer.objects.last()
        donation = request.data["amount"]
        name = request.data["name"]
        id = request.data["id"]

        if id in self.seen_ids:
            return Response({"message": "Already seen", "status": 400})

        self.seen_ids.add(id)

        try:
            donation = float(donation)
            timer.new_donation(donation)

        except Exception as e:
            return Response({"message": "Invalid donation", "status": 400})

        timer.send_ticket()

        write_log(f"New donation: {name} - {donation}")

        return Response({"message": "Donation added", "status": 200})

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def add_time(self, request, pk=None):
        timer = Timer.objects.last()
        time = request.data["time"]
        username = (
            request.data["username"] if "username" in request.data else "anonymous"
        )

        try:
            timer.add_time(float(time))

        except Exception as e:
            return Response({"message": "Invalid time", "status": 400})

        timer.send_ticket()

        write_log(f"{username} added time: {time} seconds")

        return Response({"message": "Time added", "status": 200})

    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser])
    def pause(self, request, pk=None):
        timer = Timer.objects.last()
        user = request.user
        if timer.pause_timer(user.username):
            timer.send_ticket()
            return Response({"message": "Timer paused", "status": 200})
        return Response({"message": "Timer already paused", "status": 400})

    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser])
    def resume(self, request, pk=None):
        timer = Timer.objects.last()
        user = request.user
        if timer.resume_timer(user.username):
            timer.send_ticket()
            return Response({"message": "Timer resumed", "status": 200})
        return Response({"message": "Timer not paused", "status": 400})


class TipGoalViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = TipGoal.objects.all()
    serializer_class = TipGoalSerializer
