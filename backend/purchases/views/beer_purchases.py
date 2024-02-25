from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from core.shared.pagination import page_number_pagination_factory
from purchases.filters.beer_purchase import BeerPurchaseFilterSet
from purchases.models import BeerPurchase
from purchases.serializers.beer_purchase import (
    BeerPurchaseSerializer,
    BeerPurchaseCreateSerializer
)

BeerPurchasePagination = page_number_pagination_factory(page_size=30)


class BeerPurchasesViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = BeerPurchaseSerializer
    pagination_class = BeerPurchasePagination
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = BeerPurchaseFilterSet
    search_fields = ('beer__name', 'beer__style__name')

    def get_queryset(self) -> QuerySet[BeerPurchase]:
        return BeerPurchase.objects.filter(
            sold_to=self.request.user
        ).select_related('beer', 'sold_to', 'beer__style')

    def get_serializer_class(self):
        if self.action == 'create':
            return BeerPurchaseCreateSerializer

        return BeerPurchaseSerializer
