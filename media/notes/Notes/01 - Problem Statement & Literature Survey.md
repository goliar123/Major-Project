# 📚 01 - Problem Statement & Literature Survey

## 🎯 1. Problem Statement

Multi-agent architectures (e.g., AutoGen, ChatDev, MetaGPT) employ multiple specialized LLM agents collaborating through conversational turns, tool executions, and shared environments to solve complex software engineering, research, and analytics tasks. 

However, when a multi-agent system produces an incorrect final answer or crashes during execution:
- **Manual Debugging Bottleneck**: Interaction traces routinely reach dozens or hundreds of conversational turns and tens of thousands of tokens. Developers must manually read every single prompt and tool execution to find where the process went off track.
- **Cascading Error Propagation**: In multi-agent collaboration, an error made by an early upstream agent (e.g., generating an invalid SQL query, hallucinating a schema, or misconfiguring a function parameter) is passed to subsequent downstream agents. The downstream agents attempt to use this corrupted data, eventually triggering an exception, an assertion failure, or an empty output in the final steps.
- **Symptom Misattribution**: Existing automated LLM-as-a-judge frameworks analyze steps in isolation or evaluate the whole trace in a single monolithic prompt. They consistently blame the downstream agent (the **symptom** step, such as a tester or summarizer) rather than the originating agent that corrupted the state (the **root cause** step).

---

## 🔍 2. Identified Research Gaps

```
+---------------------------------------------------------------------------------------+
| SOTA ACCURACY GAP IN PUBLISHED LITERATURE (2025–2026)                                  |
|                                                                                       |
|   53.5%                     14.2%                             <30.0%                  |
|   Agent-Level Accuracy      Step-Level Accuracy               Strict Joint Accuracy   |
|   (Zhang et al., ICML 2025) (Barely above random chance)      (Top 2026 Frameworks)   |
+---------------------------------------------------------------------------------------+
```

1. **Step Localization Remains Effectively Unsolved**:
   While predicting *which* agent made a mistake reaches ~53.5%, pinpointing the *exact decisive turn/step* collapses to **14.2%** (near random chance).
2. **Symptoms Mistaken for Root Causes**:
   Most approaches lack explicit data-flow dependency tracking, so an agent that crashes because of corrupted upstream inputs is falsely penalized.
3. **Long-Context Degradation & Token Window Limits**:
   12.1% of complex benchmark traces exceed 32k tokens outright, leading to truncation and "lost-in-the-middle" attention degradation when evaluated in a single prompt.
4. **Impractical Compute & Budget Demands**:
   Existing high-accuracy proposals (e.g., AgenTracer) rely on live environment counterfactual replays or reinforcement learning fine-tuning, requiring massive GPU budgets.
5. **Absence of Practical Developer Tooling**:
   Most prior work is published purely as academic benchmarks without delivering an interactive, inspectable tool developers can use in real-world workflows.

---

## 📖 3. Literature Survey Matrix (12 Primary Papers: 2025–2026)

