## Secure Coding Standards (Python + Repo-wide)

General
- Do not commit secrets. Use environment variables or secret managers. CI enforces Gitleaks.
- Pin dependencies and audit them via CI. Use `data/pipelines/requirements.txt`.
- Fail closed: validation errors must stop the pipeline and emit a report.
- Avoid dynamic code execution (`eval`, `exec`). Prohibited by Semgrep rules.
- Limit I/O to the repository workspace; sanitize CLI inputs; avoid path traversal.
- Log minimally; never log PII. Keep lineage metadata non-sensitive.

Python-Specific
- Prefer explicit typing for public functions; keep functions small and testable.
- Validate external inputs early; precompile regex where performance matters.
- Use safe hashing (`hashlib.sha256`) with normalization when tokenizing data.
- Handle encodings explicitly (`encoding="utf-8"`).
- Use `with` statements for file I/O and ensure directories are created with least privileges.

Dependency Hygiene
- Weekly Dependabot updates for `pip` and GitHub Actions.
- CI runs `pip-audit` on `requirements.txt` and fails on known criticals.
- Produce and publish SBOM artifacts for auditability.

Secrets Handling
- Never store API keys, tokens, or credentials in repo, code, or samples.
- If a secret is leaked, rotate immediately and add a postmortem in `compliance/evidence/audit-trail.md`.

Policy-as-Code
- Semgrep config under `security/policies/semgrep.yml` and run in CI.
- Gitleaks config under `security/policies/gitleaks.toml` and run in CI.

