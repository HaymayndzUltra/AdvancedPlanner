#!/usr/bin/env bash
set -euo pipefail

mkdir -p security/sbom
OUT="security/sbom/sbom.spdx.json"

if command -v syft >/dev/null 2>&1; then
  syft dir:. -o spdx-json > "$OUT"
  echo "SBOM written to $OUT using syft"
  exit 0
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required to generate a fallback SBOM" >&2
  exit 1
fi

python3 - << 'PY'
import os, subprocess, sys
out = os.environ.get('OUT', 'security/sbom/sbom.spdx.json')
req = 'data/pipelines/requirements.txt'
try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--disable-pip-version-check', 'cyclonedx-bom'])
    subprocess.check_call([sys.executable, '-m', 'cyclonedx_py', '-r', req, '-o', out, '-e', 'spdx-json'])
    print(f"SBOM written to {out} using cyclonedx-bom (requirements only)")
except Exception as exc:
    print(f"Failed to generate SBOM: {exc}", file=sys.stderr)
    sys.exit(1)
PY