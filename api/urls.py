from rest_framework.routers import DefaultRouter

from .views import GenreViewSet, MovieViewSet, PersonViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'persons', PersonViewSet)
router.register(r'genres', GenreViewSet)

urlpatterns = router.urls
