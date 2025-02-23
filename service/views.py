import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, status
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.decorators import action
from .models import (
    Service,
    ServiceOption,
    ServiceOptionValue,
    ServiceLocation,
)
from .serializers import (
    ServiceSerializer,
    ServiceOptionSerializer,
    ServiceOptionValueSerializer,
    ServiceLocationSerializer,
)


class IsTenantOrTeamMember(permissions.BasePermission):
    """
    Custom permission to allow only Tenants or their team members to perform restricted actions.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_id is not None


class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Service.objects.all()

    def get_serializer_context(self):
        """
        Pass request context to dynamically include options in detail view.
        """
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def partial_update(self, request, *args, **kwargs):
        """
        Allows partial update of a Service instance using PATCH.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceOptionViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceOptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Only return service options related to the provided service_id.
        """
        service_id = self.kwargs.get("service_pk")  # Get service ID from URL
        return ServiceOption.objects.filter(service_id=service_id)

    def perform_create(self, serializer):
        """
        Create a service option linked to a specific service.
        """
        service_id = self.kwargs.get("service_pk")
        service = get_object_or_404(Service, id=service_id)
        serializer.save(service=service)

    def partial_update(self, request, *args, **kwargs):
        """
        Handle PATCH requests to update a specific service option.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AvailableServicesView(APIView):
    """
    Retrieves all available services within a radius for an optional date/time.
    """

    def get(self, request):
        latitude = request.query_params.get("latitude")
        longitude = request.query_params.get("longitude")
        radius = request.query_params.get("radius", 10)  # Default to 10 miles
        date = request.query_params.get("date", None)
        time = request.query_params.get("time", None)

        if not latitude or not longitude:
            return Response(
                {"error": "Latitude and longitude are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Step 1: Fetch services in the given radius from location-service
            location_service_url = (
                f"{settings.LOCATION_SERVICE_URL}/api/locations/services"
            )
            location_params = {
                "latitude": latitude,
                "longitude": longitude,
                "radius": radius,
            }
            location_response = requests.get(
                location_service_url, params=location_params
            )

            if location_response.status_code != 200:
                return Response(
                    {"error": "Failed to fetch services from location-service."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            services = location_response.json()  # List of services with location info

            # Step 2: Filter services based on availability (if date/time provided)
            available_services = []
            if date and time:
                schedule_service_url = (
                    f"{settings.SCHEDULE_SERVICE_URL}/api/schedule/availability"
                )
                for service in services:
                    schedule_params = {
                        "service_id": service["id"],
                        "date": date,
                        "time": time,
                    }
                    schedule_response = requests.get(
                        schedule_service_url, params=schedule_params
                    )

                    if (
                        schedule_response.status_code == 200
                        and schedule_response.json().get("available")
                    ):
                        available_services.append(service)
            else:
                available_services = (
                    services  # If no date/time filter, return all services in range
                )

            # Step 3: Fetch additional details from tenant-service
            for service in available_services:
                tenant_service_url = f"{settings.TENANT_SERVICE_URL}/api/tenants/{service['tenant_id']}/services/{service['id']}"
                tenant_response = requests.get(tenant_service_url)

                if tenant_response.status_code == 200:
                    service["details"] = tenant_response.json()

            return Response(available_services, status=status.HTTP_200_OK)

        except requests.RequestException as e:
            return Response(
                {"error": f"Service request failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
