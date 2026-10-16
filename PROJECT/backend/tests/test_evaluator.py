"""
Unit tests for Benchmark Evaluation and Metrics Calculation.
"""
import pytest
from dataset.schema import AttributionVerdict
from evaluation.metrics import metrics_calculator

def test_metrics_calculation():
    verdicts = [
        AttributionVerdict(
            trace_id="t1", method_name="test", responsible_agent="A1", decisive_step_index=1,
            failure_type="bug", explanation="e1", is_correct_agent=True, is_correct_step=True, is_strictly_correct=True,
            execution_time_seconds=0.1, cache_hits=2, cache_misses=1
        ),
        AttributionVerdict(
            trace_id="t2", method_name="test", responsible_agent="A2", decisive_step_index=2,
            failure_type="bug", explanation="e2", is_correct_agent=True, is_correct_step=False, is_strictly_correct=False,
            execution_time_seconds=0.2, cache_hits=3, cache_misses=0
        )
    ]

    result = metrics_calculator.compute_benchmark_metrics(verdicts, benchmark_name="TestBench")

    assert result.total_traces == 2
    assert result.agent_level_accuracy == 100.0
    assert result.step_level_accuracy == 50.0
    assert result.strict_joint_accuracy == 50.0
    assert result.cache_hit_rate == 83.33  # 5 hits / 6 queries = 83.33%
