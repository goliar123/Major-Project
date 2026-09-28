# ⚙️ 03 - Core Engine Implementation

## 📂 1. Implementation Codebase Structure

The core engine is located under `d:/Projects/LLM/core/` and comprises the following Python modules:

```
core/
├── segmentation.py         # Trace parser, turn chunker, and token budgeter
├── cache.py                # SHA256 prompt hashing cache with SQLite/Redis/MongoDB
├── llm_client.py           # Multi-provider LLM interface (vLLM, Ollama, Gemini, Mock)
├── step_judge.py           # Cached step-wise semantic evaluator
├── dependency_linker.py    # NetworkX Directed Acyclic Graph (DAG) constructor
├── backward_traversal.py   # Backward causal traversal & root-cause resolver
├── baselines/              # Monolithic All-at-Once, Step-by-Step, Binary Search
└── engine.py               # Master attribution pipeline orchestrator
```

---

## 🧩 2. Module Deep-Dives

### 2.1. Trace Segmentation (`core/segmentation.py`)
- **Purpose**: Prevents context-window overflow on long multi-agent logs (where traces often exceed 32k tokens) by breaking the trace into ordered `ExecutionStep` instances.
- **Key Method**: `segment_trace(trace: MultiAgentTrace) -> List[ExecutionStep]`
  - Bounds individual turns to $\le 4096$ tokens.
  - Retains head ($60\%$) and tail ($30\%$) of oversized turns to preserve initial instructions and resulting error stack traces while omitting middle fluff.
- **Console Log Parser**: `parse_raw_log_text(log_text: str)` uses regex heuristics `[Sender -> Recipient]: payload` to parse unstructured console logs from AutoGen, MetaGPT, or LangGraph.

### 2.2. SHA256 Prompt Caching (`core/cache.py`)
- **Purpose**: Avoids duplicate LLM inference calls across benchmark runs and testing cycles, saving ~65% of token/GPU quota.
- **Mathematical Form**:
  $$\text{PromptHash} = \text{SHA256}(\text{ModelName} \parallel \text{"||"} \parallel \text{PromptText})$$
- **Supported Storage Backends**:
  - `sqlite`: Local default database stored in `cache.db`.
  - `redis`: High-speed in-memory cache for distributed deployment.
  - `mongodb`: Document store for persistent query logs and cached judgments.
  - `memory`: In-process fast lookup dict.
- **Key Methods**:
  - `get(prompt_text, model_name) -> Optional[Dict[str, Any]]`
  - `set(prompt_text, response_data, model_name) -> bool`
  - `get_stats() -> Dict[str, Any]` (Tracks hits, misses, hit rate percentage).

### 2.3. Unified LLM Client (`core/llm_client.py`)
- **Purpose**: Multi-provider LLM dispatcher supporting local open-weight inference and hosted cloud APIs.
- **Supported Providers**:
  - `vllm` / `ollama`: For local open-weight models (e.g. `Qwen/Qwen2.5-7B-Instruct`).
  - `openai` / `groq` / `openrouter`: OpenAI-compatible standard endpoints with JSON response mode enforcement.
  - `gemini`: Google Gemini API integration.
  - `mock`: Intelligent deterministic heuristic judge for zero-cost local testing and development.
- **Token Telemetry**: Automatically records cumulative prompt and completion tokens.

### 2.4. Step-Wise Evaluator (`core/step_judge.py`)
- **Purpose**: Evaluates a single turn $s_i$ against the overarching task goal and the immediate input context.
- **Evaluation Prompt Structure**:
  ```text
  ### STEP-WISE EVALUATION
  Task Goal: {task_goal}
  Step Index: {step_index}
  Agent: {agent_name}
  Recipient: {recipient}
  Action Type: {action_type}

  Input Context: {input_context}
  Action Payload: {action_payload}
  Output State: {output_state}
  ```
- **Output Schema**:
  ```json
  {
    "is_valid": true,
    "score": 0.95,
    "anomaly_detected": false,
    "error_category": null,
    "is_propagated_symptom": false,
    "justification": "Explanation..."
  }
  ```

### 2.5. Information-Dependency Linker (`core/dependency_linker.py`)
- **Purpose**: Builds a Directed Acyclic Graph (DAG) $G = (V, E)$ using `NetworkX`.
- **Edge Construction Rules**:
  1. **Sequential Adjacency**: Edge $(i-1 \to i)$ with `dependency_type="data_flow"`.
  2. **Message Recipient Matching**: Edge $(i \to j)$ when `Recipient(s_i) == Agent(s_j)`.
  3. **Entity & Variable Reuse**: Extracts variable names, table identifiers, and function names produced in step $i$ and checks for consumption in step $j$ (`dependency_type="shared_state"`).

### 2.6. Backward Causal Traversal (`core/backward_traversal.py`)
- **Purpose**: Distinguishes the originating **Root Cause** error from downstream **Propagated Symptoms**.
- **Algorithm**:
  1. Find all anomalous step indices: $A = \{i \mid \text{score}(i) < 0.7 \text{ or } \text{anomaly\_detected}(i) = \text{True}\}$.
  2. Locate manifest failure step $s_{\text{manifest}} = \max(A)$.
  3. Compute causal ancestor subgraph: $\text{Ancestors}(G, s_{\text{manifest}}) \cup \{s_{\text{manifest}}\}$.
  4. Isolate Root Cause $r$: The earliest step in causal ancestors whose predecessors in $G$ are all valid (clean).
  5. Classify all remaining anomalies $A \setminus \{r\}$ as **Propagated Symptoms**.
  6. Generate node statuses for visual DAG rendering (`normal` 🟢, `root_cause` 🔴, `propagated_symptom` 🟠).

---

## 🏛️ 3. Master Engine Orchestrator (`core/engine.py`)

The `AttributionEngine.attribute_trace(trace)` method binds all 5 phases into a clean end-to-end execution:

```python
def attribute_trace(self, trace: MultiAgentTrace) -> AttributionVerdict:
    # 1. Step Segmentation
    segmented_steps = self.segmenter.segment_trace(trace)
    
    # 2. Cached Step-Wise Judging
    evaluations = {s.step_index: self.judge.evaluate_step(trace.task_goal, s) for s in segmented_steps}
    
    # 3. Information Dependency DAG Construction
    dag, edges = self.linker.build_dependency_dag(segmented_steps)
    
    # 4 & 5. Backward Causal Traversal & Root Cause Resolution
    verdict = self.resolver.resolve_root_cause(
        trace_id=trace.trace_id,
        task_goal=trace.task_goal,
        steps=segmented_steps,
        evaluations=evaluations,
        dag=dag,
        edges=edges
    )
    return verdict
```

---

## 🔗 Related Notes
- [[02 - System Architecture & Design]]
- [[04 - Benchmark & Evaluation Results]]
- [[05 - API, Async Queue & Dashboard]]
