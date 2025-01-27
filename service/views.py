from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Provider, Service, ServiceOption, ServiceOptionValue
from .serializers import (
    ProviderSerializer,
    ServiceSerializer,
    ServiceOptionSerializer,
    ServiceOptionValueSerializer,
)


# Custom Permissions
class IsProviderOrCarrier(permissions.BasePermission):
    """
    Custom permission to allow only providers or carriers to perform restricted actions.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_provider_or_carrier


# Provider Views
class ProviderListCreateView(generics.ListCreateAPIView):
    """
    List and create providers for the authenticated user.
    """
    serializer_class = ProviderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Provider.objects.filter(user_id=self.request.user.user_id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.user_id)


# Service Views
class ServiceListView(generics.ListAPIView):
    """
    List services for a specific provider.
    Unauthenticated users see publicly available services.
    Authenticated providers or carriers see all services and can manage them.
    """
    serializer_class = ServiceSerializer

    def get_queryset(self):
        provider = get_object_or_404(Provider, id=self.kwargs["provider_id"])
        if self.request.user.is_authenticated and self.request.user.user_id == provider.user_id:
            # Authenticated provider sees all services
            return Service.objects.filter(provider=provider)
        # Unauthenticated or other users see only public services
        return Service.objects.filter(provider=provider, is_public=True)


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific service.
    Only the provider or carrier can update or delete a service.
    """
    serializer_class = ServiceSerializer
    permission_classes = [IsProviderOrCarrier]

    def get_queryset(self):
        return Service.objects.filter(provider_id=self.kwargs["provider_id"])


# Service Option Views
class ServiceOptionListView(generics.ListCreateAPIView):
    """
    List and create service options for a specific service.
    Unauthenticated users see publicly available options.
    Authenticated providers or carriers can manage options.
    """
    serializer_class = ServiceOptionSerializer

    def get_queryset(self):
        service = get_object_or_404(Service, id=self.kwargs["service_id"])
        if self.request.user.is_authenticated and self.request.user.user_id == service.provider.user_id:
            # Authenticated provider sees all options
            return ServiceOption.objects.filter(service=service)
        # Unauthenticated or other users see only public options
        return ServiceOption.objects.filter(service=service, is_public=True)

    def perform_create(self, serializer):
        service = get_object_or_404(Service, id=self.kwargs["service_id"])
        serializer.save(service=service)


class ServiceOptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific service option.
    Only the provider or carrier can update or delete an option.
    """
    serializer_class = ServiceOptionSerializer
    permission_classes = [IsProviderOrCarrier]

    def get_queryset(self):
        return ServiceOption.objects.filter(service_id=self.kwargs["service_id"])


# Service Option Value Views
class ServiceOptionValueListView(generics.ListCreateAPIView):
    """
    List and create service option values for a specific option.
    Unauthenticated users see public values.
    Authenticated providers or carriers can manage values.
    """
    serializer_class = ServiceOptionValueSerializer

    def get_queryset(self):
        option = get_object_or_404(ServiceOption, id=self.kwargs["option_id"])
        if self.request.user.is_authenticated and self.request.user.user_id == option.service.provider.user_id:
            # Authenticated provider sees all values
            return ServiceOptionValue.objects.filter(option=option)
        # Unauthenticated or other users see only public values
        return ServiceOptionValue.objects.filter(option=option, is_public=True)

    def perform_create(self, serializer):
        option = get_object_or_404(ServiceOption, id=self.kwargs["option_id"])
        serializer.save(option=option)


class ServiceOptionValueDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific service option value.
    Only the provider or carrier can update or delete a value.
    """
    serializer_class = ServiceOptionValueSerializer
    permission_classes = [IsProviderOrCarrier]

    def get_queryset(self):
        return ServiceOptionValue.objects.filter(option_id=self.kwargs["option_id"])