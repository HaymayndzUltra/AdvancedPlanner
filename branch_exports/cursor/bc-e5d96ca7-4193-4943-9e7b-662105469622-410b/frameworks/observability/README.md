Observability & Monitoring Framework (Artifact-First)

Overview
This repo contains an artifact-first observability framework with immutable handoffs, automated quality gates, and governance integration.

Structure
- artifacts/: Authoritative YAML/MD artifacts (logs_index.yaml, metrics_catalog.yaml, alert_rules.md, handoff_manifest.yaml)
- schemas/: JSON/YAML schemas for validation
- tools/: CLI validators, packagers, and digest generator (Python)
- digests/: Per-cycle digest outputs
- .github/workflows/: CI workflows

Quickstart
1) Install Python 3.11+ and pipx or pip
2) pip install -r requirements.txt
3) make validate
4) make package
5) make digest

Make Targets
- make lint: Run static lint
- make validate: Run schema_lint + consistency + parity
- make package: Generate and seal handoff_manifest.yaml
- make verify: Verify sealed manifest against artifacts
- make digest: Generate cycle digest in digests/

Artifacts
- artifacts/logs_index.yaml
- artifacts/metrics_catalog.yaml
- artifacts/alert_rules.md
- artifacts/handoff_manifest.yaml (generated)
- digests/YYYY-MM-DD-digest.md (generated)

Governance
- Enforces Critical=0 by default via validators
- Requires tags: service, owner, tier, environment

Support
Contact: observability-framework@company.com
