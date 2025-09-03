---
schema_version: 1
cycle_id: "2025-09-02"
registry:
  - exception_id: EX-2025-001
    title: Temporary waiver for third-party SCA medium alerts
    owner: team-appsec
    scope:
      service: payments-api
      tags: [license]
      applies_to_findings: [F-1234, F-5678]
    justification: Vendor patch pending; risk accepted for 14 days.
    expires_on: "2025-10-01"
    ticket: SEC-8123
    approved_by: ciso@company.com
    status: approved
---

# Exceptions Registry

This registry captures approved and scoped exceptions with expiries and compensating controls.