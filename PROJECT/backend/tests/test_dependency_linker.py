"""
Unit tests for Dependency Linker and DAG Construction.
"""
import pytest
from dataset.schema import ExecutionStep
from core.dependency_linker import DependencyLinker

def test_dag_construction():
    linker = DependencyLinker()
    steps = [
        ExecutionStep(step_index=0, agent_name="Architect", recipient="Coder", action_payload="Define function calc_profit()"),
        ExecutionStep(step_index=1, agent_name="Coder", recipient="Tester", action_payload="Implemented def calc_profit(): return revenue - cost", input_context="Define function calc_profit()"),
        ExecutionStep(step_index=2, agent_name="Tester", recipient="Architect", action_payload="Ran unit tests on calc_profit", input_context="Implemented def calc_profit(): return revenue - cost")
    ]

    G, edges = linker.build_dependency_dag(steps)

    assert G.number_of_nodes() == 3
    assert G.has_edge(0, 1)
    assert G.has_edge(1, 2)
    assert len(edges) >= 2
