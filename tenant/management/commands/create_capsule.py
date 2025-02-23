from django.core.management.base import BaseCommand
from tenant.models import Tenant


# TODO: GET USER ID FROM USER SERVICE
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Tenant.objects.get_or_create(name="Capsule Company", defaults=plan)

        self.stdout.write(self.style.SUCCESS("Default plans created successfully!"))
