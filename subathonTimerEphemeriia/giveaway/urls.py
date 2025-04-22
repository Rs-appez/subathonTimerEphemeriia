from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import index, admin, create_calendar, edit_calendar
from .views_api import CalendarViewSet, RewardViewSet, CellViewSet, BaseCalendarViewSet, CalendarCellViewSet

router = DefaultRouter()

router.register(r"calendar", CalendarViewSet, basename="calendar")
router.register(r"reward", RewardViewSet, basename="reward")
router.register(r"base_cell", CellViewSet, basename="base_cell")
router.register(r"base_calendar", BaseCalendarViewSet, basename="base_calendar")
router.register(r"cell", CalendarCellViewSet, basename="cell")

urlpatterns = [
    path("api/", include(router.urls)),
    path("", index, name="index"),
    path("admin/", admin, name="admin"),
    path("admin/<int:calendar_id>/", edit_calendar, name="admin_arg"),
    path("admin/create/", create_calendar, name="create_calendar"),
]
