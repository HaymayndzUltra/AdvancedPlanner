## Performance Budgets

- Endpoint budgets (local CI):
  - GET /tasks/: p50 < 25ms, p95 < 60ms
  - POST /tasks/: p50 < 30ms, p95 < 80ms
  - PATCH/DELETE /tasks/{id}: p50 < 30ms, p95 < 80ms
  - Health endpoints: p50 < 10ms

- Load baseline (to be run in staging):
  - 100 RPS sustained for 60s, error rate < 0.1%
  - CPU < 70%, memory stable

- Notes:
  - Benchmarks are guidance for in-memory store; revisit for DB-backed implementation.