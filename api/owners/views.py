from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import OwnerCreateSerializer, OwnerReadSerializer, OwnerUpdateSerializer
from .services import OwnerService

class OwnerListCreateView(APIView):
    def get(self, request):
        owners = OwnerService.list_owners()

        serializer = OwnerReadSerializer(
            owners,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = OwnerCreateSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        owner = OwnerService.create_owner(
            serializer.validated_data
        )

        output = OwnerReadSerializer(owner)

        return Response(
            output.data,
            status=status.HTTP_201_CREATED
        )

class OwnerDetailView(APIView):
    def get(self, request, owner_id):
        owner = OwnerService.retrieve_owner(owner_id)

        serializer = OwnerReadSerializer(owner)
        return Response(serializer.data)

    def put(self, request, owner_id):
        serializer = OwnerUpdateSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        owner = OwnerService.update_owner(
            owner_id,
            serializer.validated_data
        )

        output = OwnerReadSerializer(owner)

        return Response(output.data)

    def delete(self, request, owner_id):
        OwnerService.delete_owner(owner_id=owner_id)

        return Response(status=status.HTTP_204_NO_CONTENT)