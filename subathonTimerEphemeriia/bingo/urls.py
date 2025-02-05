from django.urls import path, include

from .views import activate_bingo, index, admin, activate_item, admin_bingo, reset_bingo
from .views_api import BingoViewSet, BingoItemViewSet, BingoItemUserViewSet, UserViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"bingo", BingoViewSet, basename="bingo")
router.register(r"bingo_item", BingoItemViewSet, basename="bingo_item")
router.register(r"bingo_item_user", BingoItemUserViewSet, basename="bingo_item_user")
router.register(r"user", UserViewSet, basename="user")

urlpatterns = [
    path("api/", include(router.urls)),
    path("", index, name="index"),
    path("reset/<int:bingo_id>/", reset_bingo, name="reset_bingo"),
    path("activate/<int:bingo_id>/", activate_bingo, name="activate_bingo"),
    path("admin/", admin, name="admin"),
    path("admin/bingo/", admin_bingo, name="admin_bingo"),
    path("admin/<int:bingo_id>/", admin, name="admin_arg"),
    path(
        "admin/<int:bingo_id>/activate/<int:item_id>/",
        activate_item,
        name="activate_item",
    ),
]
