# Policy -> Rules -> Tags -> Owners

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
