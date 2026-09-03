# Meridian Disputes

Meridian is an operations service for card-payment disputes. Agents create cases against captured payments, attach evidence, submit cases, and receive asynchronous processor decisions.

## Architecture

The DRF API is split into organisation access (`accounts`), captured payments (`payments`), dispute workflows (`disputes`), append-only operational audit records (`audit`), and processor callbacks (`integrations`). PostgreSQL is the production store; SQLite is supported for local exercises.

## Setup

Requires Python 3.9+.

```bash
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

On macOS/Linux use `source .venv/bin/activate`. Run tests with `pytest` and configuration checks with `python manage.py check` and `python manage.py makemigrations --check`.

## Environment

`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `ALLOWED_HOSTS`, and `PROCESSOR_WEBHOOK_SECRET` configure the app. Set `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD` to use PostgreSQL; otherwise SQLite is used.

## Infrastructure and workers

`docker compose up -d db` starts PostgreSQL. This service has no separate worker: processor decisions arrive over `POST /webhooks/processor/`. Start the API with `python manage.py runserver`.
