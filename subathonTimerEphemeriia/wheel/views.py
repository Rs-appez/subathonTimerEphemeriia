from django.shortcuts import render

from .models import Whell, Entry


def index(request):
    wheel = Whell.objects.filter(active=True).first()
    if not wheel:
        return render(request, "wheel_error.html")

    entries = Entry.objects.filter(whell=wheel).order_by("?")

    return render(request, "wheel.html", {
        "wheel": wheel,
        "entries": entries,
    })
