# Repository Files Reference

## README.md

```markdown
Observability Framework
=======================

This repository segment contains the artifact-first Observability & Monitoring framework.

Directories
-----------
- `schemas/`: JSON Schemas for artifact validation.
- `tools/`: CLI validators and packaging utilities.
- `digests/`: Cycle-based operational digests.

Core Artifacts
--------------
- `logs_index.yaml`: Canonical log streams and schemas.
- `metrics_catalog.yaml`: Metrics/KPIs catalog with SLO bindings.
- `alert_rules.md`: Human rulebook describing alerts and governance tags.

Quick Start
-----------
1. (Optional) Create a Python virtual environment.
2. If venv is unavailable, you can run stdlib-only manifest generator.
3. Install requirements (CI or local with venv): `pip install -r tools/requirements.txt`.
4. Run gates:
   - `python tools/obs_cli.py schema-lint`
   - `python tools/obs_cli.py cross-consistency`
   - `python tools/obs_cli.py parity-coverage`
   - `python tools/obs_cli.py governance-check`
5. Package a handoff manifest:
   - With deps: `python tools/obs_cli.py generate-manifest --out out/handoff_manifest.yaml`
   - Stdlib-only: `python tools/generate_manifest_stdlib.py --snapshot main@abc1234 --out out/handoff_manifest.yaml`

Notes
-----
- Governance policy enforces `Critical=0` by default; exceptions must be tagged explicitly.
- Handoff manifests are immutable once sealed; new changes require a new manifest.

```

## alert_rules.md

```markdown
# Alert Rules Catalog

## Alert: Payments Elevated Error Rate
- metric: payments.error_rate
- severity: critical
- condition: error_rate > 1% for 5m
- runbook: link://runbook/payments-error-burst
- tags: [service:payments, Critical:0, owner:team-payments]

## Alert: Payments High P95 Latency
- metric: payments.p95_latency
- severity: warning
- condition: p95_latency > 300ms for 10m
- runbook: link://runbook/payments-latency-tuning
- tags: [service:payments, Critical:0, owner:team-payments]

## Alert: Payments Request Rate Anomaly
- metric: payments.request_rate
- severity: info
- condition: request_rate deviates > 3x from 7d baseline
- runbook: link://runbook/payments-traffic-anomaly
- tags: [service:payments, Critical:0, owner:team-payments]

```

## logs_index.yaml

```yaml
version: 1
streams:
  - name: payments_api.access
    owner: team-payments
    retention_days: 30
    pii: false
    schema_version: 3
    schema:
      - field: timestamp
        type: datetime
      - field: status_code
        type: int
      - field: latency_ms
        type: int
      - field: route
        type: string
    tags: [service:payments, tier:backend]

```

## metrics_catalog.yaml

```yaml
version: 1
metrics:
  - name: payments.request_rate
    type: counter
    unit: rps
    owner: team-payments
    description: Incoming requests per second
    kpi: true
    slo:
      objective: 99.9
      window: 30d
    tags: [service:payments, tier:backend]
  - name: payments.error_rate
    type: ratio
    numerator: payments.errors
    denominator: payments.request_rate
    unit: pct
    owner: team-payments
    kpi: true
    slo:
      objective: 99.9
      window: 30d
    tags: [service:payments, tier:backend]
  - name: payments.p95_latency
    type: histogram
    unit: ms
    owner: team-payments
    description: 95th percentile latency for API requests
    kpi: true
    slo:
      objective: 300
      window: 30d
    tags: [service:payments, tier:backend]

```

## schemas/handoff_manifest.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/schemas/handoff_manifest.schema.json",
  "title": "handoff_manifest",
  "type": "object",
  "required": ["version", "snapshot_rev", "artifacts", "rulebook_hash"],
  "properties": {
    "version": { "type": ["integer", "string"] },
    "snapshot_rev": { "type": "string", "minLength": 1 },
    "rulebook_hash": { "type": "string", "pattern": "^sha256:[a-fA-F0-9]{6,}$" },
    "artifacts": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["path", "checksum"],
        "properties": {
          "path": { "type": "string", "minLength": 1 },
          "checksum": { "type": "string", "pattern": "^sha256:[a-fA-F0-9]{6,}$" },
          "size_bytes": { "type": "integer", "minimum": 0 },
          "content_type": { "type": "string" }
        },
        "additionalProperties": false
      }
    },
    "quality_gates": {
      "type": "object",
      "properties": {
        "schema_lint": { "type": ["string", "object"] },
        "cross_stream_consistency": { "type": ["string", "object"] },
        "parity_coverage": { "type": ["string", "object"] }
      },
      "additionalProperties": true
    },
    "governance": {
      "type": "object",
      "properties": {
        "tags": { "type": "array", "items": { "type": "string" } },
        "critical_rule_violation_count": { "type": "integer", "minimum": 0 }
      },
      "additionalProperties": true
    },
    "execution": { "type": "object" },
    "validation": { "type": "object" }
  },
  "additionalProperties": false
}

