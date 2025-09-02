# Alert Rules Catalog

## Alert: Payments Elevated Error Rate
- metric: payments.error_rate
- severity: critical
- condition: error_rate > 1% for 5m
- runbook: link://runbook/payments-error-burst
- tags: [service:payments, Critical:0, owner:team-payments]

## Alert: Payments High P95 Latency
- metric: payments.p95_latency
- severity: warning
- condition: p95_latency > 300ms for 10m
- runbook: link://runbook/payments-latency-tuning
- tags: [service:payments, Critical:0, owner:team-payments]

## Alert: Payments Request Rate Anomaly
- metric: payments.request_rate
- severity: info
- condition: request_rate deviates > 3x from 7d baseline
- runbook: link://runbook/payments-traffic-anomaly
- tags: [service:payments, Critical:0, owner:team-payments]

