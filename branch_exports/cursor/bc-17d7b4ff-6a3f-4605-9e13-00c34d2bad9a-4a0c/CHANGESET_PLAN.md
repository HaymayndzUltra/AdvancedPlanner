## Ordered edits/additions (file → change)
1) /workspace/frameworks/security/policy/exceptions.md → Add approved exception for F‑0001 (PII in logs) with expiry and compensating controls.
2) /workspace/frameworks/security/manifests/2025-09/handoff_manifest.yaml → Add governance section (tags[], exceptions_ref, critical_issues) and align snapshot_rev; re‑seal.
3) /workspace/frameworks/qa-test/artifacts/2025-09/handoff_manifest.yaml → Add governance section (tags[], policy_exceptions_ref, critical_issues); re‑seal with unified snapshot_rev.
4) /workspace/frameworks/observability/artifacts/handoff_manifest.yaml → Add governance section (tags[], rulebook_ref, critical_issues); align snapshot_rev; re‑seal.
5) /workspace/frameworks/planning-fe/manifests/2025-09-02-handoff_manifest.yaml → Align snapshot_rev to unified value; ensure governance.tags[] are present; re‑seal.
6) /workspace/frameworks/security/digests/2025-09-02-digest.md → Replace placeholders with lifecycle status, KPI baselines, and gate evidence links.
7) /workspace/frameworks/planning-fe/digests/2025-09-02-digest.md → Add explicit gate outcomes and evidence links; include KPI baselines where feasible.
8) /workspace/frameworks/qa-test/digests/2025-09-02-digest.md → Add evidence links for gates and confirm Critical=0 statement referencing policy_exceptions.md.

## New/updated artifacts
- Name: Security exception (PII logs)
  - Path: /workspace/frameworks/security/policy/exceptions.md (append new entry)
  - Required fields: exception_id, title, owner, scope.service, related_findings[], justification, compensating_controls, expires_on, approved_by, status
  - Example stub:
    - exception_id: EX-2025-09-PII-LOGS
      title: Temporary waiver for PII redaction rollout
      owner: team-appsec
      scope: { service: payments-api, tags: [PII, logging] }
      related_findings: [F-0001]
      justification: Redaction patch rollout in progress; risk accepted temporarily.
      compensating_controls: increased monitoring, log sampling, alerting on PII patterns
      expires_on: "2025-10-15"
      approved_by: ciso@company.com
      status: approved

- Name: Governance block (manifests)
  - Paths:
    - /workspace/frameworks/security/manifests/2025-09/handoff_manifest.yaml
    - /workspace/frameworks/qa-test/artifacts/2025-09/handoff_manifest.yaml
    - /workspace/frameworks/observability/artifacts/handoff_manifest.yaml
  - Required fields:
    - governance:
      - tags: [stream:<name>, owner:<team>, environment:<env>, Critical:0]
      - exceptions_ref | policy_exceptions_ref | rulebook_ref: <path>
      - critical_issues: 0

- Name: Snapshot alignment (all manifests)
  - Paths:
    - /workspace/frameworks/security/manifests/2025-09/handoff_manifest.yaml
    - /workspace/frameworks/qa-test/artifacts/2025-09/handoff_manifest.yaml
    - /workspace/frameworks/observability/artifacts/handoff_manifest.yaml
    - /workspace/frameworks/planning-fe/manifests/2025-09-02-handoff_manifest.yaml
  - Required fields:
    - snapshot_rev: "main@986b378aed13dd70f678417f7725a3fac4458ed6" (or chosen unified snapshot)
    - artifacts[].sha256: recomputed
    - sealed metadata: updated on re‑seal

- Name: Gate evidence links (digests)
  - Paths:
    - /workspace/frameworks/security/digests/2025-09-02-digest.md
    - /workspace/frameworks/planning-fe/digests/2025-09-02-digest.md
    - /workspace/frameworks/qa-test/digests/2025-09-02-digest.md
  - Required fields:
    - Gate Outcomes section with PASS/FAIL and evidence links (logs or manifest paths)
    - KPI Summary with at least baseline placeholders and trends (if available)

## Gate checks after each change
- After 1–3:
  - schema_lint: Validate updated YAML/MD front‑matter (exceptions) and manifest schema.
  - cross_stream_consistency: For QA, re‑check story_ref/endpoint_ref mapping; for Security, re‑run taxonomy checks on findings.
  - parity/coverage: Confirm thresholds met (QA: critical path mapping; Security: presence of required artifacts).
- After 4–5:
  - schema_lint: Validate observability manifest against schema.
  - cross_stream_consistency: Observability tag requirements (service, owner, tier, environment).
  - parity/coverage: Ensure 100% KPI alert coverage remains satisfied.
- After 6–8:
  - Verify digests include gate evidence links and reflect governance Critical=0.

## Owners and deadlines (placeholders)
- Security exceptions/governance: Owner: team-appsec; Due: 2025-09-06
- QA manifest governance/snapshot: Owner: qa-platform; Due: 2025-09-06
- Observability manifest governance/snapshot: Owner: obs-platform; Due: 2025-09-06
- Planning FE snapshot/digest updates: Owner: planning-fe; Due: 2025-09-06
- Final cross‑framework verification and GO decision: Owner: release-management; Due: 2025-09-07