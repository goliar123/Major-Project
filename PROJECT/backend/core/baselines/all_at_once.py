"""
Baseline 1: All-at-Once LLM-as-a-Judge.
Dumps the entire multi-agent trace history into a single monolithic prompt.
Published Baseline: ~53.5% Agent-level, ~14.2% Step-level accuracy.
Vulnerable to context window overflow on traces > 32k tokens.
"""
from typing import Dict, Any, List
from dataset.schema import MultiAgentTrace, AttributionVerdict, NodeStatus
from core.llm_client import llm_client
from core.cache import cache_manager
from config.settings import settings
from config.logging_config import logger

ALL_AT_ONCE_PROMPT_TEMPLATE = """You are evaluating a failed multi-agent execution trace.
Task Goal: {task_goal}

Execution Trace History:
{trace_history}

Analyze the entire trace and determine:
1. Which agent is responsible for the failure?
2. At which exact step index (0-indexed) did the decisive error occur?
3. Provide an explanation.

Output valid JSON only:
{{
  "responsible_agent": "ExactAgentName",
  "decisive_step_index": 0,
  "explanation": "Reason for failure..."
}}
"""

class AllAtOnceBaseline:
    def __init__(self):
        self.llm = llm_client
        self.cache = cache_manager

    def attribute(self, trace: MultiAgentTrace) -> AttributionVerdict:
        history_lines = []
        for s in trace.steps:
            history_lines.append(
                f"[Step {s.step_index}] Agent: {s.agent_name} -> Recipient: {s.recipient}\n"
                f"Action: {s.action_type}\n"
                f"Payload: {s.action_payload}\n"
                f"State: {s.output_state}\n"
            )
        trace_history = "\n".join(history_lines)
        
        prompt = ALL_AT_ONCE_PROMPT_TEMPLATE.format(
            task_goal=trace.task_goal,
            trace_history=trace_history
        )

        model_name = settings.LLM_MODEL
        cached = self.cache.get(prompt, model_name)
        if cached:
            res = cached
        else:
            res = self.llm.query_json(prompt)
            self.cache.set(prompt, res, model_name)

        agent = res.get("responsible_agent", trace.steps[-1].agent_name if trace.steps else "Unknown")
        step_idx = int(res.get("decisive_step_index", len(trace.steps) - 1 if trace.steps else 0))
        # Ensure within bounds
        if step_idx >= len(trace.steps):
            step_idx = len(trace.steps) - 1
        if step_idx < 0:
            step_idx = 0

        explanation = res.get("explanation", "Evaluated using All-at-Once monolithic baseline.")

        nodes = [
            NodeStatus(
                step_index=s.step_index,
                step_id=s.step_id,
                agent_name=s.agent_name,
                status="root_cause" if s.step_index == step_idx else "normal",
                score=0.0 if s.step_index == step_idx else 1.0,
                reason="Flagged by All-at-Once judge" if s.step_index == step_idx else "Normal"
            )
            for s in trace.steps
        ]

        return AttributionVerdict(
            trace_id=trace.trace_id,
            method_name="Baseline (All-at-Once)",
            responsible_agent=agent,
            decisive_step_index=step_idx,
            failure_type="baseline_judgement",
            explanation=f"[All-at-Once Baseline] {explanation}",
            graph_nodes=nodes,
            graph_edges=[]
        )

all_at_once_baseline = AllAtOnceBaseline()
