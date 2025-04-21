import django_filters
from .models import Listing

class ListingFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    
    class Meta:
        model = Listing
        fields = {
            'city__name': ['exact'],
            'category__name': ['exact'],
            # The min_price and max_price filters will be applied separately
        }
