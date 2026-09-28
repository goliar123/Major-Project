# 🕵️ Automated Failure Attribution for LLM-Based Multi-Agent Systems

> **Academic Year:** 2026–2027 | **Course:** B. Tech IV Year / I Semester (GR22A4082)
> **Department:** Computer Science & Engineering, Gokaraju Rangaraju Institute of Engineering and Technology (GRIET)
> **Batch No:** D2 | **Guide:** Dr. D. Ushasree (Assistant Professor)
> **Team Members:**
> - Rachapalli S Prabhaadhithya (23241A05Q3)
> - Rathod Ajay (23241A05Q4)
> - Noel Paul (23241A05Q6)
> - Talagapu Niranjan (23241A05R1)

---

## 🗺️ Map of Content (MOC)

This vault contains the complete architectural specification, theoretical foundations, implementation details, evaluation benchmarks, and review documentation for our capstone project.

1. [[01 - Problem Statement & Literature Survey]]
   - Multi-agent debugging challenges, symptom misattribution, long-context degradation, survey of 12 primary papers (2025–2026), and baseline accuracy gaps.
2. [[02 - System Architecture & Design]]
   - End-to-end 5-phase pipeline, Level-0 & Level-1 Data Flow Diagrams (DFD), Process Logic, and Entity-Relationship (ER) schema.
3. [[03 - Core Engine Implementation]]
   - Detailed code walk-throughs of Trace Segmentation, SHA256 Prompt Caching, Dependency Linker (DAG), Backward Causal Traversal, and Baseline Judges.
4. [[04 - Benchmark & Evaluation Results]]
   - Evaluation on the **Who&When** dataset (ICML 2025: 184 traces), comparative accuracy tables (Agent, Step, Strict Joint), and latency/cost analysis.
5. [[05 - API, Async Queue & Dashboard]]
   - FastAPI REST API specification, Celery/Redis asynchronous workers, and Streamlit interactive DAG visualizer.
6. [[06 - Review-2 Presentation & Viva Guide]]
   - Project presentation summary, viva Q&A, demo scripts, and faculty review preparation.
7. [[07 - Theoretical Concepts & Core Mechanisms]]
   - Exhaustive mathematical and algorithmic guide to Graph Building, Backward Traversal, Typed Connections, Semantic Anomaly Detection, and System Hardening.
8. [[08 - Beginner Friendly Prerequisite & Concepts Guide]]
   - Beginner-friendly first-principles guide covering AI Agents, DAGs, Cascading Failures, and Caching with intuitive analogies.
9. [[09 - Dataset Sources & Benchmark Guide]]
   - Guide to public research datasets (Who&When, MAST, TracerTraj) and scripts to export traces from AutoGen, CrewAI, and LangGraph.
10. [[10 - Why Enterprise MNCs Fail at Multi-Agent Debugging]]
   - Deep dive into why Big Tech and MNCs struggle with multi-agent debugging, monolithic prompt traps, flat vs graph logging, and silent semantic drift.
11. [[11 - Post-Hoc Attribution vs AGI & Neuro-Symbolic AI]]
   - Distinguishing post-hoc diagnostic observability from in-situ generative AGI reasoning, Process Reward Models (PRMs), and the future of self-correcting AI.
12. [[12 - Exhaustive Analysis of All 12 Research Papers (2025-2026)]]
   - Complete breakdown of all 12 primary literature papers (Zhang 2025, MAST, AgenTracer, TRAIL, CHIEF, FALAT, AgentDebugX, etc.), their methodologies, accuracy limits, and failure modes.
13. [[13 - Deep Analysis of Survey Papers & Why Root Cause Attribution is Intractably Hard]]
   - In-depth research synthesis on the Universal Autonomous Attribution problem, emergent social entanglement, silent semantic drift, and the neuro-symbolic breakthrough.
14. [[14 - Real-World Impact, Industry Utility & Viva Defense]]
   - Comprehensive guide on academic scoring criteria, enterprise utility (Sentry for AI), resume talking points, and the 30-second viva pitch.
15. [[15 - The Neuro-Symbolic Reality - Heuristics vs LLMs in Causal Attribution]]
   - The boundary between Graph Theory and LLM semantics: why heuristics work on explicit benchmarks, where regex collapses, and why neuro-symbolic fusion is the true solution.
16. [[16 - Commercialization Blueprint & Enterprise Exit Strategy]]
   - How to turn this into a venture-funded startup or acquisition target for Google, Microsoft, OpenAI, or Datadog.
17. [[17 - The Market Maturity Curve & Enterprise Product Scope]]
   - Why this wasn't built years ago, why companies currently rely on brute-force retries, and the enterprise scope needed for multi-million dollar ARR (time-travel self-healing).
18. [[18 - Detailed Dependency Graph Architecture & Specifications]]
   - Mathematical graph formalisms, Node/Edge schema, NetworkX backward traversal algorithms, and interactive Pyvis visualization.
