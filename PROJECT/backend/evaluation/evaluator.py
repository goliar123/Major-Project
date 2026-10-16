"""
Benchmark Evaluator Harness for Who&When and Multi-Agent Failure Attribution.
Runs comparative evaluations between the Proposed Dependency-Aware Engine and Baselines.
"""
from typing import List, Dict, Any, Optional
from dataset.schema import MultiAgentTrace, AttributionVerdict, BenchmarkResult
from dataset.loader import dataset_loader
from core.engine import attribution_engine
from core.baselines.all_at_once import all_at_once_baseline
from core.baselines.step_by_step import step_by_step_baseline
from core.baselines.binary_search import binary_search_baseline
from evaluation.metrics import metrics_calculator
from config.logging_config import logger

class BenchmarkEvaluator:
    def __init__(self):
        self.methods = {
            "proposed": attribution_engine.attribute_trace,
            "all_at_once": all_at_once_baseline.attribute,
            "step_by_step": step_by_step_baseline.attribute,
            "binary_search": binary_search_baseline.attribute
        }

    def evaluate_method(
        self,
        method_name: str,
        traces: Optional[List[MultiAgentTrace]] = None,
        subset: Optional[str] = None,
        max_traces: Optional[int] = None
    ) -> BenchmarkResult:
        """Evaluates a single method on a list of traces."""
        if traces is None:
            traces = dataset_loader.load_traces(subset=subset)

        if max_traces:
            traces = traces[:max_traces]

        method_func = self.methods.get(method_name)
        if not method_func:
            raise ValueError(f"Unknown method '{method_name}'. Available: {list(self.methods.keys())}")

        verdicts: List[AttributionVerdict] = []
        logger.info(f"Running evaluation for method '{method_name}' on {len(traces)} traces...")

        for trace in traces:
            try:
                verdict = method_func(trace)
                
                # Check accuracy against ground truth
                if trace.ground_truth:
                    gt = trace.ground_truth
                    agent_match = (verdict.responsible_agent.strip().lower() == gt.responsible_agent.strip().lower())
                    step_match = (verdict.decisive_step_index == gt.decisive_step_index)
                    verdict.is_correct_agent = agent_match
                    verdict.is_correct_step = step_match
                    verdict.is_strictly_correct = agent_match and step_match

                verdicts.append(verdict)
            except Exception as e:
                logger.error(f"Error evaluating trace {trace.trace_id} with {method_name}: {e}")

        benchmark_title = f"Who&When ({subset or 'All'}) - {method_name}"
        return metrics_calculator.compute_benchmark_metrics(verdicts, benchmark_name=benchmark_title)

    def run_comparative_benchmark(
        self,
        traces: Optional[List[MultiAgentTrace]] = None,
        subset: Optional[str] = None,
        max_traces: Optional[int] = None
    ) -> Dict[str, BenchmarkResult]:
        """Runs all methods side-by-side to generate a comparative analysis table."""
        if traces is None:
            traces = dataset_loader.load_traces(subset=subset)
        if max_traces:
            traces = traces[:max_traces]

        results = {}
        for method_name in ["all_at_once", "step_by_step", "binary_search", "proposed"]:
            results[method_name] = self.evaluate_method(
                method_name=method_name,
                traces=traces,
                subset=subset
            )
        return results

benchmark_evaluator = BenchmarkEvaluator()
