# Dublin Transfers

Contributed by Jesse.

Suggested time: 90–120 minutes.

This service creates domestic and SEPA transfers for business current accounts.
It is split across customer ownership, accounts, beneficiaries, transfer
orchestration, and the clearing-bank adapter.

## Start here

Read `INCIDENT.md`, then `docs/API.md` and `docs/CLEARING_RUNBOOK.md`. Establish
the complete test baseline before changing code. Several symptoms share a root
cause, while others do not.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py test
```

The starting suite intentionally has failures. Preserve the API contract and
same-account idempotency while making the smallest coherent production changes.
Add at least one test covering a boundary not already represented.
