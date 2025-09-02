#!/usr/bin/env bash
set -euo pipefail

print_usage() {
  echo "Usage: $0 [ROOT_DIR] [DEST_DIR] [AGG_FILE]" >&2
  echo "  ROOT_DIR: Repo root (default: git root or current dir)" >&2
  echo "  DEST_DIR: Copy destination directory (default: ROOT_DIR/_ref_copy)" >&2
  echo "  AGG_FILE: Concatenated reference file (default: ROOT_DIR/_reference_all_files.txt)" >&2
}

if [[ ${1:-} == "-h" || ${1:-} == "--help" ]]; then
  print_usage
  exit 0
fi

ROOT_DIR=${1:-"$(git rev-parse --show-toplevel 2>/dev/null || pwd)"}
DEST_DIR=${2:-"$ROOT_DIR/_ref_copy"}
AGG_FILE=${3:-"$ROOT_DIR/_reference_all_files.txt"}

mkdir -p "$DEST_DIR"

timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "# Reference Dump" > "$AGG_FILE"
echo "# Generated: $timestamp" >> "$AGG_FILE"
echo "# Root: $ROOT_DIR" >> "$AGG_FILE"
echo >> "$AGG_FILE"

cd "$ROOT_DIR"

mapfile -t files < <(
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git ls-files
  else
    find . -type f \
      ! -path "./.git/*" \
      ! -path "./_ref_copy/*" \
      ! -name "_reference_all_files.txt"
  fi
)

is_text_file() {
  local file=$1
  if [[ ! -s "$file" ]]; then
    # empty files are fine
    return 0
  fi
  # grep -Iq exits 0 for text, 1 for binary
  if grep -Iq . "$file" 2>/dev/null; then
    return 0
  fi
  return 1
}

should_skip() {
  local file=$1
  # Skip our outputs and git internals
  if [[ "$file" == ".git"* ]]; then return 0; fi
  if [[ "$file" == "${DEST_DIR#$ROOT_DIR/}"* ]]; then return 0; fi
  if [[ "$ROOT_DIR/$file" == "$AGG_FILE" ]]; then return 0; fi
  if [[ "$file" == "_reference_all_files.txt" ]]; then return 0; fi
  if [[ "$file" == "_ref_copy"* ]]; then return 0; fi
  return 1
}

total=0
copied=0
concatenated=0
skipped_binary=0
skipped_large=0

for f in "${files[@]}"; do
  # Normalize path: drop leading ./ if present
  file=${f#./}
  if ! should_skip "$file"; then
    continue
  fi
  if [[ ! -f "$file" ]]; then
    continue
  fi
  total=$((total+1))

  # Copy preserving structure
  target="$DEST_DIR/$file"
  mkdir -p "$(dirname "$target")"
  cp -a "$file" "$target"
  copied=$((copied+1))

  # Skip very large files (> 1 MiB) from aggregation
  size_bytes=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file")
  if [[ "$size_bytes" -gt 1048576 ]]; then
    skipped_large=$((skipped_large+1))
    continue
  fi

  if ! is_text_file "$file"; then
    skipped_binary=$((skipped_binary+1))
    continue
  fi

  {
    echo "----- FILE: $file -----"
    cat "$file"
    echo
    echo "----- END FILE: $file -----"
    echo
  } >> "$AGG_FILE"
  concatenated=$((concatenated+1))
done

echo "Copied:        $copied" >> "$AGG_FILE"
echo "Concatenated:  $concatenated" >> "$AGG_FILE"
echo "SkippedBinary: $skipped_binary" >> "$AGG_FILE"
echo "SkippedLarge:  $skipped_large" >> "$AGG_FILE"

echo "Done. Copied $copied files to $DEST_DIR and concatenated $concatenated into $AGG_FILE" >&2

