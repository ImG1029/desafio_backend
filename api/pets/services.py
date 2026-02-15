from django.shortcuts import get_object_or_404
from .models import Pet

class PetService:
    @staticmethod
    def create_pet(validated_data):
        pet = Pet.objects.create(**validated_data)
        return pet

    @staticmethod
    def retrieve_pet(pk: int):
        pet = get_object_or_404(
            Pet.objects.select_related("owner"),
            pk=pk
        )
        return pet

    @staticmethod
    def list_pets():
        return Pet.objects.select_related("owner").all()

    @staticmethod
    def update_pet(instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance

    @staticmethod
    def delete_pet(instance):
        instance.delete()