

# ===== MERGED FROM FINAL_CONSOLIDATED_REPORT1_V4.md =====

# GLOBAL_ANALYSIS_vNext.md

## Executive summary
- All frameworks conceptually align to lifecycle PLANNED → READY_FOR_HANDOFF → PACKAGED → EXECUTED → VALIDATED → IMPROVE, but several artifacts lack lifecycle_state fields.
- Sealed handoff manifests exist as stubs; checksums are placeholders and must be computed and frozen.
- Path inconsistencies exist for Observability digests and Security exceptions/waivers; standardize paths across docs and CI.
- Security gate uses summary.critical_open (present in one stub), but another stub omits summary; unify schema and CI evaluation.
- QA handoff manifest update shows only governance.tags[], not full sealing fields; confirm and backfill snapshot_rev, rulebook_hash, sealed, artifacts with checksums.
- Planning FE/BE manifests lack lifecycle_state; add and ensure a single snapshot_rev across FE/BE/QA/Security/Observability.
- Metrics spine incomplete: only Observability digest is defined; add per-cycle digests for Security, Planning, and QA.
- Governance: governance.tags[] is usually present, but enforce everywhere including digests and manifests; ensure Security exceptions carry approver, expiry, and rationale.
- CI/CD workflow and gates config are designed but not proven; wire them to enforce schema_lint, cross_stream_consistency, parity/coverage, and Critical=0.
- Readiness: NO-GO until evidence-backed digests are attached, checksums computed, paths normalized, and CI proves all gates on sealed, immutable artifacts.

## Global rules conformance (by evidence)
- Event lifecycle: partial. Missing lifecycle_state in several manifests/digests. See: /workspace/FINAL_CONSOLIDATED_REPORT_V3.md L137-L160, L183-L200, L206-L221, L312-L334, L601-L628. Lifecycle standard reference: /workspace/End_to_End_Master_Plan_WITH_Instructions.md L3325-L3329.
- Quality gates: declared; enforcement pending CI wiring. See: /workspace/FINAL_CONSOLIDATED_REPORT_V3.md L248-L260 (QA gates), L164-L179 (Security gate rule), L349-L368 and L669-L681 (CI config stubs).
- Immutable handoff: manifests marked sealed but have empty checksums; compute and freeze. See: /workspace/FINAL_CONSOLIDATED_REPORT_V3.md L147-L153, L195-L200, L218-L221, L322-L331, L588-L597, L644-L647.
- Governance: tags present in most stubs; ensure in all, including digests and exceptions. See: /workspace/FINAL_CONSOLIDATED_REPORT_V3.md L142-L147, L188-L195, L211-L218, L267-L269, L282-L284, L319-L321, L585-L587, L641-L647, L669-L681.
- Metrics spine: Observability digest defined; others missing. See: /workspace/FINAL_CONSOLIDATED_REPORT_V3.md L274-L309, L600-L628; memory bank index references additional digests that don’t exist yet, L339-L345, L655-L661.

## Per-framework findings and fixes

### Security
Gaps and inconsistencies
- Exceptions/waivers path conflict: /workspace/frameworks/security/policy/exceptions.yaml (L108-L131) vs frameworks/security/waivers.yaml (L495-L517) and CI expecting frameworks/security/waivers.yaml (L676-L679).
- findings.yaml schema divergence: release gate relies on summary.critical_open (L167-L176) but later stub (L473-L493) has findings[] without summary; current earlier stub (L89-L104) includes summary (L97-L101).
- Security handoff manifest lacks lifecycle_state and has empty checksums (L137-L160, L147-L153).
- No security per-cycle digest; memory index references a non-existent security digest (L340-L345 vs L655-L661).

