from django.contrib.auth.models import User
from django.db import models

class Account(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="accounts",
    )
    license_number = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
    )

    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "accounts"

    def __str__(self):
        return f"{self.user.username} (License: {self.license_number})"
