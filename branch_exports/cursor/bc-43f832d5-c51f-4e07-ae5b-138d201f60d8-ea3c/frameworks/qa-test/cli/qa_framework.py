#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

try:
	import yaml
except ImportError:
	print("PyYAML not installed. Please run: pip install pyyaml jsonschema", file=sys.stderr)
	raise

try:
	from jsonschema import validate, Draft202012Validator
except ImportError:
	print("jsonschema not installed. Please run: pip install jsonschema", file=sys.stderr)
	raise

# Determine repository root (parent of 'frameworks')
REPO_ROOT = Path(__file__).resolve().parents[3]
QA_ROOT = REPO_ROOT / "frameworks/qa-test"
SCHEMAS = QA_ROOT / "schemas"
ARTIFACTS_ROOT = QA_ROOT / "artifacts"
RULEBOOK = QA_ROOT / "rules/rulebook.yaml"


def load_yaml(path: Path):
	with open(path, "r", encoding="utf-8") as f:
		return yaml.safe_load(f)


def load_json_schema(name: str):
	with open(SCHEMAS / name, "r", encoding="utf-8") as f:
		return json.load(f)


def sha256_file(path: Path) -> str:
	sha = hashlib.sha256()
	with open(path, "rb") as f:
		for chunk in iter(lambda: f.read(8192), b""):
			sha.update(chunk)
	return sha.hexdigest()


def schema_lint(artifacts_dir: Path) -> bool:
	ok = True
	# test_matrix.yaml
	tm_path = artifacts_dir / "test_matrix.yaml"
	if tm_path.exists():
		try:
			schema = load_json_schema("test_matrix.schema.json")
			Draft202012Validator(schema).validate(load_yaml(tm_path))
			print(f"schema_lint: OK {tm_path}")
		except Exception as e:
			print(f"schema_lint: FAIL {tm_path}: {e}")
			ok = False
	# handoff manifest checked at sealing time
	# qa_evidence_index.yaml
	ei_path = artifacts_dir / "qa_evidence_index.yaml"
	if ei_path.exists():
		try:
			schema = load_json_schema("qa_evidence_index.schema.json")
			Draft202012Validator(schema).validate(load_yaml(ei_path))
			print(f"schema_lint: OK {ei_path}")
		except Exception as e:
			print(f"schema_lint: FAIL {ei_path}: {e}")
			ok = False
	# compliance_map.md not strictly YAML; skip strict schema
	return ok


def cross_stream_consistency(planning_fe: Path, planning_be: Path, artifacts_dir: Path) -> bool:
	"""Ensure story_ref and endpoint_ref referenced in test_matrix exist in planning docs."""
	ok = True
	fe = load_yaml(planning_fe) if planning_fe.exists() else {"backlog": []}
	be = load_yaml(planning_be) if planning_be.exists() else {"backlog": []}
	fe_ids = {item.get("id") for item in fe.get("backlog", [])}
	be_endpoints = set()
	for item in be.get("backlog", []):
		for ep in item.get("endpoints", []) or []:
			be_endpoints.add(ep.get("id"))

	tm = load_yaml(artifacts_dir / "test_matrix.yaml")
	for m in tm.get("mappings", []):
		story = m.get("story_ref")
		endpoint = m.get("endpoint_ref")
		if story and story not in fe_ids:
			print(f"consistency: FAIL unknown story_ref {story}")
			ok = False
		if endpoint and endpoint not in be_endpoints:
			print(f"consistency: FAIL unknown endpoint_ref {endpoint}")
			ok = False
	return ok


def compute_parity_coverage(planning_fe: Path, artifacts_dir: Path, parity_threshold: float) -> tuple[bool, float]:
	fe = load_yaml(planning_fe) if planning_fe.exists() else {"backlog": []}
	planned = [i for i in fe.get("backlog", []) if "critical_path" in (i.get("tags") or [])]
	planned_ids = {i.get("id") for i in planned}
	tm = load_yaml(artifacts_dir / "test_matrix.yaml")
	mapped_ids = {m.get("story_ref") for m in tm.get("mappings", [])}
	mapped_critical = planned_ids & mapped_ids
	parity = (len(mapped_critical) / len(planned_ids)) if planned_ids else 1.0
	return parity >= parity_threshold, parity * 100.0


