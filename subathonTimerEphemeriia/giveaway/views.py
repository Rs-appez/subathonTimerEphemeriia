from django.shortcuts import render, HttpResponseRedirect

from .models import Calendar
from .serializers import CalendarSerializer


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/giveaway/")

    calendar = Calendar.objects.filter(is_active=True).last()
    calendar_json = CalendarSerializer(calendar).data

    return render(request, "giveaway/index.html", {"calendar": calendar_json})
