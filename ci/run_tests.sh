#!/usr/bin/env bash
set -euo pipefail

VENV=.venv
PYTHON=python3

# Ensure user base bin is on PATH for user installations
export PATH="$HOME/.local/bin:$PATH"

# Try to create a virtualenv; if it fails, continue without it
if ! $PYTHON -m venv "$VENV" >/dev/null 2>&1; then
  echo "Warning: venv unavailable. Proceeding without virtualenv." >&2
  USE_VENV=0
else
  USE_VENV=1
fi

if [[ ${USE_VENV:-0} -eq 1 ]]; then
  source "$VENV/bin/activate"
  PYCMD=python
  PIP_ARGS=""
else
  PYCMD=$PYTHON
  # Allow installing into system-managed env for CI container
  PIP_ARGS="--break-system-packages --user"
fi

$PYCMD -m pip install -U pip $PIP_ARGS

# Helper to install requirements if any of the candidate paths exist
install_if_exists() {
  local label="$1"; shift
  for candidate in "$@"; do
    if [[ -f "$candidate" ]]; then
      echo "Installing $label from $candidate"
      $PYCMD -m pip install -r "$candidate" $PIP_ARGS
      return 0
    fi
  done
  echo "Note: none of the $label files found; skipping: $*" >&2
  return 0
}

# Install optional data/pipelines requirements if present (F5)
install_if_exists "pipelines requirements" \
  data/pipelines/requirements.txt \
  /workspace/data/pipelines/requirements.txt

# Project/dev requirements (optional)
install_if_exists "dev requirements" \
  requirements-dev.txt \
  /workspace/requirements-dev.txt

mkdir -p ci/reports

# First run (produces coverage.xml and junit.xml via pytest addopts)
first_status=0
pytest -q || first_status=$?
echo "$first_status" > ci/reports/first_status.code

# Second run for flakiness detection
second_status=0
pytest -q --junitxml=ci/reports/junit_second.xml || second_status=$?
echo "$second_status" > ci/reports/second_status.code

# Verify coverage xml exists
if [[ ! -f ci/reports/coverage.xml ]]; then
  echo "Coverage report missing after pytest." >&2
fi

# Note: Final result evaluated by gates
exit 0