from fastapi import FastAPI

from .routers import health, tasks
from .settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Task Service",
        version="0.1.0",
        description="Backend Task Service implementing CRUD and health endpoints.",
        docs_url="/docs" if settings.enable_docs else None,
        redoc_url="/redoc" if settings.enable_docs else None,
        openapi_url="/openapi.json" if settings.enable_openapi else None,
    )

    # Routers
    app.include_router(health.router)
    if settings.enable_tasks_feature:
        app.include_router(tasks.router)

    return app


app = create_app()

