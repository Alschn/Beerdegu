import django_filters as filters

from rooms.models import Room


class RoomsFilterSet(filters.FilterSet):
    class Meta:
        model = Room
        fields = {
            'name': ['icontains'],
            'slots': ['exact'],
            'state': ['exact'],
            'created_at': ['lte', 'gte'],
        }
