# Northstar FX Quotes

Northstar issues short-lived foreign-exchange quotes to business customers and books accepted quotes exactly once.

## Architecture

`marketdata` adapts provider rates, `quotes` applies customer pricing and caches hot pairs, `conversions` books accepted quotes, and `customers` owns access and markup configuration. PostgreSQL is the production database and Redis is the shared cache; local tests use SQLite and an in-memory cache.

## Setup and operation

Requires Python 3.9+.

```bash
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Run `pytest`, `python manage.py check`, and `python manage.py makemigrations --check` to validate a change. There is no separate worker in this service.

Set `DJANGO_SECRET_KEY`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `REDIS_URL`, and `QUOTE_TTL_SECONDS` as needed. Run `docker compose up -d` for PostgreSQL and Redis.
