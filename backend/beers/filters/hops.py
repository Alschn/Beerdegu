import django_filters as filters

from beers.models import Hop


class HopsFilterSet(filters.FilterSet):
    class Meta:
        model = Hop
        fields = {
            'name': ['icontains'],
            'country': ['icontains'],
        }
