from django.conf import settings

from .models import PriceSnapshot


def latest_price(instrument):
    return PriceSnapshot.objects.filter(instrument=instrument).latest("observed_at")


def require_fresh(snapshot, as_of):
    age_ms = (as_of - snapshot.observed_at).total_seconds()
    if age_ms > settings.MAX_PRICE_AGE_MS:
        raise ValueError("market price is stale")
