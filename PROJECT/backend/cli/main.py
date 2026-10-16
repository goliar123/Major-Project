"""
Dedicated Command-Line Interface (`agent-trace` / `cli.main`)
Automated Failure Attribution for LLM-Based Multi-Agent Systems.

Commands:
  diagnose    Diagnose a multi-agent trace file (JSON, LangGraph, Who&When)
  watch       Live real-time streaming watcher with shadow monitoring
  benchmark   Run evaluation across the Who&When benchmark suite
  cache       Inspect or clear the SHA256 evaluation cache
  test-llm    Test connectivity with local Ollama (llama3.2) or active LLM
  serve       Launch the Streamlit dashboard or FastAPI REST server
"""
import sys
import os
import time
import argparse
import subprocess
from pathlib import Path
from typing import Optional, List

# Reconfigure stdout/stderr to UTF-8 on Windows to prevent cp1252 emoji crash
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.text import Text
from rich import box

from config.settings import settings
from dataset.loader import dataset_loader
from core.segmentation import trace_segmenter
from core.engine import attribution_engine
from core.cache import cache_manager
from core.step_judge import step_judge
from core.live_monitor import live_trace_monitor
from cli.log_watcher import log_watcher
from dataset.schema import ExecutionStep, MultiAgentTrace

console = Console(force_terminal=True, legacy_windows=False)

BANNER = r"""[bold cyan]
   ___                    __     ______                     
  / _ | ___ _ ___  ___   / /_   /_  __/____ ___ _ ____ ___  
 / __ |/ _ `// -_)/ _ \ / __/    / /  / __// _ `// __// -_) 
/_/ |_|\_, / \__//_//_/ \__/    /_/  /_/   \_,_/ \__/ \__/  
      /___/                                                 [/bold cyan]
[bold white] Automated Failure Attribution for LLM Multi-Agent Systems [/bold white]
[dim] Neuro-Symbolic Causal Graph Engine | v1.2.0 [/dim]
"""

