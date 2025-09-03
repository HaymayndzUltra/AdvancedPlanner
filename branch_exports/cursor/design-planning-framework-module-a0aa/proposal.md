### 1) Executive Summary

This document defines a complete Planning Framework module for the frontend (planning-fe) with artifact-first interoperability and a deterministic event lifecycle. The framework privileges durable, portable artifacts (YAML/MD/JSON) to encode scope, intent, and evidence; enforces quality gates at lifecycle transitions; and produces an immutable, checksummed handoff manifest compliant with governance. Each planning cycle emits a digest capturing KPIs, gate outcomes, and improvement actions.

Lifecycle states: PLANNED → READY_FOR_HANDOFF → PACKAGED → EXECUTED → VALIDATED → IMPROVE. At each relevant transition, quality gates run: schema_lint, cross_stream_consistency, and parity/coverage. Handoffs are sealed via a manifest with checksums, a snapshot_rev, and a rulebook_hash. A governance overlay uses tags[] and enforces a Critical==0 rule. A metrics spine defines KPIs and produces a digest per cycle for traceability and review.


### 2) Deliverables (fe_task_breakdown.yaml, story_map.md, handoff_manifest.yaml, digest.md)

- fe_task_breakdown.yaml: Canonical FE task inventory for the cycle.
- story_map.md: User outcomes, journeys, and release slices for FE scope.
- handoff_manifest.yaml: Immutable manifest sealing a releasable unit.
- digest.md: Per-cycle metrics summary and decisions log.

Locations and naming:
- Proposal: `/reports/agent_reviews/planning-fe/<date>-proposal.md` (this doc)
- Digest: `/frameworks/planning-fe/digests/<date>-digest.md`
- Planning artifacts (suggested): `/frameworks/planning-fe/artifacts/<snapshot_rev>/...`

Artifact-first interop (YAML/MD/JSON):
- YAML for structured data (tasks, manifest) with explicit schemas.
- Markdown for narrative artifacts (story map, digest) with structured sections.
- JSON optionally mirrored for API/automation consumption.

Key field expectations:
- fe_task_breakdown.yaml entries: id, title, description, owner, tags[], priority, effort, status, dependencies[], acceptance_criteria[], risk, planned_in, linked_story_map_nodes[].
- handoff_manifest.yaml: manifest_id, sealed=true, created_at, created_by, snapshot_rev, rulebook_hash, artifact_checksums{path→sha256}, gate_results{schema_lint, cross_stream_consistency, parity_coverage}, governance{tags[], critical_violations, decision_log_ref}, prior_manifest_id(optional), notes.


### 3) Events & Gates

Lifecycle events:
- PLANNED: Scope defined; tasks and story map drafted.
- READY_FOR_HANDOFF: Scope frozen; gates pass; manifest prepared for sealing.
- PACKAGED: Artifacts packaged and checksummed; manifest sealed and published.
- EXECUTED: Work executed against the sealed plan; deviations recorded.
- VALIDATED: Outcomes measured; parity/coverage verified; acceptance criteria met.
- IMPROVE: Retrospective and improvements queued into the next PLANNED.

Quality gates (run at transitions as noted):
- schema_lint (PLANNED→READY_FOR_HANDOFF): All YAML/JSON conform to schemas; required fields set; IDs unique and resolvable.
- cross_stream_consistency (PLANNED→READY_FOR_HANDOFF): FE plan aligns with dependencies (e.g., BE, Design); no dangling contracts.
- parity/coverage (VALIDATED→IMPROVE): Planned vs executed parity; coverage thresholds met (e.g., % of planned tasks delivered, scope variance, test parity where applicable).

Exit criteria per transition:
- To enter READY_FOR_HANDOFF: schema_lint=pass, cross_stream_consistency=pass, governance Critical==0.
- To enter PACKAGED: immutable handoff_manifest.yaml created with checksums; signatures (if used) collected.
- To enter EXECUTED: packaging published; execution change log enabled; deviations tracked.
- To enter VALIDATED: execution completed; evidence attached; parity/coverage computed.
- To enter IMPROVE: validation complete; digest finalized; improvement items captured.


### 4) Workflow

1) Author artifacts (PLANNED)
- Draft story_map.md (outcomes, slices) and fe_task_breakdown.yaml (tasks).
- Assign owners, dependencies, and acceptance criteria. Tag risks and priorities.

2) Validate and freeze scope
- Run schema_lint on all YAML/JSON.
- Run cross_stream_consistency checks against upstream/downstream plans.
- Apply governance overlay; enforce Critical==0.

