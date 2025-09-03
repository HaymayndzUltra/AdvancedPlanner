# Architecture & API Docs

Artifacts produced by the Architecture & API track.

## Diagrams
- `diagrams/system-context.mmd`
- `diagrams/component.mmd`
- `diagrams/deployment.mmd`
- `diagrams/sequence-task-lifecycle.mmd`
- `diagrams/data-model.mmd`

## ADRs
See `adr/` folder for decisions:
- 0001 Architecture style and service boundaries
- 0002 API versioning strategy
- 0003 Data store and schema governance
- 0004 Security, authentication, and authorization

## Contracts
- OpenAPI v1: `contracts/api/openapi-v1.yaml`
- Mocks: `contracts/mocks/openapi-v1-mock.json`

## Data Model & Migration
- Schema: `contracts/data/schema.sql`
- Migrations: `contracts/data/migrations/`
- Seeds: `contracts/data/seeds/`
- Plan: `docs/architecture/data-migration-plan.md`

## Performance
- Budgets: `docs/architecture/performance-budgets.md`
- Baseline Load Test: `tests/load/k6-baseline.js`