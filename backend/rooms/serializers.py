from rest_framework import serializers

from beers.serializers import SimplifiedBeerSerializer
from rooms.models import Room
from users.serializers import UserSerializer


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ('password',)


class DetailedRoomSerializer(RoomSerializer):
    host = UserSerializer(read_only=True)
    users = UserSerializer(many=True, read_only=True)
    beers = SimplifiedBeerSerializer(many=True, read_only=True)
