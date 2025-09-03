## Executive summary
- Overall: frameworks are largely aligned on artifacts, gates, and sealing; gaps remain in governance, lifecycle explicitness, and snapshot consistency.
- Mixed snapshots across frameworks violate the “no mixed snapshots” rule for the same cycle.
- Governance tags: not present “everywhere” (manifests missing governance.tags[]); “Critical=0 or approved exception” is not uniformly enforced.
- Security: open Critical finding without a scoped, time‑boxed exception breaches Critical=0.
- Planning: lifecycle and gates are defined but not consistently surfaced in artifacts; digest/metrics present but partial placeholders.
- QA: strong implementation; add governance.tags[] to manifest to satisfy global rule.
- Observability: solid sealing and gates; add governance.tags[] to manifest for consistency with global rule.
- Metrics spine: digests exist in all four, but Security/Planning digests contain placeholders; add KPI baselines and gate evidence links.
- Compliance of evidence indices/checksums: mostly present; standardize rulebook_hash provenance and governance sections across manifests.
- Readiness: NO‑GO until snapshot and Critical=0 governance are corrected and governance tags are uniformly applied.

## Per‑framework findings and fixes

### QA
Findings
- Missing governance.tags[] at manifest level.
  - File: /workspace/frameworks/qa-test/artifacts/2025-09/handoff_manifest.yaml
  - Issue: no governance section; global rule requires governance.tags[] everywhere.
- “Critical=0 or exception” not explicitly recorded in manifest.
  - File: /workspace/frameworks/qa-test/artifacts/2025-09/handoff_manifest.yaml
  - Issue: no explicit governance.critical status or exception references.

Fixes
- Add governance section to manifest:
  - governance:
    - tags: [stream:qa, owner:qa-platform, environment:staging, Critical:0]
    - policy_exceptions_ref: frameworks/qa-test/artifacts/2025-09/policy_exceptions.md
- Add governance.critical_issues: 0 to manifest to codify Critical=0 state.
- Add KPI links in digest to gate evidence:
  - File: /workspace/frameworks/qa-test/digests/2025-09-02-digest.md
  - Add “Evidence” links for schema_lint, consistency, parity/coverage outputs.

### Security
Findings
- Critical finding without approved, scoped exception (breaches Critical=0 rule).
  - File: /workspace/frameworks/security/artifacts/2025-09/sec_findings.yaml (finding id F-0001; severity: Critical)
  - No matching approved exception in /workspace/frameworks/security/policy/exceptions.md.
- Manifest lacks governance.tags[] and explicit critical count.
  - File: /workspace/frameworks/security/manifests/2025-09/handoff_manifest.yaml
- Lifecycle states not explicitly captured in artifacts/digest.
  - File: /workspace/frameworks/security/digests/2025-09-02-digest.md (placeholders; no lifecycle status or evidence links)
- Snapshot alignment: uses git:abcdef1234 while other frameworks use branch@sha or a different commit (see Cross‑framework).

Fixes
- Add an approved exception for F‑0001 with expiry and compensating controls:
  - File: /workspace/frameworks/security/policy/exceptions.md
  - New entry: exception_id EX-2025-09-PII-LOGS, scope {service: payments-api}, related_findings [F-0001], expires_on 2025‑10‑15, compensating_controls (log sampling + runtime alerting), approved_by, status approved.
- Add governance to manifest:
  - governance:
    - tags: [stream:security, owner:team-appsec, environment:staging, Critical:0]
    - exceptions_ref: frameworks/security/policy/exceptions.md
  - governance.critical_issues: 0 (after exception approval) or leave >0 until exception is merged, then seal.
- Update digest with lifecycle section (PLANNED→…→IMPROVE) and gate evidence links; replace “TBD” with KPI skeletons for the cycle.
- Align snapshot_rev to the unified cycle snapshot (see Cross‑framework plan).

