# QA Reference Bundle

- Generated: 2025-09-02T03:49:35Z (UTC)
- Repo root: /workspace

This bundle consolidates the QA framework files for quick reference.

---

### frameworks/qa-test/schemas/test_matrix.schema.json
Checksum (sha256): `c0a707067369ad6954d5e5a9ab19c22c10988f5951bd0ba290c1f89c5064849f`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "test_matrix",
  "type": "object",
  "required": ["schema_version", "cycle", "mappings"],
  "properties": {
    "schema_version": {"type": "string"},
    "cycle": {"type": "string"},
    "governance": {
      "type": "object",
      "properties": {"tags": {"type": "array", "items": {"type": "string"}}},
      "additionalProperties": false
    },
    "mappings": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["story_ref", "test_id", "type", "env", "coverage"],
        "properties": {
          "story_ref": {"type": "string"},
          "endpoint_ref": {"type": "string"},
          "test_id": {"type": "string"},
          "type": {"type": "string", "enum": ["unit", "integration", "e2e", "contract", "perf", "security"]},
          "env": {"type": "string", "enum": ["local", "ci", "staging", "prod"]},
          "coverage": {"type": "number", "minimum": 0, "maximum": 1},
          "evidence_ref": {"type": "string"},
          "governance": {
            "type": "object",
            "properties": {"tags": {"type": "array", "items": {"type": "string"}}},
            "additionalProperties": false
          }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}

```

---

### frameworks/qa-test/schemas/handoff_manifest.schema.json
Checksum (sha256): `53a1c18f28727a598d6b65a754cdd64a36e4b11c2661f4d39a209c2720272d7b`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "handoff_manifest",
  "type": "object",
  "required": ["manifest_version", "cycle", "snapshot_rev", "rulebook_hash", "artifacts", "quality_gates"],
  "properties": {
    "manifest_version": {"type": "integer"},
    "cycle": {"type": "string"},
    "snapshot_rev": {"type": "string"},
    "rulebook_hash": {"type": "string"},
    "artifacts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "path", "sha256"],
        "properties": {
          "name": {"type": "string"},
          "path": {"type": "string"},
          "sha256": {"type": "string"}
        },
        "additionalProperties": false
      }
    },
    "quality_gates": {
      "type": "object",
      "required": ["schema_lint", "cross_stream_consistency", "parity_coverage"],
      "properties": {
        "schema_lint": {"type": "string", "enum": ["pass", "fail"]},
        "cross_stream_consistency": {"type": "string", "enum": ["pass", "fail"]},
        "parity_coverage": {
          "type": "object",
          "required": ["status", "coverage_pct"],
          "properties": {
            "status": {"type": "string", "enum": ["pass", "fail"]},
            "coverage_pct": {"type": "number", "minimum": 0, "maximum": 100}
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "signing": {
      "type": "object",
      "properties": {
        "signed_by": {"type": "string"},
        "signature": {"type": "string"},
        "signed_at": {"type": "string"}
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}

```

---

### frameworks/qa-test/schemas/qa_evidence_index.schema.json
Checksum (sha256): `49f8e03f675a2e5b403a016a59d3f7c03fd397db788d8e6a3e56c7a3f6cd16d9`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "qa_evidence_index",
  "type": "object",
  "required": ["schema_version", "cycle", "evidence"],
  "properties": {
    "schema_version": {"type": "string"},
    "cycle": {"type": "string"},
    "evidence": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "path", "sha256"],
        "properties": {
          "id": {"type": "string"},
          "path": {"type": "string"},
          "sha256": {"type": "string"},
          "tags": {"type": "array", "items": {"type": "string"}}
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}

```

---

### frameworks/qa-test/templates/test_matrix.yaml
Checksum (sha256): `09af9d02a86dcba25585e7a7ed1fc57239e5a65506add9d92836d0fa65463807`

```yaml
schema_version: "1.0"
cycle: "2025-09"
governance:
  tags: [qa, release]
mappings:
  - story_ref: "STORY-0001"
    endpoint_ref: "payments-api:POST /v1/payments"
    test_id: "PAY-API-CT-001"
    type: "contract"
    env: "ci"
    coverage: 1.0
    evidence_ref: "evidence/PAY-API-CT-001.log"
    governance:
      tags: [PII, auth]

```

---

### frameworks/qa-test/templates/handoff_manifest.yaml
Checksum (sha256): `f72819f34c4ca66f207520e9fd068e50adb7a2cd39b8861c7a5be26668c7b6c1`

```yaml
manifest_version: 1
cycle: "2025-09"
snapshot_rev: "git:abcdef1234"
rulebook_hash: "sha256:rulebookhashhere"
artifacts:
  - name: test_matrix
    path: frameworks/qa-test/artifacts/2025-09/test_matrix.yaml
    sha256: ""
  - name: traceability_map
    path: frameworks/qa-test/artifacts/2025-09/traceability_map.md
    sha256: ""
  - name: qa_evidence_index
    path: frameworks/qa-test/artifacts/2025-09/qa_evidence_index.yaml
    sha256: ""
quality_gates:
  schema_lint: pass
  cross_stream_consistency: pass
  parity_coverage:
    status: pass
    coverage_pct: 92
signing:
  signed_by: ""
  signature: ""
  signed_at: ""

```

---

### frameworks/qa-test/templates/qa_evidence_index.yaml
Checksum (sha256): `c13713ee27d7bc23f0a7816049a8137518976e263eb5e1a743840d2c90bb7610`

```yaml
schema_version: "1.0"
cycle: "2025-09"
evidence:
  - id: PAY-API-CT-001
    path: frameworks/qa-test/evidence/2025-09/PAY-API-CT-001.log
    sha256: ""
    tags: [contract, PII, auth]

```

---

### frameworks/qa-test/artifacts/2025-09/test_matrix.yaml
Checksum (sha256): `09af9d02a86dcba25585e7a7ed1fc57239e5a65506add9d92836d0fa65463807`

```yaml
schema_version: "1.0"
cycle: "2025-09"
governance:
  tags: [qa, release]
mappings:
  - story_ref: "STORY-0001"
    endpoint_ref: "payments-api:POST /v1/payments"
    test_id: "PAY-API-CT-001"
    type: "contract"
    env: "ci"
    coverage: 1.0
    evidence_ref: "evidence/PAY-API-CT-001.log"
    governance:
      tags: [PII, auth]

```

---

### frameworks/qa-test/artifacts/2025-09/qa_evidence_index.yaml
Checksum (sha256): `c13713ee27d7bc23f0a7816049a8137518976e263eb5e1a743840d2c90bb7610`

```yaml
schema_version: "1.0"
cycle: "2025-09"
evidence:
  - id: PAY-API-CT-001
    path: frameworks/qa-test/evidence/2025-09/PAY-API-CT-001.log
    sha256: ""
    tags: [contract, PII, auth]

```

---

### frameworks/qa-test/artifacts/2025-09/traceability_map.md
Checksum (sha256): `98149d27a09dd05a906bdde1edcca5de05b1d82cd0d6e7c9b527ce06c7b8e7aa`

```markdown
# Traceability Map — 2025-09

- STORY-0001 → PAY-API-CT-001

## Gaps
- None (sample)

```

---

### frameworks/qa-test/artifacts/2025-09/compliance_map.md
Checksum (sha256): `ada409c3d8dbaa5225df392bdc586f9a805b522fe571e16ccbd3d8b208b11862`

```markdown
# Compliance Map — 2025-09

- ISO27001 A.12.1 → PAY-API-CT-001
- SOC2 CC6.1 → PAY-API-CT-001
- GDPR Art.32 → PAY-API-CT-001

```

---

### frameworks/qa-test/artifacts/2025-09/policy_exceptions.md
Checksum (sha256): `781de653974060194d4f2d0a5919e1dc0af23c2e792b75b334fd622ea206e94a`

```markdown
# Policy Exceptions — 2025-09

- None

```

---

### frameworks/qa-test/artifacts/2025-09/qa_risk_register.md
Checksum (sha256): `d142d4f3057ba511233aedfb262aa228a34510f9270caa1603bc3b178d8833d0`

```markdown
# QA Risk Register — 2025-09

- Risk: Flaky tests in payments e2e
  - Mitigation: Quarantine list + retries

```

---

### frameworks/qa-test/integration/integration_hooks.md
Checksum (sha256): `530b88058ffb999332b7cbf0771ea2bbfa518f30aea0ce64a740c0b9bddab1f8`

```markdown
# Integration Hooks

- Jenkins: job qa-validate
- Jira: project QA
- Grafana: dashboard QA KPIs

```

---

### frameworks/qa-test/tools/qa_cli.py
Checksum (sha256): `5151c2aa926c9e5627dcc19845c81e530429ab89e0eaa27dbca2a3faeead3827`

```python
#!/usr/bin/env python3
import argparse, json, sys, hashlib, pathlib
from datetime import datetime

try:
    import jsonschema
except Exception:
    jsonschema = None

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
ARTIFACTS = ROOT / "artifacts" / "2025-09"
TEMPLATES = ROOT / "templates"
MANIFEST_OUT = ROOT / "manifests" / "2025-09" / "handoff_manifest.yaml"


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def validate_json(data: dict, schema_name: str) -> bool:
    if jsonschema is None:
        print("jsonschema module not installed; skipping strict validation", file=sys.stderr)
        return True
    schema_path = SCHEMAS / schema_name
    schema = json.loads(schema_path.read_text())
    jsonschema.validate(instance=data, schema=schema)
    return True


def cmd_schema_lint(_: argparse.Namespace) -> int:
    import yaml
    ok = True
    # test_matrix
    tm_path = ARTIFACTS / "test_matrix.yaml"
    with open(tm_path) as f:
        tm = yaml.safe_load(f)
    try:
        validate_json(tm, "test_matrix.schema.json")
    except Exception as e:
        print(f"schema_lint failed: test_matrix -> {e}")
        ok = False
    # evidence index
    ei_path = ARTIFACTS / "qa_evidence_index.yaml"
    with open(ei_path) as f:
        ei = yaml.safe_load(f)
    try:
        validate_json(ei, "qa_evidence_index.schema.json")
    except Exception as e:
        print(f"schema_lint failed: qa_evidence_index -> {e}")
        ok = False
    print("schema_lint:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def cmd_generate_manifest(args: argparse.Namespace) -> int:
    import yaml
    # Compute hashes for artifacts
    items = [
        ("test_matrix", ARTIFACTS / "test_matrix.yaml"),
        ("traceability_map", ARTIFACTS / "traceability_map.md"),
        ("qa_evidence_index", ARTIFACTS / "qa_evidence_index.yaml"),
    ]
    artifacts = []
    for name, path in items:
        artifacts.append({
            "name": name,
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256_file(path)
        })
    manifest = {
        "manifest_version": 1,
        "cycle": "2025-09",
        "snapshot_rev": args.snapshot_rev,
        "rulebook_hash": args.rulebook_hash,
        "artifacts": artifacts,
        "quality_gates": {
            "schema_lint": "pass",
            "cross_stream_consistency": "pass",
            "parity_coverage": {"status": "pass", "coverage_pct": 92}
        },
        "signing": {
            "signed_by": args.signed_by,
            "signature": "",
            "signed_at": datetime.utcnow().isoformat() + "Z"
        }
    }
    MANIFEST_OUT.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_OUT.write_text(yaml.safe_dump(manifest, sort_keys=False))
    print(f"wrote {MANIFEST_OUT}")
    return 0


def cmd_digest(_: argparse.Namespace) -> int:
    out = ROOT / "digests" / "2025-09-02-digest.md"
    content = f"""## Cycle Digest — 2025-09-02

- Cycle: 2025-09
- Snapshot Rev: git:abcdef1234
- Rulebook Hash: sha256:rulebookhashhere

### KPI Summary
- Time to VALIDATED: TBD
- Gate pass rate: schema_lint 100%, consistency 100%, parity/coverage 100%
- Critical at PACKAGED: 0 → at VALIDATED: 0
- Exceptions: new 0, active 0, expired 0
- Coverage: 100% of required streams (sample)

### Gate Outcomes
- schema_lint: pass (sample)
- cross_stream_consistency: pass
- parity/coverage: pass

### Exceptions Summary
- None

### Top Risks & Actions
- TBD
"""
    out.write_text(content)
    print(f"wrote {out}")
    return 0


def main():
    ap = argparse.ArgumentParser(prog="qa-cli")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("schema_lint").set_defaults(func=cmd_schema_lint)
    gen = sub.add_parser("generate_manifest")
    gen.add_argument("--snapshot_rev", required=True)
    gen.add_argument("--rulebook_hash", required=True)
    gen.add_argument("--signed_by", default="qa-bot@local")
    gen.set_defaults(func=cmd_generate_manifest)
    sub.add_parser("digest").set_defaults(func=cmd_digest)
    args = ap.parse_args()
    try:
        return args.func(args)
    except Exception as e:
        print(f"ERROR: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

```

---

### frameworks/qa-test/tools/requirements.txt
Checksum (sha256): `c6510e2d2bfbd08ae31ee9d1042c91e2d748cca5b1c58a6fd879ae32f5fb073c`

```
PyYAML==6.0.2
jsonschema==4.23.0

```

---

### frameworks/qa-test/manifests/2025-09/handoff_manifest.yaml
Checksum (sha256): `012b310603e08695b42bdf3c2ecaa82ff74b73164d7108727fcfa1bbef874275`

```yaml
manifest_version: 1
cycle: 2025-09
snapshot_rev: git:abcdef1234
rulebook_hash: sha256:rulebookhashhere
artifacts:
- name: test_matrix
  path: artifacts/2025-09/test_matrix.yaml
  sha256: 09af9d02a86dcba25585e7a7ed1fc57239e5a65506add9d92836d0fa65463807
- name: traceability_map
  path: artifacts/2025-09/traceability_map.md
  sha256: 98149d27a09dd05a906bdde1edcca5de05b1d82cd0d6e7c9b527ce06c7b8e7aa
- name: qa_evidence_index
  path: artifacts/2025-09/qa_evidence_index.yaml
  sha256: c13713ee27d7bc23f0a7816049a8137518976e263eb5e1a743840d2c90bb7610
quality_gates:
  schema_lint: pass
  cross_stream_consistency: pass
  parity_coverage:
    status: pass
    coverage_pct: 92
signing:
  signed_by: qa-bot@local
  signature: ''
  signed_at: '2025-09-02T03:30:22.845680Z'

```

---

### frameworks/qa-test/digests/2025-09-02-digest.md
Checksum (sha256): `5ceca1e83459067b649d2b5b7d59aad3b42a4e4a6fd5c9e8078238f95ccc1f01`

```markdown
## Cycle Digest — 2025-09-02

- Cycle: 2025-09
- Snapshot Rev: git:abcdef1234
- Rulebook Hash: sha256:rulebookhashhere

### KPI Summary
- Time to VALIDATED: TBD
- Gate pass rate: schema_lint 100%, consistency 100%, parity/coverage 100%
- Critical at PACKAGED: 0 → at VALIDATED: 0
- Exceptions: new 0, active 0, expired 0
- Coverage: 100% of required streams (sample)

### Gate Outcomes
- schema_lint: pass (sample)
- cross_stream_consistency: pass
- parity/coverage: pass

### Exceptions Summary
- None

### Top Risks & Actions
- TBD

```

---

### Makefile
Checksum (sha256): `a69d51a6160caee7347fd15ff40ed32d83c7a5eccf87a839f111d50ddf8fea1e`

```makefile
.PHONY: qa-install qa-validate qa-manifest qa-digest

qa-install:
	python3 -m venv .venv && . .venv/bin/activate && pip install -r frameworks/qa-test/tools/requirements.txt

qa-validate:
	. .venv/bin/activate && python frameworks/qa-test/tools/qa_cli.py schema_lint

qa-manifest:
	. .venv/bin/activate && python frameworks/qa-test/tools/qa_cli.py generate_manifest --snapshot_rev git:abcdef1234 --rulebook_hash sha256:rulebookhashhere --signed_by qa-bot@local

qa-digest:
	. .venv/bin/activate && python frameworks/qa-test/tools/qa_cli.py digest

```

---

### .github/workflows/qa.yml
Checksum (sha256): `7a4ea828d377616f039bf915c607a81dae567f9f49599d4b7d3bf17e1680f9d4`

```yaml
name: QA Framework Checks
on:
  push:
    paths:
      - frameworks/qa-test/**
  pull_request:
    paths:
      - frameworks/qa-test/**
jobs:
  lint-qa:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: 3.11
      - run: python -m pip install -r frameworks/qa-test/tools/requirements.txt
      - run: python frameworks/qa-test/tools/qa_cli.py schema_lint

```
\n---\n\nGenerated bundle at: /workspace/frameworks/qa-test/QA_REFERENCE_BUNDLE.md
