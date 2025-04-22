from django.shortcuts import render, HttpResponseRedirect

from .models import Calendar, BaseCalendar
from .serializers import CalendarSerializer, BaseCalendarSerializer


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/giveaway/")

    calendar = Calendar.objects.filter(is_active=True).last()
    calendar_json = CalendarSerializer(calendar).data

    return render(request, "giveaway/index.html", {"calendar": calendar_json})


def admin(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/giveaway/admin/")

    active_calendar = Calendar.objects.filter(is_active=True).last()
    calendars = Calendar.objects.all()

    active_calendar_json = (
        CalendarSerializer(active_calendar).data if active_calendar else None
    )
    calendars_json = CalendarSerializer(calendars, many=True).data

    return render(
        request,
        "giveaway/admin.html",
        {"calendars": calendars_json, "active_calendar": active_calendar_json},
    )


def create_calendar(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/giveaway/admin/create/")

    base_calendars = BaseCalendar.objects.all().order_by("size")
    base_calendars_json = BaseCalendarSerializer(base_calendars, many=True).data

    return render(
        request,
        "giveaway/create_calendar.html",
        {"base_calendars": base_calendars_json},
    )


def edit_calendar(request, calendar_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/giveaway/admin/edit/")

    calendar = Calendar.objects.get(id=calendar_id)
    calendar_json = CalendarSerializer(calendar).data

    return render(
        request,
        "giveaway/update_calendar.html",
        {"calendar": calendar_json},
    )


def activate_calendar(request, calendar_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/giveaway/admin/")

    calendar = Calendar.objects.get(id=calendar_id)
    if calendar:
        calendar.activate()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def deactivate_calendar(request, calendar_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/giveaway/admin/")

    calendar = Calendar.objects.get(id=calendar_id)
    if calendar:
        calendar.desactivate()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def delete_calendar(request, calendar_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/giveaway/admin/")

    calendar = Calendar.objects.get(id=calendar_id)
    if calendar:
        calendar.delete()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
