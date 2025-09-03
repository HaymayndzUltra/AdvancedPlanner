# Data Migration Plan

## Scope
Initial rollout of Orchestrator core schema: `agents`, `tasks`, `task_events`, `artifacts`, `contracts`.

## Environments
- Dev → Staging → Production with promotion gates.

## Strategy
- Forward-only SQL migrations stored under `contracts/data/migrations` with semantic numbering.
- Immutable migration files; corrections via new migrations.

## Process
1. Generate SQL migration in feature branch.
2. Run in ephemeral DB for CI (lint + apply + rollback test where applicable).
3. Apply to staging via migration job; verify app smoke tests.
4. Promote to production during maintenance window if required.

## Rollback
- Schema rollbacks only when safe; otherwise forward fix with corrective migration.
- Data restoration via snapshots/backups.

## Data Seeding
- Minimal seed: insert OpenAPI v1 contract reference.

## Observability
- Log migration start/stop, duration, and row counts affected.