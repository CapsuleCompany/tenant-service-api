from django.db import models
from common.models import BaseModel


class Tenant(BaseModel):
    """
    Represents a service provider managed by a team of users.
    """

    user_id = models.CharField(
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


class TenantTeam(BaseModel):
    """
    Represents a team member with specific roles for a provider.
    """

    provider = models.ForeignKey(
        "tenant.Tenant",
        on_delete=models.CASCADE,
        related_name="team_members",
        help_text="The provider this team member belongs to.",
    )
    user_id = models.CharField(
        max_length=255,
        help_text="The ID of the user (from the user microservice).",
    )
    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("staff", "Staff"),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="staff",
        help_text="Role of the team member within the provider.",
    )

    class Meta:
        db_table = "Team"

    def __str__(self):
        return f"{self.user_id} ({self.role}) - {self.provider.name}"


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
    address = models.TextField(
        blank=True, help_text="Human-readable address for the location."
    )

    class Meta:
        db_table = "Location"

    def __str__(self):
        return f"Location {self.location_id} for {self.provider.name}"


class Role(BaseModel):
    """
    Represents a role assigned to users within a provider's team.
    """

    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Name of the role (e.g., 'Owner', 'Admin', 'Staff').",
    )
    description = models.TextField(
        blank=True,
        help_text="A description of the role and its responsibilities.",
    )
    is_custom = models.BooleanField(
        default=False,
        help_text="Indicates if the role is a custom role created by the provider.",
    )
    created_by = models.ForeignKey(
        "tenant.TenantTeam",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_roles",
        help_text="The team member who created the custom role.",
    )

    class Meta:
        db_table = "Role"
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.name