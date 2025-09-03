from fastapi.testclient import TestClient

from src.backend.app.main import create_app
from src.backend.app.settings import reset_settings_cache
from src.backend.app.storage import store


def get_client() -> TestClient:
    # Ensure feature flags are defaulted/enabled for these tests
    reset_settings_cache()
    app = create_app()
    return TestClient(app)


def test_list_initially_empty():
    client = get_client()
    store._tasks.clear()  # reset in-memory
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == {"items": []}


def test_create_and_get_task():
    client = get_client()
    store._tasks.clear()
    response = client.post("/tasks/", json={"title": "Task A", "description": "Desc"})
    assert response.status_code == 201
    created = response.json()
    task_id = created["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    fetched = response.json()
    assert fetched["title"] == "Task A"


def test_update_and_delete_task():
    client = get_client()
    store._tasks.clear()
    created = client.post("/tasks/", json={"title": "Task B"}).json()
    task_id = created["id"]

    upd = client.patch(f"/tasks/{task_id}", json={"description": "New", "status": "in_progress"})
    assert upd.status_code == 200
    body = upd.json()
    assert body["description"] == "New"
    assert body["status"] == "in_progress"

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    missing = client.get(f"/tasks/{task_id}")
    assert missing.status_code == 404

