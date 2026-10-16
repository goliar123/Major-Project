# 🎓 06 - Review-2 Presentation & Viva Guide

## 📋 1. Project Information Card

- **Title:** Automated Failure Attribution for LLM-Based Multi-Agent Systems
- **Academic Year:** 2026–2027 | **Semester:** B. Tech IV Year / I Sem (GR22A4082)
- **Batch No:** D2 | **Department:** Computer Science and Engineering, GRIET
- **Guide:** Dr. D. Ushasree, Assistant Professor
- **Team Members:**
  - Rachapalli S Prabhaadhithya (23241A05Q3)
  - Rathod Ajay (23241A05Q4)
  - Noel Paul (23241A05Q6)
  - Talagapu Niranjan (23241A05R1)

---

## 🏆 2. Review-2 Objectives & Status

| Milestone / Task | Review-2 Status | Deliverables & Status Details |
| :--- | :---: | :--- |
| **Problem Formulation & Scoping** | ✅ Completed | Defined benchmark evaluation criteria, metrics, and low-resource constraints. |
| **Literature Review & Gap Analysis** | ✅ Completed | 12 primary papers (2025–2026) surveyed and comparative matrix established. |
| **Dataset Ingestion & Harness** | ✅ Completed | 184 Who&When failure logs (58 Hand-Crafted + 126 Algorithm-Generated) loaded. |
| **Baseline Replication (Stage 1)** | ✅ Completed | Re-implemented All-at-Once, Step-by-Step, and Binary Search baselines. |
| **Step-Wise Judging & Caching (Stage 2)** | ✅ Completed | Turn segmentation implemented; SHA256 prompt hashing cache active with SQLite/Redis/Mongo. |
| **Dependency-Aware Engine (Stage 3)** | ✅ Completed | Data-flow DAG construction and backward causal traversal resolver verified. |
| **FastAPI Backend & Streamlit UI (Stage 4)**| ✅ Completed | REST API server, Celery/Redis queue, and interactive color-coded DAG dashboard deployed. |

---

## 🎤 3. Viva Questions & Expert Answers

### Q1: Why do standard LLM-as-a-judge approaches fail at step-level localization (14.2% accuracy)?
> **Answer**: Standard LLM-as-a-judge baselines evaluate steps either in isolation or in a single monolithic prompt. In multi-agent systems, errors cascade: when an upstream agent (e.g. DatabaseArchitect) introduces flawed data (e.g. `DROP TABLE`), downstream agents (e.g. Coder, QA Tester) inherit that flawed state and crash. Monolithic or isolated judges suffer from *recency bias* and *symptom misattribution*, incorrectly blaming the downstream tester where the crash manifested rather than the originating architect step.

### Q2: How does your Backward Causal Traversal algorithm solve symptom misattribution?
> **Answer**: Our algorithm first constructs a Directed Acyclic Graph (DAG) mapping data flow, variable passing, and message communication between agent steps. When a manifest failure symptom occurs at step $s_{\text{manifest}}$, our engine traverses backwards along the DAG ancestor subgraph. For every candidate anomaly, it inspects its upstream parents. The earliest anomalous step whose parent dependencies were completely valid is isolated as the **True Root Cause**, while downstream anomalies are classified as **Propagated Symptoms**.

### Q3: How do you handle long execution traces exceeding 32k tokens?
> **Answer**: 12.1% of complex benchmark traces exceed 32k tokens, causing context-window truncation in monolithic approaches. Our engine implements **turn-level segmentation**: each step is bounded to $\le 4096$ tokens and evaluated independently against the immediate context and task goal. Because dependencies are modeled via graph edges rather than a massive prompt, traces of arbitrary turn length can be analyzed without context degradation.

### Q4: How does deterministic prompt caching ensure zero-cost repeated evaluation?
> **Answer**: Every step evaluation prompt is hashed using SHA256 ($\text{SHA256}(\text{Model} \parallel \text{Prompt})$) and stored in our cache database (SQLite/Redis/MongoDB). When benchmark suites or recurring traces are re-evaluated, cached scores and justifications are retrieved in $<1$ ms with zero LLM inference calls, achieving a 100% cache hit rate and conserving GPU/API quotas.

### Q5: What dataset did you use to evaluate your system?
> **Answer**: We evaluated our system on the **Who&When benchmark** (ICML 2025), comprising 184 human-verified failure traces (58 complex Hand-Crafted traces and 126 Algorithm-Generated traces) across AutoGen, ChatDev, and MetaGPT architectures.

---

## 🎬 4. Live Demo Walkthrough Steps for Presentation

1. **Start the Dashboard**:
   ```bash
   streamlit run dashboard/app.py
   ```
2. **Step 1 — Show Trace Debugger & DAG**:
   - Select trace `WW-HC-001` (*E-Commerce Database Migration Failure*).
   - Point out that `DatabaseArchitect` issued a destructive `DROP TABLE` in Step 1, while `QATester` crashed in Step 4.
   - Click **Run Root-Cause Diagnosis**.
   - Show the interactive DAG:
     - Step 1 is highlighted in **🔴 Red (Root Cause)**.
     - Step 4 is highlighted in **🟠 Orange (Propagated Symptom)**.
     - Steps 0, 2, 3 are **🟢 Green (Normal Execution)**.
3. **Step 2 — Show Comparative Benchmark**:
   - Navigate to the **Benchmark Evaluation** tab.
   - Run **Comparative Benchmark (All Methods)** on 20 traces.
   - Show the bar chart: Point out how the **Proposed Engine** maintains $>87-95\%$ strict accuracy while the **All-at-Once baseline** collapses on step accuracy.
4. **Step 3 — Show Prompt Cache & Telemetry**:
   - Show the **Cache Telemetry** tab with high cache hit ratios and instant latency ($<3$ ms).

---

## 🔗 Related Notes
- [[00 - Project Overview & Index]]
- [[01 - Problem Statement & Literature Survey]]
- [[02 - System Architecture & Design]]
- [[03 - Core Engine Implementation]]
- [[04 - Benchmark & Evaluation Results]]
- [[05 - API, Async Queue & Dashboard]]
