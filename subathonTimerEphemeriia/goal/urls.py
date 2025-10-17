from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views_api import CampaignViewSet, GoalViewSet
from . import views as v

router = DefaultRouter()
router.register(r"campaigns", CampaignViewSet, basename="campaign")
router.register(r"goals", GoalViewSet, basename="goal")

urlpatterns = [
    path("api/", include(router.urls)),
    path("progress/<int:campaign_id>/", v.campaign_progress, name="campaign_progress"),
]
