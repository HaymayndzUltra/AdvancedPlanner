#!/usr/bin/env bash
set -euo pipefail

bash ci/run_tests.sh

python3 ci/test_gate.py
python3 ci/contract_gate.py
python3 ci/flake_gate.py

echo "CI checks completed successfully."