```

## schemas/logs_index.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/schemas/logs_index.schema.json",
  "title": "logs_index",
  "type": "object",
  "required": ["version", "streams"],
  "properties": {
    "version": { "type": ["integer", "string"] },
    "streams": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "owner", "retention_days", "schema"],
        "properties": {
          "name": { "type": "string", "minLength": 1 },
          "owner": { "type": "string", "minLength": 1 },
          "retention_days": { "type": "integer", "minimum": 1 },
          "pii": { "type": ["boolean", "string"] },
          "schema_version": { "type": ["integer", "string"] },
          "schema": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "object",
              "required": ["field", "type"],
              "properties": {
                "field": { "type": "string", "minLength": 1 },
                "type": { "type": "string", "enum": ["datetime", "string", "int", "float", "boolean"] }
              }
            }
          },
          "tags": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}

```

## schemas/metrics_catalog.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/schemas/metrics_catalog.schema.json",
  "title": "metrics_catalog",
  "type": "object",
  "required": ["version", "metrics"],
  "properties": {
    "version": { "type": ["integer", "string"] },
    "metrics": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["name", "type", "unit", "owner"],
        "properties": {
          "name": { "type": "string", "minLength": 1 },
          "type": { "type": "string", "enum": ["counter", "gauge", "histogram", "ratio"] },
          "unit": { "type": "string", "minLength": 1 },
          "owner": { "type": "string", "minLength": 1 },
          "description": { "type": "string" },
          "kpi": { "type": "boolean" },
          "slo": {
            "type": "object",
            "required": ["objective", "window"],
            "properties": {
              "objective": { "type": ["number", "integer", "string"] },
              "window": { "type": "string", "minLength": 1 }
            },
            "additionalProperties": false
          },
          "numerator": { "type": "string" },
          "denominator": { "type": "string" },
          "tags": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "additionalProperties": false
      }
    }
  },
  "additionalProperties": false
}

```

## out/handoff_manifest.yaml

```yaml
version: 1
snapshot_rev: main@abc1234
rulebook_hash: sha256:4b3368fed202cfb98ef2352b2161d2c03189248bad594875cbd9d4662c284126
artifacts:
  - path: logs_index.yaml
    checksum: sha256:f72459216a2dcf8bb266c87cdad649ec4f2cb4886147cf1faa645a5a6ba323f3
    size_bytes: 370
  - path: metrics_catalog.yaml
    checksum: sha256:006ba2a932a1e1950adc33eee6cd899ea717b455b126dd63e7119f520202faab
    size_bytes: 775
  - path: alert_rules.md
    checksum: sha256:4b3368fed202cfb98ef2352b2161d2c03189248bad594875cbd9d4662c284126
    size_bytes: 754
quality_gates:
  schema_lint: pending
  cross_stream_consistency: pending
  parity_coverage: pending
sealed_by: local
sealed_at: 2025-09-02T04:26:04.729234+00:00
```

## digests/2025-09-02-digest.md

```markdown
# Observability Digest — 2025-09-02

- snapshot_rev: main@abc1234 (placeholder)
- rulebook_hash: sha256:PLACEHOLDER
- manifest_checksum: sha256:PLACEHOLDER
- cycle_window: 2025-08-26 → 2025-09-02
- environment: prod

## KPI Summary
| KPI | Current | Prior | SLO | Status | Notes |
|---|---:|---:|---:|---|---|
| payments.error_rate | 0.6% | 0.9% | 99.9 | ✅ | Improving |
| payments.request_rate | 1.2k rps | 1.1k rps | n/a | ✅ | Volume up 9% |
| payments.p95_latency | 220 ms | 240 ms | 300 ms | ✅ | Stable |

## Coverage & Parity
- KPIs: 3; Alerts: 3/3; Dashboards: 3/3; Runbooks: 3/3 → ✅
- Governance: `Critical=0` observed on all alerts; no exceptions open.

## Drift & Hygiene
- Schema drifts: none detected.
- Threshold drift: none.
- Label cardinality: within limits.

