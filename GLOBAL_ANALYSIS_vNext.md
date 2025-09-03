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

