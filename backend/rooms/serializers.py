from rest_framework import serializers

from beers.serializers import SimplifiedBeerSerializer
from rooms.models import Room, Rating
from users.serializers import UserSerializer


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ('password',)


class DetailedRoomSerializer(RoomSerializer):
    host = UserSerializer(read_only=True)
    users = UserSerializer(many=True, read_only=True)
    beers = SimplifiedBeerSerializer(many=True, read_only=True)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = [
            'color', 'foam', 'smell', 'taste', 'opinion', 'note'
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
