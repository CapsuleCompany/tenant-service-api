from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .views import ProviderView, ServiceView

urlpatterns = [
    # Business logic endpoints
    path('providers/', ProviderView.as_view(), name='provider-list'),
    path('providers/<int:provider_id>/services/', ServiceView.as_view(), name='service-list'),

    # OpenAPI Schema
    path('schema/', permission_classes([AllowAny])(SpectacularAPIView.as_view()), name='schema'),

    # Swagger UI
    path('docs/', permission_classes([AllowAny])(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger-ui'),

    # Redoc UI
    path('redoc/', permission_classes([AllowAny])(SpectacularRedocView.as_view(url_name='schema')), name='redoc'),
]
