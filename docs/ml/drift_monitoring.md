# Drift Monitoring Plan

- Scope: `user_country_code`, `session_events_7d`, `total_spend_30d` and label rate
- Metrics:
  - Feature Drift: PSI target < 0.2; warn at 0.1
  - Label Drift: weekly purchase rate change warn > 25%, fail > 50%
- Data Windows: reference = last stable quarter; current = last 30 days
- Alerts: Slack channel #ml-alerts; PagerDuty for fail thresholds
- Actions: retrain if PSI > 0.2 or label drift fail; review features

## Checks (initial)
- users.country_code distribution vs reference (PSI)
- session_events.event_type distribution vs reference (PSI)
- transactions.amount mean/variance shift (t-test/levene as proxy)
- Weekly purchase label rate delta vs reference window

## Evidence & Handoff
- Store drift evidence under `data/pipelines/out/validation/*_drift.json`
- Link evidence in release notes when enabling new models/features