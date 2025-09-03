# Security & Compliance Framework — Reference Bundle (2025-09-02)

This document aggregates the contents of all created artifacts for easy reference.

## frameworks/security/artifacts/2025-09/sec_findings.yaml
    schema_version: 1.0
    run_id: 2025-09-02.01
    snapshot_rev: "git:abcdef1234"
    rulebook_hash: "sha256:rulebookhashhere"
    stream: "payments-service"
    cycle: "2025-09"
    owners:
      - team: "payments-sec"
      - team: "app-platform"
    tags: [PII, auth]
    findings:
      - id: F-0001
        title: "PII in logs"
        severity: Critical
        category: data_exposure
        tags: [PII, logging]
        status: Open
        evidence_uri: s3://bucket/logs/sample
        first_seen: 2025-08-28
        last_seen: 2025-09-02
        affected_assets: ["payments-api", "worker-ingest"]
        controls: [LOG-RED-001, DLP-002]
        references: [CWE-312]
      - id: F-0002
        title: "Missing license header"
        severity: Low
        category: license
        tags: [license]
        status: Resolved


## frameworks/security/policy/policy_map.md
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


## frameworks/security/policy/exceptions.md
    # Exceptions Registry
    
    - EX-001
      - Scope: payments-service/log-sanitizer
      - Related Findings: [F-0001]
      - Justification: Redaction rollout in progress
      - Risk: Medium
      - Temporary Compensating Controls: log sampling + alerting
      - Approved By: CISO (sig: sha256:...)
      - Requested: 2025-09-02, Expires: 2025-10-15


## frameworks/security/manifests/2025-09/handoff_manifest.yaml
    manifest_version: 1
    cycle: "2025-09"
    snapshot_rev: "git:abcdef1234"
    rulebook_hash: "sha256:rulebookhashhere"
    artifacts:
      - name: sec_findings
        path: frameworks/security/artifacts/2025-09/sec_findings.yaml
        sha256: "b824dccf59940b051a9eddff2c533d89dd551172dc913e8eb38066a66f606f85"
      - name: policy_map
        path: frameworks/security/policy/policy_map.md
        sha256: "1628f9540458ef0d702a5dbe79d3ea47732b6e4d47a8ca8ef01949786e502699"
      - name: exceptions
        path: frameworks/security/policy/exceptions.md
        sha256: "ae09637711fdfabd4c49152de3e3d9c5312d6db5a39225f1d4f5a9e701f52a72"
    quality_gates:
      schema_lint: TBD
      cross_stream_consistency: TBD
      parity_coverage: TBD
    signing:
      signed_by: TBD
      signature: TBD
      signed_at: TBD


## frameworks/security/digests/2025-09-02-digest.md
    ## Cycle Digest — 2025-09-02
    
    - Cycle: 2025-09
    - Snapshot Rev: git:abcdef1234
    - Rulebook Hash: sha256:rulebookhashhere
    
    ### KPI Summary
    - Time to VALIDATED: TBD
    - Gate pass rate: schema_lint TBD, consistency TBD, parity/coverage TBD
    - Critical at PACKAGED: TBD -> at VALIDATED: TBD
    - Exceptions: new TBD, active TBD, expired TBD
    - Coverage: TBD of required streams
    
    ### Gate Outcomes
    - schema_lint: TBD
    - cross_stream_consistency: TBD
    - parity/coverage: TBD
    
    ### Exceptions Summary
    - List active and new exceptions with scope and expiry.
    
    ### Top Risks & Actions
    - Summarize top risks and assigned actions.


## frameworks/security/schemas/sec_findings.schema.json
    {
      "$schema": "https://json-schema.org/draft/2020-12/schema",
      "$id": "https://company.example/schemas/sec_findings.schema.json",
      "title": "Security Findings",
      "type": "object",
      "required": [
        "schema_version",
        "run_id",
        "snapshot_rev",
        "rulebook_hash",
        "stream",
        "cycle",
        "owners",
        "tags",
        "findings"
      ],
      "properties": {
        "schema_version": { "type": ["string", "number"] },
        "run_id": { "type": "string" },
        "snapshot_rev": { "type": "string" },
        "rulebook_hash": { "type": "string" },
        "stream": { "type": "string" },
        "cycle": { "type": "string" },
        "owners": {
          "type": "array",
          "items": { "type": "object", "properties": { "team": { "type": "string" } }, "required": ["team"] }
        },
        "tags": { "type": "array", "items": { "type": "string" } },
        "findings": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["id", "title", "severity", "status"],
            "properties": {
              "id": { "type": "string" },
              "title": { "type": "string" },
              "severity": { "type": "string", "enum": ["Critical", "High", "Medium", "Low"] },
              "category": { "type": "string" },
              "tags": { "type": "array", "items": { "type": "string" } },
              "status": { "type": "string" }
            }
          }
        }
      }
    }


## frameworks/security/schemas/handoff_manifest.schema.json
    {
      "$schema": "https://json-schema.org/draft/2020-12/schema",
      "$id": "https://company.example/schemas/handoff_manifest.schema.json",
      "title": "Handoff Manifest",
      "type": "object",
      "required": ["manifest_version", "cycle", "snapshot_rev", "rulebook_hash", "artifacts", "quality_gates"],
      "properties": {
        "manifest_version": { "type": ["integer", "string"] },
        "cycle": { "type": "string" },
        "snapshot_rev": { "type": "string" },
        "rulebook_hash": { "type": "string" },
        "artifacts": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["name", "path", "sha256"],
            "properties": {
              "name": { "type": "string" },
              "path": { "type": "string" },
              "sha256": { "type": "string" }
            }
          }
        },
        "quality_gates": {
          "type": "object",
          "properties": {
            "schema_lint": {},
            "cross_stream_consistency": {},
            "parity_coverage": {}
          }
        },
        "signing": {
          "type": "object",
          "properties": {
            "signed_by": { "type": ["string", "null"] },
            "signature": { "type": ["string", "null"] },
            "signed_at": { "type": ["string", "null"] }
          }
        }
      }
    }
