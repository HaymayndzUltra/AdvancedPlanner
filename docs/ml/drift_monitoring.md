# Drift Monitoring Plan

- Scope: `user_country_code`, `session_events_7d`, `total_spend_30d` and label rate
- Metrics:
  - Feature Drift: PSI target < 0.2; warn at 0.1
  - Label Drift: weekly purchase rate change warn > 25%, fail > 50%
- Data Windows: reference = last stable quarter; current = last 30 days
- Alerts: Slack channel #ml-alerts; PagerDuty for fail thresholds
- Actions: retrain if PSI > 0.2 or label drift fail; review features