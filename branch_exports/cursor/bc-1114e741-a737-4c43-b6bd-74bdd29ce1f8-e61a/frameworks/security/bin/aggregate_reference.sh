#!/usr/bin/env bash
set -euo pipefail

OUT="/workspace/frameworks/security/reference/created-files-reference.md"
mkdir -p "$(dirname "$OUT")"

cat > "$OUT" << 'EOF'
# Created Files Reference

This file aggregates the contents of all files created/updated in this session for reference.

EOF

append_file() {
  local label="$1"
  local path="$2"
  if [[ -f "$path" ]]; then
    echo -e "\n---\n\n## ${label}\n\nPath: ${path}\n" >> "$OUT"
    echo '\`\`\`' >> "$OUT"
    cat "$path" >> "$OUT"
    echo -e '\n\`\`\`' >> "$OUT"
  fi
}

append_file "requirements.txt" "/workspace/requirements.txt"
append_file "Tags Taxonomy" "/workspace/frameworks/security/config/tags.md"
append_file "Streams Registry" "/workspace/frameworks/security/config/streams.md"
append_file "Schema: sec_findings" "/workspace/frameworks/security/schemas/sec_findings.schema.json"
append_file "Schema: policy_map" "/workspace/frameworks/security/schemas/policy_map.schema.json"
append_file "Schema: exceptions" "/workspace/frameworks/security/schemas/exceptions.schema.json"
append_file "Schema: handoff_manifest" "/workspace/frameworks/security/schemas/handoff_manifest.schema.json"
append_file "Schema: digest" "/workspace/frameworks/security/schemas/digest.schema.json"
append_file "Template: policy_map.md" "/workspace/frameworks/security/policy/policy_map.md"
append_file "Template: exceptions.md" "/workspace/frameworks/security/policy/exceptions.md"
append_file "Artifact: sec_findings.yaml (2025-09)" "/workspace/frameworks/security/artifacts/2025-09/sec_findings.yaml"
append_file "Manifest: handoff_manifest.yaml (2025-09)" "/workspace/frameworks/security/manifests/2025-09/handoff_manifest.yaml"
append_file "Digest: 2025-09-02" "/workspace/frameworks/security/digests/2025-09-02-digest.md"
append_file "CLI: security_framework.py" "/workspace/frameworks/security/bin/security_framework.py"
append_file "CI: security-framework.yml" "/workspace/.github/workflows/security-framework.yml"

printf "\n\nDone. Wrote %s\n" "$OUT"