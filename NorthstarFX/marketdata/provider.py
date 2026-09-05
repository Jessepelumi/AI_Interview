from dataclasses import dataclass
from decimal import Decimal
from django.utils import timezone
from .models import MarketRate

@dataclass(frozen=True)
class Rate:
    value: Decimal
    observed_at: object

class DatabaseRateProvider:
    def get_rate(self, sell_currency, buy_currency):
        direct = MarketRate.objects.filter(base_currency=sell_currency, quote_currency=buy_currency).first()
        if direct:
            return Rate(direct.rate, direct.observed_at)
        inverse = MarketRate.objects.filter(base_currency=buy_currency, quote_currency=sell_currency).first()
        if not inverse:
            raise LookupError("No market rate available")
        return Rate(inverse.rate, inverse.observed_at)
