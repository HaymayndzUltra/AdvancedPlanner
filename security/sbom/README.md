# SBOM

This repository publishes an SPDX JSON SBOM via CI at `security/sbom/sbom.spdx.json`.

Local generation options:
- If you have Syft installed:
  - `syft dir:. -o spdx-json > security/sbom/sbom.spdx.json`
- Via the helper script:
  - `bash security/sbom/generate-sbom.sh`

Scope includes source files and `pip` dependencies pinned in `data/pipelines/requirements.txt`.