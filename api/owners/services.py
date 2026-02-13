from django.shortcuts import get_object_or_404
from .models import Owner


class OwnerService:
    @staticmethod
    def create_owner(validated_data):

        owner = Owner.objects.create(**validated_data)
        return owner

    @staticmethod
    def update_owner(owner_id, validated_data):

        owner = get_object_or_404(Owner, id=owner_id)

        for field, value in validated_data.items():
            setattr(owner, field, value)

        owner.save()
        return owner

    @staticmethod
    def list_owners():
        return Owner.objects.all()

    @staticmethod
    def retrieve_owner(owner_id):
        owner = get_object_or_404(Owner, id=owner_id)
        return owner

    @staticmethod
    def delete_owner(owner_id):
        owner = get_object_or_404(Owner, id=owner_id)
        owner.delete()