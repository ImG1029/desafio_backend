from django.db import models

from api.owners.models import Owner


class Pet(models.Model):
    name = models.CharField(max_length=255, blank=False)
    species = models.CharField(max_length=255, blank=False)
    breed = models.CharField(max_length=255, blank=False)
    birth_date = models.DateField(blank=True)

    owner = models.ForeignKey(
        Owner,
        on_delete=models.PROTECT,
        related_name="pets"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pets"

    def __str__(self):
        return f"{self.name} ({self.species})"
