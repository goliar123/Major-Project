# 🌐 05 - API, Async Queue & Dashboard

## 🚀 1. Developer Tooling Architecture

Our system provides two complementary interfaces:
1. **FastAPI REST API & Celery Task Queue**: For programmatic integration into CI/CD pipelines, agent runtimes, and automated test runners.
2. **Streamlit Interactive Developer Dashboard**: For human developers to inspect failed traces, explore information DAGs, and analyze benchmark metrics.

---

## ⚡ 2. FastAPI REST Backend (`api/main.py`, `api/routes.py`)

Run the server:
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive Swagger UI: `http://localhost:8000/docs`

### API Endpoints:

| Method | Endpoint | Description | Request / Response |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Service health status check | `{"status": "healthy"}` |
| `POST` | `/api/v1/attribute` | Submits a multi-agent trace for failure diagnosis | **Body**: `MultiAgentTrace`<br>**Returns**: `AttributionVerdict` (Responsible Agent, Decisive Step, Justification, DAG Nodes/Edges) |
| `GET` | `/api/v1/traces` | Lists Who&When benchmark traces | **Query**: `subset=hand_crafted`, `limit=10`<br>**Returns**: `List[MultiAgentTrace]` |
| `GET` | `/api/v1/traces/{trace_id}` | Retrieves specific trace by ID | **Returns**: `MultiAgentTrace` |
| `POST` | `/api/v1/benchmark/run` | Triggers benchmark evaluation suite | **Query**: `method=proposed`, `subset=all`<br>**Returns**: `BenchmarkResult` (Accuracies, Latencies, Verdicts) |
| `GET` | `/api/v1/cache/stats` | Returns prompt cache statistics | `{"hits": 240, "misses": 15, "hit_rate_pct": 94.12}` |
| `POST` | `/api/v1/cache/clear` | Clears evaluation prompt cache | `{"message": "Cache successfully cleared."}` |

---

## 📬 3. Asynchronous Worker Queue (`api/celery_tasks.py`)

For high-throughput multi-agent test environments:
- **Broker**: Redis (`redis://localhost:6379/0`)
- **Backend**: Redis (`redis://localhost:6379/1`)
- **Task**: `tasks.attribute_trace_async(trace_dict)`
- **Graceful Fallback**: If Celery/Redis is not running in local development, FastAPI executes synchronous attribution seamlessly.

---

## 🖥️ 4. Interactive Developer Dashboard (`dashboard/app.py`)

Run the dashboard:
```bash
streamlit run dashboard/app.py
```
Access at: `http://localhost:8501`

### Dashboard Feature Tabs:

### Tab 1: 🔍 Trace Debugger & DAG Visualizer
- **Trace Selector**: Choose any trace from the 184 Who&When benchmark corpus or custom uploads.
- **Root-Cause Verdict Banner**: Instantly displays the responsible agent, decisive step index, diagnosis latency, and cache hits.
- **Interactive Pyvis DAG**:
  - 🔴 **Red Node (Crimson)**: Originating Root Cause error step.
  - 🟠 **Orange Node (Amber)**: Downstream Propagated Symptom steps (inherited errors).
  - 🟢 **Green Node (Emerald)**: Normal execution steps.
  - Interactive zoom, drag, and tooltips displaying step health scores and rationales.
- **Step-by-Step Inspector**: Expandable cards displaying Agent, Recipient, Action Payload (auto-highlighted Python/SQL), and judge justification.

### Tab 2: 📊 Who&When Benchmark Evaluation
- Select subset (Hand-Crafted 58, Algorithm-Generated 126, or All 184).
- Select evaluation mode: Comparative Benchmark (All Methods) or individual methods.
- Displays live accuracy cards and Matplotlib bar chart comparisons.

### Tab 3: 📤 Custom Log & JSON Ingestion
- Upload JSON trace files or paste raw console dialogue logs from AutoGen, ChatDev, MetaGPT, or LangGraph.
- Automatically segments logs and executes instant causal diagnosis.

### Tab 4: ⚡ Cache & Resource Telemetry
- Real-time cache hit/miss monitor and cache database reset controls.

---

## 🔗 Related Notes
- [[02 - System Architecture & Design]]
- [[03 - Core Engine Implementation]]
- [[04 - Benchmark & Evaluation Results]]
