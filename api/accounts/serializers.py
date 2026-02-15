from rest_framework import serializers
from .models import Account


class AccountReadSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = Account
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "license_number",
            "created_at",
        ]
        read_only_fields = ['id', 'created_at']

class AccountRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)

    license_number = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
    )

class AccountUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=False, allow_blank=True)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
