from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from core.shared.pagination import page_number_pagination_factory
from ratings.filters import RatingsFilterSet
from ratings.models import Rating
from ratings.permissons import CanDeleteRatingPermission
from ratings.serializers import (
    RatingListSerializer,
    RatingDetailSerializer,
    RatingUpdateSerializer,
    RatingCreateSerializer
)

RatingsPagination = page_number_pagination_factory(page_size=50)


class RatingsViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    GET     /api/ratings/                     - list all current user's ratings

    POST    /api/ratings/                     - create new rating

    GET     /api/ratings/<int:id>/            - retrieve rating

    PATCH   /api/ratings/<int:id>/            - update rating

    DELETE  /api/ratings/<int:id>/            - delete rating
    """
    permission_classes = [IsAuthenticated, CanDeleteRatingPermission]
    pagination_class = RatingsPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RatingsFilterSet
    http_method_names = ('get', 'post', 'patch', 'delete')
    search_fields = (
        'beer__name', 'beer__brewery__name',
        'room__name', 'added_by__username'
    )
    ordering_fields = ('id', 'created_at', 'updated_at')
    lookup_field = 'id'

    def get_queryset(self) -> QuerySet[Rating]:
        if not self.request.user.is_authenticated:
            return Rating.objects.none()

        if self.action == 'list':
            return Rating.objects.filter(
                added_by=self.request.user
            ).select_related('added_by', 'beer').order_by('-created_at')

        if self.action == 'retrieve':
            return Rating.objects.filter(
                added_by=self.request.user
            ).select_related(
                'added_by', 'beer', 'room', 'room__host',
                'beer__brewery', 'beer__style'
            ).prefetch_related(
                'beer__hops'
            ).order_by('-created_at')

        return Rating.objects.filter(added_by=self.request.user).order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'list':
            return RatingListSerializer

        if self.action == 'create':
            return RatingCreateSerializer

        if self.action == 'partial_update':
            return RatingUpdateSerializer

        return RatingDetailSerializer

    def perform_create(self, serializer: RatingCreateSerializer) -> None:
        serializer.save(added_by=self.request.user)
