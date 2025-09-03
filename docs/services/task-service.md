## Task Service

Exposes health endpoints and simple in-memory Tasks CRUD. Intended as a scaffold aligned with API-first workflow; replace in-memory store with persistent DB during evolution.

- Base URL: `/`
- OpenAPI: `/openapi.json` (feature flag controlled)
- Docs: `/docs`, `/redoc` (feature flag controlled)

### Endpoints
- `GET /health/live` → Liveness
- `GET /health/ready` → Readiness
- `GET /tasks/` → List tasks
- `POST /tasks/` → Create task
- `GET /tasks/{id}` → Retrieve task
- `PATCH /tasks/{id}` → Update task
- `DELETE /tasks/{id}` → Delete task

### Configuration
Environment variables with prefix `TASKS_`:
- `TASKS_ENABLE_DOCS` (default: true)
- `TASKS_ENABLE_OPENAPI` (default: true)
- `TASKS_ENABLE_TASKS_FEATURE` (default: true)

### Seed Data
`src/backend/app/seed.py` provides a simple loader that inserts a few example tasks into the in-memory store.

### Run Locally
```
uvicorn src.backend.app.main:app --reload
```

