import django_filters.rest_framework as filters

from rooms.models import Rating


class RatingsFilterSet(filters.FilterSet):
    class Meta:
        model = Rating
        fields = {
            'beer': ['exact', 'in'],
            'room': ['exact', 'in'],
            'added_by': ['exact', 'in'],
            'note': ['gte', 'lte', 'gt', 'lt', 'exact', 'range'],
            'created_at': ['gte', 'lte'],
            'updated_at': ['gte', 'lte'],
        }
