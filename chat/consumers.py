import json

from channels.generic.websocket import AsyncWebsocketConsumer # The class we're using
from asgiref.sync import sync_to_async # Implement later
# Import the user model
from user.models import Users

# Import the Message model
from .models import Room, Message
# Create a consumer class
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room based on name in the URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user_id = data['user_id']
        room = data['room']
        
        await self.save_message(user_id, room, message)
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id
        }))
    # Add a new method to the class
    @sync_to_async
    def save_message(self, user_id, room, message):
        user = Users.objects.get(pk=user_id)
        room = Room.objects.get(slug=room)

        Message.objects.create(user=user, room=room, content=message)