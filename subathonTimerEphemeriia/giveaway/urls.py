from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views, views_api, views_partial

router = DefaultRouter()

router.register(r"calendar", views_api.CalendarViewSet, basename="calendar")
router.register(r"reward", views_api.RewardViewSet, basename="reward")
router.register(r"base_cell", views_api.CellViewSet, basename="base_cell")
router.register(
    r"base_calendar", views_api.BaseCalendarViewSet, basename="base_calendar"
)
router.register(r"cell", views_api.CalendarCellViewSet, basename="cell")

app_name = "giveaway"

urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.index, name="index"),
    path("admin/", views.admin, name="calendar_admin"),
    path("admin/<int:calendar_id>/", views.edit_calendar, name="calendar_admin_arg"),
    path(
        "admin/shuffle_rewards/<int:calendar_id>/",
        views_partial.shuffle_rewards,
        name="shuffle_rewards",
    ),
    path(
        "admin/close_all_cells/<int:calendar_id>/",
        views_partial.close_all_cells,
        name="close_all_cells",
    ),
    path(
        "admin/<int:calendar_id>/activate/",
        views.activate_calendar,
        name="activate_calendar",
    ),
    path(
        "admin/<int:calendar_id>/deactivate/",
        views.deactivate_calendar,
        name="deactivate_calendar",
    ),
    path(
        "admin/<int:calendar_id>/delete/",
        views.delete_calendar,
        name="delete_calendar",
    ),
    path("admin/create/", views.create_calendar, name="create_calendar"),
    path("admin/rewards/create/", views.create_reward, name="create_reward"),
]
