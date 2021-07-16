from datetime import timedelta

from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from rooms.models import Room, UserInRoom
from users.serializers import UserSerializer


@database_sync_to_async
def get_users_in_room(room_name: str):
    try:
        room = Room.objects.get(name=room_name)

        # filter m2m intersection table to find inactive records (UserInRoom instance)
        user_room = UserInRoom.objects.filter(
            room=room, last_active__lt=timezone.now() - timedelta(minutes=1)
        )

        if user_room.count() != 0:
            # get user column only from query set
            users_to_remove = user_room.values_list('user', flat=True)
            # unpack it and remove each element
            room.users.remove(*users_to_remove)

        # users have been updated, only active users are inside the room now
        active_users = room.users.all()
        serialized = UserSerializer(active_users, many=True).data
        return serialized
    except Room.DoesNotExist:
        return []


@database_sync_to_async
def bump_users_last_active_field(room_name: str, user: User):
    if user.is_anonymous:
        return

    try:
        room = Room.objects.get(name=room_name)
        user_room = UserInRoom.objects.get(room=room, user=user)
        user_room.last_active = timezone.now()
        user_room.save()

    except ObjectDoesNotExist:
        return


@database_sync_to_async
def save_user_form(room_name: str, user: User):
    if user.is_anonymous:
        return
    # to do


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
