# Feature Store

- Registry: docs/data/feature_store/features.yaml
- Serving: offline via warehouse tables; online (future) via Redis-backed service.
- Refresh: daily for user features; hourly for session aggregates.