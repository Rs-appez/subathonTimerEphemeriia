from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/(?P<group_name>\w+)/$", consumers.TicksSyncConsumer.as_asgi()),
]
