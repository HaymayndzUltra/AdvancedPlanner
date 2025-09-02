# CHANGESET_PLAN_vNext.md

## Ordered, idempotent task list (path → change → reason)

1) /workspace/frameworks/security/findings.yaml → ADD → Establish Critical=0 registry with governance overlay  
- New artifact stub (YAML):
```yaml
schema_version: 1
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:rulebookhashhere"
owners:
  - team: "security-platform"
governance:
  tags: [security, critical_zero, release]
summary:
  critical_open: 0
  high_open: 0
  medium_open: 0
  low_open: 0
findings: []
lifecycle_state: READY_FOR_HANDOFF
```
- Gate after change: schema_lint=pass; parity/coverage=n/a; cross_stream_consistency=n/a  
- Owner/Deadline: security-platform@company — 2025-09-05

2) /workspace/frameworks/security/policy/exceptions.yaml → ADD → Implement waiver schema with expiry/owner/rationale/compensating controls  
- New artifact stub (YAML):
```yaml
schema_version: 1
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:rulebookhashhere"
governance:
  tags: [security, waiver]
exceptions:
  - exception_id: "EX-2025-09-001"
    rule_id: "LOG-RED-001"
    scope:
      service: "payments-api"
      tags: [PII, logging]
    owner: "team-appsec"
    approver: "ciso@company.com"
    expiry: "2025-10-15"
    rationale: "Temporary redaction rollout; low residual risk."
    compensating_controls:
      - "Increased log sampling and alerts"
      - "PII detection on sink"
lifecycle_state: PLANNED
```
- Gate after change: schema_lint=pass  
- Owner/Deadline: appsec@company — 2025-09-06

3) /workspace/frameworks/security/manifests/2025-09/handoff_manifest.yaml → UPDATE → Ensure governance.tags[], snapshot_rev, rulebook_hash; seal manifest  
- Updated fields (YAML skeleton):
```yaml
manifest_version: 1
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:rulebookhashhere"
governance:
  tags: [security, release, critical_zero]
  rationale: "Release readiness: Critical=0; waivers tracked."
  expiry: "2025-10-31"
sealed: true
artifacts:
  - name: findings
    path: frameworks/security/findings.yaml
    sha256: ""
  - name: exceptions
    path: frameworks/security/policy/exceptions.yaml
    sha256: ""
quality_gates:
  schema_lint: pass
  cross_stream_consistency: pass
  parity_coverage:
    status: pass
    coverage_pct: 100.0
```
- Gate after change: schema_lint=pass; seal validates checksums present  
- Owner/Deadline: security-platform@company — 2025-09-06

4) /workspace/frameworks/security/rules/release_gates.yaml → ADD → Block release if any Critical unresolved  
- New artifact stub (YAML):
```yaml
policy_version: 1
rules:
  - id: "critical_zero_enforcement"
    description: "Block release if critical_open > 0"
    source: "frameworks/security/findings.yaml"
    evaluation:
      condition: "summary.critical_open == 0"
      on_fail: "block_release"
governance:
  tags: [security, gate]
```
- Gate after change: n/a (consumed by CI)  
- Owner/Deadline: security-platform@company — 2025-09-06

5) /workspace/frameworks/planning-fe/manifests/2025-09-02-handoff_manifest.yaml → ADD/ALIGN → Standardize path base; add snapshot_rev, governance.fields[]; seal  
- New artifact stub (YAML):
```yaml
manifest_version: 1
cycle_id: "2025-09-02"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:rulebookhashhere"
governance:
  tags: [planning, fe, release]
  fields:
    owner: "fe-planning@company"
    risk: "low"
    compliance: ["none"]
sealed: true
artifacts:
  - path: frameworks/planning-fe/tasks/2025-09-02-fe_task_breakdown.yaml
    sha256: ""
  - path: frameworks/planning-fe/storymaps/2025-09-02-story_map.md
    sha256: ""
```
- Gate after change: schema_lint=pass; cross_stream_consistency (with QA mappings)=pass  
- Owner/Deadline: fe-planning@company — 2025-09-07

6) /workspace/frameworks/planning-be/manifests/2025-09-02-handoff_manifest.yaml → ADD/ALIGN → Standardize path base; add snapshot_rev, governance.fields[]; seal  
- New artifact stub (YAML):
```yaml
manifest_version: 1
cycle_id: "2025-09-02"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:rulebookhashhere"
governance:
  tags: [planning, be, release]
  fields:
    owner: "be-planning@company"
    risk: "low"
    compliance: ["none"]
sealed: true
artifacts:
  - path: frameworks/planning-be/backlog/2025-09-02-be_backlog.yaml
    sha256: ""
```
- Gate after change: schema_lint=pass; cross_stream_consistency (with QA endpoint_ref)=pass  
- Owner/Deadline: be-planning@company — 2025-09-07

7) /workspace/frameworks/qa-test/artifacts/2025-09/compliance_map.md → ADD → Map standards/controls to tests, with evidence refs  
- New artifact stub (MD):
```markdown
---
schema_version: 1
cycle_id: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:rulebookhashhere"
governance:
  tags: [qa, compliance]
---
# Compliance Map — 2025-09

- standard: ISO27001
  control: LOG-RED-001
  test_ids: [QA-API-ADDR-VAL-001]
  evidence_refs: [artifacts/2025-09/evidence/addr_validate_postman.json]
```
- Gate after change: schema_lint=n/a (MD w/ front matter); parity/coverage=pass for critical stories  
- Owner/Deadline: qa-platform@company — 2025-09-06

