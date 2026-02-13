from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PetCreateSerializer, PetReadSerializer, PetOwnerUpdateSerializer
from .services import PetService

class PetListCreateView(APIView):
    def get(self, request):
        pets = PetService.list_pets()

        serialier = PetReadSerializer(
            pets,
            many=True
        )

        return Response(serialier.data)

    def post(self, request):
        serializer = PetCreateSerializer(
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
    def get(self, request, pet_id):
        pet = PetService.retrieve_pet(pet_id)

        serializer = PetReadSerializer(pet)
        return Response(serializer.data)

    def put(self, request, pet_id):
        serializer = PetCreateSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        pet = PetService.update_pet(
            pet_id,
            serializer.validated_data
        )

        output = PetReadSerializer(pet)

        return Response(
            output.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pet_id):
        PetService.delete_pet(pet_id)

        return Response(status=status.HTTP_204_NO_CONTENT)
