from django.db import models

from asgiref.sync import async_to_sync
import channels.layers
import json

from django.conf import settings


class Reward(models.Model):
    reward_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def send_ticket(self):
        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            settings.REWARD_GROUP_NAME,
            {
                "type": "new_ticks",
                "content": json.dumps(
                    {
                        "name": self.name,
                    }
                ),
            },
        )
