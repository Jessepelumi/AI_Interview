# Acceptance criteria

The incident is resolved when:

- all visible tests pass without weakening assertions;
- direct and group grants are isolated to their intended workspace;
- grant creation and revocation are reflected in the next protected read;
- delayed or duplicate index events cannot regress an ACL projection;
- search performs an authoritative access check before returning protected metadata;
- an export queued before revocation cannot produce an artifact afterward;
- retries of terminal export jobs remain idempotent;
- Django checks and migration drift checks pass;
- the suite passes with PostgreSQL and Redis using Docker Compose.

Operational constraints:

- Do not solve the incident by disabling caching, search, or exports globally.
- Do not shorten TTLs as the sole correctness mechanism.
- Do not expose document existence through different unauthorized responses.
- Preserve the existing HTTP contract unless a regression test demonstrates a documented mismatch.
- Keep correctness independent of broker ordering and worker delay.
