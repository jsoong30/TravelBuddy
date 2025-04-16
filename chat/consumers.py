import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get room_slug from the URL route:
        self.room_slug = self.scope['url_route']['kwargs']['room_slug']
        # Create a group name using the room slug:
        self.room_group_name = f'chat_{self.room_slug}'

        # Join the group:
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # Accept the WebSocket connection:
        await self.accept()
        print(f"[CONNECT] {self.channel_name} connected to group {self.room_group_name}")

    async def disconnect(self, close_code):
        # Leave the group:
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"[DISCONNECT] {self.channel_name} disconnected from group {self.room_group_name}")

    async def receive(self, text_data):
        # Log and process incoming messages:
        print(f"[RECEIVE] {self.channel_name} received: {text_data}")
        try:
            data = json.loads(text_data)
            message = data.get('message', '')
        except Exception as e:
            print("[ERROR] Unable to parse message:", e)
            return

        # Broadcast the message to the group:
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',  # This will call the chat_message method below
                'message': message,
            }
        )
        print(f"[GROUP SEND] Message broadcasted to group {self.room_group_name}")

    async def chat_message(self, event):
        # Receive message from group:
        message = event['message']
        # Send message to WebSocket:
        await self.send(text_data=json.dumps({
            'message': message
        }))
        print(f"[SEND] Sent message: {message} to {self.channel_name}")
