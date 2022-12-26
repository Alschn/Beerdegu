from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from beers.filters.beers import BeerFilterSet
from beers.models import Beer
from beers.serializers import (
    BeerSerializer, DetailedBeerSerializer,
)
from core.shared.pagination import page_number_pagination_factory

BeersPagination = page_number_pagination_factory(page_size=30)


class BeersViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    GET     /api/beers/             - list all beers
    GET     /api/beers/<int:id>/    - retrieve beer
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = BeersPagination
    serializer_class = BeerSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = BeerFilterSet
    search_fields = ('name', 'brewery__name', 'style__name')

    def get_queryset(self) -> QuerySet[Beer]:
        return Beer.objects.order_by('-id')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return DetailedBeerSerializer

        return super().get_serializer_class()
