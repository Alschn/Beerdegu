import django_filters.rest_framework as filters

from purchases.models import BeerPurchase


class BeerPurchaseFilterSet(filters.FilterSet):
    # todo: add beer csv filter

    class Meta:
        model = BeerPurchase
        fields = {
            'packaging': ['exact'],
            'price': ['exact', 'lte', 'gte'],
            'volume_ml': ['exact', 'lte', 'gte'],
            'purchased_at': ['exact', 'lte', 'gte'],
        }
