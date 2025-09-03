#!/usr/bin/env python3
import sys

def read_code(path: str) -> int:
    try:
        return int(open(path).read().strip())
    except Exception:
        return 1

first = read_code("ci/reports/first_status.code")
second = read_code("ci/reports/second_status.code")

if first != 0 or second != 0:
    print(f"Tests failed: first={first} second={second}", file=sys.stderr)
    sys.exit(1)

print("Tests: PASS")
sys.exit(0)