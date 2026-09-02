# Django debugging interview lab

This folder contains three independent, intentionally defective Django codebases.
Each one models the kind of maintenance task where a client reports incorrect
behaviour and the candidate must establish the contract, locate the defect, make
the smallest safe change, and prove it with tests.

## Exercises

| Exercise | Primary surface | Suggested time |
| --- | --- | ---: |
| `01_checkout_quotes` | Business rules, money and rounding | 30–40 minutes |
| `02_clinic_availability` | ORM aggregation and tenant isolation | 40–50 minutes |
| `03_credit_webhooks` | Transactions, units and safe retries | 45–60 minutes |

Each project is standalone. Start with its `README.md`; do not open
`_interviewer_notes` until you want the answer key.

## Common setup

Python 3.11 or newer is recommended. From this folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Then enter one exercise and run:

```bash
python manage.py test
```

The starting suites are expected to contain failures. A correctly repaired
exercise has a fully passing suite.

## Suggested interview rules

1. Treat tests and the written acceptance criteria as evidence, not as permission
   to hard-code their examples.
2. Do not change an assertion merely to make the suite green. If a test appears
   wrong, explain the contract conflict before changing it.
3. Prefer the smallest production-code change that covers the general case.
4. Add at least one useful test beyond the supplied regression tests.
5. Finish by explaining the root cause, why the fix is safe, and what remains a
   production risk.

## Bounded AI-assistance option

An interviewer can allow AI while preserving the signal by requiring the
candidate to:

- drive all investigation and choose which files or errors to share;
- keep a short log of prompts and resulting decisions;
- reject or amend suggestions they cannot explain;
- write or improve at least one test themselves; and
- give the final root-cause and risk explanation without AI.

