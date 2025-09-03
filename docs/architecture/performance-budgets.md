# Performance Budgets

## API Budgets (p50/p95)
- POST /v1/tasks: 120ms / 300ms
- GET /v1/tasks: 100ms / 250ms
- PATCH /v1/tasks/{id}: 100ms / 250ms
- PUT /v1/tasks/{id}/artifacts: 150ms / 350ms

## Throughput Targets
- 200 RPS sustained on /health and read endpoints
- 50 RPS sustained on write endpoints

## Error Budgets
- Availability: 99.9% monthly (allowed error budget ~43.2 min)
- 5xx rate < 0.1%

## Concurrency
- Target 500 concurrent connections; graceful at 1000

## Data Store
- P95 DB query latency < 50ms for indexed reads, < 100ms for writes

## Message Broker
- P95 publish/consume < 50ms intra-VPC