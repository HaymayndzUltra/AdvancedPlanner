## Abuse Cases and QA Collaboration

How to use: Convert these into negative tests and add them to the QA plan. Security CI gates will run alongside QA to prevent regressions.

File Inputs
- Malicious CSV with formula injection (=CMD|'/C calc'!A0) in cells.
  - Expectation: written outputs should not evaluate or preserve formulas; treat content as data only.
- Path traversal in `--input` (e.g., `../../etc/passwd`).
  - Expectation: CLI rejects directories outside the repo workspace or fails closed.
- Non-UTF8 encoded CSV.
  - Expectation: deterministic failure with clear validation error, no partial outputs.

Privacy Controls
- Emails with Unicode homographs to bypass hashing normalization.
  - Expectation: `.lower().strip()` normalization applied prior to hashing.
- IP strings mixing IPv4-mapped IPv6 formats.
  - Expectation: anonymizer returns network address without leaking host bits.
- Transactions with random last4 that collide.
  - Expectation: tokens may collide but raw last4 are removed; validate absence of plaintext last4.

Operational
- Extremely large CSV causing memory pressure.
  - Expectation: validation fails fast or process limits documented; future: streaming reader.
- Attempted secret commit added to samples.
  - Expectation: Gitleaks blocks PR and evidence stored under `compliance/evidence/scans/secrets/`.

Test Hooks
- Place adversarial fixtures under `data/pipelines/samples/abuse/` (do not include secrets).
- Add CI job to run the pipeline on those fixtures and assert failure where expected.

