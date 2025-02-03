from django.db import models
from common.models import BaseModel
import uuid


class Tenant(BaseModel):
    """
    Represents a service provider managed by a team of users.
    """

    user_id = models.UUIDField(
        max_length=255,
        help_text="The ID of the primary user managing this provider (obtained from JWT).",
    )
    name = models.CharField(
        max_length=255, help_text="Name of the provider (e.g., business name)."
    )
    description = models.TextField(
        blank=True, help_text="A description of the provider's business."
    )
    logo = models.CharField(
        max_length=255, blank=True, null=True, help_text="Logo of the provider."
    )
    contact_email = models.EmailField(
        blank=True, help_text="Contact email for this provider."
    )
    phone_number = models.CharField(
        max_length=15, blank=True, help_text="Contact phone number for the provider."
    )
    is_disabled = models.BooleanField(
        default=False, help_text="Indicates whether the provider is disabled."
    )

    class Meta:
        db_table = "Organization"

    def __str__(self):
        return self.name


class TenantLocation(BaseModel):
    """
    Represents a location associated with a provider.
    """

    provider = models.ForeignKey(
        "tenant.Tenant",
        on_delete=models.CASCADE,
        related_name="locations",
        help_text="The provider this location belongs to.",
    )
    location_id = models.UUIDField(
        help_text="A reference to the location in the location service."
    )

    class Meta:
        db_table = "Location"

    def __str__(self):
        return f"Location {self.location_id} for {self.provider.name}"


class TenantPlan(models.Model):
    tenant = models.OneToOneField("Tenant", on_delete=models.CASCADE, related_name="plan")
    plan_name = models.CharField(max_length=50, help_text="Plan name")
    max_users = models.IntegerField(default=1)
    max_storage_gb = models.IntegerField(default=10)
    custom_roles = models.BooleanField(default=False)
    feature_flags = models.JSONField(default=dict, help_text="Custom feature toggles for this plan.")


class TenantRole(models.Model):
    """
    Defines roles within a tenant. This allows for custom role creation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="roles")
    name = models.CharField(max_length=50, help_text="Custom role name")
    permissions = models.JSONField(default=dict, help_text="Permissions associated with this role")

    class Meta:
        db_table = "TenantRoles"
        unique_together = ("tenant", "name")

    def __str__(self):
        return f"{self.tenant.name} - {self.name}"

