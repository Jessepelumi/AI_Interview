# Exercise 1: Checkout quote totals

Contributed by Jesse.

Suggested time: 30–40 minutes.

## Client report

The checkout team reports that quote totals are too low when a basket contains
more than one unit of a product. Finance has also found occasional one-penny
differences on percentage coupons.

The issue is visible through `POST /api/quotes/`, but the pricing rules live below
the HTTP layer.

## Contract

- A line total is the product's unit price multiplied by the requested quantity.
- The subtotal is the sum of all line totals.
- An active percentage coupon is applied once to the complete subtotal.
- Monetary results use two decimal places and conventional `ROUND_HALF_UP`
  rounding. For example, a raw discount of `0.005` becomes `0.01`.
- An inactive coupon has no effect.
- Existing response field names and string-formatted money values are public API.

## Task

Reproduce the failures, identify the root cause or causes, and make the smallest
correct production change. Keep existing passing behaviour intact and add at
least one test for an edge case you consider important.

Run the suite with:

```bash
python manage.py test
```

Solutions are intentionally not stored on `main`. Create a separate branch in
your fork before making changes.
