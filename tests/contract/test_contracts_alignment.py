import os
import re
import yaml
import pytest

CONTRACTS_DIR = "/workspace/docs/data/contracts"
SCHEMAS_DIR = "/workspace/docs/data/schemas"


def _load_contract(path: str) -> dict:
    # Contract front matter is YAML between --- lines
    content = open(path, encoding="utf-8").read()
    if content.startswith("---"):
        fm, _, rest = content[3:].partition("---")
        data = yaml.safe_load(fm)
        return data or {}
    return {}


def _has_unique(field_spec: dict) -> bool:
    constraints = field_spec.get("constraints") or []
    # Allow either string 'unique' or dict {unique: true}
    if any(item == "unique" for item in constraints):
        return True
    return any(isinstance(item, dict) and item.get("unique") for item in constraints)


def test_users_contract_has_schema_and_dq_alignment():
    c = _load_contract(os.path.join(CONTRACTS_DIR, "users.md"))
    assert c.get("schema_ref"), "users contract missing schema_ref"
    schema_path = "/workspace/docs/data/schemas/users.yaml"
    schema = yaml.safe_load(open(schema_path))
    fields = {f["name"]: f for f in schema["fields"]}
    assert fields["user_id"]["nullable"] is False
    assert fields["email"]["nullable"] is False
    assert _has_unique(fields["user_id"]) and _has_unique(fields["email"]) 


def test_session_events_contract_enum_covered_by_schema():
    c = _load_contract(os.path.join(CONTRACTS_DIR, "session_events.md"))
    assert c.get("schema_ref")
    schema = yaml.safe_load(open(os.path.join(SCHEMAS_DIR, "session_events.yaml")))
    event_type = [f for f in schema["fields"] if f["name"] == "event_type"][0]
    enums = None
    for item in event_type.get("constraints", []) or []:
        if isinstance(item, dict) and "enum" in item:
            enums = item["enum"]
    assert enums and set(enums) >= set(["session_start", "session_end", "page_view", "click", "purchase", "login", "logout", "error"]) 


def test_transactions_contract_enums_present():
    schema = yaml.safe_load(open(os.path.join(SCHEMAS_DIR, "transactions.yaml")))
    fields = {f["name"]: f for f in schema["fields"]}
    currency = fields["currency"]["constraints"][0]["enum"]
    status = fields["status"]["constraints"][0]["enum"]
    assert set(["USD","EUR","GBP","CAD","AUD","INR","JPY","BRL","MXN"]).issubset(set(currency))
    assert set(["authorized","captured","settled","refunded","voided","chargeback","failed"]).issubset(set(status))