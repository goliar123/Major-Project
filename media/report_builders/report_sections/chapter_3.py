"""
Chapter 3: System Requirements Specification module for Major Project Phase-I Report (B12 Format).
"""
import os
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

DIAG_DIR = "/home/goliar/Documents/LLM/media/diagrams/docs_diagrams"

def add_chapter_3(b):
    doc = b.doc

    def set_cell_background(cell, hex_color):
        from docx.oxml import parse_xml
        from docx.oxml.ns import nsdecls
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=40, bottom=40, left=70, right=70):
        from docx.oxml import parse_xml
        from docx.oxml.ns import nsdecls
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    b.h1("CHAPTER 3: SYSTEM REQUIREMENTS SPECIFICATION")

    b.h2("3.1 Introduction")
    b.p(
        "The System Requirements Specification (SRS) establishes the authoritative technical contract governing the development, verification, "
        "and evaluation of the Automated Failure Attribution Engine. Formulated in accordance with IEEE Std 830-1998 standards, this specification "
        "delineates the functional requirements, operational boundaries, non-functional quality attributes, hardware constraints, data models, and "
        "UML structural designs necessary to deliver deterministic, explainable, and computationally efficient failure attribution for multi-agent systems."
    )

    b.h3("3.1.1 Purpose")
    b.p(
        "The primary purpose of this specification is to provide a complete, rigorous, and unambiguous reference for software engineers, MLOps "
        "practitioners, quality assurance teams, and academic evaluators. In production multi-agent environments, diagnosing failures has historically "
        "relied on ad-hoc script inspection or manual review of massive execution logs. This document defines the functional requirements and "
        "architectural specifications for an autonomous, neuro-symbolic platform that replaces manual post-mortem debugging with deterministic "
        "graph-theoretic root cause isolation. The system ensures that enterprise developers can rapidly pinpoint faulty agents, eliminate symptom "
        "misattribution, understand cascading state corruptions, and deploy reliable multi-agent workflows."
    )

    b.h3("3.1.2 Definitions, Acronyms and Abbreviations")
    b.p("Table 3.1.3: Definitions, Acronyms and Abbreviations", bold=True, size=11, space_before=4, space_after=2)
    tbl_terms = doc.add_table(rows=16, cols=2)
    tbl_terms.alignment = WD_TABLE_ALIGNMENT.CENTER
    terms_data = [
        ("Term / Acronym", "Definition"),
        ("LLM", "Large Language Model, autoregressive neural network trained on massive corpora for language reasoning."),
        ("Multi-Agent System (MAS)", "Architecture composing multiple autonomous LLM instances collaborating toward a shared objective."),
        ("DAG", "Directed Acyclic Graph, a finite directed graph with no directed cycles used to model causal information dependencies."),
        ("Symptom Misattribution", "The diagnostic error of blaming a downstream crashing agent instead of the upstream originating error step."),
        ("Originating Root Cause", "The earliest execution step in a DAG that introduced corrupted state despite receiving clean parent inputs."),
        ("Propagated Symptom", "An anomalous step that inherited flawed state from an upstream root cause and exhibited secondary failure."),
        ("Independent Logic Bug", "A secondary failure occurring due to an agent's internal reasoning flaw independent of upstream state."),
        ("Transitive Ancestor Closure", "The complete set of all upstream graph nodes possessing a directed path reaching the manifest failure."),
        ("Topological Sort", "A linear ordering of graph vertices such that for every directed edge u -> v, u precedes v in the ordering."),
        ("SHA256 Prompt Hashing", "Cryptographic hash computed from model name and normalized prompt text to enable deterministic caching."),
        ("Ollama", "High-performance local LLM execution engine providing OpenAI-compatible REST endpoints for inference."),
        ("Pydantic", "Data validation and settings management library using Python type annotations for strict schema enforcement."),
        ("NetworkX", "Python package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks."),
        ("Who&When Benchmark", "Standardized ICML 2025 benchmark callset measuring agent-level (Who) and step-level (When) attribution accuracy."),
        ("MockJudge", "Rule-based heuristic evaluator with 25+ failure signature patterns serving as zero-downtime offline fallback.")
    ]
    for r_idx, (t, d) in enumerate(terms_data):
        row = tbl_terms.rows[r_idx]
        row.cells[0].text = t
        row.cells[1].text = d
        if r_idx == 0:
            set_cell_background(row.cells[0], "E2E8F0")
            set_cell_background(row.cells[1], "E2E8F0")
            row.cells[0].paragraphs[0].runs[0].bold = True
            row.cells[1].paragraphs[0].runs[0].bold = True
        set_cell_margins(row.cells[0], top=20, bottom=20, left=50, right=50)
        set_cell_margins(row.cells[1], top=20, bottom=20, left=50, right=50)

    b.h3("3.1.3 Scope")
    b.p(
        "The scope of the Automated Failure Attribution Engine spans the complete lifecycle of post-execution multi-agent diagnosis:\n\n"
        "1. Ingestion of Multi-Agent Trace Logs: Ingests trace logs in structured JSON, JSONL, and unstructured console text emitted by Microsoft AutoGen, "
        "LangChain LangGraph, CrewAI, and MetaGPT.\n"
        "2. Context Token Budgeting: Enforces strict per-step token ceilings (default 4,096 tokens) utilizing an intelligent head-and-tail slicing policy "
        "that prevents LLM context overflow while preserving critical initial instructions and terminal error traces.\n"
        "3. Localized Semantic Turn Evaluation: Executes discrete turn-level evaluations querying a local Qwen2.5:7b model via Ollama in structured JSON "
        "mode, determining step validity, anomaly severity, and semantic bug categories.\n"
        "4. Deterministic Cryptographic Caching: Implements a multi-tier cache (in-memory dictionary and SQLite persistent store) indexed by SHA256 hashes "
        "of canonical prompt text, eliminating redundant inference and achieving sub-millisecond lookups.\n"
        "5. Zero-Downtime Heuristic Fallback: Integrates a rule-based MockJudge featuring 25+ regex and substring failure signatures to guarantee continuous "
        "diagnostic availability during local LLM service interruptions.\n"
        "6. Information Dependency Graph Synthesis: Synthesizes a NetworkX DiGraph capturing sequential execution flow (confidence 0.85) and long-range "
        "shared state dependencies (confidence 0.95) extracted via regex entity matching.\n"
        "7. Backward Causal Traversal & Root Cause Isolation: Traverses the DAG backward from the manifest failure symptom, computes the Transitive "
        "Ancestor Closure, and applies topological blame resolution to isolate the true Originating Root Cause.\n"
        "8. 2D Error Taxonomy Classification: Maps every anomalous node along Causal Role (Root Cause, Propagated Symptom, Independent Bug) and Semantic "
        "Bug Category across 25+ failure types.\n"
        "9. Shortest Causal Path Computation: Computes the step-by-step failure chain from originating root cause to final manifest crash using Dijkstra's algorithm.\n"
        "10. Presentation & API Services: Provides an interactive Streamlit web dashboard for visual graph inspection and a high-throughput FastAPI REST "
        "interface for automated CI/CD pipeline integration.\n\n"
        "Explicitly Out of Scope for Phase-I: Real-time socket-level agent execution interception (pausing execution mid-stream), automated code-patch "
        "synthesis, and proprietary commercial cloud APM platform integrations (Datadog, Dynatrace).",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY
    )

    b.h3("3.1.4 References")
    b.p(
        "1. IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications.\n"
        "2. ICML 2025 Who&When Dataset: Benchmarking Failure Attribution in LLM-Based Multi-Agent Systems.\n"
        "3. Pearl, Judea. 'Causality: Models, Reasoning, and Inference.' Cambridge University Press, 2009.\n"
        "4. NetworkX Developer Documentation: Algorithms for Directed Acyclic Graphs (Release 3.2).\n"
        "5. Ollama API Documentation: OpenAI Compatibility Endpoints (/v1/chat/completions).\n"
        "6. Pydantic v2 Documentation: Data Validation and High-Performance Parsing.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY
    )

    b.h3("3.1.5 Overview")
    b.p(
        "The remainder of this chapter is structured into four core divisions: Section 3.2 provides the general system description including product "
        "perspective, functional breakdown, user classes, operational constraints, and dependencies; Section 3.3 details the 15 functional requirements, "
        "12 non-functional requirements, user interface specifications, database schemas, and hardware matrices; Section 3.4 presents the 7 UML and "
        "architectural diagrams with accompanying technical narratives; and Section 3.5 provides a synthesis summary.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY
    )

    b.h2("3.2 General Description")
    b.h3("3.2.1 Product Perspective")
    b.p(
        "The Automated Failure Attribution Engine operates as an autonomous diagnostic middleware and observability platform for LLM multi-agent "
        "ecosystems. It does not replace the underlying multi-agent frameworks (such as AutoGen or LangGraph); rather, it interfaces with their output "
        "logs and runtime traces. The major external entities interacting with the system include:\n\n"
        "• AI Engineer / System Developer: Submits execution traces for diagnostic inspection, configures evaluation parameters, and views causal graph visualizations.\n"
        "• Multi-Agent Frameworks: Upstream orchestrators (AutoGen, ChatDev, MetaGPT, CrewAI) that generate execution traces during autonomous operation.\n"
        "• Local LLM Inference Engine: An Ollama or vLLM daemon hosting Qwen2.5:7b, servicing semantic evaluation prompts via high-throughput HTTP REST calls.\n"
        "• Diagnostic Cache Store: Persistent SQLite database storing SHA256 prompt-response pairs to prevent redundant GPU evaluations.\n"
        "• CI/CD Pipeline: Automated testing workflows invoking the attribution engine via REST API to evaluate regression test traces.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY
    )

    b.h3("3.2.2 Product Functions")
    b.p(
        "The system executes the following 14 major functional operations:\n"
        "1. Trace Parsing: Ingests structured JSON/JSONL and raw unstructured text logs.\n"
        "2. Token Budgeting: Enforces token bounds via 60% head and 30% tail retention to prevent context overflow.\n"
        "3. Step Normalization: Instantiates standardized ExecutionStep entities capturing agent name, recipient, payload, and state.\n"
        "4. SHA256 Hashing: Computes deterministic 256-bit hashes combining model identifier and canonical prompt content.\n"
        "5. Cache Lookup & Management: Retrieves cached verdicts in O(1) time or updates persistent SQLite storage upon cache miss.\n"
        "6. Local LLM Evaluation: Formulates expert diagnostic prompts instructing the model to return structured JSON verdicts.\n"
        "7. Heuristic Fallback: Automatically routes queries to MockJudge containing 25+ failure signatures when the LLM daemon is offline.\n"
        "8. Sequential Flow Linking: Establishes directed execution flow edges (confidence 0.85) between adjacent conversation steps.\n"
        "9. Entity Dependency Extraction: Extracts programming identifiers via regex and establishes shared_state edges (confidence 0.95).\n"
        "10. Transitive Ancestor Closure: Computes all upstream causal dependencies reaching the manifest symptom via nx.ancestors().\n"
        "11. Topological Root Cause Isolation: Sorts anomalous nodes topologically and identifies the earliest node with clean parent states.\n"
        "12. 2D Error Taxonomy Classification: Classifies nodes into Root Cause, Propagated Symptom, Independent Bug, or Recovery Failure.\n"
        "13. Shortest Causal Path Computation: Computes the step-by-step propagation chain from root cause to final crash using Dijkstra's algorithm.\n"
        "14. Interactive Visual Presentation: Renders interactive DAGs, trace inspectors, and benchmark comparisons in Streamlit and FastAPI.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY
    )

    b.h3("3.2.3 User Characteristics")
    b.p(
        "The system is designed for five distinct user classes:\n\n"
        "1. AI & LLM Systems Engineers: Deeply familiar with multi-agent orchestration, prompt engineering, and conversational state debugging. Require fine-grained causal chain inspection.\n"
        "2. MLOps & Observability Engineers: Responsible for system reliability, CI/CD pipeline integration, and GPU resource budgeting. Require fast caching and API automation.\n"
        "3. Academic Researchers & Benchmark Evaluators: Focused on evaluating attribution accuracy, comparing baseline algorithms, and reproducing Who&When benchmark results.\n"
        "4. Software Quality Assurance (QA) Engineers: Inspecting failure traces from automated test suites to identify whether failures stem from code generation or agent logic.\n"
        "5. System Administrators: Managing server infrastructure, Ollama daemons, SQLite cache pruning, and REST endpoint availability.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY
    )

    b.h3("3.2.4 General Constraints")
    b.p(
        "The design and deployment of the system are subject to 12 operational constraints:\n"
        "1. Determinism Constraint: Graph traversal and topological sorting must be 100% deterministic given identical step evaluations.\n"
        "2. Offline Inference Constraint: The primary evaluator must operate locally (via Ollama) without requiring proprietary external APIs (such as OpenAI).\n"
        "3. Memory Footprint Constraint: The DAG representation must scale efficiently, consuming <100MB RAM for traces up to 1,000 steps.\n"
        "4. Cache Collision Constraint: The caching engine must use SHA256 (256-bit entropy) ensuring negligible collision probability across millions of prompts.\n"
        "5. Context Window Constraint: Discrete step evaluation prompts must strictly remain within the 4,096 token boundary of the local model.\n"
        "6. Time Complexity Constraint: Graph traversal algorithms (ancestors, topological sort, shortest path) must execute in O(V + E) time.\n"
        "7. Zero-Downtime Fallback: When the local LLM daemon is unreachable, the system must transparently fall back to MockJudge without raising uncaught exceptions.\n"
        "8. Trace Format Independence: The segmenter must normalize diverse orchestrator schemas into a unified Pydantic schema.\n"
        "9. Non-Destructive Storage: Cache pruning or database updates must maintain transactional ACID guarantees in SQLite.\n"
        "10. Python Runtime Constraint: Core modules must be fully compatible with modern Python 3.12+ and 3.14 runtimes.\n"
        "11. API Latency Constraint: Cached attribution queries must return complete verdicts within <50 milliseconds.\n"
        "12. Reproducibility Constraint: All benchmark metric calculations must strictly conform to the ICML 2025 Who&When evaluation protocols.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY
    )

    b.h3("3.2.5 Assumptions and Dependencies")
    b.p(
        "Assumptions:\n"
        "• The ingested execution traces accurately capture chronological agent interactions.\n"
        "• Upstream multi-agent systems maintain persistent agent names across conversational turns.\n"
        "• A functioning Python 3.12+ environment with NetworkX and Pydantic is available.\n"
        "• For neural evaluation, Ollama or an OpenAI-compatible endpoint is reachable over localhost HTTP.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY
    )

    b.p("Table 3.2.5: Software Dependencies and Operational Purpose", bold=True, size=11, space_before=4, space_after=2)
    tbl_deps = doc.add_table(rows=10, cols=2)
    tbl_deps.alignment = WD_TABLE_ALIGNMENT.CENTER
    deps_data = [
        ("Dependency", "Purpose"),
        ("Python 3.14 / venv", "Core runtime environment executing pipeline orchestrator and test suites."),
        ("NetworkX (3.x)", "Constructs Directed Acyclic Graphs, computes transitive ancestor closures, and shortest paths."),
        ("Pydantic (v2)", "Enforces strict type validation, JSON schema generation, and data serialization."),
        ("Ollama / Qwen2.5:7b", "Provides local GPU/CPU neural language model inference for step-wise evaluation."),
        ("SQLite3 (Built-in)", "Provides persistent ACID-compliant key-value prompt cache storage."),
        ("FastAPI / Uvicorn", "Exposes asynchronous REST API endpoints for programmatic trace submission."),
        ("Streamlit (1.38+)", "Renders interactive web dashboard, DAG visualizer, and benchmark runner."),
        ("HTTPX", "High-performance asynchronous HTTP client handling LLM endpoint communications."),
        ("Pytest (8.x)", "Executes automated unit and integration regression test suites.")
    ]
    for r_idx, (d, p_val) in enumerate(deps_data):
        row = tbl_deps.rows[r_idx]
        row.cells[0].text = d
        row.cells[1].text = p_val
        if r_idx == 0:
            set_cell_background(row.cells[0], "E2E8F0")
            set_cell_background(row.cells[1], "E2E8F0")
            row.cells[0].paragraphs[0].runs[0].bold = True
            row.cells[1].paragraphs[0].runs[0].bold = True
        set_cell_margins(row.cells[0], top=20, bottom=20, left=50, right=50)
        set_cell_margins(row.cells[1], top=20, bottom=20, left=50, right=50)

    b.h2("3.3 Specific Requirements")
    b.h3("3.3.1 Functional Requirements")
    
    fr_list = [
        ("FR-01: Heterogeneous Trace Ingestion",
         "The system shall ingest multi-agent execution traces in structured JSON, JSONL, and unstructured console text formats.",
         "Raw multi-agent execution log file.",
         "Standardized MultiAgentTrace domain entity.",
         "Extracts trace_id, task_goal, agent names, action payloads, and tool outputs using flexible key matching."),
        
        ("FR-02: Context Token Budgeting & Truncation",
         "The system shall enforce a strict token ceiling (default 4096 tokens) on individual step payloads to prevent LLM context overflow.",
         "Unbounded text string from tool output or agent message.",
         "Token-bounded string retaining 60% head and 30% tail with an omission marker.",
         "Computes word/token count; splits content into head and tail slices; inserts omission notice preserving error traces."),
        
        ("FR-03: Canonical Evaluation Prompt Construction",
         "The system shall format a standardized diagnostic prompt capturing task goal, step index, agent name, recipient, input context, action payload, and output state.",
         "ExecutionStep entity and task goal string.",
         "Structured canonical prompt string.",
         "Interpolates step attributes into a deterministic template enforcing consistent whitespace and token alignment."),
         
        ("FR-04: Deterministic SHA256 Cache Key Generation",
         "The system shall compute a cryptographic SHA256 hash from the concatenated model identifier and canonical prompt text.",
         "Model name string and canonical prompt string.",
         "64-character hexadecimal SHA256 hash string.",
         "Normalizes strings via strip(); computes hashlib.sha256(f'{model}||{prompt}').hexdigest()."),
         
        ("FR-05: Multi-Tier Cache Lookup & Persistence",
         "The system shall check in-memory cache and persistent SQLite tables before invoking LLM inference.",
         "SHA256 prompt hash.",
         "StepEvaluation entity on cache hit, or None on cache miss.",
         "Queries memory dict -> queries SQLite prompt_cache table -> increments hit/miss counters -> updates cache on completion."),
         
        ("FR-06: Structured Local LLM Evaluation",
         "The system shall query a local Ollama instance hosting Qwen2.5:7b using OpenAI-compatible JSON mode.",
         "Prompt string and expert diagnostic system prompt.",
         "JSON object containing is_valid, score, anomaly_detected, error_category, and justification.",
         "Dispatches POST request to /v1/chat/completions with response_format={'type': 'json_object'}; parses response into StepEvaluation."),
         
        ("FR-07: Heuristic MockJudge Zero-Downtime Fallback",
         "The system shall automatically fall back to rule-based evaluation if the LLM endpoint is unreachable.",
         "Step context and action payload text.",
         "Heuristic StepEvaluation verdict.",
         "Scans text against 25+ regex/substring failure patterns (e.g., 'reset to nan', 'drop table', 'lisinopril'); assigns calibrated scores."),
         
        ("FR-08: Sequential Graph Edge Construction",
         "The system shall add directed edges between adjacent conversational turns representing execution flow.",
         "List of ExecutionStep entities.",
         "NetworkX DiGraph with sequential edges (confidence 0.85).",
         "Iterates through steps from 1 to N-1; creates DependencyEdge(source=i-1, target=i, type='data_flow')."),
         
        ("FR-09: Long-Range Entity & State Linking",
         "The system shall identify cross-step variable passing and message replies between non-adjacent agents.",
         "Source and target step payloads.",
         "Long-range DependencyEdge entities (confidence 0.95).",
         r"Extracts programming identifiers (\b[a-z_][a-z0-9_]{3,}\b); filters stop words; links matching entities as shared_state."),
         
        ("FR-10: Manifest Symptom Identification",
         "The system shall isolate the latest anomalous step in the execution trace.",
         "Dictionary of StepEvaluation entities.",
         "Integer index of manifest failure symptom.",
         "Filters steps where anomaly_detected=True or score < 0.7; selects the highest step index; falls back to step N-1."),
         
        ("FR-11: Transitive Ancestor Closure Computation",
         "The system shall compute all graph ancestors that have a directed path reaching the manifest symptom.",
         "NetworkX DiGraph and manifest failure index.",
         "Set of causal ancestor step indices.",
         "Executes nx.ancestors(dag, manifest_failure_idx); adds manifest failure index; intersects with anomalous indices."),
         
        ("FR-12: Topological Root Cause Isolation",
         "The system shall identify the earliest anomalous step whose immediate graph parents are completely clean.",
         "Causal anomaly list and DAG predecessor structure.",
         "Integer index of true Originating Root Cause.",
         "Iterates in topological order; checks dag.predecessors(cand); if no predecessor is anomalous, selects candidate and halts."),
         
        ("FR-13: 2D Error Taxonomy Classification",
         "The system shall categorize every node along Causal Role and Semantic Bug Category dimensions.",
         "Root cause index, anomaly list, and StepEvaluations.",
         "List of NodeStatus entities (root_cause, propagated_symptom, normal).",
         "Partitions anomalies: earliest clean-parent node = root_cause; remaining causal anomalies = propagated_symptom; maps 25+ bug categories."),
         
        ("FR-14: Shortest Causal Path Generation",
         "The system shall compute the minimal step-by-step propagation chain from root cause to final symptom.",
         "DAG, root cause index, and manifest symptom index.",
         "List of step indices representing the causal chain.",
         "Executes nx.shortest_path(dag, source=root_cause, target=manifest_failure); formats multi-tier explanation."),
         
        ("FR-15: Benchmark Evaluation & Comparative Analytics",
         "The system shall evaluate full trace suites against ground truth annotations and compare against baselines.",
         "List of MultiAgentTrace entities with GroundTruth.",
         "BenchmarkResult entity.",
         "Computes Agent-level Accuracy (Who), Step-level Accuracy (When), and Strict Joint Accuracy; compares against All-at-Once baseline.")
    ]

    for title, desc, inp, out, proc in fr_list:
        b.h4(title)
        b.p(f"Description: {desc}", size=11.5, space_after=2)
        b.p(f"• Input: {inp}", size=11, space_after=1)
        b.p(f"• Output: {out}", size=11, space_after=1)
        b.p(f"• Processing Logic: {proc}", size=11, space_after=6)

    b.h3("3.3.2 Non-Functional Requirements")
    nfr_list = [
        ("NFR-01: Performance & Graph Traversal Latency", "Graph operations including transitive ancestor closure (nx.ancestors), topological sorting, and shortest-path computation must execute within O(V + E) time complexity, completing in <10 milliseconds for traces up to 1,000 nodes."),
        ("NFR-02: Cache Hit Efficiency & Latency Reduction", "The SHA256 prompt hashing cache must eliminate 100% of redundant LLM inference calls on duplicate prompts, achieving a cache hit retrieval latency of <2 milliseconds from SQLite and <0.1 milliseconds from in-memory cache."),
        ("NFR-03: High Availability & Zero-Downtime Fallback", "The attribution pipeline must guarantee 100% diagnostic availability. In the event of network timeouts, GPU out-of-memory errors, or local Ollama daemon termination, the system must transparently fall back to the heuristic MockJudge without failing the trace."),
        ("NFR-04: Deterministic Reproducibility", "Given identical trace inputs and cache states, the backward traversal and blame resolution algorithms must produce 100% identical AttributionVerdict outputs across repeated executions."),
        ("NFR-05: Context Window Memory Safety", "The segmentation module must enforce a strict token budget ensuring that no single evaluation prompt exceeds the maximum context window of the target local language model (4,096 tokens)."),
        ("NFR-06: Modularity & Loose Coupling", "The architecture must maintain strict separation of concerns across segmentation, evaluation, graph linking, causal traversal, and reporting modules, allowing individual components to be upgraded independently."),
        ("NFR-07: Data Integrity & Storage Safety", "Cache writes to SQLite must maintain ACID compliance using write-ahead logging (WAL) and primary key uniqueness constraints on prompt hashes, preventing corrupt writes during concurrent trace evaluation."),
        ("NFR-08: Scalability", "The system must support batch evaluation of benchmark datasets containing hundreds of traces without unbounded memory growth, releasing graph structures following verdict generation."),
        ("NFR-09: Diagnostic Explainability", "Every attribution verdict must provide human-readable, multi-tier narrative justifications explaining why the selected step was deemed the originating root cause and how downstream steps inherited the flawed state."),
        ("NFR-10: Test Coverage & Verification", "The codebase must maintain an automated test suite achieving 100% pass rates across unit and integration tests covering backward traversal, cache operations, dependency linking, and API endpoints."),
        ("NFR-11: Security & Local Privacy", "The default operational mode must process all execution traces entirely on local hardware, ensuring that proprietary enterprise code and sensitive agent prompts are never transmitted over external networks."),
        ("NFR-12: Portability & Cross-Platform Support", "The codebase must operate seamlessly across Linux (Ubuntu, Fedora), macOS, and Windows environments supporting Python 3.12+ virtual environments.")
    ]
    for title, desc in nfr_list:
        b.h4(title)
        b.p(desc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=11.5, space_after=6)

    b.h3("3.3.3 User Interface Requirements")
    b.p(
        "The system provides a comprehensive Streamlit-based web dashboard and FastAPI endpoints structured into 7 core views:\n\n"
        "1. Executive Diagnostics Dashboard: Provides high-level operational statistics including total traces evaluated, average attribution latency, overall cache hit rate, and distribution of identified error categories.\n"
        "2. Trace Inspector & Step Browser: Enables chronological inspection of discrete agent turns. Users can view agent roles, recipient identifiers, input context, action payloads, and raw tool output states with syntax highlighting.\n"
        "3. Interactive DAG Visualization Canvas: Renders the NetworkX dependency graph with color-coded node statuses (Green: Normal, Red: Originating Root Cause, Orange: Propagated Symptom, Grey: Unreached). Clicking a node reveals its LLM anomaly score and justification.\n"
        "4. Causal Path Explorer: Displays the shortest-path chain tracing the step-by-step propagation of corrupted state from the originating fault to the final manifest crash.\n"
        "5. Baseline Comparison Studio: Runs traces concurrently through All-at-Once, Step-by-Step Isolated, Binary Search, and Dependency-Aware Backward Traversal, displaying side-by-side blame matrices and accuracy comparisons.\n"
        "6. Benchmark Suite Runner: Executes the full 184-trace Who&When benchmark suite, plotting accuracy bar charts (Agent-level, Step-level, Strict Joint) and token consumption metrics.\n"
        "7. System Settings & Cache Manager: Provides configuration controls for LLM model selection (Qwen2.5:7b, Gemini, Mock), anomaly score threshold (default 0.7), cache backend switching (SQLite/Redis), and cache purge actions.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY
    )

    b.h3("3.3.4 Metadata and Schema of Database")
    b.p(
        "The persistence architecture of the Automated Failure Attribution Engine is designed around a dual-tier storage strategy: "
        "SQLite provides lightweight, ACID-compliant local relational persistence for prompt caching and trace metadata, while NetworkX "
        "manages in-memory directed graphs during diagnostic traversal. To guarantee strict data integrity, type safety, and zero schema drift, "
        "all database entities are mapped to Pydantic BaseModels in the Python application layer before persistence. The relational schema is "
        "formalized across seven relational tables detailed in Tables 3.5 through 3.11.",
        align=WD_ALIGN_PARAGRAPH.JUSTIFY
    )

    # Table 3.5: multi_agent_traces Schema
    t35_headers = ["Field Name", "Data Type", "Constraints", "Semantic Description"]
    t35_rows = [
        ["trace_id", "VARCHAR(64)", "PRIMARY KEY, NOT NULL", "Unique alphanumeric identifier generated for each ingested multi-agent trace."],
        ["title", "VARCHAR(255)", "NOT NULL", "Human-readable descriptive title of the multi-agent task or benchmark scenario."],
        ["environment_name", "VARCHAR(64)", "NOT NULL", "Execution framework name (e.g., autogen, chatdev, metagpt, gaia, assistantbench)."],
        ["task_goal", "TEXT", "NOT NULL", "The global user prompt, objective specification, and constraints governing orchestration."],
        ["total_steps", "INTEGER", "CHECK(total_steps > 0)", "Total count of discrete conversational turns or tool execution steps in the trace."],
        ["final_outcome", "VARCHAR(32)", "NOT NULL", "Terminal execution status: 'success', 'manifest_failure', 'timeout', or 'exception'."],
        ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "ISO-8601 timestamp recording when the trace log was ingested and parsed."]
    ]
    b.styled_table("Table 3.5: multi_agent_traces Table Schema", t35_headers, t35_rows, col_widths=[1.3, 1.1, 1.4, 2.62])

    # Table 3.6: execution_steps Schema
    t36_headers = ["Field Name", "Data Type", "Constraints", "Semantic Description"]
    t36_rows = [
        ["step_id", "VARCHAR(64)", "PRIMARY KEY, NOT NULL", "Unique identifier for the discrete execution turn (format: trace_id_step_index)."],
        ["trace_id", "VARCHAR(64)", "FOREIGN KEY REFERENCES multi_agent_traces(trace_id)", "Foreign key binding the step to its parent execution trace."],
        ["step_index", "INTEGER", "NOT NULL, CHECK(step_index >= 0)", "Zero-based chronological sequence index of the turn within the trace."],
        ["agent_name", "VARCHAR(64)", "NOT NULL", "Persona identity of the agent generating the action (e.g., Coder, Critic, WebScraper)."],
        ["recipient", "VARCHAR(64)", "NOT NULL", "Target recipient persona or tool receiver (e.g., UserProxy, Executor, PythonInterpreter)."],
        ["action_type", "VARCHAR(64)", "NOT NULL", "Classification of turn action: 'message_send', 'tool_call', 'code_execution', 'reply'."],
        ["action_payload", "TEXT", "NOT NULL", "Raw or bounded natural language message text or tool arguments generated by agent."],
        ["output_state", "TEXT", "NULL", "Observed environment return value, stdout execution logs, or API response payload."],
        ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Timestamp recording step parsing and persistence."]
    ]
    b.styled_table("Table 3.6: execution_steps Table Schema", t36_headers, t36_rows, col_widths=[1.3, 1.1, 1.4, 2.62])

    # Table 3.7: step_evaluations Schema
    t37_headers = ["Field Name", "Data Type", "Constraints", "Semantic Description"]
    t37_rows = [
        ["evaluation_id", "VARCHAR(64)", "PRIMARY KEY, NOT NULL", "Unique UUID identifying the discrete semantic turn evaluation verdict."],
        ["step_id", "VARCHAR(64)", "FOREIGN KEY REFERENCES execution_steps(step_id)", "Foreign key binding the evaluation to the assessed execution step."],
        ["is_valid", "BOOLEAN", "NOT NULL", "Boolean flag indicating whether the step satisfied task constraints without error."],
        ["score", "FLOAT", "NOT NULL, CHECK(score BETWEEN 0.0 AND 1.0)", "Continuous diagnostic validity score assigned by local Qwen2.5:7b (threshold 0.7)."],
        ["anomaly_detected", "BOOLEAN", "NOT NULL", "Binary indicator set to True when score < 0.7 or when explicit failure pattern is matched."],
        ["error_category", "VARCHAR(64)", "NULL", "Fine-grained semantic bug category mapped from 25+ failure taxonomy signatures."],
        ["justification", "TEXT", "NOT NULL", "Detailed natural language reasoning emitted by LLM explaining the assigned step score."],
        ["prompt_hash", "VARCHAR(64)", "NOT NULL, INDEXED", "SHA256 cryptographic hash of canonical prompt text linking to prompt_cache."],
        ["cached", "BOOLEAN", "NOT NULL", "Flag indicating whether evaluation was retrieved from SQLite cache or computed via LLM."],
        ["evaluated_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Timestamp recording when the evaluation verdict was produced."]
    ]
    b.styled_table("Table 3.7: step_evaluations Table Schema", t37_headers, t37_rows, col_widths=[1.3, 1.1, 1.4, 2.62])

    # Table 3.8: dependency_edges Schema
    t38_headers = ["Field Name", "Data Type", "Constraints", "Semantic Description"]
    t38_rows = [
        ["edge_id", "VARCHAR(64)", "PRIMARY KEY, NOT NULL", "Unique UUID identifying the directed graph dependency relationship."],
        ["trace_id", "VARCHAR(64)", "FOREIGN KEY REFERENCES multi_agent_traces(trace_id)", "Foreign key linking edge to the parent execution trace DAG."],
        ["source_step_idx", "INTEGER", "NOT NULL", "Step index of the upstream dependency source node (u)."],
        ["target_step_idx", "INTEGER", "NOT NULL, CHECK(target_step_idx > source_step_idx)", "Step index of downstream dependent node (v) enforcing DAG acyclicity."],
        ["edge_type", "VARCHAR(32)", "NOT NULL", "Relationship type: 'execution_flow' (turn adjacency), 'shared_state' (variable), 'message_reply'."],
        ["confidence", "FLOAT", "NOT NULL, CHECK(confidence BETWEEN 0.0 AND 1.0)", "Calibrated edge reliability weight (0.85 for sequential flow; 0.95 for matched entities)."],
        ["matched_tokens", "TEXT", "NULL", "Comma-separated list of programming identifiers or variable tokens establishing the link."]
    ]
    b.styled_table("Table 3.8: dependency_edges Table Schema", t38_headers, t38_rows, col_widths=[1.3, 1.1, 1.4, 2.62])

    # Table 3.9: prompt_cache Schema
    t39_headers = ["Field Name", "Data Type", "Constraints", "Semantic Description"]
    t39_rows = [
        ["prompt_hash", "VARCHAR(64)", "PRIMARY KEY, NOT NULL", "SHA256 hexadecimal hash computed over normalized prompt text and model identifier."],
        ["model_name", "VARCHAR(64)", "NOT NULL", "Identifier of the language model producing completion (e.g., qwen2.5:7b)."],
        ["prompt_text", "TEXT", "NOT NULL", "Complete canonical prompt text dispatched to the LLM inference daemon."],
        ["response_json", "TEXT", "NOT NULL", "Serialized JSON string containing structured evaluation verdict returned by model."],
        ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Timestamp recording initial cache insertion upon cache miss."],
        ["access_count", "INTEGER", "DEFAULT 1, CHECK(access_count >= 1)", "Telemetry counter tracking cumulative cache hits for cache eviction heuristics."],
        ["last_accessed_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Timestamp of most recent cache hit lookup."]
    ]
    b.styled_table("Table 3.9: prompt_cache Table Schema", t39_headers, t39_rows, col_widths=[1.3, 1.1, 1.4, 2.62])

    # Table 3.10: attribution_verdicts Schema
    t310_headers = ["Field Name", "Data Type", "Constraints", "Semantic Description"]
    t310_rows = [
        ["verdict_id", "VARCHAR(64)", "PRIMARY KEY, NOT NULL", "Unique UUID identifying the diagnostic attribution decision."],
        ["trace_id", "VARCHAR(64)", "FOREIGN KEY REFERENCES multi_agent_traces(trace_id)", "Foreign key binding verdict to evaluated multi-agent trace."],
        ["responsible_agent", "VARCHAR(64)", "NOT NULL", "Persona name of the agent isolated as the true originating root cause (Who)."],
        ["decisive_step_index", "INTEGER", "NOT NULL", "Zero-based step sequence index where the originating corruption began (When)."],
        ["failure_type", "VARCHAR(64)", "NOT NULL", "Classified 2D taxonomy label (e.g., root_cause, propagated_symptom, independent_bug)."],
        ["root_cause_explanation", "TEXT", "NOT NULL", "Multi-tier narrative justifying why upstream parents are clean and how error originated."],
        ["shortest_causal_path", "TEXT", "NOT NULL", "JSON array of step indices representing minimal propagation chain via Dijkstra."],
        ["execution_time_sec", "FLOAT", "NOT NULL", "Total wall-clock runtime in seconds required to complete end-to-end attribution."],
        ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Timestamp recording diagnostic verdict generation."]
    ]
    b.styled_table("Table 3.10: attribution_verdicts Table Schema", t310_headers, t310_rows, col_widths=[1.3, 1.1, 1.4, 2.62])

    # Table 3.11: benchmark_results Schema
    t311_headers = ["Field Name", "Data Type", "Constraints", "Semantic Description"]
    t311_rows = [
        ["benchmark_id", "VARCHAR(64)", "PRIMARY KEY, NOT NULL", "Unique identifier for the benchmark evaluation run."],
        ["dataset_name", "VARCHAR(64)", "NOT NULL", "Evaluated benchmark callset identifier (e.g., WhoAndWhen_ICML2025)."],
        ["total_traces", "INTEGER", "NOT NULL, CHECK(total_traces > 0)", "Total number of multi-agent traces evaluated in benchmark suite (184)."],
        ["agent_accuracy", "FLOAT", "NOT NULL, CHECK(agent_accuracy BETWEEN 0.0 AND 100.0)", "Percentage of traces where responsible agent was correctly identified (Who accuracy)."],
        ["step_accuracy", "FLOAT", "NOT NULL, CHECK(step_accuracy BETWEEN 0.0 AND 100.0)", "Percentage of traces where exact originating step index was isolated (When accuracy)."],
        ["strict_joint_accuracy", "FLOAT", "NOT NULL", "Percentage of traces where BOTH agent and exact step matched ground truth simultaneously."],
        ["avg_latency_sec", "FLOAT", "NOT NULL", "Mean attribution execution latency per trace across benchmark suite."],
        ["total_tokens_used", "INTEGER", "NOT NULL", "Total prompt and completion tokens consumed during benchmark execution."],
        ["executed_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Timestamp recording completion of benchmark evaluation."]
    ]
    b.styled_table("Table 3.11: benchmark_results Table Schema", t311_headers, t311_rows, col_widths=[1.3, 1.1, 1.4, 2.62])

    b.h3("3.3.5 Hardware Requirements")
    b.p("Table 3.3.5.1: Minimum Hardware Requirements", bold=True, size=11, space_before=4, space_after=2)
    tbl_min_hw = doc.add_table(rows=6, cols=2)
    tbl_min_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    min_hw_data = [
        ("Component", "Minimum Requirement"),
        ("Processor", "Quad-Core Intel Core i5 / AMD Ryzen 5 (2.5 GHz or higher)"),
        ("RAM", "8 GB DDR4 System Memory"),
        ("Storage", "10 GB Available SSD Storage (for Python virtual environment & SQLite cache)"),
        ("GPU", "Integrated Graphics (utilizes CPU quantization for Ollama Qwen2.5:7b)"),
        ("Network", "Localhost loopback interface (for REST communication with Ollama daemon)")
    ]
    for r_idx, (c, r) in enumerate(min_hw_data):
        row = tbl_min_hw.rows[r_idx]
        row.cells[0].text = c
        row.cells[1].text = r
        if r_idx == 0:
            set_cell_background(row.cells[0], "E2E8F0")
            set_cell_background(row.cells[1], "E2E8F0")
            row.cells[0].paragraphs[0].runs[0].bold = True
            row.cells[1].paragraphs[0].runs[0].bold = True
        set_cell_margins(row.cells[0], top=20, bottom=20, left=50, right=50)
        set_cell_margins(row.cells[1], top=20, bottom=20, left=50, right=50)

    b.p("", space_after=4)
    b.p("Table 3.3.5.2: Recommended Hardware Requirements", bold=True, size=11, space_before=4, space_after=2)
    tbl_rec_hw = doc.add_table(rows=6, cols=2)
    tbl_rec_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    rec_hw_data = [
        ("Component", "Recommended Requirement"),
        ("Processor", "8-Core Intel Core i7 / AMD Ryzen 7 (3.5 GHz or higher)"),
        ("RAM", "16 GB to 32 GB High-Speed DDR5 Memory"),
        ("Storage", "50 GB NVMe PCIe SSD"),
        ("GPU", "NVIDIA RTX 3060 / 4060 or higher with 8GB+ VRAM (CUDA acceleration for LLM inference)"),
        ("Network", "Broadband internet connection (for initial Qwen2.5:7b model weight download)")
    ]
    for r_idx, (c, r) in enumerate(rec_hw_data):
        row = tbl_rec_hw.rows[r_idx]
        row.cells[0].text = c
        row.cells[1].text = r
        if r_idx == 0:
            set_cell_background(row.cells[0], "E2E8F0")
            set_cell_background(row.cells[1], "E2E8F0")
            row.cells[0].paragraphs[0].runs[0].bold = True
            row.cells[1].paragraphs[0].runs[0].bold = True
        set_cell_margins(row.cells[0], top=20, bottom=20, left=50, right=50)
        set_cell_margins(row.cells[1], top=20, bottom=20, left=50, right=50)

    b.h2("3.4 Architecture and UML Diagrams")
    
    b.h3("3.4.1 Architecture Diagram")
    b.p(
        "The architecture of the Automated Failure Attribution Engine follows the committee-approved modular 5-stage pipeline (established in Review-2). "
        "The system enforces a strict boundary between raw orchestrator log parsing, local neural semantic evaluation, graph dependency "
        "synthesis, backward causal traversal, and presentation layers. Figure 3.1 illustrates the end-to-end data processing pipeline from raw "
        "multi-agent execution traces to the final 2D error taxonomy report."
    )
    b.fig(f"{DIAG_DIR}/fig_3_1_architecture.png", "Figure 3.1: Architecture Diagram (Review-2 Approved Modular Pipeline with Ingestion, StepJudge, Linker & Backward Traversal)")
    b.p(
        "As depicted in Figure 3.1, raw execution traces from AutoGen, LangGraph, or MetaGPT are first ingested by the TraceSegmenter, "
        "which normalizes turns and budgets tokens. Bounded steps are forwarded in parallel to the StepJudge and DependencyLinker. "
        "The StepJudge interacts with the SHA256 cache engine and local Ollama daemon to produce semantic anomaly evaluations, while the "
        "DependencyLinker constructs the NetworkX DiGraph. The Backward Causal Traversal Resolver executes transitive ancestor closure and "
        "topological blame resolution, producing the final AttributionVerdict displayed in the Streamlit UI."
    )
    b.p(
        "The primary architectural breakthrough is the complete decoupling of neural evaluation from causal reasoning. Neural networks excel "
        "at local semantic comprehension—evaluating whether an action payload is valid given its immediate input context. However, neural networks "
        "struggle with global structural reasoning across complex, multi-branching DAGs. Conversely, graph algorithms excel at structural "
        "traversal but cannot evaluate natural language. By assigning local evaluation to the LLM and global causality to NetworkX, our architecture "
        "achieves theoretical determinism and empirical accuracy."
    )

    b.h3("3.4.2 Use Case Diagram")
    b.p(
        "The Use Case Diagram models the core interactions between external actors (AI Engineers, CI/CD Test Pipelines, Local LLMs, "
        "and Cache Stores) and the functional boundaries of the attribution system. Figure 3.2 illustrates these operational relationships."
    )
    b.fig(f"{DIAG_DIR}/fig_3_2_use_case.png", "Figure 3.2: Use Case Diagram for Automated Failure Attribution System")
    b.p(
        "The primary human actor (AI Engineer) initiates trace ingestion, inspects visual DAGs, configures anomaly thresholds, and compares "
        "baseline diagnostics. Automated CI/CD pipelines trigger programmatic attribution via REST API to evaluate regression logs. "
        "Secondary system actors (Ollama LLM and SQLite Cache) service step evaluation prompts and hash lookups."
    )
    b.p(
        "The use cases are structured hierarchically: trace ingestion triggers step segmentation, which in turn invokes prompt cache checks. "
        "A cache miss activates the local LLM inference use case. Once step evaluations are complete, graph construction and backward traversal "
        "use cases execute automatically, concluding with report generation and interactive canvas rendering."
    )

    b.h3("3.4.3 Class Diagram")
    b.p(
        "The Class Diagram represents the object-oriented structure of the diagnostic engine, detailing domain entities, attributes, "
        "type annotations, and method signatures across core modules. Figure 3.3 provides the comprehensive class hierarchy."
    )
    b.fig(f"{DIAG_DIR}/fig_3_3_class.png", "Figure 3.3: Class Diagram of Multi-Agent Failure Attribution System")
    b.p(
        "The domain model is anchored by MultiAgentTrace, composing a collection of ExecutionStep entities. The AttributionEngine orchestrates "
        "singleton instances of TraceSegmenter, StepJudge, DependencyLinker, and BackwardTraversalResolver. The AttributionCache manages "
        "hash computation and SQLite storage, while BackwardTraversalResolver produces the final AttributionVerdict containing NodeStatus lists."
    )
    b.p(
        "Every class adheres to the Single Responsibility Principle. Pydantic's BaseModel serves as the superclass for all data transfer "
        "objects, guaranteeing automatic JSON validation, type coercion, and strict schema compliance across module boundaries."
    )

    b.h3("3.4.4 Sequence Diagram")
    b.p(
        "The Sequence Diagram illustrates the chronological sequence of method invocations and asynchronous message exchanges occurring "
        "during the end-to-end attribution of a failed multi-agent execution trace. Figure 3.4 diagrams this workflow."
    )
    b.fig(f"{DIAG_DIR}/fig_3_4_sequence.png", "Figure 3.4: Sequence Diagram of Multi-Agent Attribution Workflow")
    b.p(
        "The sequence demonstrates how the AttributionEngine coordinates segmentation, queries the StepJudge with cache-first checks, "
        "dispatches prompt requests to Ollama upon cache misses, builds the NetworkX DAG, and invokes the BackwardTraversalResolver "
        "to compute transitive closures and return the final diagnosis to the user interface."
    )
    b.p(
        "A critical sequence optimization is the synchronous cache interrogation: for any prompt hash already residing in SQLite, the StepJudge "
        "returns in less than 2 milliseconds, bypassing the multi-second LLM inference cycle entirely and enabling real-time trace diagnosis."
    )

    b.h3("3.4.5 Data Flow Diagram - Level 0")
    b.p(
        "The Level 0 Data Flow Diagram (Context Diagram) establishes the high-level boundary of the failure attribution platform, "
        "illustrating data flows between external entities and the central attribution engine. Figure 3.5 presents the Level 0 DFD."
    )
    b.fig(f"{DIAG_DIR}/fig_3_5_dfd_lvl0.png", "Figure 3.5: Data Flow Diagram - Level 0 (Context Level)")
    b.p(
        "External frameworks supply raw execution logs; developers provide task goals and configuration queries; the local LLM provides "
        "semantic judgments; the database handles prompt cache records; and the engine outputs verdicts, causal chains, and interactive DAGs."
    )

    b.h3("3.4.6 Data Flow Diagram - Level 1")
    b.p(
        "The Level 1 Data Flow Diagram decomposes the primary system into its six core sub-processes and associated internal data stores. "
        "Figure 3.6 presents the detailed Level 1 processing architecture."
    )
    b.fig(f"{DIAG_DIR}/fig_3_6_dfd_lvl1.png", "Figure 3.6: Data Flow Diagram - Level 1 (Detailed Subsystems)")
    b.p(
        "Process 1.0 (Segmentation) produces bounded steps; Process 2.0 (Step-Wise Judge) interacts with Data Store D1 (Prompt Cache); "
        "Process 3.0 (Dependency Linker) writes to Data Store D2 (DAG Store); Process 4.0 executes backward traversal; Process 5.0 resolves "
        "the 2D taxonomy; and Process 6.0 writes final verdicts to Data Store D3 for display on the interactive dashboard."
    )

    b.h3("3.4.7 Entity Relationship Diagram")
    b.p(
        "The Entity Relationship Diagram specifies the relational database schema, primary/foreign key associations, and cardinalities "
        "governing persistent storage. Figure 3.7 diagrams these relational entities."
    )
    b.fig(f"{DIAG_DIR}/fig_3_7_erd.png", "Figure 3.7: Entity Relationship Diagram for Multi-Agent Failure Attribution Schema")
    b.p(
        "MULTI_AGENT_TRACE maintains 1:N relationships with EXECUTION_STEP and DEPENDENCY_EDGE, and 1:1 relationships with ATTRIBUTION_VERDICT "
        "and GROUND_TRUTH. Each EXECUTION_STEP has a 1:1 relationship with STEP_EVALUATION, which references PROMPT_CACHE via prompt_hash."
    )

    b.h2("3.5 Summary")
    b.p(
        "Chapter 3 established the formal requirements specification for the Automated Failure Attribution Engine. The functional and "
        "non-functional requirements ensure high diagnostic precision, sub-millisecond cache retrieval, and mathematical determinism. "
        "The accompanying architectural, use case, class, sequence, DFD, and ER diagrams provide a multi-faceted structural blueprint "
        "for system implementation. The next chapter details the underlying algorithmic methodology."
    )
    b.page_break()
