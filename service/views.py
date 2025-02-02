from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
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


# Custom Permissions
class IsTenantOrTeamMember(permissions.BasePermission):
    """
    Custom permission to allow only Tenants or their team members to perform restricted actions.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_id is not None


# Service Views
class ServiceListView(generics.ListAPIView):
    """
    List services for a specific provider.
    Unauthenticated users see publicly available services.
    Authenticated providers or team members see all services and can manage them.
    """

    serializer_class = ServiceSerializer

    def get_queryset(self):
        provider = get_object_or_404(Tenant, id=self.kwargs["provider_id"])
        if (
            self.request.user.is_authenticated
            and self.request.user.user_id == provider.user_id
        ):
            return Service.objects.filter(provider=provider)
        return Service.objects.filter(provider=provider, is_public=True)


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific service.
    Unauthenticated users can retrieve the service details.
    Authenticated providers or team members can perform CRUD operations.
    """

    serializer_class = ServiceSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [IsTenantOrTeamMember()]

    def get_queryset(self):
        return Service.objects.filter(provider_id=self.kwargs["provider_id"])


# Service Location Views
class ServiceLocationListCreateView(generics.ListCreateAPIView):
    """
    List and create locations for a specific service.
    """

    serializer_class = ServiceLocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        service = get_object_or_404(Service, id=self.kwargs["service_id"])
        return ServiceLocation.objects.filter(service=service)

    def perform_create(self, serializer):
        service = get_object_or_404(Service, id=self.kwargs["service_id"])
        serializer.save(service=service)


# Service Option Views
class ServiceOptionListView(generics.ListCreateAPIView):
    """
    List and create service options for a specific service.
    """

    serializer_class = ServiceOptionSerializer

    def get_queryset(self):
        service = get_object_or_404(Service, id=self.kwargs["service_id"])
        return ServiceOption.objects.filter(service=service)

    def perform_create(self, serializer):
        service = get_object_or_404(Service, id=self.kwargs["service_id"])
        serializer.save(service=service)


class ServiceOptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific service option.
    """

    serializer_class = ServiceOptionSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [IsTenantOrTeamMember()]

    def get_queryset(self):
        return ServiceOption.objects.filter(service_id=self.kwargs["service_id"])


# Service Option Value Views
class ServiceOptionValueListView(generics.ListCreateAPIView):
    """
    List and create service option values for a specific option.
    """

    serializer_class = ServiceOptionValueSerializer

    def get_queryset(self):
        option = get_object_or_404(ServiceOption, id=self.kwargs["option_id"])
        return ServiceOptionValue.objects.filter(option=option)

    def perform_create(self, serializer):
        option = get_object_or_404(ServiceOption, id=self.kwargs["option_id"])
        serializer.save(option=option)


class ServiceOptionValueDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific service option value.
    """

    serializer_class = ServiceOptionValueSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [IsTenantOrTeamMember()]

    def get_queryset(self):
        return ServiceOptionValue.objects.filter(option_id=self.kwargs["option_id"])
