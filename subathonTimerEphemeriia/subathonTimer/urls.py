from django.urls import path, include
from .views import TimerViewSet, index, start_timer

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'timer', TimerViewSet, basename='timer')

urlpatterns = [
    path('api/', include(router.urls)),
    path('',index, name='index'),
    path('start_timer',start_timer, name='start_timer'),
]