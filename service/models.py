import requests
from django.db import models
from common.models import BaseModel
from django.conf import settings


class Service(BaseModel):
    """
    Represents a service offered by a provider.
    """

    tenant = models.ForeignKey(
        "tenant.Tenant",
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
        help_text="Image representing the service.",
    )
    duration_minutes = models.PositiveIntegerField(
        null=True, blank=True, help_text="Duration of the service in minutes."
    )
    is_public = models.BooleanField(default=False)

    class Meta:
        db_table = "Service"

    def __str__(self):
        return self.name


class ServiceLocation(BaseModel):
    """
    Represents a specific location where a service is offered, including its range,
    availability, and integration with external scheduling and location services.
    """

    service = models.ForeignKey(
        "Service",
        on_delete=models.CASCADE,
        related_name="service_locations",
        help_text="The service offered at this location.",
    )
    location = models.ForeignKey(
        "tenant.TenantLocation",
        on_delete=models.CASCADE,
        related_name="service_locations",
        help_text="The location where this service is available.",
    )
    service_range_mi = models.FloatField(
        default=10.0, help_text="Service range in miles from this location."
    )
    availability_start = models.TimeField(
        null=True, blank=True, help_text="Service availability start time."
    )
    availability_end = models.TimeField(
        null=True, blank=True, help_text="Service availability end time."
    )
    external_schedule_id = models.UUIDField(
        null=True, blank=True, help_text="Reference to the scheduling system."
    )
    external_location_id = models.UUIDField(
        null=True, blank=True, help_text="Reference to the location service."
    )

    class Meta:
        db_table = "ServiceLocation"

    def __str__(self):
        return f"{self.service.name} at {self.location}"

    def get_availability(self):
        """
        Fetch availability data from the scheduling service.
        """
        if not self.external_schedule_id:
            return {"error": "No external schedule ID provided."}

        url = f"{settings.SCHEDULE_SERVICE_URL}/api/availability/{self.external_schedule_id}/"
        response = requests.get(url, headers={"Authorization": f"Bearer {settings.SERVICE_API_KEY}"})

        if response.status_code == 200:
            return response.json()
        return {"error": "Failed to fetch availability.", "status": response.status_code}

    def get_address(self):
        """
        Fetch address details from the location service.
        """
        if not self.external_location_id:
            return {"error": "No external location ID provided."}

        url = f"{settings.LOCATION_SERVICE_URL}/api/locations/{self.external_location_id}/"
        response = requests.get(url, headers={"Authorization": f"Bearer {settings.SERVICE_API_KEY}"})

        if response.status_code == 200:
            return response.json()
        return {"error": "Failed to fetch location details.", "status": response.status_code}


class ServiceOption(BaseModel):
    """
    Represents customizable options for a service.
    """

    service = models.ForeignKey(
        "Service", on_delete=models.CASCADE, related_name="options"
    )
    name = models.CharField(
        max_length=255, help_text="Name of the option (e.g., 'Choose a size')."
    )
    is_required = models.BooleanField(
        default=False, help_text="Indicates if this option is required."
    )
    max_selections = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Maximum number of selections allowed for this option.",
    )

    class Meta:
        db_table = "ServiceOption"

    def __str__(self):
        return f"{self.name} (Service: {self.service.name})"


class ServiceOptionValue(BaseModel):
    """
    Represents individual values for a service option.
    """

    option = models.ForeignKey(
        "ServiceOption", on_delete=models.CASCADE, related_name="values"
    )
    name = models.CharField(
        max_length=255, help_text="Name of the value (e.g., 'Large', 'Medium')."
    )
    additional_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Additional price for this option value.",
    )

    class Meta:
        db_table = "ServiceOptionValue"

    def __str__(self):
        return f"{self.name} (Option: {self.option.name})"
