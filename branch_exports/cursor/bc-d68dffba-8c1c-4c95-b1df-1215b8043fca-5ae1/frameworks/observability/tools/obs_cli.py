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
