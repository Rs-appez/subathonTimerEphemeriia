from django.urls import path, include

from .views import index, admin, activate_item, admin_bingo
from .views import BingoViewSet, BingoItemViewSet, BingoItemUserViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'bingo', BingoViewSet, basename='bingo')
router.register(r'bingo_item', BingoItemViewSet, basename='bingo_item')
router.register(r'bingo_item_user', BingoItemUserViewSet, basename='bingo_item_user')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', index, name='index'),
    path('admin/', admin, name='admin'),
    path('admin/bingo/', admin_bingo, name='admin_bingo'),
    path('admin/<int:bingo_id>/', admin, name='admin_arg'),
    path('admin/<int:bingo_id>/activate/<int:item_id>/', activate_item, name='activate_item'),

]