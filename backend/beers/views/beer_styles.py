from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from beers.models import BeerStyle
from beers.serializers import (
    BeerStyleSerializer,
)


class BeerStylesViewSet(viewsets.ModelViewSet):
    """
    GET     api/styles/          - list all beer styles
    POST    api/styles/          - create new beer style
    GET     api/styles/<int:id>/ - retrieve beer style
    PUT     api/styles/<int:id>/ - update beer style
    PATCH   api/styles/<int:id>/ - partially update beer style
    DELETE  api/styles/<int:id>/ - delete beer style
    """
    queryset = BeerStyle.objects.all()
    serializer_class = BeerStyleSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrReadOnly]
