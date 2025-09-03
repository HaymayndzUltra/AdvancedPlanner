# GLOBAL_ANALYSIS_vNext.md

## Executive summary (≤10 bullets)

- Governance and sealing fields require normalization across frameworks (add governance.tags[], snapshot_rev, rulebook_hash).
- Security Critical=0 gate lacks a canonical findings/waivers registry; create and wire to CI.
- Planning manifests need governance fields and a sealed handoff manifest to ensure snapshot integrity.
- QA artifacts largely present; add governance block to handoff manifest and ensure compliance_map header.
- Observability digest must include gate evidence sections, not just KPIs; add sealed manifest.
- Cross-stream gates (schema_lint, consistency, parity/coverage) must be enforced in CI with block_on_fail.
- Snapshot integrity requires single snapshot_rev for the cycle (no mixed revisions across frameworks).
- Memory-bank collector should link all per-cycle digests to enable auditability.
- Minimal exceptions allowed only with explicit expiry, approver, and compensating controls.
- Readiness contingent on passing all gates and Security Critical=0 (or valid, unexpired exceptions).

## Per-framework findings after applying checklist

### Security
- What changed: Added design for `frameworks/security/findings.yaml` and `frameworks/security/waivers.yaml` with required fields, governance.tags[], snapshot_rev, rulebook_hash.
- Gaps remaining: Findings content TBD; ensure any accepted_risk items reference valid, unexpired waivers with compensating controls.
- Gates: `security_critical_zero` integrated via CI using findings + waivers.

### Planning
- What changed: Governance fields/tags to be added to `frameworks/planning-fe/tasks/2025-09-02-fe_task_breakdown.yaml` and `frameworks/planning-be/backlog/2025-09-02-be_backlog.yaml` plus a new sealed planning handoff manifest.
- Gaps remaining: Compute checksums when sealing; confirm no mixed `snapshot_rev` across FE/BE/QA.
- Gates: `schema_lint`, `snapshot_integrity` pass when manifests contain required fields and aligned snapshot.

### QA
- What changed: Add governance.tags[] to QA handoff manifest; ensure compliance_map has metadata header (snapshot_rev, rulebook_hash, governance.tags[]).
- Gaps remaining: None functionally, assuming existing test_matrix and evidence index validate against schemas.
- Gates: `schema_lint`, `cross_stream_consistency`, `parity/coverage` enforced; parity threshold >= 0.9.

### Observability
- What changed: Introduce per-cycle digest with KPI (MTTA, MTTR), incident summaries, and Gate Evidence; add sealed observability handoff manifest.
- Gaps remaining: Populate actual KPI values and attach evidence (links to logs/metrics).
- Gates: Evidence presence check (non-empty sections) and manifest schema lint.

## Cross-framework integration map

- Producers → Artifacts → Consumers
  - Security → `frameworks/security/findings.yaml`, `frameworks/security/waivers.yaml` → CI gate `security_critical_zero`, Observability digest (gate evidence)
  - Planning → FE/BE manifests, sealed `frameworks/planning/manifests/2025-09/handoff_manifest.yaml` → QA consistency checks, CI snapshot_integrity gate, Observability digest
  - QA → `frameworks/qa-test/artifacts/2025-09/handoff_manifest.yaml`, `test_matrix.yaml`, `compliance_map.md` → CI schema_lint, consistency, parity gates; Observability digest
  - Observability → `frameworks/observability/digests/2025-09/digest_2025-09-02.md`, sealed manifest → Memory bank collector, Exec reporting
  - Integration → `dev-workflow/ci/gates_config.yaml` → All CI workflows and release pipeline
  - Aggregation → `memory-bank/digests/2025-09/index.md` → Executives, Audit, Runbooks

## Final readiness decision

Decision: NO-GO

Rationale tied to gates:
- `security_critical_zero`: Pending; findings registry not yet populated, and exceptions not validated → block.
- `schema_lint`: Expected to pass after planned updates, but enforcement not yet configured in CI → block until `dev-workflow/ci/gates_config.yaml` lands.
- `cross_stream_consistency`: Expected to pass (QA ↔ Planning mappings align), but must be revalidated post-governance updates.
- `parity/coverage`: Threshold (≥0.9) expected to pass based on current test_matrix; must be verified in CI and captured in Observability Gate Evidence.
- `snapshot_integrity`: Will pass once sealed Planning manifest confirms single `snapshot_rev` across frameworks; currently unsealed → block.
- Observability Gate Evidence: Digest exists for QA, but standardized evidence sections across all frameworks are not yet published → block.

