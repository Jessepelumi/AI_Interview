from decimal import Decimal
from django.db import models
from accounts.models import Organisation

class Payment(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.PROTECT)
    processor_reference = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.CharField(max_length=3)
    captured_at = models.DateTimeField()
    refundable_amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0"))
