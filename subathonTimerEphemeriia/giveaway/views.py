from django.shortcuts import render, HttpResponseRedirect

from .models import Calendar
from .serializers import CalendarSerializer


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

    active_calendar_json = CalendarSerializer(active_calendar).data if active_calendar else None
    calendars_json = CalendarSerializer(calendars, many=True).data

    return render(
        request,
        "giveaway/admin.html",
        {"calendars": calendars_json, "active_calendar": active_calendar_json},
    )
