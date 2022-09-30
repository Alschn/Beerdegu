from rest_framework.routers import DefaultRouter

from beers.views import (
    BeersViewSet, BeerStylesViewSet, BreweriesViewSet, HopsViewSet
)

router = DefaultRouter()
router.register(r'beers', BeersViewSet, basename='beers')
router.register(r'styles', BeerStylesViewSet, basename='styles')
router.register(r'breweries', BreweriesViewSet, basename='breweries')
router.register(r'hops', HopsViewSet, basename='hops')

urlpatterns = router.urls
