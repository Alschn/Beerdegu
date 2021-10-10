from rest_framework import serializers

from beers.serializers import SimplifiedBeerSerializer
from rooms.models import Room, Rating
from users.serializers import UserSerializer


class RoomSerializer(serializers.ModelSerializer):
    has_password = serializers.SerializerMethodField()

    class Meta:
        model = Room
        exclude = ('password',)

    def get_has_password(self, obj):
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


class RatingSerializer(serializers.ModelSerializer):
    beer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = [
            'color', 'foam', 'smell', 'taste', 'opinion', 'note', 'beer'
        ]

    def to_representation(self, instance):
        my_fields = self.Meta.fields
        data = super().to_representation(instance)
        # Replace None with empty string, so that client does not receive nulls
        for field in my_fields:
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
