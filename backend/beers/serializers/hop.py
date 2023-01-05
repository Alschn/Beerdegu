from rest_framework import serializers

from beers.models import Hop


class HopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hop
        fields = ('id', 'name', 'description', 'country')


class EmbeddedHopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hop
        fields = ('id', 'name')
