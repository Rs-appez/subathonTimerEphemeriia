from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import index, admin, create_calendar, edit_calendar
from .views_api import CalendarViewSet, RewardViewSet, CellViewSet

router = DefaultRouter()

router.register(r"calendar", CalendarViewSet, basename="calendar")
router.register(r"reward", RewardViewSet, basename="reward")
router.register(r"cell", CellViewSet, basename="cell")

urlpatterns = [
    path("api/", include(router.urls)),
    path("", index, name="index"),
    path("admin/", admin, name="admin"),
    path("admin/<int:calendar_id>/", edit_calendar, name="admin_arg"),
    path("admin/create/", create_calendar, name="create_calendar"),
]
