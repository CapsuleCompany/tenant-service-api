from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .views import ProviderView, ServiceView, ServiceOptionView, ServiceOptionValueView


urlpatterns = [
    # Business logic endpoints
    path("providers/", ProviderView.as_view(), name="provider-list"),
    path(
        "providers/<int:provider_id>/services/",
        ServiceView.as_view(),
        name="service-list",
    ),
    path(
        "services/<int:service_id>/options/",
        ServiceOptionView.as_view(),
        name="service-option-list-create",
    ),
    path(
        "services/<int:service_id>/options/<int:option_id>/",
        ServiceOptionView.as_view(),
        name="service-option-detail",
    ),
    path(
        "options/<int:option_id>/values/",
        ServiceOptionValueView.as_view(),
        name="service-option-value-list-create",
    ),
    path(
        "options/<int:option_id>/values/<int:value_id>/",
        ServiceOptionValueView.as_view(),
        name="service-option-value-detail",
    ),
    # OpenAPI Schema
    path(
        "schema/",
        permission_classes([AllowAny])(SpectacularAPIView.as_view()),
        name="schema",
    ),
    path(
        "docs/",
        permission_classes([AllowAny])(
            SpectacularSwaggerView.as_view(url_name="schema")
        ),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        permission_classes([AllowAny])(SpectacularRedocView.as_view(url_name="schema")),
        name="redoc",
    ),
]
