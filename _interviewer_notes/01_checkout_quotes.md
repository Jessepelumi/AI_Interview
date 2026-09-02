# Interviewer notes: Checkout quote totals

## Intended defects

Both defects are in `quotes/services.py`.

1. The subtotal generator adds each unit price once and ignores
   `item["quantity"]`.
2. `Decimal.quantize()` uses the active decimal context (normally
   `ROUND_HALF_EVEN`) because no rounding mode is supplied. The written contract
   requires `ROUND_HALF_UP`.

An appropriately narrow repair multiplies each unit price by the quantity and
passes `rounding=ROUND_HALF_UP` when quantizing the discount. No view or model
change is required.

## Useful candidate-added tests

- mixed quantities with a coupon, proving the discount is calculated after the
  complete subtotal;
- quantity zero/negative input, accompanied by a clear decision about which
  layer owns validation;
- a value just below a half-penny boundary.

## Evaluation signals

Strong candidates trace the HTTP symptom into the service, retain `Decimal`,
explain why float would be unsafe, avoid special-casing fixture values, and run
the complete suite after the fix.

