import csv
import json
import os

import pytest

from data.pipelines.pipeline import run_pipeline, infer_target_path


def test_users_pipeline_writes_masked_users(tmp_output_dir, samples_dir):
    code = run_pipeline("users", os.path.join(samples_dir, "users.csv"), tmp_output_dir)
    assert code == 0
    target = infer_target_path("users", tmp_output_dir)
    assert os.path.exists(target)
    rows = list(csv.DictReader(open(target)))
    assert rows
    for r in rows:
        assert r["email"].endswith("@redacted.local")
        assert r["phone_number"] == ""
        assert r["full_name"].endswith("***")


def test_session_events_pipeline_anonymizes_ip(tmp_output_dir, samples_dir):
    code = run_pipeline("session_events", os.path.join(samples_dir, "session_events.csv"), tmp_output_dir)
    assert code == 0
    target = infer_target_path("session_events", tmp_output_dir)
    rows = list(csv.DictReader(open(target)))
    assert rows
    for r in rows:
        ip = r["ip_address"]
        assert ip == "192.168.0.0" or ip.endswith("::")


def test_transactions_pipeline_tokenizes_last4(tmp_output_dir, samples_dir):
    code = run_pipeline("transactions", os.path.join(samples_dir, "transactions.csv"), tmp_output_dir)
    assert code == 0
    target = infer_target_path("transactions", tmp_output_dir)
    rows = list(csv.DictReader(open(target)))
    assert rows
    for r in rows:
        assert r.get("card_last4", "") == ""
        assert "card_last4_token" in r and r["card_last4_token"].startswith("tok_")


@pytest.mark.integration
def test_validation_error_produces_report(tmp_output_dir, tmp_path):
    invalid_csv = tmp_path / "bad_users.csv"
    invalid_csv.write_text("user_id,email\n,not-an-email\n")
    code = run_pipeline("users", str(invalid_csv), tmp_output_dir)
    assert code == 1
    report = os.path.join(tmp_output_dir, "validation", "users_report.json")
    assert os.path.exists(report)
    data = json.load(open(report))
    assert data["error_count"] > 0