import uuid

from django.db import models

from customers.models import Organisation


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, related_name="accounts"
    )
    currency = models.CharField(max_length=3, default="EUR")
    available_balance = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return f"{self.organisation} {self.currency}"
