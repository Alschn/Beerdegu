from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from beers.models import Hop


class HopSerializer(serializers.ModelSerializer):
    country = CountryField()

    class Meta:
        model = Hop
        fields = (
            'id',
            'name',
            'country',
            'description',
        )


class HopEmbeddedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hop
        fields = (
            'id',
            'name',
        )
