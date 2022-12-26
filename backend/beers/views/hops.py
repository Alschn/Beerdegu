from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from beers.models import Hop
from beers.serializers import (
    HopSerializer,
)
from core.shared.pagination import page_number_pagination_factory

HopsPagination = page_number_pagination_factory(page_size=100)


class HopsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    GET     /api/hops/              - list all hops

    GET     /api/hops/<int:id>/     - retrieve hop
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = HopsPagination
    serializer_class = HopSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = None
    search_fields = ('name',)

    def get_queryset(self) -> QuerySet[Hop]:
        return Hop.objects.order_by('-id')
