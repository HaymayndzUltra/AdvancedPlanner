# TASK CHECKLIST (Derived from Final Consolidated Report)

This checklist translates the consolidated changeset plan into actionable, step-by-step items. It is grouped by framework, plus cross-framework integration tasks. Each item is atomic and ready to be executed by agents.

## Security Framework
- [ ] Create `security/findings.yaml` capturing all Critical=0 issues.
- [ ] Implement waiver schema for exceptions with `expiry` and `owner` fields.
- [ ] Update all manifests to include `governance.tags[]` with rationale + expiry.
- [ ] Add automated gate to block release if any Critical=0 unresolved.

## Planning Framework
- [ ] Align all files in `planning/manifests/` to consistent path bases.
- [ ] Add `snapshot_rev` to every planning manifest.
- [ ] Add `governance.fields[]` to each planning manifest.

## QA Framework
- [ ] Create `qa/compliance_map.md` mapping schema coverage.
- [ ] Add automated lint + coverage parity checks as quality gates.
- [ ] Ensure cross-stream consistency validation is enforced.

## Observability Framework
- [ ] Generate `observability/digest_cycleN.md` for each cycle.
- [ ] Include MTTA, MTTR, incident summaries in each digest.
- [ ] Attach gate evidence (logs, metrics, validation) to each digest.

## Cross-Framework Integration
- [ ] Seal all manifests with `snapshot_rev` and `rulebook_hash`.
- [ ] Collect QA + Security + Planning + Observability digests into `/memory-bank/digests/`.
- [ ] Configure CI/CD to validate manifests, enforce governance checks, and block release on unresolved Critical issues.

---
⚡ Use this checklist to drive the next background agent cycle. Agents should mark off items, propose edits, or generate new files as required.
