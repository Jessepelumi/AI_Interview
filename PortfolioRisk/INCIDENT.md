# Incident RISK-902: options exposure and stale-price controls

## Summary

The options desk found accepted orders whose displayed notional was 100 times
smaller than the broker notional. During the same review, a ten-second-old price
was accepted despite a five-second freshness policy. Sell tickets created through
the public API also increased rather than reduced signed exposure.

Security reported that a valid user could submit an order to a portfolio owned by
a desk they had not joined by changing the portfolio ID in the URL.

## Evidence

```text
symbol=ACME-C100 quantity=2 price=2.50 exposure=5.00 broker_notional=500.00
price_age=10.004 threshold=5000 result=fresh
api_side=SELL stored_side=SELL model_choices=[B,S] signed_exposure=+250.00
actor=outsider portfolio=US-Options response=201
```

## Acceptance criteria

- API `BUY`/`SELL` values map losslessly to the model's `B`/`S` codes.
- Signed exposure is negative for sells.
- Instrument contract multipliers apply to notional.
- `MAX_PRICE_AGE_MS` is interpreted in milliseconds.
- Only members of a portfolio's desk can submit orders to it.
- Fresh equity orders and provider timestamp ingestion continue to work.
