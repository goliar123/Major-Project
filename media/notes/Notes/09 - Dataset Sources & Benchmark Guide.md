# 📦 09 - Dataset Sources & Benchmark Guide

This guide details all available data sources, public research benchmark repositories, and methods to capture real traces from modern multi-agent frameworks (AutoGen, CrewAI, LangGraph, MetaGPT).

---

## 🗃️ 1. Built-In Dataset (Ready to Test Right Now)

Your local project already contains the complete **184 Who&When benchmark traces**:
- **Location:** [`dataset/data/who_and_when_traces.json`](file:///d:/Projects/LLM/dataset/data/who_and_when_traces.json)
- **Composition:**
  - **58 Hand-Crafted Traces:** Complex multi-agent reasoning, deep cascading bugs, and multi-turn collaboration across AutoGen, ChatDev, and MetaGPT.
  - **126 Algorithm-Generated Traces:** Programmatically injected faults, schema mismatches, and parameter corruptions.
- **How to access:**
  - **In Streamlit UI:** Select any trace from the dropdown under the **Trace Debugger** tab.
  - **In CLI:** Run `python -m evaluation.benchmark_runner --compare`.

---

## 🌐 2. Public Research Benchmarks & Datasets

| Benchmark / Dataset | Reference Paper | Traces | Description & Links |
| :--- | :--- | :---: | :--- |
| **Who&When Benchmark** | *Which Agent Causes Task Failures and When?* (ICML 2025 Spotlight) | 184 traces | Built on **GAIA** and **AssistantBench** queries across AutoGen and ChatDev. Ground-truth labeled with responsible agent, decisive step, and failure reason. [arXiv:2505.00212](https://arxiv.org/abs/2505.00212) |
| **MAST-Data** | *Why Do Multi-Agent LLM Systems Fail?* (NeurIPS 2025) | 1,600+ traces | Failure taxonomy dataset spanning 7 MAS frameworks with inter-annotator agreement $\kappa = 0.88$. [arXiv:2503.13657](https://arxiv.org/abs/2503.13657) |
| **TracerTraj** | *AgenTracer: Who Is Inducing Failure in Agentic Systems?* (2025) | 2,500 trajectories | Programmatic fault-injected multi-agent execution traces. [arXiv:2509.03312](https://arxiv.org/abs/2509.03312) |
| **AgentErrorBench** | *AgentDebug: Where LLM Agents Fail* (2025) | 800+ trajectories | Single & multi-agent traces collected across ALFWorld, GAIA, and WebShop. [arXiv:2509.25370](https://arxiv.org/abs/2509.25370) |

---

## 🛠️ 3. How to Capture Traces from Real Multi-Agent Frameworks

### A. AutoGen (Microsoft)
Capture the chat history at the end of a group chat:
```python
import json

# Run AutoGen GroupChat
chat_result = user_proxy.initiate_chat(manager, message="Build a portfolio analyzer")

# Export to trace JSON format
trace_payload = {
    "workflow_name": "autogen_portfolio_run",
    "orchestrator": "AutoGen",
    "task_goal": "Build a portfolio analyzer",
    "steps": [
        {
            "step_index": idx,
            "agent_name": msg.get("name", "Agent"),
            "recipient": "GroupChat",
            "action_type": "message",
            "action_payload": msg.get("content", ""),
            "output_state": "Delivered"
        }
        for idx, msg in enumerate(chat_result.chat_history)
    ]
}

with open("my_autogen_trace.json", "w") as f:
    json.dump(trace_payload, f, indent=2)
```

### B. CrewAI
Capture step outputs using CrewAI callbacks:
```python
from crewai import Crew, Agent, Task

# Capture outputs from crew.kickoff()
result = my_crew.kickoff()

# Save execution logs or task outputs
trace_payload = {
    "workflow_name": "crewai_market_research",
    "orchestrator": "CrewAI",
    "steps": [
        {
            "step_index": idx,
            "agent_name": task.agent.role,
            "action_type": "task_execution",
            "action_payload": str(task.output),
            "output_state": task.output.raw if hasattr(task.output, 'raw') else "Finished"
        }
        for idx, task in enumerate(my_crew.tasks)
    ]
}
```

### C. LangGraph
Export state execution history:
```python
# Stream LangGraph state events
trace_events = []
for event in graph.stream({"messages": [("user", "Fetch Q2 financial data")]}):
    for node_name, state in event.items():
        trace_events.append({
            "agent": node_name,
            "action": "state_update",
            "summary": str(state)
        })

trace_payload = {
    "workflow_name": "langgraph_pipeline",
    "orchestrator": "LangGraph",
    "execution_trace": trace_events
}
```

---

## 🔄 4. How to Feed Any Trace into Our Tool

1. **Dashboard UI:** Open `http://localhost:8501`, go to **📤 Custom Log / JSON Ingestion**, and paste your JSON or raw console log.
2. **API:** Send a `POST` request to `http://localhost:8000/api/v1/attribute`.
3. **Python:** Call `attribution_engine.attribute_trace(trace)`.

---

## 🔗 Related Notes
- [[00 - Project Overview & Index]]
- [[01 - Problem Statement & Literature Survey]]
- [[04 - Benchmark & Evaluation Results]]
