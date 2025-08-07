from rest_framework import serializers
from restaurants.models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'  # 모든 필드를 포함