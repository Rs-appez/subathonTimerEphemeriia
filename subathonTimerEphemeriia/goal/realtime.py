import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from .models import Campaign
from .serializers import CampaignSerializer


def update_campaign(campaign: Campaign) -> None:
    """
    Send a ticket to update the campaign.
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"campaign_{campaign.id}",
        {
            "type": "new_ticks",
            "content": json.dumps(
                {
                    "type": "campaign_update",
                    "campaign": CampaignSerializer(campaign).data,
                }
            ),
        },
    )
