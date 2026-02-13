from django.shortcuts import get_object_or_404
from .models import Pet

class PetService:
    @staticmethod
    def create_pet(validated_data):
        pet = Pet.objects.create(**validated_data)
        return pet

    @staticmethod
    def retrieve_pet(pet_id):
        pet = get_object_or_404(Pet, id=pet_id)
        return pet

    @staticmethod
    def list_pets():
        return Pet.objects.all()

    @staticmethod
    def update_pet(pet_id, validated_data):
        pet = get_object_or_404(Pet, id=pet_id)

        for field, value in validated_data.items():
            setattr(pet, field, value)

        pet.save()
        return pet

    @staticmethod
    def delete_pet(pet_id):
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()