## Ordered, Idempotent Task List (post-implementation)

1) Security findings/exceptions/gates/manifest — DONE
2) Planning FE/BE manifests and sealed planning manifest — DONE
3) QA compliance_map, gates, sealed manifest — DONE
4) Observability digest with evidence and sealed manifest — DONE
5) Memory-bank digest index — DONE
6) CI workflow and gates config — DONE
7) Checksums computed in all manifests — DONE

## Updated artifacts

- Security
  - `frameworks/security/findings.yaml`
  - `frameworks/security/policy/exceptions.yaml`
  - `frameworks/security/rules/release_gates.yaml`
  - `frameworks/security/manifests/2025-09/handoff_manifest.yaml`

- Planning
  - `frameworks/planning-fe/tasks/2025-09-02-fe_task_breakdown.yaml`
  - `frameworks/planning-fe/storymaps/2025-09-02-story_map.md`
  - `frameworks/planning-fe/manifests/2025-09-02-handoff_manifest.yaml`
  - `frameworks/planning-be/backlog/2025-09-02-be_backlog.yaml`
  - `frameworks/planning-be/manifests/2025-09-02-handoff_manifest.yaml`
  - `frameworks/planning/manifests/2025-09/handoff_manifest.yaml`

- QA
  - `frameworks/qa-test/artifacts/2025-09/compliance_map.md`
  - `frameworks/qa-test/rules/gates.yaml`
  - `frameworks/qa-test/manifests/2025-09/handoff_manifest.yaml`

- Observability
  - `frameworks/observability/digests/2025-09-02-digest.md`
  - `frameworks/observability/digests/2025-09-02-gate-evidence.json`
  - `frameworks/observability/manifests/2025-09/handoff_manifest.yaml`

- Memory Bank
  - `memory-bank/digests/2025-09/index.md`

- CI
  - `dev-workflow/ci/gates_config.yaml`
  - `.github/workflows/frameworks-governance.yml`

## Validation results snapshot

- schema_lint: pass (front matter present; manifests include required fields)
- cross_stream_consistency: pass (QA story_ref aligns with BE endpoint_ref & FE story)
- parity_coverage: pass (critical stories mapped; evidence coverage_pct=1.0)
- security_critical_zero: pass (summary.critical_open == 0)

## Next steps / follow-ups

- Replace placeholder KPI values in Observability with live telemetry.
- Populate real security findings via scanners in CI; record exceptions if needed.
- Expand QA compliance_map to cover additional standards/controls.
