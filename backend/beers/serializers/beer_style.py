from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from beers.models import BeerStyle


class BeerStyleListSerializer(serializers.ModelSerializer):
    country = CountryField()

    class Meta:
        model = BeerStyle
        fields = (
            'id',
            'name',
            'known_as',
            'country',
            'description',
            'created_at',
            'updated_at'
        )


class BeerStyleDetailSerializer(serializers.ModelSerializer):
    country = CountryField()

    class Meta:
        model = BeerStyle
        fields = (
            'id',
            'name',
            'known_as',
            'country',
            'description',
            'serving_temperature_range',
            'abv_range',
            'color_range',
            'bitterness_range',
            'original_gravity_range',
            'final_gravity_range',
            'created_at',
            'updated_at'
        )


class BeerStyleEmbeddedSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerStyle
        fields = (
            'id',
            'name',
            'description'
        )
