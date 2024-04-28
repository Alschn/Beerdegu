from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from rest_framework import serializers

from beers.models import Beer
from beers.serializers import BeerSimplifiedSerializer
from rooms.models import Room, BeerInRoom
from users.serializers.user import UserSerializer

User = get_user_model()

RESTRICTED_ROOM_NAMES = ('create', 'join', 'none', 'null', 'undefined', 'true', 'false')


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            'id', 'name', 'has_password',
            'host', 'slots', 'state',
            'created_at', 'updated_at',
            'users', 'beers', 'users_count',
        )


def get_hosted_not_finished_rooms(host: User) -> QuerySet[Room]:
    return Room.objects.filter(host=host).exclude(state=Room.State.FINISHED)


class RoomListSerializer(serializers.ModelSerializer):
    host = UserSerializer()

    class Meta:
        model = Room
        fields = (
            'id', 'name', 'has_password',
            'host', 'slots', 'state',
            'created_at', 'updated_at', 'users_count',
        )


class RoomCreateSerializer(serializers.ModelSerializer):
    host = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
    )
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
    )

    restricted_room_names = RESTRICTED_ROOM_NAMES

    def __init__(self, *args, user: User = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Room
        fields = ('name', 'password', 'slots', 'host')

    def validate_name(self, name: str) -> str:
        name = name.lower()

        if name in self.restricted_room_names:
            raise serializers.ValidationError(
                f'Room name `{name}` is restricted!',
                code='restricted_room_name'
            )

        return name

    def validate_host(self, host: User) -> User:
        user = self.user or self.context['request'].user

        if user != host:
            raise serializers.ValidationError(
                'You can only create rooms for yourself.',
                code='host_not_self'
            )

        not_finished_hosted_rooms = get_hosted_not_finished_rooms(host)
        if not_finished_hosted_rooms.exists():
            raise serializers.ValidationError(
                'User is already a host of another room, which is not in `FINISHED` state!',
                code='host_already_hosting'
            )

        return host


class RoomDetailedSerializer(RoomSerializer):
    host = UserSerializer(read_only=True)
    users = UserSerializer(many=True, read_only=True)
    beers = BeerSimplifiedSerializer(many=True, read_only=True)


class RoomJoinSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, allow_blank=True)

    # todo: add read_only fields so that to_representation does not have to be changed

    instance: Room

    def __init__(self, *args, user: User = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Room
        fields = ('password',)

    def validate_password(self, password: str) -> str:
        if self.instance.has_password and self.instance.password != password:
            raise serializers.ValidationError('Invalid password!')

        elif not self.instance.has_password and password != "":
            raise serializers.ValidationError('This room does not have a password but one was provided!')

        return password

    def validate(self, attrs: dict) -> dict:
        if self.instance.users.count() >= self.instance.slots:
            raise serializers.ValidationError({'slots': f'Room {self.instance.name} is full!'})

        return attrs

    def save(self, **kwargs) -> Room:
        user = self.user or self.context['request'].user

        if not self.instance.users.filter(id=user.id).exists():
            self.instance.users.add(user)

        return self.instance

    def to_representation(self, instance: Room) -> dict:
        serializer = RoomSerializer(instance)
        return serializer.data


class RoomAddBeerSerializer(serializers.Serializer):
    beer_id = serializers.IntegerField()

    def __init__(self, *args, beers_in_room: QuerySet[BeerInRoom] = None, room: Room = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.beers_in_room = beers_in_room
        self.room = room

    def validate_beer_id(self, beer_id: int) -> int:
        if not Beer.objects.filter(id=beer_id).exists():
            raise serializers.ValidationError(f'Beer with id `{beer_id}` does not exist!')

        if self.beers_in_room.filter(beer__id=beer_id).exists():
            raise serializers.ValidationError(f'Beer with id `{beer_id}` is already in this room!')

        return beer_id

    @transaction.atomic
    def save(self, **kwargs) -> Beer:
        beer = Beer.objects.get(id=self.validated_data['beer_id'])
        BeerInRoom.objects.create(
            room=self.room,
            beer=beer
        )
        return Beer.objects.filter(rooms=self.room).order_by(
            'rooms_through__order'
        )


class RoomDeleteBeerSerializer(serializers.Serializer):
    beer_id = serializers.IntegerField()

    def __init__(self, *args, beers_in_room: QuerySet[BeerInRoom] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.beers_in_room = beers_in_room

    def validate_beer_id(self, beer_id: int) -> int:
        if not self.beers_in_room.filter(beer__id=beer_id).exists():
            raise serializers.ValidationError(f'Beer with id `{beer_id}` is not in this room!')

        return beer_id

    def save(self, **kwargs) -> None:
        beer_id = self.validated_data['beer_id']
        self.beers_in_room.get(beer__id=beer_id).delete()
