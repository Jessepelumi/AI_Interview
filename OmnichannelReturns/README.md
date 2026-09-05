# Omnichannel Returns

Contributed by Jesse.

Suggested time: 100–130 minutes.

This service handles web orders returned through stores or warehouses. It spans
catalogue data, inventory locations, order economics, return workflows, and
carrier label requests.

Read `INCIDENT.md`, `docs/RETURNS_API.md`, and `docs/CARRIER_CONTRACT.md`. Treat
stored order economics as the source of truth rather than recomputing the original
sale from today's catalogue.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py test
```

The starting failures are intentional. Keep return processing idempotent and
preserve the passing quantity controls.
