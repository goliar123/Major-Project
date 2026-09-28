"""
Unit tests for FastAPI REST Endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_list_traces_endpoint():
    response = client.get("/api/v1/traces?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5

def test_attribute_endpoint():
    payload = {
        "trace_id": "api-test-01",
        "task_goal": "Migrate DB schema",
        "steps": [
            {
                "step_index": 0,
                "agent_name": "User",
                "action_payload": "Migrate schema without losing data"
            },
            {
                "step_index": 1,
                "agent_name": "DBArchitect",
                "action_payload": "DROP TABLE users;"
            },
            {
                "step_index": 2,
                "agent_name": "Tester",
                "action_payload": "AssertionError: 0 rows found"
            }
        ]
    }
    response = client.post("/api/v1/attribute", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["responsible_agent"] == "DBArchitect"
    assert data["decisive_step_index"] == 1
    assert "DROP TABLE" in data["explanation"]

def test_cache_stats_endpoint():
    response = client.get("/api/v1/cache/stats")
    assert response.status_code == 200
    data = response.json()
    assert "hits" in data
    assert "misses" in data

def test_live_session_api():
    # 1. Start live session
    start_resp = client.post("/api/v1/live/start?trace_id=api_live_01&task_goal=Test+Live+API&expected_output=success")
    assert start_resp.status_code == 200
    assert start_resp.json()["status"] == "started"

    # 2. Ingest step
    step_payload = {
        "step_index": 0,
        "agent_name": "Worker",
        "action_payload": "Execute live step"
    }
    ingest_resp = client.post("/api/v1/live/ingest?trace_id=api_live_01", json=step_payload)
    assert ingest_resp.status_code == 200
    assert ingest_resp.json()["step_index"] == 0

    # 3. Finish session
    finish_resp = client.post("/api/v1/live/finish?trace_id=api_live_01&final_output=success&status=COMPLETED")
    assert finish_resp.status_code == 200
    assert finish_resp.json()["clean_run"] is True
