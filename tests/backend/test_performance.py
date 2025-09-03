import time

from fastapi.testclient import TestClient

from src.backend.app.main import create_app


def test_list_tasks_performance_budget():
    client = TestClient(create_app())

    start = time.perf_counter()
    resp = client.get("/tasks/")
    duration_ms = (time.perf_counter() - start) * 1000

    assert resp.status_code == 200
    # Budget: p50 single request under 25ms in CI env
    assert duration_ms < 25.0

