#!/usr/bin/env python3
import hashlib
import os
import re
from typing import List, Tuple


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def update_manifest_sha(manifest_path: str, artifact_paths: List[str]) -> Tuple[bool, List[Tuple[str, str]]]:
    if not os.path.exists(manifest_path):
        return False, []
    with open(manifest_path, "r", encoding="utf-8") as f:
        text = f.read()
    updates: List[Tuple[str, str]] = []
    for artifact in artifact_paths:
        rel = artifact
        digest = sha256_file("/workspace/" + rel)
        # replace the sha256 value after the matching path block
        pattern = rf"(path:\s*{re.escape(rel)}\s*\n\s*sha256:\s*)(?:\"[^\"]*\"|\S*)"
        new = rf"\g<1>{digest}"
        new_text, n = re.subn(pattern, new, text)
        if n > 0:
            updates.append((rel, digest))
            text = new_text
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(text)
    return True, updates


def main() -> None:
    changes = []
    # Security manifest
    ok, upd = update_manifest_sha(
        "/workspace/frameworks/security/manifests/2025-09/handoff_manifest.yaml",
        [
            "frameworks/security/findings.yaml",
            "frameworks/security/policy/exceptions.yaml",
        ],
    )
    changes.extend(upd)

    # Planning FE/BE manifests
    ok, upd = update_manifest_sha(
        "/workspace/frameworks/planning-fe/manifests/2025-09-02-handoff_manifest.yaml",
        [
            "frameworks/planning-fe/tasks/2025-09-02-fe_task_breakdown.yaml",
            "frameworks/planning-fe/storymaps/2025-09-02-story_map.md",
        ],
    )
    changes.extend(upd)
    ok, upd = update_manifest_sha(
        "/workspace/frameworks/planning-be/manifests/2025-09-02-handoff_manifest.yaml",
        [
            "frameworks/planning-be/backlog/2025-09-02-be_backlog.yaml",
        ],
    )
    changes.extend(upd)
    ok, upd = update_manifest_sha(
        "/workspace/frameworks/planning/manifests/2025-09/handoff_manifest.yaml",
        [
            "frameworks/planning-fe/tasks/2025-09-02-fe_task_breakdown.yaml",
            "frameworks/planning-be/backlog/2025-09-02-be_backlog.yaml",
        ],
    )
    changes.extend(upd)

    # QA manifest
    ok, upd = update_manifest_sha(
        "/workspace/frameworks/qa-test/manifests/2025-09/handoff_manifest.yaml",
        [
            "frameworks/qa-test/artifacts/2025-09/compliance_map.md",
        ],
    )
    changes.extend(upd)

    # Observability manifest
    ok, upd = update_manifest_sha(
        "/workspace/frameworks/observability/manifests/2025-09/handoff_manifest.yaml",
        [
            "frameworks/observability/digests/2025-09-02-digest.md",
        ],
    )
    changes.extend(upd)

    # Print summary
    for rel, digest in changes:
        print(f"updated {rel} sha256={digest}")


if __name__ == "__main__":
    main()

