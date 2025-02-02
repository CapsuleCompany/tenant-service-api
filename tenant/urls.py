from django.urls import path
from .views import (
    TenantListCreateView,
    TenantLocationListCreateView
)

urlpatterns = [
    # Tenants
    path(
        "",
        TenantListCreateView.as_view(),
        name="provider-list-create",
    ),
    path(
        "<uuid:provider_id>/locations/",
        TenantLocationListCreateView.as_view(),
        name="provider-location-list-create",
    ),]