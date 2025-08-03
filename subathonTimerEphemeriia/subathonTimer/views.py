from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import permission_required, user_passes_test

from .utils import get_logs, get_donators, get_gifters
from utils.permissions import is_streamer

from .models import Timer, CarouselAnnouncement
from .serializers import CarouselAnnouncementSerializer
from .views_api import TimerViewSet


@permission_required("subathonTimer.view_timer")
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
            "tip_validated": tip_validated[: timer.timer_nb_tips],
            "total_tips": timer.timer_total_donations,
            "subs": subs,
            "sub_nb_goals": timer.timer_nb_subs,
            "sub_goals_values": sub_goals_values,
            "sub_validated": sub_validated[: timer.timer_nb_subs],
            "total_subs": timer.timer_total_subscriptions,
            "timer_paused": timer.timer_paused,
            "paused_time": timer.display_paused_time(),
        },
    )


@permission_required("subathonTimer.view_timer")
def add_time(request):
    if request.method == "POST":
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
            f"/timer/add_time_success?message={res.data['message']}&status={
                res.data['status']
            }"
        )

    elif request.method == "GET":
        timer = Timer.objects.last()
        return render(
            request,
            "subathonTimer/addTime.html",
            {
                "logs": get_logs(),
                "timer_paused": timer.timer_paused,
                "multiplicator_sub_on": timer.multiplicator_sub_on,
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


@permission_required("subathonTimer.view_timer")
def add_time_success(request):
    timer = Timer.objects.last()
    return render(
        request,
        "subathonTimer/addTime.html",
        {
            "message": request.GET.get("message", ""),
            "status": request.GET.get("status"),
            "logs": get_logs(),
            "timer_paused": timer.timer_paused,
            "multiplicator_sub_on": timer.multiplicator_sub_on,
        },
    )


@user_passes_test(is_streamer)
def start_timer(request):
    if request.method == "POST":
        timer = Timer.objects.last()
        timer.start_timer()
        return redirect("index_timer")


@permission_required("subathonTimer.view_timer")
def pause_timer(request):
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
            f"/timer/add_time_success?message={res.data['message']}&status={
                res.data['status']
            }"
        )


@permission_required("subathonTimer.view_timer")
def refresh_timer(request):
    if request.method == "POST":
        req = HttpRequest()
        req.method = "POST"
        req.user = request.user

        tvs = TimerViewSet()
        res = tvs.refresh(req)

        return redirect(
            f"/timer/add_time_success?message={res.data['message']}&status={
                res.data['status']
            }"
        )


@permission_required("subathonTimer.view_timer")
def toggle_sub_multiplicator(request):
    if request.method == "POST":
        req = HttpRequest()
        req.method = "POST"
        req.user = request.user

        timer = Timer.objects.last()

        try:
            toggle = request.POST.get("toggle_multiplicator").lower() == "true"
            timer.toggle_sub_multiplicator(toggle)
        except Exception as e:
            return redirect(
                "/timer/add_time_success?message=Error in request&status=400"
            )

        message = "Multiplicator actived" if toggle else "Multiplicator desactived"

        return redirect(f"/timer/add_time_success?message={message}&status=200")


@permission_required("subathonTimer.view_timer")
def tip_progress(request):
    timer = Timer.objects.last()
    last_goal = timer.get_last_tip_goal()

    return render(
        request,
        "subathonTimer/tipProgress.html",
        {"total_tips": timer.timer_total_donations, "last_goal": last_goal.goal_amount},
    )


@permission_required("subathonTimer.view_timer")
def sub_progress(request):
    timer = Timer.objects.last()
    total_subs = timer.timer_total_subscriptions

    return render(
        request,
        "subathonTimer/totalSub.html",
        {"total_subs": total_subs},
    )


@permission_required("subathonTimer.view_timer")
def global_timer(request):
    timer = Timer.objects.last()
    return render(
        request,
        "subathonTimer/globalTimer.html",
        {"time": timer.started_time()},
    )


@permission_required("subathonTimer.view_timer")
def carousel_announcement(request):
    timer = Timer.objects.last()
    announcements = CarouselAnnouncement.objects.filter(timer=timer).all()
    announcements_json = CarouselAnnouncementSerializer(announcements, many=True).data
    switch_time = timer.nb_seconds_announcement

    return render(
        request,
        "subathonTimer/carouselAnnouncement.html",
        {
            "announcements": announcements,
            "announcements_json": announcements_json,
            "switch_time": switch_time,
        },
    )
