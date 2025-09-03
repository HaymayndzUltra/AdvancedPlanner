## Ordered list of edits/additions (file path → change description)
1. /workspace/frameworks/security/waivers.yaml → Standardize exceptions path; migrate references from /workspace/frameworks/security/policy/exceptions.yaml; ensure governance.tags[], approver, expiry, rationale, compensating_controls.
2. /workspace/frameworks/security/findings.yaml → Unify schema to include findings[] and summary.critical_open; add lifecycle_state: READY_FOR_HANDOFF.
3. /workspace/frameworks/security/manifests/2025-09/handoff_manifest.yaml → Add lifecycle_state: PACKAGED; compute sha256 for findings.yaml and waivers.yaml; confirm snapshot_rev and rulebook_hash; sealed: true.
4. /workspace/frameworks/security/digests/2025-09/digest_2025-09-02.md → ADD per-cycle digest with KPI Summary (Critical=0 proof), Gate Evidence (CI outputs), governance.tags[].
5. /workspace/frameworks/planning-fe/manifests/2025-09-02-handoff_manifest.yaml → Add lifecycle_state: PACKAGED; compute sha256 for FE tasks/story map artifacts; confirm snapshot_rev, rulebook_hash, sealed: true.
6. /workspace/frameworks/planning-be/manifests/2025-09-02-handoff_manifest.yaml → Add lifecycle_state: PACKAGED; compute sha256 for BE backlog; confirm snapshot_rev, rulebook_hash, sealed: true.
7. /workspace/frameworks/planning/manifests/2025-09/handoff_manifest.yaml → Ensure lifecycle_state: PACKAGED; fill sha256 for FE/BE artifacts; confirm snapshot_integrity gate.
8. /workspace/frameworks/qa-test/manifests/2025-09/handoff_manifest.yaml → Ensure snapshot_rev, rulebook_hash, sealed, artifacts with sha256; add lifecycle_state: PACKAGED; governance.tags[] present.
9. /workspace/frameworks/qa-test/digests/2025-09/digest_2025-09-02.md → ADD per-cycle digest with coverage, parity KPIs, and Gate Evidence; governance.tags[].
10. /workspace/frameworks/observability/digests/2025-09/digest_2025-09-02.md → Standardize digest path; populate Gate Evidence with CI logs/metrics; governance front matter.
11. /workspace/frameworks/observability/manifests/2025-09/handoff_manifest.yaml → Add lifecycle_state: PACKAGED; add sha256 for all attached evidence artifacts; confirm snapshot_rev, rulebook_hash, sealed.
12. /workspace/memory-bank/digests/2025-09/index.md → Normalize to a single index; link all four framework digests under /workspace/frameworks/.../digests/2025-09/digest_2025-09-02.md.
13. /workspace/.github/workflows/frameworks-governance.yml → Finalize CI to run schema_lint, cross_stream_consistency, parity/coverage, and Security Critical=0; fail on any violation.
14. /workspace/dev-workflow/ci/gates_config.yaml → Pin gates and thresholds; source paths for findings/waivers; enforcement_mode: block_on_fail; verify single snapshot_rev for cycle.
15. All manifests/digests above → Normalize to absolute paths under /workspace/...; ensure governance.tags[] present across all artifacts.

## New/updated artifacts (name, path, required fields, example stub)
- Security Waivers (exceptions)
  - Path: /workspace/frameworks/security/waivers.yaml
  - Required: schema_version, cycle, snapshot_rev, rulebook_hash, governance.tags[], exceptions[] {id, rule_id, scope, rationale, compensating_controls, approver, owner, requested, expiry, lifecycle_state}
```yaml
schema_version: 1
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:TBD"
governance: { tags: [security, waiver] }
exceptions:
  - id: "EX-2025-09-001"
    rule_id: "Critical=0"
    scope: "payments-api"
    rationale: "Temporary exception while fix in progress"
    compensating_controls: ["WAF rule", "High-sensitivity alert"]
    approver: "ciso@company.com"
    owner: "team-appsec"
    requested: "2025-09-02"
    expiry: "2025-09-16"
lifecycle_state: "PLANNED"
```
- Security Findings Registry
  - Path: /workspace/frameworks/security/findings.yaml
  - Required: schema_version, cycle, snapshot_rev, rulebook_hash, governance.tags[], findings[] {id, severity, title, status, detected_on, owner, waiver_ref?}, summary {critical_open}, lifecycle_state
```yaml
schema_version: 1
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:TBD"
governance: { tags: [security, critical_zero, release] }
findings: []
summary: { critical_open: 0 }
lifecycle_state: "READY_FOR_HANDOFF"
```
- Security Handoff Manifest (sealed)
  - Path: /workspace/frameworks/security/manifests/2025-09/handoff_manifest.yaml
  - Required: manifest_version, cycle, snapshot_rev, rulebook_hash, governance.tags[], sealed, artifacts[] {name, path, sha256}, quality_gates, lifecycle_state
```yaml
manifest_version: 1
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:TBD"
governance: { tags: [security, release, critical_zero] }
sealed: true
artifacts:
  - { name: "findings", path: "/workspace/frameworks/security/findings.yaml", sha256: "TBD" }
  - { name: "waivers", path: "/workspace/frameworks/security/waivers.yaml", sha256: "TBD" }
quality_gates: { schema_lint: "pass" }
lifecycle_state: "PACKAGED"
```
- Security Cycle Digest
  - Path: /workspace/frameworks/security/digests/2025-09/digest_2025-09-02.md
  - Required: front matter with schema_version, cycle, snapshot_rev, rulebook_hash, governance.tags[], KPI (Critical=0), Gate Evidence
