from fastapi.testclient import TestClient

from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Run


def test_create_run(
    db_client: TestClient,
    db_session: Session,
) -> None:
    payload = {
        "external_activity_id": "1234567890",
        "distance_meters": 1000,
        "started_at": "2026-01-01T00:00:00Z",
        "duration_seconds": 3600,
    }
    response = db_client.post("/runs", json=payload)

    assert response.status_code == 201

    response_body = response.json()
    assert isinstance(response_body["id"], int)
    assert response_body["created_at"] is not None
    assert response_body["updated_at"] is not None
    assert response_body["external_activity_id"] == payload["external_activity_id"]
    assert response_body["distance_meters"] == payload["distance_meters"]
    assert response_body["duration_seconds"] == payload["duration_seconds"]
    assert datetime.fromisoformat(
        response_body["started_at"]
    ) == datetime.fromisoformat(payload["started_at"])
    saved_run = db_session.get(Run, response_body["id"])

    assert saved_run is not None
    assert saved_run.external_activity_id == payload["external_activity_id"]
    assert saved_run.distance_meters == payload["distance_meters"]


def test_create_run_rejects_zero_distance(
    db_client: TestClient,
) -> None:
    payload = {
        "external_activity_id": "1234567890",
        "distance_meters": 0,
        "started_at": "2026-01-01T00:00:00Z",
        "duration_seconds": 3600,
    }
    response = db_client.post("/runs", json=payload)

    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "distance_meters"]
    assert error["type"] == "greater_than"


def test_create_run_rejects_duplicate_external_activity_id(
    db_client: TestClient,
    db_session: Session,
) -> None:
    payload = {
        "external_activity_id": "duplicate-activity",
        "distance_meters": 1000,
        "started_at": "2026-01-01T00:00:00Z",
        "duration_seconds": 3600,
    }

    first_response = db_client.post("/runs", json=payload)
    second_response = db_client.post("/runs", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "Run already exists",
    }
    saved_run = db_session.get(
        Run,
        first_response.json()["id"],
    )
    assert saved_run is not None

    next_payload = payload.copy()
    next_payload["external_activity_id"] = "activity-after-duplicate"

    next_response = db_client.post("/runs", json=next_payload)

    assert next_response.status_code == 201


def test_get_run_returns_existing_run(
    db_client: TestClient,
) -> None:
    payload = {
        "external_activity_id": "get-activity",
        "distance_meters": 5000,
        "started_at": "2026-01-01T00:00:00Z",
        "duration_seconds": 1800,
    }

    create_response = db_client.post("/runs", json=payload)
    assert create_response.status_code == 201

    created_run = create_response.json()
    response = db_client.get(f"/runs/{created_run['id']}")

    assert response.status_code == 200

    response_body = response.json()
    assert response_body["id"] == created_run["id"]
    assert response_body["external_activity_id"] == "get-activity"
    assert response_body["distance_meters"] == 5000

def test_get_run_returns_404_for_missing_id(
    db_client: TestClient,
) -> None:
    response = db_client.get("/runs/999999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Run not found",
    }