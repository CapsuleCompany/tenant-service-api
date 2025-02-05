from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from .serializers import (
    TenantSerializer,
    TenantLocationSerializer,
)
from .models import Tenant


class TenantViewSet(viewsets.ModelViewSet):
    """
    List and create Tenants for the authenticated user.
    """

    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tenant.objects.all()

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."}, status=401
            )
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()


class TenantLocationView(viewsets.ModelViewSet):
    """
    List and create locations for a specific Tenant.
    """

    serializer_class = TenantLocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TenantLocation.objects.filter(
            provider__user_id=self.request.user.user_id
        )

    def perform_create(self, serializer):
        provider = get_object_or_404(Tenant, id=self.kwargs["provider_id"])
        serializer.save(provider=provider)
