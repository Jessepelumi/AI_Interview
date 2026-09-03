# Incident PAY-4182: Irish transfers mispriced and delayed

## Customer impact

From 6 July, several Dublin business customers reported that transfers submitted
near the 17:00 local clearing cutoff were assigned the wrong settlement day.
Finance also found that some Irish customers were charged the international
fallback fee. Separately, a second current account reusing a mobile-app reference
received the first account's transfer response.

The beneficiary team reports a rise in HTTP 400 responses after clients migrated
to API v2, even though their requests match the published schema.

## Evidence

```text
org=184 country=IE fee_rule=DEFAULT amount=1000.00 fee=3.00
requested_at=2026-07-06T16:30:00Z settlement_date=2026-07-06
client_reference=mobile-101 account=8f... returned_account=31...
POST /api/beneficiaries/ {"iban":"IE64..."} -> 400 account_number required
```

## Expected behaviour

- Fee configuration uses ISO 3166-1 alpha-2 country codes exactly as documented.
- The 17:00 cutoff is evaluated in the account organisation's IANA time zone.
- Weekends are not settlement days.
- A client reference is idempotent within one debit account, not globally.
- The public beneficiary representation uses `iban`.
- A beneficiary cannot be used by another organisation.

Do not replace decimal money with float or special-case Dublin dates.
