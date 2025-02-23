from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .serializers import *
from .models import *
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
        return Tenant.objects.all()

    def perform_create(self, serializer):
        """
        Restrict tenant creation based on the user's plan.
        """
        user = self.request.user
        tenants = Tenant.objects.all()

        user_plan = TenantPlan.objects.get(name="Free")

        if tenants.count() >= user_plan.max_tenants:
            raise ValidationError(
                {
                    "error": f"Tenant creation limit reached for your current plan ({tenants.count()}/{user_plan.max_tenants})."
                }
            )

        serializer.save(owner_id=user, plan=user_plan)


class TenantLocationView(viewsets.ModelViewSet):
    """
    List and create locations for a specific Tenant.
    """

    serializer_class = TenantLocationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return TenantLocation.objects.filter(
            provider__user_id=self.request.user.user_id
        )

    def perform_create(self, serializer):
        provider = get_object_or_404(Tenant, id=self.kwargs["provider_id"])
        serializer.save(provider=provider)


class TenantPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Tenant Plans.
    """

    serializer_class = TenantPlanSerializer
    queryset = TenantPlan.objects.all()
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        tenants = self.get_queryset()
        serializer = self.get_serializer(tenants, many=True)
        return Response(serializer.data)
