---
contract: users
version: 1.0.0
owner: data-platform
producers:
  - app.identity-service
consumers:
  - analytics.warehouse
  - ml.feature_store
slo:
  availability: 99.9%
  freshness: PT24H
  dq_checks:
    - unique(user_id) == 100%
    - unique(email) == 100%
    - not_null(user_id,email,created_at,updated_at)
    - format(email) == RFC5322
privacy:
  pii: contains
  controls:
    - at_rest_encryption
    - in_transit_tls
    - masking_for_non_admin_roles
schema_ref: ../../docs/data/schemas/users.yaml
---

# Users Data Contract

This document defines the producer/consumer contract for the canonical `users` dataset. Producers must emit data conforming to the referenced schema and respect the privacy and DQ SLOs. Consumers may rely on contract guarantees and versioned change management.

## Breaking/Non-Breaking Changes
- Non-breaking: adding nullable fields; extending enums with backward-compatible defaults.
- Breaking: removing fields; changing types; reducing nullability; altering semantics.

## Change Management
- Versioning: semantic, starting at 1.0.0.
- Deprecations: announce 2 cycles prior; dual-write fields with `_v2` suffix; migration plan documented.

## Privacy & Security
- Email and phone are classified PII; apply masking for non-admin roles.
- GDPR deletion honored within 30 days.

## DQ SLAs & Alerts
- Daily validation jobs enforce the DQ checks above. Alerts page Security on policy violations related to PII exposure; page Data Platform on availability/freshness breaches.

