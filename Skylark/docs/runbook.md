# Access incident runbook fragment

When investigating a reported unauthorized read:

1. Record document ID, actor user ID, workspace slug, endpoint, response time, and request ID.
2. Compare the actor's active membership and group subjects with the document's active grants.
3. Record authoritative `acl_version` and any version present in derived projections.
4. Check ACL mutation commit time, cache decision source, event delivery order, and queue age.
5. Preserve job and event payloads before replaying them.

Safe mitigations include pausing artifact publication for the affected workspace and bypassing a suspect derived projection while retaining an authoritative check. Purging a single customer's relevant cache entries may reduce exposure but is not a complete fix.

Never bulk-delete cache keys, replay all ACL events, or regenerate all exports during triage without incident-commander approval.
