from django.core.management.base import BaseCommand
from tenant.models import TenantPlan

class Command(BaseCommand):
    help = "Delete all tenant plans"

    def handle(self, *args, **kwargs):
        TenantPlan.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("All tenant plans deleted successfully!"))