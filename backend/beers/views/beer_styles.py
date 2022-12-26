from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from beers.filters.beer_styles import BeerStylesFilterSet
from beers.models import BeerStyle
from beers.serializers import (
    BeerStyleSerializer,
)
from core.shared.pagination import page_number_pagination_factory

BeerStylesPagination = page_number_pagination_factory(page_size=100)


class BeerStylesViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    GET     /api/styles/            - list all beer styles
    GET     /api/styles/<int:id>/   - retrieve beer style
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = BeerStylesPagination
    serializer_class = BeerStyleSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = BeerStylesFilterSet
    search_fields = ('name',)

    def get_queryset(self) -> QuerySet[BeerStyle]:
        return BeerStyle.objects.order_by('-id')
