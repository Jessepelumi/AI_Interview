from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from django.core.cache import cache
from .models import Quote
from marketdata.provider import DatabaseRateProvider

def _rate_key(sell_currency, buy_currency):
    return f"rate:{sell_currency}"

def priced_rate(customer, sell_currency, buy_currency, provider=None):
    provider = provider or DatabaseRateProvider()
    key = _rate_key(sell_currency, buy_currency)
    raw = cache.get(key)
    if raw is None:
        raw = provider.get_rate(sell_currency, buy_currency).value
        cache.set(key, str(raw), timeout=settings.QUOTE_TTL_SECONDS)
    raw = Decimal(raw)
    return raw * (Decimal("1") - Decimal(customer.markup_bps) / Decimal("10000"))

def create_quote(customer, sell_currency, buy_currency, sell_amount, provider=None):
    rate = priced_rate(customer, sell_currency.upper(), buy_currency.upper(), provider)
    buy_amount = Decimal(str(float(sell_amount) * float(rate))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return Quote.objects.create(customer=customer, sell_currency=sell_currency.upper(), buy_currency=buy_currency.upper(),
        sell_amount=sell_amount, buy_amount=buy_amount, rate=rate, expires_at=datetime.now() + timedelta(seconds=settings.QUOTE_TTL_SECONDS))
