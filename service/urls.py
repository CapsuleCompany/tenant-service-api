from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ServiceViewSet, ServiceOptionViewSet

router = DefaultRouter()
router.register(r"", ServiceViewSet, basename="service")

services_router = NestedDefaultRouter(router, r"", lookup="service")
services_router.register(r"options", ServiceOptionViewSet, basename="service-options")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(services_router.urls)),
]