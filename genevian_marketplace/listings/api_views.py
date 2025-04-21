# listings/api_views.py
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db.models import Case, When, Value, IntegerField

from .models import Listing, City, Category, ListingImage, FREE, PAID
from .serializers import (
    ListingSerializer,
    CitySerializer,
    CategorySerializer,
    ListingImageSerializer,
)


class ListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listings.
    - Free users can post up to 3 listings per week with only 1 image per listing.
    - Paid ads (via premium subscription or ad conversion) allow up to 10 images and extended features.
    - Free ads expire after 14 days; paid ads expire after 30 days.
    """

    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Keep these for other filters (but we'll handle category manually)
    filterset_fields = {"city__name": ["exact"], "category__name": ["iexact"]}
    search_fields = ["title", "description"]
    ordering_fields = ["price", "created_at"]

    def get_queryset(self):
        qs = Listing.objects.all().annotate(
            is_paid=Case(
                When(ad_type=PAID, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        )
        # Manual filtering: if a query parameter "category__name" exists, filter by it (iexact)
        category_name = self.request.query_params.get("category__name")
        if category_name:
            print("Filtering listings with category (iexact):", category_name)
            qs = qs.filter(category__name__iexact=category_name)
        return qs.order_by("-is_paid", "-created_at")

    def perform_create(self, serializer):
        user = self.request.user
        ad_type = self.request.data.get(
            "ad_type", FREE
        )  # default to free if not provided
        # Enforce weekly limit for free ads
        if ad_type == FREE:
            recent_ads_count = Listing.objects.filter(
                user=user, created_at__gte=timezone.now() - timedelta(days=7)
            ).count()
            if recent_ads_count >= 3:
                raise ValidationError(
                    "You have reached your weekly limit of 3 free listings. Convert this ad to paid for more postings and additional images."
                )
        new_images = self.request.FILES.getlist("images")
        # Enforce image limits based on ad type
        if ad_type == FREE:
            if len(new_images) > 1:
                raise ValidationError(
                    "Free ads can only include one image. Convert to paid to add more images."
                )
        elif ad_type == PAID:
            if len(new_images) > 10:
                new_images = new_images[:10]  # Or raise an error if preferred.
        listing = serializer.save(user=user, ad_type=ad_type)
        for img in new_images:
            ListingImage.objects.create(listing=listing, image=img)

    def perform_update(self, serializer):
        listing = serializer.save()
        # Allow conversion of a free ad to paid via update by sending ad_type in the request.
        ad_type = self.request.data.get("ad_type", listing.ad_type)
        listing.ad_type = ad_type
        listing.save()
        new_images = self.request.FILES.getlist("images")
        if new_images:
            existing_images_count = listing.images.count()
            if ad_type == FREE:
                allowed_new = 1 - existing_images_count
                if allowed_new <= 0 or len(new_images) > allowed_new:
                    raise ValidationError(
                        "Free ads can only have one image. Convert to paid for additional images."
                    )
            elif ad_type == PAID:
                allowed_new = 10 - existing_images_count
                if allowed_new < len(new_images):
                    raise ValidationError(
                        "Paid ads can have a maximum of 10 images. Please remove some images."
                    )
            for img in new_images:
                ListingImage.objects.create(listing=listing, image=img)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def my_listings(self, request):
        """Return only the listings for the currently logged-in user."""
        user = request.user
        queryset = self.get_queryset().filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticated])
    def convert_to_paid(self, request, pk=None):
        """Convert a free ad to a paid ad and update its expiration date."""
        listing = self.get_object()
        if listing.ad_type == PAID:
            return Response({"detail": "Listing is already a paid ad."}, status=400)
        listing.ad_type = PAID
        listing.expires_at = timezone.now() + timedelta(days=30)
        listing.save()
        return Response({"detail": "Listing converted to paid ad successfully."})


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ListingImageViewSet(viewsets.ModelViewSet):
    queryset = ListingImage.objects.all()
    serializer_class = ListingImageSerializer
    permission_classes = [IsAuthenticated]
