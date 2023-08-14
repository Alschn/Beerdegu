import django_filters as filters
from django_filters import widgets

from beers.models import Beer, Hop


class BeerFilterSet(filters.FilterSet):
    hops__in = filters.ModelMultipleChoiceFilter(
        field_name='hops',
        lookup_expr='exact',
        queryset=Hop.objects.all(),
        widget=widgets.CSVWidget,
        label='Hop is in',
        help_text='Multiple values may be separated by commas.',
    )

    class Meta:
        model = Beer
        fields = {
            'name': ['icontains'],
            'brewery': ['in'],
            'brewery__name': ['icontains'],
            'style': ['in'],
            'style__name': ['icontains'],
            'percentage': ['gte', 'lte', 'exact', 'range'],
            'volume_ml': ['gte', 'lte', 'exact', 'range'],
            'hop_rate': ['gte', 'lte', 'exact', 'range'],
            'extract': ['gte', 'lte', 'exact', 'range'],
            'IBU': ['gte', 'lte', 'exact', 'range'],
            'hops__name': ['icontains'],
        }