19. [[19 - Embedding HTML, CSS & Custom Diagrams in Obsidian]]
   - Complete guide on native HTML5/CSS3 cards, pure inline SVG diagrams, Mermaid contrast fixes, and `<iframe>` interactive Pyvis embeds in Obsidian.
20. [[20 - Dedicated CLI Tool Reference & Command Guide]]
   - Terminal-first command suite (`diagnose`, `watch`, `benchmark`, `cache`, `test-llm`, `serve`), flags, outputs, and Pyvis HTML export.

---

## ⚡ Executive Summary

When complex LLM-based multi-agent systems (AutoGen, ChatDev, MetaGPT) fail, developers are forced to manually inspect hundreds of turns of dialogue and tool logs. Published LLM-as-a-judge approaches achieve only **53.5% agent-level** and **14.2% step-level accuracy** because they evaluate steps in isolation and blame downstream **symptoms** rather than the originating **root cause**.

Our solution delivers an automated, lightweight developer toolkit that:
1. **Segments traces** into bounded turns to prevent context window explosion on long traces (>32k tokens).
2. **Caches semantic evaluations** using SHA256 prompt hashing to ensure zero redundant GPU/API expense.
3. **Constructs an Information-Dependency DAG** mapping variable flow and message exchange across agents.
4. **Executes Backward Causal Traversal** from the manifest failure to isolate the earliest invalid step whose upstream dependencies were valid.
5. **Presents results** in an interactive **Streamlit Dashboard**, high-performance **FastAPI REST API**, and a dedicated **Rich CLI Terminal Tool**.

<div style="background: #181825; border: 1px solid #313244; border-radius: 12px; padding: 20px; margin: 18px 0; color: #cdd6f4; font-family: sans-serif;">
  <div style="font-weight: bold; font-size: 1.05em; color: #89b4fa; margin-bottom: 12px; text-align: center;">⚡ Automated End-to-End Failure Attribution Pipeline</div>
  <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 8px;">
    <div style="flex: 1 1 140px; background: #1e1e2e; border: 1.5px solid #f38ba8; border-radius: 8px; padding: 12px; text-align: center;">
      <div style="font-size: 0.75em; font-weight: 800; color: #f38ba8; text-transform: uppercase;">Input</div>
      <div style="font-weight: 700; font-size: 0.9em; color: #ffffff; margin-top: 4px;">Failed Trace Log</div>
    </div>
    <div style="color: #89b4fa; font-size: 1.3em; font-weight: bold;">➔</div>
    <div style="flex: 1 1 140px; background: #1e1e2e; border: 1.5px solid #89b4fa; border-radius: 8px; padding: 12px; text-align: center;">
      <div style="font-size: 0.75em; font-weight: 800; color: #89b4fa; text-transform: uppercase;">Phase 1</div>
      <div style="font-weight: 700; font-size: 0.9em; color: #ffffff; margin-top: 4px;">Segmentation</div>
    </div>
    <div style="color: #89b4fa; font-size: 1.3em; font-weight: bold;">➔</div>
    <div style="flex: 1 1 140px; background: #1e1e2e; border: 1.5px solid #a6e3a1; border-radius: 8px; padding: 12px; text-align: center;">
      <div style="font-size: 0.75em; font-weight: 800; color: #a6e3a1; text-transform: uppercase;">Phase 2</div>
      <div style="font-weight: 700; font-size: 0.9em; color: #ffffff; margin-top: 4px;">SHA256 Judge Cache</div>
    </div>
    <div style="color: #89b4fa; font-size: 1.3em; font-weight: bold;">➔</div>
    <div style="flex: 1 1 140px; background: #1e1e2e; border: 1.5px solid #fab387; border-radius: 8px; padding: 12px; text-align: center;">
      <div style="font-size: 0.75em; font-weight: 800; color: #fab387; text-transform: uppercase;">Phase 4</div>
      <div style="font-weight: 700; font-size: 0.9em; color: #ffffff; margin-top: 4px;">Backward Traversal</div>
    </div>
    <div style="color: #89b4fa; font-size: 1.3em; font-weight: bold;">➔</div>
    <div style="flex: 1 1 140px; background: #1e1e2e; border: 1.5px solid #94e2d5; border-radius: 8px; padding: 12px; text-align: center;">
      <div style="font-size: 0.75em; font-weight: 800; color: #94e2d5; text-transform: uppercase;">Verdict</div>
      <div style="font-weight: 700; font-size: 0.9em; color: #ffffff; margin-top: 4px;">Root Cause Isolated</div>
    </div>
  </div>
</div>

---

## 🏷️ Tags
#LLM #MultiAgentSystems #RootCauseAnalysis #CausalDAG #Benchmark #WhoAndWhen #FastAPI #Streamlit #CLI #CapstoneProject #GRIET #ResearchSurvey #Startup #Commercialization #Obsidian
