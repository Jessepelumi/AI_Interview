# Incident SOCIAL-311: Dublin schedules drift and accounts cross

## Customer report

Dublin creators scheduling a 09:00 post during summer see publication at 10:00
local time. The problem is not reproduced in January. Moderation callbacks marked
`allow` are also producing rejected drafts after a provider API upgrade.

Security found that the post listing endpoint returns captions from workspaces the
authenticated user has never joined. The publishing worker sometimes receives
401 from the channel API for secondary workspaces even though their connection
tokens are current.

## Evidence

```text
workspace_tz=Europe/Dublin input=2026-06-15T09:00:00+01:00 stored=09:00:00Z
moderation_provider=allow internal_outcome=rejected
GET /api/posts actor=niamh workspace_ids=[12,91]
channel_workspace=91 auth_token_source=settings.SOCIAL_API_TOKEN response=401
```

## Acceptance criteria

- An aware scheduled instant remains the same instant when stored in UTC.
- IANA time zones handle Dublin winter and summer without fixed offsets.
- Provider `allow`, `block`, and `review` values map to internal outcomes.
- Users list only posts in workspaces they belong to.
- Outbound requests use the selected workspace connection's token.
- Caption serialization and publication idempotency remain intact.
