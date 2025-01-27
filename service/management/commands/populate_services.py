from django.core.management.base import BaseCommand
from model_bakery import baker
from service.models import Provider, Service, ServiceOption, ServiceOptionValue
from . import progress_bar


class Command(BaseCommand):
    help = "Populate the database with sample providers, services, and options using bakery."

    def handle(self, *args, **options):
        # Delete existing data to avoid duplicates
        self.stdout.write("Clearing existing data...")
        Provider.objects.all().delete()
        Service.objects.all().delete()
        ServiceOption.objects.all().delete()
        ServiceOptionValue.objects.all().delete()

        # Define providers
        providers = [
            {
                "name": "Green Thumb Landscaping",
                "description": "Expert landscaping and lawn care services.",
                "user_id": 1,
                "contact_email": "greenthumb@example.com",
                "phone_number": "123-456-7890",
            },
            {
                "name": "QuickMove Services",
                "description": "Reliable moving and packing services.",
                "user_id": 1,
                "contact_email": "quickmove@example.com",
                "phone_number": "987-654-3210",
            },
            {
                "name": "Style Studio Salon",
                "description": "Professional hair and beauty services.",
                "user_id": 1,
                "contact_email": "stylestudio@example.com",
                "phone_number": "555-555-5555",
            },
        ]

        # Populate providers with progress bar
        self.stdout.write("Populating providers...")
        provider_instances = []
        for provider_data in progress_bar(
            providers, prefix="Providers", suffix="Complete", length=50
        ):
            provider_instances.append(baker.make(Provider, **provider_data))

        # Define services
        services = [
            {
                "provider": provider_instances[0],
                "name": "Lawn Mowing",
                "category": "Landscaping",
                "description": "Mow and edge your lawn to perfection.",
                "price": 50.00,
            },
            {
                "provider": provider_instances[0],
                "name": "Garden Maintenance",
                "category": "Landscaping",
                "description": "Keep your garden neat and healthy.",
                "price": 80.00,
            },
            {
                "provider": provider_instances[1],
                "name": "Local Moving",
                "category": "Moving",
                "description": "Move your belongings within the city.",
                "price": 150.00,
            },
            {
                "provider": provider_instances[1],
                "name": "Packing Service",
                "category": "Moving",
                "description": "Professional packing for a stress-free move.",
                "price": 75.00,
            },
            {
                "provider": provider_instances[2],
                "name": "Haircut",
                "category": "Hair Services",
                "description": "Get a fresh new look.",
                "price": 30.00,
            },
            {
                "provider": provider_instances[2],
                "name": "Hair Coloring",
                "category": "Hair Services",
                "description": "Professional hair coloring services.",
                "price": 100.00,
            },
        ]

        # Populate services with progress bar
        self.stdout.write("Populating services...")
        service_instances = []
        for service_data in progress_bar(
            services, prefix="Services", suffix="Complete", length=50
        ):
            service_instances.append(baker.make(Service, **service_data))

        # Define options and values
        options_and_values = [
            {
                "service": service_instances[0],
                "name": "Grass Height",
                "is_required": True,
                "max_selections": 1,
                "values": [
                    {"name": "Short", "additional_price": 0.00},
                    {"name": "Medium", "additional_price": 5.00},
                    {"name": "Tall", "additional_price": 10.00},
                ],
            },
            {
                "service": service_instances[1],
                "name": "Maintenance Type",
                "is_required": True,
                "max_selections": 1,
                "values": [
                    {"name": "Weeding", "additional_price": 20.00},
                    {"name": "Pruning", "additional_price": 15.00},
                ],
            },
            {
                "service": service_instances[4],
                "name": "Hair Length",
                "is_required": True,
                "max_selections": 1,
                "values": [
                    {"name": "Short", "additional_price": 0.00},
                    {"name": "Medium", "additional_price": 5.00},
                    {"name": "Long", "additional_price": 10.00},
                ],
            },
        ]

        # Populate options and values with progress bar
        self.stdout.write("Populating options and values...")
        for option_data in progress_bar(
            options_and_values, prefix="Options", suffix="Complete", length=50
        ):
            option = baker.make(
                ServiceOption,
                service=option_data["service"],
                name=option_data["name"],
                is_required=option_data["is_required"],
                max_selections=option_data["max_selections"],
            )
            for value_data in option_data["values"]:
                baker.make(ServiceOptionValue, option=option, **value_data)

        self.stdout.write(self.style.SUCCESS("Database populated successfully!"))
