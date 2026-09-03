from django.db import models

from accounts.models import Account
from beneficiaries.models import Beneficiary


class Transfer(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"

    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="transfers")
    beneficiary = models.ForeignKey(
        Beneficiary, on_delete=models.PROTECT, related_name="transfers"
    )
    client_reference = models.CharField(max_length=64, unique=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    requested_at = models.DateTimeField()
    settlement_date = models.DateField()
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.PENDING
    )

    def __str__(self):
        return self.client_reference
