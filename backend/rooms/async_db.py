from datetime import timedelta

from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from beers.serializers import BeerSerializer
from rooms.models import Room, UserInRoom, BeerInRoom, Rating
from rooms.serializers import RatingSerializer
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
def save_user_form(room_name: str, user: User, beer_id: str, data):
    if user.is_anonymous or not beer_id or not data:
        return

    try:
        user_room = BeerInRoom.objects.get(room__name=room_name, beer__id=beer_id)
        rating = user_room.ratings.filter(added_by=user)

        clean_data = data
        clean_data.pop('beer_id', None)

        # if no note was chosen, it might be an empty string
        # if it happens to be string somehow, turn it into int
        if isinstance(clean_data['note'], str):
            try:
                clean_data['note'] = int(clean_data['note'])
            except ValueError:
                clean_data['note'] = None

        # Create new rating if one does not exist
        if not rating.exists():
            # Add added_by field to the dictionary, from which Rating instance will be created
            clean_data['added_by'] = user
            new_rating = Rating.objects.create(**clean_data)
            # add rating to m2m field
            user_room.ratings.add(new_rating)
            return RatingSerializer(new_rating).data

        # If rating exists, update it with received data
        rating.update(**clean_data)

        return RatingSerializer(instance=rating.first()).data

    except ObjectDoesNotExist:
        return


@database_sync_to_async
def get_user_form_data(room_name: str, user: User, beer_id: str):
    if user.is_anonymous or not beer_id:
        return

    try:
        beer_room = BeerInRoom.objects.get(room__name=room_name, beer__id=beer_id)
        rating = beer_room.ratings.filter(added_by=user)

        if not rating.exists():
            new_rating = Rating.objects.create(
                added_by=user
            )
            beer_room.ratings.add(new_rating)
            return RatingSerializer(new_rating).data
        return RatingSerializer(rating.first()).data

    except ObjectDoesNotExist:
        return


@database_sync_to_async
def get_beers_in_room(room_name: str):
    try:
        room = Room.objects.get(name=room_name)
        beers = room.beers.all()
        serialized = BeerSerializer(beers, many=True).data
        return serialized
    except ObjectDoesNotExist:
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
