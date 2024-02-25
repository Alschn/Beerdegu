from rest_framework.routers import DefaultRouter

from purchases.views.beer_purchases import BeerPurchasesViewSet

router = DefaultRouter()
router.register(r'beer-purchases', BeerPurchasesViewSet, basename='beer-purchases')

urlpatterns = router.urls
