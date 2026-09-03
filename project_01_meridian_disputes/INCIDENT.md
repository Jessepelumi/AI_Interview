# Incident MD-1842: dispute workflow inconsistencies

## Customer and operator report

Since the processor integration rollout, operations agents report that a small number of dispute pages return records belonging to another merchant when opened from a copied link. Separately, processor retries appear to leave duplicate history entries, and several cases that should still have been actionable were marked late around midnight.

One support case also shows a dispute moving directly from draft to closed after an agent clicked submit twice while a processor callback was arriving.

## Expected behaviour

- An agent can access only disputes belonging to an organisation in which they are a member.
- A case follows the documented lifecycle and cannot skip required review stages.
- Re-delivery of the same processor event has no additional effect.
- Deadline decisions are consistent for timezone-aware instants.
- Amount validation is exact for the payment currency.

## Observed behaviour

Application logs include repeated entries such as:

```text
INFO state:won dispute=417 event=evt_91B
INFO state:won dispute=417 event=evt_91B
ERROR Processor callback failed dispute_id=588
```

The processor considers a `2xx` response acknowledgement and will not retry it.

## Reproduction

1. Create two organisations and one agent in only the first.
2. Authenticate as that agent and request the second organisation's dispute by numeric ID.
3. Deliver the same signed `dispute.won` event twice.
4. Compare the dispute, processor-event, and audit tables.

## Acceptance criteria

- Tenant isolation applies consistently to collection and detail/actions.
- Supported transitions still work and unsupported transitions are rejected.
- Webhook delivery is authenticated, idempotent, and safely retryable.
- Deadline and monetary boundary cases have regression coverage.
- Existing valid API behavior remains compatible and the full suite passes.
