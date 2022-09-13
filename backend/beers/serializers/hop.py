from rest_framework import serializers

from beers.models import Hop


class HopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hop
        fields = '__all__'


class EmbeddedHopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hop
        fields = ['id', 'name']
