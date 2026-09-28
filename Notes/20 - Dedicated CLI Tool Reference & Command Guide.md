# 💻 20 - Dedicated CLI Tool Reference & Command Guide (`agent-trace`)

This document provides the complete command reference, flags, usage examples, and architecture for the **Dedicated Command-Line Interface (`agent-trace` / `python -m cli.main`)**.

---

## 🚀 1. Overview & Installation

The CLI provides terminal-first, real-time observability, trace diagnosis, live log watching, benchmark evaluation, and cache management for multi-agent systems without opening a web browser.

```html
<div style="background: #181825; border: 1px solid #313244; border-radius: 12px; padding: 20px; margin: 18px 0; color: #cdd6f4; font-family: sans-serif;">
  <div style="font-weight: bold; font-size: 1.05em; color: #89b4fa; margin-bottom: 12px; text-align: center;">⚡ CLI Command Suite Overview</div>
  <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 8px;">
    <div style="flex: 1 1 140px; background: #1e1e2e; border: 1.5px solid #89b4fa; border-radius: 8px; padding: 12px; text-align: center;">
      <div style="font-size: 0.75em; font-weight: 800; color: #89b4fa;">DIAGNOSE</div>
      <div style="font-weight: 700; font-size: 0.9em; color: #ffffff; margin-top: 4px;">Inspect Trace Files</div>
    </div>
    <div style="color: #89b4fa; font-size: 1.3em; font-weight: bold;">•</div>
    <div style="flex: 1 1 140px; background: #1e1e2e; border: 1.5px solid #a6e3a1; border-radius: 8px; padding: 12px; text-align: center;">
      <div style="font-size: 0.75em; font-weight: 800; color: #a6e3a1;">WATCH</div>
      <div style="font-weight: 700; font-size: 0.9em; color: #ffffff; margin-top: 4px;">Real-Time Log Stream</div>
    </div>
    <div style="color: #89b4fa; font-size: 1.3em; font-weight: bold;">•</div>
    <div style="flex: 1 1 140px; background: #1e1e2e; border: 1.5px solid #cba6f7; border-radius: 8px; padding: 12px; text-align: center;">
      <div style="font-size: 0.75em; font-weight: 800; color: #cba6f7;">BENCHMARK</div>
      <div style="font-weight: 700; font-size: 0.9em; color: #ffffff; margin-top: 4px;">Run Evaluation Suite</div>
    </div>
    <div style="color: #89b4fa; font-size: 1.3em; font-weight: bold;">•</div>
    <div style="flex: 1 1 140px; background: #1e1e2e; border: 1.5px solid #f9e2af; border-radius: 8px; padding: 12px; text-align: center;">
      <div style="font-size: 0.75em; font-weight: 800; color: #f9e2af;">CACHE</div>
      <div style="font-weight: 700; font-size: 0.9em; color: #ffffff; margin-top: 4px;">Stats & Pruning</div>
    </div>
    <div style="color: #89b4fa; font-size: 1.3em; font-weight: bold;">•</div>
    <div style="flex: 1 1 140px; background: #1e1e2e; border: 1.5px solid #94e2d5; border-radius: 8px; padding: 12px; text-align: center;">
      <div style="font-size: 0.75em; font-weight: 800; color: #94e2d5;">TEST-LLM</div>
      <div style="font-weight: 700; font-size: 0.9em; color: #ffffff; margin-top: 4px;">Verify Ollama Llama-3.2</div>
    </div>
  </div>
</div>
```

---

## 🛠️ 2. Detailed Command Reference

### A. `diagnose`: Inspect & Attribute Any Trace File
Runs the Neuro-Symbolic Causal Attribution Engine on any saved trace file (JSON, LangGraph execution dump, or Who&When benchmark trace).

```bash
python -m cli.main diagnose <path/to/trace.json> [--method proposed] [--export-html dag.html]
```

**Options:**
* `<file>`: Path to trace JSON file.
* `--method`: Attribution algorithm to use (`proposed`, `all_at_once`, `step_by_step`, `binary_search`). Default: `proposed`.
* `--export-html`: Generates and exports an interactive physics-enabled Pyvis DAG canvas (`.html`).

