import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AppointmentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.stylist_id = self.scope['url_route']['kwargs'].get('stylist_id')
        self.salon_id = self.scope['url_route']['kwargs'].get('salon_id')

        if self.stylist_id:
            self.group_name = f'stylist_{self.stylist_id}'
        elif self.salon_id:
            self.group_name = f'salon_{self.salon_id}'
        else:
            await self.close()
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass  # Not expecting to receive from client

    async def appointment_update(self, event):
        await self.send(text_data=json.dumps(event['data']))
