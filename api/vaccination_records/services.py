from datetime import timedelta

from django.shortcuts import get_object_or_404

from .models import VaccinationRecord

class VaccinationRecordService:
    @staticmethod
    def create_vaccination_record(validated_data):
        record = VaccinationRecord.objects.create(**validated_data)
        if not record.next_dose_recommendation and record.vaccine.recommended_interval_days:
            record.next_dose_recommendation = (
                    record.vaccinated_at.date() +
                    timedelta(days=record.vaccine.recommended_interval_days)
            )
            record.save()

        return record

    @staticmethod
    def retrieve_vaccination_record(pk: int):
        record = get_object_or_404(
            VaccinationRecord,
            pk=pk
        )
        return record

    @staticmethod
    def list_vaccine_records():
        return VaccinationRecord.objects.all()

    @staticmethod
    def update_vaccination_record(instance, validated_data):
        vaccine_changed = 'vaccine' in validated_data

        for field, value in validated_data.items():
            setattr(instance, field, value)

        if vaccine_changed and 'next_dose_recommendation' not in validated_data:
            if instance.vaccine.recommended_interval_days:
                instance.next_dose_recommendation = (
                        instance.vaccinated_at.date() +
                        timedelta(days=instance.vaccine.recommended_interval_days)
                )

        instance.save()
        return instance

    @staticmethod
    def delete_vaccination_record(instance):
        instance.delete()
