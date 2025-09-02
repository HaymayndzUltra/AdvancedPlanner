#!/usr/bin/env bash
set -euo pipefail

# Usage: ./concat_all.sh [output_file]
# Concatenates repository text-like files into a single reference file with clear section headers.

OUT_FILE="${1:-/workspace/_ALL_FILES_REFERENCE.txt}"

# File globs to include (text-focused); skip binaries and large dirs
INCLUDE_GLOBS=(
  "**/*.md" "**/*.txt" "**/*.yaml" "**/*.yml" "**/*.json" "**/*.py" "**/*.sh" "**/*.ts" "**/*.tsx" "**/*.js" "**/*.css" "**/*.html"
)

# Exclusions
EXCLUDES=(
  ".git" "node_modules" "dist" "build" "tmp" "bin" "lib" "lib64" "usr" "proc" "sys" "dev" "var" "mnt" "media" "opt" "boot" "sbin" "run" "home" "root"
)

# Resolve to workspace root if run elsewhere
ROOT="/workspace"
cd "$ROOT"

# Prepare output
: > "$OUT_FILE"

echo "# Repository Combined Reference" >> "$OUT_FILE"
echo "# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$OUT_FILE"
echo >> "$OUT_FILE"

# Build find command
FIND_ARGS=( . )
for ex in "${EXCLUDES[@]}"; do
  FIND_ARGS+=( -path "./$ex" -prune -o )
done
FIND_ARGS+=( -type f \( )
for i in "${!INCLUDE_GLOBS[@]}"; do
  glob="${INCLUDE_GLOBS[$i]}"
  FIND_ARGS+=( -name "${glob##*/}" -o )
done
# remove trailing -o and close paren
unset FIND_ARGS[-1]
FIND_ARGS+=( \) -print )

# Collect files
mapfile -t FILES < <(find "${FIND_ARGS[@]}" -type f -print0 | xargs -0 -I{} realpath {} | sort | grep -v -F -- "$(realpath $OUT_FILE)")

for f in "${FILES[@]}"; do
  # Skip files larger than ~512KB to keep output reasonable
  if [ $(stat -c%s "$f") -gt 524288 ]; then
    echo -e "\n\n===== SKIPPED LARGE FILE: $f (>$((524288/1024))KB) =====" >> "$OUT_FILE"
    continue
  fi
  echo -e "\n\n===== BEGIN FILE: $f =====" >> "$OUT_FILE"
  # Attempt safe display; if binary, note and skip
  if command -v file >/dev/null 2>&1; then mime=$(file -b --mime-type "$f"); else mime=; fi; if echo "$mime" | grep -qiE "^text/|json|yaml"; then
    cat "$f" >> "$OUT_FILE"
  else
    # Fallback: try cat but guard
    if LC_ALL=C grep -qP "\x00" "$f" 2>/dev/null; then
      echo "[binary content omitted]" >> "$OUT_FILE"
    else
      cat "$f" >> "$OUT_FILE"
    fi
  fi
  echo -e "\n===== END FILE: $f =====" >> "$OUT_FILE"

done

echo "Wrote $OUT_FILE"
