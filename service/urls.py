from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .views import (
    ProviderListCreateView,
    ProviderLocationListCreateView,
    ServiceListView,
    ServiceDetailView,
    ServiceLocationListCreateView,
    ServiceOptionListView,
    ServiceOptionDetailView,
    ServiceOptionValueListView,
    ServiceOptionValueDetailView,
)

urlpatterns = [
    # Providers
    path(
        "",
        ProviderListCreateView.as_view(),
        name="provider-list-create",
    ),
    path(
        "<uuid:provider_id>/locations/",
        ProviderLocationListCreateView.as_view(),
        name="provider-location-list-create",
    ),

    # Services
    path(
        "<uuid:provider_id>/",
        ServiceListView.as_view(),
        name="provider-service-list",
    ),
    path(
        "<uuid:provider_id>/services/<uuid:id>/",
        ServiceDetailView.as_view(),
        name="service-detail",
    ),
    path(
        "<uuid:provider_id>/services/<uuid:service_id>/locations/",
        ServiceLocationListCreateView.as_view(),
        name="service-location-list-create",
    ),

    # Service Options
    path(
        "<uuid:provider_id>/services/<uuid:service_id>/options/",
        ServiceOptionListView.as_view(),
        name="service-option-list-create",
    ),
    path(
        "<uuid:provider_id>/services/<uuid:service_id>/options/<uuid:option_id>/",
        ServiceOptionDetailView.as_view(),
        name="service-option-detail",
    ),

    # Service Option Values
    path(
        "<uuid:provider_id>/services/<uuid:service_id>/options/<uuid:option_id>/values/",
        ServiceOptionValueListView.as_view(),
        name="service-option-value-list-create",
    ),
    path(
        "<uuid:provider_id>/services/<uuid:service_id>/options/<uuid:option_id>/values/<uuid:value_id>/",
        ServiceOptionValueDetailView.as_view(),
        name="service-option-value-detail",
    ),

    # OpenAPI Schema
    path(
        "api/schema/",
        permission_classes([AllowAny])(SpectacularAPIView.as_view()),
        name="schema",
    ),
    path(
        "api/docs/",
        permission_classes([AllowAny])(
            SpectacularSwaggerView.as_view(url_name="schema")
        ),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        permission_classes([AllowAny])(
            SpectacularRedocView.as_view(url_name="schema")
        ),
        name="redoc",
    ),
]