from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

# Constants for ad types
FREE = "free"
PAID = "paid"
AD_TYPE_CHOICES = (
    (FREE, "Free"),
    (PAID, "Paid"),
)


class City(models.Model):
    name = models.CharField(max_length=100)
    canton = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listings"
    )
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True, related_name="listings"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="listings",
    )
    ad_type = models.CharField(max_length=10, choices=AD_TYPE_CHOICES, default=FREE)
    expires_at = models.DateTimeField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # New field

    def save(self, *args, **kwargs):
        # Set expiration based on ad_type: free ads expire after 14 days; paid ads after 30 days.
        if not self.expires_at:
            if self.ad_type == PAID:
                self.expires_at = timezone.now() + timedelta(days=30)
            else:
                self.expires_at = timezone.now() + timedelta(days=14)
        super().save(*args, **kwargs)

    def days_remaining(self):
        if self.expires_at:
            delta = self.expires_at - timezone.now()
            return max(delta.days, 0)
        return None

    def __str__(self):
        return self.title


class ListingImage(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="listing_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.listing.title}"
