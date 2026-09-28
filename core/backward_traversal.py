"""
Backward Causal Traversal and Root-Cause Resolver.
Traverses the dependency DAG backwards from the manifest failure symptom to isolate
the earliest originating error step (Root Cause) from downstream inherited symptoms.
"""
from typing import List, Dict, Set, Tuple, Optional
import networkx as nx
from dataset.schema import (
    ExecutionStep,
    AttributionVerdict,
    StepEvaluation,
    DependencyEdge,
    NodeStatus
)
from config.logging_config import logger

class BackwardTraversalResolver:
    def resolve_root_cause(
        self,
        trace_id: str,
        task_goal: str,
        steps: List[ExecutionStep],
        evaluations: Dict[int, StepEvaluation],
        dag: nx.DiGraph,
        edges: List[DependencyEdge]
    ) -> AttributionVerdict:
        """
        Executes backward traversal on DAG to find root-cause step.
        """
        num_steps = len(steps)
        if num_steps == 0:
            return AttributionVerdict(
                trace_id=trace_id,
                method_name="Dependency-Aware Backward Traversal",
                responsible_agent="None",
                decisive_step_index=0,
                failure_type="empty_trace",
                explanation="No execution steps provided."
            )

        # 1. Identify all anomalous / low-scoring steps
        anomalous_indices: List[int] = []
        for idx in range(num_steps):
            ev = evaluations.get(idx)
            if ev and (ev.anomaly_detected or ev.score < 0.7):
                anomalous_indices.append(idx)

        # If no anomaly was flagged by step judge, fallback to final step as failure symptom
        if not anomalous_indices:
            anomalous_indices = [num_steps - 1]

        # 2. Backward traversal from the latest failure point
        manifest_failure_idx = anomalous_indices[-1]
        
        # Traverse backwards to find the earliest invalid node in the causal ancestor subgraph
        causal_ancestors: Set[int] = nx.ancestors(dag, manifest_failure_idx)
        causal_ancestors.add(manifest_failure_idx)
        
        # Candidate failure steps that lie within the causal path leading to the symptom
        causal_anomalies = sorted([idx for idx in anomalous_indices if idx in causal_ancestors])

        if not causal_anomalies:
            causal_anomalies = [manifest_failure_idx]

        # 3. Root Cause Isolation: Find earliest anomaly whose parents are clean / valid
        root_cause_idx = causal_anomalies[0]
        for cand_idx in causal_anomalies:
            predecessors = list(dag.predecessors(cand_idx))
            # Check if any parent was already anomalous
            parent_anomalies = [p for p in predecessors if p in anomalous_indices and p < cand_idx]
            if not parent_anomalies:
                # This step is the source of the corruption!
                root_cause_idx = cand_idx
                break

        # 4. Partition anomalies into Root Cause vs Propagated Symptoms
        root_step = steps[root_cause_idx]
        root_eval = evaluations.get(root_cause_idx)
        
        propagated_symptoms = [idx for idx in anomalous_indices if idx != root_cause_idx]
        
        # Build causal dependency chain from root cause to final failure
        try:
            if root_cause_idx == manifest_failure_idx:
                causal_chain = [root_cause_idx]
            else:
                causal_chain = nx.shortest_path(dag, source=root_cause_idx, target=manifest_failure_idx)
        except Exception:
            causal_chain = [root_cause_idx, manifest_failure_idx]

        # Identify key multi-tier failure roles
        upstream_triggers = [i for i in anomalous_indices if evaluations.get(i) and evaluations[i].error_category in ["scraping_block", "url_parameter_corruption", "destructive_sql_query", "clinical_contraindication"]]
        code_bugs = [i for i in anomalous_indices if evaluations.get(i) and evaluations[i].error_category in ["state_tree_corruption", "validation_failure", "off_by_one_error", "mathematical_error", "invalid_hyperparameter"]]
        recovery_failures = [i for i in anomalous_indices if evaluations.get(i) and evaluations[i].error_category in ["context_overflow", "recursion_limit_halt"]]

        # 5. Format graph node statuses for UI visualizer
        node_statuses: List[NodeStatus] = []
        for idx, s in enumerate(steps):
            ev = evaluations.get(idx)
            score = ev.score if ev else 1.0
            
            if idx == root_cause_idx:
                status = "root_cause"
                reason = ev.justification if ev else "Originating root cause error step."
            elif idx in propagated_symptoms:
                status = "propagated_symptom"
                reason = f"Propagated downstream symptom inheriting flawed state: {ev.justification if ev else 'Inherited anomaly'}"
            else:
                status = "normal"
                reason = ev.justification if ev else "Normal execution step."

            node_statuses.append(NodeStatus(
                step_index=idx,
                step_id=s.step_id,
                agent_name=s.agent_name,
                status=status,
                score=score,
                reason=reason
            ))

        failure_category = root_eval.error_category if (root_eval and root_eval.error_category) else "agent_logic_flaw"
        
        # Construct multi-tier explanation
        explanation_parts = [
            f"Agent '{root_step.agent_name}' at Step {root_step.step_id.replace('step_', '') or root_cause_idx} initiated the failure chain: {root_eval.justification if root_eval else 'Earliest invalid step.'}"
        ]

        if code_bugs and code_bugs[0] != root_cause_idx:
            bug_step = steps[code_bugs[0]]
            explanation_parts.append(f"\n• Primary Bug: Agent '{bug_step.agent_name}' ({bug_step.step_id}) - {evaluations[code_bugs[0]].justification}")
        
        if recovery_failures:
            rec_step = steps[recovery_failures[0]]
            explanation_parts.append(f"\n• Secondary Failure (Recovery Breakdown): Agent '{rec_step.agent_name}' ({rec_step.step_id}) - {evaluations[recovery_failures[0]].justification}")

        if propagated_symptoms:
            explanation_parts.append(f"\n• Downstream Symptom Steps: {propagated_symptoms} exhibited cascading effects leading to final abort.")

        explanation = "\n".join(explanation_parts)

        logger.info(f"Resolved Root Cause: Agent '{root_step.agent_name}' at Step {root_cause_idx} for trace {trace_id}")

        return AttributionVerdict(
            trace_id=trace_id,
            method_name="Dependency-Aware Backward Traversal",
            responsible_agent=root_step.agent_name,
            decisive_step_index=root_cause_idx,
            decisive_step_id=root_step.step_id,
            failure_type=failure_category,
            explanation=explanation,
            root_cause_step=root_step,
            propagated_symptom_indices=propagated_symptoms,
            causal_dependency_chain=causal_chain,
            graph_nodes=node_statuses,
            graph_edges=edges
        )

backward_traversal_resolver = BackwardTraversalResolver()
