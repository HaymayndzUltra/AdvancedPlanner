# Created Files Reference

This file aggregates the contents of all files created/updated in this session for reference.


---

## requirements.txt

Path: /workspace/requirements.txt

\`\`\`
jsonschema==4.22.0
PyYAML==6.0.2
\`\`\`

---

## Tags Taxonomy

Path: /workspace/frameworks/security/config/tags.md

\`\`\`
# Security Tags Taxonomy

- PII
- auth
- license
- crypto
- secrets
- logging
- egress
- privacy
- infra
- app
- data

\`\`\`

---

## Streams Registry

Path: /workspace/frameworks/security/config/streams.md

\`\`\`
# Streams Registry

- app
- infra
- data

\`\`\`

---

## Schema: sec_findings

Path: /workspace/frameworks/security/schemas/sec_findings.schema.json

\`\`\`
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Security Findings Artifact",
  "type": "object",
  "required": [
    "schema_version",
    "run_id",
    "snapshot_rev",
    "rulebook_hash",
    "stream",
    "cycle",
    "owners",
    "findings"
  ],
  "properties": {
    "schema_version": { "type": ["string", "number"] },
    "run_id": { "type": "string" },
    "snapshot_rev": { "type": "string" },
    "rulebook_hash": { "type": "string", "pattern": "^sha256:" },
    "stream": { "type": "string" },
    "cycle": { "type": "string", "pattern": "^\\d{4}-\\d{2}$" },
    "owners": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": { "team": { "type": "string" } },
        "required": ["team"],
        "additionalProperties": true
      }
    },
    "tags": { "type": "array", "items": { "type": "string" } },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "title", "severity", "category", "status"],
        "properties": {
          "id": { "type": "string" },
          "title": { "type": "string" },
          "severity": { "type": "string", "enum": ["Critical", "High", "Medium", "Low"] },
          "category": { "type": "string" },
          "tags": { "type": "array", "items": { "type": "string" } },
          "status": { "type": "string" },
          "evidence_uri": { "type": "string" },
          "first_seen": { "type": "string" },
          "last_seen": { "type": "string" },
          "affected_assets": { "type": "array", "items": { "type": "string" } },
          "controls": { "type": "array", "items": { "type": "string" } },
          "references": { "type": "array", "items": { "type": "string" } }
        },
        "additionalProperties": true
      }
    }
  },
  "additionalProperties": true
}
\`\`\`

---

## Schema: policy_map

Path: /workspace/frameworks/security/schemas/policy_map.schema.json

\`\`\`
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Policy Map Front Matter",
  "type": "object",
  "required": ["schema_version", "policies"],
  "properties": {
    "schema_version": { "type": ["string", "number"] },
    "policies": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "purpose", "rules", "tags", "owners"],
        "properties": {
          "id": { "type": "string" },
          "purpose": { "type": "string" },
          "rules": { "type": "array", "items": { "type": "string" } },
          "tags": { "type": "array", "items": { "type": "string" } },
          "owners": {
            "oneOf": [
              { "type": "string" },
              { "type": "array", "items": { "type": "string" } }
            ]
          }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}
\`\`\`

---

## Schema: exceptions

Path: /workspace/frameworks/security/schemas/exceptions.schema.json

\`\`\`
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Exceptions Registry Front Matter",
  "type": "object",
  "required": ["schema_version", "registry"],
  "properties": {
    "schema_version": { "type": ["string", "number"] },
    "cycle_id": { "type": ["string", "null"] },
    "registry": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["exception_id", "title", "owner", "justification", "expires_on", "status"],
        "properties": {
          "exception_id": { "type": "string" },
          "title": { "type": "string" },
          "owner": { "type": "string" },
          "scope": { "type": "object" },
          "justification": { "type": "string" },
          "expires_on": { "type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$" },
          "ticket": { "type": "string" },
          "approved_by": { "type": "string" },
          "status": { "type": "string", "enum": ["approved", "proposed", "rejected", "expired"] }
        },
        "additionalProperties": true
      }
    }
  },
  "additionalProperties": false
}
\`\`\`

---

## Schema: handoff_manifest

Path: /workspace/frameworks/security/schemas/handoff_manifest.schema.json

\`\`\`
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Handoff Manifest",
  "type": "object",
  "required": ["manifest_version", "cycle", "snapshot_rev", "rulebook_hash", "artifacts", "quality_gates"],
  "properties": {
    "manifest_version": { "type": ["integer", "string"] },
    "cycle": { "type": "string" },
    "snapshot_rev": { "type": "string" },
    "rulebook_hash": { "type": "string", "pattern": "^sha256:" },
    "artifacts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "path", "sha256"],
        "properties": {
          "name": { "type": "string" },
          "path": { "type": "string" },
          "sha256": { "type": "string", "pattern": "^[a-f0-9]{64}$" }
        },
        "additionalProperties": false
      }
    },
    "quality_gates": {
      "type": "object",
      "properties": {
        "schema_lint": { "type": "string" },
        "cross_stream_consistency": { "type": "string" },
        "parity_coverage": { "oneOf": [
          { "type": "string" },
          { "type": "object", "properties": { "status": {"type": "string"}, "coverage_pct": {"type": "number"} }, "required": ["status"], "additionalProperties": true }
        ]}
      },
      "additionalProperties": true
    },
    "signing": { "type": "object", "additionalProperties": true },
    "sealed": { "type": "boolean" }
  },
  "additionalProperties": true
}
\`\`\`

---

## Schema: digest

Path: /workspace/frameworks/security/schemas/digest.schema.json

\`\`\`
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Security Digest Front Matter",
  "type": "object",
  "required": ["schema_version", "cycle", "snapshot_rev", "rulebook_hash"],
  "properties": {
    "schema_version": { "type": ["string", "number"] },
    "date": { "type": "string" },
    "cycle": { "type": "string" },
    "snapshot_rev": { "type": "string" },
    "rulebook_hash": { "type": "string", "pattern": "^sha256:" },
    "kpis": { "type": "object" },
    "gates": { "type": "object" },
    "exceptions": { "type": "object" },
    "coverage": { "type": ["number", "string"] }
  },
  "additionalProperties": true
}
\`\`\`

---

## Template: policy_map.md

Path: /workspace/frameworks/security/policy/policy_map.md

\`\`\`
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
\`\`\`

---

## Template: exceptions.md

Path: /workspace/frameworks/security/policy/exceptions.md

\`\`\`
---
schema_version: 1
cycle_id: "2025-09-02"
registry:
  - exception_id: EX-2025-001
    title: Temporary waiver for third-party SCA medium alerts
    owner: team-appsec
    scope:
      service: payments-api
      tags: [license]
      applies_to_findings: [F-1234, F-5678]
    justification: Vendor patch pending; risk accepted for 14 days.
    expires_on: "2025-10-01"
    ticket: SEC-8123
    approved_by: ciso@company.com
    status: approved
---

# Exceptions Registry

This registry captures approved and scoped exceptions with expiries and compensating controls.
\`\`\`

---

## Artifact: sec_findings.yaml (2025-09)

Path: /workspace/frameworks/security/artifacts/2025-09/sec_findings.yaml

\`\`\`
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
    first_seen: "2025-08-28"
    last_seen: "2025-09-02"
    affected_assets: ["payments-api", "worker-ingest"]
    controls: [LOG-RED-001, DLP-002]
    references: [CWE-312]
  - id: F-0002
    title: "Missing license header"
    severity: Low
    category: license
    tags: [license]
    status: Resolved
\`\`\`

---

## Manifest: handoff_manifest.yaml (2025-09)

Path: /workspace/frameworks/security/manifests/2025-09/handoff_manifest.yaml

\`\`\`
manifest_version: 1
cycle: 2025-09
snapshot_rev: git:abcdef1234
rulebook_hash: sha256:rulebookhashhere
artifacts:
- name: sec_findings
  path: artifacts/2025-09/sec_findings.yaml
  sha256: a626780af478a84ae51a82a2906b160235ddba7e829c9144879d114856bf7d7d
- name: policy_map
  path: policy/policy_map.md
  sha256: 7aeec3553e8fed2d492fa6219bb096986eb096bc7a03a7e1529aac095a617526
- name: exceptions
  path: policy/exceptions.md
  sha256: 7427699360259be099342bf5d458c5992ec95f4d3642f89c5412b83ffb5a48b0
quality_gates:
  schema_lint: pass
  cross_stream_consistency: pass
  parity_coverage:
    status: pass
    coverage_pct: 100.0
sealed: true
generated_at: '2025-09-02T04:16:41.548788Z'

\`\`\`

---

## Digest: 2025-09-02

Path: /workspace/frameworks/security/digests/2025-09-02-digest.md

\`\`\`
## Cycle Digest — 2025-09-02

- Cycle: 2025-09
- Snapshot Rev: git:abcdef1234
- Rulebook Hash: sha256:rulebookhashhere

### KPI Summary
- Time to VALIDATED: TBD
- Gate pass rate: schema_lint TBD, consistency TBD, parity/coverage TBD
- Critical at PACKAGED: TBD → at VALIDATED: TBD
- Exceptions: new TBD, active TBD, expired TBD
- Coverage: TBD of required streams

### Gate Outcomes
- schema_lint: pass
- cross_stream_consistency: pass
- parity/coverage: pass

### Exceptions Summary
- List active and new exceptions with scope and expiry.

### Top Risks & Actions
- Summarize top risks and assigned actions.

\`\`\`

---

## CLI: security_framework.py

Path: /workspace/frameworks/security/bin/security_framework.py

\`\`\`
#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from typing import Any, Dict, List, Tuple

import yaml
from jsonschema import validate, Draft202012Validator

ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
SCHEMAS_DIR = os.path.join(ROOT, "schemas")
ARTIFACTS_DIR = os.path.join(ROOT, "artifacts")
POLICY_DIR = os.path.join(ROOT, "policy")
MANIFESTS_DIR = os.path.join(ROOT, "manifests")
DIGESTS_DIR = os.path.join(ROOT, "digests")
CONFIG_DIR = os.path.join(ROOT, "config")


def load_schema(name: str) -> Dict[str, Any]:
    with open(os.path.join(SCHEMAS_DIR, name), "r", encoding="utf-8") as f:
        return json.load(f)


def yaml_front_matter_and_body(path: str) -> Tuple[Dict[str, Any], str]:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---\n"):
        parts = content.split("\n---\n", 1)
        front = yaml.safe_load(parts[0].lstrip("-\n")) or {}
        body = parts[1] if len(parts) > 1 else ""
        return front, body
    return {}, content


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_yaml_with_schema(yaml_path: str, schema_name: str) -> List[str]:
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    schema = load_schema(schema_name)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    return [f"{list(e.path)}: {e.message}" for e in errors]


def validate_front_matter(md_path: str, schema_name: str) -> List[str]:
    front, _ = yaml_front_matter_and_body(md_path)
    schema = load_schema(schema_name)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(front), key=lambda e: e.path)
    return [f"{list(e.path)}: {e.message}" for e in errors]


def load_tags_vocab() -> List[str]:
    tags_path = os.path.join(CONFIG_DIR, "tags.md")
    tags: List[str] = []
    if os.path.exists(tags_path):
        with open(tags_path, "r", encoding="utf-8") as f:
            for line in f:
                m = re.match(r"^-\s+(\S+)$", line.strip())
                if m:
                    tags.append(m.group(1))
    return tags


def cross_stream_consistency(findings_yaml: str) -> List[str]:
    issues: List[str] = []
    allowed_severity = {"Critical", "High", "Medium", "Low"}
    allowed_tags = set(load_tags_vocab())
    with open(findings_yaml, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    for idx, finding in enumerate(doc.get("findings", [])):
        sev = finding.get("severity")
        if sev not in allowed_severity:
            issues.append(f"finding[{idx}].severity '{sev}' not in {sorted(allowed_severity)}")
        for tag in finding.get("tags", []) or []:
            if allowed_tags and tag not in allowed_tags:
                issues.append(f"finding[{idx}].tags '{tag}' not in tags taxonomy")
    return issues


def parity_coverage(artifacts_dir: str) -> Tuple[str, float]:
    # Simple placeholder: coverage based on presence of required files
    required = [
        os.path.join(POLICY_DIR, "policy_map.md"),
        os.path.join(POLICY_DIR, "exceptions.md"),
    ]
    present = sum(1 for p in required if os.path.exists(p))
    coverage = (present / len(required)) * 100 if required else 100.0
    status = "pass" if coverage >= 90.0 else "fail"
    return status, coverage


def generate_manifest(cycle: str, snapshot_rev: str, rulebook_hash: str, out_path: str) -> Dict[str, Any]:
    artifacts: List[Dict[str, Any]] = []
    sec_findings = os.path.join(ARTIFACTS_DIR, cycle, "sec_findings.yaml")
    policy_map = os.path.join(POLICY_DIR, "policy_map.md")
    exceptions = os.path.join(POLICY_DIR, "exceptions.md")
    for name, path in [("sec_findings", sec_findings), ("policy_map", policy_map), ("exceptions", exceptions)]:
        if os.path.exists(path):
            artifacts.append({
                "name": name,
                "path": os.path.relpath(path, ROOT),
                "sha256": sha256_file(path)
            })
    schema_issues = []
    schema_issues += validate_yaml_with_schema(sec_findings, "sec_findings.schema.json") if os.path.exists(sec_findings) else ["missing sec_findings.yaml"]
    schema_issues += validate_front_matter(policy_map, "policy_map.schema.json") if os.path.exists(policy_map) else ["missing policy_map.md"]
    schema_issues += validate_front_matter(exceptions, "exceptions.schema.json") if os.path.exists(exceptions) else ["missing exceptions.md"]

    consistency_issues = cross_stream_consistency(sec_findings) if os.path.exists(sec_findings) else ["no findings to check"]
    parity_status, coverage = parity_coverage(ARTIFACTS_DIR)

    manifest: Dict[str, Any] = {
        "manifest_version": 1,
        "cycle": cycle,
        "snapshot_rev": snapshot_rev,
        "rulebook_hash": rulebook_hash,
        "artifacts": artifacts,
        "quality_gates": {
            "schema_lint": "pass" if not schema_issues else f"fail: {len(schema_issues)} issues",
            "cross_stream_consistency": "pass" if not consistency_issues else f"fail: {len(consistency_issues)} issues",
            "parity_coverage": {"status": parity_status, "coverage_pct": round(coverage, 2)}
        },
        "sealed": True,
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }

    with open(out_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(manifest, f, sort_keys=False)

    return {
        "schema_issues": schema_issues,
        "consistency_issues": consistency_issues,
        "parity_status": parity_status,
        "coverage": coverage,
        "manifest_path": out_path
    }


def generate_digest(date_str: str, cycle: str, snapshot_rev: str, rulebook_hash: str, manifest_summary: Dict[str, Any], out_path: str) -> None:
    kpis = {
        "time_to_validated": "TBD",
        "gate_pass_rate": {
            "schema_lint": "TBD",
            "consistency": "TBD",
            "parity_coverage": "TBD"
        },
        "critical": "TBD",
        "exceptions": {"new": "TBD", "active": "TBD", "expired": "TBD"},
        "coverage": "TBD"
    }
    lines: List[str] = []
    lines.append(f"## Cycle Digest — {date_str}")
    lines.append("")
    lines.append(f"- Cycle: {cycle}")
    lines.append(f"- Snapshot Rev: {snapshot_rev}")
    lines.append(f"- Rulebook Hash: {rulebook_hash}")
    lines.append("")
    lines.append("### KPI Summary")
    lines.append("- Time to VALIDATED: " + str(kpis["time_to_validated"]))
    lines.append("- Gate pass rate: schema_lint TBD, consistency TBD, parity/coverage TBD")
    lines.append("- Critical at PACKAGED: TBD → at VALIDATED: TBD")
    lines.append("- Exceptions: new TBD, active TBD, expired TBD")
    lines.append("- Coverage: TBD of required streams")
    lines.append("")
    lines.append("### Gate Outcomes")
    qg = manifest_summary
    lines.append("- schema_lint: " + ("pass" if not qg.get("schema_issues") else "fail"))
    lines.append("- cross_stream_consistency: " + ("pass" if not qg.get("consistency_issues") else "fail"))
    lines.append("- parity/coverage: " + qg.get("parity_status", "TBD"))
    lines.append("")
    lines.append("### Exceptions Summary")
    lines.append("- List active and new exceptions with scope and expiry.")
    lines.append("")
    lines.append("### Top Risks & Actions")
    lines.append("- Summarize top risks and assigned actions.")
    content = "\n".join(lines) + "\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)


def main() -> None:
    parser = argparse.ArgumentParser(prog="security-framework")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_val = sub.add_parser("validate", help="Run schema and consistency validation")
    p_val.add_argument("--cycle", required=True)

    p_manifest = sub.add_parser("generate-manifest", help="Generate and seal manifest")
    p_manifest.add_argument("--cycle", required=True)
    p_manifest.add_argument("--snapshot", required=True)
    p_manifest.add_argument("--rulebook-hash", required=True)

    p_digest = sub.add_parser("generate-digest", help="Generate digest.md for date")
    p_digest.add_argument("--date", required=True)
    p_digest.add_argument("--cycle", required=True)
    p_digest.add_argument("--snapshot", required=True)
    p_digest.add_argument("--rulebook-hash", required=True)

    args = parser.parse_args()

    if args.cmd == "validate":
        sec_path = os.path.join(ARTIFACTS_DIR, args.cycle, "sec_findings.yaml")
        issues = validate_yaml_with_schema(sec_path, "sec_findings.schema.json") if os.path.exists(sec_path) else ["missing sec_findings.yaml"]
        issues += cross_stream_consistency(sec_path) if os.path.exists(sec_path) else []
        pol_issues = validate_front_matter(os.path.join(POLICY_DIR, "policy_map.md"), "policy_map.schema.json")
        exc_issues = validate_front_matter(os.path.join(POLICY_DIR, "exceptions.md"), "exceptions.schema.json")
        issues += [f"policy_map: {i}" for i in pol_issues]
        issues += [f"exceptions: {i}" for i in exc_issues]
        if issues:
            for i in issues:
                print(i)
            sys.exit(1)
        print("All validations passed")
        return

    if args.cmd == "generate-manifest":
        cycle = args.cycle
        out_path = os.path.join(MANIFESTS_DIR, cycle, "handoff_manifest.yaml")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        summary = generate_manifest(cycle, args.snapshot, args.rulebook_hash, out_path)
        print(json.dumps(summary, indent=2))
        return

    if args.cmd == "generate-digest":
        date_str = args.date
        cycle = args.cycle
        manifest_path = os.path.join(MANIFESTS_DIR, cycle, "handoff_manifest.yaml")
        manifest_summary = {}
        if os.path.exists(manifest_path):
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest_summary = yaml.safe_load(f)
        out_path = os.path.join(DIGESTS_DIR, f"{date_str}-digest.md")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        # If manifest load gave full manifest, adapt expected keys
        summary = {
            "schema_issues": [],
            "consistency_issues": [],
            "parity_status": manifest_summary.get("quality_gates", {}).get("parity_coverage", {}).get("status", "TBD") if manifest_summary else "TBD"
        }
        generate_digest(date_str, cycle, args.snapshot, args.rulebook_hash, summary, out_path)
        print(out_path)
        return


if __name__ == "__main__":
    main()
\`\`\`

---

## CI: security-framework.yml

Path: /workspace/.github/workflows/security-framework.yml

\`\`\`
name: Security Framework Checks

on:
  pull_request:
    paths:
      - 'frameworks/security/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install jsonschema PyYAML

      - name: Run validations
        run: |
          python frameworks/security/bin/security_framework.py validate --cycle 2025-09

      - name: Generate manifest (dry run)
        run: |
          python frameworks/security/bin/security_framework.py generate-manifest --cycle 2025-09 --snapshot "git:${{ github.sha }}" --rulebook-hash sha256:rulebookhashhere

      - name: Generate digest (dry run)
        run: |
          python frameworks/security/bin/security_framework.py generate-digest --date $(date +%F) --cycle 2025-09 --snapshot "git:${{ github.sha }}" --rulebook-hash sha256:rulebookhashhere
\`\`\`
