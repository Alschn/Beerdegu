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


class DetailedBeerSerializer(ModelSerializer):
    hops = EmbeddedHopsSerializer(many=True, read_only=True)
    style = EmbeddedStyleSerializer(read_only=True)
    brewery = EmbeddedBrewerySerializer(read_only=True)

    class Meta:
        model = Beer
        fields = '__all__'


class BeerSerializer(ModelSerializer):
    def to_representation(self, instance):
        """
        GET request uses DetailedBeerSerializer to display detailed data.
        POST/PUT/PATCH requests are handled by BeerSerializer (this includes api forms).
        """
        if self.context['request'].method == 'GET':
            serializer = DetailedBeerSerializer(instance)
            return serializer.data
        return super().to_representation(instance)

    class Meta:
        model = Beer
        fields = '__all__'
