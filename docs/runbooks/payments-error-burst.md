# Runbook: Payments Error Burst

## When This Fires
- Critical: High error budget burn (5m>14.4x AND 1h>6x)
- Warning: Slow burn (30m>3x AND 6h>1x)

## Immediate Actions
- Acknowledge alert and open incident ticket.
- Check Grafana dashboard  (service=payments).
- Verify recent deployments via annotations. If correlated, consider rollback.

## Triage Checklist
- Inspect top error codes and routes.
- Check upstream dependencies and rate limiters.
- Review recent config/feature flag changes.

## Mitigation
- Rollback recent deployment if errors began post-deploy.
- Apply feature flag kill-switch for offending path.

## Verification
- Error ratio returns below budget within 10 minutes.
- Burn alerts resolve and SLO compliance trend normalizes.

## Postmortem
- Add root cause, timeline, and prevention actions to the retro document.

