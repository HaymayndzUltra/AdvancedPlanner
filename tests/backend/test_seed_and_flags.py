from fastapi.testclient import TestClient

from src.backend.app.main import create_app
from src.backend.app.seed import load_seed_data
from src.backend.app.settings import reset_settings_cache
from src.backend.app.storage import store


def test_seed_loader_populates_tasks():
    store._tasks.clear()
    load_seed_data()
    app = create_app()
    client = TestClient(app)
    resp = client.get("/tasks/")
    assert resp.status_code == 200
    assert len(resp.json()["items"]) >= 3


def test_feature_flag_disables_tasks(monkeypatch):
    store._tasks.clear()
    monkeypatch.setenv("TASKS_ENABLE_TASKS_FEATURE", "false")
    reset_settings_cache()
    app = create_app()
    client = TestClient(app)
    resp = client.get("/tasks/")
    # When disabled, route should 404
    assert resp.status_code == 404