3) Prepare for handoff (READY_FOR_HANDOFF)
- Compute checksums (sha256) for every artifact referenced.
- Capture snapshot_rev (git SHA or semantic snapshot tag) and rulebook_hash (hash of the gate and governance ruleset).

4) Package and seal (PACKAGED)
- Assemble handoff_manifest.yaml with checksums, snapshot_rev, rulebook_hash, gate_results, governance fields, and sealed=true.
- Optionally sign manifest; publish to the repo location and/or artifact registry.

5) Execute (EXECUTED)
- Track deviations, scope changes, and exception approvals. Link back to tasks by id.

6) Validate (VALIDATED)
- Compute parity/coverage; verify acceptance criteria; mark validation status per task.

7) Improve (IMPROVE)
- Produce cycle digest.md (KPIs, deltas, decisions, follow-ups). File improvement backlog for next PLANNED.


### 5) Handoff & Sealing

- Immutability: handoff_manifest.yaml is immutable once sealed. Any changes require a new manifest_id and snapshot_rev with explicit linkage to the prior_manifest_id.
- Checksums: Use SHA-256 per artifact path; store as artifact_checksums{path→sha256}.
- Snapshot: snapshot_rev anchors the artifact set to a repository state (e.g., git commit SHA or tag).
- Rulebook: rulebook_hash is a stable hash of the ruleset for gates and governance; changes require recalculation.
- Publication: Store the sealed manifest alongside artifacts (e.g., `/frameworks/planning-fe/artifacts/<snapshot_rev>/handoff_manifest.yaml`) and reference it from the digest.


### 6) Governance Integration

- tags[] overlay: Every task and artifact supports free-form tags (e.g., Critical, Regulatory, Security, UX, Performance).
- Critical==0 rule: Requires zero critical violations to progress at any gate. Violations include missing acceptance criteria for Critical items, failing cross-stream contracts, or missing owners.
- Decision log: Governance outcomes and waivers recorded and referenced in handoff_manifest.yaml.governance.decision_log_ref and summarized in the digest.


### 7) Metrics & Digest

KPI spine (tracked per cycle and summarized in digest.md):
- Plan accuracy: delivered_vs_planned_ratio.
- On-time handoffs: percent of READY_FOR_HANDOFF by planned date.
- Cross-stream pass rate: cross_stream_consistency pass % at first run.
- Parity/coverage: % coverage vs target; variance of scope (+/-).
- Governance compliance: Critical violations count (must be 0), waivers used.
- Gate reliability: re-run rate to green; mean time to green.

Digest content:
- Metadata: cycle id/date, snapshot_rev, rulebook_hash, owners.
- Gate outcomes: pass/fail, evidence links.
- KPI table with targets vs actuals and deltas.
- Scope changes and deviations summary with references to tasks.
- Decisions, risks, and improvement actions queued.


### 8) Acceptance Criteria

- All four artifacts exist for the cycle: fe_task_breakdown.yaml, story_map.md, handoff_manifest.yaml, digest.md.
- Lifecycle transitions are recorded and only occur when gates pass.
- handoff_manifest.yaml is sealed, immutable, and includes checksums, snapshot_rev, rulebook_hash, gate results, and governance metadata.
- Governance Critical==0 enforced at all required gates; any waivers explicitly documented.
- Digest published with KPI spine and links to manifest and artifacts.
- Traceability: every task links to story map nodes and appears in at least one KPI.


### 9) Risks & Mitigations

- Risk: Schema drift — Mitigation: lock schemas via rulebook_hash, add schema versioning and CI enforcement.
- Risk: Cross-stream misalignment — Mitigation: automated contract checks; explicit dependency records and owners.
- Risk: Overhead/perceived bureaucracy — Mitigation: provide templates, pre-commit hooks, and fast linting to reduce friction.
- Risk: Incomplete evidence at validation — Mitigation: require acceptance_criteria and evidence refs before VALIDATED.
- Risk: Manifest tampering — Mitigation: checksums and optional signing; store manifests in write-once locations.


### 10) Timeline & Next Steps

- Day 0–1: Finalize schemas and rulebook; agree on KPI spine.
- Day 2–3: Author templates for fe_task_breakdown.yaml, story_map.md, handoff_manifest.yaml, and digest.md.
- Day 4: Wire CI checks (schema_lint, cross_stream_consistency) and governance overlay.
- Day 5: Dry-run a cycle; seal a sample manifest; publish the first digest.
- Week 2: Pilot on one product slice; refine based on IMPROVE feedback; roll out broadly.

---
Owner: Planning Engineering (FE)
Date: 2025-09-02
Scope: planning-fe