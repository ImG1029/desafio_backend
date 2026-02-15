from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PetWriteSerializer, PetReadSerializer
from .services import PetService
from ..accounts.permissions import ResourcePermission


class PetListCreateView(APIView):
    permission_classes = [IsAuthenticated, ResourcePermission]
    queryset = PetService.list_pets()

    def get(self, request):
        pets = PetService.list_pets()

        serialier = PetReadSerializer(
            pets,
            many=True
        )

        return Response(serialier.data)

    def post(self, request):
        serializer = PetWriteSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        pet = PetService.create_pet(
            serializer.validated_data
        )

        output = PetReadSerializer(pet)

        return Response(
            output.data,
            status=status.HTTP_201_CREATED
        )

class PetDetailView(APIView):
    permission_classes = [IsAuthenticated, ResourcePermission]
    queryset = PetService.list_pets()

    def get(self, request, pk):
        pet = PetService.retrieve_pet(pk)

        serializer = PetReadSerializer(pet)
        return Response(serializer.data)

    def put(self, request, pk):
        pet = PetService.retrieve_pet(pk)

        serializer = PetWriteSerializer(
            instance=pet,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        updated_pet = PetService.update_pet(
            pet,
            serializer.validated_data
        )

        output = PetReadSerializer(updated_pet)

        return Response(
            output.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):
        pet = PetService.retrieve_pet(pk)

        serializer = PetWriteSerializer(
            instance=pet,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        updated_pet = PetService.update_pet(
            pet,
            serializer.validated_data
        )

        output = PetReadSerializer(updated_pet)

        return Response(
            output.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        pet = PetService.retrieve_pet(pk)
        PetService.delete_pet(pet)

        return Response(status=status.HTTP_204_NO_CONTENT)