```markdown
---
schema_version: 1
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:TBD"
governance: { tags: [security, digest] }
---
## KPI: Critical=0
## Gate Evidence
- CI output: link
```
- Planning FE/BE Handoff Manifests (sealed)
  - Paths:
    - /workspace/frameworks/planning-fe/manifests/2025-09-02-handoff_manifest.yaml
    - /workspace/frameworks/planning-be/manifests/2025-09-02-handoff_manifest.yaml
  - Required: manifest_version, cycle_id, snapshot_rev, rulebook_hash, governance.tags[], governance.fields[], sealed, artifacts[] {path, sha256}, lifecycle_state
```yaml
manifest_version: 1
cycle_id: "2025-09-02"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:TBD"
governance: { tags: [planning, fe], fields: { owner: "fe@company", risk: "low" } }
sealed: true
artifacts:
  - { path: "/workspace/frameworks/planning-fe/tasks/2025-09-02-fe_task_breakdown.yaml", sha256: "TBD" }
lifecycle_state: "PACKAGED"
```
- Planning Aggregator Handoff Manifest (sealed)
  - Path: /workspace/frameworks/planning/manifests/2025-09/handoff_manifest.yaml
  - Required: as per L579-L597 plus lifecycle_state
```yaml
manifest_version: 1
cycle: 2025-09
snapshot_rev: git:abcdef1234
rulebook_hash: sha256:TBD
sealed: true
governance: { tags: [planning, sealed] }
artifacts:
  - { name: "planning_fe_tasks", path: "/workspace/frameworks/planning-fe/tasks/2025-09-02-fe_task_breakdown.yaml", sha256: "TBD" }
  - { name: "planning_be_backlog", path: "/workspace/frameworks/planning-be/backlog/2025-09-02-be_backlog.yaml", sha256: "TBD" }
quality_gates: { schema_lint: "pass", snapshot_integrity: "pass" }
lifecycle_state: "PACKAGED"
```
- QA Handoff Manifest (sealed)
  - Path: /workspace/frameworks/qa-test/manifests/2025-09/handoff_manifest.yaml
  - Required: snapshot_rev, rulebook_hash, governance.tags[], sealed, artifacts[] {path, sha256}, lifecycle_state
```yaml
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:TBD"
governance: { tags: [qa, release, compliance] }
sealed: true
artifacts: []
lifecycle_state: "PACKAGED"
```
- QA Cycle Digest
  - Path: /workspace/frameworks/qa-test/digests/2025-09/digest_2025-09-02.md
  - Required: coverage, parity KPIs, Gate Evidence, governance front matter
```markdown
---
schema_version: 1
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:TBD"
governance: { tags: [qa, digest] }
---
## KPIs: coverage, parity
## Gate Evidence
```
- Observability Digest (standardized)
  - Path: /workspace/frameworks/observability/digests/2025-09/digest_2025-09-02.md
  - Required: KPI (MTTA/MTTR), Incident Summaries, Gate Evidence; governance front matter
```markdown
---
schema_version: 1
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:TBD"
governance: { tags: [observability, digest] }
---
## KPI Summary
## Gate Evidence
```
- Observability Handoff Manifest (sealed)
  - Path: /workspace/frameworks/observability/manifests/2025-09/handoff_manifest.yaml
  - Required: add lifecycle_state and sha256 for attached evidence
```yaml
lifecycle_state: "PACKAGED"
artifacts:
  - { name: "digest_2025-09-02", path: "/workspace/frameworks/observability/digests/2025-09/digest_2025-09-02.md", sha256: "TBD" }
```
- Memory Bank Index
  - Path: /workspace/memory-bank/digests/2025-09/index.md
  - Required: links to all four framework digests (paths above)

- CI Gates Config
  - Path: /workspace/dev-workflow/ci/gates_config.yaml
  - Required: schema_version, gates {schema_lint, cross_stream_consistency, parity_coverage.threshold, security_critical_zero {source, exceptions}}, enforcement_mode: block_on_fail

- Governance Workflow
  - Path: /workspace/.github/workflows/frameworks-governance.yml
  - Required: run gates per gates_config.yaml; ensure failure on any violation

## Gate checks to run after each change
- schema_lint: All YAML/MD front matter valid; manifests include snapshot_rev, rulebook_hash, governance.tags[].
- cross_stream_consistency: QA story_ref and BE endpoint_ref resolve in planning.
- parity/coverage: Parity threshold ≥0.90; 100% for critical path stories.
- snapshot_integrity: Single snapshot_rev across all artifacts for the cycle.
- security_critical_zero: summary.critical_open == 0 OR valid, unexpired waiver with approver and compensating controls.
- evidence_present (Observability): Gate Evidence sections non-empty with artifact links and checksums.

## Owners and deadlines (placeholders)
- Security: security-platform@company — 2025-09-06
- Planning FE/BE: fe-planning@company, be-planning@company — 2025-09-07
- QA: qa-platform@company — 2025-09-06
- Observability: sre-observability@company — 2025-09-07
- CI/Governance: release-eng@company — 2025-09-08

