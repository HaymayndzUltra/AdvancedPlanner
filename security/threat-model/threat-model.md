## Threat Model — Data Pipelines (STRIDE + LINDDUN)

Scope
- Data ETL tool at `data/pipelines/pipeline.py` that reads CSV inputs, applies privacy controls, validates against YAML schemas in `docs/data/schemas/*`, writes sanitized outputs to `data/pipelines/out/warehouse/*.csv`, and emits lineage metadata to `data/pipelines/out/lineage/*.json`.
- Environments: local dev and CI only (no production infra in this repo). Assumes artifacts may contain sensitive test data that mimics real PII.

System Overview
- Inputs: CSV files (`users.csv`, `session_events.csv`, `transactions.csv`).
- Processing: privacy transformations (email hashing, IP anonymization, card last4 tokenization), schema validation, lineage JSON emission.
- Outputs: sanitized CSVs, validation reports, lineage records.
- Trust Boundaries: file system boundaries (input vs. output), CI runner environment, repository secrets store (must remain empty in this repo).

Data Classification
- Users: email, name, phone (PII).
- Session events: IP address (personal data, potential location/identity inference).
- Transactions: card last4 (payment metadata, not PAN but still sensitive); tokens generated via SHA-256 truncation.

Assumptions
- No plaintext secrets stored in repo or artifacts.
- Privacy controls in `apply_privacy_controls` remain enabled and are not bypassed.
- Dependency versions are pinned (`requirements.txt`) and audited in CI.

STRIDE Analysis (key threats & mitigations)
- Spoofing: forged inputs masquerading as valid CSVs.
  - Mitigations: strict schema validation (`validate_records`), fail-fast on errors, CI-only controlled inputs.
- Tampering: alteration of outputs or lineage.
  - Mitigations: write-only generation per run, distinct output directories, CI artifacts with checksums; future: signed artifacts.
- Repudiation: lack of traceability for transformations.
  - Mitigations: lineage JSON with timestamp, dataset, source/target paths, counts; CI audit trail retained under `compliance/evidence/`.
- Information Disclosure: leakage of PII from inputs.
  - Mitigations: privacy controls for emails, phones, IPs, last4 tokens; validation report redacts raw fields; secret scanning in CI.
- Denial of Service: large or malformed CSVs.
  - Mitigations: validation step; consider row count/size limits in future.
- Elevation of Privilege: executing unexpected code paths.
  - Mitigations: no dynamic eval; Semgrep gates block `eval/exec`, dangerous subprocess usage.

LINDDUN (privacy threats)
- Linkability/Identifiability: re-identification risk via stable tokens.
  - Mitigations: SHA-256 truncation with domain-specific prefixes; avoid storing raw identifiers.
- Non-repudiation: ensure transformations are accountable.
  - Mitigations: lineage records and CI logs.
- Detectability/Disclosure: presence of individuals detectable in outputs.
  - Mitigations: anonymization and masking; allow configurable suppression for rare values in future.
- Unawareness/Non-compliance: contributors unaware of privacy posture.
  - Mitigations: `security/secure-coding-standards.md`; CI gates; evidence folder.

Abuse Cases (see `abuse-cases.md` for QA integration)
- CSV with embedded secrets or tokens.
- Overly permissive file paths (path traversal in `--input`).
- Non-UTF8 content leading to partial reads and leakage.
- Adversarial IP formats to bypass anonymization.

Security Requirements
- Enforce CI gates: Semgrep (SAST), Gitleaks (secrets), dependency audit, SBOM generation and publishing as artifact.
- Zero critical vulnerabilities prior to merge to `integration`.
- Policy-as-code rules pass; any P0/P1 findings block merges.

Planned Improvements
- Artifact signing/attestation (SLSA provenance) on release jobs.
- Configurable privacy thresholds (k-anonymity-like suppression for rare categories).
- DAST scope once any networked service appears in the repo.

