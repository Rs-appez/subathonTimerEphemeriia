from django.urls import path, include

from .views import index, admin, BingoViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'bingo', BingoViewSet, basename='bingo')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', index, name='index'),
    path('admin/', admin, name='admin'),
    path('admin/<int:bingo_id>/', admin, name='admin_arg'),
]