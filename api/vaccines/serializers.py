from rest_framework import serializers
from .models import Vaccine

class VaccineWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = [
            "name",
            "type",
            "manufacturer",
            "recommended_interval_days"
        ]

class VaccineReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = [
            "id",
            "name",
            "type",
            "manufacturer",
            "recommended_interval_days",
            "created_at",
        ]