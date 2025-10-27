from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404
from django.http import  HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import LevelTracker
from .serializers import LevelTrackerSerializer


@permission_required("levelTrack.view_leveltracker")
def index(request, id: int):
    lt = get_object_or_404(LevelTracker, pk=id)
    lt_data = LevelTrackerSerializer(lt).data
    return render(request, "index.html", {"tracker": lt_data})


@permission_required("levelTrack.change_leveltracker")
def admin_view(request, id: int):
    lt = get_object_or_404(LevelTracker, pk=id)

    if request.method == "POST":
        current_level = request.POST.get("new_level")
        try:
            current_level = int(current_level)
        except (TypeError, ValueError):
            return HttpResponse("Invalid current level", status=400)
        lt.update_level(current_level)
        return redirect("bar_tracker_admin", id=lt.id)

    return render(request, "admin_view.html", {"tracker": lt})
