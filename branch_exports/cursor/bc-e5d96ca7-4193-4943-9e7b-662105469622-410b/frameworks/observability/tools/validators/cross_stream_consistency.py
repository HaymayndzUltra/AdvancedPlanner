from __future__ import annotations

import sys
from typing import Dict, List, Set

from rich import print

from .common import read_yaml, assert_required_tags, assert_critical_zero


REQUIRED_TAG_KEYS = ["service", "owner", "tier", "environment"]


def main(artifacts_dir: str) -> int:
    status = 0
    logs = read_yaml(f"{artifacts_dir}/logs_index.yaml")
    metrics = read_yaml(f"{artifacts_dir}/metrics_catalog.yaml")

    # Ensure service ownership alignment
    log_services: Set[str] = set()
    for stream in logs.get("streams", []):
        tags = stream.get("tags", [])
        try:
            assert_required_tags(tags, REQUIRED_TAG_KEYS)
        except Exception as exc:
            print(f"[red]FAIL[/] logs_index tag check for {stream.get('name')}: {exc}")
            status = 1
        for t in tags:
            if t.startswith("service:"):
                log_services.add(t.split(":", 1)[1])

    metric_services: Set[str] = set()
    for m in metrics.get("metrics", []):
        tags = m.get("tags", [])
        try:
            assert_required_tags(tags, REQUIRED_TAG_KEYS)
        except Exception as exc:
            print(f"[red]FAIL[/] metrics_catalog tag check for {m.get('name')}: {exc}")
            status = 1
        for t in tags:
            if t.startswith("service:"):
                metric_services.add(t.split(":", 1)[1])

    missing_in_metrics = log_services - metric_services
    if missing_in_metrics:
        print(f"[yellow]WARN[/] services present in logs but not metrics: {sorted(missing_in_metrics)}")

    # Governance: Critical=0 across alerts
    try:
        with open(f"{artifacts_dir}/alert_rules.md", "r", encoding="utf-8") as f:
            txt = f.read()
        # naive parse: collect tag lines
        tag_lines = [line for line in txt.splitlines() if line.strip().startswith("- tags:")]
        for line in tag_lines:
            inside = line.split("[", 1)[-1].split("]", 1)[0]
            tags = [t.strip() for t in inside.split(",") if t.strip()]
            assert_critical_zero(tags)
        print("[green]OK[/] Governance Critical=0 check")
    except Exception as exc:
        print(f"[red]FAIL[/] Governance check: {exc}")
        status = 1

    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
