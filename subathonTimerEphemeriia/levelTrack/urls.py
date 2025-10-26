from django.urls import path, include

from . import views as v

urlpatterns = [path("<int:id>/", v.index, name="bar_tracker")]