def seal_manifest(cycle: str, artifacts_dir: Path, out_path: Path, parity_pct: float, gates: dict):
	rulebook_hash = hashlib.sha256((RULEBOOK.read_text(encoding="utf-8")).encode("utf-8")).hexdigest()
	artifact_entries = []
	for rel in [
		"test_matrix.yaml",
		"traceability_map.md",
		"qa_evidence_index.yaml",
		"compliance_map.md",
		"policy_exceptions.md",
		"integration_hooks.md",
		"qa_risk_register.md",
	]:
		p = artifacts_dir / rel
		if p.exists():
			artifact_entries.append({
				"name": Path(rel).stem,
				"path": str(p.relative_to(REPO_ROOT)),
				"sha256": sha256_file(p)
			})

	manifest = {
		"manifest_version": 1,
		"cycle": cycle,
		"snapshot_rev": load_yaml(artifacts_dir / "test_matrix.yaml").get("snapshot_rev"),
		"rulebook_hash": f"sha256:{rulebook_hash}",
		"sealed": True,
		"artifacts": artifact_entries,
		"quality_gates": {
			"schema_lint": "pass" if gates.get("schema_lint") else "fail",
			"cross_stream_consistency": "pass" if gates.get("consistency") else "fail",
			"parity_coverage": {
				"status": "pass" if gates.get("parity") else "fail",
				"coverage_pct": round(parity_pct, 2)
			}
		}
	}
	with open(out_path, "w", encoding="utf-8") as f:
		yaml.safe_dump(manifest, f, sort_keys=False)
	print(f"sealed manifest: {out_path}")


def main():
	parser = argparse.ArgumentParser(description="QA Framework CLI")
	parser.add_argument("command", choices=["lint", "gates", "seal", "all"], help="Action to perform")
	parser.add_argument("--cycle", dest="cycle", default="2025-09")
	args = parser.parse_args()

	artifacts_dir = ARTIFACTS_ROOT / args.cycle
	planning_fe = REPO_ROOT / "frameworks/planning-fe/tasks/2025-09-02-fe_task_breakdown.yaml"
	planning_be = REPO_ROOT / "frameworks/planning-be/backlog/2025-09-02-be_backlog.yaml"
	rulebook = load_yaml(RULEBOOK)
	parity_threshold = float(rulebook.get("policy", {}).get("parity_threshold", 0.9))

	if args.command in ("lint", "all"):
		ok = schema_lint(artifacts_dir)
		if args.command == "lint":
			return 0 if ok else 1

	if args.command in ("gates", "all"):
		ok_lint = schema_lint(artifacts_dir)
		ok_consistency = cross_stream_consistency(planning_fe, planning_be, artifacts_dir)
		ok_parity, parity_pct = compute_parity_coverage(planning_fe, artifacts_dir, parity_threshold)
		print(f"gates: schema_lint={ok_lint}, consistency={ok_consistency}, parity>={parity_threshold} => {ok_parity} ({parity_pct:.1f}%)")
		if args.command == "gates":
			return 0 if (ok_lint and ok_consistency and ok_parity) else 2

	if args.command in ("seal", "all"):
		ok_lint = schema_lint(artifacts_dir)
		ok_consistency = cross_stream_consistency(planning_fe, planning_be, artifacts_dir)
		ok_parity, parity_pct = compute_parity_coverage(planning_fe, artifacts_dir, parity_threshold)
		gates = {"schema_lint": ok_lint, "consistency": ok_consistency, "parity": ok_parity}
		out_path = artifacts_dir / "handoff_manifest.yaml"
		seal_manifest(args.cycle, artifacts_dir, out_path, parity_pct, gates)
		# Validate manifest against schema
		schema = load_json_schema("handoff_manifest.schema.json")
		Draft202012Validator(schema).validate(load_yaml(out_path))
		print("manifest schema: OK")
		return 0 if all(gates.values()) else 3

	return 0


if __name__ == "__main__":
	sys.exit(main())