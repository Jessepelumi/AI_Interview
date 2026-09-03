# Subscription Entitlements

Contributed by Jesse.

Suggested time: 110–140 minutes.

This service exposes plan features, consumes billing-provider webhooks, records
payments, and answers entitlement checks for customers in multiple time zones.

Read `INCIDENT.md`, `docs/PLANS_API.md`, and `docs/BILLING_WEBHOOK.md`. Provider
identifiers are opaque and are not guaranteed unique across providers.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py test
```

The failing tests are deliberate. Preserve atomic processing and same-provider
idempotency while repairing all public-contract and entitlement defects.
