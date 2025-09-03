---
title: "ADR 0003: Primary Data Store and Schema Governance"
status: Proposed
date: 2025-09-03
deciders: Architecture/Data Team
---

## Context
The system manages tasks, agents, events, and artifacts with transactional requirements and reporting needs.

## Decision
- Use PostgreSQL as the primary relational store.
- Use UUIDv7 for primary keys; server-generated timestamps in UTC.
- Normalize core entities (tasks, agents, contracts, events); index for common queries.
- Store large artifacts and blobs in object storage; keep references in DB.
- Govern schema via migration files under `contracts/data/migrations` with review gates.

## Rationale
PostgreSQL provides ACID transactions, rich indexing, JSONB for flexibility, and mature tooling.

## Consequences
- Requires migration discipline and capacity planning.
- Object storage introduces eventual consistency for artifacts; mitigated by signed URLs and retries.

## Alternatives
- NoSQL (e.g., DynamoDB): scales well but complicates relational queries and transactions.
- Single-DB monolith: simpler but harder to scale scheduler independently.