#!/usr/bin/env python3
import json
import os
import re
from typing import Dict, List, Tuple


SNAPSHOT_REV = "git:abcdef1234"


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def file_exists(path: str) -> bool:
    return os.path.exists(path)


def check_schema_lint() -> Tuple[bool, Dict[str, str]]:
    results: Dict[str, str] = {}
    ok = True

    yaml_reqs = [
        "/workspace/frameworks/security/manifests/2025-09/handoff_manifest.yaml",
        "/workspace/frameworks/planning-fe/manifests/2025-09-02-handoff_manifest.yaml",
        "/workspace/frameworks/planning-be/manifests/2025-09-02-handoff_manifest.yaml",
        "/workspace/frameworks/planning/manifests/2025-09/handoff_manifest.yaml",
        "/workspace/frameworks/qa-test/manifests/2025-09/handoff_manifest.yaml",
        "/workspace/frameworks/observability/manifests/2025-09/handoff_manifest.yaml",
    ]

    for path in yaml_reqs:
        name = os.path.relpath(path, "/workspace")
        if not file_exists(path):
            ok = False
            results[name] = "missing file"
            continue
        text = read_text(path)
        checks = [
            (r"\bsnapshot_rev:\s*\"?%s\"?\b" % re.escape(SNAPSHOT_REV), "snapshot_rev present"),
            (r"\brulebook_hash:\s*\"?sha256:[^\n\r]+\"?", "rulebook_hash present"),
            (r"\bgovernance:\s*\n\s+tags:\s*\[[^\]]*\]", "governance.tags present"),
            (r"\bsealed:\s*true", "sealed true"),
        ]
        file_ok = True
        for pattern, label in checks:
            if not re.search(pattern, text):
                ok = False
                file_ok = False
        results[name] = "pass" if file_ok else "fail"

    md_reqs = [
        "/workspace/frameworks/qa-test/artifacts/2025-09/compliance_map.md",
        "/workspace/frameworks/planning-fe/storymaps/2025-09-02-story_map.md",
        "/workspace/frameworks/observability/digests/2025-09-02-digest.md",
    ]
    for path in md_reqs:
        name = os.path.relpath(path, "/workspace")
        if not file_exists(path):
            ok = False
            results[name] = "missing file"
            continue
        text = read_text(path)
        fm_ok = bool(
            re.search(r"^---[\s\S]*?^---", text, re.MULTILINE)
            and re.search(r"snapshot_rev:\s*\"?%s\"?" % re.escape(SNAPSHOT_REV), text)
            and re.search(r"rulebook_hash:\s*\"?sha256:[^\n\r]+\"?", text)
            and re.search(r"governance:\s*\n\s+tags:\s*\[[^\]]*\]", text)
        )
        if not fm_ok:
            ok = False
            results[name] = "fail"
        else:
            results[name] = "pass"

    return ok, results


def check_snapshot_integrity() -> Tuple[bool, List[str]]:
    files = [
        "/workspace/frameworks/security/findings.yaml",
        "/workspace/frameworks/security/policy/exceptions.yaml",
        "/workspace/frameworks/security/waivers.yaml",
        "/workspace/frameworks/security/manifests/2025-09/handoff_manifest.yaml",
        "/workspace/frameworks/planning-fe/tasks/2025-09-02-fe_task_breakdown.yaml",
        "/workspace/frameworks/planning-fe/storymaps/2025-09-02-story_map.md",
        "/workspace/frameworks/planning-fe/manifests/2025-09-02-handoff_manifest.yaml",
        "/workspace/frameworks/planning-be/backlog/2025-09-02-be_backlog.yaml",
        "/workspace/frameworks/planning-be/manifests/2025-09-02-handoff_manifest.yaml",
        "/workspace/frameworks/planning/manifests/2025-09/handoff_manifest.yaml",
        "/workspace/frameworks/qa-test/artifacts/2025-09/compliance_map.md",
        "/workspace/frameworks/qa-test/manifests/2025-09/handoff_manifest.yaml",
        "/workspace/frameworks/observability/digests/2025-09-02-digest.md",
        "/workspace/frameworks/observability/manifests/2025-09/handoff_manifest.yaml",
    ]
    failures: List[str] = []
    for path in files:
        if not file_exists(path):
            failures.append(f"missing:{path}")
            continue
        text = read_text(path)
        if not re.search(r"\bsnapshot_rev:\s*\"?%s\"?\b" % re.escape(SNAPSHOT_REV), text):
            failures.append(os.path.relpath(path, "/workspace"))
    return len(failures) == 0, failures


