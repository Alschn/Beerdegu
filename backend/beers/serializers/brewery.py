from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from beers.models import Brewery


class BrewerySerializer(serializers.ModelSerializer):
    country = CountryField()

    class Meta:
        model = Brewery
        fields = (
            'id',
            'name',
            'city',
            'country',
            'year_established',
            'image',
            'website',
            'description',
            'created_at',
            'updated_at'
        )


class EmbeddedBrewerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Brewery
        fields = ('id', 'name')
