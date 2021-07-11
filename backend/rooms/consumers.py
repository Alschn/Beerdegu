import json
from channels.generic.websocket import AsyncWebsocketConsumer


class RoomConsumer(AsyncWebsocketConsumer):
    room_name: str
    room_group_name: str

    commands = {
        'get_new_message': 'get_new_message',
    }

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)  # parsed object

        print(f"Received:\n{data}")

        if not data.get('command'):
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': self.commands.get(data.command, 'invalid_command'),
                'message': data.message,
            }
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    """
    Event handlers:
    - get_new_message
    - invalid_command
    """

    async def get_new_message(self, event):
        """
        Receive message -> Broadcast it to others and update client
        'get_new_message' -> 'set_new_message'
        """
        str_message: str = event['message']

        await self.send(text_data=json.dumps({
            'data': str_message,
            'command': 'set_new_message'
        }))

    async def invalid_command(self, event):
        pass
