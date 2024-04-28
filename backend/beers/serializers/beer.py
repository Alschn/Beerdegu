import re
from decimal import Decimal
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.handlers.wsgi import WSGIRequest
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from beers.models import Beer, Hop
from beers.serializers.beer_style import EmbeddedBeerStyleSerializer
from beers.serializers.brewery import EmbeddedBrewerySerializer
from beers.serializers.hop import EmbeddedHopsSerializer
from rooms.models import BeerInRoom


class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = (
            'id',
            'name',
            'description',
            'brewery',
            'style',
            'hops',
            'image',
            'percentage',
            'volume_ml',
            'hop_rate',
            'extract',
            'IBU',
        )

    def to_representation(self, instance: Beer) -> dict:
        representation = super().to_representation(instance)
        representation['image'] = build_file_url(representation['image'], self.context.get('request'))
        return representation


class SimplifiedBeerSerializer(serializers.ModelSerializer):
    brewery = StringRelatedField(read_only=True)
    style = StringRelatedField(read_only=True)

    class Meta:
        model = Beer
        fields = ('id', 'image', 'name', 'brewery', 'style')


class BeerRepresentationalSerializer(SimplifiedBeerSerializer):
    class Meta:
        model = Beer
        fields = (
            'id', 'name', 'brewery', 'style', 'percentage',
            'hop_rate', 'extract', 'IBU',
            'image', 'description'
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = build_file_url(representation['image'], self.context.get('request'))
        return representation


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
    """
    BeerSerializer with serialized relationships fields.
    Used when handling GET method (list/retrieve action).
    """
    hops = EmbeddedHopsSerializer(many=True, read_only=True)
    style = EmbeddedBeerStyleSerializer(read_only=True)
    brewery = EmbeddedBrewerySerializer(read_only=True)


class BeerEmbeddedSerializer(BeerSerializer):
    """
    BeerSerializer with serialized brewery and style related fields.
    """
    style = EmbeddedBeerStyleSerializer(read_only=True)
    brewery = EmbeddedBrewerySerializer(read_only=True)


class BeerCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField(allow_null=True, required=False)

    class Meta:
        model = Beer
        fields = (
            'id',
            'name',
            'brewery',
            'style',
            'percentage',
            'volume_ml',
            'hop_rate',
            'extract',
            'IBU',
            'image',
            'description',
            'hops'
        )

    @transaction.atomic
    def create(self, validated_data: dict) -> Beer:
        hops: list[Hop] = validated_data.pop('hops')
        instance = super().create(validated_data)
        instance.hops.set(hops)
        return instance


class BeerInRatingSerializer(SimplifiedBeerSerializer):
    # todo: separate serializer for beer embedded in rating
    pass


def build_file_url(url: str | None, request: WSGIRequest) -> str | None:
    """
    A little bit hacky way to get correct file url regardless of current environment.
    Compatible with previous implementation of Beer.image field (URLField with link to external websites)

    Todo (?): Create custom FileField including this logic.
    """

    if not url:
        return

    # backward compatible with old urls (which were external links)
    if external_url := _extract_external_url(url):
        return external_url

    # everything is fine, since absolute uri was build from request
    if request:
        return url

    # usage without request in serializer's context (e.g. in websockets or unit tests),
    # when using AWS S3 or local storage

    if settings.USE_AWS_S3:
        return urljoin(settings.MEDIA_URL, url)

    current_site = Site.objects.get_current()
    return urljoin(current_site.domain, url)


def _extract_external_url(url: str | None) -> str | None:
    # http or https and anything after,
    # but not at the beginning of a string
    pattern = r'(?<!^)https?.*$'
    match = re.search(pattern, url)
    if not match:
        return None

    external_url = url[match.start():]

    # case: wrongly encoded url
    if '%3A' in external_url:
        # add missing colon and slash
        external_url = external_url.replace('%3A', ':/')
        return external_url

    # no need to adjust url
    if external_url.startswith('http://') or external_url.startswith('https://'):
        return external_url

    protocol, *parts = external_url.split('/')
    protocol = protocol.replace(':', '')
    new_external_url = f'{protocol}://{"/".join(parts)}'
    return new_external_url
