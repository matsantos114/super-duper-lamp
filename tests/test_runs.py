from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_run() -> None:
    payload = {
        "external_activity_id": "1234567890",
        "distance_meters": 1000,
        "started_at": "2026-01-01T00:00:00Z",
        "duration_seconds": 3600,
    }
    response = client.post("/runs", json=payload)

    assert response.status_code == 201

    response_body = response.json()

    assert response_body["external_activity_id"] == payload["external_activity_id"]
    assert response_body["distance_meters"] == payload["distance_meters"]
    assert response_body["duration_seconds"] == payload["duration_seconds"]
    assert response_body["started_at"] == payload["started_at"]


def test_create_run_rejects_zero_distance() -> None:
    payload = {
        "external_activity_id": "1234567890",
        "distance_meters": 0,
        "started_at": "2026-01-01T00:00:00Z",
        "duration_seconds": 3600,
    }
    response = client.post("/runs", json=payload)

    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "distance_meters"]
    assert error["type"] == "greater_than"

