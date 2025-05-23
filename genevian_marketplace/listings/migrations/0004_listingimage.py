# Generated by Django 5.1.6 on 2025-03-15 12:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("listings", "0003_category_listing_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="ListingImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="listing_images/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                (
                    "listing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="listings.listing",
                    ),
                ),
            ],
        ),
    ]
