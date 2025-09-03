---
title: "ADR 0001: Architecture Style and Service Boundaries"
status: Proposed
date: 2025-09-03
deciders: Architecture/API Team
---

## Context
The platform orchestrates multiple background agents through a central API and scheduler. Requirements include:
- Clear system boundaries for UI, API, agents, and data stores
- Contract-first development with versioned APIs
- Horizontal scalability and reliable task processing
- Security (authn/z), auditability, and observability

## Decision
- Adopt a service-oriented architecture with a single Orchestrator API service and a separate Scheduler worker pool.
- Use REST (OpenAPI) for external contracts (v1), with potential future GraphQL facade for UI aggregation.
- Use a message broker for decoupled task dispatch and backpressure.
- Persist state in PostgreSQL; store large artifacts in object storage.
- Enforce auth via OAuth2/OIDC bearer tokens; service-to-service via mTLS and scoped tokens.

## Rationale
- REST with OpenAPI offers broad tooling and contract test support. Scheduler separation allows independent scaling and failure isolation. PostgreSQL meets relational needs with strong consistency; object storage is ideal for large artifacts.

## Consequences
- Additional operational components (broker, object storage) to manage.
- Clear contract boundaries enable parallel development and contract testing.
- Enables gradual evolution to more services if needed.

## Alternatives
- Monolith only: simpler ops but limited scalability and isolation.
- gRPC only: efficient but less friendly for browser/UI and external integrators.
- Event-only architecture: complex consistency and harder debugging.