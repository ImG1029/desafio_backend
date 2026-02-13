from django.db import models


class Pet(models.Model):
    name = models.CharField(max_length=255, blank=False)
    species = models.CharField(max_length=255, blank=False)
    breed = models.CharField(max_length=255, blank=False)
    birth_date = models.DateField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pets"

    def __str__(self):
        return self.name
