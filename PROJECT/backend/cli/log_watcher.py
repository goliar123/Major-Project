"""
Streaming Log Watcher and Multi-Agent Event Parser.
Tails growing log files, reads piped standard input, and converts raw events into structured ExecutionSteps.
"""
import time
import os
import json
import re
from typing import Generator, Optional, Dict, Any, Union
from pathlib import Path
from dataset.schema import ExecutionStep
from config.logging_config import logger

class StreamingLogWatcher:
    @staticmethod
    def tail_file(file_path: Union[str, Path], poll_interval: float = 0.2) -> Generator[str, None, None]:
        """
        Yields newly appended lines from a file in real-time (like tail -f).
        """
        p = Path(file_path)
        while not p.exists():
            logger.debug(f"Waiting for log file to be created: {file_path}")
            time.sleep(0.5)

        with open(p, "r", encoding="utf-8", errors="replace") as f:
            # Go to the beginning of the file to read existing contents first
            while True:
                line = f.readline()
                if line:
                    yield line
                else:
                    time.sleep(poll_interval)

    @staticmethod
    def parse_event_line(line: str, step_index: int = 0) -> Optional[ExecutionStep]:
        """
        Parses an incoming raw line or JSON string into an ExecutionStep.
        """
        stripped = line.strip()
        if not stripped:
            return None

        # 1. Try parsing structured JSON
        if (stripped.startswith("{") and stripped.endswith("}")) or (stripped.startswith("[{") and stripped.endswith("}]")):
            try:
                data = json.loads(stripped)
                if isinstance(data, list) and data:
                    data = data[0]
                if isinstance(data, dict):
                    agent = data.get("agent") or data.get("agent_name") or data.get("node") or "Agent"
                    action_type = data.get("action") or data.get("action_type") or "execution"
                    
                    # Extract payload & summary
                    summary = data.get("summary") or data.get("reason") or data.get("error") or ""
                    payload = data.get("action_payload") or data.get("tool_input") or data.get("outputs") or summary or json.dumps(data)
                    if isinstance(payload, (dict, list)):
                        payload = json.dumps(payload)

                    status = data.get("status") or "SUCCESS"
                    out_state = data.get("tool_output") or data.get("output_state") or status
                    if isinstance(out_state, (dict, list)):
                        out_state = json.dumps(out_state)

                    return ExecutionStep(
                        step_id=f"step_{data.get('step', step_index + 1)}",
                        step_index=step_index,
                        agent_name=agent,
                        recipient=data.get("recipient") or "NextStep",
                        action_type=action_type,
                        input_context=str(data.get("inputs") or data.get("input_context") or ""),
                        action_payload=f"{payload} | {summary}" if summary and summary not in payload else payload,
                        output_state=f"Status: {status} | {out_state}"
                    )
            except Exception:
                pass

        # 2. Check standard AutoGen / ChatDev format: "[Sender -> Recipient]: Message"
        autogen_match = re.match(r"^\[?([A-Za-z0-9_-]+)\s*(?:->|to)\s*([A-Za-z0-9_-]+)\]?:\s*(.*)$", stripped, re.DOTALL)
        if autogen_match:
            sender = autogen_match.group(1).strip()
            recipient = autogen_match.group(2).strip()
            content = autogen_match.group(3).strip()
            return ExecutionStep(
                step_id=f"step_{step_index + 1}",
                step_index=step_index,
                agent_name=sender,
                recipient=recipient,
                action_type="message",
                input_context="Piped dialogue stream",
                action_payload=content,
                output_state="Message delivered"
            )

        # 3. Check simple agent tag format: "[AgentName]: Message"
        tag_match = re.match(r"^\[([A-Za-z0-9_-]+)\]:\s*(.*)$", stripped, re.DOTALL)
        if tag_match:
            sender = tag_match.group(1).strip()
            content = tag_match.group(2).strip()
            return ExecutionStep(
                step_id=f"step_{step_index + 1}",
                step_index=step_index,
                agent_name=sender,
                recipient="Group",
                action_type="execution_step",
                input_context="",
                action_payload=content,
                output_state="Delivered"
            )

        # 4. Fallback unstructured log line
        return ExecutionStep(
            step_id=f"step_{step_index + 1}",
            step_index=step_index,
            agent_name=f"Worker_{step_index % 3 + 1}",
            recipient="NextStep",
            action_type="log_line",
            input_context="",
            action_payload=stripped,
            output_state=""
        )

log_watcher = StreamingLogWatcher()
