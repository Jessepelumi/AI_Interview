# Debugging Interview Lab

This repository contains independent, intentionally defective Django codebases.
Each exercise models a production-maintenance interview: understand an unfamiliar
system, infer the intended behaviour, locate the defect, make the smallest correct
change, and prove the repair with tests.

## Repository rule

The `main` branch is problem-only. It must always contain the unsolved version of
every exercise.

- New problems may be contributed to `main` through a pull request.
- Solutions must never be committed or merged into `main`.
- Solve an exercise on a separate branch in your fork. A local uncommitted
  solution is also fine, although creating a branch first is safer.
- Private answer keys or solution notes belong in the ignored `.solutions/`
  directory, not in tracked files.

## Exercises

Every exercise directory uses only the PascalCase problem name, for example
`BookingRace`. Contributor attribution belongs in the exercise README and the
table below rather than in the folder name.

| Exercise | Contributor | Primary surface | Suggested time |
| --- | --- | --- | ---: |
| [`CheckoutQuotes`](CheckoutQuotes/) | Jesse | Business rules, money and rounding | 30–40 minutes |
| [`ClinicAvailability`](ClinicAvailability/) | Jesse | ORM aggregation and tenant isolation | 40–50 minutes |
| [`CreditWebhooks`](CreditWebhooks/) | Jesse | Transactions, units and safe retries | 45–60 minutes |
| [`NorthstarFX`](NorthstarFX/) | Tony | FX pricing, caching and idempotent booking | 75–100 minutes |
| [`MeridianDisputes`](MeridianDisputes/) | Tony | Card disputes, audit and processor callbacks | 60 minutes |
| [`DublinTransfers`](DublinTransfers/) | Jesse | Banking transfers, regional settlement and scoped idempotency | 90–120 minutes |
| [`PortfolioRisk`](PortfolioRisk/) | Jesse | Quant/trading risk, market data and desk isolation | 100–130 minutes |
| [`CreatorPublishing`](CreatorPublishing/) | Jesse | Social scheduling, moderation and tenant integrations | 90–120 minutes |
| [`OmnichannelReturns`](OmnichannelReturns/) | Jesse | Retail refunds, inventory and carrier routing | 100–130 minutes |
| [`SubscriptionEntitlements`](SubscriptionEntitlements/) | Jesse | Billing webhooks, plan serialization and regional access | 110–140 minutes |

## Solve an exercise

Fork and clone the repository, then enter the exercise you want to solve. From
inside that codebase, update `main` and create a dedicated solution branch before
editing:

```bash
cd CheckoutQuotes
git switch main
git pull --ff-only
git switch -c your_name/solvecheckoutquotes
```

Replace `your_name` with your name or account handle. Solution branches follow
`<contributor_name>/solve<codebasename>` in lowercase.

Git branches apply to the entire repository even when created from an exercise
directory. Working from inside the selected codebase simply keeps the session
focused on that exercise.

Create a local virtual environment and install the exercise's dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Establish the starting failure before changing production code:

```bash
python manage.py test
```

The starting suite is intentionally not green. After repairing the defect, the
complete exercise suite should pass. Add at least one regression or edge-case
test, then commit only to your solution branch. Do not open a solution pull
request against `main`.

If you want to share a solution, push the solution branch to your fork and share
a link to that branch without merging it into the upstream repository.

## Contribute a new problem

Problem contributions are welcome on `main`.

1. Fork the repository and branch from the latest unsolved `main`:

   ```bash
   git switch main
   git pull --ff-only
   git switch -c your_name/addbookingrace
   ```

2. Add one self-contained directory named only for the problem in PascalCase,
   for example `BookingRace`. Choose a unique, descriptive name.

3. Include, at minimum:

   - a project `README.md` crediting the contributor and containing the client
     report, behavioural contract, suggested time, setup steps, and task;
   - the application code and migrations needed to run from a fresh clone;
   - a local `requirements.txt` with pinned dependencies;
   - deterministic tests that expose the intended defect;
   - at least one passing control test, so the project is demonstrably runnable.

4. Keep the exercise realistic and bounded. The intended repair should normally
   fit within a 30–60 minute interview and should not require network services,
   private credentials, or paid APIs.

5. Verify the clean starting state. Record the number and names of expected
   failures in the pull-request description. Failures must come from the exercise,
   not from missing dependencies, broken migrations, or invalid scaffolding.

6. Submit the unsolved codebase in a pull request to `main`. Do not include the
   fix, an answer key, a solution patch, revealing code comments, or generated
   files such as databases and `__pycache__` directories.

Reviewers should validate the proposed repair privately on a temporary branch or
worktree, then discard it before merging only the unsolved problem into `main`.

Because failures are intentional, do not add a root CI job that expects every
exercise suite to pass. Repository-level validation should check setup, Django
configuration and migrations, then compare each exercise with its documented
expected failures. A permanently red default-branch check hides genuine breakage.

## Contribution checklist

Before requesting review, confirm that:

- the directory is a unique PascalCase problem name such as `BookingRace`;
- the exercise README identifies its contributor;
- setup works from a fresh virtual environment;
- Django system checks and migrations are valid;
- the documented failing tests fail for the intended business defect;
- unaffected/control tests pass;
- no solution or answer key is tracked; and
- no existing exercise was renamed or reformatted unnecessarily.

## Interview rules

1. Treat tests and acceptance criteria as evidence, not as permission to
   hard-code their examples.
2. Do not change an assertion merely to make the suite green. If a test appears
   wrong, explain the contract conflict first.
3. Prefer the smallest production-code change that handles the general case.
4. Add at least one useful test beyond the supplied regression tests.
5. Finish by explaining the root cause, why the fix is safe, and what production
   risk remains.

## Bounded AI assistance

An interviewer can allow AI while preserving the signal by requiring candidates
to drive the investigation, keep a short prompt log, reject suggestions they
cannot explain, write or improve at least one test themselves, and present the
final root-cause and risk analysis unaided.