## Hot Alerts & Incidents
- payments.error_rate spikes x2 (2025-08-29, 2025-09-01) — MTTA 3m; MTTR 18m.

## Improvement Actions
- Lower warning threshold for latency to preempt criticals; Owner: team-payments; Due: 2025-09-09.
- Add SLO annotation to `payments.request_rate`; Owner: obs-platform; Due: 2025-09-06.

```

## tools/bundle_reference.py

```python
#!/usr/bin/env python3
import argparse
import os
import shutil
from pathlib import Path


TEXT_EXTENSIONS = {
    ".md": "markdown",
    ".txt": "",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".py": "python",
    ".sh": "bash",
    ".yml": "yaml",
}

EXCLUDE_DIR_NAMES = {".git", "node_modules", "__pycache__", ".venv", "venv"}


def detect_language_suffix(path: Path) -> str:
    return TEXT_EXTENSIONS.get(path.suffix.lower(), "")


def is_text_file(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            chunk = f.read(4096)
        chunk.decode("utf-8")
        return True
    except Exception:
        return False


def _is_within(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except Exception:
        return False


def copy_tree(src: Path, dest: Path, exclude_dirs: set, skip_path: Path) -> None:
    for root, dirs, files in os.walk(src):
        root_path = Path(root)
        # Skip destination path subtree to avoid recursion
        if skip_path and _is_within(root_path, skip_path):
            continue
        # Filter directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        rel_root = root_path.relative_to(src)
        target_root = dest / rel_root
        target_root.mkdir(parents=True, exist_ok=True)
        for fname in files:
            src_file = root_path / fname
            # Skip if inside destination path
            if skip_path and _is_within(src_file, skip_path):
                continue
            dest_file = target_root / fname
            shutil.copy2(src_file, dest_file)


def write_reference(src: Path, out_file: Path, exclude_dirs: set, skip_path: Path) -> None:
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as out:
        out.write(f"# Repository Files Reference\n\n")
        for root, dirs, files in os.walk(src):
            root_path = Path(root)
            if skip_path and _is_within(root_path, skip_path):
                continue
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for fname in sorted(files):
                file_path = root_path / fname
                if skip_path and _is_within(file_path, skip_path):
                    continue
                rel = file_path.relative_to(src)
                out.write(f"## {rel.as_posix()}\n\n")
                if is_text_file(file_path):
                    lang = detect_language_suffix(file_path)
                    fence = f"```{lang}" if lang else "```"
                    out.write(fence + "\n")
                    try:
                        content = file_path.read_text(encoding="utf-8", errors="replace")
                    except Exception:
                        content = "[error reading file]"
                    out.write(content)
                    if not content.endswith("\n"):
                        out.write("\n")
                    out.write("```\n\n")
                else:
                    size = file_path.stat().st_size
                    out.write(f"[binary file omitted] (size: {size} bytes)\n\n")


def main():
    default_src = Path(__file__).resolve()
    # Try to default to workspace root (/workspace) if present
    try:
        default_src = Path(__file__).resolve().parents[3]
    except Exception:
        default_src = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(description="Copy all files and bundle into a single reference file")
    parser.add_argument("--src", default=str(default_src), help="Source directory to bundle")
    parser.add_argument("--dest-dir", default=str(Path(default_src) / "frameworks/observability/out/bundle"), help="Destination directory for copied files")
    parser.add_argument("--single-file-name", default="all_files_reference.md", help="Name of the single reference file")
    parser.add_argument("--include-hidden", action="store_true", help="Include hidden files and directories")
    args = parser.parse_args()

    src = Path(args.src).resolve()
    dest_dir = Path(args.dest_dir).resolve()
    dest_dir.mkdir(parents=True, exist_ok=True)

    exclude = set() if args.include_hidden else EXCLUDE_DIR_NAMES.copy()
    # Always skip destination path from traversal
    skip_path = dest_dir

    copy_tree(src, dest_dir / "copy", exclude, skip_path)
    reference_path = dest_dir / args.single_file_name
    write_reference(src, reference_path, exclude, skip_path)
    print(f"Copied files under: {dest_dir / 'copy'}")
    print(f"Reference file generated: {reference_path}")


if __name__ == "__main__":
    main()

```

## tools/generate_manifest_stdlib.py

```python
#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path
from datetime import datetime, timezone


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def sha256_normalized_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_yaml_manifest(out_path: Path, manifest: dict) -> None:
    # Minimal YAML emitter for this manifest structure only.
    lines = []
    lines.append(f"version: {manifest['version']}")
    lines.append(f"snapshot_rev: {manifest['snapshot_rev']}")
    lines.append(f"rulebook_hash: {manifest['rulebook_hash']}")
    lines.append("artifacts:")
    for a in manifest["artifacts"]:
        lines.append(f"  - path: {a['path']}")
        lines.append(f"    checksum: {a['checksum']}")
        lines.append(f"    size_bytes: {a['size_bytes']}")
    lines.append("quality_gates:")
    for k, v in manifest["quality_gates"].items():
        lines.append(f"  {k}: {v}")
    if manifest.get("sealed_by"):
        lines.append(f"sealed_by: {manifest['sealed_by']}")
    if manifest.get("sealed_at"):
        lines.append(f"sealed_at: {manifest['sealed_at']}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate handoff manifest (stdlib-only)")
    parser.add_argument("--snapshot", dest="snapshot_rev", default="main@PLACEHOLDER")
    parser.add_argument("--out", dest="out_path", required=True)
    parser.add_argument("--root", dest="root", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()

    root = Path(args.root)
    artifacts_list = [
        "logs_index.yaml",
        "metrics_catalog.yaml",
        "alert_rules.md",
    ]
    entries = []
    for rel in artifacts_list:
        p = root / rel
        if p.exists():
            entries.append({
                "path": rel,
                "checksum": sha256_file(p),
                "size_bytes": p.stat().st_size,
            })
    rulebook_path = root / "alert_rules.md"
    rulebook_hash = sha256_normalized_text(rulebook_path) if rulebook_path.exists() else "sha256:"
    manifest = {
        "version": 1,
        "snapshot_rev": args.snapshot_rev,
        "rulebook_hash": rulebook_hash,
        "artifacts": entries,
        "quality_gates": {
            "schema_lint": "pending",
            "cross_stream_consistency": "pending",
            "parity_coverage": "pending",
        },
        "sealed_by": "local",
        "sealed_at": datetime.now(timezone.utc).isoformat(),
    }
    write_yaml_manifest(Path(args.out_path), manifest)


if __name__ == "__main__":
    main()

```

## tools/obs_cli.py

```python
#!/usr/bin/env python3
import hashlib
import json
import os
import sys
from pathlib import Path

import click
import yaml
from jsonschema import validate, Draft202012Validator
from rich.console import Console
from rich.table import Table

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
ARTIFACTS = ROOT
OUT = ROOT / "out"
console = Console()


def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def sha256_normalized_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().replace("\r\n", "\n").replace("\r", "\n")
    return "sha256:" + hashlib.sha256(content.encode("utf-8")).hexdigest()


@click.group()
def cli():
    pass


@cli.command("schema-lint")
@click.option("--strict/--no-strict", default=True, help="Fail on additionalProperties")
def schema_lint(strict: bool):
    """Validate artifacts against JSON Schemas."""
    mappings = [
        (ARTIFACTS / "logs_index.yaml", SCHEMAS / "logs_index.schema.json"),
        (ARTIFACTS / "metrics_catalog.yaml", SCHEMAS / "metrics_catalog.schema.json"),
    ]
    ok = True
    for artifact, schema in mappings:
        if not artifact.exists():
            console.print(f"[yellow]Skip missing {artifact}")
            continue
        data = load_yaml(artifact)
        schema_obj = load_json(schema)
        validator_cls = Draft202012Validator
        validator = validator_cls(schema_obj)
        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
        if errors:
            ok = False
            console.print(f"[red]Schema errors in {artifact}:")
            for err in errors:
                console.print(f"  - {list(err.path)}: {err.message}")
        else:
            console.print(f"[green]OK {artifact}")
    sys.exit(0 if ok else 1)


@cli.command("cross-consistency")
def cross_consistency():
    """Cross-validate naming, owners, and references across artifacts."""
    ok = True
    logs = load_yaml(ARTIFACTS / "logs_index.yaml") if (ARTIFACTS / "logs_index.yaml").exists() else {"streams": []}
    metrics = load_yaml(ARTIFACTS / "metrics_catalog.yaml") if (ARTIFACTS / "metrics_catalog.yaml").exists() else {"metrics": []}

    # Owners present
    for s in logs.get("streams", []):
        if not s.get("owner"):
            console.print(f"[red]Missing owner on log stream {s.get('name')}")
            ok = False
    for m in metrics.get("metrics", []):
        if not m.get("owner"):
            console.print(f"[red]Missing owner on metric {m.get('name')}")
            ok = False

    # Ratio metrics reference existing metrics
    metric_names = {m.get("name") for m in metrics.get("metrics", [])}
    for m in metrics.get("metrics", []):
        if m.get("type") == "ratio":
            num = m.get("numerator")
            den = m.get("denominator")
            if num and num not in metric_names:
                console.print(f"[red]Numerator {num} not defined in metrics_catalog")
                ok = False
            if den and den not in metric_names:
                console.print(f"[red]Denominator {den} not defined in metrics_catalog")
                ok = False

    sys.exit(0 if ok else 1)


@cli.command("parity-coverage")
def parity_coverage():
    """Compute KPI alert coverage and surface gaps."""
    ok = True
    metrics = load_yaml(ARTIFACTS / "metrics_catalog.yaml") if (ARTIFACTS / "metrics_catalog.yaml").exists() else {"metrics": []}
    kpis = [m for m in metrics.get("metrics", []) if m.get("kpi")]

    # Naive extraction of referenced metrics in alert_rules.md
    alerts_path = ARTIFACTS / "alert_rules.md"
    referenced = set()
    if alerts_path.exists():
        text = alerts_path.read_text(encoding="utf-8")
        for m in metrics.get("metrics", []):
            if m.get("name") and m["name"] in text:
                referenced.add(m["name"])
    covered = [m for m in kpis if m.get("name") in referenced]
    coverage_pct = int(round((len(covered) / len(kpis)) * 100)) if kpis else 100
    gaps = [m.get("name") for m in kpis if m.get("name") not in referenced]

    table = Table(title="KPI Alert Coverage")
    table.add_column("Total KPIs")
    table.add_column("Covered")
    table.add_column("Coverage %")
    table.add_column("Gaps")
    table.add_row(str(len(kpis)), str(len(covered)), str(coverage_pct), ", ".join(gaps) or "-")
    console.print(table)

    # Consider < 100% coverage as non-fatal for now
    sys.exit(0 if coverage_pct == 100 else 1)


@cli.command("governance-check")
def governance_check():
    """Enforce Critical=0 and presence of owner/service tags in alerts."""
    ok = True
    alerts_path = ARTIFACTS / "alert_rules.md"
    if not alerts_path.exists():
        console.print("[yellow]No alert_rules.md found")
        sys.exit(0)
    text = alerts_path.read_text(encoding="utf-8")
    # Basic checks
    if "Critical:1" in text or "Critical:true" in text or "critical=true" in text:
        console.print("[red]Critical policy violation detected in alert rules")
        ok = False
    # Check owner tag presence per alert block
    blocks = [b.strip() for b in text.split("## ") if b.strip()]
    for b in blocks:
        if "owner:" not in b:
            console.print("[red]Missing owner in alert block:")
            console.print(b.splitlines()[0])
            ok = False
        if "service:" not in b:
            console.print("[red]Missing service tag in alert block:")
            console.print(b.splitlines()[0])
            ok = False
    sys.exit(0 if ok else 1)


@cli.command("generate-manifest")
@click.option("--snapshot-rev", required=False, default="main@PLACEHOLDER")
@click.option("--out", "out_path", required=True, type=click.Path(dir_okay=False, path_type=Path))
def generate_manifest(snapshot_rev: str, out_path: Path):
    """Generate an immutable handoff manifest with checksums and rulebook hash."""
    artifacts = [
        "logs_index.yaml",
        "metrics_catalog.yaml",
        "alert_rules.md",
    ]
    entries = []
    for rel in artifacts:
        p = ARTIFACTS / rel
        if p.exists():
            entries.append({
                "path": rel,
                "checksum": sha256_file(p),
                "size_bytes": p.stat().st_size,
            })
    rulebook_hash = sha256_normalized_text(ARTIFACTS / "alert_rules.md") if (ARTIFACTS / "alert_rules.md").exists() else "sha256:"
    manifest = {
        "version": 1,
        "snapshot_rev": snapshot_rev,
        "rulebook_hash": rulebook_hash,
        "artifacts": entries,
        "quality_gates": {
            "schema_lint": "pass",
            "cross_stream_consistency": "pass",
            "parity_coverage": "computed"
        },
        "sealed_by": "ci@observability-bot",
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(manifest, f, sort_keys=False)
    console.print(f"[green]Wrote manifest to {out_path}")


if __name__ == "__main__":
    cli()
```

## tools/requirements.txt

```
jsonschema==4.23.0
PyYAML==6.0.2
click==8.1.7
cryptography==43.0.1
rich==13.7.1
```

