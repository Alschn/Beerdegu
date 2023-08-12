from rest_framework.routers import DefaultRouter

from ratings.views import RatingsViewSet

router = DefaultRouter()
router.register(r'ratings', RatingsViewSet, basename='ratings')

urlpatterns = router.urls
