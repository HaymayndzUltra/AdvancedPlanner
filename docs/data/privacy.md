# Data Privacy & Classification

This document summarizes data classification, PII handling, retention, and access controls for the canonical datasets.

## Classification Taxonomy
- public: Non-sensitive operational metadata, safe for wide sharing
- internal: Default classification for business data without PII
- confidential: Sensitive data; includes PII or financial attributes

## PII Classes (examples)
- email: RFC 5322 email addresses
- name: Person names
- phone: E.164 phone numbers
- ip: IPv4/IPv6 addresses
- pan_fragment: Non-sensitive fragments (e.g., last4) of card PAN

## Datasets (current)
- users (confidential; contains PII)
  - Fields with PII: email, full_name, phone_number
  - Retention: delete after P7Y; GDPR erasure window P30D
  - Access tiers: analyst=masked; data_scientist=masked; admin=full
- session_events (internal/confidential mix; contains PII)
  - Fields with PII: ip_address (masked/anonymized)
  - Retention: delete after P365D
  - Access tiers: analyst=masked; data_scientist=masked; admin=full
- transactions (confidential; contains PII-like fragments)
  - Fields with PII: card_last4 (tokenized → card_last4_token)
  - Retention: delete after P7Y; immediate masking policy on card fragments
  - Access tiers: finance_analyst=masked; admin=full

## Controls & Policies
- Encryption: at rest and in transit for all datasets
- Masking:
  - Email: tokenized domain-local replacement
  - Phone: redaction to last 2 digits
  - IP: IPv4 /16, IPv6 /64 anonymization
  - Card last4: tokenized; source field cleared
- Access tiers by role: enforced via `security.access_tiers` in schemas
- Retention: declared per dataset under `retention` with ISO 8601 periods

## Operational Notes
- Pipelines apply privacy controls prior to validation and warehousing
- Lineage JSON captures row_count and validation status for auditability
- Schema changes that affect PII must update this doc and `schemas/*.yaml`
