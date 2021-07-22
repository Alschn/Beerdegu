from decimal import Decimal

from rest_framework.relations import StringRelatedField
from rest_framework import serializers

from beers.models import Beer, Hop, BeerStyle, Brewery
from rooms.models import BeerInRoom


class HopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hop
        fields = '__all__'


class EmbeddedHopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hop
        fields = ['id', 'name']


class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerStyle
        fields = '__all__'


class EmbeddedStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerStyle
        exclude = ('description',)


class BrewerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Brewery
        fields = '__all__'


class EmbeddedBrewerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Brewery
        fields = ['id', 'name']


class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = '__all__'


class SimplifiedBeerSerializer(serializers.ModelSerializer):
    brewery = StringRelatedField(read_only=True)
    style = StringRelatedField(read_only=True)

    class Meta:
        model = Beer
        fields = ('id', 'name', 'brewery', 'style')


class BeerRepresentationalSerializer(SimplifiedBeerSerializer):
    class Meta:
        model = Beer
        fields = ('id', 'name', 'brewery', 'style', 'percentage', 'image', 'description')


class BeerWithResultsSerializer(serializers.ModelSerializer):
    beer = SimplifiedBeerSerializer()
    average_rating = serializers.DecimalField(
        max_digits=4, decimal_places=2,
        min_value=Decimal(0), max_value=Decimal(10),
    )

    class Meta:
        model = BeerInRoom
        fields = ('beer', 'average_rating')


class DetailedBeerSerializer(BeerSerializer):
    """BeerSerializer with serialized relationships fields.
    Used when handling GET method (list/retrieve action)."""
    hops = EmbeddedHopsSerializer(many=True, read_only=True)
    style = EmbeddedStyleSerializer(read_only=True)
    brewery = EmbeddedBrewerySerializer(read_only=True)
