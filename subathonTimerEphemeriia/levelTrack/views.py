from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from .models import LevelTracker
from .serializers import LevelTrackerSerializer


def index(request, id: int):
    lt = get_object_or_404(LevelTracker, pk=id)
    lt_data = LevelTrackerSerializer(lt).data
    return render(request, "index.html", {"tracker": lt_data})
