from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from .models import Calendar


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
@require_http_methods(["POST"])
def close_all_cells(request, calendar_id: int):
    calendar = get_object_or_404(Calendar, id=calendar_id)
    calendar.close_all_cells()
    return render(
        request,
        "giveaway/partials/cells-container.html",
        {"sorted_cells": calendar.get_sorted_cells()},
    )
