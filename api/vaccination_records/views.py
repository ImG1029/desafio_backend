from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import VaccinationRecordReadSerializer, VaccinationRecordCreateSerializer
from .services import VaccinationRecordService
from ..accounts.permissions import IsRecordOwnerOrAdmin, IsVeterinarian


class VaccinationRecordListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsRecordOwnerOrAdmin]

    def get(self, request):
        records = VaccinationRecordService.list_vaccine_records()
        serializer = VaccinationRecordReadSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VaccinationRecordCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            account = request.user.accounts
        except:
            return Response(
                {"detail": "User account not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data
        validated_data['veterinarian'] = account

        vaccine = VaccinationRecordService.create_vaccination_record(
            serializer.validated_data
        )

        output = VaccinationRecordReadSerializer(vaccine)
        return Response(
            output.data,
            status=status.HTTP_201_CREATED
        )

class VaccinationRecordDetailView(APIView):
    permission_classes = [IsAuthenticated, IsRecordOwnerOrAdmin]

    def get(self, request, pk):
        record = VaccinationRecordService.retrieve_vaccination_record(pk)

        serializer = VaccinationRecordReadSerializer(record)
        return Response(serializer.data)

    def put(self, request, pk):
        record = VaccinationRecordService.retrieve_vaccination_record(pk)

        self.check_object_permissions(request, record)

        serializer = VaccinationRecordCreateSerializer(
            instance=record,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        validated_data.pop('veterinarian', None)

        updated_vaccination_record = VaccinationRecordService.update_vaccination_record(
            record,
            serializer.validated_data
        )

        output = VaccinationRecordReadSerializer(updated_vaccination_record)

        return Response(
            output.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):
        record = VaccinationRecordService.retrieve_vaccination_record(pk)

        self.check_object_permissions(request, record)

        serializer = VaccinationRecordCreateSerializer(
            instance=record,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        validated_data.pop('veterinarian', None)

        updated_vaccination_record = VaccinationRecordService.update_vaccination_record(
            record,
            serializer.validated_data
        )

        output = VaccinationRecordReadSerializer(updated_vaccination_record)

        return Response(
            output.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        if not request.user.is_superuser:
            return Response(
                {"detail": "Only administrators can delete vaccination records."},
                status=status.HTTP_403_FORBIDDEN
            )

        record = VaccinationRecordService.retrieve_vaccination_record(pk)
        VaccinationRecordService.delete_vaccination_record(record)

        return Response(status=status.HTTP_204_NO_CONTENT)