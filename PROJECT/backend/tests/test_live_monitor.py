"""
Unit tests for LiveTraceMonitor, StreamingLogWatcher, and Real-Time Incremental DAG attribution.
"""
import pytest
from core.live_monitor import live_trace_monitor, LiveTraceSession
from cli.log_watcher import log_watcher
from dataset.schema import ExecutionStep

def test_live_session_clean_run():
    session = live_trace_monitor.start_session(
        trace_id="test_live_clean",
        task_goal="Generate summary report for Q2 earnings",
        expected_output="Apex Silicon"
    )

    step1 = ExecutionStep(
        step_index=0,
        agent_name="Coordinator",
        action_type="plan",
        action_payload="Querying Q2 revenue",
        output_state="Task planned"
    )
    eval1, edges1 = session.ingest_step(step1)
    assert eval1.score >= 0.7
    assert len(session.dag.nodes) == 1

    step2 = ExecutionStep(
        step_index=1,
        agent_name="Analyst",
        action_type="draft",
        action_payload="Apex Silicon generated $14.2B in Q2.",
        output_state="Report assembled"
    )
    eval2, edges2 = session.ingest_step(step2)
    assert len(session.dag.nodes) == 2
    assert len(edges2) >= 1  # Sequential data_flow edge

    # Successful completion matching expected output
    verdict = session.finish_session(
        final_output="Apex Silicon generated $14.2B in Q2. Summary complete.",
        status="COMPLETED"
    )
    assert verdict is None  # Clean run, no attribution needed!

def test_live_session_conflict_triggered_attribution():
    session = live_trace_monitor.start_session(
        trace_id="test_live_conflict",
        task_goal="Migrate database and preserve users table",
        expected_output="users table preserved"
    )

    # Step 0: Plan
    session.ingest_step(ExecutionStep(
        step_index=0,
        agent_name="Planner",
        action_type="plan",
        action_payload="Plan DB migration"
    ))

    # Step 1: Flawed action (DROP TABLE)
    session.ingest_step(ExecutionStep(
        step_index=1,
        agent_name="DBArchitect",
        action_type="sql",
        action_payload="DROP TABLE users; -- destructive command",
        output_state="Table dropped."
    ))

    # Step 2: Downstream symptom
    session.ingest_step(ExecutionStep(
        step_index=2,
        agent_name="Tester",
        action_type="test",
        action_payload="AssertionError: 0 records found in users table",
        output_state="Test failed."
    ))

    assert len(session.dag.nodes) == 3
    assert len(session.shadow_anomalies) >= 1

    # Conclude with conflict
    verdict = session.finish_session(
        final_output="Migration aborted due to missing records.",
        status="FAILED"
    )

    assert verdict is not None
    assert verdict.responsible_agent == "DBArchitect"
    assert verdict.decisive_step_index == 1
    print(f"Attributed to: {verdict.responsible_agent} at Step {verdict.decisive_step_index}")

def test_log_watcher_parsing():
    autogen_line = "[Architect -> Developer]: Implement the auth middleware."
    step = log_watcher.parse_event_line(autogen_line, step_index=0)
    assert step is not None
    assert step.agent_name == "Architect"
    assert step.recipient == "Developer"

    json_line = '{"step": 144, "agent": "writer_agent", "action": "patch_table", "status": "FAILED", "summary": "Reset to NaN"}'
    step_json = log_watcher.parse_event_line(json_line, step_index=1)
    assert step_json is not None
    assert step_json.agent_name == "writer_agent"
    assert "Reset to NaN" in step_json.action_payload
