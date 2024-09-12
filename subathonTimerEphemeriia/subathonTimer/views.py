from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Timer
from .serializers import TimerSerializer
from .utils import write_log


def index(request):
    timer = Timer.objects.last()
    if timer is None:
        time = "no timer"
    else:
        time = timer.display_time()
        started = timer.timer_active
    return render(request, "index.html", {"time": time, "started": started})


def add_time(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/admin_django/login/?next=/add_time/")

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
        
        return render(request, "addTime.html", {"message": res.data["message"], "status": res.data["status"]})

    elif request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/admin_django/login/?next=/add_time/")
        return render(request, "addTime.html", {})


def start_timer(request):
    if request.method == "POST":
        timer = Timer.objects.last()
        timer.timer_active = True
        timer.save()
        return redirect("index")


class TimerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Timer.objects.all()
    serializer_class = TimerSerializer

    seen_ids = set()

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

        if id in self.seen_ids:
            return Response({"message": "Already seen", "status": 400})

        self.seen_ids.add(id)

        try:
            tier = int(tier)

            if not timer.new_sub(tier):
                raise Exception

        except Exception:
            return Response({"message": "Invalid tier", "status": 400})

        timer.send_ticket()

        write_log(f"New sub: {username} - {tier}")

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
