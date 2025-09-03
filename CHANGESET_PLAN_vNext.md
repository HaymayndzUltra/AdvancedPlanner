# CHANGESET_PLAN_vNext.md

## Ordered, Idempotent Task List (path → change → reason)

1) frameworks/security/findings.yaml → CREATE → Establish Security Critical=0 source of truth
2) frameworks/security/waivers.yaml → CREATE → Define exceptions schema with expiry, owner, rationale, compensating controls
3) frameworks/qa-test/artifacts/2025-09/handoff_manifest.yaml → UPDATE → Add governance.tags[] and confirm sealed fields
4) frameworks/qa-test/artifacts/2025-09/compliance_map.md → ENSURE/UPDATE → Ensure schema coverage mapped; add governance metadata header
5) frameworks/planning-fe/tasks/2025-09-02-fe_task_breakdown.yaml → UPDATE → Add governance.fields[] and governance.tags[]
6) frameworks/planning-be/backlog/2025-09-02-be_backlog.yaml → UPDATE → Add governance.fields[] and governance.tags[]
7) frameworks/planning/manifests/2025-09/handoff_manifest.yaml → CREATE → Seal planning artifacts (checksums, snapshot_rev, rulebook_hash)
8) frameworks/observability/digests/2025-09/digest_2025-09-02.md → CREATE → Emit per-cycle digest with MTTA/MTTR, incidents, gate evidence
9) frameworks/observability/artifacts/2025-09/handoff_manifest.yaml → CREATE → Seal observability digest and attachments
10) memory-bank/digests/2025-09/index.md → CREATE → Collect QA, Security, Planning, Observability digests
11) dev-workflow/ci/gates_config.yaml → CREATE → Configure CI to enforce schema_lint, cross_stream_consistency, parity/coverage, Critical=0 gate

## New/Updated Artifacts (required fields + stub snippets)

### 1) Security Findings Registry
- name: security findings
- path: frameworks/security/findings.yaml
- required fields: schema_version, cycle_id, snapshot_rev, rulebook_hash, governance.tags[], findings[] (id, severity, title, status, detected_on, owner, waiver_ref?)

```yaml
schema_version: 1
cycle_id: 2025-09
snapshot_rev: git:abcdef1234
rulebook_hash: sha256:TBD_rulebook_hash
governance:
  tags: [security, criticality, release_gate]
findings:
  - id: SEC-CRIT-001
    severity: Critical
    title: Placeholder critical example (replace with real scan result)
    status: open # open | mitigated | accepted_risk
    detected_on: 2025-09-02
    owner: security-lead@example.com
    waiver_ref: EX-2025-09-SEC-001 # optional; must exist in waivers.yaml if status=accepted_risk
```

### 2) Security Waivers / Exceptions Registry
- name: security policy waivers
- path: frameworks/security/waivers.yaml
- required fields: schema_version, cycle_id, snapshot_rev, rulebook_hash, governance.tags[], exceptions[] {id, rule_id, scope, rationale, compensating_controls, approver, owner, requested, expiry}

```yaml
schema_version: 1
cycle_id: 2025-09
snapshot_rev: git:abcdef1234
rulebook_hash: sha256:TBD_rulebook_hash
governance:
  tags: [security, exception, risk_acceptance]
exceptions:
  - id: EX-2025-09-SEC-001
    rule_id: Critical=0
    scope: payments-api/orders-pagination
    rationale: Temporary acceptance while remediation in flight
    compensating_controls: Increased monitoring on error rate and auth anomalies
    approver: CISO <ciso@example.com>
    owner: security-lead@example.com
    requested: 2025-09-02
    expiry: 2025-10-15
```

### 3) QA Handoff Manifest (update)
- name: qa handoff manifest
- path: frameworks/qa-test/artifacts/2025-09/handoff_manifest.yaml
- change: add governance.tags[] (retain existing sealed, snapshot_rev, rulebook_hash)

```yaml
# insert or ensure the following top-level block exists
governance:
  tags: [qa, gates, sealed]
```

### 4) QA Compliance Map (ensure/update)
- name: qa compliance map
- path: frameworks/qa-test/artifacts/2025-09/compliance_map.md
- change: ensure file exists and add governance metadata header

```markdown
---
snapshot_rev: git:abcdef1234
rulebook_hash: sha256:TBD_rulebook_hash
governance:
  tags: [qa, compliance, coverage]
---

### Compliance Map — 2025-09
- standard: <standard>
  control: <control>
  test_ids: []
  evidence_refs: []
```

### 5) Planning FE manifest (update)
- name: planning fe tasks
- path: frameworks/planning-fe/tasks/2025-09-02-fe_task_breakdown.yaml
- change: add governance.fields[] and governance.tags[] at top-level

```yaml
# insert/ensure at top-level
governance:
  fields: [version, cycle_id, snapshot_rev, owners, backlog]
  tags: [planning, fe]
```

### 6) Planning BE manifest (update)
- name: planning be backlog
- path: frameworks/planning-be/backlog/2025-09-02-be_backlog.yaml
- change: add governance.fields[] and governance.tags[] at top-level

```yaml
# insert/ensure at top-level
governance:
  fields: [version, cycle_id, snapshot_rev, owners, backlog]
  tags: [planning, be]
```

