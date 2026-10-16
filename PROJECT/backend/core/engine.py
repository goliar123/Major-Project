"""
Core Orchestrator for the Automated Failure Attribution Engine.
Executes the full 5-stage pipeline:
1. Step Segmentation
2. Cached Step-Wise LLM Evaluation
3. Information Dependency Linker (DAG)
4. Backward Causal Traversal
5. Root-Cause vs. Symptom Resolution
"""
import time
from typing import Optional, Dict, Any, List
from dataset.schema import MultiAgentTrace, AttributionVerdict, StepEvaluation
from core.segmentation import trace_segmenter
from core.step_judge import step_judge
from core.dependency_linker import dependency_linker
from core.backward_traversal import backward_traversal_resolver
from core.cache import cache_manager
from core.llm_client import llm_client
from config.logging_config import logger

class AttributionEngine:
    def __init__(self):
        self.segmenter = trace_segmenter
        self.judge = step_judge
        self.linker = dependency_linker
        self.resolver = backward_traversal_resolver
        self.cache = cache_manager

    def attribute_trace(self, trace: MultiAgentTrace) -> AttributionVerdict:
        """Runs end-to-end attribution on a single multi-agent trace."""
        start_time = time.time()
        initial_cache_hits = self.cache.hits
        initial_cache_misses = self.cache.misses
        initial_tokens = llm_client.total_tokens_consumed

        logger.info(f"Starting Failure Attribution for Trace: {trace.trace_id} ({trace.title or 'Untitled'})")

        # Phase 1: Step Segmentation & Context Token Budgeting
        segmented_steps = self.segmenter.segment_trace(trace)
        trace.steps = segmented_steps

        # Phase 2: Cached Step-Wise Evaluation
        evaluations: Dict[int, StepEvaluation] = {}
        for step in segmented_steps:
            eval_res = self.judge.evaluate_step(trace.task_goal, step)
            evaluations[step.step_index] = eval_res

        # Phase 3: Dependency Graph (DAG) Construction
        dag, edges = self.linker.build_dependency_dag(segmented_steps)

        # Phase 4 & 5: Backward Causal Traversal & Root-Cause Resolution
        verdict = self.resolver.resolve_root_cause(
            trace_id=trace.trace_id,
            task_goal=trace.task_goal,
            steps=segmented_steps,
            evaluations=evaluations,
            dag=dag,
            edges=edges
        )

        # Compute metrics against Ground Truth if present
        if trace.ground_truth:
            gt = trace.ground_truth
            agent_match = (verdict.responsible_agent.strip().lower() == gt.responsible_agent.strip().lower())
            step_match = (verdict.decisive_step_index == gt.decisive_step_index)
            verdict.is_correct_agent = agent_match
            verdict.is_correct_step = step_match
            verdict.is_strictly_correct = agent_match and step_match

        verdict.execution_time_seconds = round(time.time() - start_time, 4)
        verdict.cache_hits = self.cache.hits - initial_cache_hits
        verdict.cache_misses = self.cache.misses - initial_cache_misses
        verdict.total_tokens_used = llm_client.total_tokens_consumed - initial_tokens

        logger.info(
            f"Attribution Finished: Blamed [{verdict.responsible_agent}] at Step {verdict.decisive_step_index} "
            f"in {verdict.execution_time_seconds}s (Cache Hits: {verdict.cache_hits})"
        )
        return verdict

attribution_engine = AttributionEngine()
