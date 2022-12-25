from django.db import transaction
from django.db.models import QuerySet
from rest_framework import serializers

from beers.models import Beer
from beers.serializers import SimplifiedBeerSerializer
from rooms.models import Room, BeerInRoom
from users.serializers.user import UserSerializer


class RoomSerializer(serializers.ModelSerializer):
    has_password = serializers.SerializerMethodField()

    class Meta:
        model = Room
        exclude = ('password',)

    def get_has_password(self, obj: Room) -> bool:
        # cast to bool to check if password exists
        return not not obj.password


class CreateRoomSerializer(serializers.ModelSerializer):
    host = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Room
        fields = ['name', 'password', 'slots', 'host']


class DetailedRoomSerializer(RoomSerializer):
    host = UserSerializer(read_only=True)
    users = UserSerializer(many=True, read_only=True)
    beers = SimplifiedBeerSerializer(many=True, read_only=True)


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
            room=self.room, beer=beer
        )
        return Beer.objects.filter(room=self.room).order_by('id')


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
