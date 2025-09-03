## Roadmap & Milestones — Agent-Orchestrated Delivery Platform (AODP)

### Team & Capacity Assumptions
- Team: 6 core tracks (Planning, UX, Architecture/API, FE, BE, QA/Security) with shared Release/Observability.
- Capacity: ~6–8 agent-weeks per calendar week (parallel agents), accounting for coordination overhead.

### Timeline (aligned to Master Execution Schedule)
- Weeks 1–2: Discovery, Planning, UX in parallel; PRD/roadmap/backlog drafted and signed off EOW2.
- Weeks 3–6: Architecture/API finalized W3; Implementation FE/BE iterate W3–W6; Data/ML optional.
- Weeks 5–8: QA/Security fully integrated; Release pipelines hardened; Observability dashboards live; RC by W7.

### Milestones
M1 — Foundations (EOW2)
- PRD approved; backlog prioritized with traceability IDs.
- Design tokens and component specs drafted; initial OpenAPI/GraphQL contract for Onboarding.

M2 — Contracts & Pipelines (EOW3)
- ADRs approved; API mocks/stubs; contract test suite green on integration branch.
- CI pipeline with security scans (SAST/DAST), SBOM, and artifact signing.

M3 — Vertical Slice Ready (EOW5)
- FE Onboarding UI integrated with mocked API; BE service skeleton live in staging behind flag.
- Unit/integration tests ≥ 80% coverage for Onboarding modules.

M4 — Slice Integrated (EOW6)
- FE switches from mocks to live API; e2e smoke green in staging; feature flags allow canary.
- Observability dashboards show p95 latency, error rate, and RPS; alerts tuned.

M5 — Release Candidate (EOW7)
- Nightly merge train stable (< 5% failure); security checks zero critical; accessibility checks AA.
- RC cut with release notes and rollback plan.

M6 — MVP Complete (EOW8)
- Onboarding slice GA (or production-ready staging); KPIs tracked; retro completed with actions.

### Rough Estimates (ROM)
- Planning artifacts (this PR): 8–12 agent-days.
- UX tokens + components (M1–M2): 10–15 agent-days.
- Architecture contracts + ADRs (M1–M2): 10–15 agent-days.
- Implementation Onboarding slice (M2–M4): 25–35 agent-days (FE 12–18, BE 13–17).
- QA/Security & CI hardening (M2–M5): 15–20 agent-days.
- Release/Observability (M3–M5): 8–12 agent-days.

### Dependencies & Gates
- PRD sign-off gates M2 start.
- Contract tests green gate nightly merge train.
- Security zero-critical gate RC.
- Accessibility AA gate M5.

### Risks & Contingencies
- If contract churn delays M2, split Onboarding slice into two smaller increments.
- If CI becomes bottleneck, add parallel runners and test sharding; prioritize flake reduction.

