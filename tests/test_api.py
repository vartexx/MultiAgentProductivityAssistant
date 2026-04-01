from __future__ import annotations

from collections.abc import Iterator

import app.db.models  # noqa: F401
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.routes import get_db
from app.db.database import Base
from app.main import app


@pytest.fixture
def client(tmp_path) -> Iterator[TestClient]:
    db_path = tmp_path / "test_api.db"
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_root_and_health(client: TestClient) -> None:
    root = client.get("/")
    assert root.status_code == 200
    root_payload = root.json()
    assert root_payload["docs"] == "/docs"
    assert root_payload["health"] == "/health"
    assert root_payload["api_prefix"] == "/api/v1"

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {"status": "ok"}


def test_tasks_create_and_list_with_valid_date(client: TestClient) -> None:
    create_response = client.post(
        "/api/v1/tasks",
        json={
            "user_id": "user-123",
            "title": "Prepare sprint notes",
            "due_date": "2026-04-02",
            "metadata": {"priority": "high"},
        },
    )

    assert create_response.status_code == 200
    task_payload = create_response.json()
    assert task_payload["title"] == "Prepare sprint notes"
    assert task_payload["due_date"] == "2026-04-02"
    assert task_payload["created_at"].endswith("Z")

    list_response = client.get("/api/v1/tasks", params={"user_id": "user-123"})
    assert list_response.status_code == 200
    listed = list_response.json()
    assert len(listed) == 1
    assert listed[0]["title"] == "Prepare sprint notes"
    assert listed[0]["created_at"].endswith("Z")


def test_tasks_reject_invalid_due_date(client: TestClient) -> None:
    response = client.post(
        "/api/v1/tasks",
        json={
            "user_id": "user-123",
            "title": "Invalid date task",
            "due_date": "not-a-date",
            "metadata": {},
        },
    )

    assert response.status_code == 422


def test_notes_create_and_list(client: TestClient) -> None:
    create_response = client.post(
        "/api/v1/notes",
        json={
            "user_id": "user-abc",
            "title": "Standup",
            "body": "Captured blockers and follow-ups.",
            "metadata": {"team": "platform"},
        },
    )

    assert create_response.status_code == 200
    note_payload = create_response.json()
    assert note_payload["title"] == "Standup"
    assert note_payload["created_at"].endswith("Z")

    list_response = client.get("/api/v1/notes", params={"user_id": "user-abc"})
    assert list_response.status_code == 200
    listed = list_response.json()
    assert len(listed) == 1
    assert listed[0]["title"] == "Standup"
    assert listed[0]["created_at"].endswith("Z")


def test_execute_workflow(client: TestClient) -> None:
    response = client.post(
        "/api/v1/workflows/execute",
        json={
            "user_id": "user-xyz",
            "goal": "Schedule meetings and capture notes",
            "context": {"timeframe": "this week", "priority": "high"},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] in {"success", "failed"}
    assert payload["workflow_run_id"] >= 1
    assert len(payload["steps"]) >= 2

    runs_response = client.get("/api/v1/workflow-runs", params={"user_id": "user-xyz"})
    assert runs_response.status_code == 200
    runs_payload = runs_response.json()
    assert len(runs_payload) >= 1
    assert runs_payload[0]["created_at"].endswith("Z")
