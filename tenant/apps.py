from django.apps import AppConfig
from django.db.models.signals import pre_migrate
from django.db import connection


class TenantConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tenant"

    def ready(self):
        import tenant.signals

        pre_migrate.connect(create_schema, sender=self)


def create_schema(sender, **kwargs):
    schema_name = "tenant_api"
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")