Actionable fixes
- Standardize exceptions registry to /workspace/frameworks/security/waivers.yaml; update any references currently pointing to /workspace/frameworks/security/policy/exceptions.yaml (L108-L131).
- Unify findings.yaml schema to include both findings[] and summary.critical_open; adjust gate evaluation to compute summary if missing.
- Add lifecycle_state: PACKAGED to security handoff manifest and compute sha256 for findings.yaml and waivers.yaml before sealing.
- Add /workspace/frameworks/security/digests/2025-09/digest_2025-09-02.md with governance front matter, KPI summary (e.g., Critical=0 proof), and Gate Evidence; include governance.tags[].
- Update memory bank index to point to the added security digest (see Cross-framework fixes).

### Planning (FE/BE)
Gaps and inconsistencies
- FE/BE handoff manifests omit lifecycle_state; see FE L183-L200, BE L206-L221.
- Checksums are placeholders; must be computed and sealed (L195-L200, L218-L221).
- Planning sealed aggregator manifest path exists at frameworks/planning/manifests/... (L576), which is fine, but must also carry lifecycle_state and actual checksums (L579-L597).

Actionable fixes
- Add lifecycle_state: PACKAGED to FE/BE manifests and aggregator manifest.
- Compute sha256 for FE tasks and BE backlog; insert into FE/BE manifests and the planning aggregator manifest.
- Enforce snapshot_integrity across FE/BE/QA/Security/Observability at CI (L669-L681).

### QA
Gaps and inconsistencies
- Handoff manifest update only shows governance.tags[] (L264-L271); confirm snapshot_rev, rulebook_hash, sealed, artifacts with checksums are present; otherwise add.
- No QA per-cycle digest referenced; memory bank index implies a QA digest (L340-L345, L655-L661) but none is defined.

Actionable fixes
- Ensure /workspace/frameworks/qa-test/manifests/2025-09/handoff_manifest.yaml includes snapshot_rev, rulebook_hash, sealed, artifacts with sha256, lifecycle_state: PACKAGED.
- Add /workspace/frameworks/qa-test/digests/2025-09/digest_2025-09-02.md with KPIs (coverage, parity), Gate Evidence, governance.tags[].
- Keep QA gates config at /workspace/frameworks/qa-test/rules/gates.yaml (L248-L260); wire to CI.

### Observability
Gaps and inconsistencies
- Digest path inconsistent: /workspace/frameworks/observability/digests/2025-09-02-digest.md (L274-L309, L323-L325) vs /workspace/frameworks/observability/digests/2025-09/digest_2025-09-02.md (L600-L628); standardize.
- Digest sections are placeholders; Gate Evidence lacks concrete attachments (L292-L301).
- Observability handoff manifest lacks lifecycle_state (L312-L334).

Actionable fixes
- Standardize digest path to /workspace/frameworks/observability/digests/2025-09/digest_2025-09-02.md; update manifest references accordingly.
- Attach evidence artifacts (log excerpts, metric snapshots, CI outputs) and include their sha256 checksums in the observability handoff manifest.
- Add lifecycle_state: PACKAGED to observability handoff manifest.

## Cross-framework gaps and integration fixes

Gaps
- Mixed absolute vs relative paths across docs (e.g., L181-L224 vs L576-L681).
- Memory bank index paths inconsistent (L336-L347 vs L651-L660).
- CI wiring is illustrative only; enforcement not proven (L349-L368, L669-L681).

Fixes
- Normalize all references to absolute paths under /workspace/...; update all manifests and CI configs accordingly.
- Use a single memory bank index at /workspace/memory-bank/digests/2025-09/index.md referencing:
  - /workspace/frameworks/qa-test/digests/2025-09/digest_2025-09-02.md
  - /workspace/frameworks/security/digests/2025-09/digest_2025-09-02.md
  - /workspace/frameworks/planning/digests/2025-09/digest_2025-09-02.md
  - /workspace/frameworks/observability/digests/2025-09/digest_2025-09-02.md
- Finalize /.github/workflows/frameworks-governance.yml and /workspace/dev-workflow/ci/gates_config.yaml; ensure CI fails on any gate violation.

