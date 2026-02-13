from rest_framework import serializers
from .models import Pet


class PetCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    species = serializers.CharField(max_length=255)
    breed = serializers.CharField(max_length=255)
    birth_date = serializers.DateField()

class PetReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = [
            "name",
            "species",
            "breed",
            "birth_date"
        ]

class PetOwnerUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    species = serializers.CharField(max_length=255)
    breed = serializers.CharField(max_length=255)
    birth_date = serializers.DateField()