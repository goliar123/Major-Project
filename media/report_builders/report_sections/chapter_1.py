"""
Chapter 1: Introduction module for Major Project Phase-I Report (B12 Format).
"""
def add_chapter_1(b):
    b.h1("CHAPTER 1: INTRODUCTION")

    b.h2("1.1 Background: The Rise of Autonomous Multi-Agent Systems")
    b.p(
        "The historical progression of artificial intelligence research over the past decade has transitioned through multiple distinct "
        "epochs: from supervised discriminative deep learning and convolutional neural networks, to transformer-based foundational self-attention "
        "architectures, and most recently, to autonomous agentic intelligence. Early deployments of generative Large Language Models (LLMs)—typified "
        "by OpenAI's GPT-3 and early versions of ChatGPT—operated primarily as stateless, single-turn query-response systems. While effective for "
        "isolated text summarization, language translation, and zero-shot question answering, single-turn language models exhibit severe cognitive "
        "and architectural ceilings when tasked with solving long-horizon, multi-objective engineering challenges. Monolithic models suffer from "
        "bounded context windows, cumulative attentional drift, a lack of self-correction capabilities, and the inability to maintain persistent "
        "computational state across iterative problem-solving cycles."
    )
    b.p(
        "To surmount these fundamental constraints, the artificial intelligence research community pioneered multi-agent orchestration frameworks. "
        "The foundational philosophy of multi-agent systems (MAS) draws directly upon organizational psychology, distributed systems theory, and "
        "classical software engineering principles: complex, high-entropy objectives are best accomplished through division of labor, role "
        "specialization, and collaborative peer review. Frameworks such as Microsoft AutoGen, LangGraph, CrewAI, MetaGPT, and ChatDev operationalized "
        "this philosophy by enabling developers to configure specialized societies of autonomous agents. In these collaborative networks, each agent "
        "is initialized with an individualized system persona, operational objectives, memory buffers, and tool capabilities."
    )
    b.p(
        "For example, in an autonomous software development collective, a multi-agent system instantiates a Planner agent to decompose high-level "
        "user specifications into modular architecture design documents; a Software Engineer agent to author Python implementation scripts; a "
        "Code Reviewer agent to perform static analysis, check edge cases, and enforce security policies; a Sandboxed Executor agent to invoke compilers "
        "and execute unit test suites within isolated Docker containers; and a Quality Assurance (QA) monitor to benchmark runtime metrics against "
        "formal service level agreements. Through iterative conversational message passing, agents debate design alternatives, critique each other's "
        "intermediate drafts, execute diagnostic tools, and refine outputs until consensus is achieved. This cooperative paradigm has unlocked "
        "extraordinary autonomous capabilities across diverse enterprise domains, including automated financial portfolio risk auditing, multi-modal "
        "clinical triage workflows, autonomous penetration testing, and scientific literature data mining."
    )

    b.h2("1.2 The Failure Attribution Challenge in Agentic Systems")
    b.p(
        "Despite their unprecedented collaborative power, multi-agent orchestrations exhibit extreme operational fragility. As multi-agent "
        "networks expand in execution depth, node cardinality, and tool-invocation complexity, diagnosing and debugging orchestration failures "
        "becomes an exponentially challenging forensic endeavor. Multi-agent execution traces are characterized by non-deterministic state "
        "transitions, probabilistic reasoning drifts, and multi-step cascading dependencies that fundamentally defy conventional software debugging "
        "methodologies."
    )
    b.p(
        "In traditional distributed software systems—such as microservice architectures running on Kubernetes—inter-component communication is "
        "strictly regulated by deterministic interface contracts, strongly typed protocol buffers (gRPC), OpenAPI schemas, and HTTP status codes. "
        "If a specific microservice encounters an unhandled null pointer or database timeout, it emits an explicit, typed exception accompanied "
        "by a deterministic call stack trace. Distributed tracing telemetry frameworks, such as OpenTelemetry or Jaeger, propagate correlation "
        "IDs across service boundaries, enabling software engineers to inspect the exact RPC span where the defect occurred. In sharp contrast, "
        "communicative LLM agents interact primarily through natural language dialogue or loosely structured JSON text payloads. Semantic errors—such "
        "as an unstated assumption, an incorrect arithmetic calculation, an invalid parameter value, or an ungrounded hallucination—do not trigger "
        "immediate runtime exceptions. Instead, corrupted state is seamlessly packaged into plausible-sounding natural language and propagated "
        "downstream into the input context of subsequent agents."
    )
    b.p(
        "Consequently, an error introduced at an early conversational turn travels silently through the multi-agent collective. Downstream agents, "
        "lacking ground-truth verification mechanisms, consume the corrupted context as legitimate ground truth, incorporating the flawed premise "
        "into their own reasoning cycles. By the time the orchestration collapses—often dozens of conversational turns and thousands of generated "
        "tokens later—the terminal crash manifests at an agent that had absolutely no role in originating the defect. Diagnosing such failure cascades "
        "requires unraveling a complex web of semantic interactions, where the visible symptom and the originating root cause are separated by "
        "vast temporal and conversational distances."
    )

    b.h2("1.3 The Pathology of Symptom Misattribution")
    b.p(
        "We identify and formally define this critical diagnostic pathology as 'Symptom Misattribution'. Symptom Misattribution is the error of "
        "attributing the root cause of a multi-agent orchestration failure to the downstream agent where the failure visibly manifested, rather than "
        "to the upstream agent that initially introduced the corrupt state or violated task constraints."
    )
    b.p(
        "To concretely illustrate the mechanics and consequences of Symptom Misattribution, consider an enterprise financial analysis orchestration "
        "comprising six specialized agents tasked with processing corporate filings and computing valuation metrics:\n\n"
        "• Step 0 (Planner Agent): Decomposes the financial audit goal into data scraping, ratio computation, risk analysis, and schema validation subtasks.\n"
        "• Step 1 (Search Agent): Fetches quarterly balance sheets and income statements from SEC EDGAR filings.\n"
        "• Step 2 (Writer Agent - Root Cause): Formats the financial data table. However, due to an unhandled regular expression edge case, the Writer agent inadvertently replaces the operating margin float value of Vantage Tech with 'NaN' (Not a Number).\n"
        "• Step 3 (Computation Worker - Propagated Symptom): Ingests the corrupted table. It calculates portfolio risk metrics, carrying forward the 'NaN' operating margin without throwing an error because Python's math library permits float('nan') propagation.\n"
        "• Step 4 (Risk Auditor - Propagated Symptom): Generates executive commentary. It observes the missing metric and notes in narrative text that Vantage Tech requires further review, approving the text tone.\n"
        "• Step 5 (Database Architect - Manifest Symptom): Executes an insertion script to persist the final structured report into a PostgreSQL data warehouse via a strict Pydantic model. The Pydantic schema validator encounters the 'NaN' field and throws a fatal runtime exception: 'ValidationError: operating_margin cannot be NaN; float constraint violated'."
    )
    b.p(
        "When this trace is reviewed by a conventional monitoring tool or a software engineer using traditional stack trace inspection, the entire "
        "diagnostic focus immediately fixes upon Step 5 (Database Architect). The stack trace points exclusively to the Database Architect's "
        "Pydantic validation line. In response, a naive developer would spend hours modifying Step 5's schema validation logic—perhaps attempting "
        "to coerce NaNs to zeros or relax database constraints—completely failing to address the true bug at Step 2 where the Writer agent corrupted "
        "the raw tabular data. Symptom Misattribution leads to incorrect bug fixes, degraded code quality, wasted developer productivity, and persistent "
        "vulnerabilities in production autonomous workflows."
    )

    b.h2("1.4 Limitations of Existing Diagnostic Approaches")
    b.p(
        "Existing automated approaches for evaluating and debugging multi-agent systems suffer from fatal structural limitations that render them "
        "incapable of solving Symptom Misattribution:\n\n"
        "1. Monolithic LLM-as-a-Judge (All-at-Once Evaluation): The prevailing baseline in the academic literature involves aggregating the entire "
        "conversational history of a multi-agent trace—often exceeding 15,000 to 30,000 tokens—into a single massive prompt and asking an advanced LLM "
        "(such as GPT-4 or Claude 3.5) to identify the responsible agent and decisive step index. Multiple recent studies (Arawjo et al., 2024; Zheng et al., "
        "2023) have revealed that monolithic evaluators suffer from severe cognitive failure modes. Language models exhibit pronounced 'Lost in the "
        "Middle' attention degradation and extreme recency bias: because the final exception stack trace appears at the very end of the prompt context, "
        "the model's self-attention mechanism disproportionately focuses on the terminal crashing turn. Monolithic judges overwhelmingly assign blame to "
        "the terminal agent, achieving a step-level attribution accuracy of only ~14.2% on standardized benchmarks.\n\n"
        "2. Isolated Step-by-Step Evaluation: An alternative heuristic evaluates each execution turn independently in isolation, assessing whether the step "
        "satisfies local constraints. While this eliminates context window saturation, it introduces a complementary failure mode: it cannot model "
        "information propagation across steps. When an isolated evaluator inspects Step 3 or Step 4 in the earlier financial example, it observes that the "
        "agent acted on 'NaN' inputs and produced an anomalous output, thus flagging every intermediate step as anomalous. Lacking a causal graph, the "
        "isolated evaluator typically defaults to blaming the final anomalous step encountered, achieving only ~35.6% step-level accuracy.\n\n"
        "3. Binary Search Trace Bisection: Some testing frameworks attempt to locate the failure turn using binary search across step indices. However, "
        "binary search relies on the fundamental mathematical assumption of monotonicity: that if step k is faulty, all steps after k are faulty, and "
        "all steps before k are valid. In real-world multi-agent systems, failure patterns are frequently non-monotonic. An agent may commit an error, a "
        "subsequent agent may partially recover or mask the error, and a third agent may introduce an independent second bug. Binary search breaks down "
        "completely in the presence of compound, multi-culprit fault scenarios, achieving only ~41.7% step-level accuracy."
    )

    b.h2("1.5 Proposed Solution: A Neuro-Symbolic Causal Graph Engine")
    b.p(
        "To overcome the fatal limitations of existing methods, this project proposes a novel Neuro-Symbolic Causal Graph Engine that enforces a "
        "principled separation between semantic natural language comprehension and causal structural reasoning. The foundational insight of our "
        "approach is that neural networks and symbolic graph algorithms possess complementary strengths:\n\n"
        "• The Neural Component (Local LLM StepJudge): Large Language Models excel at localized semantic reasoning. Given a single execution turn, its "
        "immediate input context, and the task goal, an LLM can accurately determine whether the agent's action was logically sound, whether it respected "
        "domain constraints, or whether it introduced a factual, mathematical, or procedural error. By evaluating steps individually rather than "
        "monolithically, the LLM operates within a clean, bounded context window (<= 4,096 tokens), completely immune to recency bias.\n\n"
        "• The Symbolic Component (Deterministic Causal Graph Traversal): Graph algorithms excel at global structural reasoning. Once steps are "
        "evaluated and dependencies are mapped into a Directed Acyclic Graph (DAG) using NetworkX, the engine applies mathematically rigorous graph "
        "traversals. By computing the Transitive Ancestor Closure from the manifest failure symptom, sorting anomalous ancestors topologically, and "
        "identifying the earliest anomaly whose immediate parents are completely valid, the symbolic engine deterministically isolates the originating "
        "root cause without relying on probabilistic LLM guessing."
    )
    b.p(
        "To ensure industrial viability, the system integrates a deterministic SHA256 prompt hashing cache. Because step evaluation prompts are "
        "canonicalized, identical execution steps evaluated across debugging iterations achieve 100% cache hit rates, reducing diagnostic latency from "
        "seconds to sub-milliseconds and slashing GPU compute costs. A 25-pattern heuristic MockJudge provides zero-downtime offline fallback, ensuring "
        "the diagnostic pipeline remains operational even during local model downtime."
    )

    b.h2("1.6 Key Objectives of the Project")
    b.p(
        "The primary objectives of this Phase-I Major Project are formulated as follows:\n\n"
        "1. Multi-Format Trace Parsing & Segmentation: Build an extensible trace ingestion engine supporting structured JSON/JSONL schemas (AutoGen, "
        "LangGraph, CrewAI, MetaGPT) and unstructured console logs, with an intelligent token budgeting mechanism that preserves critical head instructions "
        "and tail exception traces.\n"
        "2. Deterministic Inference Caching: Develop a cryptographic SHA256 prompt hashing engine with multi-tier storage (in-memory dictionary and "
        "persistent SQLite database) to eliminate redundant LLM calls and achieve sub-millisecond cache retrieval.\n"
        "3. Localized Semantic Step Evaluation: Deploy a locally hosted Qwen2.5:7b model via Ollama in structured JSON mode to evaluate turn-level validity, "
        "accompanied by an offline MockJudge heuristic evaluator with 25+ failure signature patterns.\n"
        "4. Dependency DAG Synthesis: Implement an information dependency linker that models sequential execution flow (confidence 0.85) and extracts "
        "programming identifiers via regex to capture long-range shared state mutations (confidence 0.95) within a NetworkX DiGraph.\n"
        "5. Two-Phase Backward Causal Traversal: Formulate and implement graph algorithms computing the Transitive Ancestor Closure and topological blame "
        "resolution to isolate the true Originating Root Cause.\n"
        "6. 2D Error Taxonomy Classification: Establish a comprehensive taxonomy classifying nodes along Causal Role (Root Cause, Propagated Symptom, "
        "Independent Bug, Recovery Failure) and Semantic Bug Category (25+ types).\n"
        "7. Rigorous Empirical Benchmarking: Benchmark the engine against the complete 184-trace ICML 2025 Who&When dataset, quantitatively evaluating "
        "Agent-level, Step-level, and Strict Joint accuracy against All-at-Once, Step-by-Step, and Binary Search baselines.\n"
        "8. Interactive Diagnostic Presentation: Deliver a production-grade Streamlit dashboard featuring color-coded DAG rendering, step inspection, "
        "and REST API endpoints for seamless automated CI/CD pipeline integration."
    )

    b.h2("1.7 Organization of the Report")
    b.p(
        "The remainder of this report is organized as follows:\n"
        "• Chapter 2 (Literature Survey): Reviews communicative multi-agent frameworks, causal graph modeling, LLM-as-a-judge methodologies, standardized "
        "failure benchmarks, research gaps, formal problem definitions, and the proposed solution.\n"
        "• Chapter 3 (System Requirements Specification): Provides the complete functional requirements (FR-01 to FR-15), non-functional requirements "
        "(NFR-01 to NFR-12), user interface specifications, database schemas, hardware tables, and seven detailed UML and architectural diagrams.\n"
        "• Chapter 4 (Methodology): Details the 12 functional modules, the 15-step execution methodology, technical principles, and implementation progress.\n"
        "• Chapter 5 (Conclusion and Future Scope): Synthesizes key project findings, architectural contributions, and outlines 14 future research directions.\n"
        "• Chapter 6 (References): Documents academic and technical citations."
    )
    b.page_break()
