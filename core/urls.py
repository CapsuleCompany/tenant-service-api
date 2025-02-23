from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

urlpatterns = [
    path("api/services/", include("service.urls")),
    path("api/tenant/", include("tenant.urls")),
]

urlpatterns += [
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
        permission_classes([AllowAny])(SpectacularRedocView.as_view(url_name="schema")),
        name="redoc",
    ),
]
