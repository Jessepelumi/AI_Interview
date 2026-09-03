# Creator Publishing

Contributed by Jesse.

Suggested time: 90–120 minutes.

This multi-tenant service creates, moderates, schedules, and publishes social
posts through workspace-specific channel connections.

Start with `INCIDENT.md`, `docs/PUBLISHING_API.md`, and
`docs/MODERATION_PROVIDER.md`. The public vocabulary, internal model values, and
third-party vocabulary are deliberately separate contracts.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py test
```

The starting suite intentionally includes failures. Resolve the complete incident
without weakening workspace isolation or hard-coding seasonal offsets.
