from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Service, Booking, Payment
from .serializers import ServiceSerializer, BookingSerializer, PaymentSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.user_id
        queryset = Service.objects.filter(provider_id=user_id)
        if not queryset.exists():
            return Service.objects.none()
        return queryset

    def perform_create(self, serializer):
        # Set the provider_id to the logged-in user's ID
        user_id = self.request.user.user_id
        serializer.save(provider_id=user_id)


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Allow users to view bookings where they are the client
        user_id = self.request.user.user_id
        return Booking.objects.filter(client_id=user_id)

    def perform_create(self, serializer):
        # Set the client_id to the logged-in user's ID
        user_id = self.request.user.user_id

        service = serializer.validated_data['service']
        if service.provider_id == user_id:
            raise PermissionDenied("You cannot book your own service.")
        serializer.save(client_id=user_id)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Allow users to view payments for bookings they made
        user_id = self.request.user.user_id
        return Payment.objects.filter(booking__client_id=user_id)
