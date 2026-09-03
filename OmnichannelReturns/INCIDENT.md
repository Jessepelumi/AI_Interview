# Incident RET-774: Dublin store returns

## Summary

Dublin stores report that documented return requests receive HTTP 400 unless they
send an old internal field name. For accepted requests, stock is appearing in the
original Belfast fulfilment warehouse rather than the store that physically
received it. Refunds on discounted multi-unit lines are also wrong.

The An Post label integration rejects some parcels as 750–1500 kg, and Irish
returns are being routed to the global fallback carrier.

## Evidence

```text
POST /api/returns reason_code=unwanted -> 400 reason required
return_location=DUB-01 stock_increment_location=BFS-WH
line_paid=61.50 returned_units=2/3 refund=40.00 expected=41.00
weight_grams=1500 outbound_weight_kg=1500.000
country=IE carrier=globalpost
```

## Acceptance criteria

- API field names match the documented public contract.
- Refunds proportionally allocate the actual paid line total, including discount
  and recorded tax, with half-up penny rounding.
- Saleable stock returns to the receiving location exactly once.
- Carrier weights are kilograms and routing uses uppercase ISO country codes.
- Over-return protection and product linkage remain correct.
