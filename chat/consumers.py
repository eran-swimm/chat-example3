import logging
import json
from channels.generic.websocket import AsyncWebsocketConsumer


logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']
        logger.info(
            'Connect room_name=%s channel_name=%s user=%s',
            self.room_name,
            self.channel_name,
            self.scope['user'])
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': {
                    'id': self.user.id,
                    'full_name': self.user.get_full_name(),
                    'short_name': self.user.get_short_name(),
                }
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = '{}: {}'.format(event['user']['short_name'], event['message'])
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
