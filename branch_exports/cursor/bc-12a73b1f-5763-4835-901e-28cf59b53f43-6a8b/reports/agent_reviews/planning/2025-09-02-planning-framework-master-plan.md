## Planning Framework Master Plan (Merged)

This document consolidates all Planning framework inputs (c1, c2, c3) into a single aligned plan.

### Sources
- FE Digest: `frameworks/planning-fe/digests/2025-09-02-digest.md`
- FE Manifest: `frameworks/planning-fe/manifests/2025-09-02-handoff_manifest.yaml`
- FE Story Map: `frameworks/planning-fe/storymaps/2025-09-02-story_map.md`
- FE Task Breakdown: `frameworks/planning-fe/tasks/2025-09-02-fe_task_breakdown.yaml`
- BE Digest: `frameworks/planning-be/digests/PLN-BE-2024-01-digest.md`
- Governance Rulebook: `rules/master-rules/planning-fe/rulebook.v1.yaml`

### Verified FE Manifest
- snapshot_rev: 986b378aed13dd70f678417f7725a3fac4458ed6
- rulebook_hash: 34c981297f6696c93b5844b91256e56609f27fdf2d9a360907bcc5d6d91066a9
- manifest_checksum_sha256: dce1007ec2447148e8269aedb3997f8c6d45f45b07859dcc2fc62310f6c31f4a
- artifact checksums:
  - tasks: 10b938f0994ffcc1a3cdff03f25f907f24f2a53ab634a65b08ff6955222bb120
  - story_map: 3081ed3a58f1e0766ef94cf9487f89d1e080ea2d2d4ea7e73f7302e6be782e9d
  - digest: 7b3cffb676af1d5c39c1f33219677d07ca56839471753a0852400f01648f3cf0

### Alignment Summary
- Lifecycle states aligned across FE/BE: PLANNED → READY_FOR_HANDOFF → PACKAGED → EXECUTED → VALIDATED → IMPROVE.
- Gates harmonized: schema_lint, cross_stream_consistency, parity/coverage; Critical=0 governance enforced.
- Artifact-first: YAML/MD/JSON across both streams; FE manifest sealed with checksums, snapshot_rev, and rulebook_hash.
- Metrics spine: Digest includes KPIs and gate outcomes; BE digest mirrors design-phase KPIs.

### Next Actions
- Wire CI jobs to compute and verify checksums and gate results for FE artifacts.
- Expand cross_stream_consistency validators to include BE contracts and design assets.
- Publish FE governance rulebook reference across streams and add checks in CI.
