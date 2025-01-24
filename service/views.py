from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Provider, Service
from .serializers import ProviderSerializer, ServiceSerializer


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
        data['user_id'] = user_id
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
            return Response(
                [],
                status=status.HTTP_404_NOT_FOUND
            )

        services = Service.objects.filter(provider=provider)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, provider_id):
        user_id = request.user.user_id
        try:
            provider = Provider.objects.get(id=provider_id, user_id=user_id)
        except Provider.DoesNotExist:
            return Response(
                [],
                status=status.HTTP_404_NOT_FOUND
            )

        data = request.data.copy()
        data['provider'] = provider.id
        serializer = ServiceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
