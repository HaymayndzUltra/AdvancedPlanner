#!/usr/bin/env bash
set -euo pipefail

# Determine repo root
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
OUT_FILE="$REPO_ROOT/frameworks/qa-test/QA_REFERENCE_BUNDLE.md"
TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

guess_lang() {
  case "$1" in
    *.json) echo "json" ;;
    *.yaml|*.yml) echo "yaml" ;;
    *.md) echo "markdown" ;;
    *.py) echo "python" ;;
    Makefile) echo "makefile" ;;
    *.sh) echo "bash" ;;
    *) echo "" ;;
  esac
}

sha256_of() {
  local path="$1"
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$path" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$path" | awk '{print $1}'
  else
    echo "(sha256 unavailable)"
  fi
}

write_section() {
  local relpath="$1"
  local lang="$2"
  local fullpath="$REPO_ROOT/$relpath"
  echo -e "\n---\n" >> "$OUT_FILE"
  echo "### $relpath" >> "$OUT_FILE"
  if [[ -f "$fullpath" ]]; then
    local sum
    sum="$(sha256_of "$fullpath")"
    echo "Checksum (sha256): \`$sum\`" >> "$OUT_FILE"
    echo >> "$OUT_FILE"
    echo "\`\`\`$lang" >> "$OUT_FILE"
    cat "$fullpath" >> "$OUT_FILE"
    echo >> "$OUT_FILE"
    echo "\`\`\`" >> "$OUT_FILE"
  else
    echo >> "$OUT_FILE"
    echo "_Missing file at generation time._" >> "$OUT_FILE"
  fi
}

main() {
  mkdir -p "$(dirname "$OUT_FILE")"
  cat > "$OUT_FILE" <<EOF
# QA Reference Bundle

- Generated: $TIMESTAMP (UTC)
- Repo root: $REPO_ROOT

This bundle consolidates the QA framework files for quick reference.
EOF

  # Files to include (relative to repo root)
  files=(
    "frameworks/qa-test/schemas/test_matrix.schema.json"
    "frameworks/qa-test/schemas/handoff_manifest.schema.json"
    "frameworks/qa-test/schemas/qa_evidence_index.schema.json"

    "frameworks/qa-test/templates/test_matrix.yaml"
    "frameworks/qa-test/templates/handoff_manifest.yaml"
    "frameworks/qa-test/templates/qa_evidence_index.yaml"

    "frameworks/qa-test/artifacts/2025-09/test_matrix.yaml"
    "frameworks/qa-test/artifacts/2025-09/qa_evidence_index.yaml"
    "frameworks/qa-test/artifacts/2025-09/traceability_map.md"
    "frameworks/qa-test/artifacts/2025-09/compliance_map.md"
    "frameworks/qa-test/artifacts/2025-09/policy_exceptions.md"
    "frameworks/qa-test/artifacts/2025-09/qa_risk_register.md"

    "frameworks/qa-test/integration/integration_hooks.md"
    "frameworks/qa-test/tools/qa_cli.py"
    "frameworks/qa-test/tools/requirements.txt"

    "frameworks/qa-test/manifests/2025-09/handoff_manifest.yaml"
    "frameworks/qa-test/digests/2025-09-02-digest.md"

    "Makefile"
    ".github/workflows/qa.yml"
  )

  for f in "${files[@]}"; do
    write_section "$f" "$(guess_lang "$f")"
  done

  echo "\n---\n\nGenerated bundle at: $OUT_FILE" >> "$OUT_FILE"
  echo "Wrote $OUT_FILE"
}

main "$@"