### 7) Planning Sealed Handoff Manifest (new)
- name: planning handoff manifest
- path: frameworks/planning/manifests/2025-09/handoff_manifest.yaml
- required fields: manifest_version, cycle, snapshot_rev, rulebook_hash, sealed, governance.tags[], artifacts[] {name, path, sha256}, quality_gates {schema_lint, snapshot_integrity}

```yaml
manifest_version: 1
cycle: 2025-09
snapshot_rev: git:abcdef1234
rulebook_hash: sha256:TBD_rulebook_hash
sealed: true
governance:
  tags: [planning, sealed]
artifacts:
  - name: planning_fe_tasks
    path: frameworks/planning-fe/tasks/2025-09-02-fe_task_breakdown.yaml
    sha256: TBD
  - name: planning_be_backlog
    path: frameworks/planning-be/backlog/2025-09-02-be_backlog.yaml
    sha256: TBD
quality_gates:
  schema_lint: pass
  snapshot_integrity: pass # no mixed snapshot_rev across FE/BE/QA
```

### 8) Observability Digest (new)
- name: observability cycle digest
- path: frameworks/observability/digests/2025-09/digest_2025-09-02.md
- required sections: Cycle, Snapshot Rev, Rulebook Hash, KPI (MTTA, MTTR), Incident Summaries, Gate Evidence (schema_lint, cross_stream_consistency, parity/coverage), Attachments

```markdown
## Observability Cycle Digest — 2025-09-02
- Cycle: 2025-09
- Snapshot Rev: git:abcdef1234
- Rulebook Hash: sha256:TBD_rulebook_hash

### KPI Summary
- MTTA: TBD
- MTTR: TBD

### Incident Summaries
- ID: INC-2025-09-001
  summary: TBD
  impact: TBD
  resolution: TBD

### Gate Evidence
- schema_lint: pass/fail (link to logs)
- cross_stream_consistency: pass/fail (link to logs)
- parity_coverage: pass/fail, coverage_pct: TBD

### Attachments
- logs: path/to/logs
- metrics: path/to/metrics
```

### 9) Observability Handoff Manifest (new)
- name: observability handoff manifest
- path: frameworks/observability/artifacts/2025-09/handoff_manifest.yaml
- required fields: manifest_version, cycle, snapshot_rev, rulebook_hash, sealed, governance.tags[], artifacts[] {name, path, sha256}

```yaml
manifest_version: 1
cycle: 2025-09
snapshot_rev: git:abcdef1234
rulebook_hash: sha256:TBD_rulebook_hash
sealed: true
governance:
  tags: [observability, sealed]
artifacts:
  - name: digest
    path: frameworks/observability/digests/2025-09/digest_2025-09-02.md
    sha256: TBD
```

### 10) Cross-Framework Digest Collector (new)
- name: memory-bank digests index
- path: memory-bank/digests/2025-09/index.md
- required content: links to QA, Security, Planning, Observability digests

```markdown
## Cycle Digests — 2025-09

- QA: frameworks/qa-test/digests/2025-09-02-digest.md
- Security: frameworks/security/digests/2025-09/cycle_digest.md
- Planning: frameworks/planning/digests/2025-09/cycle_digest.md
- Observability: frameworks/observability/digests/2025-09/digest_2025-09-02.md
```

### 11) CI Gates Configuration (new)
- name: CI gates config
- path: dev-workflow/ci/gates_config.yaml
- required fields: schema_version, gates {schema_lint, cross_stream_consistency, parity_coverage, security_critical_zero}, enforcement_mode: block_on_fail

```yaml
schema_version: 1
gates:
  schema_lint: true
  cross_stream_consistency: true
  parity_coverage:
    enabled: true
    threshold: 0.9
  security_critical_zero:
    enabled: true
    source: frameworks/security/findings.yaml
    exceptions: frameworks/security/waivers.yaml
enforcement_mode: block_on_fail
```

## Gate Checks to Run After Each Change

- After 1–2 (Security): security_critical_zero → PASS when no Critical open OR all mapped to valid exceptions (unexpired, with compensating controls)
- After 3–7 (QA/Planning): schema_lint → PASS; snapshot_integrity → PASS (all snapshot_rev == git:abcdef1234)
- After 3 & 6 (QA/Planning cross): cross_stream_consistency → PASS (test_matrix story_ref and endpoint_ref resolve in planning)
- After 8–9 (Observability): schema_lint (manifests) + evidence_present check → PASS (Gate Evidence section populated)
- After 10–11 (Integration/CI): dry-run pipeline → PASS (all configured gates evaluate to pass or block as intended)

## Owners & Deadlines (placeholders)

- Security (items 1–2): owner security-lead@example.com — deadline 2025-09-10
- QA (items 3–4): owner qa-platform@example.com — deadline 2025-09-08
- Planning (items 5–7): owner planning-pmo@example.com — deadline 2025-09-09
- Observability (items 8–9): owner obs-team@example.com — deadline 2025-09-08
- Integration/CI (items 10–11): owner release-eng@example.com — deadline 2025-09-11

## Lifecycle and Governance Enforcement

- Lifecycle states to record per artifact: PLANNED → READY_FOR_HANDOFF → PACKAGED → EXECUTED → VALIDATED → IMPROVE
- Every manifest/digest must carry: snapshot_rev, rulebook_hash, governance.tags[]
- Sealed manifests (QA/Planning/Observability/Security) must include checksums for artifacts and be immutable once sealed

