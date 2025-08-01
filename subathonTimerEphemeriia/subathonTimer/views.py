from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpRequest

from .utils import get_logs, get_donators, get_gifters

from .models import Timer
from .views_api import TimerViewSet

from datetime import timedelta, datetime

def index(request):
    timer = Timer.objects.last()
    tip_goals_values = []
    tip_validated = []
    tips = []

    sub_goals_values = []
    sub_validated = []
    subs = []

    if timer is None:
        time = "no timer"
    else:
        time = timer.display_time()
        started = timer.timer_active

        tips = timer.get_tip_goal()
        subs = timer.get_sub_goal()

        for goal in tips:
            tip_validated.append(goal.validated)
            tip_goals_values.append(goal.goal_amount)

        for goal in subs:
            sub_validated.append(goal.validated)
            sub_goals_values.append(goal.goal_amount)

    return render(
        request,
        "subathonTimer/index.html",
        {
            "time": time,
            "started": started,
            "tips": tips,
            "tip_nb_goals": timer.timer_nb_tips,
            "tip_goals_values": tip_goals_values,
            "tip_validated": tip_validated[:timer.timer_nb_tips],
            "total_tips": timer.timer_total_donations,
            "subs": subs,
            "sub_nb_goals": timer.timer_nb_subs,
            "sub_goals_values": sub_goals_values,
            "sub_validated": sub_validated[:timer.timer_nb_subs],
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
            f"/timer/add_time_success?message={res.data['message']}&status={res.data['status']}"
        )

    elif request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/admin_django/login/?next=/timer/add_time/")
        timer = Timer.objects.last()
        return render(
            request,
            "subathonTimer/addTime.html",
            {
                "logs": get_logs(),
                "timer_paused": timer.timer_paused,
                "multiplicator_on": timer.multiplicator_on,
            },
        )


def list_participants(request):
    donators = get_donators()
    gifters = get_gifters()
    return render(
        request,
        "subathonTimer/participants.html",
        {"donators": donators, "gifters": gifters},
    )


def subannivesary_summary(request):
    timer = Timer.objects.get(timer_name="subaniversery")
    time = timer.get_total_time()
    dons = timer.timer_total_donations
    subs = timer.timer_total_subscriptions
    bits = timer.timer_total_bits

    return render(
        request,
        "subathonTimer/summarySubanniversary.html",
        {"time": time, "dons": dons, "subs": subs, "bits": bits},
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
            "logs": get_logs(),
            "timer_paused": timer.timer_paused,
            "multiplicator_on": timer.multiplicator_on,
        },
    )


def start_timer(request):
    if request.method == "POST":
        timer = Timer.objects.last()
        timer.start_timer()
        return redirect("index_timer")


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
            f"/timer/add_time_success?message={res.data['message']}&status={res.data['status']}"
        )


def toggle_multiplicator(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/timer/add_time/")
    if request.method == "POST":
        req = HttpRequest()
        req.method = "POST"
        req.user = request.user

        timer = Timer.objects.last()

        try:
            toggle = request.POST.get("toggle_multiplicator").lower() == "true"
            timer.toggle_multiplicator(toggle)
        except Exception as e:
            return redirect(
                "/timer/add_time_success?message=Error in request&status=400"
            )

        message = "Multiplicator actived" if toggle else "Multiplicator desactived"

        return redirect(f"/timer/add_time_success?message={message}&status=200")


def tip_progress(request):
    timer = Timer.objects.last()
    last_goal = timer.get_last_tip_goal()

    return render(
        request,
        "subathonTimer/tipProgress.html",
        {"total_tips": timer.timer_total_donations, "last_goal": last_goal.goal_amount},
    )


def sub_progress(request):
    timer = Timer.objects.last()
    total_subs = timer.timer_total_subscriptions

    return render(
        request,
        "subathonTimer/totalSub.html",
        {"total_subs": total_subs},
    )


def global_timer(request):
    timer = Timer.objects.last()
    return render(
        request,
        "subathonTimer/globalTimer.html",
        {"time": timer.started_time()},
    )
