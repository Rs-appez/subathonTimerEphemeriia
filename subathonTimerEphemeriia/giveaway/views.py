from django.contrib.auth.decorators import permission_required, user_passes_test
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.views.decorators.http import require_http_methods
from utils.permissions import is_streamer

from .models import BaseCalendar, Calendar
from .serializers import BaseCalendarSerializer, CalendarSerializer


@user_passes_test(is_streamer)
def index(request):
    calendar = Calendar.objects.filter(is_active=True).last()
    calendar_json = CalendarSerializer(calendar).data

    return render(request, "giveaway/index.html", {"calendar": calendar_json})


@permission_required("giveaway.view_calendar")
def admin(request):
    calendars = Calendar.objects.all()
    active_calendar = calendars.filter(is_active=True).last()

    active_calendar_json = (
        CalendarSerializer(active_calendar).data if active_calendar else None
    )
    calendars_json = CalendarSerializer(calendars, many=True).data

    return render(
        request,
        "giveaway/admin.html",
        {"calendars": calendars_json, "active_calendar": active_calendar_json},
    )


@permission_required("giveaway.add_calendar")
def create_calendar(request):
    base_calendars = BaseCalendar.objects.all().order_by("size")
    base_calendars_json = BaseCalendarSerializer(base_calendars, many=True).data

    return render(
        request,
        "giveaway/create_calendar.html",
        {"base_calendars": base_calendars_json},
    )


@permission_required("giveaway.change_calendar")
def edit_calendar(request, calendar_id):
    calendar = get_object_or_404(Calendar, id=calendar_id)
    sorted_cells = calendar.get_sorted_cells()

    return render(
        request,
        "giveaway/update_calendar.html",
        {"calendar": calendar, "sorted_cells": sorted_cells},
    )


@permission_required("giveaway.change_calendar")
@require_http_methods(["POST"])
def shuffle_rewards(request, calendar_id: int):
    calendar = get_object_or_404(Calendar, id=calendar_id)
    calendar.shuffle_reward()
    return render(
        request,
        "giveaway/partials/cells-container.html",
        {"sorted_cells": calendar.get_sorted_cells()},
    )


@permission_required("giveaway.change_calendar")
def activate_calendar(request, calendar_id):
    calendar = Calendar.objects.get(id=calendar_id)
    if calendar:
        calendar.activate()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@permission_required("giveaway.change_calendar")
def deactivate_calendar(request, calendar_id):
    calendar = Calendar.objects.get(id=calendar_id)
    if calendar:
        calendar.deactivate()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@permission_required("giveaway.delete_calendar")
def delete_calendar(request, calendar_id):
    calendar = Calendar.objects.get(id=calendar_id)
    if calendar:
        calendar.delete()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@permission_required("giveaway.add_reward")
def create_reward(request):
    return render(request, "giveaway/create_reward.html")