# ==============================================================================
# 1. DIAGNOSE / INSPECT COMMAND
# ==============================================================================
def cmd_diagnose(file_path: str, method: str = "proposed", export_html: Optional[str] = None):
    p = Path(file_path)
    if not p.exists():
        console.print(f"[bold red]Error:[/bold red] File not found: `{file_path}`")
        return

    console.print(BANNER)
    console.print(f"[bold]Loading trace from:[/bold] `{p.name}` ...")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        task = progress.add_task("[cyan]Parsing trace and segmenting turns...", total=None)
        
        # Load JSON file into dict
        try:
            import json
            with open(p, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            if isinstance(raw_data, list):
                if raw_data and isinstance(raw_data[0], dict) and ("steps" in raw_data[0] or "execution_trace" in raw_data[0]):
                    raw_data = raw_data[0]
                else:
                    raw_data = {"steps": raw_data}
            trace = trace_segmenter.parse_custom_json(raw_data)
        except Exception:
            trace = dataset_loader.get_trace_by_id(p.stem)
            if not trace:
                console.print(f"[bold red]Error:[/bold red] Could not parse `{file_path}` into a valid trace.")
                return

        progress.update(task, description="[yellow]Executing Causal Attribution Engine (DAG + Traversal)...")
        start_time = time.time()
        if method == "all_at_once":
            from baselines.all_at_once import all_at_once_baseline
            verdict = all_at_once_baseline.attribute(trace)
        elif method == "step_by_step":
            from baselines.step_by_step import step_by_step_baseline
            verdict = step_by_step_baseline.attribute(trace)
        elif method == "binary_search":
            from baselines.binary_search import binary_search_baseline
            verdict = binary_search_baseline.attribute(trace)
        else:
            verdict = attribution_engine.attribute_trace(trace)
        elapsed = time.time() - start_time

    # Trace Overview Panel
    console.print(Panel(
        f"[bold]Trace ID:[/bold] {trace.trace_id} | [bold]Total Turns:[/bold] {len(trace.steps)} | [bold]Environment:[/bold] {trace.environment_name}\n"
        f"[bold]Task Goal:[/bold] {trace.task_goal}\n"
        f"[bold]Evaluation Model:[/bold] {settings.LLM_MODEL} ({settings.LLM_PROVIDER}) | [bold]Diagnostic Latency:[/bold] {elapsed:.3f}s",
        title="[bold green]Trace Metadata[/bold green]",
        border_style="cyan"
    ))

    # Steps Table
    table = Table(title=f"Execution Steps Breakdown ({len(trace.steps)} Steps)", box=box.ROUNDED, expand=True)
    table.add_column("Step", justify="center", style="cyan", width=8)
    table.add_column("Agent", justify="left", style="bold magenta", width=18)
    table.add_column("Action Summary", justify="left", style="white")
    table.add_column("Score", justify="center", width=8)
    table.add_column("Diagnosis", justify="center", width=22)

    root_idx = verdict.decisive_step_index
    causal_set = set(verdict.causal_dependency_chain)

    for s in trace.steps:
        eval_obj = s.evaluation
        score_val = eval_obj.score if eval_obj else 1.0
        score_str = f"{score_val:.2f}"

        if s.step_index == root_idx:
            status_badge = "[bold red]🔴 ROOT CAUSE[/bold red]"
        elif s.step_index in causal_set and s.step_index < root_idx:
            status_badge = "[bold yellow]⚡ TRIGGER[/bold yellow]"
        elif s.step_index in causal_set and s.step_index > root_idx:
            status_badge = "[bold orange3]🟠 SYMPTOM[/bold orange3]"
        elif score_val < 0.7:
            status_badge = "[yellow]⚠️ ANOMALY[/yellow]"
        else:
            status_badge = "[green]🟢 HEALTHY[/green]"

        payload_preview = (s.action_payload[:75] + "...") if len(s.action_payload) > 75 else s.action_payload
        table.add_row(f"#{s.step_index + 1}", s.agent_name, payload_preview, score_str, status_badge)

    console.print(table)

    # Attribution Verdict Panel
    chain_str = " ➔ ".join([f"Step {idx + 1}" for idx in verdict.causal_dependency_chain])
    console.print(Panel(
        f"[bold red]🚨 ROOT CAUSE ATTRIBUTION REPORT[/bold red]\n\n"
        f"📍 [bold]Responsible Agent:[/bold] [bold red]{verdict.responsible_agent}[/bold red]\n"
        f"🔢 [bold]Decisive Step Number:[/bold] [bold yellow]Step {verdict.decisive_step_index + 1}[/bold yellow] (ID: `{verdict.decisive_step_id}`)\n"
        f"🏷️ [bold]Failure Category:[/bold] {verdict.failure_type}\n"
        f"🔗 [bold]Causal Dependency Chain:[/bold] {chain_str}\n\n"
        f"[bold white]Detailed Diagnosis:[/bold white]\n{verdict.explanation}\n\n"
        f"[dim]Cache Hits: {verdict.cache_hits} | Cache Misses: {verdict.cache_misses} | Execution Time: {verdict.execution_time_seconds:.3f}s[/dim]",
        title="[bold red]Verdict Summary[/bold red]",
        border_style="red"
    ))

    # Optional HTML Export
    if export_html:
        try:
            from pyvis.network import Network
            net = Network(height="650px", width="100%", directed=True, bgcolor="#181825", font_color="#ffffff")
            for node in verdict.graph_nodes:
                color = "#f38ba8" if node.status == "root_cause" else ("#fab387" if node.status == "propagated_symptom" else "#a6e3a1")
                net.add_node(node.step_index, label=f"#{node.step_index+1} {node.agent_name}", color=color, title=node.reason)
            for edge in verdict.graph_edges:
                net.add_edge(edge.source_step_index, edge.target_step_index, title=edge.dependency_type)
            net.save_graph(export_html)
            console.print(f"[bold green]✔ Visual Pyvis DAG exported successfully to:[/bold green] `{export_html}`")
        except Exception as e:
            console.print(f"[yellow]Warning: Could not export HTML DAG: {e}[/yellow]")


# ==============================================================================
# 2. LIVE WATCH COMMAND
# ==============================================================================
def cmd_watch(log_file: str, task_goal: str, expected_output: Optional[str] = None, max_steps: int = 200):
    console.print(BANNER)
    trace_id = f"live_{Path(log_file).stem}_{int(time.time())}"
    session = live_trace_monitor.start_session(trace_id, task_goal, expected_output)

    console.print(Panel(
        f"[bold]Target File:[/bold] `{log_file}`\n"
        f"[bold]Task Goal:[/bold] {task_goal}\n"
        f"[bold]Expected Output:[/bold] {expected_output or '[None - Trigger on status failure]'}\n"
        f"[dim]Shadow Monitoring Active: Building DAG incrementally without early interruption...[/dim]",
        title="[bold green]Live Multi-Agent Stream Monitor[/bold green]",
        border_style="green"
    ))

    step_count = 0
    final_output = ""
    terminal_status = "COMPLETED"

    try:
        for raw_line in log_watcher.tail_file(log_file):
            if not raw_line.strip():
                continue

            if any(k in raw_line for k in ["TERMINATED", "FORCE_TERMINATED", "UnrecoverableSchemaError", "FAILED"]):
                terminal_status = "FAILED"
            if "SUCCESSFULLY COMPLETED" in raw_line or "TASK_DONE" in raw_line:
                terminal_status = "COMPLETED"

            final_output += "\n" + raw_line
            step = log_watcher.parse_event_line(raw_line, step_index=step_count)
            if not step:
                continue

            eval_res, edges = session.ingest_step(step)
            step_count += 1

            badge = "[yellow]⚠️ Flagged[/yellow]" if (eval_res.anomaly_detected or eval_res.score < 0.7) else "[green]🟢 Healthy[/green]"
            preview = (step.action_payload[:80] + "...") if len(step.action_payload) > 80 else step.action_payload
            console.print(f"[dim]Turn #{step_count}[/dim] [bold]{step.agent_name}[/bold]: {preview} ({badge})")

            if step_count >= max_steps:
                break
            time.sleep(0.01)

    except KeyboardInterrupt:
        console.print("\n[yellow]Monitoring halted by user (Ctrl+C). Concluding session...[/yellow]")

    console.print("\n[bold cyan]Evaluating Terminal State & Conflict Resolution...[/bold cyan]")
    verdict = session.finish_session(final_output, status=terminal_status)

    if verdict is None:
        console.print(Panel(
            f"[bold green]✅ Workflow Completed Successfully![/bold green]\n"
            f"All {step_count} steps executed without terminal failure or goal conflicts.\n"
            f"[dim]All intermediate warnings resolved cleanly.[/dim]",
            title="Execution Verdict: PASS",
            border_style="green"
        ))
    else:
        console.print(Panel(
            f"[bold red]🚨 FAILURE ATTRIBUTION VERDICT: ROOT CAUSE LOCATED[/bold red]\n\n"
            f"📍 [bold]Responsible Agent:[/bold] [bold red]{verdict.responsible_agent}[/bold red]\n"
            f"🔢 [bold]Decisive Root Step:[/bold] [bold yellow]Step {verdict.decisive_step_index + 1}[/bold yellow]\n"
            f"🏷️ [bold]Failure Category:[/bold] {verdict.failure_type}\n\n"
            f"[bold white]Detailed Diagnosis:[/bold white]\n{verdict.explanation}",
            title="[bold red]Automated Failure Attribution Report[/bold red]",
            border_style="red"
        ))


# ==============================================================================
# 3. BENCHMARK EVALUATION COMMAND
# ==============================================================================
def cmd_benchmark(method: str = "proposed", subset: Optional[str] = None, limit: Optional[int] = 10):
    from evaluation.evaluator import benchmark_evaluator
    console.print(BANNER)
    console.print(f"[bold cyan]Running Who&When Benchmark Evaluation Suite[/bold cyan] (Method: [bold]{method}[/bold], Subset: {subset or 'All'}, Limit: {limit})...\n")

    with Progress(
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        task = progress.add_task("[cyan]Evaluating benchmark traces...", total=limit or 50)
        res = benchmark_evaluator.evaluate_method(method_name=method, subset=subset, max_traces=limit)
        progress.update(task, completed=limit or 50)

    # Print Results Table
    table = Table(title="Benchmark Evaluation Results", box=box.ROUNDED, expand=True)
    table.add_column("Metric", justify="left", style="bold white")
    table.add_column("Score / Value", justify="center", style="bold cyan")

    table.add_row("Total Traces Evaluated", str(res.evaluated_traces))
    table.add_row("Agent-Level Accuracy", f"{res.agent_level_accuracy:.1f}%")
    table.add_row("Step-Level Accuracy", f"{res.step_level_accuracy:.1f}%")
    table.add_row("Strict Joint Accuracy", f"[bold green]{res.strict_joint_accuracy:.1f}%[/bold green]")
    table.add_row("Avg Execution Time / Trace", f"{res.avg_execution_time_per_trace:.3f}s")
    table.add_row("Cache Hit Rate", f"{res.cache_hit_rate:.1f}%")
    console.print(table)


# ==============================================================================
# 4. CACHE COMMAND
# ==============================================================================
def cmd_cache(action: str):
    if action == "stats":
        stats = cache_manager.get_stats()
        table = Table(title="Evaluation Prompt Cache Statistics", box=box.ROUNDED)
        table.add_column("Field", style="bold magenta")
        table.add_column("Value", style="cyan")
        for k, v in stats.items():
            table.add_row(str(k), str(v))
        console.print(table)
    elif action == "clear":
        cache_manager.clear()
        console.print("[bold green]✔ SQLite evaluation cache successfully cleared.[/bold green]")


# ==============================================================================
# 5. TEST LLM COMMAND
# ==============================================================================
def cmd_test_llm():
    from scripts.test_ollama_connection import test_connection
    test_connection()


# ==============================================================================
# 6. SERVE COMMAND
# ==============================================================================
def cmd_serve(target: str, port: int):
    console.print(BANNER)
    if target == "dashboard":
        console.print(f"[bold green]Starting Streamlit Dashboard on port {port}...[/bold green]")
        subprocess.run(["streamlit", "run", "dashboard/app.py", "--server.port", str(port)])
    elif target == "api":
        console.print(f"[bold green]Starting FastAPI Uvicorn Server on port {port}...[/bold green]")
        import uvicorn
        uvicorn.run("api.main:app", host="0.0.0.0", port=port, reload=True)


# ==============================================================================
# MAIN ENTRYPOINT
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(description="Automated Multi-Agent Failure Attribution CLI (`agent-trace`)")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # 1. Diagnose
    diag_p = subparsers.add_parser("diagnose", help="Diagnose a multi-agent trace file")
    diag_p.add_argument("file", help="Path to trace file (JSON, LangGraph log, Who&When)")
    diag_p.add_argument("--method", default="proposed", choices=["proposed", "all_at_once", "step_by_step", "binary_search"])
    diag_p.add_argument("--export-html", help="Path to export interactive Pyvis HTML DAG (e.g. dag.html)")

    # 2. Watch
    watch_p = subparsers.add_parser("watch", help="Watch a streaming log file in real-time")
    watch_p.add_argument("--log-file", required=True, help="Path to log file to tail")
    watch_p.add_argument("--goal", required=True, help="Overarching task goal")
    watch_p.add_argument("--expect", help="Expected substring/regex in final output")
    watch_p.add_argument("--max-steps", type=int, default=200)

    # 3. Benchmark
    bm_p = subparsers.add_parser("benchmark", help="Run Who&When benchmark evaluation")
    bm_p.add_argument("--subset", choices=["hand_crafted", "algorithm_generated"])
    bm_p.add_argument("--limit", type=int, default=10)
    bm_p.add_argument("--method", default="proposed")

    # 4. Cache
    cache_p = subparsers.add_parser("cache", help="Manage SHA256 prompt cache")
    cache_p.add_argument("action", choices=["stats", "clear"])

    # 5. Test LLM
    subparsers.add_parser("test-llm", help="Test connection to Ollama/active LLM")

    # 6. Serve
    serve_p = subparsers.add_parser("serve", help="Launch UI Dashboard or REST API")
    serve_p.add_argument("target", choices=["dashboard", "api"])
    serve_p.add_argument("--port", type=int, default=8501)

    args = parser.parse_args()

    if args.command == "diagnose":
        cmd_diagnose(args.file, args.method, args.export_html)
    elif args.command == "watch":
        cmd_watch(args.log_file, args.goal, args.expect, args.max_steps)
    elif args.command == "benchmark":
        cmd_benchmark(args.method, args.subset, args.limit)
    elif args.command == "cache":
        cmd_cache(args.action)
    elif args.command == "test-llm":
        cmd_test_llm()
    elif args.command == "serve":
        cmd_serve(args.target, args.port)
    else:
        console.print(BANNER)
        parser.print_help()

if __name__ == "__main__":
    main()
