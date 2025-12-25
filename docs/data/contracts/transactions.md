---
contract: transactions
version: 1.0.0
owner: finance-data-platform
producers:
  - payments.gateway
  - orders.service
consumers:
  - analytics.warehouse
  - finance.accounting
slo:
  availability: 99.95%
  freshness: PT24H
  dq_checks:
    - unique(transaction_id) == 100%
    - not_null(transaction_id,user_id,amount,currency,status,created_at,updated_at)
    - enum(currency) in [USD,EUR,GBP,CAD,AUD,INR,JPY,BRL,MXN]
    - enum(status) in [authorized,captured,settled,refunded,voided,chargeback,failed]
privacy:
  pii: contains
  controls:
    - pan_fragment_tokenization
    - at_rest_encryption
    - in_transit_tls
schema_ref: ../../docs/data/schemas/transactions.yaml
---

# Transactions Data Contract

Defines canonical financial transaction data. Financial compliance requires stricter availability and privacy SLAs. PAN fragments must be tokenized; raw PANs are forbidden.

## Idempotency & Corrections
- Upserts by `transaction_id`; late arriving updates allowed for 7 days.
- Corrections logged via `status` transitions; audits retained per retention policy.

