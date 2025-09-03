#!/usr/bin/env bash
set -euo pipefail

# Usage: ./pack_reference.sh [ROOT_DIR] [OUTPUT_FILE]
# Defaults: ROOT_DIR=/workspace, OUTPUT_FILE=$ROOT_DIR/reference_all_files.txt

ROOT_DIR="${1:-/workspace}"
OUTPUT_FILE="${2:-$ROOT_DIR/reference_all_files.txt}"

# Ensure absolute path for OUTPUT_FILE
case "$OUTPUT_FILE" in
  /*) ;; # absolute
  *) OUTPUT_FILE="$ROOT_DIR/$OUTPUT_FILE" ;;
esac

# Exclude directories and large files; include only text-like files
# Adjust size threshold as needed
SIZE_MAX="5M"

tmp_list="$(mktemp)"
trap 'rm -f "$tmp_list"' EXIT

find "$ROOT_DIR" -type f \
  ! -path "$OUTPUT_FILE" \
  -not -path "$ROOT_DIR/.git/*" \
  -not -path "$ROOT_DIR/.venv/*" \
  -not -path "$ROOT_DIR/node_modules/*" \
  -not -path "$ROOT_DIR/__pycache__/*" \
  -not -path "$ROOT_DIR/.mypy_cache/*" \
  -not -path "$ROOT_DIR/.ruff_cache/*" \
  -not -path "$ROOT_DIR/.cache/*" \
  -size -$SIZE_MAX \
  -print | sort > "$tmp_list"

{
  echo "# Combined Reference File"
  echo "# Root: $ROOT_DIR"
  echo "# Generated: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  echo
} > "$OUTPUT_FILE"

while IFS= read -r file_path; do
  # Skip the output file itself if discovered
  [ "$file_path" = "$OUTPUT_FILE" ] && continue
  # Only include text files (best-effort)
  if grep -Iq . "$file_path"; then
    rel_path="${file_path#${ROOT_DIR}/}"
    printf '\n===== START: %s =====\n' "$rel_path" >> "$OUTPUT_FILE"
    cat "$file_path" >> "$OUTPUT_FILE" || true
    printf '\n===== END: %s =====\n' "$rel_path" >> "$OUTPUT_FILE"
  fi
done < "$tmp_list"

echo "Wrote $OUTPUT_FILE"
