from channels.db import database_sync_to_async
from django.contrib.auth.models import User

from rooms.models import Room
from users.serializers import UserSerializer


@database_sync_to_async
def get_users_in_room(room_name: str):
    try:
        room = Room.objects.get(name=room_name)
        serialized = UserSerializer(room.users.all(), many=True).data
        return serialized
    except Room.DoesNotExist:
        return []


@database_sync_to_async
def join_room(room_name: str, user: User):
    try:
        room = Room.objects.get(name=room_name)
        participants = room.users
        if not participants.filter(id=user.id).exists():
            participants.add(user)
    except Room.DoesNotExist:
        pass


@database_sync_to_async
def leave_room(room_name: str, user: User):
    if user.is_anonymous:
        return
    try:
        room = Room.objects.get(room=room_name)
        participants = room.users
        if participants.filter(id=user.id).exists():
            participants.remove(user)
    except Room.DoesNotExist:
        return
