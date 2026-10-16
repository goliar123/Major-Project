"""
Baseline 3: Binary Search Trace Judge.
Performs hierarchical bisection across the trace steps to narrow down suspect region.
"""
from typing import Dict, Any, List
from dataset.schema import MultiAgentTrace, AttributionVerdict, NodeStatus
from core.step_judge import step_judge
from config.logging_config import logger

class BinarySearchBaseline:
    def __init__(self):
        self.judge = step_judge

    def attribute(self, trace: MultiAgentTrace) -> AttributionVerdict:
        if not trace.steps:
            return AttributionVerdict(
                trace_id=trace.trace_id,
                method_name="Baseline (Binary Search)",
                responsible_agent="Unknown",
                decisive_step_index=0,
                failure_type="empty",
                explanation="Empty trace."
            )

        low = 0
        high = len(trace.steps) - 1
        found_idx = high

        # Perform binary search over step indices
        while low <= high:
            mid = (low + high) // 2
            ev = self.judge.evaluate_step(trace.task_goal, trace.steps[mid])
            if ev.anomaly_detected or ev.score < 0.7:
                found_idx = mid
                high = mid - 1
            else:
                low = mid + 1

        blamed_step = trace.steps[found_idx]
        nodes = [
            NodeStatus(
                step_index=s.step_index,
                step_id=s.step_id,
                agent_name=s.agent_name,
                status="root_cause" if s.step_index == found_idx else "normal",
                score=0.0 if s.step_index == found_idx else 1.0,
                reason="Isolated via Binary Search" if s.step_index == found_idx else "Normal"
            )
            for s in trace.steps
        ]

        return AttributionVerdict(
            trace_id=trace.trace_id,
            method_name="Baseline (Binary Search)",
            responsible_agent=blamed_step.agent_name,
            decisive_step_index=found_idx,
            decisive_step_id=blamed_step.step_id,
            failure_type="binary_search_anomaly",
            explanation=f"[Binary Search Baseline] Isolated Step {found_idx} ({blamed_step.agent_name}) as earliest anomalous bisection midpoint.",
            graph_nodes=nodes,
            graph_edges=[]
        )

binary_search_baseline = BinarySearchBaseline()
