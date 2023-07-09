from decimal import Decimal

from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from beers.models import Beer
from beers.serializers.beer_style import EmbeddedBeerStyleSerializer
from beers.serializers.brewery import EmbeddedBrewerySerializer
from beers.serializers.hop import EmbeddedHopsSerializer
from rooms.models import BeerInRoom


class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = (
            'id', 'name', 'brewery', 'style',
            'percentage', 'volume_ml', 'hop_rate',
            'extract', 'IBU', 'image', 'description',
            'hops'
        )


class SimplifiedBeerSerializer(serializers.ModelSerializer):
    brewery = StringRelatedField(read_only=True)
    style = StringRelatedField(read_only=True)

    class Meta:
        model = Beer
        fields = ('id', 'name', 'brewery', 'style')


class BeerRepresentationalSerializer(SimplifiedBeerSerializer):
    class Meta:
        model = Beer
        fields = (
            'id', 'name', 'brewery', 'style', 'percentage',
            'hop_rate', 'extract', 'IBU',
            'image', 'description'
        )


class BeerWithResultsSerializer(serializers.ModelSerializer):
    beer = SimplifiedBeerSerializer()
    average_rating = serializers.DecimalField(
        max_digits=4, decimal_places=2,
        min_value=Decimal(0), max_value=Decimal(10),
    )

    class Meta:
        model = BeerInRoom
        fields = ('order', 'beer', 'average_rating')


class DetailedBeerSerializer(BeerSerializer):
    """BeerSerializer with serialized relationships fields.
    Used when handling GET method (list/retrieve action)."""
    hops = EmbeddedHopsSerializer(many=True, read_only=True)
    style = EmbeddedBeerStyleSerializer(read_only=True)
    brewery = EmbeddedBrewerySerializer(read_only=True)
