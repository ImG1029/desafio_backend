from django.db import models

class Owner(models.Model):
    name = models.CharField(max_length=255, blank=False)
    cpf = models.IntegerField(unique=True)
    email = models.EmailField(blank=True)
    phone_number = models.IntegerField(blank=False)
    address = models.CharField(max_length=255, blank=False)
    address_2 = models.IntegerField(blank=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table  = "owners"

    def __str__(self):
        return self.name