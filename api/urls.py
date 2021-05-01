from rest_framework.routers import DefaultRouter

from .views import MovieViewSet, PersonViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'persons', PersonViewSet)

urlpatterns = router.urls
