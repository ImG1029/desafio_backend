from rest_framework import serializers
from .models import Pet
from ..owners.models import Owner


class PetWriteSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=Owner.objects.all()
    )
    class Meta:
        model = Pet
        fields = [
            "name",
            "species",
            "breed",
            "birth_date",
            "owner",
        ]

class PetReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "species",
            "breed",
            "birth_date",
            "owner",
            "created_at",
        ]