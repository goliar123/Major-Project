"""
Real-Time Incremental Trace Monitor & Shadow Failure Attribution Engine.
Builds the information dependency DAG on-the-fly as agents execute, scores turns in
shadow memory without early intervention, and triggers backward causal traversal
upon terminal failure or output goal conflict.
"""
import time
from typing import Dict, Any, List, Optional, Tuple
import networkx as nx
from dataset.schema import (
    ExecutionStep,
    MultiAgentTrace,
    AttributionVerdict,
    StepEvaluation,
    DependencyEdge
)
from core.step_judge import step_judge
from core.dependency_linker import dependency_linker
from core.backward_traversal import backward_traversal_resolver
from config.logging_config import logger

class LiveTraceSession:
    def __init__(self, trace_id: str, task_goal: str, expected_output: Optional[str] = None):
        self.trace_id = trace_id
        self.task_goal = task_goal
        self.expected_output = expected_output
        self.steps: List[ExecutionStep] = []
        self.evaluations: Dict[int, StepEvaluation] = {}
        self.dag = nx.DiGraph()
        self.edges: List[DependencyEdge] = []
        self.start_time = time.time()
        self.shadow_anomalies: List[int] = []
        self.is_active = True

    def ingest_step(self, step: ExecutionStep) -> Tuple[StepEvaluation, List[DependencyEdge]]:
        """
        Incrementally adds a single execution turn to the session DAG,
        evaluates step health in shadow memory, and computes incoming causal edges.
        """
        step_idx = len(self.steps)
        step.step_index = step_idx
        if not step.step_id:
            step.step_id = f"step_{step_idx + 1}"

        self.steps.append(step)

        # 1. Shadow Evaluation (Background Step-Wise Judge)
        evaluation = step_judge.evaluate_step(self.task_goal, step)
        self.evaluations[step_idx] = evaluation

        if evaluation.anomaly_detected or evaluation.score < 0.7:
            self.shadow_anomalies.append(step_idx)
            logger.debug(f"[SHADOW ALERT] Step {step_idx} ({step.agent_name}) flagged: {evaluation.error_category}")

        # 2. Incremental DAG Node Creation
        self.dag.add_node(
            step_idx,
            step_id=step.step_id,
            agent=step.agent_name,
            action_type=step.action_type,
            score=evaluation.score,
            is_anomalous=evaluation.anomaly_detected
        )

        # 3. Dynamic Dependency Linkage with prior active turns
        new_edges: List[DependencyEdge] = []
        
        # A. Sequential Temporal Flow (i-1 -> i)
        if step_idx > 0:
            seq_edge = DependencyEdge(
                source_step_index=step_idx - 1,
                target_step_index=step_idx,
                dependency_type="data_flow",
                confidence=0.85
            )
            self.dag.add_edge(step_idx - 1, step_idx, type="data_flow", weight=0.85)
            new_edges.append(seq_edge)
            self.edges.append(seq_edge)

        # B. Message-Reply & Entity Data Flow across all prior steps
        for prior_idx in range(step_idx):
            prior_step = self.steps[prior_idx]
            
            # Message handoff
            if prior_step.recipient == step.agent_name:
                handoff_edge = DependencyEdge(
                    source_step_index=prior_idx,
                    target_step_index=step_idx,
                    dependency_type="message_reply",
                    confidence=0.90
                )
                self.dag.add_edge(prior_idx, step_idx, type="message_reply", weight=0.90)
                new_edges.append(handoff_edge)
                self.edges.append(handoff_edge)

            # Shared state / variable lineage
            extracted_entities = dependency_linker._extract_key_entities(
                (prior_step.action_payload + " " + (prior_step.output_state or "")).lower()
            )
            target_text = (step.action_payload + " " + (step.input_context or "")).lower()
            matched_entities = [ent for ent in extracted_entities if ent in target_text and len(ent) > 4]

            if matched_entities:
                entity_edge = DependencyEdge(
                    source_step_index=prior_idx,
                    target_step_index=step_idx,
                    data_variable=", ".join(matched_entities[:3]),
                    dependency_type="shared_state",
                    confidence=0.95
                )
                self.dag.add_edge(prior_idx, step_idx, type="shared_state", weight=0.95)
                new_edges.append(entity_edge)
                self.edges.append(entity_edge)

        return evaluation, new_edges

    def finish_session(self, final_output: str, status: str = "COMPLETED") -> Optional[AttributionVerdict]:
        """
        Evaluates terminal status. If the final output fails or conflicts with expectations,
        triggers backward causal traversal to isolate the root cause.
        """
        self.is_active = False
        duration = time.time() - self.start_time

        # Check for failure or conflict
        has_failed = status.upper() in ["FAILED", "FORCE_TERMINATED", "ERROR", "CRASHED"]
        has_conflict = False

        if self.expected_output and self.expected_output.strip():
            # Check if expected regex / keywords exist in final output
            if self.expected_output.lower() not in final_output.lower():
                has_conflict = True
                logger.warning(f"Session {self.trace_id} terminal conflict: Output did not contain '{self.expected_output}'.")

        # If clean completion without failure/conflict, return None (clean run)
        if not has_failed and not has_conflict and not self.shadow_anomalies:
            logger.info(f"Session {self.trace_id} completed CLEAN in {duration:.2f}s with 0 conflicts.")
            return None

        # Failure / Conflict occurred -> Trigger Backward Causal Traversal
        logger.info(f"Session {self.trace_id} concluded with anomalies (Failed={has_failed}, Conflict={has_conflict}). Triggering Backward Traversal.")
        
        verdict = backward_traversal_resolver.resolve_root_cause(
            trace_id=self.trace_id,
            task_goal=self.task_goal,
            steps=self.steps,
            evaluations=self.evaluations,
            dag=self.dag,
            edges=self.edges
        )
        return verdict


class LiveTraceMonitor:
    """Manager for multiple live trace monitoring sessions."""
    def __init__(self):
        self.sessions: Dict[str, LiveTraceSession] = {}

    def start_session(self, trace_id: str, task_goal: str, expected_output: Optional[str] = None) -> LiveTraceSession:
        session = LiveTraceSession(trace_id=trace_id, task_goal=task_goal, expected_output=expected_output)
        self.sessions[trace_id] = session
        logger.info(f"Started live trace session: {trace_id} (Goal: {task_goal[:60]}...)")
        return session

    def get_session(self, trace_id: str) -> Optional[LiveTraceSession]:
        return self.sessions.get(trace_id)

    def close_session(self, trace_id: str):
        if trace_id in self.sessions:
            del self.sessions[trace_id]

live_trace_monitor = LiveTraceMonitor()