Smallest exceptions (time-bounded, with compensating controls)
- If Gate Evidence cannot be attached immediately: temporary exception OBS-EVIDENCE-EXP-2025-09 with 7-day expiry and compensating control of tightened monitoring and manual on-call validation.
- If an open critical Security finding exists: temporary waiver EX-CRIT-BLOCK-2025-09 with CISO approval, 14-day expiry, and added WAF rule plus high-sensitivity alerting.

## Cross-framework integration plan
- Producers → Artifacts → Consumers
  - Planning (FE/BE) → /workspace/frameworks/planning-*/manifests/... (sealed) → QA for parity and cross_stream_consistency; CI snapshot_integrity.
  - QA → /workspace/frameworks/qa-test/manifests/... (sealed), /workspace/frameworks/qa-test/digests/... → Observability Gate Evidence; CI parity/coverage and schema_lint.
  - Security → /workspace/frameworks/security/findings.yaml, /workspace/frameworks/security/waivers.yaml, /workspace/frameworks/security/digests/... → CI Critical=0 gate; Observability Gate Evidence.
  - Observability → /workspace/frameworks/observability/digests/... (evidence-attached), /workspace/frameworks/observability/manifests/... (sealed) → Memory bank index; Executive rollups.
  - Aggregation → /workspace/memory-bank/digests/2025-09/index.md → Executives, Audit, Runbooks.

## Final readiness decision
- Decision: NO-GO
- Rationale: Evidence attachments are missing, checksums are not computed, lifecycle_state missing in several artifacts, path inconsistencies unresolved, and CI enforcement is not yet proven on sealed artifacts with a single snapshot_rev and rulebook_hash.




---



# CHANGESET_PLAN_vNext.md

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

# ===== MERGED FROM FINAL_CONSOLIDATED_REPORT2_V4.md =====

## GLOBAL_ANALYSIS_vNext.md

### Executive summary
- Frameworks mostly align to lifecycle and gates; minor path/field drift remains.
- Single snapshot_rev used across stubs: git:abcdef1234; checksums still blank in sealed manifests.
- Security registry and release gate defined; findings content and CI evidence missing (see L27-L29, L349-L368).
- Exceptions path conflict: `policy/exceptions.yaml` vs `waivers.yaml` must be unified (see L108-L131 vs L495-L517, L676-L679).
- Planning FE/BE manifests added; add central sealed planning manifest and fill checksums (see L181-L223, L573-L597).
- QA gates declared; coverage metrics and evidence links not yet recorded (see L43-L45, L246-L260).
- Observability digest/manifest added; Gate Evidence placeholders need concrete artifacts and sha256s (see L46-L52, L273-L308, L312-L334).
- Metrics spine incomplete: missing per-cycle digests for Security, Planning, QA while Memory Bank index expects them (see L336-L345).
- CI workflow stub present; add gates config and correct paths; enforce block-on-fail (see L349-L368).
- Final readiness: NO-GO until evidence attached, checksums filled, and CI gates pass on sealed artifacts (see L69-L74).

### Per-framework findings (gaps, inconsistencies, risks) with actionable fixes

- Security
  - Gaps
    - Findings content not populated; Critical=0 unproven (L27-L29).
    - CI evidence not attached to Observability digest (L27-L29, L46-L52).
    - Metrics spine: no Security digest yet; Memory Bank expects it (L336-L345).
  - Inconsistencies
    - Exceptions path drift: `frameworks/security/policy/exceptions.yaml` (L108-L131) vs `frameworks/security/waivers.yaml` (L495-L517) and CI pointing to waivers (L676-L679).
    - Field drift: `cycle` (L90) vs `cycle_id` (L480) across security stubs.
  - Fixes
    - Populate `findings.yaml` with real findings; keep `summary.critical_open` accurate and set `lifecycle_state` to READY_FOR_HANDOFF.
    - Standardize on `frameworks/security/policy/exceptions.yaml`; update all references (including CI config) to that path.
    - Add Security digest `frameworks/security/digests/2025-09-02-digest.md` with KPI + Gate Evidence; link from Observability and Memory Bank.
    - Fill sha256s in `frameworks/security/manifests/2025-09/handoff_manifest.yaml` artifacts and set `sealed: true` only when hashes present (L135-L160).
    - Normalize field name to `cycle` across Security artifacts; include `governance.tags[]` everywhere.

