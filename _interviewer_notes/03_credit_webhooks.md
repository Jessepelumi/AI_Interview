# Interviewer notes: Account-credit webhooks

## Intended defects

Both defects are in `credits/services.py`.

1. `amount_minor` is used directly as a major-unit decimal. It must be divided by
   `Decimal("100")` before changing the balance.
2. The idempotency record is committed before account lookup and balance update.
   If later processing raises, the event remains and its retry is misclassified as
   a duplicate. The event creation, balance update, and processed timestamp must
   share a `transaction.atomic()` boundary.

An appropriately narrow repair converts units and decorates/wraps
`apply_provider_event` in `transaction.atomic`. The unique constraint remains the
source of idempotency.

## Useful candidate-added tests

- a one-penny event and a zero-minor-unit event;
- an exception after the balance save, proving both balance and event roll back;
- two different event IDs both apply;
- malformed or negative amounts, accompanied by an explicit ownership decision
  about schema validation.

## Evaluation signals

Strong candidates distinguish idempotency from atomicity, explain why deleting a
stale event in an exception handler is less safe than rollback, preserve the
database uniqueness constraint, and notice/update the duplicate test's amount
expectation once units are corrected.
