---
schema_version: 1
policies:
  - id: LOG-RED-001
    purpose: Redact PII in logs
    rules: [rule:regex_pii_redaction, rule:log_sink_blocklist]
    tags: [PII, logging]
    owners: security-observability@company
  - id: DLP-002
    purpose: Prevent sensitive exfiltration
    rules: [rule:egress_dlp_scan]
    tags: [PII, egress]
    owners: data-security@company
---

# Policy  Rules  Tags  Owners

- LOG-RED-001
  - Purpose: Redact PII in logs
  - Rules: [rule:regex_pii_redaction, rule:log_sink_blocklist]
  - Tags: [PII, logging]
  - Owners: security-observability@company

- DLP-002
  - Purpose: Prevent sensitive exfiltration
  - Rules: [rule:egress_dlp_scan]
  - Tags: [PII, egress]
  - Owners: data-security@company