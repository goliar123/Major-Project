"""
Command-Line Runner for Benchmark Evaluation.
Usage:
    python -m evaluation.benchmark_runner --subset hand_crafted --limit 20
    python -m evaluation.benchmark_runner --compare
"""
import argparse
import sys
import os
from pathlib import Path

# Add project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rich.console import Console
from rich.table import Table
from evaluation.evaluator import benchmark_evaluator
from dataset.loader import dataset_loader

console = Console()

def run_cli():
    parser = argparse.ArgumentParser(description="Multi-Agent Failure Attribution Benchmark Runner")
    parser.add_argument("--method", type=str, default="proposed", choices=["proposed", "all_at_once", "step_by_step", "binary_search", "compare"], help="Method to evaluate")
    parser.add_argument("--compare", action="store_true", help="Run comparative benchmark across all methods")
    parser.add_argument("--subset", type=str, default=None, choices=["hand_crafted", "algorithm_generated", None], help="Subset of benchmark")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of traces to evaluate")
    args = parser.parse_args()

    if args.compare:
        args.method = "compare"

    traces = dataset_loader.load_traces(subset=args.subset)
    if args.limit:
        traces = traces[:args.limit]

    console.print(f"\n[bold cyan]=== Who&When Multi-Agent Failure Attribution Benchmark ===[/bold cyan]")
    console.print(f"Total Traces to evaluate: [bold green]{len(traces)}[/bold green] (Subset: {args.subset or 'All'})\n")

    if args.method == "compare":
        results = benchmark_evaluator.run_comparative_benchmark(traces=traces, subset=args.subset)
        
        table = Table(title="Comparative Method Analysis on Who&When Benchmark")
        table.add_column("Method", style="cyan", no_wrap=True)
        table.add_column("Agent-Level Acc (%)", style="magenta")
        table.add_column("Step-Level Acc (%)", style="yellow")
        table.add_column("Strict Joint Acc (%)", style="green")
        table.add_column("Avg Latency (s)", style="white")
        table.add_column("Cache Hit Rate (%)", style="blue")

        for method_key, res in results.items():
            name_map = {
                "all_at_once": "All-at-Once (Naive Baseline)",
                "step_by_step": "Step-by-Step (Isolated)",
                "binary_search": "Binary Search (Bisection)",
                "proposed": "Proposed (Dependency-Aware DAG)"
            }
            table.add_row(
                name_map.get(method_key, method_key),
                f"{res.agent_level_accuracy}%",
                f"{res.step_level_accuracy}%",
                f"{res.strict_joint_accuracy}%",
                f"{res.avg_execution_time_per_trace}s",
                f"{res.cache_hit_rate}%"
            )
        console.print(table)

    else:
        result = benchmark_evaluator.evaluate_method(method_name=args.method, traces=traces, subset=args.subset)
        
        table = Table(title=f"Evaluation Results: {result.benchmark_name}")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="bold green")

        table.add_row("Total Traces Evaluated", str(result.evaluated_traces))
        table.add_row("Agent-Level Accuracy", f"{result.agent_level_accuracy}%")
        table.add_row("Step-Level Accuracy", f"{result.step_level_accuracy}%")
        table.add_row("Strict Joint Accuracy", f"{result.strict_joint_accuracy}%")
        table.add_row("Average Execution Time", f"{result.avg_execution_time_per_trace} s")
        table.add_row("Prompt Cache Hit Rate", f"{result.cache_hit_rate}%")
        table.add_row("Total Tokens Consumed", str(result.total_token_count))

        console.print(table)

if __name__ == "__main__":
    run_cli()
