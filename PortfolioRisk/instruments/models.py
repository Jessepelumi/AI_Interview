from django.db import models


class Instrument(models.Model):
    class AssetType(models.TextChoices):
        EQUITY = "equity", "Equity"
        OPTION = "option", "Option"
        FUTURE = "future", "Future"

    symbol = models.CharField(max_length=24, unique=True)
    asset_type = models.CharField(max_length=12, choices=AssetType.choices)
    quote_currency = models.CharField(max_length=3)
    contract_multiplier = models.DecimalField(
        max_digits=10, decimal_places=2, default=1
    )

    def __str__(self):
        return self.symbol
