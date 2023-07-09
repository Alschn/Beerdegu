from datetime import timedelta

from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import F, QuerySet
from django.db.models.aggregates import Avg
from django.db.models.fields import DecimalField
from django.utils import timezone

from beers.serializers import BeerRepresentationalSerializer, BeerWithResultsSerializer
from rooms.models import Room, UserInRoom, BeerInRoom, Rating
from rooms.serializers import RatingSerializer, RoomSerializer
from users.serializers.user import UserSerializer

INACTIVE_TIMEOUT_SECONDS = 60


def filter_inactive_users_in_room(room: Room) -> QuerySet[UserInRoom]:
    return UserInRoom.objects.filter(
        last_active__lte=timezone.now() - timedelta(seconds=INACTIVE_TIMEOUT_SECONDS),
        room=room
    )


def try_remove_inactive_users_in_room(room: Room) -> None:
    inactive_users_in_room = filter_inactive_users_in_room(room)
    if not inactive_users_in_room.exists():
        return

    users_to_remove = inactive_users_in_room.values_list('user', flat=True)
    room.users.remove(*users_to_remove)


@transaction.atomic
def get_users_in_room(room_name: str):
    try:
        room = Room.objects.get(name=room_name)
    except Room.DoesNotExist:
        return []

    try_remove_inactive_users_in_room(room)

    # users have been updated, only active users are inside the room now
    active_users = room.users.all()
    serialized = UserSerializer(active_users, many=True).data
    return serialized


def bump_users_last_active_field(room_name: str, user: User) -> None:
    if user.is_anonymous:
        return

    try:
        user_room = UserInRoom.objects.get(room__name=room_name, user=user)
    except ObjectDoesNotExist:
        return

    user_room.last_active = timezone.now()
    user_room.save(update_fields=['last_active'])


@transaction.atomic
def save_user_form(room_name: str, user: User, beer_id: str, data: dict):
    if user.is_anonymous or not beer_id or not data:
        return

    try:
        beer_in_room = BeerInRoom.objects.get(room__name=room_name, beer__id=beer_id)
    except ObjectDoesNotExist:
        return

    user_ratings = beer_in_room.ratings.filter(added_by=user)

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
    if not user_ratings.exists():
        # Add added_by field to the dictionary, from which Rating instance will be created
        new_rating = Rating.objects.create(**clean_data, added_by=user)
        # add rating to m2m field
        beer_in_room.ratings.add(new_rating)
        return RatingSerializer(instace=new_rating).data

    # If rating exists, update it with received data
    user_ratings.update(**clean_data)
    rating = user_ratings.first()
    return RatingSerializer(instance=rating).data


def get_user_form_data(room_name: str, user: User, beer_id: str):
    if user.is_anonymous or not beer_id:
        return

    try:
        beer_in_room = BeerInRoom.objects.get(room__name=room_name, beer__id=beer_id)
    except ObjectDoesNotExist:
        return

    ratings = beer_in_room.ratings.filter(added_by=user)
    rating = ratings.first()

    if not rating:
        new_rating = Rating.objects.create(added_by=user)
        beer_in_room.ratings.add(new_rating)
        return RatingSerializer(new_rating).data

    return RatingSerializer(instance=rating).data


def get_beers_in_room(room_name: str):
    try:
        room = Room.objects.get(name=room_name)
    except ObjectDoesNotExist:
        return []

    beers = room.beers.order_by('beerinroom__order')
    serialized = BeerRepresentationalSerializer(beers, many=True).data
    return serialized


def get_current_room(room_name: str):
    try:
        room = Room.objects.get(name=room_name)
    except ObjectDoesNotExist:
        return

    serialized = RoomSerializer(room).data
    return serialized


def change_room_state_to(state: str, room_name: str):
    try:
        room = Room.objects.get(name=room_name)
    except ObjectDoesNotExist:
        return

    serializer = RoomSerializer(instance=room, data={'state': state}, partial=True)
    if not serializer.is_valid(raise_exception=False):
        return RoomSerializer(room).data

    serializer.save()
    return serializer.data


def get_final_user_beer_ratings(room_name: str, user: User):
    if user.is_anonymous:
        return

    ratings = Rating.objects.filter(
        added_by=user,
        belongs_to__room__name=room_name
    ).annotate(
        beer=F('belongs_to__beer')
    ).order_by(
        'belongs_to__order'
    )
    serialized = RatingSerializer(ratings, many=True).data
    return serialized


def get_final_beers_ratings(room_name: str):
    beers_in_room = BeerInRoom.objects.filter(room__name=room_name)
    if not beers_in_room.exists():
        return []

    beers_with_ratings = beers_in_room.annotate(
        average_rating=Avg('ratings__note', output_field=DecimalField())
    ).order_by('order')
    serialized = BeerWithResultsSerializer(beers_with_ratings, many=True).data
    return serialized


async_get_users_in_room = database_sync_to_async(get_users_in_room)
async_bump_users_last_active_field = database_sync_to_async(bump_users_last_active_field)
async_save_user_form = database_sync_to_async(save_user_form)
async_get_user_form_data = database_sync_to_async(get_user_form_data)
async_get_beers_in_room = database_sync_to_async(get_beers_in_room)
async_get_current_room = database_sync_to_async(get_current_room)
async_change_room_state_to = database_sync_to_async(change_room_state_to)
async_get_final_user_beer_ratings = database_sync_to_async(get_final_user_beer_ratings)
async_get_final_beers_ratings = database_sync_to_async(get_final_beers_ratings)
