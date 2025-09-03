#!/usr/bin/env python3
import sys
import os
import xml.etree.ElementTree as ET

FIRST = "ci/reports/junit.xml"
SECOND = "ci/reports/junit_second.xml"
THRESHOLD = 0.02


def read_suite(path: str):
    if not os.path.exists(path):
        return {}
    root = ET.parse(path).getroot()
    cases = {}
    for tc in root.iter("testcase"):
        name = f"{tc.get('classname','')}.{tc.get('name','')}"
        failed = tc.find("failure") is not None or tc.find("error") is not None
        cases[name] = failed
    return cases


def main() -> int:
    first = read_suite(FIRST)
    second = read_suite(SECOND)
    if not first or not second:
        print("JUnit files missing; skipping flake gate.")
        return 0
    keys = set(first) | set(second)
    flip = sum(1 for k in keys if first.get(k, False) != second.get(k, False))
    rate = flip / max(1, len(keys))
    if rate >= THRESHOLD:
        print(f"Flake rate {rate:.2%} >= threshold {THRESHOLD:.2%}", file=sys.stderr)
        return 1
    print(f"Flake rate {rate:.2%} OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())