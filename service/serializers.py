from rest_framework import serializers
from .models import Service, Booking, Payment
from datetime import timezone


class ServiceSerializer(serializers.ModelSerializer):
    provider_id = serializers.CharField(read_only=True)  # Ensure provider_id is read-only

    class Meta:
        model = Service
        fields = ['id', 'provider_id', 'name', 'description', 'price', 'created_at', 'updated_at']


class BookingSerializer(serializers.ModelSerializer):
    client_id = serializers.CharField(read_only=True)  # Ensure client_id is read-only

    class Meta:
        model = Booking
        fields = ['id', 'service', 'client_id', 'date', 'time', 'status', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Ensure the booking date and time are valid.
        """
        if data['date'] < timezone.now().date():
            raise serializers.ValidationError("Booking date cannot be in the past.")
        return data


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'booking', 'amount', 'status', 'transaction_id', 'created_at', 'updated_at']
