import json

from channels.generic.websocket import AsyncWebsocketConsumer

from rooms.async_db import (
    get_users_in_room, bump_users_last_active_field,
    leave_room, save_user_form, get_beers_in_room, get_user_form_data,
)


class RoomConsumer(AsyncWebsocketConsumer):
    room_name: str
    room_group_name: str
    private_group_name: str

    commands = {
        # two sided actions: client -> server -> client
        'get_new_message': 'get_new_message',
        'get_users': 'get_users',
        'get_beers': 'get_beers',
        # one sided actions: client -> server
        'user_active': 'user_active',
    }

    private_commands = {
        # two sided actions: client -> server -> client
        'get_form_data': 'get_form_data',
        # one sided actions: client -> server
        'user_form_save': 'user_form_save',
    }

    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name

        self.private_group_name = f"room_user_{self.scope['user'].username}"

        # public room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # private room - user specific
        await self.channel_layer.group_add(
            self.private_group_name,
            self.channel_name
        )

        await self.accept()

        # fetch users in room on join
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'get_users'},
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)  # parsed object
        command = data.get('command')

        print(f"Received:\n{data}\nFrom: {self.scope.get('user')}")

        if not command:
            return

        if command in self.private_commands:
            await self.channel_layer.group_send(
                self.private_group_name,
                {
                    'type': self.private_commands[command],
                    'data': data.get('data'),
                }
            )
        else:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': self.commands.get(command, 'invalid_command'),
                    'data': data.get('data'),
                }
            )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_discard(
            self.private_group_name,
            self.channel_name
        )

    """
    Event handlers:
    - get_new_message
    - get_users
    - get_beers
    - get_form_data
    
    - user_active
    - user_form_save
    
    - invalid_command
    """

    async def get_new_message(self, event):
        """
        Receive message => Broadcast it to others and update client
        'get_new_message' => 'set_new_message'
        """
        str_message: str = event['data']

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

    async def get_beers(self, event):
        beers = await get_beers_in_room(room_name=self.room_name)
        await self.send(text_data=json.dumps({
            'data': beers,
            'command': 'set_beers'
        }))

    async def get_form_data(self, event):
        beer_id = event.get('data')
        form_data = await get_user_form_data(
            room_name=self.room_name,
            user=self.scope['user'],
            beer_id=beer_id
        )
        await self.send(text_data=json.dumps({
            'command': 'set_form_data',
            'data': form_data,
        }))

    async def user_active(self, event):
        """
        Client reports that they are active by sending command 'user_active'
        Server updates last_active field.
        """
        user = self.scope['user']
        await bump_users_last_active_field(room_name=self.room_name, user=user)

    async def user_form_save(self, event):
        user = self.scope['user']
        received_data = event.get('data')
        beer_id = received_data.get('beer_id')
        await save_user_form(
            room_name=self.room_name, user=user,
            beer_id=beer_id, data=received_data
        )

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
