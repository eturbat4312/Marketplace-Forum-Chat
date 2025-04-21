from django.core.management.base import BaseCommand
from django.utils import timezone
from listings.models import Listing

class Command(BaseCommand):
    help = "Delete listings that have expired (older than 30 days)."

    def handle(self, *args, **options):
        now = timezone.now()
        expired_listings = Listing.objects.filter(expires_at__lt=now)
        count = expired_listings.count()
        expired_listings.delete()
        self.stdout.write(self.style.SUCCESS(f"Successfully deleted {count} expired listings."))
