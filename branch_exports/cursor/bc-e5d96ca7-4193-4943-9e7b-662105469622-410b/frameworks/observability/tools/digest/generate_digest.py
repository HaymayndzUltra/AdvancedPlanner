from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from typing import Set

from rich import print

from ..validators.common import read_yaml


def main(artifacts_dir: str, digests_dir: str) -> int:
    manifest_path = os.path.join(artifacts_dir, "handoff_manifest.yaml")
    if not os.path.exists(manifest_path):
        print("[red]ERROR[/] No sealed manifest found. Run make package first.")
        return 1
    manifest = read_yaml(manifest_path)
    metrics = read_yaml(os.path.join(artifacts_dir, "metrics_catalog.yaml"))
    kpis = [m for m in metrics.get("metrics", []) if bool(m.get("kpi"))]
    kpi_names: Set[str] = {m["name"] for m in kpis}

    # Simple digest with placeholders for current/prior
    cycle = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = os.path.join(digests_dir, f"{cycle}-digest.md")
    lines = []
    lines.append(f"# Observability Digest — {cycle}")
    lines.append("")
    lines.append(f"- snapshot_rev: {manifest.get('snapshot_rev')}")
    lines.append(f"- rulebook_hash: {manifest.get('rulebook_hash')}")
    # checksum of manifest file itself
    lines.append(f"- manifest_checksum: <sealed>")
    lines.append(f"- cycle_window: <t-7d → {cycle}>")
    lines.append(f"- environment: prod")
    lines.append("")
    lines.append("### KPI Summary")
    lines.append("| KPI | Current | Prior | SLO | Status |")
    lines.append("|---|---:|---:|---:|---|")
    for k in sorted(kpi_names):
        lines.append(f"| {k} | <n/a> | <n/a> | <n/a> | N/A |")
    lines.append("")
    lines.append("### Coverage & Parity")
    lines.append("- KPIs: %d; Alerts: <x/x>; Dashboards: <x/x>; Runbooks: <x/x> → <status>" % (len(kpi_names)))
    lines.append("")
    lines.append("### Drift & Hygiene")
    lines.append("- Schema drifts: <none>")
    lines.append("- Threshold drift: <none>")
    lines.append("- Label cardinality: <within limits>")
    lines.append("")
    lines.append("### Hot Alerts & Incidents")
    lines.append("- <none>")
    lines.append("")
    lines.append("### Improvement Actions")
    lines.append("- <tbd>")
    lines.append("")
    lines.append("### Appendix")
    lines.append("- Linked manifest: handoff_manifest.yaml")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[green]OK[/] Wrote digest {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
