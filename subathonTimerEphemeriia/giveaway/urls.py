from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views_api import CalendarViewSet, RewardViewSet, CellViewSet

router = DefaultRouter()

router.register(r"calendar", CalendarViewSet, basename="calendar")
router.register(r"reward", RewardViewSet, basename="reward")
router.register(r"cell", CellViewSet, basename="cell")

urlpatterns = [
    path("api/", include(router.urls)),
]
