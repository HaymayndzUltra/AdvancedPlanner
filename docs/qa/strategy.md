---
owner: qa-engineering
version: 1.0.0
last_updated: 2025-09-02
quality_targets:
  coverage_min: 0.80
  flake_rate_max: 0.02
  ci_stability: green_main_and_integration
integration_requirements:
  - contract_tests_gate_merges
  - defect_reporting_to_implementation_and_architecture
---

### QA & Test Strategy

This strategy defines the quality approach, test suites, data management, and CI quality gates for this repository. It aligns with the product requirements, data contracts under `docs/data/contracts`, and the CI gates config in `dev-workflow/ci/gates_config.yaml`.

### Test Types and Scope
- **Unit tests**: Validate pure functions in `data/pipelines/pipeline.py` (masking, anonymization, tokenization, constraints building, validation logic).
- **Integration tests**: Run `run_pipeline(...)` for each dataset against sample CSVs, verifying schema compliance, privacy transforms, and output artifacts.
- **Contract tests (gate)**: Parse contracts in `docs/data/contracts/*.md`, resolve referenced schema, and assert schema enforces contract DQ expectations (unique, enums, formats). Failures block merges.
- **E2E tests**: Execute pipelines end-to-end (subprocess) on valid and invalid datasets; assert success path artifacts and failure path validation reports.

### Coverage & Flakiness
- **Coverage target**: >= 80% line coverage on `data/pipelines/pipeline.py` measured by `pytest-cov`.
- **Flake rate target**: < 2%. CI runs tests twice and computes flaky rate from JUnit results; exceeding threshold fails the build.

### Test Data Management
- **Seed data**: Canonical valid samples live in `data/pipelines/samples/*.csv` (source of truth).
- **Invalid seeds**: Tests generate minimal invalid CSVs in temp dirs (no secrets). E2E tests assert validation reports are produced on failure.
- **Schemas**: Canonical YAML schemas live at `docs/data/schemas/*.yaml` and are referenced by the pipeline. Contract tests verify presence and alignment.

### Privacy & Security Validations
- Users: email masked, phone cleared for non-admin contexts, name partially redacted.
- Session events: IP anonymized (IPv4 zero last two octets, IPv6 /64 network address).
- Transactions: PAN fragments tokenized; raw fragments removed.

### CI Pipeline Overview (ci/*)
- Install deps; cache venv when possible.
- Run unit/integration/contract/E2E tests with coverage and JUnit output.
- Re-run tests to measure flakiness; enforce < 2%.
- Enforce coverage >= 80% via quality gate.
- Enforce contract gate via `ci/contract_gate.py`.
- Publish reports to `ci/reports/*` as build artifacts.

### Quality Gates
- CI must be green on `main` and `integration`.
- Block merges on: contract test failures, coverage < 80%, flake rate >= 2%, or missing framework evidence referenced by `dev-workflow/ci/gates_config.yaml`.

### Defect Reporting
- Test failures under `tests/contract/*` are tagged Architecture.
- Other failures are tagged Implementation.
- CI emits `ci/reports/defects.json` summarizing failures; share with the respective owners.

### Local Developer Workflow
- `make venv && make install` to set up.
- `make test` to run full suite with coverage.
- `make ci` to run CI-equivalent checks locally.

### Change Management
- Update schemas and contract tests alongside any contract change.
- Breaking pipeline changes require updating integration and E2E tests.