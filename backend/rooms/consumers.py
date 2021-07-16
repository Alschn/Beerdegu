import json

from channels.generic.websocket import AsyncWebsocketConsumer

from rooms.async_db import (
    get_users_in_room, bump_users_last_active_field,
    leave_room
)


class RoomConsumer(AsyncWebsocketConsumer):
    room_name: str
    room_group_name: str

    commands = {
        # two sided actions
        'get_new_message': 'get_new_message',
        'get_users': 'get_users',
        # one sided actions
        'user_active': 'user_active'
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
        command = data.get('command')

        print(f"Received:\n{data}\nFrom: {self.scope.get('user')}")

        if not command:
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': self.commands.get(command, 'invalid_command'),
                'message': data.get('message'),
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
    
    - get_users
    - user_active
    
    - invalid_command
    """

    async def get_new_message(self, event):
        """
        Receive message => Broadcast it to others and update client
        'get_new_message' => 'set_new_message'
        """
        str_message: str = event['message']

        await self.send(text_data=json.dumps({
            'data': str_message,
            'command': 'set_new_message'
        }))

    async def get_users(self, event):
        """
        Receive get_users command => Broadcast list of users and update client
        'get_users' => 'set_users'
        """
        users = await get_users_in_room(room_name=self.room_name)
        await self.send(text_data=json.dumps({
            'data': users,
            'command': 'set_users',
        }))

    async def user_active(self, event):
        """
        Client reports that they are active by sending command 'user_active'
        Server updates last_active field.
        """
        user = self.scope['user']
        await bump_users_last_active_field(room_name=self.room_name, user=user)

    async def user_leave_room(self, event):
        # check if it works later
        user = self.scope['user']
        await leave_room(
            room_name=self.room_name,
            user=user
        )
        users = await get_users_in_room(room_name=self.room_name)
        await self.send(text_data=json.dumps({
            'data': users,
            'message': f'{user.username} has left the room',
            'command': 'set_users',
        }))

    async def invalid_command(self, event):
        pass
