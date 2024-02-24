from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from beers.serializers import (
    SimplifiedBeerSerializer,
    EmbeddedBeerStyleSerializer
)
from beers.serializers.brewery import SimplifiedBrewerySerializer
from ratings.serializers.rating import RatingWithSimplifiedBeerSerializer
from rooms.serializers.room import RoomListSerializer


class StatisticsQueryParamsSerializer(serializers.Serializer):
    date_from = serializers.DateField()
    date_to = serializers.DateField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        if validated_data['date_from'] > validated_data['date_to']:
            raise ValidationError({"date_from": "`date_from` field value cannot be greater than `date_to`."})

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
    recently_consumed_beers = SimplifiedBeerSerializer(many=True)
    highest_rating = RatingWithSimplifiedBeerSerializer(allow_null=True)
    lowest_rating = RatingWithSimplifiedBeerSerializer(allow_null=True)
    beer_styles_count = serializers.IntegerField(min_value=0)
    favourite_beer_style = EmbeddedBeerStyleSerializer(allow_null=True)
    breweries_count = serializers.IntegerField(min_value=0)
    favourite_brewery = SimplifiedBrewerySerializer(allow_null=True)
    beer_styles_distribution_chart = EntityDistributionSerializer(many=True)
    breweries_distribution_chart = EntityDistributionSerializer(many=True)
