from rest_framework import serializers

from beers.serializers.beer import DetailedBeerSerializer, BeerInRatingSerializer
from rooms.models import Rating
from rooms.serializers.room import RoomListSerializer
from users.serializers.user import UserSerializer


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = (
            'color',
            'foam',
            'smell',
            'taste',
            'opinion',
            'note',
            'beer'
        )

    def to_representation(self, instance: Rating):
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


class RatingListSerializer(serializers.ModelSerializer):
    added_by = UserSerializer()
    beer = BeerInRatingSerializer()
    room = RoomListSerializer()

    class Meta:
        model = Rating
        fields = (
            'id',
            'added_by',
            'beer',
            'room',
            'color',
            'foam',
            'smell',
            'taste',
            'opinion',
            'note',
            'created_at',
            'updated_at',
        )


class RatingDetailSerializer(serializers.ModelSerializer):
    added_by = UserSerializer()
    beer = DetailedBeerSerializer()
    room = RoomListSerializer()

    class Meta:
        model = Rating
        fields = (
            'id',
            'added_by',
            'beer',
            'room',
            'color',
            'foam',
            'smell',
            'taste',
            'opinion',
            'note',
            'created_at',
            'updated_at'
        )


class RatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = (
            'id',
            'added_by',
            'beer',
            'room',
            'color',
            'foam',
            'smell',
            'taste',
            'opinion',
            'note',
            'created_at',
            'updated_at'
        )
        read_only_fields = (
            'id',
            'added_by',
            'room',
            'created_at',
            'updated_at'
        )


class RatingUpdateSerializer(serializers.ModelSerializer):
    # same as in RatingListSerializer, so that the types match
    added_by = UserSerializer()
    beer = BeerInRatingSerializer()
    room = RoomListSerializer()

    class Meta:
        model = Rating
        fields = (
            'id',
            'added_by',
            'beer',
            'room',
            'color',
            'foam',
            'smell',
            'taste',
            'opinion',
            'note',
            'created_at',
            'updated_at'
        )
        read_only_fields = (
            'id',
            'added_by',
            'beer',
            'room',
            'created_at',
            'updated_at'
        )
