---
title: "ADR 0002: API Versioning Strategy"
status: Proposed
date: 2025-09-03
deciders: Architecture/API Team
---

## Context
Multiple agents and UIs will integrate with the Orchestrator API. Contracts must be stable with non-breaking changes and predictable evolution.

## Decision
- Use URI-based, major versioned REST endpoints: `/v1/...`.
- Minor/patch changes are backward-compatible and documented via OpenAPI.
- Breaking changes require a new major version (`/v2`) and sunset policy.
- Provide machine-readable deprecation metadata in responses and documentation.
- Maintain parallel contract tests for all supported majors.

## Rationale
Clear, explicit versioning simplifies routing, caching, and documentation. It aligns with tooling and reduces ambiguity for clients.

## Consequences
- Multiple versions may be supported concurrently; increased maintenance.
- Enables safe evolution without blocking downstream agents.

## Alternatives
- Header-based versioning: flexible but less visible and more complex for caching/CDN.
- No versioning: too risky for multi-agent environment.