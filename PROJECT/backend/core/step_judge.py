"""
Cached Step-Wise LLM Evaluator.
Evaluates individual steps against immediate input context and overarching task goals.
Integrates SHA256 prompt hashing cache to prevent duplicate computation.
"""
from typing import Dict, Any, Tuple
from config.settings import settings
from config.logging_config import logger
from dataset.schema import ExecutionStep, StepEvaluation
from core.cache import cache_manager
from core.llm_client import llm_client

STEP_JUDGE_SYSTEM_PROMPT = """You are an expert diagnostic evaluator for LLM-based Multi-Agent Systems.
Your goal is to evaluate a single execution step within a multi-agent collaboration.
Analyze whether the action taken by the agent is logically valid, satisfies task constraints, or introduces an anomaly/bug.
Distinguish between:
1. Originating Error: The agent introduced a bug, wrong logic, invalid parameters, or security vulnerability.
2. Propagated Symptom: The agent received flawed or corrupted data from an upstream agent and merely reported or crashed because of it.

You must output valid JSON with the following schema:
{
  "is_valid": true | false,
  "score": float between 0.0 (total failure) and 1.0 (completely correct),
  "anomaly_detected": true | false,
  "error_category": string or null,
  "is_propagated_symptom": true | false,
  "justification": "concise explanation of why this step is normal or anomalous"
}
"""

class StepJudge:
    def __init__(self):
        self.cache = cache_manager
        self.llm = llm_client

    def evaluate_step(self, task_goal: str, step: ExecutionStep) -> StepEvaluation:
        """Evaluates a single execution step, using SHA256 caching."""
        prompt = self._build_prompt(task_goal, step)
        model_name = settings.LLM_MODEL
        prompt_hash = self.cache.compute_hash(prompt, model_name)

        # Check Cache
        cached_result = self.cache.get(prompt, model_name)
        if cached_result:
            logger.debug(f"[CACHE HIT] Step {step.step_index} evaluated from cache.")
            eval_obj = StepEvaluation(
                step_index=step.step_index,
                step_id=step.step_id,
                is_valid=cached_result.get("is_valid", True),
                score=float(cached_result.get("score", 1.0)),
                anomaly_detected=cached_result.get("anomaly_detected", False),
                error_category=cached_result.get("error_category"),
                justification=cached_result.get("justification", "Evaluated from cache."),
                prompt_hash=prompt_hash,
                cached=True
            )
            step.evaluation = eval_obj
            return eval_obj

        # Cache Miss: Query LLM
        logger.debug(f"[CACHE MISS] Querying LLM for step {step.step_index} ({step.agent_name}).")
        raw_verdict = self.llm.query_json(prompt, system_prompt=STEP_JUDGE_SYSTEM_PROMPT)

        # Store in Cache
        self.cache.set(prompt, raw_verdict, model_name)

        eval_obj = StepEvaluation(
            step_index=step.step_index,
            step_id=step.step_id,
            is_valid=raw_verdict.get("is_valid", True),
            score=float(raw_verdict.get("score", 1.0)),
            anomaly_detected=raw_verdict.get("anomaly_detected", False),
            error_category=raw_verdict.get("error_category"),
            justification=raw_verdict.get("justification", "Evaluated by LLM Judge."),
            prompt_hash=prompt_hash,
            cached=False
        )
        step.evaluation = eval_obj
        return eval_obj

    def _build_prompt(self, task_goal: str, step: ExecutionStep) -> str:
        """Constructs canonical prompt string for step evaluation."""
        return f"""### STEP-WISE EVALUATION
Task Goal: {task_goal}
Step Index: {step.step_index}
Agent: {step.agent_name}
Recipient: {step.recipient}
Action Type: {step.action_type}

Input Context:
{step.input_context or "[None/Initial Step]"}

Action Payload:
{step.action_payload or "[Empty Payload]"}

Output State:
{step.output_state or "[No State Returned]"}
"""

step_judge = StepJudge()
