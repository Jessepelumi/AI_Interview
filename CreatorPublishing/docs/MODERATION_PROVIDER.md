# Moderation provider v3

The provider response field `decision` has one of:

- `allow` — content may be published;
- `block` — content must be rejected;
- `review` — hold for manual review.

The provider stopped returning the old values `approved` and `blocked` on
1 June 2026. Unknown values must not be auto-approved.
