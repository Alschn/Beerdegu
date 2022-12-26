import django_filters as filters

from beers.models import Brewery


class BreweriesFilterSet(filters.FilterSet):
    class Meta:
        model = Brewery
        fields = {
            'name': ['icontains'],
            'city': ['icontains'],
            'country': ['icontains'],
        }
