from rest_framework import serializers

from beers.serializers import SimplifiedBeerSerializer
from rooms.models import Room
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
