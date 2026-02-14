from django.shortcuts import get_object_or_404

from .models import Vaccine

class VaccineService:
    @staticmethod
    def create_vaccine(validated_data):
        vaccine = Vaccine.objects.create(**validated_data)
        return vaccine

    @staticmethod
    def retrieve_vaccine(pk: int):
        vaccine = get_object_or_404(
            Vaccine,
            pk=pk
        )
        return vaccine

    @staticmethod
    def list_vaccines():
        return Vaccine.objects.all()

    @staticmethod
    def update_vaccine(instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance

    @staticmethod
    def delete_vaccine(instance):
        instance.delete()