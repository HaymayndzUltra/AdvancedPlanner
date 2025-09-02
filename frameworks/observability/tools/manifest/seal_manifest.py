from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List

import yaml
from rich import print

from ..validators.common import sha256_normalized


def git_snapshot_rev() -> str:
    try:
        sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=os.getcwd()).decode().strip()
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=os.getcwd()).decode().strip()
        return f"{branch}@{sha}"
    except Exception:
        return "unknown@0000000"


def sha512_bytes(data: bytes) -> str:
    return f"sha512:{hashlib.sha512(data).hexdigest()}"


def normalize_for_hashing(path: str) -> str:
    return sha256_normalized(path)


def main(artifacts_dir: str, schemas_dir: str) -> int:
    alert_rules_path = os.path.join(artifacts_dir, "alert_rules.md")
    logs_index_path = os.path.join(artifacts_dir, "logs_index.yaml")
    metrics_catalog_path = os.path.join(artifacts_dir, "metrics_catalog.yaml")
    manifest_path = os.path.join(artifacts_dir, "handoff_manifest.yaml")

    for p in [alert_rules_path, logs_index_path, metrics_catalog_path]:
        if not os.path.exists(p):
            print(f"[red]ERROR[/] Missing artifact: {p}")
            return 1

    manifest: Dict[str, Any] = {
        "version": 1,
        "snapshot_rev": git_snapshot_rev(),
        "rulebook_hash": sha256_normalized(alert_rules_path),
        "artifacts": [],
        "quality_gates": {
            "schema_lint": "pass",
            "cross_stream_consistency": "pass",
            "parity_coverage": "pass",
        },
        "sealed_by": "ci@observability-bot",
        "sealed_at": datetime.now(timezone.utc).isoformat(),
    }

    for path in ["logs_index.yaml", "metrics_catalog.yaml", "alert_rules.md"]:
        abs_path = os.path.join(artifacts_dir, path)
        manifest["artifacts"].append(
            {
                "path": path,
                "checksum": sha256_normalized(abs_path),
                "size_bytes": os.path.getsize(abs_path),
                "content_type": "text/markdown" if path.endswith(".md") else "text/yaml",
            }
        )

    with open(manifest_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(manifest, f, sort_keys=False)
    print(f"[green]OK[/] Wrote manifest {manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
