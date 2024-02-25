from rest_framework import serializers

from purchases.models import BeerPurchase


class BeerPurchaseSerializer(serializers.ModelSerializer):
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
