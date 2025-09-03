# Planning FE Framework

Artifacts per cycle:
- `tasks/{cycle_id}-fe_task_breakdown.yaml`
- `storymaps/{cycle_id}-story_map.md`
- `manifests/{cycle_id}-handoff_manifest.yaml`
- `digests/{cycle_id}-digest.md`

States: PLANNED → READY_FOR_HANDOFF → PACKAGED → EXECUTED → VALIDATED → IMPROVE.

Quality gates: schema_lint, cross_stream_consistency, parity/coverage. Governance: tags[] and Critical==0 rule.
