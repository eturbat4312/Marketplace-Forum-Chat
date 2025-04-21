from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ListingViewSet, CityViewSet, CategoryViewSet, ListingImageViewSet

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'cities', CityViewSet, basename='city')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'listing-images', ListingImageViewSet, basename='listing-image')

urlpatterns = [
    path('', include(router.urls)),
]
