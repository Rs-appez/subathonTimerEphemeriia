from django.urls import path, include
from .views import (
    index,
    start_timer,
    add_time,
    add_time_success,
    toggle_sub_multiplicator,
    toggle_tip_multiplicator,
    tip_progress,
    sub_progress,
    pause_timer,
    global_timer,
    list_participants,
    subannivesary_summary,
    carousel_announcement,
)
from .views_api import TimerViewSet
from .views_sse import sse_stream

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"timer", TimerViewSet, basename="timer")

urlpatterns = [
    path("api/", include(router.urls)),
    path("", index, name="index_timer"),
    path("start_timer", start_timer, name="start_timer"),
    path("add_time/", add_time, name="add_time"),
    path("add_time_success/", add_time_success, name="add_time_success"),
    path(
        "toggle_sub_multiplicator",
        toggle_sub_multiplicator,
        name="toggle_sub_multiplicator",
    ),
    path(
        "toggle_tip_multiplicator",
        toggle_tip_multiplicator,
        name="toggle_tip_multiplicator",
    ),
    path("tip_progress", tip_progress, name="tip_progress"),
    path("sub_progress", sub_progress, name="sub_progress"),
    path("pause_timer", pause_timer, name="pause_timer"),
    path("global_timer", global_timer, name="global_timer"),
    path("list_participants/", list_participants, name="list_participants"),
    path(
        "subanniversary_summary/", subannivesary_summary, name="subanniversary_summary"
    ),
    path("carousel_announcement/", carousel_announcement, name="carousel_announcement"),
    path("events/", sse_stream, name="sse_stream"),
]
