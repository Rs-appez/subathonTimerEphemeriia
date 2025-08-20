from django.shortcuts import render

from .models import Whell, Entry
from .serializers import WhellSerializer, EntrySerializer


def index(request):
    wheel = Whell.objects.filter(active=True).first()
    if not wheel:
        return render(request, "wheel_error.html")

    wheel_serializer = WhellSerializer(wheel)

    return render(
        request,
        "wheel.html",
        {
            "wheel": wheel_serializer.data
        },
    )
