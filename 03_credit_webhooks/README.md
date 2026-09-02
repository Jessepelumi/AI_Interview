# Exercise 3: Account-credit webhooks

Suggested time: 45–60 minutes.

## Client report

A payment provider sends `credit.applied` webhooks with amounts in minor currency
units (pence/cents). Customers are receiving much larger balances than they paid
for. Support has also found that when a webhook arrives before the matching
account has replicated into this service, retrying the same event later does not
apply the credit.

The provider can deliver the same event more than once, so idempotency must remain
intact.

## Contract

- `data.amount_minor` is an integer number of pence/cents; account balances are
  stored in major units with two decimal places.
- A successfully applied provider event changes the balance exactly once.
- Duplicate delivery of an already processed event is a no-op.
- If processing raises before completion, no partial event record or balance
  change is committed; a later delivery of that event can succeed.
- Successful events have a non-null `processed_at` timestamp.
- Keep the public result object and webhook response shape unchanged.

## Task

Trace the failures through the webhook view and service, then make the smallest
safe fix. Add at least one test for a monetary or retry edge case. Do not weaken
the unique event constraint.

Run the suite with:

```bash
python manage.py test
```

Do not read the top-level `_interviewer_notes` until you want the solution.

