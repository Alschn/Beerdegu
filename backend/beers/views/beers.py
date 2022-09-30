from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from beers.models import Beer
from beers.serializers import (
    BeerSerializer, DetailedBeerSerializer,
)


class BeersViewSet(viewsets.ModelViewSet):
    """
    GET     api/beers/          - list all beers
    POST    api/beers/          - create new beer
    GET     api/beers/<int:id>/ - retrieve beer
    PUT     api/beers/<int:id>/ - update beer
    PATCH   api/beers/<int:id>/ - partially update beer
    DELETE  api/beers/<int:id>/ - delete beer
    """
    queryset = Beer.objects.all()
    serializer_class = BeerSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'brewery__name', 'style__name']

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action in ['list', 'retrieve']:
            return DetailedBeerSerializer
        return super().get_serializer_class()
