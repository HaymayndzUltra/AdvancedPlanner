# RAD Register — Risks, Assumptions, Dependencies

- Traceability ID: RAD-REGISTER-001
- Version: 0.1 (Draft)
- Date: TBD
- Program: AI Governor Framework
- Related: docs/discovery/brief.md

## Prioritization Scale

- Impact: H/M/L
- Likelihood: H/M/L
- Priority: P0 (critical), P1 (high), P2 (medium), P3 (low)

## Risks

- RISK-001: Inconsistent AI output causes rework and integration failures
  - Impact: High; Likelihood: Medium; Priority: P1
  - Signals: High PR rejection rate; late API contract mismatches
  - Mitigations: Contract-first development, automated contract tests on integration branch
  - Owners: Eng Leads, Architecture
- RISK-002: Documentation/rules drift from code reduces reliability
  - Impact: Medium-High; Likelihood: Medium; Priority: P1
  - Signals: Onboarding delays; repeated context clarifications
  - Mitigations: In-repo rules/READMEs as source of truth; doc sync after changes
  - Owners: Eng Leads, Docs
- RISK-003: Security issues discovered late in release cycle
  - Impact: High; Likelihood: Medium; Priority: P1
  - Signals: Critical vulns at release; unscannable dependencies
  - Mitigations: Policy-as-code, SBOM, SAST/DAST embedded in CI; secrets scanning
  - Owners: Security
- RISK-004: Parallel work conflicts without strong coordination
  - Impact: High; Likelihood: Medium; Priority: P1
  - Signals: Merge-train failures; blocked PRs; contract divergence
  - Mitigations: Strategy B with nightly merge trains; early QA; feature flags
  - Owners: Eng Leads, Release
- RISK-005: Insufficient observability increases MTTR and alert fatigue
  - Impact: Medium-High; Likelihood: Medium; Priority: P2
  - Signals: Noisy alerts; missing deployment markers; slow incident resolution
  - Mitigations: SLO/SLI definition, dashboards, alert noise budgets, deployment markers
  - Owners: SRE/Observability
- RISK-006: Compliance/privacy constraints block or delay features
  - Impact: High; Likelihood: Low-Med; Priority: P2
  - Signals: Data handling uncertainty; unclear retention/consent requirements
  - Mitigations: Early Legal/Privacy review; data contract and retention policy
  - Owners: Legal/Privacy, Data/Architecture
- RISK-007: Stakeholder misalignment on KPIs and sign-off criteria
  - Impact: Medium; Likelihood: Medium; Priority: P2
  - Signals: Late scope churn; unclear success definitions
  - Mitigations: Stakeholder interview plan; explicit KPI registry with traceability
  - Owners: PM, Eng Leads

## Assumptions

- ASM-001: Repository remains the single source of truth for rules and workflows
  - Confidence: High
  - Validation: Enforced via PR review and CI checks on docs changes
- ASM-002: Strategy B (Swarm with Guardrails) is the orchestration baseline
  - Confidence: Medium-High
  - Validation: Reassess after Phase 1; compare DORA metrics and merge-train stability
- ASM-003: UX targets WCAG 2.2 AA and provides tokens early
  - Confidence: Medium
  - Validation: UX delivery milestones aligned with Architecture/API contracts
- ASM-004: CI can support contract tests, policy-as-code, SBOM generation
  - Confidence: Medium
  - Validation: Spike to confirm toolchain; add gates progressively

## Dependencies

- DEP-001: API contract availability (OpenAPI/GraphQL/gRPC) before BE/FE implementation
  - Unblockers: Provide stubs/mocks; align data contracts
  - Owners: Architecture/API
- DEP-002: Design tokens and component specs before FE integration
  - Unblockers: Provide interim tokens and Storybook previews
  - Owners: UX/UI
- DEP-003: CI/CD pipelines for contract tests, security scans, and artifact signing
  - Unblockers: Start with minimal pipeline; iterate gates
  - Owners: Release/DevOps, Security
- DEP-004: Observability standards and dashboards before first staging deploy
  - Unblockers: Minimal telemetry schema; add markers and alerts iteratively
  - Owners: SRE/Observability

## Review Cadence

- Weekly RAD review during Phase 1–2; risk owners update status and mitigations
- Escalate any P0/P1 changes to program leads within 24 hours

## Sign-offs

- Product Lead: Name, Date, Signature
- Engineering Lead: Name, Date, Signature