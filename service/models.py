from django.db import models
import uuid


class BaseModel(models.Model):
    """
    Base model with commonly needed fields for all models to inherit.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for each record."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The timestamp when this record was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The timestamp when this record was last updated."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates whether this record is active or not."
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Provider(BaseModel):
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

    def __str__(self):
        return self.name


class ProviderTeam(BaseModel):
    """
    Represents a team member with specific roles for a provider.
    """
    provider = models.ForeignKey(
        Provider,
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

    def __str__(self):
        return f"{self.user_id} ({self.role}) - {self.provider.name}"


class ProviderLocation(BaseModel):
    """
    Represents a location associated with a provider.
    """
    provider = models.ForeignKey(
        Provider,
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

    def __str__(self):
        return f"Location {self.location_id} for {self.provider.name}"


class Service(BaseModel):
    """
    Represents a service offered by a provider.
    """
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name="services",
        help_text="The provider offering this service.",
    )
    name = models.CharField(max_length=255, help_text="Name of the service.")
    category = models.CharField(
        max_length=50, default="other", help_text="Category of the service."
    )
    description = models.TextField(blank=True, help_text="Description of the service.")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Price of the service."
    )
    is_available = models.BooleanField(
        default=True, help_text="Indicates whether the service is available."
    )
    max_clients_per_slot = models.PositiveIntegerField(
        default=1, help_text="Maximum number of clients allowed per time slot."
    )
    image = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Image representing the service."
    )
    duration_minutes = models.PositiveIntegerField(
        null=True, blank=True, help_text="Duration of the service in minutes."
    )
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ServiceLocation(BaseModel):
    """
    Represents a specific location where a service is offered and its range.
    """
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="service_locations",
        help_text="The service offered at this location.",
    )
    location = models.ForeignKey(
        ProviderLocation,
        on_delete=models.CASCADE,
        related_name="service_locations",
        help_text="The location where this service is available.",
    )
    service_range_mi = models.FloatField(
        default=10.0,
        help_text="Service range in miles from this location."
    )
    availability_start = models.TimeField(
        null=True, blank=True, help_text="Service availability start time."
    )
    availability_end = models.TimeField(
        null=True, blank=True, help_text="Service availability end time."
    )

    def __str__(self):
        return f"{self.service.name} at {self.location}"


class ServiceOption(BaseModel):
    """
    Represents customizable options for a service.
    """
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="options"
    )
    name = models.CharField(
        max_length=255, help_text="Name of the option (e.g., 'Choose a size')."
    )
    is_required = models.BooleanField(
        default=False, help_text="Indicates if this option is required."
    )
    max_selections = models.PositiveIntegerField(
        null=True, blank=True, help_text="Maximum number of selections allowed for this option."
    )

    def __str__(self):
        return f"{self.name} (Service: {self.service.name})"


class ServiceOptionValue(BaseModel):
    """
    Represents individual values for a service option.
    """
    option = models.ForeignKey(
        ServiceOption, on_delete=models.CASCADE, related_name="values"
    )
    name = models.CharField(
        max_length=255, help_text="Name of the value (e.g., 'Large', 'Medium')."
    )
    additional_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Additional price for this option value."
    )

    def __str__(self):
        return f"{self.name} (Option: {self.option.name})"