import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ChatRoom, ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_slug = self.scope['url_route']['kwargs']['room_slug']
        self.room_group_name = f'chat_{self.room_slug}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is not None:
            print(f"[RECEIVE] {self.channel_name} received: {text_data}")
            try:
                data = json.loads(text_data)
                message = data.get('message', '')
            except Exception as e:
                print("[ERROR] Unable to parse text data:", e)
                return

            # Determine username from scope
            user = self.scope['user']
            username = user.username if user.is_authenticated else 'Anonymous'

            # Save message to the database (asynchronously)
            # Broadcast message to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'username': username,
                    'message': message,
                }
            )
            print(f"[GROUP SEND] Message broadcasted to group {self.room_group_name}")

    async def chat_message(self, event):
        # Send the username and message to WebSocket
        await self.send(text_data=json.dumps({
            'username': event['username'],
            'message': event['message'],
        }))
