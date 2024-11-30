from channels.generic.websocket import AsyncWebsocketConsumer
import json
from urllib.parse import parse_qs


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope["query_string"])
        query_string = parse_qs(self.scope["query_string"].decode())
        self.tenant_name = query_string.get("tenant_name")[0]
        print(self.tenant_name)
        # self.tenant_name = self.scope["tenant_name"]
        self.group_name = f"group_{self.tenant_name}"
        # print(self.group_name)

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print(message)

        await self.channel_layer.group_send(
            self.group_name, {"type": "notify", "message": message}
        )

    async def notify(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
