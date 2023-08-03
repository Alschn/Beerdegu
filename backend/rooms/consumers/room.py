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

logger = logging.getLogger(__name__)


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
        'user_leave': 'user_leave',
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
            # reject unauthenticated users
            await self.close()
            return

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_%s' % self.room_name

        self.private_group_name = f'room_user_{current_user.username}'

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

        # notify others that current user joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'user_join', 'data': current_user.username},
        )

        # fetch users in room on join
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'get_users'},
        )

        # get room state on join
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'get_room_state'},
        )

    async def receive_json(self, content: dict, **kwargs: Any):
        user = self.scope['user']
        command = content.get('command')
        data_content = content.get('data')

        if settings.DEBUG:
            print(f'\nReceived:\n{content}\nFrom: {user}')

        if not command:
            return

        if command in self.private_commands:
            await self.channel_layer.group_send(
                self.private_group_name,
                {
                    'type': self.private_commands[command],
                    'data': data_content,
                }
            )
        elif command in self.commands:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': self.commands[command],
                    'data': data_content,
                }
            )
        else:
            await self.invalid_command()

        await async_bump_users_last_active_field(
            room_name=self.room_name,
            user=user
        )

    async def disconnect(self, code: int):
        user = self.scope['user']
        if user.is_anonymous:
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'user_disconnect', 'data': user.username},
        )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_discard(
            self.private_group_name,
            self.channel_name
        )

    async def send_json(self, content: dict, close: bool = False):
        content = {
            'timestamp': timezone.now().isoformat(),
            **content
        }
        await super().send_json(content, close=close)

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
    - user_join
    - user_disconnect
    - user_leave
    - invalid_command
    """

    async def get_new_message(self, event: dict):
        """
        Receive message => Broadcast it to others and update client
        'get_new_message' => 'set_new_message'
        """
        user = self.scope['user']
        message = event.get('data')
        content = {
            'message': message,
            'user': str(user),
        }
        await self.send_json(
            {
                'command': 'set_new_message',
                'data': content,
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
                'command': 'set_users',
                'data': users,
            }
        )

    async def get_beers(self, event: dict):
        beers = await async_get_beers_in_room(room_name=self.room_name)
        await self.send_json(
            {
                'command': 'set_beers',
                'data': beers,
            }
        )

    async def load_beers(self, event: dict):
        """Alias for `get_beers` command handler."""

        await self.get_beers(event)

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
                'beer_id': beer_id
            }
        )

    async def user_active(self, event: dict):
        """
        Client reports that they are active by sending command 'user_active'
        Server updates last_active field.
        """
        user = self.scope['user']
        await async_bump_users_last_active_field(
            room_name=self.room_name,
            user=user
        )

    async def user_form_save(self, event: dict):
        user = self.scope['user']
        received_data = event.get('data')
        beer_id = received_data.get('beer_id')
        await async_save_user_form(
            room_name=self.room_name,
            user=user,
            beer_id=beer_id,
            data=received_data
        )

    async def get_room_state(self, event: dict):
        room = await async_get_current_room(room_name=self.room_name)
        await self.send_json(
            {
                'command': 'set_room_state',
                'data': room,
            }
        )

    async def change_room_state(self, event: dict):
        state = event.get('data')
        updated_room = await async_change_room_state_to(state=state, room_name=self.room_name)
        await self.send_json(
            {
                'command': 'set_room_state',
                'data': updated_room,
            }
        )

    async def get_final_ratings(self, event: dict):
        final = await async_get_final_beers_ratings(room_name=self.room_name)
        await self.send_json(
            {
                'command': 'set_final_results',
                'data': final,
            }
        )

    async def get_user_ratings(self, event: dict):
        user = self.scope['user']
        final = await async_get_final_user_beer_ratings(room_name=self.room_name, user=user)
        await self.send_json(
            {
                'command': 'set_user_results',
                'data': final,
            }
        )

    async def user_join(self, event: dict):
        """Server action to notify others that new user joined"""

        user = self.scope['user']
        username = event.get('data')
        if user.username == username:
            return

        await self.send_json(
            {
                'command': 'user_join',
                'data': username,
            }
        )

    async def user_leave(self, event: dict):
        user = self.scope['user']
        username = event.get('data')
        if user.username == username:
            return

        await self.send_json(
            {
                'command': 'user_leave',
                'data': username,
            }
        )

    async def user_disconnect(self, event: dict):
        user = self.scope['user']
        username = event.get('data')
        if user.username == username:
            return

        await self.send_json(
            {
                'command': 'user_disconnect',
                'data': username,
            }
        )

    async def invalid_command(self, *args, **kwargs):
        if settings.DEBUG:
            print(f'Received an invalid command!\n')
