import logging
from typing import Any

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings
from django.utils import timezone

from rooms.async_db import (
    async_get_users_in_room, async_get_beers_in_room,
    async_get_user_form_data, async_bump_users_last_active_field,
    async_save_user_form, async_get_current_room,
    async_change_room_state_to, async_get_final_beers_ratings,
    async_get_final_user_beer_ratings
)

logger = logging.getLogger('rooms.consumers.room')


class RoomConsumer(AsyncJsonWebsocketConsumer):
    room_name: str
    room_group_name: str
    private_group_name: str

    commands = {
        # two sided actions: client -> server -> client
        'get_new_message': 'get_new_message',
        'get_users': 'get_users',
        'get_beers': 'get_beers',
        'load_beers': 'load_beers',
        'get_final_ratings': 'get_final_ratings',
        # one sided actions: client -> server
        'user_active': 'user_active',
        'get_room_state': 'get_room_state',
        'change_room_state': 'change_room_state',
    }

    private_commands = {
        # two sided actions: client -> server -> client
        'get_form_data': 'get_form_data',
        'get_user_ratings': 'get_user_ratings',
        # one sided actions: client -> server
        'user_form_save': 'user_form_save',
    }

    async def connect(self):
        if not (current_user := self.scope.get('user')) or current_user.is_anonymous:
            return

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name

        self.private_group_name = f"room_user_{current_user.username}"

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

        # get room state
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'get_room_state'},
        )

    async def receive_json(self, content: dict, **kwargs: Any):
        data_content = content.get('data')

        if settings.DEBUG:
            print(f"\nReceived:\n{content}\nFrom: {self.scope.get('user')}")

        if not (command := content.get('command')):
            return

        if command in self.private_commands:
            await self.channel_layer.group_send(
                self.private_group_name,
                {
                    'type': self.private_commands[command],
                    'data': data_content,
                }
            )
        else:
            if command == "get_new_message":
                data_content = {
                    'message': content.get('data'),
                    'user': str(self.scope.get('user')),
                }

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': self.commands.get(command, 'invalid_command'),
                    'data': data_content,
                }
            )

    async def disconnect(self, code):
        if not self.scope.get('user'):
            return

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
    - load_beers
    - get_form_data
    - user_active
    - user_form_save
    - get_room_state
    - change_room_state
    - get_final_ratings
    - get_user_ratings
    - invalid_command
    """

    async def get_new_message(self, event: dict):
        """
        Receive message => Broadcast it to others and update client
        'get_new_message' => 'set_new_message'
        """
        content: dict = event.get('data')

        await self.send_json(
            {
                'data': content,
                'command': 'set_new_message',
                'timestamp': timezone.now().isoformat()
            }
        )

    async def get_users(self, event: dict):
        """
        Receive get_users command => Broadcast list of users and update client
        'get_users' => 'set_users'
        """
        users = await async_get_users_in_room(room_name=self.room_name)
        await self.send_json(
            {
                'data': users,
                'command': 'set_users',
                'timestamp': timezone.now().isoformat()
            }
        )

    async def get_beers(self, event: dict):
        beers = await async_get_beers_in_room(room_name=self.room_name)
        await self.send_json(
            {
                'data': beers,
                'command': 'set_beers',
                'timestamp': timezone.now().isoformat()
            }
        )

    async def load_beers(self, event: dict):
        beers = await async_get_beers_in_room(room_name=self.room_name)
        await self.send_json(
            {
                'data': beers,
                'command': 'set_beers',
                'timestamp': timezone.now().isoformat()
            }
        )

    async def get_form_data(self, event: dict):
        beer_id = event.get('data')
        form_data = await async_get_user_form_data(
            room_name=self.room_name,
            user=self.scope['user'],
            beer_id=beer_id
        )
        await self.send_json(
            {
                'command': 'set_form_data',
                'data': form_data,
                'timestamp': timezone.now().isoformat(),
                'beer_id': beer_id
            }
        )

    async def user_active(self, event: dict):
        """
        Client reports that they are active by sending command 'user_active'
        Server updates last_active field.
        """
        user = self.scope['user']
        await async_bump_users_last_active_field(room_name=self.room_name, user=user)

    async def user_form_save(self, event: dict):
        user = self.scope['user']
        received_data = event.get('data')
        beer_id = received_data.get('beer_id')
        await async_save_user_form(
            room_name=self.room_name, user=user,
            beer_id=beer_id, data=received_data
        )

    async def get_room_state(self, event: dict):
        room = await async_get_current_room(room_name=self.room_name)
        await self.send_json(
            {
                'command': 'set_room_state',
                'data': room,
                'timestamp': timezone.now().isoformat()
            }
        )

    async def change_room_state(self, event: dict):
        state = event.get('data')
        updated_room = await async_change_room_state_to(state=state, room_name=self.room_name)
        await self.send_json(
            {
                'command': 'set_room_state',
                'data': updated_room,
                'timestamp': timezone.now().isoformat()
            }
        )

    async def get_final_ratings(self, event: dict):
        final = await async_get_final_beers_ratings(room_name=self.room_name)
        await self.send_json(
            {
                'command': 'set_final_results',
                'data': final,
                'timestamp': timezone.now().isoformat()
            }
        )

    async def get_user_ratings(self, event: dict):
        user = self.scope['user']
        final = await async_get_final_user_beer_ratings(room_name=self.room_name, user=user)
        await self.send_json(
            {
                'command': 'set_user_results',
                'data': final,
                'timestamp': timezone.now().isoformat()
            }
        )

    async def invalid_command(self, event: dict):
        if settings.DEBUG:
            print(f'Received an invalid command!\n')
