import sys
import os
from pathlib import Path

# Add project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import json
from dataset.loader import dataset_loader
from dataset.schema import MultiAgentTrace, ExecutionStep, AttributionVerdict
from core.engine import attribution_engine
from core.cache import cache_manager
from core.segmentation import trace_segmenter
from dashboard.components.dag_viewer import dag_viewer
from dashboard.components.trace_inspector import trace_inspector
from dashboard.components.benchmark_tab import benchmark_tab

st.set_page_config(
    page_title="Automated Failure Attribution for LLM Multi-Agent Systems",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .verdict-card {
        background-color: #f8fafc;
        border-left: 5px solid #ef4444;
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🕵️ MAS Failure Debugger")
st.sidebar.markdown("**Project D2 (GRIET CSE)**")
st.sidebar.markdown("Automated Root-Cause Attribution for LLM Multi-Agent Systems")
st.sidebar.divider()

nav_option = st.sidebar.radio(
    "Navigation:",
    [
        "🔍 Trace Debugger & DAG Visualizer",
        "📊 Benchmark Evaluation (Who&When)",
        "📤 Custom Log / JSON Ingestion",
        "⚡ Cache & Resource Telemetry"
    ]
)

# Tab 1: Trace Debugger & DAG Visualizer
if nav_option == "🔍 Trace Debugger & DAG Visualizer":
    st.markdown('<div class="main-title">Multi-Agent Execution Trace Debugger</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Isolate the responsible agent, pinpoint the decisive error step, and visualize information-dependency flow.</div>', unsafe_allow_html=True)

    # Load available traces
    all_traces = dataset_loader.load_traces()
    trace_map = {f"[{t.trace_id}] {t.title or t.task_goal[:50]} ({t.environment_name})": t for t in all_traces}
    
    selected_label = st.selectbox("Select a Failed Multi-Agent Trace to Diagnose:", list(trace_map.keys()))
    selected_trace = trace_map[selected_label]

    # Trace Overview Banner
    with st.container():
        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
        c1.markdown(f"**Task Goal:** {selected_trace.task_goal}")
        c2.markdown(f"**Environment:** `{selected_trace.environment_name}`")
        c3.markdown(f"**Total Steps:** `{len(selected_trace.steps)} turns`")
        if selected_trace.ground_truth:
            c4.markdown(f"**GT Blame:** `{selected_trace.ground_truth.responsible_agent}` (Step {selected_trace.ground_truth.decisive_step_index})")

    st.divider()

    # Attribution Action
    col_btn, col_algo = st.columns([1, 2])
    with col_btn:
        run_btn = st.button("🚀 Run Root-Cause Diagnosis", type="primary", use_container_width=True)

    if run_btn or f"verdict_{selected_trace.trace_id}" in st.session_state:
        with st.spinner("Analyzing trace dependencies and traversing causal DAG..."):
            if run_btn or f"verdict_{selected_trace.trace_id}" not in st.session_state:
                verdict = attribution_engine.attribute_trace(selected_trace)
                st.session_state[f"verdict_{selected_trace.trace_id}"] = verdict
            else:
                verdict = st.session_state[f"verdict_{selected_trace.trace_id}"]

        # Diagnosis Verdict Banner
        st.subheader("🎯 Root-Cause Attribution Verdict")
        vcol1, vcol2, vcol3, vcol4 = st.columns(4)
        vcol1.metric("🚨 Responsible Agent", verdict.responsible_agent)
        vcol2.metric("📍 Decisive Root Step", f"Step {verdict.decisive_step_index}")
        vcol3.metric("⏱️ Diagnosis Latency", f"{verdict.execution_time_seconds:.3f} s")
        vcol4.metric("⚡ Cache Hits", f"{verdict.cache_hits} queries")

        st.info(f"**Justification:** {verdict.explanation}")

        # DAG Visualizer
        st.subheader("🌐 Causal Information Dependency Graph (DAG)")
        st.caption("🔴 Red = Root-Cause Error Source | 🟠 Orange = Propagated Symptom (Inherited Error) | 🟢 Green = Normal Execution")
        dag_viewer.render_dag(verdict)

        # Step-by-Step Inspector
        trace_inspector.render_inspector(selected_trace, verdict)

# Tab 2: Benchmark Evaluation
elif nav_option == "📊 Benchmark Evaluation (Who&When)":
    benchmark_tab.render()

# Tab 3: Custom Log / JSON Ingestion
elif nav_option == "📤 Custom Log / JSON Ingestion":
    st.header("📤 Custom Multi-Agent Trace Ingestion")
    st.markdown("Paste an unstructured execution log or upload a structured JSON trace file from AutoGen, ChatDev, MetaGPT, or LangGraph.")

    input_mode = st.radio("Input Format:", ["Structured JSON Trace", "Raw Multi-Agent Console Text Log"])
    
    if input_mode == "Structured JSON Trace":
        uploaded_file = st.file_uploader("Upload Trace JSON", type=["json"])
        json_text = st.text_area("Or paste JSON payload directly:", height=200)

        if st.button("Analyze Custom JSON Trace", type="primary"):
            try:
                if uploaded_file:
                    raw_dict = json.load(uploaded_file)
                elif json_text.strip():
                    raw_dict = json.loads(json_text)
                else:
                    st.error("Please upload a file or paste JSON.")
                    st.stop()

                custom_trace = trace_segmenter.parse_custom_json(raw_dict)
                verdict = attribution_engine.attribute_trace(custom_trace)
                st.success(f"Attribution Complete! Responsible Agent: **{verdict.responsible_agent}** (Step {verdict.decisive_step_index})")
                dag_viewer.render_dag(verdict)
                trace_inspector.render_inspector(custom_trace, verdict)

            except Exception as e:
                st.error(f"Failed to parse trace: {e}")

    else:
        goal_input = st.text_input("Task Goal:", value="Develop a weather reporting API endpoint.")
        raw_log = st.text_area("Paste Raw Multi-Agent Execution Log:", height=250, placeholder="[UserProxy -> Architect]: Please design the API...\n[Architect -> Coder]: Here is the schema...")
        
        if st.button("Parse & Attribute Log", type="primary"):
            if not raw_log.strip():
                st.warning("Please provide log text.")
            else:
                parsed_trace = trace_segmenter.parse_raw_log_text(raw_log, task_goal=goal_input)
                st.success(f"Successfully segmented log into {len(parsed_trace.steps)} steps.")
                verdict = attribution_engine.attribute_trace(parsed_trace)
                st.success(f"Attribution Complete! Responsible Agent: **{verdict.responsible_agent}** (Step {verdict.decisive_step_index})")
                dag_viewer.render_dag(verdict)
                trace_inspector.render_inspector(parsed_trace, verdict)

# Tab 4: Cache & Resource Telemetry
elif nav_option == "⚡ Cache & Resource Telemetry":
    st.header("⚡ SHA256 Prompt Caching & Telemetry")
    st.markdown("Monitor prompt cache hit ratios, token budget preservation, and hardware utilization.")

    stats = cache_manager.get_stats()
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Storage Backend", stats["backend"].upper())
    c2.metric("Cache Hits", stats["hits"])
    c3.metric("Cache Misses", stats["misses"])
    c4.metric("Cache Hit Rate", f"{stats['hit_rate_pct']}%")

    st.divider()
    if st.button("🗑️ Clear Cache Database", type="secondary"):
        cache_manager.clear()
        st.success("Cache cleared successfully.")
