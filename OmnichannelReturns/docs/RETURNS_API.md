# Returns API

`POST /api/returns/`

```json
{
  "order_id": 1001,
  "receiving_location": "DUB-01",
  "reason_code": "unwanted",
  "lines": [{"order_line_id": 44, "quantity": 2}]
}
```

`reason_code` is public; `reason` and `units` are internal model names. A return
line must belong to the supplied order. The sum of completed/requested return
units cannot exceed purchased quantity.