- Planning (FE/BE)
  - Gaps
    - Confirm `governance.fields[]` values and run cross_stream_consistency with QA (L35-L36).
    - Checksums blank in FE/BE manifests (L181-L223).
    - No central sealed planning manifest aggregating FE/BE artifacts in earlier section; later section introduces it (L573-L597).
    - Metrics spine: no FE/BE digests present; Memory Bank index expects them (L336-L345).
  - Inconsistencies
    - Field drift: `cycle_id` used in FE/BE manifests (L185, L208) while other manifests use `cycle`.
  - Fixes
    - Add central `frameworks/planning/manifests/2025-09/handoff_manifest.yaml` that seals FE/BE artifacts with sha256s (L573-L597).
    - Compute and fill sha256s for FE/BE artifacts; ensure `sealed: true` only after hashing.
    - Add Planning-FE and Planning-BE digests under `frameworks/planning-fe/digests/2025-09-02-digest.md` and `frameworks/planning-be/digests/2025-09-02-digest.md`.
    - Normalize to `cycle` in Planning manifests; keep `governance.tags[]` and `snapshot_rev` present.

- QA
  - Gaps
    - Record actual parity/coverage metrics and evidence links; integrate with Observability (L43-L45).
    - Metrics spine: no QA digest yet; Memory Bank index expects one (L336-L345).
  - Inconsistencies
    - None material; gates declared (L246-L260) and governance tags added to handoff (L264-L270), but coverage evidence missing.
  - Fixes
    - Update `frameworks/qa-test/artifacts/2025-09/compliance_map.md` with populated `evidence_refs` and mapped `test_ids` (L225-L244).
    - Add QA digest `frameworks/qa-test/digests/2025-09-02-digest.md` with KPI + Gate Evidence; link from Memory Bank.
    - Ensure QA handoff manifest remains sealed with single `snapshot_rev` and `governance.tags[]` (L264-L270).

- Observability
  - Gaps
    - Gate Evidence is placeholder; attach concrete logs/metrics/CI outputs and hash in manifest (L46-L52, L273-L308, L312-L334).
  - Inconsistencies
    - Digest path drift: `frameworks/observability/digests/2025-09-02-digest.md` (L273-L308) vs `frameworks/observability/digests/2025-09/digest_2025-09-02.md` (L599-L628).
  - Fixes
    - Standardize digest path to `frameworks/observability/digests/2025-09-02-digest.md`; ensure manifest references that exact path (L312-L334).
    - Attach evidence artifacts and compute sha256s before setting `sealed: true`.

### Global rules consistency check

- Event lifecycle
  - Partially met: lifecycle noted for some Security artifacts (L103, L130); missing on most manifests/digests. Fix: add `lifecycle_state` to all artifacts; advance states as gates pass.
- Quality gates
  - Declared: QA gates (L246-L260), Security release gate (L164-L179). CI stub exists (L349-L368) but needs concrete config and enforcement. Fix: add `dev-workflow/ci/gates_config.yaml` and enforce block_on_fail.
- Immutable handoff
  - Partially met: manifests marked `sealed` but sha256s are empty (e.g., L147-L153, L321-L325). Fix: compute and fill checksums; seal only when complete; validate single `snapshot_rev` across frameworks (L16, L71).
