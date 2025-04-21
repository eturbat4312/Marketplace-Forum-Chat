from django.contrib import admin
from .models import Listing, City, Category

admin.site.register(City)
admin.site.register(Category)
admin.site.register(Listing)
