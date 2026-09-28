"""
Test for 150-step competitive intelligence synthesis trace.
"""
import json
import pytest
from core.segmentation import trace_segmenter
from core.engine import attribution_engine
from core.cache import cache_manager

def test_150_step_competitive_intelligence():
    cache_manager.clear()
    raw_payload = {
      "run_id": "run_m9a721df-6b83-4921-bc74-12ea4f58c709",
      "workflow_name": "competitive_intelligence_synthesis",
      "orchestrator": "LangGraph-MultiAgent-Engine",
      "status": "FAILED",
      "total_steps": 150,
      "execution_trace": [
        {"step": 1, "agent": "supervisor", "action": "plan_workflow", "status": "COMPLETED", "summary": "Partitioned goal into 4 company dossiers: Apex, Novus, Vantage, Lumina."},
        {"step": 19, "agent": "search_agent", "action": "fetch_url", "status": "WARNING", "summary": "Target URL returned HTTP 403 Forbidden (Cloudflare Bot Mitigation)."},
        {"step": 20, "agent": "search_agent", "action": "retry_with_headers", "status": "FAILED", "summary": "Browser header spoofing failed; CAPTCHA challenge encountered."},
        {"step": 48, "agent": "fact_checker_agent", "action": "validate_matrix", "status": "WARNING", "summary": "Vantage Tech row contains null value in field 'gross_margin'."},
        {"step": 144, "agent": "writer_agent", "action": "patch_table", "status": "COMPLETED", "summary": "Updated segment table values in document payload."},
        {"step": 148, "agent": "writer_agent", "action": "run_pydantic_validation", "status": "FAILED", "summary": "ValidationError: 'operating_margin' in companies['vantage'] was reset to NaN during step 144 table patch."},
        {"step": 149, "agent": "supervisor", "action": "attempt_emergency_hotpatch", "status": "FAILED", "summary": "Context window saturation: prompt injection for emergency hotpatch exceeded token buffer by 412 tokens."},
        {"step": 150, "agent": "writer_agent", "action": "abort_execution", "status": "FORCE_TERMINATED", "summary": "Fatal UnrecoverableSchemaError: Schema validation contract violated at terminal step."}
      ]
    }

    trace = trace_segmenter.parse_custom_json(raw_payload)
    assert len(trace.steps) == 8
    
    verdict = attribution_engine.attribute_trace(trace)
    assert verdict.responsible_agent in ["writer_agent", "search_agent"]
    print("Verdict:", verdict.responsible_agent, verdict.decisive_step_index)
    print("Explanation:", verdict.explanation)