**Example Output:**
```text
╭─────────────────────────────── Trace Metadata ───────────────────────────────╮
│ Trace ID: cli_sample_01 | Total Turns: 4 | Environment: MultiAgent           │
│ Task Goal: Migrate database schema and preserve customer records             │
│ Evaluation Model: llama3.2:latest (ollama) | Diagnostic Latency: 0.012s      │
╰──────────────────────────────────────────────────────────────────────────────╯
                      Execution Steps Breakdown (4 Steps)                       
╭──────────┬────────────────────┬──────────┬──────────┬────────────────────────╮
│   Step   │ Agent              │ Action   │  Score   │       Diagnosis        │
├──────────┼────────────────────┼──────────┼──────────┼────────────────────────┤
│    #1    │ Planner            │ plan     │   0.95   │       🟢 HEALTHY       │
│    #2    │ DBArchitect        │ sql_drop │   0.00   │     🔴 ROOT CAUSE      │
│    #3    │ BackendDeveloper   │ orm_upd  │   0.95   │       🟢 HEALTHY       │
│    #4    │ QATester           │ run_test │   0.10   │       🟠 SYMPTOM       │
╰──────────┴────────────────────┴──────────┴──────────┴────────────────────────╯
╭────────────────────────────── Verdict Summary ───────────────────────────────╮
│ 🚨 ROOT CAUSE ATTRIBUTION REPORT                                             │
│                                                                              │
│ 📍 Responsible Agent: DBArchitect                                            │
│ 🔢 Decisive Step Number: Step 2 (ID: `step_2`)                               │
│ 🏷️ Failure Category: destructive_sql_query                                   │
│ 🔗 Causal Dependency Chain: Step 2 ➔ Step 4                                  │
│                                                                              │
│ Detailed Diagnosis:                                                          │
│ Agent 'DBArchitect' at Step 2 initiated the failure chain: Proposed          │
│ destructive DROP TABLE schema migration losing pre-existing records.         │
╰──────────────────────────────────────────────────────────────────────────────╯
✔ Visual Pyvis DAG exported successfully to: `dag.html`
```

---

### B. `watch`: Real-Time Streaming Log Follower
Tails an actively running agent swarm's log file (similar to `tail -f`), constructs the DAG on-the-fly, evaluates steps in shadow memory, and triggers attribution upon terminal failure or goal conflict.

```bash
python -m cli.main watch --log-file ./agent.log --goal "Scrape quarterly reports" [--expect "Revenue $14.2B"]
```

---

### C. `benchmark`: Run the Who&When Evaluation Suite
Evaluates multiple traces across the Who&When benchmark suite, calculates comparative metrics, and displays an animated progress bar and summary table.

```bash
python -m cli.main benchmark [--subset hand_crafted] [--limit 10] [--method proposed]
```

**Output Table:**
```text
                         Benchmark Evaluation Results                          
+-----------------------------------------------------------------------------+
| Metric                                           |      Score / Value       |
|--------------------------------------------------+--------------------------|
| Total Traces Evaluated                           |            10            |
| Agent-Level Accuracy                             |          100.0%          |
| Step-Level Accuracy                              |          100.0%          |
| Strict Joint Accuracy                            |          100.0%          |
| Avg Execution Time / Trace                       |          0.042s          |
| Cache Hit Rate                                   |          94.5%           |
+-----------------------------------------------------------------------------+
```

---

### D. `cache`: Inspect or Clear SHA256 Prompt Storage

```bash
# View cache statistics
python -m cli.main cache stats

# Reset and clear cache database
python -m cli.main cache clear
```

---

### E. `test-llm`: Verify Connection to Ollama (`llama3.2`)

```bash
python -m cli.main test-llm
```
*Sends a sample flawed database migration turn to `llama3.2` and verifies that the model returns valid structured diagnostic JSON.*

---

### F. `serve`: One-Command Launcher

```bash
# Launch Streamlit interactive dashboard
python -m cli.main serve dashboard --port 8501

# Launch FastAPI REST backend
python -m cli.main serve api --port 8000
```

---

## 🔗 Related Notes
- [[00 - Project Overview & Index]]
- [[03 - Core Engine Implementation]]
- [[05 - API, Async Queue & Dashboard]]
- [[18 - Detailed Dependency Graph Architecture & Specifications]]
- [[19 - Embedding HTML, CSS & Custom Diagrams in Obsidian]]
