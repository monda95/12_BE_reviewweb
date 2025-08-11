from django.urls import path, include
from rest_framework_nested import routers
from .views import RestaurantViewSet
from reviews.views import ReviewViewSet

router = routers.SimpleRouter()
router.register(r'', RestaurantViewSet, basename='restaurants')

reviews_router = routers.NestedSimpleRouter(router, r'', lookup='restaurant')
reviews_router.register(r'reviews', ReviewViewSet, basename='restaurant-reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(reviews_router.urls)),
]
