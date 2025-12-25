# Compliance Evidence

Structure
- scans/
  - secrets/ (Gitleaks JSON reports)
  - sast/ (Semgrep SARIF)
  - dependencies/ (pip-audit JSON)
- audit-trail.md (manual notes of key decisions, risk acceptances, rotations)

CI publishes artifacts into these folders. Keep human-readable summaries in `audit-trail.md`.