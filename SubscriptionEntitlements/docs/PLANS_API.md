# Plans API

`GET /api/plans/{slug}/` returns:

```json
{
  "slug": "growth",
  "name": "Growth",
  "active": true,
  "features": [{"key": "exports", "enabled": true, "limit": 50}]
}
```

`Feature.code` is an internal model name. SDKs consume the public `key` field.
