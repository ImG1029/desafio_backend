from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import VaccineWriteSerializer, VaccineReadSerializer
from .services import VaccineService
from ..accounts.permissions import ResourcePermission


class VaccineListCreateView(APIView):
    permission_classes = [IsAuthenticated, ResourcePermission]
    queryset = VaccineService.list_vaccines()

    def get(self, request):
        vaccines = VaccineService.list_vaccines()
        serializer = VaccineReadSerializer(vaccines, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VaccineWriteSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        vaccine = VaccineService.create_vaccine(
            serializer.validated_data
        )

        output = VaccineReadSerializer(vaccine)
        return Response(
            output.data,
            status=status.HTTP_201_CREATED
        )

class VaccineDetailView(APIView):
    permission_classes = [IsAuthenticated, ResourcePermission]
    queryset = VaccineService.list_vaccines()
    def get(self, request, pk):
        vaccine = VaccineService.retrieve_vaccine(pk)

        serializer = VaccineReadSerializer(vaccine)
        return Response(serializer.data)

    def put(self, request, pk):
        vaccine = VaccineService.retrieve_vaccine(pk)

        serializer = VaccineWriteSerializer(
            instance=vaccine,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        updated_vaccine = VaccineService.update_vaccine(
            vaccine,
            serializer.validated_data
        )

        output = VaccineReadSerializer(updated_vaccine)

        return Response(
            output.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):
        vaccine = VaccineService.retrieve_vaccine(pk)

        serializer = VaccineWriteSerializer(
            instance=vaccine,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        updated_vaccine = VaccineService.update_vaccine(
            vaccine,
            serializer.validated_data
        )

        output = VaccineReadSerializer(updated_vaccine)

        return Response(
            output.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        vaccine = VaccineService.retrieve_vaccine(pk)
        VaccineService.delete_vaccine(vaccine)

        return Response(status=status.HTTP_204_NO_CONTENT)