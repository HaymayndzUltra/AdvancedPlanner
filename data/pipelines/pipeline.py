#!/usr/bin/env python3
import argparse
import csv
import hashlib
import ipaddress
import json
import os
import re
import sys
from datetime import datetime, timezone

try:
    import yaml  # type: ignore
except Exception as exc:  # pragma: no cover
    print("Missing dependency: pyyaml. Install with: pip install -r data/pipelines/requirements.txt", file=sys.stderr)
    raise


SCHEMA_FILES = {
    "users": "/workspace/docs/data/schemas/users.yaml",
    "session_events": "/workspace/docs/data/schemas/session_events.yaml",
    "transactions": "/workspace/docs/data/schemas/transactions.yaml",
}


def read_yaml_file(yaml_path: str) -> dict:
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def read_csv_records(input_path: str) -> list[dict]:
    with open(input_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def write_csv_records(records: list[dict], output_path: str) -> None:
    if not records:
        raise ValueError("No records to write")
    fieldnames = list(records[0].keys())
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rec in records:
            writer.writerow(rec)


def mask_email(email: str) -> str:
    if not email:
        return email
    parts = email.split("@")
    if len(parts) != 2:
        return "***@redacted"
    local, domain = parts
    masked_local = (local[0] + "***") if local else "***"
    return f"{masked_local}@{domain}"


def mask_phone(phone: str) -> str:
    if not phone:
        return phone
    digits = re.sub(r"\D", "", phone)
    tail = digits[-2:] if len(digits) >= 2 else "**"
    return f"+**{tail}"


def anonymize_ip(ip: str) -> str:
    if not ip:
        return ip
    try:
        ip_obj = ipaddress.ip_address(ip)
        if isinstance(ip_obj, ipaddress.IPv4Address):
            parts = ip.split(".")
            return f"{parts[0]}.{parts[1]}.0.0"
        # IPv6: zero the last 64 bits
        network = ipaddress.IPv6Network(ip + "/64", strict=False)
        return str(network.network_address)
    except Exception:
        return "0.0.0.0"


def tokenize_last4(last4: str) -> str:
    if not last4:
        return last4
    token = hashlib.sha256(last4.encode("utf-8")).hexdigest()[:8]
    return f"tok_{token}"


def build_field_constraints(field_spec: dict) -> dict:
    constraints: dict = {
        "unique": False,
        "enum": None,
        "format": None,
        "regex": None,
        "min": None,
        "max": None,
    }
    for item in field_spec.get("constraints", []) or []:
        if isinstance(item, str) and item == "unique":
            constraints["unique"] = True
        elif isinstance(item, dict):
            for k, v in item.items():
                constraints[k] = v
    return constraints


def validate_records(dataset: str, schema: dict, records: list[dict]) -> dict:
    errors: list[dict] = []
    warnings: list[dict] = []
    field_specs = {f["name"]: f for f in schema.get("fields", [])}

    # Unique checks setup
    unique_fields = [n for n, spec in field_specs.items() if build_field_constraints(spec).get("unique")]
    seen_sets = {name: set() for name in unique_fields}

    # Precompile regex patterns
    email_re = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    e164_re = re.compile(r"^\+?[1-9]\d{1,14}$")
    ipv4_re = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")
    ipv6_re = re.compile(r"^[0-9a-fA-F:]+$")

    for idx, rec in enumerate(records):
        # Required fields
        for name, spec in field_specs.items():
            if not spec.get("nullable", False):
                if name not in rec or rec[name] in (None, ""):
                    errors.append({"row": idx, "field": name, "error": "required_field_missing"})

        # Field-level constraints
        for name, spec in field_specs.items():
            value = rec.get(name)
            constraints = build_field_constraints(spec)

            # Unique
            if constraints.get("unique"):
                key = (value or "__NULL__")
                if key in seen_sets[name]:
                    errors.append({"row": idx, "field": name, "error": "duplicate_value"})
                else:
                    seen_sets[name].add(key)

            # Enum
            enum_values = constraints.get("enum")
            if enum_values is not None and value not in (enum_values or []):
                # Allow empty if nullable
                if not (spec.get("nullable", False) and (value is None or value == "")):
                    errors.append({"row": idx, "field": name, "error": "enum_violation", "allowed": enum_values})

            # Format
            fmt = constraints.get("format")
            if fmt and value not in (None, ""):
                if fmt == "email" and not email_re.match(str(value)):
                    errors.append({"row": idx, "field": name, "error": "invalid_email"})
                if fmt == "e164" and not e164_re.match(str(value)):
                    errors.append({"row": idx, "field": name, "error": "invalid_e164"})
                if fmt == "ipv4_or_ipv6" and not (ipv4_re.match(str(value)) or ipv6_re.match(str(value))):
                    errors.append({"row": idx, "field": name, "error": "invalid_ip"})

            # Regex pattern
            regex_pattern = constraints.get("regex")
            if regex_pattern and value not in (None, ""):
                if not re.match(regex_pattern, str(value)):
                    errors.append({"row": idx, "field": name, "error": "regex_mismatch"})

            # Numeric min/max
            if spec.get("type") in ("integer", "decimal", "number") and value not in (None, ""):
                try:
                    numeric = float(value)
                    min_v = constraints.get("min")
                    max_v = constraints.get("max")
                    if min_v is not None and numeric < float(min_v):
                        errors.append({"row": idx, "field": name, "error": "below_min", "min": min_v})
                    if max_v is not None and numeric > float(max_v):
                        errors.append({"row": idx, "field": name, "error": "above_max", "max": max_v})
                except Exception:
                    errors.append({"row": idx, "field": name, "error": "not_numeric"})

    return {
        "errors": errors,
        "warnings": warnings,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "row_count": len(records),
    }


def apply_privacy_controls(dataset: str, records: list[dict]) -> list[dict]:
    protected: list[dict] = []
    for rec in records:
        new_rec = dict(rec)
        if dataset == "users":
            if "email" in new_rec and new_rec["email"]:
                new_rec["email"] = mask_email(new_rec.get("email", ""))
            if "full_name" in new_rec and new_rec["full_name"]:
                new_rec["full_name"] = new_rec["full_name"][0] + "***"
            if "phone_number" in new_rec and new_rec["phone_number"]:
                new_rec["phone_number"] = ""
        elif dataset == "session_events":
            if "ip_address" in new_rec and new_rec["ip_address"]:
                new_rec["ip_address"] = anonymize_ip(new_rec.get("ip_address", ""))
        elif dataset == "transactions":
            if "card_last4" in new_rec and new_rec["card_last4"]:
                new_rec["card_last4_token"] = tokenize_last4(new_rec["card_last4"])
                new_rec["card_last4"] = ""
        protected.append(new_rec)
    return protected


def emit_lineage(dataset: str, source: str, target: str, validation_report: dict, output_dir: str) -> str:
    lineage_record = {
        "dataset": dataset,
        "source": source,
        "target": target,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "validation": {
            "row_count": validation_report.get("row_count"),
            "error_count": validation_report.get("error_count"),
            "warning_count": validation_report.get("warning_count"),
        },
    }
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{dataset}-{int(datetime.now().timestamp())}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(lineage_record, f, indent=2)
    return out_path


def infer_target_path(dataset: str, output_dir: str) -> str:
    base = os.path.join(output_dir, "warehouse")
    os.makedirs(base, exist_ok=True)
    if dataset == "users":
        return os.path.join(base, "dim_users.csv")
    if dataset == "session_events":
        return os.path.join(base, "fact_session_events.csv")
    if dataset == "transactions":
        return os.path.join(base, "fact_transactions.csv")
    raise ValueError(f"Unknown dataset: {dataset}")


def run_pipeline(dataset: str, input_path: str, output_dir: str) -> int:
    if dataset not in SCHEMA_FILES:
        print(f"Unsupported dataset: {dataset}", file=sys.stderr)
        return 2

    schema_path = SCHEMA_FILES[dataset]
    if not os.path.exists(schema_path):
        print(f"Schema file not found: {schema_path}", file=sys.stderr)
        return 2

    schema = read_yaml_file(schema_path)
    records = read_csv_records(input_path)
    protected_records = apply_privacy_controls(dataset, records)
    validation_report = validate_records(dataset, schema, protected_records)

    # Fail on validation errors for strict reproducibility
    if validation_report["error_count"] > 0:
        report_dir = os.path.join(output_dir, "validation")
        os.makedirs(report_dir, exist_ok=True)
        with open(os.path.join(report_dir, f"{dataset}_report.json"), "w", encoding="utf-8") as f:
            json.dump(validation_report, f, indent=2)
        print(f"Validation failed with {validation_report['error_count']} errors. See report.", file=sys.stderr)
        return 1

    target_path = infer_target_path(dataset, output_dir)
    write_csv_records(protected_records, target_path)

    lineage_dir = os.path.join(output_dir, "lineage")
    lineage_path = emit_lineage(dataset, input_path, target_path, validation_report, lineage_dir)

    print(json.dumps({
        "dataset": dataset,
        "rows": validation_report.get("row_count"),
        "target": target_path,
        "lineage": lineage_path,
    }))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run ETL pipeline for a canonical dataset")
    parser.add_argument("--dataset", required=True, choices=list(SCHEMA_FILES.keys()))
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--output", required=True, help="Output directory root")
    args = parser.parse_args()
    return run_pipeline(args.dataset, args.input, args.output)


if __name__ == "__main__":
    sys.exit(main())

