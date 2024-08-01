from django.urls import path, include
from .views import TimerViewSet, index

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('timer', TimerViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('',index, name='index'),
]