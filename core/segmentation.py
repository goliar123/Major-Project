"""
Trace Segmentation and Token Management Module.
Segments long multi-turn execution histories into discrete, bounded execution steps
to prevent context-window overflow and long-context degradation.
"""
from typing import List, Dict, Any, Optional
import re
from dataset.schema import ExecutionStep, MultiAgentTrace
from config.settings import settings
from config.logging_config import logger

class TraceSegmenter:
    def __init__(self, max_turn_tokens: int = 4096):
        self.max_turn_tokens = max_turn_tokens

    def segment_trace(self, trace: MultiAgentTrace) -> List[ExecutionStep]:
        """
        Validates and formats execution steps in a trace, truncating oversized step payloads
        if necessary while preserving critical error messages and semantic structures.
        """
        segmented_steps: List[ExecutionStep] = []

        for idx, step in enumerate(trace.steps):
            # Ensure correct sequence index
            step.step_index = idx
            
            # Truncate / compress oversized inputs or payloads
            processed_payload = self._bound_token_length(step.action_payload)
            processed_output = self._bound_token_length(step.output_state or "")
            processed_input = self._bound_token_length(step.input_context or "")

            bounded_step = ExecutionStep(
                step_id=step.step_id,
                step_index=idx,
                agent_name=step.agent_name,
                recipient=step.recipient or "All",
                action_type=step.action_type or "message",
                input_context=processed_input,
                action_payload=processed_payload,
                output_state=processed_output,
                timestamp=step.timestamp
            )
            segmented_steps.append(bounded_step)

        logger.debug(f"Segmented trace {trace.trace_id} into {len(segmented_steps)} bounded steps.")
        return segmented_steps

    def parse_custom_json(self, raw_dict: Dict[str, Any]) -> MultiAgentTrace:
        """
        Parses diverse multi-agent JSON payloads including LangGraph, CrewAI, AutoGen, MetaGPT,
        and standard Who&When schemas into a normalized MultiAgentTrace.
        """
        trace_id = raw_dict.get("run_id") or raw_dict.get("trace_id") or "trace_custom"
        workflow = raw_dict.get("workflow_name") or raw_dict.get("title") or "Multi-Agent Workflow"
        env_name = raw_dict.get("orchestrator") or raw_dict.get("environment_name") or "MultiAgent"
        
        # Determine steps list
        raw_steps = raw_dict.get("execution_trace") or raw_dict.get("steps") or []
        
        # Infer task goal
        task_goal = raw_dict.get("task_goal")
        if not task_goal and raw_steps:
            first_step = raw_steps[0]
            inputs = first_step.get("inputs") or {}
            task_goal = inputs.get("query") or inputs.get("task") or first_step.get("input_context") or f"Execute {workflow}"
        task_goal = task_goal or f"Execute {workflow}"

        steps: List[ExecutionStep] = []
        for idx, s in enumerate(raw_steps):
            agent = s.get("agent") or s.get("agent_name") or f"Agent_{idx+1}"
            action_type = s.get("action") or s.get("action_type") or "execution"
            original_step = s.get("step") or (idx + 1)
            status = s.get("status") or ""
            summary = s.get("summary") or s.get("reason") or ""
            
            # Format inputs
            inputs_val = s.get("inputs") or s.get("input_context") or s.get("tool_input") or ""
            if isinstance(inputs_val, dict):
                input_str = "\n".join([f"{k}: {v}" for k, v in inputs_val.items()])
            else:
                input_str = str(inputs_val)

            # Format payload
            payload_parts = []
            if s.get("action"):
                payload_parts.append(f"Action: {s.get('action')}")
            if summary:
                payload_parts.append(f"Summary: {summary}")
            if s.get("tool_name"):
                payload_parts.append(f"Tool: {s.get('tool_name')}")
            if s.get("tool_input"):
                payload_parts.append(f"Tool Input: {json.dumps(s.get('tool_input')) if isinstance(s.get('tool_input'), dict) else s.get('tool_input')}")
            if s.get("outputs"):
                payload_parts.append(f"Outputs: {json.dumps(s.get('outputs')) if isinstance(s.get('outputs'), dict) else s.get('outputs')}")
            if s.get("evaluation_verdict"):
                payload_parts.append(f"Evaluation Verdict: {s.get('evaluation_verdict')} (Reason: {s.get('reason')})")
            if s.get("remedy_instruction"):
                payload_parts.append(f"Remedy Instruction: {s.get('remedy_instruction')}")
            if s.get("action_payload"):
                payload_parts.append(str(s.get("action_payload")))

            action_payload = "\n".join(payload_parts) if payload_parts else str(s)

            # Format outputs / state
            out_val = s.get("tool_output") or s.get("output_state") or status
            if isinstance(out_val, dict):
                output_str = f"Status: {status}\n" + "\n".join([f"{k}: {v}" for k, v in out_val.items()])
            else:
                output_str = f"Status: {status} | {out_val}" if status else str(out_val)
            if summary and summary not in output_str:
                output_str += f"\nDetails: {summary}"

            steps.append(ExecutionStep(
                step_id=f"step_{original_step}",
                step_index=idx,
                agent_name=agent,
                recipient=s.get("recipient") or "NextStep",
                action_type=action_type,
                input_context=input_str,
                action_payload=action_payload,
                output_state=output_str
            ))

        return MultiAgentTrace(
            trace_id=trace_id,
            title=workflow,
            environment_name=env_name,
            task_goal=task_goal,
            total_steps=len(steps),
            steps=steps,
            raw_payload=raw_dict
        )

    def parse_raw_log_text(self, log_text: str, task_goal: str = "") -> MultiAgentTrace:
        """
        Parses raw unstructured text logs (e.g. standard console output of AutoGen/MetaGPT)
        into structured MultiAgentTrace steps using regex heuristics.
        """
        # Pattern for standard multi-agent logs: "[AgentName -> Recipient]: message"
        pattern = r"(?:\[?([A-Za-z0-9_-]+)\s*(?:->|to)\s*([A-Za-z0-9_-]+)\]?:\s*(.*?)(?=\n\[?[A-Za-z0-9_-]+\s*(?:->|to)|\Z))"
        matches = list(re.finditer(pattern, log_text, re.DOTALL | re.IGNORECASE))
        
        steps: List[ExecutionStep] = []
        if matches:
            for idx, m in enumerate(matches):
                sender = m.group(1).strip()
                recipient = m.group(2).strip()
                content = m.group(3).strip()
                steps.append(ExecutionStep(
                    step_index=idx,
                    agent_name=sender,
                    recipient=recipient,
                    action_type="message",
                    action_payload=content,
                    output_state="Message delivered."
                ))
        else:
            # Fallback line-by-line split
            lines = [l.strip() for l in log_text.splitlines() if l.strip()]
            for idx, line in enumerate(lines):
                steps.append(ExecutionStep(
                    step_index=idx,
                    agent_name=f"Agent_{idx % 2 + 1}",
                    recipient="All",
                    action_type="execution_step",
                    action_payload=line,
                    output_state=""
                ))

        return MultiAgentTrace(
            task_goal=task_goal or "Infer goal from execution log",
            total_steps=len(steps),
            steps=steps
        )

    def _bound_token_length(self, text: str) -> str:
        """Approximates word/token count and trims middle content if over limit."""
        words = text.split()
        if len(words) <= self.max_turn_tokens:
            return text
        
        # Keep head and tail to preserve both initial context and final status/error message
        head_count = int(self.max_turn_tokens * 0.6)
        tail_count = int(self.max_turn_tokens * 0.3)
        omitted = len(words) - (head_count + tail_count)
        
        trimmed_words = words[:head_count] + [f"\n... [Omitted {omitted} tokens for context window efficiency] ...\n"] + words[-tail_count:]
        return " ".join(trimmed_words)

trace_segmenter = TraceSegmenter()
