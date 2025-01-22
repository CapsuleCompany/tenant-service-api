from rest_framework import routers
from .views import ServiceViewSet, BookingViewSet, PaymentViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'bookings', BookingViewSet, basename='bookings')
router.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = [
    path('api/', include(router.urls)),
]
