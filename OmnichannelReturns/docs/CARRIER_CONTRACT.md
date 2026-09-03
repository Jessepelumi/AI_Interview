# Carrier label contract

The label gateway accepts decimal kilograms under `weight_kg`. Catalogue weights
are stored as whole grams. Routing configuration is keyed by uppercase ISO
country code: `IE=anpost`, `GB=royalmail`, with `globalpost` as fallback.

Carrier calls are outside the database transaction; this exercise tests only the
deterministic request builder.
