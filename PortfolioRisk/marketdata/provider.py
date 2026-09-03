from datetime import UTC, datetime
from decimal import Decimal

from instruments.models import Instrument

from .models import PriceSnapshot


class MarketDataAdapter:
    """Adapter for the documented provider millisecond timestamp contract."""

    def ingest(self, payload):
        instrument = Instrument.objects.get(symbol=payload["symbol"])
        observed_at = datetime.fromtimestamp(payload["timestamp_ms"] / 1000, tz=UTC)
        return PriceSnapshot.objects.create(
            instrument=instrument,
            price=Decimal(str(payload["price"])),
            observed_at=observed_at,
        )
