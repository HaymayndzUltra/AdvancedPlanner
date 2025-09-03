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