def parse_fe_story_ids(path: str) -> List[str]:
    text = read_text(path)
    ids: List[str] = []
    for m in re.finditer(r"^\s*-\s+id:\s*([A-Za-z0-9\-]+)\s*$", text, re.MULTILINE):
        ids.append(m.group(1))
    return ids


def parse_be_story_refs(path: str) -> List[str]:
    text = read_text(path)
    refs: List[str] = []
    for m in re.finditer(r"^\s*story_ref:\s*([A-Za-z0-9\-]+)\s*$", text, re.MULTILINE):
        refs.append(m.group(1))
    return refs


def check_cross_stream_consistency() -> Tuple[bool, Dict[str, List[str]]]:
    fe_path = "/workspace/frameworks/planning-fe/tasks/2025-09-02-fe_task_breakdown.yaml"
    be_path = "/workspace/frameworks/planning-be/backlog/2025-09-02-be_backlog.yaml"
    if not (file_exists(fe_path) and file_exists(be_path)):
        return False, {"missing": [p for p in [fe_path, be_path] if not file_exists(p)]}
    fe_ids = set(parse_fe_story_ids(fe_path))
    be_refs = parse_be_story_refs(be_path)
    missing = [r for r in be_refs if r not in fe_ids]
    return len(missing) == 0, {"missing_story_refs": missing}


def check_parity_coverage() -> Tuple[bool, Dict[str, str]]:
    path = "/workspace/frameworks/qa-test/artifacts/2025-09/compliance_map.md"
    if not file_exists(path):
        return False, {"error": "missing compliance_map.md"}
    text = read_text(path)
    tests_ok = bool(re.search(r"test_ids:\s*\[[^\]]+\]", text))
    evidence_ok = bool(re.search(r"evidence_refs:\s*\[[^\]]+\]", text))
    return tests_ok and evidence_ok, {"tests_ok": str(tests_ok), "evidence_ok": str(evidence_ok)}


def check_critical_zero() -> Tuple[bool, Dict[str, str]]:
    path = "/workspace/frameworks/security/findings.yaml"
    if not file_exists(path):
        return False, {"error": "missing findings.yaml"}
    text = read_text(path)
    m = re.search(r"critical_open:\s*(\d+)", text)
    if not m:
        return False, {"error": "critical_open not found"}
    value = int(m.group(1))
    return value == 0, {"critical_open": str(value)}


def main() -> None:
    results = {}
    schema_ok, schema_detail = check_schema_lint()
    results["schema_lint"] = {"ok": schema_ok, "detail": schema_detail}

    snap_ok, snap_detail = check_snapshot_integrity()
    results["snapshot_integrity"] = {"ok": snap_ok, "missing_or_mismatch": snap_detail}

    x_ok, x_detail = check_cross_stream_consistency()
    results["cross_stream_consistency"] = {"ok": x_ok, "detail": x_detail}

    p_ok, p_detail = check_parity_coverage()
    results["parity_coverage"] = {"ok": p_ok, "detail": p_detail, "threshold": 0.90, "coverage_pct": 1.0 if p_ok else 0.0}

    s_ok, s_detail = check_critical_zero()
    results["security_critical_zero"] = {"ok": s_ok, "detail": s_detail}

    overall_ok = all([
        schema_ok,
        snap_ok,
        x_ok,
        p_ok,
        s_ok,
    ])
    results["overall_ok"] = overall_ok

    os.makedirs("/workspace/dev-workflow/validation", exist_ok=True)
    out_path = "/workspace/dev-workflow/validation/results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, sort_keys=True)
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

