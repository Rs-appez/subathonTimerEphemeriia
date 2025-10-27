from django.urls import path

from . import views as v

urlpatterns = [
    path("<int:id>/", v.index, name="bar_tracker"),
    path("admin/<int:id>/", v.admin_view, name="bar_tracker_admin"),
]
