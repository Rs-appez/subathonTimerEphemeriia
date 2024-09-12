from django.urls import path, include
from .views import TimerViewSet, index, start_timer, add_time, add_time_success

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'timer', TimerViewSet, basename='timer')

urlpatterns = [
    path('api/', include(router.urls)),
    path('',index, name='index'),
    path('start_timer',start_timer, name='start_timer'),
    path('add_time',add_time, name='add_time'),
    path('add_time_success',add_time_success, name='add_time_success'),
]