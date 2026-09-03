from django.db import models

from customers.models import Organisation


class Beneficiary(models.Model):
    organisation = models.ForeignKey(
        Organisation, on_delete=models.CASCADE, related_name="beneficiaries"
    )
    name = models.CharField(max_length=120)
    iban = models.CharField(max_length=34)
    bank_country = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.name} ({self.iban[-4:]})"
