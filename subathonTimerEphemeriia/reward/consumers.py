from django.conf import settings
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer


class RewardSyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.send({"type": "websocket.accept"})

        # Join ticks group
        async_to_sync(self.channel_layer.group_add)(
            settings.REWARD_GROUP_NAME, self.channel_name
        )

    def websocket_disconnect(self, event):
        # Leave ticks group
        async_to_sync(self.channel_layer.group_discard)(
            settings.REWARD_GROUP_NAME, self.channel_name
        )

    def new_ticks(self, event):
        self.send(
            {
                "type": "websocket.send",
                "text": event["content"],
            }
        )
