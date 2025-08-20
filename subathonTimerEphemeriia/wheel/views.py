from django.shortcuts import render

from .models import Whell
from .serializers import WhellSerializer


def index(request):
    wheel = Whell.objects.filter(active=True).first()
    if not wheel:
        return render(request, "wheel_error.html")

    wheel_serializer = WhellSerializer(wheel)

    return render(
        request,
        "wheel.html",
        {"wheel": wheel_serializer.data},
    )
