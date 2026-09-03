from django.db import models

from instruments.models import Instrument


class PriceSnapshot(models.Model):
    instrument = models.ForeignKey(
        Instrument, on_delete=models.CASCADE, related_name="prices"
    )
    price = models.DecimalField(max_digits=18, decimal_places=6)
    observed_at = models.DateTimeField()

    class Meta:
        indexes = [models.Index(fields=["instrument", "-observed_at"])]
