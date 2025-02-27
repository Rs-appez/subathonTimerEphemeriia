from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer


class TicksSyncConsumer(SyncConsumer):
    def __get_group_name(self):
        return self.scope["url_route"]["kwargs"]["group_name"]

    def websocket_connect(self, event):
        self.send({"type": "websocket.accept"})

        # Join ticks group
        async_to_sync(self.channel_layer.group_add)(
            self.__get_group_name(), self.channel_name
        )

    def websocket_disconnect(self, event):
        # Leave ticks group
        async_to_sync(self.channel_layer.group_discard)(
            self.__get_group_name(), self.channel_name
        )

    def new_ticks(self, event):
        self.send(
            {
                "type": "websocket.send",
                "text": event["content"],
            }
        )
