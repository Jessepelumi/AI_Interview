# Skylark

## The Access That Would Not Leave

Contributed by Jesse.

Suggested time: 60–90 minutes.

Skylark is a collaborative document platform used by enterprise workspaces. You are the secondary on-call engineer for Identity & Content Access. A customer has reported that revoked collaborators can still retrieve or discover documents, while newly shared documents sometimes remain unavailable. Security has opened a priority incident.

This repository is intentionally broken. Treat it as a production investigation: reproduce the symptoms, write regression tests, then make the smallest coherent fixes. Do not weaken an assertion to make the suite pass.

## Architecture

- `organizations`: workspaces, memberships, and request authentication
- `directory`: workspace-scoped group membership resolution
- `documents`: document storage and the read API
- `sharing`: grants, authorization decisions, and ACL mutations
- `search_index`: asynchronously maintained search projection
- `exports`: queued document export jobs

The local test path uses SQLite, Django's in-memory cache, and direct calls to deterministic worker boundaries. Docker Compose provides PostgreSQL and Redis for final verification.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
pytest
```

Use PostgreSQL and Redis after the initial diagnosis:

```bash
cp .env.example .env
docker compose up -d db redis
docker compose run --rm api python manage.py migrate
docker compose run --rm api pytest
```

## Start here

1. Read `docs/incident-report.md` without opening the implementation.
2. Read `docs/api.md` and `docs/services.md`.
3. Run the complete test suite and group failures by observable behavior.
4. Trace one read request from URL resolution through authentication, view, authorization, directory resolution, ORM queries, and serialization.
5. Add a focused regression test before each implementation change.

## Useful commands

```bash
pytest
pytest tests/test_document_access.py -vv
pytest tests/test_group_isolation.py -vv
pytest tests/test_search_projection.py -vv
pytest tests/test_export_authorization.py -vv
python manage.py check
python manage.py makemigrations --check --dry-run
```

## Repository map

The top-level apps correspond to service ownership boundaries. `tests/` contains API and service-boundary tests; `docs/` contains the incident evidence and contracts. The repository intentionally has no solution notes, answer key, or marked bug locations.
