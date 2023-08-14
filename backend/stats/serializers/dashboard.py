from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rooms.serializers.room import RoomListSerializer


class StatisticsQueryParamsSerializer(serializers.Serializer):
    date_from = serializers.DateField()
    date_to = serializers.DateField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        if validated_data['date_from'] > validated_data['date_to']:
            raise ValidationError({"date_from": "`date_from` field value cannot be greater than `date_to`."})

        return validated_data


class DashboardStatisticsSerializer(serializers.Serializer):
    # solely for the purpose of documentation
    consumed_beers_count = serializers.IntegerField()
    average_rating = serializers.FloatField(allow_null=True)
    rooms_joined_count = serializers.IntegerField()
    rooms_created_count = serializers.IntegerField()
    current_rooms = RoomListSerializer(many=True)
    # todo: add when frontend is prepared to display that data
    # highest_rating = RatingWithSimplifiedBeerSerializer(allow_null=True)
    # lowest_rating = RatingWithSimplifiedBeerSerializer(allow_null=True)
    # recently_consumed_beers = SimplifiedBeerSerializer(many=True)
