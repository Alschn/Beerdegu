from rest_framework import serializers
from beers.models import BeerStyle


class BeerStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerStyle
        fields = '__all__'


class EmbeddedBeerStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerStyle
        exclude = ('description',)
