from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from beers.filters.beer_styles import BeerStylesFilterSet
from beers.models import BeerStyle
from beers.serializers import (
    BeerStyleListSerializer,
    BeerStyleDetailSerializer
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
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = BeerStylesFilterSet
    search_fields = ('name', 'known_as')

    def get_queryset(self) -> QuerySet[BeerStyle]:
        return BeerStyle.objects.order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list':
            return BeerStyleListSerializer

        return BeerStyleDetailSerializer
