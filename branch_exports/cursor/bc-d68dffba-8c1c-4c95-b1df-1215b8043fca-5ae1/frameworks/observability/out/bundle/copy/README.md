Observability Framework
=======================

This repository segment contains the artifact-first Observability & Monitoring framework.

Directories
-----------
- `schemas/`: JSON Schemas for artifact validation.
- `tools/`: CLI validators and packaging utilities.
- `digests/`: Cycle-based operational digests.

Core Artifacts
--------------
- `logs_index.yaml`: Canonical log streams and schemas.
- `metrics_catalog.yaml`: Metrics/KPIs catalog with SLO bindings.
- `alert_rules.md`: Human rulebook describing alerts and governance tags.

Quick Start
-----------
1. (Optional) Create a Python virtual environment.
2. If venv is unavailable, you can run stdlib-only manifest generator.
3. Install requirements (CI or local with venv): `pip install -r tools/requirements.txt`.
4. Run gates:
   - `python tools/obs_cli.py schema-lint`
   - `python tools/obs_cli.py cross-consistency`
   - `python tools/obs_cli.py parity-coverage`
   - `python tools/obs_cli.py governance-check`
5. Package a handoff manifest:
   - With deps: `python tools/obs_cli.py generate-manifest --out out/handoff_manifest.yaml`
   - Stdlib-only: `python tools/generate_manifest_stdlib.py --snapshot main@abc1234 --out out/handoff_manifest.yaml`

Notes
-----
- Governance policy enforces `Critical=0` by default; exceptions must be tagged explicitly.
- Handoff manifests are immutable once sealed; new changes require a new manifest.

