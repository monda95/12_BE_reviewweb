

from django.urls import path
from reviews.views import ReviewViewSet, ReviewDetailView

urlpatterns = [
    path('restaurants/<int:restaurant_id>/reviews/', ReviewViewSet.as_view(), name='review-list'),
    path('reviews/<int:review_id>/', ReviewDetailView.as_view(), name='review-detail'),
]