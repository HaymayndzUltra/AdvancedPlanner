---
contract: session_events
version: 1.0.0
owner: data-platform
producers:
  - app.web-tracker
  - app.backend-analytics
consumers:
  - analytics.warehouse
  - ml.feature_store
slo:
  availability: 99.9%
  freshness: PT1H
  dq_checks:
    - unique(event_id) == 100%
    - not_null(event_id,user_id,session_id,event_type,event_ts,event_date)
    - enum(event_type) in [session_start,session_end,page_view,click,purchase,login,logout,error]
    - partition(event_date) coverage >= 99%
privacy:
  pii: contains
  controls:
    - ip_anonymization
    - at_rest_encryption
    - in_transit_tls
schema_ref: ../../docs/data/schemas/session_events.yaml
---

# Session Events Data Contract

Defines guarantees for the canonical event stream. Producers must batch/stream deliver within 1 hour freshness and ensure schema compliance. Consumers may leverage stable event typing and partitioning for efficient queries.

## Ordering & Deduplication
- Events are append-only; ordering not guaranteed across partitions.
- Deduplicate by `event_id`.

## PII Handling
- IP is anonymized on ingestion; do not attempt re-identification.