### Planning
Findings
- Lifecycle and gates documented but not universally reflected via governance and gates in artifacts.
  - Files:
    - /workspace/frameworks/planning-fe/manifests/2025-09-02-handoff_manifest.yaml (has governance and sealed fields; good)
    - /workspace/frameworks/planning-fe/digests/2025-09-02-digest.md (contains placeholders; add gate evidence and KPI baselines)
- Snapshot mismatch vs QA/Security/Observability (FE uses 986b378a…).
- Cross‑stream gate evidence missing in digest (links to BE deps and QA mapping).

Fixes
- Add explicit gate outcomes with evidence links to FE digest:
  - schema_lint: PASS with link to logs/output or manifest
  - cross_stream_consistency: PASS with link to QA test_matrix mapping to FE IDs and BE endpoints
  - parity/coverage: PASS with computed parity %
- Align snapshot_rev across frameworks for this cycle (see Cross‑framework).
- Ensure governance.tags[] standardized across planning FE artifacts (manifest already has; mirror tags in story_map front‑matter).

### Observability
Findings
- Manifest lacks governance.tags[].
  - File: /workspace/frameworks/observability/artifacts/handoff_manifest.yaml
- Good parity/coverage gate requiring KPI coverage; keep.

Fixes
- Add governance:
  - governance:
    - tags: [stream:observability, owner:obs-platform, environment:prod, Critical:0]
    - rulebook_ref: frameworks/observability/artifacts/alert_rules.md
- Add KPI evidence links to digest (generated by tools) if available.

## Cross‑framework gaps and fixes

Gaps
- Mixed snapshots across frameworks for the same cycle (“no mixed snapshots” violated):
  - QA: git:abcdef1234 (/workspace/frameworks/qa-test/artifacts/2025-09/test_matrix.yaml → handoff_manifest.yaml)
  - Security: git:abcdef1234 (/workspace/frameworks/security/manifests/2025-09/handoff_manifest.yaml)
  - Planning FE: 986b378aed13dd70… (/workspace/frameworks/planning-fe/manifests/2025-09-02-handoff_manifest.yaml)
  - Observability: main@986b378aed13dd70… (/workspace/frameworks/observability/artifacts/handoff_manifest.yaml)
- Governance.tags[] not present in all manifests/artifacts at a consistent location.
- Critical=0 enforcement not uniform (Security has open Critical without exception).
- Metrics spine/digests: placeholders in Security/Planning without gate evidence links.

Fixes
- Choose a single snapshot_rev for the cycle (recommend branch@986b378aed13dd70… for all four frameworks) and re‑seal manifests:
  - Update snapshot_rev and recompute checksums in each manifest.
- Add governance section to all manifests with tags[] and policy refs:
  - governance.tags[]: include at least stream, owner, environment, Critical:0
  - governance.*_ref fields: exceptions_ref/policy_exceptions_ref/rulebook_ref as applicable
  - governance.critical_issues: 0 (or include exception to reduce to 0)
- Update digests to include:
  - Gate outcomes with evidence links
  - KPI snapshot values (even if baseline) and per‑cycle digest compliance

## Cross‑framework integration plan
- Producers → Consumers:
  - Planning (FE/BE) produce: FE tasks, story map, FE manifest, FE digest
  - QA consumes: FE story IDs and BE endpoint IDs for test_matrix mappings; emits QA manifest and digest
  - Security consumes: code snapshot and policies; emits sec_findings, exceptions, security manifest and digest
  - Observability consumes: service taxonomy and deployment snapshot; emits logs_index, metrics_catalog, alert_rules, observability manifest and digest
- Artifacts/events:
  - Planning READY_FOR_HANDOFF triggers QA consistency checks (story_ref and endpoint_ref), Security policy scan, and Observability KPI catalog updates
  - PACKAGED seals per‑framework manifests with unified snapshot_rev
  - EXECUTED and VALIDATED produce digests referencing sealed manifests; IMPROVE seeds next cycle actions
- Uniform governance:
  - governance.tags[] present in all manifests
  - Critical=0 enforced at PACKAGED and VALIDATED across frameworks
  - Exceptions carry explicit expiry, compensating controls, and approver
