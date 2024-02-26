import django_filters.rest_framework as filters

from purchases.models import BeerPurchase


class BeerPurchaseFilterSet(filters.FilterSet):
    beer = filters.BaseCSVFilter(
        field_name='beer__id',
        lookup_expr='in'
    )

    class Meta:
        model = BeerPurchase
        fields = {
            'packaging': ['exact'],
            'price': ['exact', 'lte', 'gte'],
            'volume_ml': ['exact', 'lte', 'gte'],
            'purchased_at': ['exact', 'lte', 'gte'],
        }
