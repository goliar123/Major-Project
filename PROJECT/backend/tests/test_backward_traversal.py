"""
Unit tests for Backward Causal Traversal and Root Cause Isolation.
"""
import pytest
import networkx as nx
from dataset.schema import ExecutionStep, StepEvaluation, DependencyEdge
from core.backward_traversal import BackwardTraversalResolver

def test_root_cause_isolation_from_symptom():
    resolver = BackwardTraversalResolver()
    
    steps = [
        ExecutionStep(step_index=0, agent_name="User", action_payload="Do migration"),
        ExecutionStep(step_index=1, agent_name="Architect", action_payload="DROP TABLE users"),
        ExecutionStep(step_index=2, agent_name="Coder", action_payload="Execute drop table"),
        ExecutionStep(step_index=3, agent_name="Tester", action_payload="Assert test failed: 0 records")
    ]

    # Create DAG: 0 -> 1 -> 2 -> 3
    dag = nx.DiGraph()
    dag.add_edges_from([(0, 1), (1, 2), (2, 3)])
    edges = [
        DependencyEdge(source_step_index=0, target_step_index=1),
        DependencyEdge(source_step_index=1, target_step_index=2),
        DependencyEdge(source_step_index=2, target_step_index=3)
    ]

    # Step 1 introduced the error; Steps 2 and 3 exhibited cascading symptoms
    evaluations = {
        0: StepEvaluation(step_index=0, step_id="s0", is_valid=True, score=1.0, anomaly_detected=False, justification="Normal"),
        1: StepEvaluation(step_index=1, step_id="s1", is_valid=False, score=0.0, anomaly_detected=True, error_category="destructive_sql", justification="Dropped table"),
        2: StepEvaluation(step_index=2, step_id="s2", is_valid=True, score=0.9, anomaly_detected=False, justification="Executed as requested"),
        3: StepEvaluation(step_index=3, step_id="s3", is_valid=False, score=0.1, anomaly_detected=True, error_category="assertion_fail", justification="Test failed")
    }

    verdict = resolver.resolve_root_cause(
        trace_id="test-trace-1",
        task_goal="Migrate DB",
        steps=steps,
        evaluations=evaluations,
        dag=dag,
        edges=edges
    )

    assert verdict.responsible_agent == "Architect"
    assert verdict.decisive_step_index == 1
    assert 3 in verdict.propagated_symptom_indices
