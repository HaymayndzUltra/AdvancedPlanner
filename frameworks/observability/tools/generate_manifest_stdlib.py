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

