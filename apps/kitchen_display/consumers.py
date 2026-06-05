import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import KitchenOrder

class KitchenConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group = 'kitchen_updates'
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        order_id = data.get('order_id')
        if action == 'update_status':
            # Update DB (synchronous in real use)
            await self.channel_layer.group_send(
                self.group, {'type': 'order_status', 'order_id': order_id, 'status': data['status']}
            )

    async def order_status(self, event):
        await self.send(text_data=json.dumps({
            'order_id': event['order_id'],
            'status': event['status']
        }))