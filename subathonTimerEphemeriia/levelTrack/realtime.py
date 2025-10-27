import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import LevelTracker
from .serializers import LevelTrackerSerializer


def update_level(level: LevelTracker) -> None:
    """
    Send a ticket to update the level.
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"level_{level.id}",
        {
            "type": "new_ticks",
            "content": json.dumps(
                {
                    "type": "level_update",
                    "level": LevelTrackerSerializer(level).data,
                }
            ),
        },
    )
