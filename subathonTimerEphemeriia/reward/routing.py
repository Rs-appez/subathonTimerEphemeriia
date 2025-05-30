from django.urls import re_path
from .consumers import RewardSyncConsumer

websocket_urlpatterns = [
    re_path(r"ws/reward/$", RewardSyncConsumer.as_asgi()),
]
