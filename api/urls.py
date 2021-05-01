from rest_framework.routers import DefaultRouter

from .views import MovieViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet)

urlpatterns = router.urls
