from django.db import models


class Provider(models.Model):
    """
    Represents a service provider managed by a user.
    Since users are managed outside this microservice, we rely on `user_id` from JWT.
    """

    user_id = models.CharField(
        max_length=255,
        help_text="The ID of the user managing this provider (obtained from JWT).",
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
    address = models.UUIDField(
        null=True,
        blank=True,
        help_text="A reference to the provider's primary address in the location microservice.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Service(models.Model):
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
    predicted_category = models.CharField(
        max_length=50,
        blank=True,
        help_text="Category suggested by AI (can be overridden manually).",
    )
    description = models.TextField(blank=True, help_text="Description of the service.")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Price of the service."
    )
    is_available = models.BooleanField(
        default=True, help_text="Indicates whether the service is available."
    )
    availability_start = models.TimeField(
        null=True, blank=True, help_text="Service availability start time."
    )
    availability_end = models.TimeField(
        null=True, blank=True, help_text="Service availability end time."
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
    location = models.UUIDField(
        null=True,
        blank=True,
        help_text="Reference to the service location in the location microservice.",
    )
    service_range_mi = models.FloatField(
        null=True,
        blank=True,
        help_text="Service range in miles from the specified location.",
    )
    duration_minutes = models.PositiveIntegerField(
        null=True, blank=True, help_text="Duration of the service in minutes."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ServiceOption(models.Model):
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
        null=True,
        blank=True,
        help_text="Maximum number of selections allowed for this option.",
    )

    def __str__(self):
        return f"{self.name} (Service: {self.service.name})"


class ServiceOptionValue(models.Model):
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
        help_text="Additional price for this option value.",
    )

    def __str__(self):
        return f"{self.name} (Option: {self.option.name})"
