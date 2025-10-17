from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views_api import CampaignViewSet, GoalViewSet

router = DefaultRouter()
router.register(r"campaigns", CampaignViewSet, basename="campaign")
router.register(r"goals", GoalViewSet, basename="goal")

urlpatterns = [
    path("api/", include(router.urls)),
]
