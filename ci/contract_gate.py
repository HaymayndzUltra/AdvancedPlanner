#!/usr/bin/env python3
import json
import os
import sys
import yaml

CONTRACTS = [
    ("users", "/workspace/docs/data/schemas/users.yaml"),
    ("session_events", "/workspace/docs/data/schemas/session_events.yaml"),
    ("transactions", "/workspace/docs/data/schemas/transactions.yaml"),
]


def check_schema_presence() -> list[str]:
    missing = []
    for name, path in CONTRACTS:
        if not os.path.exists(path):
            missing.append(f"Missing schema for {name}: {path}")
    return missing


def check_coverage_threshold(cov_xml_path: str, min_rate: float) -> list[str]:
    # naive parse: read 'line-rate' attribute if present, else skip
    if not os.path.exists(cov_xml_path):
        return [f"Coverage report not found: {cov_xml_path}"]
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse(cov_xml_path)
        root = tree.getroot()
        rate = float(root.attrib.get("line-rate", 0.0))
        if rate < min_rate:
            return [f"Coverage {rate:.2%} < required {min_rate:.2%}"]
    except Exception as exc:
        return [f"Failed to parse coverage XML: {exc}"]
    return []


def main() -> int:
    failures: list[str] = []
    failures += check_schema_presence()
    failures += check_coverage_threshold("ci/reports/coverage.xml", 0.80)
    if failures:
        print("\nCI Contract Gate Failures:\n" + "\n".join(f" - {m}" for m in failures), file=sys.stderr)
        return 1
    print("CI Contract Gate: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())