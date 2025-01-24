from .models import Provider, Service, ServiceOption, ServiceOptionValue
from .serializers import (
    ProviderSerializer,
    ServiceSerializer,
    ServiceOptionSerializer,
    ServiceOptionValueSerializer,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class ProviderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.user_id  # Assume user_id is populated via JWT
        providers = Provider.objects.filter(user_id=user_id)
        if not providers.exists():
            return Response([], status=status.HTTP_404_NOT_FOUND)
        serializer = ProviderSerializer(providers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user_id = request.user.user_id
        data = request.data.copy()
        data["user_id"] = user_id
        serializer = ProviderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, provider_id):
        user_id = request.user.user_id
        try:
            provider = Provider.objects.get(id=provider_id, user_id=user_id)
        except Provider.DoesNotExist:
            return Response([], status=status.HTTP_404_NOT_FOUND)

        services = Service.objects.filter(provider=provider)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, provider_id):
        user_id = request.user.user_id
        try:
            provider = Provider.objects.get(id=provider_id, user_id=user_id)
        except Provider.DoesNotExist:
            return Response([], status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data["provider"] = provider.id
        serializer = ServiceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceOptionView(APIView):
    """
    View to list, create, update, and delete service options.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, service_id=None, option_id=None):
        if option_id:
            # Retrieve a specific service option
            option = ServiceOption.objects.filter(
                id=option_id, service_id=service_id
            ).first()
            if not option:
                return Response(
                    {"detail": "Service option not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = ServiceOptionSerializer(option)
        else:
            # List all options for a service
            options = ServiceOption.objects.filter(service_id=service_id)
            serializer = ServiceOptionSerializer(options, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, service_id=None):
        # Attach the service_id to the request data
        data = request.data
        data["service"] = (
            service_id  # Associate the service option with the correct service
        )

        serializer = ServiceOptionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Save the service option
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, service_id=None, option_id=None):
        # Update an existing service option
        option = ServiceOption.objects.filter(
            id=option_id, service_id=service_id
        ).first()
        if not option:
            return Response(
                {"detail": "Service option not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ServiceOptionSerializer(option, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, service_id=None, option_id=None):
        # Delete a service option
        option = ServiceOption.objects.filter(
            id=option_id, service_id=service_id
        ).first()
        if not option:
            return Response(
                {"detail": "Service option not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        option.delete()
        return Response(
            {"detail": "Service option deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ServiceOptionValueView(APIView):
    """
    View to list, create, update, and delete service option values.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, option_id=None, value_id=None):
        if value_id:
            # Retrieve a specific service option value
            value = ServiceOptionValue.objects.filter(
                id=value_id, option_id=option_id
            ).first()
            if not value:
                return Response(
                    {"detail": "Service option value not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = ServiceOptionValueSerializer(value)
        else:
            # List all values for a service option
            values = ServiceOptionValue.objects.filter(option_id=option_id)
            serializer = ServiceOptionValueSerializer(values, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, option_id=None):
        # Create a new service option value
        data = request.data
        data["option"] = option_id  # Associate with the correct option
        serializer = ServiceOptionValueSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, option_id=None, value_id=None):
        # Update an existing service option value
        value = ServiceOptionValue.objects.filter(
            id=value_id, option_id=option_id
        ).first()
        if not value:
            return Response(
                {"detail": "Service option value not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ServiceOptionValueSerializer(
            value, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, option_id=None, value_id=None):
        # Delete a service option value
        value = ServiceOptionValue.objects.filter(
            id=value_id, option_id=option_id
        ).first()
        if not value:
            return Response(
                {"detail": "Service option value not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        value.delete()
        return Response(
            {"detail": "Service option value deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
