from django.db import models

from api.accounts.models import Account
from api.pets.models import Pet
from api.vaccines.models import Vaccine


class VaccinationRecord(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.PROTECT,
        related_name="vaccination_records"
    )

    vaccine = models.ForeignKey(
        Vaccine,
        on_delete=models.PROTECT,
        related_name="vaccination_records"
    )

    veterinarian = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="vaccination_records"
    )

    vaccinated_at = models.DateTimeField(auto_now_add=True)
    next_dose_recommendation = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "vaccination_records"
        ordering = ["-vaccinated_at"]

    def __str__(self):
        return f"{self.pet.name} - {self.vaccine.name} on {self.vaccinated_at.date()}"


