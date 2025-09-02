from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List

from rich import print

from .common import validate_yaml_with_schema


def main(artifacts_dir: str, schemas_dir: str) -> int:
    checks: List[tuple[str, str]] = [
        ("logs_index.yaml", "logs_index.schema.yaml"),
        ("metrics_catalog.yaml", "metrics_catalog.schema.yaml"),
        ("handoff_manifest.yaml", "handoff_manifest.schema.yaml"),
    ]
    status = 0
    for artifact_name, schema_name in checks:
        artifact_path = os.path.join(artifacts_dir, artifact_name)
        schema_path = os.path.join(schemas_dir, schema_name)
        if not os.path.exists(artifact_path):
            # handoff_manifest is generated later; skip missing
            if artifact_name == "handoff_manifest.yaml":
                print(f"[yellow]SKIP[/] {artifact_name} (not present)")
                continue
            print(f"[red]ERROR[/] Missing {artifact_name}")
            status = 1
            continue
        try:
            validate_yaml_with_schema(artifact_path, schema_path)
            print(f"[green]OK[/] {artifact_name} against {schema_name}")
        except Exception as exc:
            print(f"[red]FAIL[/] {artifact_name}: {exc}")
            status = 1
    # alert_rules.md is markdown; ensure required sections exist (light check)
    alert_md = os.path.join(artifacts_dir, "alert_rules.md")
    if not os.path.exists(alert_md):
        print("[red]ERROR[/] Missing alert_rules.md")
        status = 1
    else:
        txt = Path(alert_md).read_text(encoding="utf-8")
        required_snippets = ["##", "metric:", "severity:", "runbook:", "tags:"]
        if not all(snip in txt for snip in required_snippets):
            print("[red]FAIL[/] alert_rules.md missing required sections")
            status = 1
        else:
            print("[green]OK[/] alert_rules.md structural check")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
