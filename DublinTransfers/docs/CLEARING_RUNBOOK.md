# Clearing and configuration runbook

`BANK_FEE_BPS_BY_COUNTRY` is keyed by uppercase ISO country code. Current values:
Ireland 15 bps, Great Britain 20 bps, fallback 30 bps.

The clearing cutoff is 17:00 in the organisation's configured IANA time zone.
It is not a fixed UTC hour: `Europe/Dublin` moves between UTC and UTC+1. Requests
at or after cutoff settle on the next weekday. Public holidays are outside this
exercise's scope.

The downstream request builder must receive a whitespace-free uppercase IBAN,
two-decimal amount string, ISO execution date, and account currency.
