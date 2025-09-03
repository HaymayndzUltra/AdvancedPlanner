### Release Checklist

Owner: Release Manager

- Preconditions
  - QA gate passed (test report attached)
  - Security gate passed (scan report, SBOM, attestations)
  - Change approval recorded (ticket/link)
  - SLO risk reviewed with SRE

- Build & Sign
  - Verify CI build green on `integration`
  - Verify SBOM uploaded and Cosign attestations

- Staging Deploy
  - Deploy commit SHA to `staging` via Deploy workflow
  - Smoke tests and key user flows validated
  - Error budget burn checked (< threshold)

- Production Canary
  - Start canary rollout (10% → 25% → 50%)
  - Monitor KPIs: error rate, latency, saturation, business metrics
  - Hold points honored between steps

- Promote to Full
  - Environment approval completed
  - Promote workflow executed successfully

- Post-Release
  - Deployment marker sent to observability
  - Update CHANGELOG and status page
  - Schedule retro if incidents or near-misses occurred

