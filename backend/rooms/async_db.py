from datetime import timedelta

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import QuerySet, Subquery, OuterRef
from django.db.models.aggregates import Avg
from django.db.models.fields import FloatField
from django.utils import timezone

from beers.models import Beer
from beers.serializers import BeerRepresentationalSerializer, BeerWithResultsSerializer
from ratings.models import Rating
from ratings.serializers import RatingSerializer
from rooms.models import Room, UserInRoom, BeerInRoom
from rooms.serializers import RoomSerializer
from users.serializers.user import UserSerializer

User = get_user_model()

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
def get_users_in_room(room_name: str) -> list[dict]:
    try:
        room = Room.objects.get(name=room_name)
    except Room.DoesNotExist:
        return []

    try_remove_inactive_users_in_room(room)

    # users have been updated, only active users are inside the room now
    active_users = room.users.all()

    serializer = UserSerializer(active_users, many=True)
    return serializer.data


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
def save_user_form(room_name: str, user: User, beer_id: str, data: dict) -> dict | None:
    if user.is_anonymous or not beer_id or not data:
        return

    user_ratings = Rating.objects.filter(
        added_by=user,
        room__name=room_name,
        beer__id=beer_id
    )

    clean_data = data
    clean_data.pop('beer_id', None)

    # if no note was chosen, it might be an empty string
    # if it happens to be string somehow, turn it into int
    if isinstance(clean_data['note'], str):
        try:
            clean_data['note'] = int(clean_data['note'])
        except ValueError:
            clean_data['note'] = None

    # update existing rating
    if user_ratings.exists():
        user_ratings.update(**clean_data)
        rating = user_ratings.first()
        serializer = RatingSerializer(instance=rating)
        return serializer.data

    try:
        room = Room.objects.get(name=room_name)
        beer = Beer.objects.get(id=beer_id)
    except ObjectDoesNotExist:
        return

    # create new rating if it's missing
    new_rating = Rating.objects.create(
        **clean_data,
        added_by=user,
        room=room,
        beer=beer
    )

    serializer = RatingSerializer(instance=new_rating)
    return serializer.data


def get_user_form_data(room_name: str, user: User, beer_id: str) -> dict | None:
    if user.is_anonymous or not beer_id:
        return

    ratings = Rating.objects.filter(
        added_by=user,
        room__name=room_name,
        beer__id=beer_id
    )
    rating = ratings.first()

    if rating:
        serializer = RatingSerializer(instance=rating)
        return serializer.data

    try:
        beer = Beer.objects.get(id=beer_id)
        room = Room.objects.get(name=room_name)
    except ObjectDoesNotExist:
        return

    new_rating = Rating.objects.create(
        added_by=user,
        beer=beer,
        room=room
    )

    serializer = RatingSerializer(new_rating)
    return serializer.data


def get_beers_in_room(room_name: str) -> list[dict]:
    try:
        room = Room.objects.get(name=room_name)
    except ObjectDoesNotExist:
        return []

    beers = room.beers.order_by('rooms_through__order')
    serializer = BeerRepresentationalSerializer(beers, many=True)
    return serializer.data


def get_current_room(room_name: str) -> dict | None:
    try:
        room = Room.objects.get(name=room_name)
    except ObjectDoesNotExist:
        return

    serializer = RoomSerializer(room)
    return serializer.data


def change_room_state_to(state: str, room_name: str) -> dict | None:
    try:
        room = Room.objects.get(name=room_name)
    except ObjectDoesNotExist:
        return

    serializer = RoomSerializer(instance=room, data={'state': state}, partial=True)
    if not serializer.is_valid(raise_exception=False):
        return RoomSerializer(room).data

    serializer.save()
    return serializer.data


def get_final_user_beer_ratings(room_name: str, user: User) -> list[dict]:
    related_beer_in_room = BeerInRoom.objects.filter(
        room__name=room_name,
        beer=OuterRef('beer')
    )
    ratings = Rating.objects.filter(
        added_by=user,
        room__name=room_name
    ).annotate(
        beer_order=Subquery(
            related_beer_in_room.values('order')[:1]
        ),
    ).order_by('beer_order')

    serializer = RatingSerializer(ratings, many=True)
    return serializer.data


def get_final_beers_ratings(room_name: str):
    beers_in_room = BeerInRoom.objects.filter(room__name=room_name).only('beer', 'room', 'order')
    if not beers_in_room.exists():
        return []

    # find average rating for each beer in the room
    rating_subquery = Rating.objects.filter(
        beer=OuterRef('beer'), room=OuterRef('room')
    ).values('beer', 'room').annotate(
        average_rating=Avg('note', output_field=FloatField()),
    )

    beers_with_ratings = beers_in_room.annotate(
        average_rating=Subquery(
            rating_subquery.values('average_rating')[:1]
        )
    ).order_by('order')

    serializer = BeerWithResultsSerializer(beers_with_ratings, many=True)
    return serializer.data


async_get_users_in_room = database_sync_to_async(get_users_in_room)
async_bump_users_last_active_field = database_sync_to_async(bump_users_last_active_field)
async_save_user_form = database_sync_to_async(save_user_form)
async_get_user_form_data = database_sync_to_async(get_user_form_data)
async_get_beers_in_room = database_sync_to_async(get_beers_in_room)
async_get_current_room = database_sync_to_async(get_current_room)
async_change_room_state_to = database_sync_to_async(change_room_state_to)
async_get_final_user_beer_ratings = database_sync_to_async(get_final_user_beer_ratings)
async_get_final_beers_ratings = database_sync_to_async(get_final_beers_ratings)
