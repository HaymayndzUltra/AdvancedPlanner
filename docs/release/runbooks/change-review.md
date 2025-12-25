### Change Review Process

Purpose: Ensure safe, compliant releases with clear accountability.

Steps

1) Change Proposal
   - Link PR(s), scope, risk level, rollout plan, rollback plan
   - Owner and approvers identified (Eng Lead, QA Lead, Security, SRE)

2) Evidence
   - QA: Test report, coverage, flake rate
   - Security: SAST/DAST summary, SBOM, vulnerability status
   - Performance: baseline vs target, load test if applicable

3) Approvals
   - Minimum approvers: Eng Lead + QA + Security (high risk adds SRE)
   - GitHub environment approval enforced for production

4) Pre-Deploy Checklist
   - Feature flags ready to disable new paths
   - Observability dashboards and alerts prepared

5) Decision & Record
   - Approve/Reject with comments and ticket linkage
   - Store record in `CHANGELOG.md` and ticketing system

