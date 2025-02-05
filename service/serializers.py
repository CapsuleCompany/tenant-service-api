from rest_framework import serializers
from .models import (
    Service,
    ServiceLocation,
    ServiceOption,
    ServiceOptionValue,
)


class ServiceLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceLocation
        fields = [
            "id",
            "service",
            "location",
            "service_range_mi",
            "availability_start",
            "availability_end",
        ]
        read_only_fields = ["id"]


class ServiceOptionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOptionValue
        fields = [
            "id",
            "name",
            "additional_price",
        ]
        read_only_fields = ["id"]


class ServiceOptionSerializer(serializers.ModelSerializer):
    values = ServiceOptionValueSerializer(many=True)

    class Meta:
        model = ServiceOption
        fields = ["id", "service", "name", "is_required", "max_selections", "values"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        values_data = validated_data.pop("values", [])
        service_option = ServiceOption.objects.create(**validated_data)
        for value_data in values_data:
            ServiceOptionValue.objects.create(option=service_option, **value_data)
        return service_option

    def update(self, instance, validated_data):
        values_data = validated_data.pop("values", [])
        instance.name = validated_data.get("name", instance.name)
        instance.is_required = validated_data.get("is_required", instance.is_required)
        instance.max_selections = validated_data.get("max_selections", instance.max_selections)
        instance.save()

        # Handle updating, creating, and deleting option values
        existing_ids = {value.id for value in instance.values.all()}
        received_ids = {value_data.get("id") for value_data in values_data if "id" in value_data}

        # Delete values not present in the update request
        ServiceOptionValue.objects.filter(option=instance, id__in=existing_ids - received_ids).delete()

        for value_data in values_data:
            value_id = value_data.get("id", None)
            if value_id:
                value_instance = ServiceOptionValue.objects.get(id=value_id, option=instance)
                for attr, value in value_data.items():
                    setattr(value_instance, attr, value)
                value_instance.save()
            else:
                ServiceOptionValue.objects.create(option=instance, **value_data)

        return instance


class ServiceSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            "id",
            "tenant",
            "name",
            "category",
            "description",
            "price",
            "is_available",
            "max_clients_per_slot",
            "image",
            "duration_minutes",
            "is_public",
            "options",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_options(self, obj):
        """
        Return service options only in the detail view.
        """
        request = self.context.get("request")
        if request and request.parser_context.get("kwargs", {}).get("pk"):
            options = ServiceOption.objects.filter(service=obj)
            return ServiceOptionSerializer(options, many=True).data
        return None

    def create(self, validated_data):
        service = Service.objects.create(**validated_data)
        return service

    def update(self, instance, validated_data):
        options_data = validated_data.pop("options", [])
        instance.name = validated_data.get("name", instance.name)
        instance.category = validated_data.get("category", instance.category)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.is_available = validated_data.get(
            "is_available", instance.is_available
        )
        instance.max_clients_per_slot = validated_data.get(
            "max_clients_per_slot", instance.max_clients_per_slot
        )
        instance.image = validated_data.get("image", instance.image)
        instance.duration_minutes = validated_data.get(
            "duration_minutes", instance.duration_minutes
        )
        instance.save()

        # Update or create service options
        for option_data in options_data:
            option_id = option_data.get("id", None)
            if option_id:
                option_instance = ServiceOption.objects.get(
                    id=option_id, service=instance
                )
                option_serializer = ServiceOptionSerializer(
                    option_instance, data=option_data, partial=True
                )
                option_serializer.is_valid(raise_exception=True)
                option_serializer.save()
            else:
                self.fields["options"].create(option_data)
        return instance
