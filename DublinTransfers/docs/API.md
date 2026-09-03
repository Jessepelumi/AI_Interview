# Transfers API v2

## Create beneficiary

`POST /api/beneficiaries/`

```json
{
  "organisation_id": 184,
  "name": "Printer Repairs",
  "iban": "IE64IRCE92050112345678",
  "bank_country": "IE"
}
```

The response uses the same fields plus `id`. The deprecated v1 name
`account_number` is not accepted or returned by v2.

## Create transfer

`POST /api/accounts/{account_id}/transfers/`

```json
{
  "beneficiary_id": 42,
  "amount": "250.00",
  "client_reference": "mobile-101"
}
```

The same account and client reference must return the original logical transfer.
Different accounts may independently use the same client reference.