- Governance
  - Mostly present (`governance.tags[]` across stubs), but ensure everywhere including new digests/manifests (multiple references throughout, e.g., L142-L146, L188-L193, L232-L235, L319-L321).
- Metrics spine
  - Incomplete: Only Observability digest defined; Security/Planning/QA digests missing (L336-L345). Fix: add per-framework digests and link from Memory Bank.

### Cross-framework integration plan (producers → consumers)
- Security → `frameworks/security/findings.yaml`, `frameworks/security/policy/exceptions.yaml` → CI gate `security_critical_zero`, Observability Gate Evidence (see L164-L179, L349-L368).
- Planning (FE/BE) → sealed `frameworks/planning/manifests/2025-09/handoff_manifest.yaml` → QA cross_stream_consistency, CI snapshot_integrity, Observability (see L573-L597).
- QA → `frameworks/qa-test/artifacts/2025-09/handoff_manifest.yaml`, `compliance_map.md` → CI schema_lint, parity/coverage; Observability (see L225-L244, L264-L270).
- Observability → `frameworks/observability/digests/2025-09-02-digest.md`, sealed manifest → Memory Bank (see L273-L308, L312-L334).
- Memory Bank → `memory-bank/digests/2025-09/index.md` collects all per-cycle digests (see L336-L345).
- CI → `/.github/workflows/frameworks-governance.yml` + `dev-workflow/ci/gates_config.yaml` enforce gates and block on fail (see L349-L368).

### Final readiness decision
- NO-GO: Evidence attachments and checksums are incomplete; CI gate enforcement not proven; digest coverage across all frameworks missing (see L69-L74).


---



## CHANGESET_PLAN_vNext.md

### Ordered, idempotent edits (path → change)
1) `/workspace/frameworks/security/findings.yaml` → ADD/POPULATE → Real findings with accurate `summary.critical_open`; ensure `governance.tags[]`, `snapshot_rev`, `rulebook_hash`, `lifecycle_state`.
2) `/workspace/frameworks/security/policy/exceptions.yaml` → ADD/ALIGN → Canonical exceptions registry with expiry, approver, rationale, compensating controls; use this path everywhere (unify vs `waivers.yaml`).
3) `/workspace/frameworks/security/manifests/2025-09/handoff_manifest.yaml` → UPDATE → Compute and fill `sha256` for artifacts; keep `sealed: true` only when complete.
4) `/workspace/frameworks/security/rules/release_gates.yaml` → ADD → Enforce Critical=0 from findings registry.
5) `/workspace/dev-workflow/ci/gates_config.yaml` → ADD → Configure gates; set `exceptions: frameworks/security/policy/exceptions.yaml` (replace `waivers.yaml`).
6) `/workspace/frameworks/planning-fe/manifests/2025-09-02-handoff_manifest.yaml` → ADD → FE handoff manifest; fill artifact `sha256`s; normalize to `cycle` field.
7) `/workspace/frameworks/planning-be/manifests/2025-09-02-handoff_manifest.yaml` → ADD → BE handoff manifest; fill artifact `sha256`s; normalize to `cycle`.
8) `/workspace/frameworks/planning/manifests/2025-09/handoff_manifest.yaml` → ADD → Central sealed manifest aggregating FE/BE artifacts with `sha256`s.
9) `/workspace/frameworks/planning-fe/tasks/2025-09-02-fe_task_breakdown.yaml` → UPDATE → Add `governance.fields[]`, `governance.tags[]`; ensure `snapshot_rev`, `rulebook_hash`.
10) `/workspace/frameworks/planning-be/backlog/2025-09-02-be_backlog.yaml` → UPDATE → Add `governance.fields[]`, `governance.tags[]`; ensure `snapshot_rev`, `rulebook_hash`.
11) `/workspace/frameworks/qa-test/artifacts/2025-09/compliance_map.md` → ADD/UPDATE → Ensure front matter and populate `test_ids` and `evidence_refs`.
12) `/workspace/frameworks/qa-test/rules/gates.yaml` → ADD → Declare QA gates and parity threshold.
13) `/workspace/frameworks/qa-test/manifests/2025-09/handoff_manifest.yaml` → UPDATE → Ensure `governance.tags[]`, single `snapshot_rev`, and sealed checksums present.
14) `/workspace/frameworks/observability/digests/2025-09-02-digest.md` → ADD → Standardize digest path; include KPI + Gate Evidence; attach evidence links.
15) `/workspace/frameworks/observability/manifests/2025-09/handoff_manifest.yaml` → ADD → Seal digest; compute `sha256` for attachments.
16) `/workspace/frameworks/security/digests/2025-09-02-digest.md` → ADD → Security per-cycle digest with KPI + Gate Evidence.
17) `/workspace/frameworks/planning-fe/digests/2025-09-02-digest.md` and `/workspace/frameworks/planning-be/digests/2025-09-02-digest.md` → ADD → Planning digests (FE and BE).
18) `/workspace/frameworks/qa-test/digests/2025-09-02-digest.md` → ADD → QA per-cycle digest with KPI + Gate Evidence.
19) `/workspace/memory-bank/digests/2025-09/index.md` → ADD/UPDATE → Collect all per-cycle digests (QA, Security, Planning-FE/BE, Observability).
20) `/.github/workflows/frameworks-governance.yml` → ADD → CI workflow stub to run gates on PRs under `frameworks/**`.

