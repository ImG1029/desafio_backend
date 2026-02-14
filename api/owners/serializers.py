from rest_framework import serializers
from .models import Owner
from ..pets.serializers import PetReadSerializer


class OwnerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    cpf = serializers.IntegerField(max_value=99999999999)
    email = serializers.EmailField()
    phone_number = serializers.IntegerField(min_value=1100000000, max_value=99999999999)
    address = serializers.CharField(max_length=255)
    address_2 = serializers.IntegerField()

class OwnerReadSerializer(serializers.ModelSerializer):
    pets = PetReadSerializer(many=True)
    class Meta:
        model = Owner
        fields = [
            "name",
            "cpf",
            "email",
            "phone_number",
            "address",
            "address_2",
            "created_at",
            "pets"
        ]

class OwnerUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone_number = serializers.IntegerField(min_value=1100000000, max_value=99999999999)
    address = serializers.CharField(max_length=255)
    address_2 = serializers.IntegerField()