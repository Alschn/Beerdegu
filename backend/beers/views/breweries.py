from django.db.models import QuerySet
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from beers.models import Brewery
from beers.serializers import (
    BrewerySerializer,
)
from core.shared.pagination import page_number_pagination_factory

BreweriesPagination = page_number_pagination_factory(page_size=100)


class BreweriesViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    GET     /api/breweries/             - list all breweries
    GET     /api/breweries/<int:id>/    - retrieve brewery
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = BreweriesPagination
    serializer_class = BrewerySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', 'city', 'country')

    def get_queryset(self) -> QuerySet[Brewery]:
        return Brewery.objects.order_by('-id')
