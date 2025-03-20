from django.shortcuts import render

from .models import Calendar
from .serializers import CalendarSerializer


def index(request):
    calendar = Calendar.objects.filter(is_active=True).last()
    calendar_json = CalendarSerializer(calendar).data

    return render(request, "giveaway/index.html", {"calendar": calendar_json})
