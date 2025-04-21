from rest_framework import serializers
from django.utils import timezone
from .models import Listing, City, Category, ListingImage, FREE, PAID


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name", "canton"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ["id", "image", "uploaded_at"]


class ListingSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), source="city", write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    creator_username = serializers.CharField(source="user.username", read_only=True)
    images = ListingImageSerializer(many=True, read_only=True)
    days_remaining = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "description",
            "price",
            "created_at",
            "user",
            "creator_username",
            "city",
            "city_id",
            "category",
            "category_id",
            "images",
            "phone_number",
            "ad_type",
            "expires_at",
            "days_remaining",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "user",
            "creator_username",
            "city",
            "category",
            "images",
            "expires_at",
            "days_remaining",
        ]

    def get_days_remaining(self, obj):
        if obj.expires_at:
            delta = obj.expires_at - timezone.now()
            return max(delta.days, 0)
        return None
