from django.urls import path, include

urlpatterns = [
    path("service/", include("service.urls")),
]
