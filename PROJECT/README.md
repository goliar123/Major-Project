# Automated Failure Attribution for LLM-Based Multi-Agent Systems
**B.Tech Major Project Phase-1 · Batch B12 · Department of CSE · GRIET**

---

## 👥 Project Team & Mentorship
- **Rachapalli S Prabhaadhithya** (23241A05Q3)
- **Rathod Ajay** (23241A05Q4)
- **Noel Paul** (23241A05Q6)
- **Talagapu Niranjan** (23241A05R1)
- **Internal Guide:** Dr. D. Ushasree, Assistant Professor, Dept of CSE, GRIET

---

## 🏗️ System Architecture & Segregated Layout

```
LLM/
├── media/                                  # All presentation, document, and media assets
│   ├── presentations/                      # PPTX and PDF review decks
│   │   ├── D1_Review_3_PW.pptx
│   │   ├── D1_Review_3_PW.pdf
│   │   ├── Review_3_Automated_Failure_Attribution_B12.pptx
│   │   └── Review_3_Automated_Failure_Attribution_B12.pdf
│   ├── reports/                            # Formal 56-page Phase-1 Report (.docx, .pdf, .md)
│   │   ├── Major_Project_Phase1_Report_B12.docx
│   │   ├── Major_Project_Phase1_Report_B12.pdf
│   │   └── Major_Project_Phase1_Report.md
│   ├── diagrams/                           # Architectural, UML, DFD & ERD PNG diagrams
│   ├── report_builders/                    # Automated Pandoc & report generation scripts
│   └── notes/                              # Detailed theoretical Obsidian notes & study guides
│
└── PROJECT/                                # Full-Stack Software Engineering System
    ├── backend/                            # Python / FastAPI Diagnostic Engine
    │   ├── api/                            # REST Endpoints (routes.py, main.py, celery_tasks.py)
    │   ├── core/                           # Neuro-Symbolic Attribution Engine
    │   │   ├── dependency_linker.py        # Information Dependency DAG builder
    │   │   ├── backward_traversal.py       # Two-Phase Backward Causal Traversal resolver
    │   │   ├── step_judge.py               # Step-wise LLM evaluation with caching
    │   │   ├── cache.py                    # Deterministic SHA-256 prompt hashing (SQLite)
    │   │   ├── segmentation.py             # Context window budgeting & token manager
    │   │   ├── live_monitor.py             # Real-time streaming trace monitor
    │   │   └── llm_client.py               # Local Qwen2.5:7b (Ollama) & mock heuristic client
    │   ├── dataset/                        # Who&When Benchmark Dataset (184 multi-agent traces)
    │   ├── evaluation/                     # Benchmark evaluator & metrics calculator
    │   ├── dashboard/                      # Streamlit Python Diagnostic Dashboard
    │   ├── tests/                          # Automated Pytest suite (27 passing tests)
    │   └── main.py                         # Root entrypoint for backend
    │
    ├── frontend/                           # Modern React / Vite / Tailwind UI
    │   ├── src/components/
    │   │   ├── DagVisualizer.jsx           # Interactive Causal DAG (vis-network)
    │   │   ├── TraceInspector.jsx          # Forensic turn-by-turn inspector
    │   │   ├── BenchmarkView.jsx           # Empirical comparison table & live runner
    │   │   ├── CustomIngestionView.jsx     # 1-Click presets & raw console log parser
    │   │   ├── TelemetryView.jsx           # SHA-256 cache hits/misses & storage gauges
    │   │   └── Navbar.jsx                  # Header with real-time backend connection status
    │   └── src/services/api.js             # Client for FastAPI backend
    │
    ├── start_all.sh                        # One-click launcher for backend & frontend
    ├── start_backend.sh                    # Launches FastAPI on http://localhost:8000
    ├── start_frontend.sh                   # Launches React/Vite on http://localhost:5173
    ├── start_dashboard.sh                  # Launches Streamlit on http://localhost:8501
    ├── run_tests.sh                        # Executes full pytest suite (27/27 passing)
    └── test_all_who_and_when.sh            # Runs full Who&When benchmark on all 184 traces
```

---

## 🚀 Quickstart: Running the System

### Option 1: Full-Stack React + FastAPI Platform (Recommended)
```bash
cd PROJECT
./start_all.sh
```
- **Web UI:** [http://localhost:5173](http://localhost:5173)
- **API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check:** [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

### Option 2: Run Who&When Benchmark (184 Traces)
```bash
cd PROJECT
./test_all_who_and_when.sh
```
Evaluates all 184 multi-agent traces across AutoGen, ChatDev, and MetaGPT, reporting agent-level and step-level attribution accuracy (86.96%) against ICML 2025 baselines.

### Option 3: Python-Native Streamlit Dashboard
```bash
cd PROJECT
./start_dashboard.sh
```
- **Streamlit App:** [http://localhost:8501](http://localhost:8501)

### Option 4: Run Verification Test Suite (Pytest)
```bash
cd PROJECT
./run_tests.sh
```
Executes all 27 unit and integration tests covering API routes, causal traversal, dependency linking, deterministic prompt caching, log parsing, live streaming, and Who&When benchmark validation.

---

## 🔬 Core Algorithmic Contributions
1. **Dependency-Aware Backward Traversal ($O(V_c + E_c)$)**:
   Traverses only the causal ancestor subgraph $\text{Anc}(s_{\text{manifest}})$, isolating the true root cause $s^*$ from downstream inherited symptoms.
2. **Deterministic SHA-256 Prompt Caching**:
   Hashes `SHA256(Goal + StepContext + ActionPayload)` into SQLite B-Tree keys, achieving a **78.2% token budget reduction** and **~1.2 ms cached turn evaluation**.
3. **Suppression of LLM Recency Bias**:
   Eliminates the tendency of monolithic LLMs to blame the terminal agent where the crash surfaced, improving localization accuracy from 14.2% (All-at-Once) to **61.2%**.
