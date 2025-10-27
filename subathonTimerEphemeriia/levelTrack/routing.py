from django.urls import re_path
from .consumers import LevelSyncConsumer

websocket_urlpatterns = [
    re_path(r"ws/levelTrackers/(?P<tracker_id>\w+)/?$", LevelSyncConsumer.as_asgi()),
]
