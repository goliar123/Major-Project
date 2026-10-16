"""
Baseline 2: Step-by-Step Isolated Evaluator.
Evaluates each step sequentially in isolation without information dependency tracking.
Suffers from symptom misattribution: blames the first step that displays an error symptom
rather than the upstream originating cause.
"""
from typing import Dict, Any, List
from dataset.schema import MultiAgentTrace, AttributionVerdict, NodeStatus
from core.step_judge import step_judge
from config.logging_config import logger

class StepByStepBaseline:
    def __init__(self):
        self.judge = step_judge

    def attribute(self, trace: MultiAgentTrace) -> AttributionVerdict:
        if not trace.steps:
            return AttributionVerdict(
                trace_id=trace.trace_id,
                method_name="Baseline (Step-by-Step Isolated)",
                responsible_agent="Unknown",
                decisive_step_index=0,
                failure_type="empty",
                explanation="Empty trace."
            )

        # Evaluate each step in isolation
        blamed_step_idx = len(trace.steps) - 1  # Default to last step
        first_failing_eval = None

        node_statuses = []
        for s in trace.steps:
            ev = self.judge.evaluate_step(trace.task_goal, s)
            # Naive approach: blames the LAST anomalous step or step with visible exception
            if ev.anomaly_detected or ev.score < 0.7:
                blamed_step_idx = s.step_index
                first_failing_eval = ev

        for s in trace.steps:
            node_statuses.append(NodeStatus(
                step_index=s.step_index,
                step_id=s.step_id,
                agent_name=s.agent_name,
                status="root_cause" if s.step_index == blamed_step_idx else "normal",
                score=0.0 if s.step_index == blamed_step_idx else 1.0,
                reason="Identified by isolated step-wise evaluation." if s.step_index == blamed_step_idx else "Normal"
            ))

        blamed_step = trace.steps[blamed_step_idx]
        reason = first_failing_eval.justification if first_failing_eval else "Identified as lowest scoring isolated step."

        return AttributionVerdict(
            trace_id=trace.trace_id,
            method_name="Baseline (Step-by-Step Isolated)",
            responsible_agent=blamed_step.agent_name,
            decisive_step_index=blamed_step_idx,
            decisive_step_id=blamed_step.step_id,
            failure_type="isolated_anomaly",
            explanation=f"[Step-by-Step Baseline] Blamed Agent '{blamed_step.agent_name}' at Step {blamed_step_idx} based on isolated symptom detection: {reason}",
            graph_nodes=node_statuses,
            graph_edges=[]
        )

step_by_step_baseline = StepByStepBaseline()