### New/updated artifacts (required fields + stub snippets)

- Security Findings
  - name: security findings
  - path: `frameworks/security/findings.yaml`
  - required: `schema_version`, `cycle`, `snapshot_rev`, `rulebook_hash`, `governance.tags[]`, `summary`, `findings[]`, `lifecycle_state`
~~~yaml
schema_version: 1
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:TBD_rulebook_hash"
governance:
  tags: [security, critical_zero, release]
summary:
  critical_open: 0
  high_open: 0
  medium_open: 0
  low_open: 0
findings: []
lifecycle_state: READY_FOR_HANDOFF
~~~

- Security Exceptions (canonical)
  - name: security policy exceptions
  - path: `frameworks/security/policy/exceptions.yaml`
  - required: `schema_version`, `cycle`, `snapshot_rev`, `rulebook_hash`, `governance.tags[]`, `exceptions[] {exception_id, rule_id, scope, owner, approver, expiry, rationale, compensating_controls}`, `lifecycle_state`
~~~yaml
schema_version: 1
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:TBD_rulebook_hash"
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
~~~

- Security Release Gates
  - name: security release gates
  - path: `frameworks/security/rules/release_gates.yaml`
  - required: `policy_version`, `rules[]`, `governance.tags[]`
~~~yaml
policy_version: 1
rules:
  - id: "critical_zero_enforcement"
    description: "Block release if summary.critical_open > 0"
    source: "frameworks/security/findings.yaml"
    evaluation:
      condition: "summary.critical_open == 0"
      on_fail: "block_release"
governance:
  tags: [security, gate]
~~~

- Security Handoff Manifest (seal with hashes)
  - name: security handoff manifest
  - path: `frameworks/security/manifests/2025-09/handoff_manifest.yaml`
  - required: `manifest_version`, `cycle`, `snapshot_rev`, `rulebook_hash`, `sealed`, `governance.tags[]`, `artifacts[] {name, path, sha256}`, `quality_gates`, `lifecycle_state`
~~~yaml
manifest_version: 1
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:TBD_rulebook_hash"
governance:
  tags: [security, release, critical_zero]
  rationale: "Release readiness: Critical=0; waivers tracked."
  expiry: "2025-10-31"
sealed: true
artifacts:
  - name: findings
    path: frameworks/security/findings.yaml
    sha256: "<fill>"
  - name: exceptions
    path: frameworks/security/policy/exceptions.yaml
    sha256: "<fill>"
