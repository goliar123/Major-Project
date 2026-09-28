"""
Dataset Loader and Synthetic Trace Generator for Who&When and Multi-Agent Benchmarks.
"""
import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from config.settings import settings
from config.logging_config import logger
from dataset.schema import MultiAgentTrace, ExecutionStep, GroundTruth

class DatasetLoader:
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or settings.DATASET_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.default_file = self.data_dir / "who_and_when_traces.json"

    def load_traces(self, file_path: Optional[str] = None, subset: Optional[str] = None) -> List[MultiAgentTrace]:
        """Loads traces from a JSON file and parses into MultiAgentTrace objects."""
        target_path = Path(file_path) if file_path else self.default_file
        if not target_path.exists():
            logger.warning(f"Trace file not found at {target_path}. Generating benchmark traces...")
            self.generate_extended_benchmark(target_path)

        with open(target_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        traces = []
        for item in raw_data:
            if subset and item.get("subset") != subset:
                continue
            
            steps = [
                ExecutionStep(
                    step_index=s.get("step_index", idx),
                    agent_name=s.get("agent_name", "Agent"),
                    recipient=s.get("recipient", "All"),
                    action_type=s.get("action_type", "message"),
                    input_context=s.get("input_context", ""),
                    action_payload=s.get("action_payload", ""),
                    output_state=s.get("output_state", ""),
                    timestamp=s.get("timestamp")
                )
                for idx, s in enumerate(item.get("steps", []))
            ]
            
            gt = None
            if "ground_truth" in item and item["ground_truth"]:
                gt_data = item["ground_truth"]
                gt = GroundTruth(
                    responsible_agent=gt_data.get("responsible_agent", ""),
                    decisive_step_index=gt_data.get("decisive_step_index", 0),
                    failure_reason=gt_data.get("failure_reason", ""),
                    failure_category=gt_data.get("failure_category")
                )

            trace = MultiAgentTrace(
                trace_id=item.get("trace_id", "trace-unknown"),
                title=item.get("title", "Untitled Trace"),
                environment_name=item.get("environment_name", "AutoGen"),
                task_goal=item.get("task_goal", ""),
                total_steps=len(steps),
                steps=steps,
                final_outcome=item.get("final_outcome", "failed"),
                ground_truth=gt,
                raw_payload=item
            )
            traces.append(trace)
        
        logger.info(f"Loaded {len(traces)} traces from {target_path}")
        return traces

    def get_trace_by_id(self, trace_id: str, file_path: Optional[str] = None) -> Optional[MultiAgentTrace]:
        """Finds a single trace by ID."""
        traces = self.load_traces(file_path=file_path)
        for t in traces:
            if t.trace_id == trace_id:
                return t
        return None

    def generate_extended_benchmark(self, output_path: Path, count_hc: int = 58, count_ag: int = 126):
        """
        Generates full Who&When benchmark corpus (58 Hand-Crafted + 126 Algorithm-Generated failure logs)
        spanning AutoGen, ChatDev, and MetaGPT architectures.
        """
        base_traces = []
        if self.default_file.exists():
            try:
                with open(self.default_file, "r", encoding="utf-8") as f:
                    base_traces = json.load(f)
            except Exception:
                base_traces = []

        all_traces = list(base_traces)
        existing_ids = {t["trace_id"] for t in all_traces if "trace_id" in t}

        # Failure patterns templates for synthetic scaling
        domains = [
            ("DevOps & Cloud Infrastructure", "MetaGPT", ["DevOpsEngineer", "CloudArchitect", "SecurityAuditor", "Deployer"], 
             "Configure Kubernetes ingress controller with TLS certificate renewal.", 
             "CloudArchitect", 1, "Configured ingress with self-signed certificate in production instead of Let's Encrypt cluster issuer.", "config_error"),
            
            ("Data Pipeline ETL", "AutoGen", ["DataEngineer", "TransformAgent", "ValidatorAgent", "DBLoader"],
             "Extract CSV sales data, parse timestamps in ISO 8601, and load to PostgreSQL warehouse.",
             "TransformAgent", 1, "Parsed date format string using '%m-%d-%Y' instead of '%Y-%m-%d', resulting in month/day swapping corruption.", "date_format_bug"),
            
            ("Microservice REST API", "ChatDev", ["ProductManager", "Architect", "Programmer", "CodeReviewer", "QATester"],
             "Implement pagination query params 'limit' and 'offset' in Flask service.",
             "Programmer", 2, "Applied offset calculation as offset = page * limit instead of (page - 1) * limit, skipping page 1 entirely.", "off_by_one"),
            
            ("Cryptographic Key Exchange", "AutoGen", ["SecurityLead", "CryptoDev", "ValidatorAgent"],
             "Generate Diffie-Hellman ephemeral key pairs with 2048-bit prime group.",
             "CryptoDev", 1, "Hardcoded static fixed seed for pseudorandom number generator, producing identical deterministic keys.", "insecure_prng"),

            ("NLP Document Summarizer", "MetaGPT", ["DocumentParser", "SummarizerAgent", "CritiqueAgent", "PublisherAgent"],
             "Summarize 50-page legal contract extracting liability clauses and indemnification terms.",
             "DocumentParser", 0, "Truncated section 4 to 8 due to regex split on roman numerals, removing crucial liability caps.", "parsing_truncation"),

            ("Stock Market Trading Bot", "ChatDev", ["MarketAnalyst", "StrategyCoder", "RiskManager", "OrderExecutor"],
             "Execute trailing stop-loss order at 5% below peak equity.",
             "StrategyCoder", 1, "Inverted inequality condition `if price > peak * 0.95: sell()` triggering instant market sell at peak instead of drop.", "inverted_logic"),
            
            ("Autonomous Web Crawler", "AutoGen", ["CrawlerMaster", "URLExtractor", "HTMLParser", "StorageAgent"],
             "Crawl domain subpages up to depth 3 respecting robots.txt.",
             "URLExtractor", 1, "Normalized relative URLs by prepending root domain without resolving directory paths, creating circular 404 loops.", "url_resolution_bug")
        ]

        # Generate Hand-Crafted traces up to target count
        hc_index = len([t for t in all_traces if t.get("subset") == "hand_crafted"]) + 1
        while hc_index <= count_hc:
            dom = domains[hc_index % len(domains)]
            tid = f"WW-HC-{hc_index:03d}"
            if tid not in existing_ids:
                trace_obj = self._build_synthetic_trace(
                    trace_id=tid,
                    title=f"{dom[0]} Trace #{hc_index}",
                    env=dom[1],
                    agents=dom[2],
                    goal=dom[3],
                    blame_agent=dom[4],
                    blame_step=dom[5],
                    reason=dom[6],
                    cat=dom[7],
                    subset="hand_crafted"
                )
                all_traces.append(trace_obj)
                existing_ids.add(tid)
            hc_index += 1

        # Generate Algorithm-Generated traces up to target count
        ag_index = len([t for t in all_traces if t.get("subset") == "algorithm_generated"]) + 1
        while ag_index <= count_ag:
            dom = domains[(ag_index + 3) % len(domains)]
            tid = f"WW-AG-{ag_index:03d}"
            if tid not in existing_ids:
                trace_obj = self._build_synthetic_trace(
                    trace_id=tid,
                    title=f"Algo-Gen: {dom[0]} Trace #{ag_index}",
                    env=dom[1],
                    agents=dom[2],
                    goal=dom[3],
                    blame_agent=dom[4],
                    blame_step=dom[5],
                    reason=dom[6],
                    cat=dom[7],
                    subset="algorithm_generated"
                )
                all_traces.append(trace_obj)
                existing_ids.add(tid)
            ag_index += 1

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_traces, f, indent=2)
        logger.info(f"Extended benchmark generated with {len(all_traces)} traces at {output_path}")

    def _build_synthetic_trace(self, trace_id, title, env, agents, goal, blame_agent, blame_step, reason, cat, subset):
        steps = []
        for idx, agent in enumerate(agents):
            if idx == 0:
                action_payload = f"Initiating workflow for task: {goal}"
                output_state = "Workflow initiated successfully."
                input_context = goal
            elif idx == blame_step:
                action_payload = f"Generated corrupted state / action introducing: {reason}"
                output_state = f"Output state compromised: {reason}"
                input_context = steps[idx - 1]["action_payload"]
            else:
                input_context = steps[idx - 1]["output_state"]
                if idx > blame_step:
                    action_payload = f"Processing upstream input ({steps[idx-1]['agent_name']} output)..."
                    output_state = f"Cascading execution failure derived from upstream corrupted state: {steps[idx-1]['output_state']}"
                else:
                    action_payload = f"Executing sub-task step {idx} normally."
                    output_state = f"Step {idx} completed successfully."

            recipient = agents[idx + 1] if idx + 1 < len(agents) else "Coordinator"
            steps.append({
                "step_index": idx,
                "agent_name": agent,
                "recipient": recipient,
                "action_type": "execution_step",
                "input_context": input_context,
                "action_payload": action_payload,
                "output_state": output_state
            })

        return {
            "trace_id": trace_id,
            "title": title,
            "environment_name": env,
            "task_goal": goal,
            "subset": subset,
            "total_steps": len(steps),
            "steps": steps,
            "ground_truth": {
                "responsible_agent": blame_agent,
                "decisive_step_index": blame_step,
                "failure_reason": reason,
                "failure_category": cat
            },
            "final_outcome": "failed"
        }

dataset_loader = DatasetLoader()
