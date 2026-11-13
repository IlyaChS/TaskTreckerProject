import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.db import Base, get_db


SQLALCHEMY_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)

def test_create_task(client):
    response = client.post(
        "/tasks/",
        json={
            "title": "Learn FastAPI",
            "description": "Practice automated testing"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Learn FastAPI"
    assert data["description"] == "Practice automated testing"
    assert data["is_completed"] is False


def test_get_tasks(client):
    client.post(
        "/tasks/",
        json={
            "title": "Learn Python",
            "description": "Practice Python programming"
        }
    )
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_task_by_id(client):
    create_response = client.post(
        "/tasks/",
        json={
            "title": "Learn SQL",
            "description": "Practice SQL queries"
        }
    )
    task_id = create_response.json()["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_get_nonexistent_task(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_task_validation(client):
    response = client.post(
        "/tasks/",
        json={
            "title": "Hi",
            "description": "Valid description"
        }
    )
    assert response.status_code == 422


def test_update_task(client):
    create_response = client.post(
        "/tasks/",
        json={
            "title": "Old title",
            "description": "Old description"
        }
    )
    task_id = create_response.json()["id"]
    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "New title",
            "description": "New description"
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New title"


def test_patch_task(client):
    create_response = client.post(
        "/tasks/",
        json={
            "title": "Old title",
            "description": "Some description"
        }
    )
    task_id = create_response.json()["id"]
    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "title": "Updated title"
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"
    assert response.json()["description"] == "Some description"


def test_delete_completed_task(client):
    create_response = client.post(
        "/tasks/",
        json={
            "title": "Completed task",
            "description": "Task to delete"
        }
    )
    task_id = create_response.json()["id"]
    client.patch(
        f"/tasks/{task_id}",
        json={
            "is_completed": True
        }
    )
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200


def test_delete_incomplete_task(client):
    create_response = client.post(
        "/tasks/",
        json={
            "title": "Incomplete task",
            "description": "Task should not be deleted"
        }
    )
    task_id = create_response.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 400