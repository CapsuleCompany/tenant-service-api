from rest_framework import serializers
from .models import Provider, Service, ServiceOption, ServiceOptionValue


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = [
            "id",
            "name",
            "description",
            "logo",
            "contact_email",
            "phone_number",
            "address",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


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
        fields = "__all__"
        extra_kwargs = {
            "service": {"required": True},
        }
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
        instance.max_selections = validated_data.get(
            "max_selections", instance.max_selections
        )
        instance.save()

        # Update or create option values
        for value_data in values_data:
            value_id = value_data.get("id", None)
            if value_id:
                value_instance = ServiceOptionValue.objects.get(
                    id=value_id, option=instance
                )
                for attr, value in value_data.items():
                    setattr(value_instance, attr, value)
                value_instance.save()
            else:
                ServiceOptionValue.objects.create(option=instance, **value_data)
        return instance


class ServiceSerializer(serializers.ModelSerializer):
    options = ServiceOptionSerializer(many=True, required=False)

    class Meta:
        model = Service
        fields = [
            "id",
            "provider",
            "name",
            "category",
            "predicted_category",
            "description",
            "price",
            "is_available",
            "availability_start",
            "availability_end",
            "max_clients_per_slot",
            "image",
            "location",
            "service_range_mi",
            "duration_minutes",
            "options",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        options_data = validated_data.pop("options", [])
        service = Service.objects.create(**validated_data)
        for option_data in options_data:
            values_data = option_data.pop("values", [])
            service_option = ServiceOption.objects.create(
                service=service, **option_data
            )
            for value_data in values_data:
                ServiceOptionValue.objects.create(option=service_option, **value_data)
        return service

    def update(self, instance, validated_data):
        options_data = validated_data.pop("options", [])
        instance.name = validated_data.get("name", instance.name)
        instance.category = validated_data.get("category", instance.category)
        instance.predicted_category = validated_data.get(
            "predicted_category", instance.predicted_category
        )
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.is_available = validated_data.get(
            "is_available", instance.is_available
        )
        instance.availability_start = validated_data.get(
            "availability_start", instance.availability_start
        )
        instance.availability_end = validated_data.get(
            "availability_end", instance.availability_end
        )
        instance.max_clients_per_slot = validated_data.get(
            "max_clients_per_slot", instance.max_clients_per_slot
        )
        instance.image = validated_data.get("image", instance.image)
        instance.location = validated_data.get("location", instance.location)
        instance.service_range_mi = validated_data.get(
            "service_range_mi", instance.service_range_mi
        )
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
