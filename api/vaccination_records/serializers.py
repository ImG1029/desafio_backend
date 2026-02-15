from rest_framework import serializers
from .models import VaccinationRecord
from ..accounts.serializers import AccountReadSerializer
from ..pets.serializers import PetReadSerializer
from ..vaccines.serializers import VaccineReadSerializer


class VaccinationRecordReadSerializer(serializers.ModelSerializer):
    pet = PetReadSerializer(read_only=True)
    vaccine = VaccineReadSerializer(read_only=True)
    veterinarian = AccountReadSerializer(read_only=True)

    class Meta:
        model = VaccinationRecord
        fields = [
            'id',
            'pet',
            'vaccine',
            'veterinarian',
            'vaccinated_at',
            'next_dose_recommendation',
        ]
        read_only_fields = ['id', 'vaccinated_at']

class VaccinationRecordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccinationRecord
        fields = [
            'pet',
            'vaccine',
            'veterinarian',
            'next_dose_recommendation',
        ]

    def validate_pet(self, value):
        if not value:
            raise serializers.ValidationError("Pet is required")
        return value

    def validate_vaccine(self, value):
        if not value:
            raise serializers.ValidationError("Vaccine is required")
        return value

    def validate_veterinarian(self, value):
        if value and not value.user.is_active:
            raise serializers.ValidationError("Veterinarian account is not active")
        return value
