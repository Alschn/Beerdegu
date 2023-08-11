from django.urls import path
from rest_framework.routers import DefaultRouter

from rooms.views import (
    RatingsViewSet,
    RoomsViewSet,
    BeersInRoomView
)

router = DefaultRouter()
router.register(r'rooms', RoomsViewSet, basename='rooms')
router.register(r'ratings', RatingsViewSet, basename='ratings')

urlpatterns = [
    *router.urls,
    path('rooms/<str:room_name>/beers/', BeersInRoomView.as_view(), name='rooms-detail-beers')
]
