import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.e2e
def test_e2e_users_cli(tmp_path):
    out_dir = tmp_path / "out"
    cmd = [sys.executable, "/workspace/data/pipelines/pipeline.py", "--dataset", "users", "--input", "/workspace/data/pipelines/samples/users.csv", "--output", str(out_dir)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0, res.stderr
    # stdout contains JSON summary
    summary = json.loads(res.stdout.strip())
    assert summary["dataset"] == "users"
    assert os.path.exists(summary["target"]) 
    assert os.path.exists(summary["lineage"]) 


@pytest.mark.e2e
def test_e2e_failure_writes_validation_report(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("user_id,email\n,invalid\n")
    out_dir = tmp_path / "out"
    cmd = [sys.executable, "/workspace/data/pipelines/pipeline.py", "--dataset", "users", "--input", str(bad), "--output", str(out_dir)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 1
    report = out_dir / "validation" / "users_report.json"
    assert report.exists()