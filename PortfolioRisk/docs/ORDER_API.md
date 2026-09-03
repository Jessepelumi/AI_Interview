# Order API contract

`POST /api/portfolios/{portfolio_id}/orders/`

```json
{
  "instrument": "ACME-C100",
  "side": "SELL",
  "quantity": "2.0000",
  "client_order_id": "terminal-8821"
}
```

The external side vocabulary is `BUY` and `SELL`. The database uses exchange
codes `B` and `S`; serializers own this boundary. `client_order_id` is idempotent
within a portfolio. A user outside the owning desk receives 404 so portfolio
existence is not disclosed.
