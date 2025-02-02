from django.urls import path, include

urlpatterns = [
    path("api/services/", include("service.urls")),
    path("api/tenant/", include("tenant.urls")),
]