| S.No | Paper Title & Year | Authors | Key Methodology & Metrics | Datasets Used | Observed Shortcomings & Gaps |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems** (ICML 2025 Spotlight) | S. Zhang, M. Yin, J. Zhang et al. | Evaluated All-at-Once, Step-by-Step, and Binary Search LLM judges. Best result: **53.5% agent-level, 14.2% step-level accuracy**. | Who&When (127 failure logs on GAIA and AssistantBench) | Step accuracy barely above chance. Monolithic prompt cannot fit long traces; isolated evaluation blames symptoms. |
| **2** | **Why Do Multi-Agent LLM Systems Fail? (MAST)** (NeurIPS 2025) | M. Cemri, M. Z. Pan, S. Yang et al. | First empirical taxonomy: 14 failure modes in 3 categories with LLM annotation pipeline ($\kappa = 0.88$). | MAST-Data (1,600+ traces across 7 MAS frameworks) | Explains *why* systems fail but does not localize *which* agent or step caused it. No step-level metric. |
| **3** | **Where LLM Agents Fail and How They Can Learn From Failures (AgentDebug)** (2025) | K. Zhu, Z. Liu, B. Li et al. | Categorizes memory, reflection, planning, action errors; feeds corrections into re-rollouts (+24% all-correct). | AgentErrorBench (ALFWorld, GAIA, WebShop) | Focuses on single-agent trajectories, not multi-agent collaboration. Requires live environment re-execution. |
| **4** | **AgenTracer: Who Is Inducing Failure in the LLM Agentic Systems?** (2025) | G. Zhang, J. Wang, J. Chen et al. | Counterfactual replay + programmatic fault injection to train AgenTracer-8B via multi-granular RL. | TracerTraj (2.5K trajectories), Who&When | Requires active trajectory re-execution and heavy GPU training budget. |
| **5** | **TRAIL: Trace Reasoning and Agentic Issue Localization** (2025) | A. Deshpande et al. | Taxonomy covering reasoning, planning, and execution errors with localization inside long traces. | TRAIL traces from GAIA & SWE-Bench | Traces routinely exceed context limits; fails to distinguish originating vs inherited errors. |
| **6** | **Where Did It All Go Wrong? A Hierarchical Look into Multi-Agent Error Attribution** (2025) | A. Banerjee, A. Nair, T. Borogovac | Coarse-to-fine attribution: narrows trace to suspect region, then isolates a step. | Who&When | Improvement limited to agent level; step accuracy remains weak because hierarchy is purely temporal, not dependency-based. |
| **7** | **AgentDiagnose: An Open Toolkit for Diagnosing LLM Agent Trajectories** (EMNLP 2025) | T. Ou, W. Guo, A. Gandhi et al. | Scores trajectories across interpretable quality dimensions to curate training data. | Agent trajectories across public benchmarks | Diagnostic scores only; does not output a responsible agent or decisive step. |
| **8** | **Automatic Failure Attribution and Critical Step Prediction via Causal Inference** (2025) | Y. Ma et al. | Pairs Shapley-value credit assignment with causal discovery over static logs. | Who&When | Static logs without intervention; Shapley computation cost scales exponentially with trace length. |
| **9** | **GraphTracer: Graph-Guided Failure Tracing in LLM Agents** (2025) | H. Zhang, Y. Shi, X. Gu et al. | Information Dependency Graphs capturing output reuse; GraphTracer-8B. | Who&When, TracerTraj | Withdrawn by authors due to methodological calculation error. |
| **10** | **From Flat Logs to Causal Graphs: Hierarchical Failure Attribution for LLM-based MAS (CHIEF)** (2026) | Y. Wang, W. Wu, J. Wang, Q. Wang | Hierarchical causal graphs, oracle-guided backtracking, progressive counterfactual screening. | Who&When (127 MAS architectures) | Relies heavily on synthesized virtual oracles and massive repeated LLM calls; latency and inference costs are unbudgeted. |
| **11** | **FALAT: Tracing Failures in LLM Agent Trajectories via Dependency-Guided Search** (2026) | M. N. Rafi, M. Ahasanuzzaman et al. | Four stages: task-conditioned prior, pruning by typed dependencies, guided search with verification. | Who&When | Multi-stage search multiplies LLM calls per trace; prohibitive cost for low-resource or open-weight models. |
| **12** | **AgentDebugX: Failure Observability, Attribution and Recovery in LLM Agents** (2026) | K. Zhu et al. | Closed loop: Detect-Attribute-Recover-Rerun with DeepDebug (28.8% exact joint accuracy on 9B backbone). | Who&When; heterogeneous runtimes | Strict joint accuracy still below 30%; infrastructure-heavy runtime requirements. |

---

## 💡 4. Proposed Solution Comparison

| Challenge Area | Existing Frameworks | Our Implemented Approach |
| :--- | :--- | :--- |
| **Context Window Limits** | Dumps entire multi-agent trace into one prompt; fails on logs > 32k tokens. | **Segments traces** into discrete bounded turns (≤4k tokens) so arbitrarily long logs remain fully analyzable. |
| **Symptom Misattribution** | Evaluates steps in isolation; blames downstream steps that merely inherited corrupted data. | **Information Dependency DAG & Backward Causal Traversal**: Backtracks along data flow to isolate the earliest corrupted node whose parents were valid. |
| **Compute & Cost** | Demands expensive RL fine-tuning, live environment re-execution, or proprietary APIs. | **Deterministic SHA256 Prompt Caching**: Open-weight models (Qwen2.5-7B) with ~65% cache reuse to stay within free GPU quotas. |
| **Practical Tooling** | Academic benchmark scripts only; no usable developer UI. | **Interactive Streamlit Developer Dashboard & FastAPI REST Backend** with live visual DAG graph inspection. |

---

## 🔗 Related Notes
- [[00 - Project Overview & Index]]
- [[02 - System Architecture & Design]]
- [[04 - Benchmark & Evaluation Results]]
