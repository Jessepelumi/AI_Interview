# Incident SUB-650: paid customers lack features

## Summary

Billing migrations introduced two providers. Some Adyen invoice events are
reported as duplicates of unrelated Stripe events, so customers remain past due.
Successful EUR 12.99 payments also appear internally as EUR 1,299.00.

Dublin customers whose subscriptions end on a local calendar date retain access
for part of the following morning during summer. SDK consumers report that plan
responses no longer contain the documented `key` property. Provider webhooks
signed according to the current documentation receive HTTP 401.

## Evidence

```text
provider=adyen event=evt_shared duplicate_of_provider=stripe
amount_minor=1299 stored_amount=1299.00
customer_tz=Europe/Dublin local=2026-06-01T00:30 utc_date=2026-05-31 access=true
GET /api/plans/growth feature={"feature_code":"exports"}
header=X-Billing-Signature response=401
```

## Acceptance criteria

- Public plan features use `key`.
- Billing signatures are read from `X-Billing-Signature`.
- Event uniqueness is `(provider, external_event_id)`.
- Minor units are divided by 100 using decimal arithmetic.
- Calendar expiry is evaluated in the customer's IANA time zone.
- Atomicity, same-provider retries, and plan limits continue to work.
