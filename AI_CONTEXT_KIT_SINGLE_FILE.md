# AI Governor Framework — Single-File Context Kit

This single file consolidates the core logic of the framework so any AI planner can quickly understand and operate within a separate repo using the same principles. It merges and normalizes the essentials from: CONSOLIDATED_DOCUMENTATION.md, DEV_WORKFLOW_DOCUMENTATION.md, and RULES_DOCUMENTATION.md.

Key normalization applied here:
- Uses a 5-step workflow (Step 0–Step 4), with Step 0 as Bootstrap.
- Uses .mdc extensions for rules for auto-loading in Cursor.
- Clarifies Architectural Decision Matrix wording for Data CRUD.

## 1) System Overview

The framework transforms generic AI assistance into a reliable, context-aware engineering partner via two components:
- Development Workflow (dev-workflow/): predictable, controllable execution (Step 0–4)
- Rules System (rules/): master rules (foundational protocols) + common rules (specialized expertise)

Directory map (authoritative names/extensions):
```
AI Governor Framework
├── Development Workflow (dev-workflow/)
│   ├── 0-bootstrap-your-project.md
│   ├── 1-create-prd.md
│   ├── 2-generate-tasks.md
│   ├── 3-process-tasks.md
│   └── 4-implementation-retrospective.md
└── Rules System (rules/)
    ├── Master Rules (master-rules/)
    │   ├── 0-how-to-create-effective-rules.mdc
    │   ├── 1-master-rule-context-discovery.mdc
    │   ├── 2-master-rule-ai-collaboration-guidelines.mdc
    │   ├── 3-master-rule-code-quality-checklist.mdc
    │   ├── 4-master-rule-code-modification-safety-protocol.mdc
    │   ├── 5-master-rule-documentation-and-context-guidelines.mdc
    │   └── 6-master-rule-complex-feature-context-preservation.mdc
    └── Common Rules (common-rules/)
        ├── common-rule-ui-foundation-design-system.mdc
        ├── common-rule-ui-interaction-a11y-perf.mdc
        └── common-rule-ui-premium-brand-dataviz-enterprise-gated.mdc
```

## 2) Development Workflow (Step 0–4)

### Step 0: Project Bootstrap & Context Engineering (Protocol 0)
Role: Project Analyst & Context Architect
- Configure `.cursor/rules/`, ensure rules use `.mdc` and have YAML frontmatter
- Map codebase structure and tech stack
- Investigate security, data flow, conventions
- Generate READMEs and project rules; establish “Context Kit”

### Step 1: Unified PRD Creation (Protocol 1)
Role: Monorepo-Aware Product Manager
Architectural Decision Matrix:

| Need Type | Implementation Target | Key Constraints | Communication |
|---|---|---|---|
| UI/Component | Frontend Application | Responsive, Theming, i18n | API calls, Direct calls |
| Business Logic | Backend Microservices | Scalability, Inter-service RPC | Full CRUD to API |
| Data CRUD | Central REST API | Exclusive DB access, OpenAPI | Direct DB queries (API layer only) |
| Static Assets | Object Storage | Caching strategy, Versioning | Direct SDK/API access |

### Step 2: Technical Task Generation (Protocol 2)
Role: Monorepo-Aware Tech Lead
- Load rules and architectural guides; deduplicate UI components
- Emit `tasks-[feature].md` with top-level tasks (UI, backend, testing, docs)
- Fill templates per layer; assign personas (System Integrator, Code Architect, QA)

### Step 3: Controlled Task Execution (Protocol 3)
Role: AI Paired Developer
- Focus Mode: one parent task per chat; complete all sub-tasks before validation
- Platform Research first; apply Safety Protocol; keep Documentation in sync
- Use formal prefixes: `[NEXT TASK]`, `[TASK COMPLETED]`, `[GIT PROPOSAL]`

### Step 4: Implementation Retrospective (Protocol 4)
Role: QA & Process Improvement Lead
- Technical self-review against rules; collaborative interview
- Propose improvements; update docs to maintain context integrity

## 3) Master Rules (Foundational Protocols)

### Rule 0: How to Create Effective Rules
Purpose: Protocol for creating maintainable, discoverable rules.
Pillars: Structure & Discoverability, Personality & Intent, Precision & Clarity, Exemplarity & Contrast.

### Rule 1: Context Discovery (BIOS) — alwaysApply: true
Purpose: Initializes operating context; loads kernel rules first.
Core: inventory rules, gather operational context, evaluate relevance, announce loaded rules first.

### Rule 2: AI Collaboration Guidelines
Purpose: Governs AI-user interaction, task planning, and tool usage.
Core: Think-first, plan → validate → execute; use tools when available; conflict/doubt protocols.

### Rule 3: Code Quality Checklist
Purpose: Baseline for robustness, reliability, clarity.
Core: try/catch for I/O, guard clauses for inputs, explicit naming, limited nesting.

### Rule 4: Code Modification Safety Protocol
Purpose: Prevent regressions with pre-analysis, risk assessment, surgical implementation, validation.
Core: impact analysis, MEDIUM/HIGH risk confirmations, backward compatibility, validation checklist.

### Rule 5: Documentation Context Integrity
Purpose: Keep documentation faithful to code; create local setup guides before integrating complex services.
Core: pre-code doc analysis, post-change audit and update.

### Rule 6: Complex Feature Context Preservation
Purpose: Protect technically complex features and collaborative refinements.
Core: detect complexity, create context snapshots, incremental enhancement, rollback readiness.

## 4) How Rules Are Loaded & Triggered

Auto-loading (Cursor): only `.mdc` files in `.cursor/rules/` are auto-activated.
BIOS First: Rule 1 (alwaysApply: true) runs first and selects additional rules.
Selection Priorities:
1. Absolute directives: `alwaysApply: true` and Collaboration Rule (Rule 2)
2. Scope match (SCOPE)
3. Keyword triggers (TRIGGERS)
4. Concept tags (TAGS)

Dynamic Re-evaluation: re-run discovery on domain/location pivots.
Project Rules: if present near edited files, include via discovery.

Quick trigger mapping:
- “modify/refactor/update/handler/router/manager/modal” → Rule 4
- “README/documentation” → Rule 5
- “complex/algorithm/state machine/api integration/large file” → Rule 6
Always active: Rule 1 + load Rule 2.

## 5) Communication & Execution Standards

- Think-First + Plan Validation (Rule 2)
- Use tools for edits/search/lints/tests when available
- Announce loaded rules first (Rule 1 Step 4)
- Focus Mode per parent task; checkpoint for validation
- Safety-first edits; present impact analysis for non-trivial changes (Rule 4)

## 6) What to Share With an External AI Planner

If you can only provide one file, share this Single-File Context Kit.

If you can attach more for machine-activation and determinism:
- Entire `.cursor/rules/` directory (master + common `.mdc`)
- `dev-workflow/*.md` for concrete loop
- `CHANGELOG.md` for history and deltas

## 7) Expected Outcomes

- Predictable execution bounded by rules and workflow
- Improved quality and safety by default
- Continuous context enrichment through retrospectives and doc sync


