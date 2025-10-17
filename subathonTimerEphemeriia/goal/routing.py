from django.urls import re_path
from .consumers import GoalSyncConsumer

websocket_urlpatterns = [
    re_path(r"ws/goal/$", GoalSyncConsumer.as_asgi()),
]
