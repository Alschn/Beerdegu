import django_filters as filters

from beers.models import BeerStyle


class BeerStylesFilterSet(filters.FilterSet):
    class Meta:
        model = BeerStyle
        fields = {
            'name': ['icontains'],
        }
