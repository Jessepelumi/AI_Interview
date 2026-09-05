# Incident FX-2271: inconsistent executable quotes

## Customer report

During a volatile morning market, customers reported that EUR/USD and EUR/GBP quotes sometimes showed the same rate. A small number of accepted conversions were booked twice, while other requests unexpectedly returned an existing conversion belonging to a different quote. Support also saw intermittent server errors at the exact moment quotes expired.

## Expected behaviour

- A cached market rate belongs only to its ordered currency pair.
- Direct and inverse provider pairs result in economically equivalent prices.
- Money calculations are deterministic decimal calculations.
- Quote expiry is timezone-safe and consistent at the boundary.
- Booking is atomic and idempotent within the correct business scope.
- A user may quote and book only for accessible customers.

## Observed behaviour

```text
quote=21b... pair=EUR/USD rate=1.07123 cache=miss
quote=781... pair=EUR/GBP rate=1.07123 cache=hit
IntegrityError during conversion booking idempotency_key=mobile-441
TypeError: can't compare offset-naive and offset-aware datetimes
```

## Reproduction

Warm a EUR/USD quote, then request EUR/GBP for the same customer. Attempt two concurrent booking requests with the same key, and repeat at the quote's expiry boundary. Also try creating a quote for a customer not linked to the authenticated user.

## Acceptance criteria

- Ordered pair caching and inverse pricing are correct.
- Monetary output is stable at rounding boundaries.
- Creation and booking enforce customer access.
- Concurrent retries yield one conversion and a consistent response.
- Expiry behavior is defined and covered by tests.
- Listing remains performant with realistic customer data.