quality_gates:
  schema_lint: pass
  cross_stream_consistency: pass
  parity_coverage:
    status: pass
    coverage_pct: 100.0
lifecycle_state: READY_FOR_HANDOFF
~~~

- Planning FE Handoff Manifest
  - name: planning fe handoff manifest
  - path: `frameworks/planning-fe/manifests/2025-09-02-handoff_manifest.yaml`
  - required: `manifest_version`, `cycle`, `snapshot_rev`, `rulebook_hash`, `governance.tags[]`, `governance.fields{owner,risk,compliance}`, `sealed`, `artifacts[] {path, sha256}`
~~~yaml
manifest_version: 1
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:TBD_rulebook_hash"
governance:
  tags: [planning, fe, release]
  fields:
    owner: "fe-planning@company"
    risk: "low"
    compliance: ["none"]
sealed: true
artifacts:
  - path: frameworks/planning-fe/tasks/2025-09-02-fe_task_breakdown.yaml
    sha256: "<fill>"
  - path: frameworks/planning-fe/storymaps/2025-09-02-story_map.md
    sha256: "<fill>"
~~~

- Planning BE Handoff Manifest
  - name: planning be handoff manifest
  - path: `frameworks/planning-be/manifests/2025-09-02-handoff_manifest.yaml`
  - required: as above
~~~yaml
manifest_version: 1
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:TBD_rulebook_hash"
governance:
  tags: [planning, be, release]
  fields:
    owner: "be-planning@company"
    risk: "low"
    compliance: ["none"]
sealed: true
artifacts:
  - path: frameworks/planning-be/backlog/2025-09-02-be_backlog.yaml
    sha256: "<fill>"
~~~

- Central Planning Handoff Manifest
  - name: planning handoff manifest (central)
  - path: `frameworks/planning/manifests/2025-09/handoff_manifest.yaml`
  - required: `manifest_version`, `cycle`, `snapshot_rev`, `rulebook_hash`, `sealed`, `governance.tags[]`, `artifacts[]`, `quality_gates`, `lifecycle_state`
~~~yaml
manifest_version: 1
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:TBD_rulebook_hash"
sealed: true
governance:
  tags: [planning, sealed]
artifacts:
  - name: planning_fe_tasks
    path: frameworks/planning-fe/tasks/2025-09-02-fe_task_breakdown.yaml
    sha256: "<fill>"
  - name: planning_be_backlog
    path: frameworks/planning-be/backlog/2025-09-02-be_backlog.yaml
    sha256: "<fill>"
quality_gates:
  schema_lint: pass
  snapshot_integrity: pass
lifecycle_state: READY_FOR_HANDOFF
~~~

- QA Compliance Map
  - name: qa compliance map
  - path: `frameworks/qa-test/artifacts/2025-09/compliance_map.md`
  - required: front matter with `schema_version`, `cycle`, `snapshot_rev`, `rulebook_hash`, `governance.tags[]`
~~~markdown
---
schema_version: 1
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:TBD_rulebook_hash"
governance:
  tags: [qa, compliance]
---
# Compliance Map — 2025-09

- standard: ISO27001
  control: LOG-RED-001
  test_ids: [QA-API-ADDR-VAL-001]
  evidence_refs: [artifacts/2025-09/evidence/addr_validate_postman.json]
~~~

- QA Gates
  - name: qa gates
  - path: `frameworks/qa-test/rules/gates.yaml`
  - required: `schema_version`, `parity_threshold`, `gates[]`, `governance.tags[]`
~~~yaml
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
~~~

- QA Handoff Manifest (update)
  - name: qa handoff manifest
  - path: `frameworks/qa-test/manifests/2025-09/handoff_manifest.yaml`
  - change: ensure `governance.tags[]`, `sealed`, single `snapshot_rev`

