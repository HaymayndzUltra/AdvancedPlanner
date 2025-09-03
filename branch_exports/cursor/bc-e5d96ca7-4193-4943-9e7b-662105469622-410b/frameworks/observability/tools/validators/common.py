from __future__ import annotations

import hashlib
import json
import os
from typing import Any, Dict

import yaml
from jsonschema import validate as jsonschema_validate, Draft7Validator


def read_yaml(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_schema(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_yaml_with_schema(yaml_path: str, schema_path: str) -> None:
    data = read_yaml(yaml_path)
    schema = load_schema(schema_path)
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    if errors:
        msgs = [f"{list(err.path)}: {err.message}" for err in errors]
        raise ValueError("; ".join(msgs))


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def normalize_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        content = f.read()
    # Normalize to LF endings
    content = content.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return content


def sha256_normalized(path: str) -> str:
    return f"sha256:{hashlib.sha256(normalize_bytes(path)).hexdigest()}"


def assert_required_tags(tag_list: list[str], required: list[str]) -> None:
    tag_keys = {t.split(":")[0] for t in tag_list if ":" in t}
    missing = [k for k in required if k not in tag_keys]
    if missing:
        raise ValueError(f"Missing required tags: {', '.join(missing)}")


def assert_critical_zero(tag_list: list[str]) -> None:
    for t in tag_list:
        if t.lower().startswith("critical:"):
            _, val = t.split(":", 1)
            if val.strip() not in {"0", "false", "no"}:
                raise ValueError("Critical must be 0 by default (Critical=0 policy)")
