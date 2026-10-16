"""
Automated Pytest Unit & Integration Tests for Who&When Benchmark (ICML 2025).
Validates that the Automated Failure Attribution Engine accurately evaluates
real Who&When benchmark traces across both Hand-Crafted and Algorithm-Generated subsets.
"""
import pytest
from dataset.loader import dataset_loader
from core.engine import attribution_engine
from evaluation.evaluator import benchmark_evaluator

def test_who_and_when_dataset_integrity():
    """Asserts that all 184 Who&When benchmark traces are loaded with ground truth labels."""
    traces = dataset_loader.load_traces()
    assert len(traces) == 184, f"Expected 184 benchmark traces, found {len(traces)}"
    
    hand_crafted = [t for t in traces if t.trace_id.startswith("WW-HC")]
    algo_generated = [t for t in traces if t.trace_id.startswith("WW-AG")]
    
    assert len(hand_crafted) == 58, f"Expected 58 hand-crafted traces, found {len(hand_crafted)}"
    assert len(algo_generated) == 126, f"Expected 126 algorithm-generated traces, found {len(algo_generated)}"
    
    # Verify each trace has valid ground truth
    for t in traces:
        assert t.ground_truth is not None, f"Trace {t.trace_id} missing ground truth"
        assert t.ground_truth.responsible_agent, f"Trace {t.trace_id} missing responsible_agent"
        assert t.ground_truth.decisive_step_index >= 0, f"Trace {t.trace_id} invalid decisive_step_index"
        assert len(t.steps) > 0, f"Trace {t.trace_id} has zero steps"

def test_who_and_when_hand_crafted_subset():
    """Tests attribution on representative Hand-Crafted benchmark traces."""
    hc_traces = dataset_loader.load_traces(subset="hand_crafted")[:10]
    
    correct_agents = 0
    correct_steps = 0
    
    for trace in hc_traces:
        verdict = attribution_engine.attribute_trace(trace)
        gt = trace.ground_truth
        
        if verdict.responsible_agent.strip().lower() == gt.responsible_agent.strip().lower():
            correct_agents += 1
        if verdict.decisive_step_index == gt.decisive_step_index:
            correct_steps += 1
            
        assert len(verdict.graph_nodes) == len(trace.steps)
        assert verdict.execution_time_seconds < 1.0
        
    # High accuracy on sample hand-crafted traces
    agent_acc = correct_agents / len(hc_traces)
    step_acc = correct_steps / len(hc_traces)
    assert agent_acc >= 0.8, f"Hand-crafted agent accuracy too low: {agent_acc}"
    assert step_acc >= 0.8, f"Hand-crafted step accuracy too low: {step_acc}"

def test_who_and_when_algorithm_generated_subset():
    """Tests attribution on representative Algorithm-Generated benchmark traces."""
    ag_traces = dataset_loader.load_traces(subset="algorithm_generated")[:10]
    
    correct_agents = 0
    correct_steps = 0
    
    for trace in ag_traces:
        verdict = attribution_engine.attribute_trace(trace)
        gt = trace.ground_truth
        
        if verdict.responsible_agent.strip().lower() == gt.responsible_agent.strip().lower():
            correct_agents += 1
        if verdict.decisive_step_index == gt.decisive_step_index:
            correct_steps += 1
            
    agent_acc = correct_agents / len(ag_traces)
    step_acc = correct_steps / len(ag_traces)
    assert agent_acc >= 0.8, f"Algo-generated agent accuracy too low: {agent_acc}"
    assert step_acc >= 0.8, f"Algo-generated step accuracy too low: {step_acc}"

def test_who_and_when_accuracy_exceeds_baselines():
    """
    Verifies that the Proposed Two-Phase Backward Traversal engine outperforms
    the published All-at-Once monolithic LLM baseline (53.5% Agent / 14.2% Step).
    """
    sample_traces = dataset_loader.load_traces()[:20]
    result_proposed = benchmark_evaluator.evaluate_method("proposed", traces=sample_traces)
    result_all_at_once = benchmark_evaluator.evaluate_method("all_at_once", traces=sample_traces)
    
    # Proposed must significantly outperform monolithic baseline
    assert result_proposed.agent_level_accuracy > result_all_at_once.agent_level_accuracy
    assert result_proposed.step_level_accuracy > result_all_at_once.step_level_accuracy
    assert result_proposed.strict_joint_accuracy > result_all_at_once.strict_joint_accuracy

def test_who_and_when_subsecond_batch_execution():
    """Validates that a batch of 15 traces executes in under 1 second using prompt caching."""
    traces = dataset_loader.load_traces()[:15]
    result = benchmark_evaluator.evaluate_method("proposed", traces=traces)
    
    assert result.avg_execution_time_per_trace < 0.1, f"Average latency too high: {result.avg_execution_time_per_trace}s"
    assert result.cache_hit_rate >= 80.0, f"Expected high cache hit rate, got {result.cache_hit_rate}%"
