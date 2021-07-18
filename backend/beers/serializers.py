from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from beers.models import Beer, Hop, BeerStyle, Brewery


class HopSerializer(ModelSerializer):
    class Meta:
        model = Hop
        fields = '__all__'


class EmbeddedHopsSerializer(ModelSerializer):
    class Meta:
        model = Hop
        fields = ['id', 'name']


class StyleSerializer(ModelSerializer):
    class Meta:
        model = BeerStyle
        fields = '__all__'


class EmbeddedStyleSerializer(ModelSerializer):
    class Meta:
        model = BeerStyle
        exclude = ('description',)


class BrewerySerializer(ModelSerializer):
    class Meta:
        model = Brewery
        fields = '__all__'


class EmbeddedBrewerySerializer(ModelSerializer):
    class Meta:
        model = Brewery
        fields = ['id', 'name']


class BeerSerializer(ModelSerializer):
    class Meta:
        model = Beer
        fields = '__all__'


class SimplifiedBeerSerializer(ModelSerializer):
    brewery = StringRelatedField(read_only=True)
    style = StringRelatedField(read_only=True)

    class Meta:
        model = Beer
        fields = ('id', 'name', 'brewery', 'style')


class BeerRepresentationalSerializer(SimplifiedBeerSerializer):
    class Meta:
        model = Beer
        fields = ('id', 'name', 'brewery', 'style', 'image', 'description')


class DetailedBeerSerializer(BeerSerializer):
    """BeerSerializer with serialized relationships fields.
    Used when handling GET method (list/retrieve action)."""
    hops = EmbeddedHopsSerializer(many=True, read_only=True)
    style = EmbeddedStyleSerializer(read_only=True)
    brewery = EmbeddedBrewerySerializer(read_only=True)
