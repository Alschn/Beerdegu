from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from beers.models import Beer
from beers.serializers.beer import (
    DetailedBeerSerializer,
    BeerInRatingSerializer,
    SimplifiedBeerSerializer
)
from purchases.models import BeerPurchase
from purchases.serializers import BeerPurchaseSimplifiedSerializer
from ratings.models import Rating
from rooms.serializers.room import RoomListSerializer
from users.serializers.user import UserSerializer


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = (
            'id',
            'color',
            'foam',
            'smell',
            'taste',
            'opinion',
            'note',
            'beer',
            'beer_purchase'
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
    beer_purchase = BeerPurchaseSimplifiedSerializer()
    room = RoomListSerializer()

    class Meta:
        model = Rating
        fields = (
            'id',
            'added_by',
            'beer',
            'beer_purchase',
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
    beer_purchase = BeerPurchaseSimplifiedSerializer()
    room = RoomListSerializer()

    class Meta:
        model = Rating
        fields = (
            'id',
            'added_by',
            'beer',
            'beer_purchase',
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
            'beer_purchase',
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

    def validate(self, attrs: dict) -> dict:
        validated_data = super().validate(attrs)
        beer: Beer = validated_data.get('beer')
        beer_purchase: BeerPurchase | None = validated_data.get('beer_purchase')

        if beer and beer_purchase and beer_purchase.beer != beer:
            message = _('Beer from beer_purchase does not match the beer.')
            raise serializers.ValidationError(
                {'beer': message, 'beer_purchase': message}
            )

        return validated_data


class RatingUpdateSerializer(serializers.ModelSerializer):
    # same as in RatingListSerializer, so that the types match
    added_by = UserSerializer()
    beer = BeerInRatingSerializer()
    beer_purchase = BeerPurchaseSimplifiedSerializer()
    room = RoomListSerializer()

    class Meta:
        model = Rating
        fields = (
            'id',
            'added_by',
            'beer',
            'beer_purchase',
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
            'beer_purchase',
            'room',
            'created_at',
            'updated_at'
        )


class RatingWithSimplifiedBeerSerializer(serializers.ModelSerializer):
    beer = SimplifiedBeerSerializer()

    class Meta:
        model = Rating
        fields = (
            'id',
            'beer',
            'beer_purchase',
            'added_by',
            'note',
            'created_at',
            'updated_at'
        )
        read_only_fields = fields
