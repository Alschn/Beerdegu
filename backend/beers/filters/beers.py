import django_filters as filters

from beers.models import Beer


class BeerFilterSet(filters.FilterSet):
    class Meta:
        model = Beer
        fields = {
            'name': ['icontains'],
            'brewery': ['in'],
            'brewery__name': ['icontains'],
            'style': ['in'],
            'style__name': ['icontains'],
            'percentage': ['gte', 'lte', 'exact'],
            'volume_ml': ['gte', 'lte', 'exact'],
            'hop_rate': ['gte', 'lte', 'exact'],
            'extract': ['gte', 'lte', 'exact'],
            'IBU': ['gte', 'lte', 'exact'],
            'hops__name': ['icontains'],
        }
