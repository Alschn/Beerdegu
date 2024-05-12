from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from beers.serializers import (
    BeerSimplifiedSerializer,
    BeerStyleEmbeddedSerializer
)
from beers.serializers.brewery import BrewerySimplifiedSerializer
from ratings.serializers.rating import RatingWithSimplifiedBeerSerializer
from rooms.serializers.room import RoomListSerializer


class StatisticsQueryParamsSerializer(serializers.Serializer):
    date_from = serializers.DateField()
    date_to = serializers.DateField()

    def validate(self, attrs: dict) -> dict:
        validated_data = super().validate(attrs)

        if validated_data['date_from'] > validated_data['date_to']:
            message = _("`%(date_from_field)s` field value cannot be greater than `%(date_to_field)s`.")
            raise ValidationError(
                message % {'date_from_field': 'date_from', 'date_to_field': 'date_to'},
                code='invalid'
            )

        return validated_data


class EntityDistributionSerializer(serializers.Serializer):
    # solely for the purpose of documentation
    name = serializers.CharField()
    count = serializers.IntegerField(min_value=0)


class DashboardStatisticsSerializer(serializers.Serializer):
    # solely for the purpose of documentation
    consumed_beers_count = serializers.IntegerField(min_value=0)
    average_rating = serializers.FloatField(allow_null=True)
    rooms_joined_count = serializers.IntegerField(min_value=0)
    rooms_created_count = serializers.IntegerField(min_value=0)
    current_rooms = RoomListSerializer(many=True)
    recently_consumed_beers = BeerSimplifiedSerializer(many=True)
    highest_rating = RatingWithSimplifiedBeerSerializer(allow_null=True)
    lowest_rating = RatingWithSimplifiedBeerSerializer(allow_null=True)
    beer_styles_count = serializers.IntegerField(min_value=0)
    favourite_beer_style = BeerStyleEmbeddedSerializer(allow_null=True)
    breweries_count = serializers.IntegerField(min_value=0)
    favourite_brewery = BrewerySimplifiedSerializer(allow_null=True)
    beer_styles_distribution_chart = EntityDistributionSerializer(many=True)
    breweries_distribution_chart = EntityDistributionSerializer(many=True)
