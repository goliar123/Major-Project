"""
Performance Evaluation Metrics for Automated Failure Attribution.
Computes Agent-level Accuracy, Step-level Accuracy, Strict Joint Accuracy,
Latency, and Token / Cost Efficiency.
"""
from typing import List, Dict, Any
from dataset.schema import AttributionVerdict, BenchmarkResult

class MetricsCalculator:
    @staticmethod
    def compute_benchmark_metrics(verdicts: List[AttributionVerdict], benchmark_name: str = "Who&When") -> BenchmarkResult:
        total = len(verdicts)
        if total == 0:
            return BenchmarkResult(
                benchmark_name=benchmark_name,
                total_traces=0,
                evaluated_traces=0,
                agent_level_accuracy=0.0,
                step_level_accuracy=0.0,
                strict_joint_accuracy=0.0,
                avg_execution_time_per_trace=0.0,
                cache_hit_rate=0.0,
                total_token_count=0,
                individual_verdicts=[]
            )

        correct_agent_count = sum(1 for v in verdicts if v.is_correct_agent is True)
        correct_step_count = sum(1 for v in verdicts if v.is_correct_step is True)
        strictly_correct_count = sum(1 for v in verdicts if v.is_strictly_correct is True)
        
        total_time = sum(v.execution_time_seconds for v in verdicts)
        total_hits = sum(v.cache_hits for v in verdicts)
        total_misses = sum(v.cache_misses for v in verdicts)
        total_tokens = sum(v.total_tokens_used for v in verdicts)

        total_queries = total_hits + total_misses
        hit_rate = (total_hits / total_queries * 100.0) if total_queries > 0 else 0.0

        return BenchmarkResult(
            benchmark_name=benchmark_name,
            total_traces=total,
            evaluated_traces=total,
            agent_level_accuracy=round(correct_agent_count / total * 100.0, 2),
            step_level_accuracy=round(correct_step_count / total * 100.0, 2),
            strict_joint_accuracy=round(strictly_correct_count / total * 100.0, 2),
            avg_execution_time_per_trace=round(total_time / total, 4),
            cache_hit_rate=round(hit_rate, 2),
            total_token_count=total_tokens,
            individual_verdicts=verdicts
        )

metrics_calculator = MetricsCalculator()
