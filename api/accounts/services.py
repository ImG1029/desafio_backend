from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.generics import get_object_or_404

from .models import Account

class AccountService:
    @staticmethod
    def create_account(validated_data):
        license_number = validated_data.pop('license_number', None)

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        account = Account.objects.create(
            user=user,
            license_number=license_number if license_number else None
        )

        return account

    @staticmethod
    def retrieve_account(pk: int):
        account = get_object_or_404(
            Account.objects.select_related("user"),
            pk=pk
        )
        return account

    @staticmethod
    def list_accounts():
        return Account.objects.select_related("user").all()

    @staticmethod
    def update_account(instance, validated_data):
        user = instance.user

        updated = False

        user_fields = ["username", "first_name", "last_name"]
        for field in user_fields:
            if field in validated_data:
                setattr(user, field, validated_data[field])
                user.save()
                updated = True

        if "license_number" in validated_data and validated_data["license_number"] != instance.license_number:
            instance.license_number = validated_data["license_number"]
            instance.save()
            updated = True

        if not updated:
            raise ValidationError("No change!")

        return instance

    @staticmethod
    def delete_account(instance):
        instance.user.is_active = False
        instance.user.save()

    @staticmethod
    def get_account_by_user(user):
        if not hasattr(user, 'account'):
            raise ValidationError("User account not found")

        return user.account

    @staticmethod
    def authenticate_user(username, password):
        user = authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials")

        if not user.is_active:
            raise AuthenticationFailed("Account is deactivated")

        try:
            account = user.accounts
        except Account.DoesNotExist:
            raise AuthenticationFailed("Account not found")

        return user, account