from rest_framework import serializers
from .models import *


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = [
            "id",
            "name",
            "description",
            "logo",
            "contact_email",
            "phone_number",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        return validated_data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        # TODO Check tenant limit
        validated_data["owner_id"] = user.user_id if user else None
        tenant, _ = Tenant.objects.get_or_create(**validated_data)
        return tenant

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class TenantLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantLocation
        fields = [
            "id",
            "provider",
            "location_id",
            "address",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class TenantPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantPlan
        fields = '__all__'
