from rest_framework.routers import DefaultRouter

from beers.views import (
    BeerViewSet, BeerStyleViewSet, BreweryViewSet, HopViewSet
)

router = DefaultRouter()
router.register(r'beers', BeerViewSet, basename='beers')
router.register(r'styles', BeerStyleViewSet, basename='styles')
router.register(r'breweries', BreweryViewSet, basename='breweries')
router.register(r'hops', HopViewSet, basename='hops')

urlpatterns = router.urls
