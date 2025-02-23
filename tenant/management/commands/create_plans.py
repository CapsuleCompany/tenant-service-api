from django.core.management.base import BaseCommand
from tenant.models import TenantPlan


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        plans = [
            {"name": "Free", "max_users": 1, "max_tenants": 1},
            {"name": "Basic", "max_users": 10, "max_tenants": 5},
            {
                "name": "Premium",
                "max_users": 50,
                "max_tenants": 20,
                "custom_roles": True,
            },
        ]

        for plan in plans:
            TenantPlan.objects.get_or_create(name=plan["name"], defaults=plan)

        self.stdout.write(self.style.SUCCESS("Default plans created successfully!"))
