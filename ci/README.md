### CI Overview

- ci/run_tests.sh: installs deps, runs pytest twice, produces coverage and JUnit reports
- ci/contract_gate.py: enforces schema presence and coverage >= 80%
- ci/flake_gate.py: computes flake rate from two JUnit runs, enforces < 2%
- ci/run_ci.sh: orchestrates the above

Artifacts are stored under ci/reports/ and uploaded by GitHub Actions.