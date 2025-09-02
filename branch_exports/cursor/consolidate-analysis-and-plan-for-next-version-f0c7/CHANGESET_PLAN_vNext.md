## Ordered, Idempotent Task List (completed)

1) frameworks/security/findings.yaml → ADD → Critical=0 registry
2) frameworks/security/policy/exceptions.yaml → ADD → Waiver schema
3) frameworks/security/waivers.yaml → ADD → Exceptions registry
4) frameworks/security/rules/release_gates.yaml → ADD → Critical=0 enforcement
5) frameworks/security/manifests/2025-09/handoff_manifest.yaml → ADD → Sealed with checksums
6) frameworks/planning-fe/tasks/2025-09-02-fe_task_breakdown.yaml → ADD → Governance fields
7) frameworks/planning-fe/storymaps/2025-09-02-story_map.md → ADD → Story map with metadata
8) frameworks/planning-fe/manifests/2025-09-02-handoff_manifest.yaml → ADD → Sealed with checksums
9) frameworks/planning-be/backlog/2025-09-02-be_backlog.yaml → ADD → Governance fields
10) frameworks/planning-be/manifests/2025-09-02-handoff_manifest.yaml → ADD → Sealed with checksums
11) frameworks/planning/manifests/2025-09/handoff_manifest.yaml → ADD → Sealed consolidated planning manifest
12) frameworks/qa-test/artifacts/2025-09/compliance_map.md → ADD → Metadata header
13) frameworks/qa-test/rules/gates.yaml → ADD → QA gates declaration
14) frameworks/qa-test/manifests/2025-09/handoff_manifest.yaml → ADD → Sealed with checksum
15) frameworks/observability/digests/2025-09-02-digest.md → ADD → KPI + Gate Evidence
16) frameworks/observability/manifests/2025-09/handoff_manifest.yaml → ADD → Sealed with checksum
17) memory-bank/digests/2025-09/index.md → ADD → Digest index
18) .github/workflows/frameworks-governance.yml → ADD → CI governance workflow
19) dev-workflow/ci/gates_config.yaml → ADD → CI gates config

## Sealing and Checksums
- Computed SHA-256 for all manifest-referenced artifacts using `dev-workflow/seal.py` and updated `sha256:` fields.

## Validation Evidence
- Ran `dev-workflow/validate.py` and produced `dev-workflow/validation/results.json`.
- Gate outcomes:
  - schema_lint: PASS
  - snapshot_integrity: PASS
  - cross_stream_consistency: PASS
  - parity_coverage: PASS (threshold 0.90, coverage 1.0)
  - security_critical_zero: PASS

## Post-change Actions
- CI will enforce the same gates via `gates_config.yaml` and the GitHub workflow on PRs under `frameworks/**`.

