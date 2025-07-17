import datetime

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from beers.serializers.beer import BeerEmbeddedSerializer
from purchases.models import BeerPurchase
from users.serializers.user import UserSerializer


class BeerPurchaseSerializer(serializers.ModelSerializer):
    beer = BeerEmbeddedSerializer()
    sold_to = UserSerializer()

    class Meta:
        model = BeerPurchase
        fields = (
            'id',
            'beer',
            'sold_to',
            'packaging',
            'price',
            'volume_ml',
            'image',
            'purchased_at',
        )


class BeerPurchaseSimplifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerPurchase
        fields = (
            'id',
            'beer',
            'sold_to',
            'packaging',
            'price',
            'volume_ml',
            'image',
            'purchased_at',
        )


class BeerPurchaseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeerPurchase
        fields = (
            'id',
            'beer',
            'sold_to',
            'packaging',
            'price',
            'volume_ml',
            'image',
            'purchased_at',
        )
        read_only_fields = ('id', 'sold_to')

    # noinspection PyMethodMayBeStatic
    def validate_purchased_at(self, value: datetime.date) -> datetime.date:
        now = timezone.now()

        if value > now.date():
            raise serializers.ValidationError(
                _('Cannot purchase beer in the future'),
                code='date_in_future'
            )

        return value
