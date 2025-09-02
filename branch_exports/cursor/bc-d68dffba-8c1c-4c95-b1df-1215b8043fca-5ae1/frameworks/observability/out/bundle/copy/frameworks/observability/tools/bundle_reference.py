#!/usr/bin/env python3
import argparse
import os
import shutil
from pathlib import Path


TEXT_EXTENSIONS = {
    ".md": "markdown",
    ".txt": "",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".py": "python",
    ".sh": "bash",
    ".yml": "yaml",
}

EXCLUDE_DIR_NAMES = {".git", "node_modules", "__pycache__", ".venv", "venv"}


def detect_language_suffix(path: Path) -> str:
    return TEXT_EXTENSIONS.get(path.suffix.lower(), "")


def is_text_file(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            chunk = f.read(4096)
        chunk.decode("utf-8")
        return True
    except Exception:
        return False


def _is_within(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except Exception:
        return False


def copy_tree(src: Path, dest: Path, exclude_dirs: set, skip_path: Path) -> None:
    for root, dirs, files in os.walk(src):
        root_path = Path(root)
        # Skip destination path subtree to avoid recursion
        if skip_path and _is_within(root_path, skip_path):
            continue
        # Filter directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        rel_root = root_path.relative_to(src)
        target_root = dest / rel_root
        target_root.mkdir(parents=True, exist_ok=True)
        for fname in files:
            src_file = root_path / fname
            # Skip if inside destination path
            if skip_path and _is_within(src_file, skip_path):
                continue
            dest_file = target_root / fname
            shutil.copy2(src_file, dest_file)


def write_reference(src: Path, out_file: Path, exclude_dirs: set, skip_path: Path) -> None:
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as out:
        out.write(f"# Repository Files Reference\n\n")
        for root, dirs, files in os.walk(src):
            root_path = Path(root)
            if skip_path and _is_within(root_path, skip_path):
                continue
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for fname in sorted(files):
                file_path = root_path / fname
                if skip_path and _is_within(file_path, skip_path):
                    continue
                rel = file_path.relative_to(src)
                out.write(f"## {rel.as_posix()}\n\n")
                if is_text_file(file_path):
                    lang = detect_language_suffix(file_path)
                    fence = f"```{lang}" if lang else "```"
                    out.write(fence + "\n")
                    try:
                        content = file_path.read_text(encoding="utf-8", errors="replace")
                    except Exception:
                        content = "[error reading file]"
                    out.write(content)
                    if not content.endswith("\n"):
                        out.write("\n")
                    out.write("```\n\n")
                else:
                    size = file_path.stat().st_size
                    out.write(f"[binary file omitted] (size: {size} bytes)\n\n")


def main():
    default_src = Path(__file__).resolve()
    # Try to default to workspace root (/workspace) if present
    try:
        default_src = Path(__file__).resolve().parents[3]
    except Exception:
        default_src = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(description="Copy all files and bundle into a single reference file")
    parser.add_argument("--src", default=str(default_src), help="Source directory to bundle")
    parser.add_argument("--dest-dir", default=str(Path(default_src) / "frameworks/observability/out/bundle"), help="Destination directory for copied files")
    parser.add_argument("--single-file-name", default="all_files_reference.md", help="Name of the single reference file")
    parser.add_argument("--include-hidden", action="store_true", help="Include hidden files and directories")
    args = parser.parse_args()

    src = Path(args.src).resolve()
    dest_dir = Path(args.dest_dir).resolve()
    dest_dir.mkdir(parents=True, exist_ok=True)

    exclude = set() if args.include_hidden else EXCLUDE_DIR_NAMES.copy()
    # Always skip destination path from traversal
    skip_path = dest_dir

    copy_tree(src, dest_dir / "copy", exclude, skip_path)
    reference_path = dest_dir / args.single_file_name
    write_reference(src, reference_path, exclude, skip_path)
    print(f"Copied files under: {dest_dir / 'copy'}")
    print(f"Reference file generated: {reference_path}")


if __name__ == "__main__":
    main()

