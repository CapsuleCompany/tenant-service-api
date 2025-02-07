from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .serializers import (
    TenantSerializer,
    TenantLocationSerializer,
)
from .models import Tenant, TenantPlan
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError


class TenantViewSet(viewsets.ModelViewSet):
    """
    List and create Tenants for the authenticated user.
    """

    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Get all tenants owned by the authenticated user.
        """
        return Tenant.objects.filter(owner_id=self.request.user.id)

    def perform_create(self, serializer):
        """
        Restrict the number of tenants based on the user's plan.
        """
        user = self.request.user
        tenants = Tenant.objects.filter(owner_id=user.user_id)

        tenant_plan, created = TenantPlan.objects.get_or_create(
            tenant=tenants.first(),
            defaults={"plan_name": "Free", "max_users": 1, "max_tenants": 1},
        )

        if tenants.count() >= tenant_plan.max_tenants:
            raise ValidationError(
                {"error": f"Tenant creation limit reached for your current plan {tenants.count()}/{tenant_plan.max_tenants}."}
            )

        tenant = serializer.save(owner_id=user.user_id)

        if created:
            TenantPlan.objects.create(
                tenant=tenant,
                plan_name="Free",
                max_users=1,
                max_tenants=1,
                custom_roles=False,
            )


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
