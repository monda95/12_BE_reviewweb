from rest_framework.generics import RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from restaurants.models import Restaurant
from .models import Review
from .serializers import ReviewSerializer, ReviewDetailSerializer, ReviewUpdateSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import viewsets, mixins

class ReviewViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(restaurant_id=self.kwargs['restaurant_pk'])

    def perform_create(self, serializer):
        restaurant = get_object_or_404(Restaurant, id=self.kwargs['restaurant_pk'])
        serializer.save(user=self.request.user, restaurant=restaurant)

class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_url_kwarg = 'review_id'

    def get_serializer_class(self):
        if self.request.method == 'PATCH' or self.request.method == 'PUT':
            return ReviewUpdateSerializer
        return ReviewDetailSerializer