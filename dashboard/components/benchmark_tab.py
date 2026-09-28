import sys
import os
from pathlib import Path

# Add project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from typing import Dict, Any, List
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from evaluation.evaluator import benchmark_evaluator
from dataset.loader import dataset_loader

class BenchmarkTab:
    @staticmethod
    def render():
        st.header("📊 Benchmark Evaluation & Comparative Analysis")
        st.markdown(
            """
            Evaluate failure attribution algorithms against the **Who&When Benchmark (ICML 2025)**.
            Compare the **Proposed Dependency-Aware Engine** against published baselines:
            - **All-at-Once**: Monolithic whole-trace LLM judge
            - **Step-by-Step**: Isolated step-wise evaluator (suffers from symptom misattribution)
            - **Binary Search**: Hierarchical bisection
            """
        )

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            subset_choice = st.selectbox(
                "Select Benchmark Subset:",
                ["All (184 Traces)", "Hand-Crafted (58 Traces)", "Algorithm-Generated (126 Traces)"],
                index=0
            )
            subset_val = None
            if "Hand-Crafted" in subset_choice:
                subset_val = "hand_crafted"
            elif "Algorithm-Generated" in subset_choice:
                subset_val = "algorithm_generated"

        with col2:
            method_mode = st.selectbox(
                "Select Evaluation Mode:",
                ["Comparative Benchmark (All Methods)", "Proposed Engine (DAG Traversal)", "All-at-Once (Monolithic)", "Step-by-Step (Isolated)", "Binary Search"],
                index=0
            )

        with col3:
            limit_traces = st.number_input("Max traces to evaluate (0 = Full Dataset):", min_value=0, max_value=200, value=20, step=5)
            limit_val = limit_traces if limit_traces > 0 else None

        if st.button("🚀 Run Benchmark Evaluation", type="primary", use_container_width=True):
            with st.spinner("Executing benchmark evaluation suite across selected traces..."):
                if "Comparative" in method_mode:
                    comp_results = benchmark_evaluator.run_comparative_benchmark(
                        subset=subset_val,
                        max_traces=limit_val
                    )
                    BenchmarkTab._display_comparative_results(comp_results)
                else:
                    method_key_map = {
                        "Proposed Engine (DAG Traversal)": "proposed",
                        "All-at-Once (Monolithic)": "all_at_once",
                        "Step-by-Step (Isolated)": "step_by_step",
                        "Binary Search": "binary_search"
                    }
                    m_key = method_key_map.get(method_mode, "proposed")
                    single_res = benchmark_evaluator.evaluate_method(
                        method_name=m_key,
                        subset=subset_val,
                        max_traces=limit_val
                    )
                    BenchmarkTab._display_single_result(single_res)

    @staticmethod
    def _display_comparative_results(comp_results: Dict[str, Any]):
        st.success("✅ Comparative Benchmark Run Completed!")

        # Build comparison DataFrame
        data = []
        name_map = {
            "all_at_once": "All-at-Once (Monolithic)",
            "step_by_step": "Step-by-Step (Isolated)",
            "binary_search": "Binary Search",
            "proposed": "Proposed (Dependency DAG)"
        }
        for k, res in comp_results.items():
            data.append({
                "Method": name_map.get(k, k),
                "Agent-Level Acc (%)": res.agent_level_accuracy,
                "Step-Level Acc (%)": res.step_level_accuracy,
                "Strict Joint Acc (%)": res.strict_joint_accuracy,
                "Avg Latency (s)": res.avg_execution_time_per_trace,
                "Cache Hit Rate (%)": res.cache_hit_rate,
                "Total Tokens": res.total_token_count
            })

        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

        # Plot Comparative Bar Chart
        st.subheader("📈 Accuracy Comparison Chart")
        fig, ax = plt.subplots(figsize=(10, 4.5))
        methods = df["Method"].tolist()
        x = range(len(methods))
        width = 0.25

        ax.bar([i - width for i in x], df["Agent-Level Acc (%)"], width=width, label="Agent-Level Acc (%)", color="#89b4fa")
        ax.bar(x, df["Step-Level Acc (%)"], width=width, label="Step-Level Acc (%)", color="#f9e2af")
        ax.bar([i + width for i in x], df["Strict Joint Acc (%)"], width=width, label="Strict Joint Acc (%)", color="#a6e3a1")

        ax.set_ylabel("Accuracy (%)")
        ax.set_title("Who&When Benchmark: Failure Attribution Accuracy Comparison")
        ax.set_xticks(list(x))
        ax.set_xticklabels(methods, rotation=10, ha="right")
        ax.legend()
        ax.grid(axis="y", linestyle="--", alpha=0.6)
        st.pyplot(fig)

    @staticmethod
    def _display_single_result(res: Any):
        st.success(f"✅ Evaluation Complete for: **{res.benchmark_name}**")
        
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Agent-Level Accuracy", f"{res.agent_level_accuracy}%")
        m2.metric("Step-Level Accuracy", f"{res.step_level_accuracy}%")
        m3.metric("Strict Joint Accuracy", f"{res.strict_joint_accuracy}%")
        m4.metric("Avg Latency", f"{res.avg_execution_time_per_trace}s")
        m5.metric("Cache Hit Rate", f"{res.cache_hit_rate}%")

        # Table of individual verdicts
        rows = []
        for v in res.individual_verdicts:
            rows.append({
                "Trace ID": v.trace_id,
                "Responsible Agent": v.responsible_agent,
                "Decisive Step": v.decisive_step_index,
                "Agent Match": "✅" if v.is_correct_agent else "❌",
                "Step Match": "✅" if v.is_correct_step else "❌",
                "Strict Match": "✅" if v.is_strictly_correct else "❌",
                "Latency (s)": v.execution_time_seconds,
                "Explanation": v.explanation[:120] + "..."
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

benchmark_tab = BenchmarkTab()
