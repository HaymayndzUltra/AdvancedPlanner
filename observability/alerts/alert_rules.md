# Alert Rulebook: Payments Service

## Availability SLO Burn (Paging)
- metric: http_requests_total (errors vs total)
- SLO: 99.9% over 30d (error budget 0.1%)
- Condition: error ratio > 14.4× budget (5m) AND > 6× budget (1h)
- Severity: critical
- Runbook: docs/runbooks/payments-error-burst.md
- Tags: [service:payments, owner:team-payments, environment:production, Critical:0]

## Availability SLO Burn (Warning)
- Condition: error ratio > 3× budget (30m) AND > 1× budget (6h)
- Severity: warning
- Runbook: docs/runbooks/payments-error-burst.md
- Tags: [service:payments, owner:team-payments, environment:production, Critical:0]

## Governance & Noise Policy
- Every critical alert must link a runbook and a dashboard panel.
- Alert noise threshold: < 10% of pages during any 7-day window.
- Review cadence: weekly in retro; adjust thresholds if false-positive rate > 10%.

