from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BotViewSet

router = DefaultRouter()
router.register(r'bot', BotViewSet, basename='bot')

urlpatterns = [
    path('api/', include(router.urls)),
]