8) /workspace/frameworks/qa-test/rules/gates.yaml → ADD → Declare QA gates and thresholds  
- New artifact stub (YAML):
```yaml
schema_version: 1
parity_threshold: 0.90
gates:
  - name: "schema_lint"
    required: true
  - name: "cross_stream_consistency"
    required: true
  - name: "parity_coverage"
    required: true
governance:
  tags: [qa, gate]
```
- Gate after change: n/a (consumed by tooling)  
- Owner/Deadline: qa-platform@company — 2025-09-06

9) /workspace/frameworks/qa-test/manifests/2025-09/handoff_manifest.yaml → UPDATE → Ensure governance.tags[] present; confirm single snapshot_rev; sealed  
- Updated fields (YAML skeleton):
```yaml
governance:
  tags: [qa, release, compliance]
```
- Gate after change: schema_lint=pass; cross_stream_consistency=pass; parity/coverage=pass  
- Owner/Deadline: qa-platform@company — 2025-09-06

10) /workspace/frameworks/observability/digests/2025-09-02-digest.md → ADD → Per-cycle digest with KPI and Gate Evidence sections  
- New artifact stub (MD):
```markdown
---
schema_version: 1
date: "2025-09-02"
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:rulebookhashhere"
governance:
  tags: [observability, digest]
---
## Cycle Digest — 2025-09-02

### KPI Summary
- MTTA: TBD
- MTTR: TBD
- Incidents: []

### Gate Evidence
- schema_lint:
  evidence: [links/logs]
  result: TBD
- cross_stream_consistency:
  evidence: [links/validation]
  result: TBD
- parity/coverage:
  evidence: [metrics/screenshots]
  result: TBD

### Incident Summaries
- id: TBD
  summary: TBD
  impact: TBD
  resolution: TBD
```
- Gate after change: n/a (digest consumer)  
- Owner/Deadline: sre-observability@company — 2025-09-07

11) /workspace/frameworks/observability/manifests/2025-09/handoff_manifest.yaml → ADD → Seal digest + evidence artifacts  
- New artifact stub (YAML):
```yaml
manifest_version: 1
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:rulebookhashhere"
governance:
  tags: [observability, release]
sealed: true
artifacts:
  - name: digest_2025-09-02
    path: frameworks/observability/digests/2025-09-02-digest.md
    sha256: ""
quality_gates:
  schema_lint: pass
  cross_stream_consistency: pass
  parity_coverage:
    status: pass
    coverage_pct: 100.0
```
- Gate after change: schema_lint=pass  
- Owner/Deadline: sre-observability@company — 2025-09-07

12) /workspace/memory-bank/digests/2025-09/ → ADD → Collect digests from all frameworks  
- New artifact stub (MD index):
```markdown
# Digest Index — 2025-09
- QA: frameworks/qa-test/digests/2025-09-02-digest.md
- Security: frameworks/security/digests/2025-09-02-digest.md
- Planning-FE: frameworks/planning-fe/digests/2025-09-02-digest.md
- Planning-BE: frameworks/planning-be/digests/2025-09-02-digest.md
- Observability: frameworks/observability/digests/2025-09-02-digest.md
```
- Gate after change: n/a  
- Owner/Deadline: release-eng@company — 2025-09-07

13) /.github/workflows/frameworks-governance.yml → ADD → CI/CD workflow to validate manifests and gates, block on Critical>0  
- New artifact stub (YAML):
```yaml
name: Frameworks Governance Gates
on:
  pull_request:
    paths:
      - "frameworks/**"
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate manifests and gates
        run: |
          echo "Run schema_lint, cross_stream_consistency, parity_coverage"
          echo "Enforce Critical=0 via frameworks/security/rules/release_gates.yaml"
```
- Gate after change: CI must fail if any gate fails; pass condition is all gates pass on sealed manifests  
- Owner/Deadline: release-eng@company — 2025-09-08

## Gate checks to run after each change (expected pass)
- schema_lint: All YAML/MD front matter validate; manifests include snapshot_rev, rulebook_hash, governance.tags[].
- cross_stream_consistency: QA story_ref and BE endpoint_ref align; planning manifests reference artifacts present.
- parity/coverage: Critical-path planning items mapped in QA; threshold ≥ 0.90 (100% for critical stories).
- Critical=0: security/findings.yaml summary.critical_open == 0 OR a valid exception exists with approved approver and non-expired expiry; release gate blocks otherwise.

## Owners & deadlines
- Security artifacts and gates: security-platform@company — by 2025-09-06/07.
- Planning-FE/BE manifests alignment: fe-planning@company, be-planning@company — by 2025-09-07.
- QA artifacts and gates: qa-platform@company — by 2025-09-06.
- Observability digest/manifest: sre-observability@company — by 2025-09-07.
- Memory bank and CI workflow: release-eng@company — by 2025-09-08.