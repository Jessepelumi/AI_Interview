# Portfolio Risk

Contributed by Jesse.

Suggested time: 100–130 minutes.

This service accepts trader orders and performs synchronous pre-trade notional
checks using reference data, portfolio ownership, and provider market prices.

Read `INCIDENT.md`, `docs/ORDER_API.md`, and `docs/MARKET_DATA.md` before making a
change. The model stores compact exchange-style values while the API exposes a
human-readable contract; do not assume they are interchangeable.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py test
```

The initial suite contains deliberate failures and passing controls. Preserve
idempotency and risk-limit behaviour while resolving all incident symptoms.
