---
title: "ADR 0004: Security, Authentication, and Authorization"
status: Proposed
date: 2025-09-03
deciders: Security & Architecture Teams
---

## Context
Agents and human users interact with the Orchestrator API. We must ensure identity, least-privilege, and audit trails.

## Decision
- Adopt OAuth2/OIDC for user authentication; JWT bearer tokens with short TTLs.
- Issue client credentials for agents; scope tokens to minimal permissions.
- Enforce mTLS for intra-service communication.
- Implement RBAC roles: `admin`, `maintainer`, `agent`, `viewer`.
- Log security events and provide audit trails for all mutating operations.
- Support request signing for artifact uploads and webhooks (HMAC).

## Rationale
Standards-based auth eases integration and security reviews. RBAC simplifies permission management across APIs.

## Consequences
- Requires identity provider configuration and token management.
- Additional operational complexity for certificate rotation.

## Alternatives
- API keys only: simpler but weaker security posture and poor auditability.