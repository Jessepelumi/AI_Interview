from django.db import models
class MarketRate(models.Model):
    base_currency = models.CharField(max_length=3)
    quote_currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=20, decimal_places=10)
    observed_at = models.DateTimeField()
    provider = models.CharField(max_length=40, default="primary")
    class Meta:
        ordering = ["-observed_at"]
