from django.urls import re_path
from .consumers import CampaignSyncConsumer

websocket_urlpatterns = [
    re_path(r"ws/campaigns/(?P<campaign_id>\w+)/?$", CampaignSyncConsumer.as_asgi()),
]
