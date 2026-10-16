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

def test_overview_endpoint():
    response = client.get("/api/v1/overview")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["total_traces"] > 0
    assert "environments" in data

def test_environments_endpoint():
    response = client.get("/api/v1/environments")
    assert response.status_code == 200
    data = response.json()
    assert "AutoGen" in data or "ChatDev" in data or "MetaGPT" in data

def test_synthetic_presets_endpoint():
    response = client.get("/api/v1/synthetic/presets")
    assert response.status_code == 200
    presets = response.json()
    assert len(presets) >= 3
    assert presets[0]["expected_blame"] == "DBArchitect"

def test_parse_raw_log_endpoint():
    raw_log = """
[User]: Please migrate database.
[DBArchitect]: DROP TABLE users;
[Tester]: AssertionError: 0 rows found.
"""
    response = client.post("/api/v1/parse/raw_log", json={
        "task_goal": "Migrate database",
        "log_text": raw_log
    })
    assert response.status_code == 200
    verdict = response.json()
    assert verdict["responsible_agent"] == "DBArchitect"

def test_parse_custom_json_endpoint():
    custom_payload = {
        "title": "Custom AutoGen Test",
        "task_goal": "Deploy app",
        "steps": [
            {"step_index": 0, "agent_name": "Dev", "action_payload": "DROP TABLE users;"},
            {"step_index": 1, "agent_name": "Monitor", "action_payload": "Alert: 0 records found in database"}
        ]
    }
    response = client.post("/api/v1/parse/custom_json", json=custom_payload)
    assert response.status_code == 200
    verdict = response.json()
    assert verdict["responsible_agent"] == "Dev"
    assert verdict["decisive_step_index"] == 0

def test_slide_deck_endpoints_ingest_evaluate_resolve():
    payload = {
        "trace_id": "slide_trace_01",
        "task_goal": "Migrate schema without losing data",
        "steps": [
            {
                "step_index": 0,
                "agent_name": "Dev",
                "action_payload": "DROP TABLE users;"
            },
            {
                "step_index": 1,
                "agent_name": "QA",
                "action_payload": "AssertionError: 0 rows found"
            }
        ]
    }

    # 1. Test /ingest (both /ingest and /api/v1/ingest)
    resp_ingest = client.post("/ingest", json=payload)
    assert resp_ingest.status_code == 200
    assert resp_ingest.json()["status"] == "ingested"
    assert resp_ingest.json()["dag_nodes_count"] == 2

    resp_v1_ingest = client.post("/api/v1/ingest", json=payload)
    assert resp_v1_ingest.status_code == 200
    assert resp_v1_ingest.json()["status"] == "ingested"

    # 2. Test /evaluate (both /evaluate and /api/v1/evaluate)
    eval_req = {
        "task_goal": "Migrate schema",
        "step": {
            "step_index": 0,
            "agent_name": "Dev",
            "action_payload": "DROP TABLE users;"
        }
    }
    resp_eval = client.post("/evaluate", json=eval_req)
    assert resp_eval.status_code == 200
    assert resp_eval.json()["anomaly_detected"] is True

    # 3. Test /resolve (both /resolve and /api/v1/resolve)
    resp_resolve = client.post("/resolve", json=payload)
    assert resp_resolve.status_code == 200
    data = resp_resolve.json()
    assert data["responsible_agent"] == "Dev"
    assert data["decisive_step_index"] == 0

    resp_v1_resolve = client.post("/api/v1/resolve", json=payload)
    assert resp_v1_resolve.status_code == 200
    assert resp_v1_resolve.json()["responsible_agent"] == "Dev"



