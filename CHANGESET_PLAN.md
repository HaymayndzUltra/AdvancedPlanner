# CHANGESET PLAN

## Ordered Edits and Additions
1) frameworks/security/artifacts/2025-09/sec_findings.yaml → Change F-0001 status to Resolved with evidence_uri OR scope an exception (see 2).
2) frameworks/security/policy/exceptions.md → Add exception for F-0001 (Temporary waiver), include: justification, compensating controls, approved_by, expires_on.
3) frameworks/qa-test/rules/rulebook.yaml → Update `artifacts.required` entry from `qa_evidence_index.md` to `qa_evidence_index.yaml`.
4) frameworks/qa-test/artifacts/2025-09/compliance_map.md → Replace with structured file: `frameworks/qa-test/artifacts/2025-09/compliance_map.yaml` (or `.json`) matching `schemas/compliance_map.schema.json`. Update references in `handoff_manifest.yaml`.
5) frameworks/qa-test/artifacts/2025-09/qa_evidence_index.yaml → Replace placeholder SHA256 values with real checksums for each evidence file.
6) frameworks/qa-test/cli/qa_framework.py → Standardize manifest paths to repo-root relative when sealing (ensure `path: frameworks/qa-test/artifacts/...`).
7) frameworks/qa-test/manifests/2025-09/handoff_manifest.yaml → Re-gen after (6) to unify path base.
8) frameworks/planning-fe/manifests/2025-09-02-handoff_manifest.yaml → Add `sealed: true` under top-level to enforce immutability parity.
9) frameworks/security/digests/2025-09-02-digest.md → Populate KPI and gate outcomes from the generated manifest; remove TBD placeholders.
10) schemas alignment (optional but recommended): Align manifest schemas across frameworks to require: `sealed` (boolean), `quality_gates` object with `schema_lint`, `cross_stream_consistency`, `parity_coverage`, and optional `compliance_check`.

## New/Updated Artifacts (Required Fields + Example Stubs)
- Name: Compliance Map (QA)
  - Path: frameworks/qa-test/artifacts/2025-09/compliance_map.yaml
  - Required fields: schema_version (int), cycle_id (string), mappings[] (standard, control, test_ids[], evidence_refs[])
  - Example stub:
    ```yaml
    schema_version: 1
    cycle_id: "2025-09"
    mappings:
      - standard: ISO27001
        control: LOG-RED-001
        test_ids: [QA-API-ADDR-VAL-001]
        evidence_refs: [evidence/addr_validate_postman.json]
    ```

- Name: Security Exception (F-0001)
  - Path: frameworks/security/policy/exceptions.md
  - Required fields (front matter): schema_version, cycle_id, registry[] (exception_id, title, owner, scope, justification, expires_on, ticket, approved_by, status)
  - Example stub:
    ```markdown
    ---
    schema_version: 1
    cycle_id: "2025-09-02"
    registry:
      - exception_id: EX-2025-09-XXX
        title: Temporary waiver for PII log redaction rollout
        owner: team-appsec
        scope:
          service: payments-api
          tags: [PII, logging]
          applies_to_findings: [F-0001]
        justification: Redaction rollout in progress; risk accepted with monitoring.
        expires_on: "2025-09-30"
        ticket: SEC-9999
        approved_by: ciso@company.com
        status: approved
    ---
    ```

- Name: Planning FE Manifest (sealed)
  - Path: frameworks/planning-fe/manifests/2025-09-02-handoff_manifest.yaml
  - Required field addition: `sealed: true`
  - Example stub (addition only):
    ```yaml
    sealed: true
    ```

## Gate Checks After Each Change
- After 1/2: Run Security validate + generate-manifest; ensure quality_gates all pass; Critical=0 or approved exception recorded.
- After 3/4/5/6/7: Run QA `qa_framework.py all` (or `make qa-manifest`), verify schema_lint, cross_stream_consistency, parity_coverage all pass; verify manifest schema; ensure `rulebook_hash` and unified paths.
- After 8: Recompute FE manifest checksum; validate digest links; confirm `sealed` present.
- After 9: Re-run Security digest generation; verify KPIs not TBD.
- After 10: Run CI for all schemas to confirm alignment.

## Owners and Deadlines (Placeholders)
- QA: qa-platform@company — Due: 2025-09-05
- Security: appsec@company — Due: 2025-09-03
- Planning FE: planning-fe@company — Due: 2025-09-03
- Observability: obs-platform@company — Due: 2025-09-04
- Integration (schemas/gates standardization): architecture@company — Due: 2025-09-09