- Observability Digest
  - name: observability cycle digest
  - path: `frameworks/observability/digests/2025-09-02-digest.md`
  - required: front matter + KPI, Gate Evidence, Incident Summaries
~~~markdown
---
schema_version: 1
date: "2025-09-02"
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:TBD_rulebook_hash"
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
~~~

- Observability Handoff Manifest
  - name: observability handoff manifest
  - path: `frameworks/observability/manifests/2025-09/handoff_manifest.yaml`
  - required: `manifest_version`, `cycle`, `snapshot_rev`, `rulebook_hash`, `sealed`, `governance.tags[]`, `artifacts[]`, `quality_gates`
~~~yaml
manifest_version: 1
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:TBD_rulebook_hash"
governance:
  tags: [observability, release]
sealed: true
artifacts:
  - name: digest_2025-09-02
    path: frameworks/observability/digests/2025-09-02-digest.md
    sha256: "<fill>"
quality_gates:
  schema_lint: pass
  cross_stream_consistency: pass
  parity_coverage:
    status: pass
    coverage_pct: 100.0
~~~

- Per-cycle Digests for Security, Planning-FE/BE, QA
  - paths:
    - `frameworks/security/digests/2025-09-02-digest.md`
    - `frameworks/planning-fe/digests/2025-09-02-digest.md`
    - `frameworks/planning-be/digests/2025-09-02-digest.md`
    - `frameworks/qa-test/digests/2025-09-02-digest.md`
  - required: front matter (`schema_version`, `date`, `cycle`, `snapshot_rev`, `rulebook_hash`, `governance.tags[]`) + KPI + Gate Evidence sections.

- Memory Bank Index
  - name: digests index
  - path: `memory-bank/digests/2025-09/index.md`
  - required: links to all per-cycle digests
~~~markdown
# Digest Index — 2025-09
- QA: frameworks/qa-test/digests/2025-09-02-digest.md
- Security: frameworks/security/digests/2025-09-02-digest.md
- Planning-FE: frameworks/planning-fe/digests/2025-09-02-digest.md
- Planning-BE: frameworks/planning-be/digests/2025-09-02-digest.md
- Observability: frameworks/observability/digests/2025-09-02-digest.md
~~~

- CI Gates Configuration
  - name: CI gates config
  - path: `dev-workflow/ci/gates_config.yaml`
  - required: `schema_version`, `gates`, `enforcement_mode: block_on_fail`
~~~yaml
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
    exceptions: frameworks/security/policy/exceptions.yaml
enforcement_mode: block_on_fail
~~~

### Gate checks to run after each change
- After Security (1–5): security_critical_zero → PASS when `summary.critical_open == 0` OR exceptions valid/unexpired with compensating controls.
- After QA/Planning (6–13): schema_lint → PASS; snapshot_integrity → PASS (all `snapshot_rev == git:abcdef1234`); cross_stream_consistency → PASS (QA story_ref ↔ Planning endpoint_ref align).
- After Observability (14–15): schema_lint + evidence_present → PASS (Gate Evidence sections populated with links); sealed manifest validates sha256s.
- After Metrics Spine (16–19): Memory Bank links resolve; all digests present and linted.
- After CI (20 + gates_config): Dry-run PR checks → PASS; CI fails on any gate failure.

### Owners & deadlines (placeholders)
- Security (1–5, 16): security-platform@company — 2025-09-07
- Planning (6–10, 17): planning-pmo@company — 2025-09-09
- QA (11–13, 18): qa-platform@company — 2025-09-08
- Observability (14–15): sre-observability@company — 2025-09-07
- Integration/Memory Bank/CI (19–20): release-eng@company — 2025-09-08

Assumptions
- Use `cycle` as the normalized field for manifests/registries; `cycle_id` may remain in legacy artifacts if tooling requires, but new/updated items use `cycle`.
- Digest paths standardized to `.../digests/2025-09-02-digest.md` across frameworks for this cycle.