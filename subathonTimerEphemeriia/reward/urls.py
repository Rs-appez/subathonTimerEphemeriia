from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views, views_api

router = DefaultRouter()

router.register(r"rewards", views_api.RewardViewSet, basename="reward")

urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.index, name="index"),
]
