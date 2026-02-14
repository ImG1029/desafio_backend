from django.db import models

class Vaccine(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    recommended_interval_days = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "vaccines"

    def __str__(self):
        return self.name