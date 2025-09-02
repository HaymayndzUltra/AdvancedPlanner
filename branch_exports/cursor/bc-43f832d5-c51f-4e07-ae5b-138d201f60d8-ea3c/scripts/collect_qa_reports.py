#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from typing import Iterable, List

DEFAULT_GLOBS = [
    "frameworks/qa-test/digests/*.md",
    "frameworks/qa-test/artifacts/2025-09/*.*",
    "frameworks/planning-fe/tasks/*-fe_task_breakdown.yaml",
    "frameworks/planning-be/backlog/*-be_backlog.yaml",
]

SEPARATOR = "\n\n" + ("=" * 80) + "\n"


def resolve_files(repo_root: Path, patterns: Iterable[str]) -> List[Path]:
    files: List[Path] = []
    for pattern in patterns:
        for path in repo_root.glob(pattern):
            if path.is_file():
                files.append(path)
    # Stable ordering by path
    files.sort()
    return files


def concatenate(files: List[Path], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as out:
        for idx, file_path in enumerate(files, 1):
            header = f"START FILE: {file_path}\n"
            footer = f"\nEND FILE: {file_path}\n"
            out.write(SEPARATOR)
            out.write(header)
            try:
                content = file_path.read_text(encoding="utf-8", errors="replace")
            except Exception as exc:
                content = f"[ERROR READING FILE: {exc}]"
            out.write(content)
            out.write(footer)
    print(f"Wrote combined report: {out_path}")
    print(f"Included {len(files)} files.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Concatenate QA reports into one reference file (copy-only)")
    parser.add_argument("--out", default="QA_REPORTS_COMBINED.txt", help="Output file path")
    parser.add_argument(
        "--glob",
        action="append",
        default=[],
        help="Additional glob pattern(s) relative to repo root to include",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    patterns = DEFAULT_GLOBS + args.glob
    files = resolve_files(repo_root, patterns)
    if not files:
        print("No files matched. Adjust patterns or verify repository layout.", file=sys.stderr)
        return 1

    out_path = (repo_root / args.out) if not Path(args.out).is_absolute() else Path(args.out)
    concatenate(files, out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())