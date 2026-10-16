# 🏛️ 02 - System Architecture & Design

## 🏗️ 1. Architecture Overview

The system processes raw or structured multi-agent execution traces through a modular 5-phase attribution engine connected to an asynchronous backend and an interactive developer presentation layer.

```mermaid
flowchart TD
    subgraph InputLayer ["1. INPUT LAYER"]
        RawTrace["Failed Multi-Agent Trace Log\n(JSON / Console Text Log)"]
    end

    subgraph CoreEngine ["2. CORE PROCESSING & EVALUATION ENGINE"]
        Seg["Phase 1: Step Segmentation\n(Turn-Level Chunking)"]
        Judge["Phase 2: Cached Step-Wise Judge\n(Semantic Scoring against Goal)"]
        Cache[("Storage & Cache\nSHA256 Prompt Hashes\n(SQLite / Redis / MongoDB)")]
        Linker["Phase 3: Dependency Linker\n(Construct Information DAG)"]
        BackTraverse["Phase 4: Backward Causal Traversal\n(Graph Walk from Symptom)"]
        Resolver["Phase 5: Root-Cause Resolver\n(Source Error vs Symptom Isolation)"]
    end

    subgraph BackendQueue ["3. BACKEND & TASK QUEUE"]
        FastAPI["FastAPI REST Server\n(/api/v1/attribute)"]
        CeleryWorker["Celery Worker\n(Asynchronous Job Processing)"]
        RedisBroker["Redis Broker & Result Store"]
    end

    subgraph PresentationLayer ["4. PRESENTATION & DEVELOPER TOOLING"]
        Dashboard["Streamlit Interactive Dashboard\n• Color-Coded DAG Visualizer\n• Step-by-Step Inspector\n• Benchmark Analytics Suite"]
        MetricsHarness["Who&When Evaluation Harness\n(Agent Acc, Step Acc, Latency)"]
    end

    RawTrace --> Seg
    Seg --> Judge
    Judge <--> Cache
    Judge --> Linker
    Linker --> BackTraverse
    BackTraverse --> Resolver
    
    FastAPI <--> CeleryWorker
    CeleryWorker <--> RedisBroker
    FastAPI --> CoreEngine
    
    Resolver --> Dashboard
    Resolver --> MetricsHarness
```

---

## 📊 2. Data Flow Diagrams (DFD)

### Level-0 DFD (Context Diagram)
```mermaid
graph LR
    User["Multi-Agent Trace Log (Developer/Benchmark)"] --> |Trace JSON| System["0.0 Automated Failure Attribution System"]
    System --> |Attributed Verdict (Responsible Agent, Decisive Step, Justification, DAG)| DevDashboard["Developer Dashboard / API Client"]
```

### Level-1 DFD (Decomposition)
```mermaid
flowchart TD
    TraceIn["Multi-Agent Trace Log"] --> P1["1.0 Trace Segmentation"]
    P1 --> |Discrete Steps| P2["2.0 Step-Wise LLM Evaluator"]
    P2 <--> |Prompt Hash / Cached Result| DB1[("D1: Prompt Hash Cache")]
    P2 --> |Evaluated Steps & Scores| P3["3.0 Dependency Linker"]
    P3 --> |Information-Linked DAG| P4["4.0 Backward Traversal Engine"]
    P4 --> |Root Cause Verdict & Partitioned Symptoms| P5["5.0 Root-Cause Resolver"]
    P5 --> Out["Developer Dashboard / Output JSON"]
```

---

## 🔄 3. Process Logic & Step-by-Step Execution

```
[Start: Ingest Failed Trace]
       │
       ▼
[Phase 1: Trace Ingestion & Segmentation]
  - Parse turn tuples: (Agent, Recipient, Action Payload, Output State, Index)
  - Compress oversized turns (>4k tokens) preserving error messages & variable names
       │
       ▼
[Phase 2: Cached Step-Wise Evaluation]
  - For each step s_i in trace:
       ├── Generate SHA256 Prompt Hash: H = SHA256(Model || Goal || StepDetails)
       ├── Check Cache (SQLite/Redis/MongoDB)
       ├── IF cache hit: Retrieve score & anomaly verdict
       └── ELSE: Query LLM Judge, parse JSON verdict, and store in Cache
       │
       ▼
[Phase 3: Dependency-Aware Graphing (DAG)]
  - Add nodes for all steps: V = {0, 1, ..., N-1}
  - Build edges (u -> v):
       ├── Sequential conversational adjacency: (i-1) -> i
       ├── Direct agent reply: Recipient(u) == Agent(v)
       └── Shared variable/state flow: Entities produced in u consumed in v
       │
       ▼
[Phase 4 & 5: Backward Causal Traversal & Root-Cause Resolution]
  - Identify anomalous nodes: A = {i | Anomaly(i) == True or Score(i) < 0.7}
  - Find manifest failure symptom: s_fail = max(A)
  - Find causal ancestors leading to failure: Anc = Ancestors(G, s_fail) U {s_fail}
  - Isolate Root Cause:
       Earliest step r in (A ∩ Anc) such that Predecessors(r) are valid (clean)
  - Partition remaining anomalies into Propagated Symptoms: S = A \ {r}
       │
       ▼
[Output Verdict & DAG to Dashboard / API]
       │
       ▼
[End]
```

---

## 🗄️ 4. Entity-Relationship (ER) Schema

```mermaid
erDiagram
    TRACES ||--|{ STEPS : contains
    STEPS ||--o{ DEPENDENCIES : "is source of"
    STEPS ||--o{ DEPENDENCIES : "is target of"
    STEPS ||..o| CACHE_JUDGEMENTS : "queries via hash"

    TRACES {
        string trace_id PK
        string title
        string environment_name "AutoGen / ChatDev / MetaGPT"
        string task_goal
        int total_steps
        string final_outcome "failed / success"
        json ground_truth "responsible_agent, decisive_step_index, reason"
    }

    STEPS {
        string step_id PK
        string trace_id FK
        int step_index
        string agent_name
        string recipient
        string action_type
        text input_context
        text action_payload
        text output_state
        float llm_score
        boolean is_anomalous
        string anomaly_reason
    }

    DEPENDENCIES {
        string dependency_id PK
        int source_step_index FK
        int target_step_index FK
        string data_variable "Variable, function, or topic passed"
        string dependency_type "data_flow / message_reply / shared_state"
        float confidence
    }

    CACHE_JUDGEMENTS {
        string prompt_hash PK "SHA256(Model || Prompt)"
        string model_name "Qwen2.5-7B-Instruct / Mock"
        text prompt_text
        json response_json "is_valid, score, anomaly_detected, reason"
        datetime created_at
    }
```

---

## 🔗 Related Notes
- [[00 - Project Overview & Index]]
- [[03 - Core Engine Implementation]]
- [[05 - API, Async Queue & Dashboard]]
