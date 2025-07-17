from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from beers.filters.beers import BeerFilterSet
from beers.models import Beer
from beers.serializers import (
    BeerSerializer,
    BeerCreateSerializer,
    BeerDetailedSerializer,
)
from core.shared.pagination import page_number_pagination_factory

BeersPagination = page_number_pagination_factory(page_size=30)


class BeersViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    GET     /api/beers/             - list all beers

    POST    /api/beers/             - create beer

    GET     /api/beers/<int:id>/    - retrieve beer
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = BeersPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = BeerFilterSet
    search_fields = ('name', 'brewery__name', 'style__name')
    ordering_fields = ('id', 'created_at', 'percentage')

    def get_queryset(self) -> QuerySet[Beer]:
        return Beer.objects.select_related(
            'brewery', 'style'
        ).prefetch_related(
            'hops'
        ).order_by('-id')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BeerDetailedSerializer

        if self.action == 'create':
            return BeerCreateSerializer

        return BeerSerializer
