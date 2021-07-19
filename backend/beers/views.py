from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from beers.models import Beer, Hop, BeerStyle, Brewery
from beers.serializers import (
    BeerSerializer, DetailedBeerSerializer,
    StyleSerializer, BrewerySerializer, HopSerializer,
)


class BeerViewSet(viewsets.ModelViewSet):
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

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action in ['list', 'retrieve']:
            return DetailedBeerSerializer
        return super().get_serializer_class()


class HopViewSet(viewsets.ModelViewSet):
    """
    GET     api/hops/          - list all hops
    POST    api/hops/          - create new hop
    GET     api/hops/<int:id>/ - retrieve hop
    PUT     api/hops/<int:id>/ - update hop
    PATCH   api/hops/<int:id>/ - partially update hop
    DELETE  api/hops/<int:id>/ - delete hop
    """
    queryset = Hop.objects.all()
    serializer_class = HopSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrReadOnly]


class BeerStyleViewSet(viewsets.ModelViewSet):
    """
    GET     api/styles/          - list all beer styles
    POST    api/styles/          - create new beer style
    GET     api/styles/<int:id>/ - retrieve beer style
    PUT     api/styles/<int:id>/ - update beer style
    PATCH   api/styles/<int:id>/ - partially update beer style
    DELETE  api/styles/<int:id>/ - delete beer style
    """
    queryset = BeerStyle.objects.all()
    serializer_class = StyleSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrReadOnly]


class BreweryViewSet(viewsets.ModelViewSet):
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
