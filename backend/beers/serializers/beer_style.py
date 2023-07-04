from rest_framework import serializers
from beers.models import BeerStyle


class BeerStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerStyle
        fields = ('id', 'name', 'description')


class EmbeddedBeerStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerStyle
        exclude = ('description',)
