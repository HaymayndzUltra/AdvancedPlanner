### Rollback Runbook

Objective: Recover service within 5 minutes if change failure observed.

Triggers
- Error rate > threshold for 3 consecutive minutes
- Latency p95 breaches SLO for 3 consecutive minutes
- Business KPI degradation > X%

Immediate Actions
1) Abort active canary: use Rollback workflow (environment + reason)
2) Undo rollout to last stable replicaset
3) Verify service health returns to baseline

Validation
- Check dashboards: error rate, latency, saturation, SLO burn
- Confirm no data corruption; run smoke tests

Communication
- Post status in incident channel; update status page if user impact
- Create incident ticket with timeline and owners

Follow-up
- Root cause analysis within 24 hours
- Add automated guardrail/test to prevent recurrence

CLI reference
```bash
kubectl-argo-rollouts -n <ns> abort app-rollout
kubectl-argo-rollouts -n <ns> undo app-rollout
```

