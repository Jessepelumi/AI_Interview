# SEV-2 security incident: delayed access revocation

**Service:** Skylark Documents  
**Customer:** Atlas Research  
**Incident commander:** Identity & Content Access on-call  
**Status at handoff:** mitigated by advising the customer not to reuse sensitive documents; investigation active

## Impact

Atlas Research removed access to a confidential launch document. For several minutes afterward, one former collaborator could still open the document and an older search result returned it. A second customer reported the opposite symptom: a newly added collaborator received `404` until later. Security considers any post-revocation content delivery a policy breach, irrespective of duration.

No public-link exposure has been reported. The affected accounts were valid users with active workspace memberships.

## Timeline (UTC)

- **09:02** — Atlas owner shares “Project Aurora” with a collaborator.
- **09:11** — Collaborator opens the document and requests a PDF export.
- **09:14** — Owner removes the grant; API returns `204`.
- **09:15** — Collaborator opens the same document URL successfully.
- **09:16** — Search returns “Project Aurora” for the collaborator after briefly removing it.
- **09:18** — The queued PDF export completes and an artifact key is recorded.
- **09:27** — Beacon Legal reports that a newly granted document returned `404` twice, then became readable without another ACL change.
- **09:41** — Support correlates both reports with the directory-cache rollout completed the previous afternoon.

## Evidence supplied to engineering

```text
09:14:07 acl.grant.revoked document=62c... principal=membership:418 acl_version=19 http=204
09:15:02 document.read document=62c... actor=418 workspace=atlas decision=allow source=cache
09:15:44 index.event.applied document=62c... event_acl_version=19 projection_acl_version=19
09:16:01 index.event.applied document=62c... event_acl_version=18 projection_acl_version=18
09:18:22 export.completed job=57b... document=62c... requested_by=418
```

Selected metrics from the same window:

```text
authorization_cache_hit_ratio          0.94 -> 0.98
acl_mutation_rate_per_minute           31   -> 34
search_index_consumer_redeliveries      2   -> 47
export_queue_oldest_age_seconds         9   -> 286
```

## Recent changes

Release `2026.10.03.2` included:

- directory subject caching moved from the identity gateway into the Django service;
- cache TTLs increased during a database load reduction;
- the search consumer changed from ordered single-partition delivery to parallel delivery;
- export workers were allowed to resume jobs delayed for up to 24 hours.

The release passed unit and smoke tests. There was no schema migration.

## Known unknowns

- Whether document retrieval, search, and export share one faulty decision or have separate enforcement points.
- Whether workspace overlap, event ordering, cache lifetime, or queue delay is required to reproduce the incident.
- Whether revocation is committed before downstream events are published.
- Whether owners and administrators follow the same path as ordinary members.
