# Service and domain notes

## Ownership

| Component | Owns | Does not own |
|---|---|---|
| Organizations | Workspace membership and request identity | Document ACLs |
| Directory | Workspace groups and membership resolution | Grant lifecycle |
| Documents | Document content and lifecycle | Search projection |
| Sharing | Grants and effective access decisions | User authentication |
| Search Index | Queryable projection | Authoritative authorization |
| Exports | Job lifecycle and artifact production | Long-lived access entitlement |

## Request and data flow

A document request authenticates a user into one workspace membership. The document is loaded within that workspace, then Sharing evaluates ownership, direct grants, and group grants. Directory group external IDs are only meaningful inside their workspace even when two customers use the same value such as `legal` or `engineering`.

ACL mutations are transactional and increment `Document.acl_version`. The version is monotonic and represents the policy state, not content edits. Consumers may receive duplicate or out-of-order events and must converge on the newest ACL version.

Search is a derived read model. It may lag for indexing, but callers must never receive a result they are not currently authorized to know about. Search delivery has at-least-once semantics.

Exports have two moments in time: acceptance by the API and execution by a worker. A queue delay does not freeze the requester's authorization. Workers must be retry-safe and must not publish an artifact after access is lost.

## Invariants

1. A workspace-scoped identity must never acquire meaning from another workspace.
2. A successful ACL mutation is visible to later authorization decisions.
3. `acl_version` never decreases in an authoritative or derived representation.
4. Derived data may be stale, but stale authorization must fail closed before protected data is returned.
5. Retrying an ACL event or export job must not weaken access control.

## Consistency and retries

- Database ACL mutations: strong consistency after commit.
- Authorization cache: optimization only; it may not redefine the policy contract.
- Directory cache: entries may be reused only where their identity scope is identical.
- Search events: at least once, duplicates and reordering expected.
- Export jobs: at least once; terminal jobs are idempotent.
