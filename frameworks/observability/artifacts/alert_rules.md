# Alert Rules Catalog
Version: 1.0
Last Updated: 2025-09-02

## Payments Elevated Error Rate
- metric: payments.error_rate
- severity: critical
- condition: error_rate > 1% for 5m
- runbook: link://runbook/payments-error-burst
- tags: [service:payments, Critical:0, owner:team-payments, environment:prod]

## Payments High Latency
- metric: payments.p95_latency
- severity: warning
- condition: p95_latency > 250 ms for 10m
- runbook: link://runbook/payments-latency
- tags: [service:payments, Critical:0, owner:team-payments, environment:prod]

## Payments Request Rate Anomaly
- metric: payments.request_rate
- severity: info
- condition: request_rate deviates > 30% from 7d baseline for 15m
- runbook: link://runbook/payments-traffic-anomaly
- tags: [service:payments, Critical:0, owner:team-payments, environment:prod]
