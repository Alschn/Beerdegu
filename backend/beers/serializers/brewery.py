from rest_framework import serializers

from beers.models import Brewery


class BrewerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Brewery
        fields = (
            'id', 'name', 'city', 'country',
            'established', 'description'
        )


class EmbeddedBrewerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Brewery
        fields = ('id', 'name')
