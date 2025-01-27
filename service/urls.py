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
    ServiceListView,
    ServiceDetailView,
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

    # Services
    path(
        "<int:provider_id>/",
        ServiceListView.as_view(),
        name="provider-service-list",
    ),
    path(
        "<int:provider_id>/services/<int:id>/",
        ServiceDetailView.as_view(),
        name="service-detail",
    ),

    # Service Options
    path(
        "<int:provider_id>/services/<int:service_id>/options/",
        ServiceOptionListView.as_view(),
        name="service-option-list-create",
    ),
    path(
        "<int:provider_id>/services/<int:service_id>/options/<int:option_id>/",
        ServiceOptionDetailView.as_view(),
        name="service-option-detail",
    ),

    # Service Option Values
    path(
        "<int:provider_id>/services/<int:service_id>/options/<int:option_id>/values/",
        ServiceOptionValueListView.as_view(),
        name="service-option-value-list-create",
    ),
    path(
        "<int:provider_id>/services/<int:service_id>/options/<int:option_id>/values/<int:value_id>/",
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