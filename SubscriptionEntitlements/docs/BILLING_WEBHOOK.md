# Billing webhook v2

`POST /webhooks/billing/{provider}/` uses the lowercase provider slug and the
hexadecimal HMAC-SHA256 signature in `X-Billing-Signature`.

`amount_minor` is an integer count of minor units. Event IDs are unique only
within one provider. Processing must atomically create the event, payment, status
change, and processed timestamp; a same-provider retry is a no-op.

`Subscription.ends_on` is inclusive in the customer's local calendar. At local
midnight after that date, access is expired.
