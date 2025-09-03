# GLOBAL ANALYSIS

## Executive Summary
- Security has an open Critical (F-0001: PII in logs) without a matching approved exception; blocks release.
- QA uses Markdown compliance map while schema expects structured mappings; evidence hashes are placeholders.
- QA rulebook references `qa_evidence_index.md` but repo uses `qa_evidence_index.yaml`; schema ref drift.
- Two QA manifest variants use different path bases; unify to a single convention to avoid drift.
- Planning FE manifest lacks an explicit `sealed: true` field; add for immutability parity.
- Observability aligns to lifecycle/gates and enforces `Critical:0` tags; parity gate requires 100% KPI alert coverage.
- Event lifecycle and quality gates conceptually align across frameworks; enforce identical field names and statuses.
- Governance tags exist but are not ubiquitous; require `governance.tags[]` or `tags[]` on all artifacts.
- Metrics spine present in all frameworks via per-cycle digests; Security digest still has TBD fields.
- Cross-framework: ensure no mixed `snapshot_rev` within any single sealed manifest and record `rulebook_hash` consistently.

## Per-Framework Findings and Fixes

### QA Framework
- Gap: `compliance_map.md` is free-form Markdown, but a JSON schema exists expecting structured mappings.
  - Evidence: `frameworks/qa-test/schemas/compliance_map.schema.json` vs artifact `frameworks/qa-test/artifacts/2025-09/compliance_map.md`.
  - Fix: Replace with structured YAML/JSON (matching schema) at `frameworks/qa-test/artifacts/2025-09/compliance_map.yaml` (or `.json`) and update references in manifest.
- Gap: Rulebook artifact name drift.
  - Evidence: `frameworks/qa-test/rules/rulebook.yaml` (artifacts.required lists `qa_evidence_index.md`) while actual is `qa_evidence_index.yaml`.
  - Fix: Update rulebook to `qa_evidence_index.yaml` and CI checks accordingly.
- Gap: Placeholder SHA256 in evidence index.
  - Evidence: `frameworks/qa-test/artifacts/2025-09/qa_evidence_index.yaml` uses 64 zeros for `sha256`.
  - Fix: Compute real SHA-256 for each evidence file and update.
- Inconsistency: Dual manifest path bases.
  - Evidence: `frameworks/qa-test/artifacts/2025-09/handoff_manifest.yaml` uses repo-root relative paths; `frameworks/qa-test/manifests/2025-09/handoff_manifest.yaml` uses framework-root relative paths.
  - Fix: Standardize on repo-root relative (`frameworks/...`) and enforce in the generator.
- Governance: Ensure `governance.tags[]` present on every test mapping.
  - Evidence: Present in examples; enforce via schema/gate.

### Security Framework
- Risk: Open Critical finding without exception.
  - Evidence: `frameworks/security/artifacts/2025-09/sec_findings.yaml` → F-0001 severity Critical, status Open; `frameworks/security/policy/exceptions.md` does not scope F-0001.
  - Fix: Either (a) mitigate and set status Resolved with evidence, or (b) add a tightly scoped exception with `expires_on` and rationale.
- Governance: Ensure `governance.tags[]` (or `tags[]`) recorded in all artifacts, and manifest captures gate results with explicit pass/fail.
  - Evidence: Manifests include gates; add tags block if missing.
- Digest completeness: KPI and gate outcomes have TBD.
  - Fix: Populate digest with actual gate outcomes post-manifest sealing.

### Planning Framework
- Manifest immutability parity.
  - Evidence: `frameworks/planning-fe/manifests/2025-09-02-handoff_manifest.yaml` lacks `sealed: true` though it records `sealed_at`/`sealed_by`.
  - Fix: Add `sealed: true` to manifest schema and file for parity with other frameworks.
- Governance: Ensure `governance.tags[]` present across all planning artifacts (tasks, storymap, manifest).
  - Evidence: Present in FE manifest; add validation to gates.

### Observability Framework
- Strong alignment: lifecycle, gates, sealed manifest with checksums, explicit `Critical:0` in alert tags, parity/coverage gate requiring 100% KPI alert coverage.
- Minor: Confirm `rulebook_hash` semantics (currently hash of `alert_rules.md`); document as the alert rulebook hash.

## Cross-Framework Gaps and Inconsistencies
- Mixed artifact naming/extensions (MD vs YAML/JSON) impede schema-lint parity.
- Divergent manifest path bases (repo-root vs framework-root) create verification drift.
- `sealed` field inconsistency (present in QA/Security/Observability, absent in Planning FE) breaks immutability parity.
- Governance tags not uniformly required at schema-level across all artifacts.

## Actionable Fixes (Summary)
- QA: Convert compliance map to structured file; fix rulebook required list; compute real evidence hashes; standardize manifest paths.
- Security: Resolve F-0001 or file exception; fill digest KPIs; add tags block to manifest front matter if needed.
- Planning: Add `sealed: true` to FE manifest and schema; add validation to gates.
- Observability: Document `rulebook_hash` = normalized hash of `alert_rules.md` and keep as standard.
- Schemas/Gates: Align manifest schema fields across frameworks and enforce governance tags + quality gates uniformly.

## Cross-Framework Integration Plan
- Producers/Consumers:
  - Planning produces sealed `handoff_manifest.yaml` (FE/BE). QA consumes planning IDs (story_ref, endpoint_ref) for `test_matrix.yaml` mapping.
  - QA produces sealed `handoff_manifest.yaml` with `traceability_map.md`, `qa_evidence_index.yaml`. Security consumes QA evidence and emits exceptions when policy requires.
  - Security produces sealed manifest of `sec_findings.yaml`, `policy_map.md`, `exceptions.md`. Observability consumes tags and critical policy signal to enforce `Critical:0` on alerts.
  - Observability produces sealed manifest and `digests/YYYY-MM-DD-digest.md` KPIs. All frameworks consume digest KPIs for per-cycle reports.
- Events (Lifecycle): All frameworks adhere to PLANNED → READY_FOR_HANDOFF → PACKAGED → EXECUTED → VALIDATED → IMPROVE; manifests are sealed at PACKAGED and referenced in VALIDATED digests.

## Final Readiness Decision
- Decision: NO-GO
- Rationale: Open Security Critical (F-0001) without approved, time-bounded exception. Additional QA compliance map/schema drift and placeholder evidence hashes must be corrected to satisfy quality gates and governance invariants.