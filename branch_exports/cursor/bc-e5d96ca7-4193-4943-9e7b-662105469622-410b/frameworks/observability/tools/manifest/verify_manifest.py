from __future__ import annotations

import os
import sys
from typing import Any, Dict

import yaml
from rich import print

from ..validators.common import sha256_normalized


def main(artifacts_dir: str) -> int:
    manifest_path = os.path.join(artifacts_dir, "handoff_manifest.yaml")
    if not os.path.exists(manifest_path):
        print(f"[red]ERROR[/] Manifest not found: {manifest_path}")
        return 1
    manifest: Dict[str, Any] = yaml.safe_load(open(manifest_path, "r", encoding="utf-8"))
    status = 0
    for art in manifest.get("artifacts", []):
        path = os.path.join(artifacts_dir, art["path"]) 
        actual = sha256_normalized(path)
        recorded = art["checksum"]
        if actual != recorded:
            print(f"[red]FAIL[/] Checksum mismatch for {art['path']}: {actual} != {recorded}")
            status = 1
        else:
            print(f"[green]OK[/] {art['path']} checksum verified")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
