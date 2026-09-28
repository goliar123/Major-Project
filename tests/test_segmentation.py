"""
Unit tests for Trace Segmentation & Token Management.
"""
import pytest
from dataset.schema import MultiAgentTrace, ExecutionStep
from core.segmentation import TraceSegmenter

def test_segment_trace():
    segmenter = TraceSegmenter(max_turn_tokens=100)
    steps = [
        ExecutionStep(step_index=0, agent_name="AgentA", action_payload="Short text"),
        ExecutionStep(step_index=1, agent_name="AgentB", action_payload=" ".join(["word"] * 250))
    ]
    trace = MultiAgentTrace(task_goal="Test Goal", steps=steps)
    segmented = segmenter.segment_trace(trace)

    assert len(segmented) == 2
    assert segmented[0].step_index == 0
    assert len(segmented[1].action_payload.split()) <= 120
    assert "Omitted" in segmented[1].action_payload

def test_parse_raw_log_text():
    segmenter = TraceSegmenter()
    raw_log = """[User -> Planner]: Build a login page.
[Planner -> Developer]: Use FastAPI and JWT.
[Developer -> Tester]: Generated auth token code."""
    trace = segmenter.parse_raw_log_text(raw_log, task_goal="Build login page")

    assert len(trace.steps) == 3
    assert trace.steps[0].agent_name == "User"
    assert trace.steps[0].recipient == "Planner"
    assert trace.steps[1].agent_name == "Planner"
    assert trace.steps[2].agent_name == "Developer"
