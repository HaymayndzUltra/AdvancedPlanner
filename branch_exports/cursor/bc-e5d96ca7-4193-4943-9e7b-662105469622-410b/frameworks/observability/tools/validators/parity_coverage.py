from __future__ import annotations

import re
import sys
from typing import Dict, List, Set

from rich import print

from .common import read_yaml


def extract_metrics_from_alert_md(alert_md_text: str) -> List[str]:
    metrics: List[str] = []
    for line in alert_md_text.splitlines():
        if line.strip().startswith("- metric:"):
            metrics.append(line.split(":", 1)[1].strip())
    return metrics


def main(artifacts_dir: str) -> int:
    status = 0
    metrics = read_yaml(f"{artifacts_dir}/metrics_catalog.yaml")
    kpis = [m for m in metrics.get("metrics", []) if bool(m.get("kpi"))]
    kpi_names: Set[str] = {m["name"] for m in kpis}

    with open(f"{artifacts_dir}/alert_rules.md", "r", encoding="utf-8") as f:
        alert_md = f.read()
    alert_metrics = set(extract_metrics_from_alert_md(alert_md))

    covered = sorted(kpi_names & alert_metrics)
    gaps = sorted(kpi_names - alert_metrics)
    coverage_pct = round(100.0 * (len(covered) / max(1, len(kpi_names))), 2)

    if gaps:
        print(f"[yellow]WARN[/] KPI alert coverage gaps: {gaps}")
    print(f"[blue]INFO[/] KPI alert coverage: {coverage_pct}% ({len(covered)}/{len(kpi_names)})")

    # Require 100% coverage for MVP
    if len(gaps) > 0:
        status = 1
        print("[red]FAIL[/] parity/coverage gate requires 100% KPI alert coverage")
    else:
        print("[green]OK[/] parity/coverage gate")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
