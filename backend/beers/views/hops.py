from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from beers.models import Hop
from beers.serializers import (
    HopSerializer,
)


class HopsViewSet(viewsets.ModelViewSet):
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
