from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from beers.models import Brewery
from beers.serializers import (
    BrewerySerializer,
)


class BreweriesViewSet(viewsets.ModelViewSet):
    """
    GET     api/breweries/          - list all breweries
    POST    api/breweries/          - create new brewery
    GET     api/breweries/<int:id>/ - retrieve brewery
    PUT     api/breweries/<int:id>/ - update brewery
    PATCH   api/breweries/<int:id>/ - partially update brewery
    DELETE  api/breweries/<int:id>/ - delete brewery
    """
    queryset = Brewery.objects.all()
    serializer_class = BrewerySerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrReadOnly]
