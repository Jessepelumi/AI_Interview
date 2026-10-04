# Documents API contract

All endpoints require:

```text
X-User-ID: <integer user id>
X-Workspace: <workspace slug>
```

The pair must resolve to an active membership. Resources outside that workspace must never be exposed. Unauthorized document access returns `404` to avoid confirming existence; malformed requests return `400`; an authenticated non-owner attempting an ACL mutation receives `403`.

## Read a document

`GET /api/documents/{document_id}/`

```json
{
  "id": "62c97b27-5ff1-4de4-8849-b0da0b72e38f",
  "title": "Project Aurora",
  "body": "Restricted launch plan",
  "content_version": 4,
  "acl_version": 19,
  "updated_at": "2026-10-04T09:14:07Z"
}
```

A user may read when they own the document or have an active direct or workspace-group grant. Revocation must affect the next authorization decision after the mutation returns success.

## Create a grant

`POST /api/sharing/grants/`

```json
{
  "document_id": "62c97b27-5ff1-4de4-8849-b0da0b72e38f",
  "principal_type": "membership",
  "principal_id": "418"
}
```

Returns `201`. A successful response means subsequent reads must observe the new policy. Group principal IDs are directory external IDs interpreted inside the document's workspace.

## Revoke a grant

`POST /api/sharing/revoke/`

```json
{"grant_id": 91}
```

Returns `204`. Repeating revocation is safe. Once acknowledged, no new document body or export artifact may be delivered using that grant.

## Search

`GET /api/search/?q=Aurora`

```json
{"results": [{"id": "62c...", "title": "Project Aurora", "body": "...", "content_version": 4, "acl_version": 19, "updated_at": "..."}]}
```

Search is eventually consistent for titles (target: 60 seconds), but authorization is not eventually consistent: stale index data must not result in unauthorized content or metadata being returned.

## Request an export

`POST /api/exports/documents/{document_id}/`

Returns `202` and a queued job. Access is checked at submission. Because execution may be delayed, policy must also hold when the artifact is produced. A job that no longer has authority becomes `denied` and has no artifact key.
