"""
Replaces all Mermaid diagrams in Notes/ with beautiful, responsive,
theme-safe HTML/CSS components and SVG diagrams.
"""
import os
import re
import shutil
from pathlib import Path

BASE_CARD = (
    "background: #181825; border: 1px solid #313244; border-radius: 12px; "
    "padding: 20px; margin: 18px 0; color: #cdd6f4; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;"
)

def html_mindmap(title, branches):
    cols = []
    for b in branches:
        head = b.get("title", "")
        color = b.get("color", "#89b4fa")
        items = b.get("items", [])
        items_html = "".join([f'<li style="margin: 6px 0; font-size: 0.88em; color: #cdd6f4;">{it}</li>' for it in items])
        cols.append(f'''
    <div style="flex: 1 1 240px; background: #1e1e2e; border-top: 3px solid {color}; border-radius: 8px; padding: 14px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
      <div style="font-weight: bold; color: {color}; font-size: 0.95em; margin-bottom: 8px;">{head}</div>
      <ul style="margin: 0; padding-left: 18px; line-height: 1.4;">
        {items_html}
      </ul>
    </div>''')
    inner = "\n".join(cols)
    return f'''<div style="{BASE_CARD}">
  <div style="font-weight: bold; font-size: 1.1em; color: #ffffff; margin-bottom: 16px; border-bottom: 1px solid #313244; padding-bottom: 8px;">🧭 {title}</div>
  <div style="display: flex; flex-wrap: wrap; gap: 14px;">
{inner}
  </div>
</div>'''

def html_flowchart(title, steps):
    items = []
    for s in steps:
        border = s.get("border", "#89b4fa")
        bg = s.get("bg", "#1e1e2e")
        num = s.get("badge", "")
        head = s.get("title", "")
        sub = s.get("desc", "")
        badge_color = s.get("badge_color", "#11111b")
        badge_bg = s.get("badge_bg", border)
        items.append(f'''
    <div style="flex: 1 1 150px; min-width: 140px; background: {bg}; border: 1.5px solid {border}; border-radius: 8px; padding: 12px; text-align: center;">
      <div style="display: inline-block; background: {badge_bg}; color: {badge_color}; font-size: 0.72em; font-weight: 800; padding: 2px 7px; border-radius: 10px; margin-bottom: 4px;">{num}</div>
      <div style="font-weight: 700; font-size: 0.9em; color: #ffffff;">{head}</div>
      {f'<div style="font-size: 0.78em; color: #a6adc8; margin-top: 4px; line-height: 1.2;">{sub}</div>' if sub else ''}
    </div>''')
    arrow = '<div style="color: #89b4fa; font-size: 1.3em; font-weight: bold;">➔</div>'
    inner = f'\n{arrow}\n'.join(items)
    header = f'<div style="font-weight: bold; font-size: 1.05em; color: #89b4fa; margin-bottom: 14px; text-align: center;">{title}</div>' if title else ""
    return f'''<div style="{BASE_CARD}">
  {header}
  <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 8px;">
{inner}
  </div>
</div>'''

def html_er_diagram():
    return f'''<div style="{BASE_CARD}">
  <div style="font-weight: bold; font-size: 1.1em; color: #89b4fa; margin-bottom: 16px; border-bottom: 1px solid #313244; padding-bottom: 8px;">📊 Entity-Relationship (ER) Schema</div>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px;">
    
    <div style="background: #1e1e2e; border: 1.5px solid #89b4fa; border-radius: 8px; padding: 14px;">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #313244; padding-bottom: 6px; margin-bottom: 8px;">
        <span style="font-weight: bold; color: #89b4fa;">TRACES</span>
        <span style="font-size: 0.75em; background: #89b4fa; color: #11111b; padding: 2px 6px; border-radius: 8px; font-weight: bold;">Entity</span>
      </div>
      <div style="font-family: monospace; font-size: 0.82em; line-height: 1.6; color: #cdd6f4;">
        <div><strong style="color: #f38ba8;">PK</strong> trace_id : string</div>
        <div>title : string</div>
        <div>environment : string</div>
        <div>task_goal : string</div>
        <div>total_steps : int</div>
        <div>final_outcome : string</div>
      </div>
    </div>

    <div style="background: #1e1e2e; border: 1.5px solid #a6e3a1; border-radius: 8px; padding: 14px;">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #313244; padding-bottom: 6px; margin-bottom: 8px;">
        <span style="font-weight: bold; color: #a6e3a1;">STEPS</span>
        <span style="font-size: 0.75em; background: #a6e3a1; color: #11111b; padding: 2px 6px; border-radius: 8px; font-weight: bold;">1 : N from Traces</span>
      </div>
      <div style="font-family: monospace; font-size: 0.82em; line-height: 1.6; color: #cdd6f4;">
        <div><strong style="color: #f38ba8;">PK</strong> step_id : string</div>
        <div><strong style="color: #fab387;">FK</strong> trace_id : string</div>
        <div>step_index : int</div>
        <div>agent_name : string</div>
        <div>action_type : string</div>
        <div>action_payload : text</div>
        <div>output_state : text</div>
      </div>
    </div>

    <div style="background: #1e1e2e; border: 1.5px solid #cba6f7; border-radius: 8px; padding: 14px;">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #313244; padding-bottom: 6px; margin-bottom: 8px;">
        <span style="font-weight: bold; color: #cba6f7;">DEPENDENCIES</span>
        <span style="font-size: 0.75em; background: #cba6f7; color: #11111b; padding: 2px 6px; border-radius: 8px; font-weight: bold;">Edges</span>
      </div>
      <div style="font-family: monospace; font-size: 0.82em; line-height: 1.6; color: #cdd6f4;">
        <div><strong style="color: #f38ba8;">PK</strong> dependency_id : string</div>
        <div><strong style="color: #fab387;">FK</strong> source_step_index : int</div>
        <div><strong style="color: #fab387;">FK</strong> target_step_index : int</div>
        <div>data_variable : string</div>
        <div>dependency_type : string</div>
        <div>confidence : float</div>
      </div>
    </div>

    <div style="background: #1e1e2e; border: 1.5px solid #f9e2af; border-radius: 8px; padding: 14px;">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #313244; padding-bottom: 6px; margin-bottom: 8px;">
        <span style="font-weight: bold; color: #f9e2af;">CACHE_JUDGEMENTS</span>
        <span style="font-size: 0.75em; background: #f9e2af; color: #11111b; padding: 2px 6px; border-radius: 8px; font-weight: bold;">SQLite</span>
      </div>
      <div style="font-family: monospace; font-size: 0.82em; line-height: 1.6; color: #cdd6f4;">
        <div><strong style="color: #f38ba8;">PK</strong> prompt_hash : string</div>
        <div>model_name : string</div>
        <div>score : float</div>
        <div>anomaly_detected : bool</div>
        <div>error_category : string</div>
        <div>justification : text</div>
      </div>
    </div>

  </div>
</div>'''

def transform_all_notes():
    notes_dir = Path(r"d:\Projects\LLM\Notes")
    notes_notes_dir = Path(r"d:\Projects\LLM\Notes\Notes")

    # 1. Note 00
    p00 = notes_dir / "00 - Project Overview & Index.md"
    c00 = p00.read_text(encoding="utf-8")
    c00 = re.sub(r'```mermaid\s*graph LR\s*A\[Failed Multi-Agent Trace\].*?```', 
                 html_flowchart("⚡ Automated End-to-End Failure Attribution Pipeline", [
                     {"badge": "Input", "title": "Failed Multi-Agent Trace", "border": "#f38ba8", "badge_bg": "#f38ba8"},
                     {"badge": "Phase 1", "title": "Trace Segmentation", "border": "#89b4fa"},
                     {"badge": "Phase 2", "title": "Cached Step Judge", "border": "#a6e3a1"},
                     {"badge": "Phase 3", "title": "Dependency Linker (DAG)", "border": "#cba6f7"},
                     {"badge": "Phase 4", "title": "Backward Causal Traversal", "border": "#fab387"},
                     {"badge": "Phase 5", "title": "Root-Cause Resolution", "border": "#f9e2af"},
                     {"badge": "Output", "title": "Dashboard & REST API", "border": "#94e2d5", "badge_bg": "#94e2d5"}
                 ]), c00, flags=re.DOTALL)
    p00.write_text(c00, encoding="utf-8")

    # 2. Note 02
    p02 = notes_dir / "02 - System Architecture & Design.md"
    c02 = p02.read_text(encoding="utf-8")
    # Diagram 1: 5-Phase
    c02 = re.sub(r'```mermaid\s*flowchart TD\s*subgraph InputLayer.*?```',
                 html_flowchart("🏗️ 5-Phase Architectural Pipeline", [
                     {"badge": "Input", "title": "Trace Logs", "desc": "JSON / Console output", "border": "#f38ba8"},
                     {"badge": "Phase 1", "title": "Segmentation", "desc": "Turn token budgeting", "border": "#89b4fa"},
                     {"badge": "Phase 2", "title": "Step Judge & Cache", "desc": "Deterministic SHA256", "border": "#a6e3a1"},
                     {"badge": "Phase 3", "title": "Dependency DAG", "desc": "Typed edge lineage", "border": "#cba6f7"},
                     {"badge": "Phase 4", "title": "Backward Traversal", "desc": "Ancestral isolation", "border": "#fab387"},
                     {"badge": "Phase 5", "title": "Delivery", "desc": "Streamlit & FastAPI", "border": "#94e2d5"}
                 ]), c02, flags=re.DOTALL)
    # Diagram 2: DFD Level-0
    c02 = re.sub(r'```mermaid\s*graph LR\s*User\["Multi-Agent Trace Log.*?```',
                 html_flowchart("Level-0 Context DFD", [
                     {"badge": "Source", "title": "Developer / Multi-Agent Swarm", "desc": "Streams execution trace JSON", "border": "#89b4fa"},
                     {"badge": "System", "title": "0.0 Failure Attribution Engine", "desc": "Neuro-Symbolic causal DAG isolation", "border": "#f38ba8", "bg": "#2d1b2d"},
                     {"badge": "Target", "title": "Dashboard / API Client", "desc": "Receives root-cause verdict & DAG", "border": "#a6e3a1"}
                 ]), c02, flags=re.DOTALL)
    # Diagram 3: DFD Level-1
    c02 = re.sub(r'```mermaid\s*flowchart TD\s*TraceIn\["Multi-Agent Trace Log"\].*?```',
                 html_flowchart("Level-1 Detailed Data Flow Diagram", [
                     {"badge": "1.0", "title": "Trace Segmentation", "desc": "Bounded turn extraction", "border": "#89b4fa"},
                     {"badge": "2.0", "title": "Step Judge & Cache", "desc": "SQLite SHA256 prompt hashing", "border": "#a6e3a1"},
                     {"badge": "3.0", "title": "Dependency Linker", "desc": "Sequential + message + shared entities", "border": "#cba6f7"},
                     {"badge": "4.0", "title": "Backward Traversal", "desc": "Isolates decisive step & causal chain", "border": "#fab387"},
                     {"badge": "5.0", "title": "Verdict Assembly", "desc": "Generates diagnosis & visual graph", "border": "#94e2d5"}
                 ]), c02, flags=re.DOTALL)
    # Diagram 4: ER
    c02 = re.sub(r'```mermaid\s*erDiagram.*?```', html_er_diagram(), c02, flags=re.DOTALL)
    p02.write_text(c02, encoding="utf-8")

    # 3. Note 07
    p07 = notes_dir / "07 - Theoretical Concepts & Core Mechanisms.md"
    c07 = p07.read_text(encoding="utf-8")
    # Diagram 1: DAG
    d_07_1 = f'''<div style="{BASE_CARD}">
  <div style="font-weight: bold; font-size: 1.05em; color: #89b4fa; margin-bottom: 12px; text-align: center;">Execution Dependency DAG G = (V, E)</div>
  <svg width="100%" height="150" viewBox="0 0 820 140" xmlns="http://www.w3.org/2000/svg" style="background: #11111b; border-radius: 8px; border: 1px solid #313244;">
    <rect x="20" y="30" width="140" height="75" rx="8" fill="#1e3a2f" stroke="#a6e3a1" stroke-width="2"/>
    <text x="90" y="55" fill="#a6e3a1" font-size="12" font-weight="bold" text-anchor="middle" font-family="sans-serif">Step 0: UserProxy</text>
    <text x="90" y="75" fill="#ffffff" font-size="10" text-anchor="middle" font-family="sans-serif">Task Goal Injection</text>
    <text x="90" y="93" fill="#a6e3a1" font-size="10" font-weight="bold" text-anchor="middle" font-family="sans-serif">🟢 CLEAN (1.00)</text>

    <line x1="160" y1="67" x2="190" y2="67" stroke="#89b4fa" stroke-width="2"/>
    <polygon points="190,67 182,62 182,72" fill="#89b4fa"/>

    <rect x="195" y="25" width="150" height="85" rx="8" fill="#441926" stroke="#f38ba8" stroke-width="3"/>
    <text x="270" y="52" fill="#f38ba8" font-size="12" font-weight="bold" text-anchor="middle" font-family="sans-serif">Step 1: DBArchitect</text>
    <text x="270" y="72" fill="#ffffff" font-size="11" text-anchor="middle" font-family="sans-serif">DROP TABLE Query</text>
    <text x="270" y="92" fill="#f38ba8" font-size="10" font-weight="bold" text-anchor="middle" font-family="sans-serif">🔴 ROOT CAUSE (0.00)</text>

    <line x1="345" y1="67" x2="375" y2="67" stroke="#89b4fa" stroke-width="2"/>
    <polygon points="375,67 367,62 367,72" fill="#89b4fa"/>

    <rect x="380" y="30" width="135" height="75" rx="8" fill="#3d271d" stroke="#fab387" stroke-width="2"/>
    <text x="447" y="55" fill="#fab387" font-size="12" font-weight="bold" text-anchor="middle" font-family="sans-serif">Step 2: Backend</text>
    <text x="447" y="75" fill="#ffffff" font-size="10" text-anchor="middle" font-family="sans-serif">Migration Script</text>
    <text x="447" y="93" fill="#fab387" font-size="10" font-weight="bold" text-anchor="middle" font-family="sans-serif">🟠 SYMPTOM (0.40)</text>

    <line x1="515" y1="67" x2="545" y2="67" stroke="#89b4fa" stroke-width="2"/>
    <polygon points="545,67 537,62 537,72" fill="#89b4fa"/>

    <rect x="550" y="30" width="130" height="75" rx="8" fill="#3d271d" stroke="#fab387" stroke-width="2"/>
    <text x="615" y="55" fill="#fab387" font-size="12" font-weight="bold" text-anchor="middle" font-family="sans-serif">Step 3: Reviewer</text>
    <text x="615" y="75" fill="#ffffff" font-size="10" text-anchor="middle" font-family="sans-serif">Syntax Check</text>
    <text x="615" y="93" fill="#fab387" font-size="10" font-weight="bold" text-anchor="middle" font-family="sans-serif">🟠 SYMPTOM (0.35)</text>

    <line x1="680" y1="67" x2="710" y2="67" stroke="#89b4fa" stroke-width="2"/>
    <polygon points="710,67 702,62 702,72" fill="#89b4fa"/>

    <rect x="715" y="30" width="95" height="75" rx="8" fill="#3d271d" stroke="#fab387" stroke-width="2"/>
    <text x="762" y="55" fill="#fab387" font-size="12" font-weight="bold" text-anchor="middle" font-family="sans-serif">Step 4</text>
    <text x="762" y="75" fill="#ffffff" font-size="10" text-anchor="middle" font-family="sans-serif">Assert: 0 rows</text>
    <text x="762" y="93" fill="#fab387" font-size="9" font-weight="bold" text-anchor="middle" font-family="sans-serif">💀 CRASH (0.1)</text>

    <path d="M 270 25 Q 515 -15 762 30" fill="none" stroke="#f9e2af" stroke-width="1.5" stroke-dasharray="4"/>
    <text x="515" y="15" fill="#f9e2af" font-size="9" text-anchor="middle" font-family="sans-serif">Shared Table: 'users'</text>
  </svg>
</div>'''
    c07 = re.sub(r'```mermaid\s*graph LR\s*subgraph ExecutionDAG.*?```', d_07_1, c07, flags=re.DOTALL)

    # Diagram 2: Backward Traversal
    c07 = re.sub(r'```mermaid\s*flowchart RL\s*S_manifest.*?```',
                 html_flowchart("⬅️ Backward Causal Traversal vs Naive Forward Judge", [
                     {"badge": "Step 150", "title": "Manifest Symptom", "desc": "Terminal Abort / Crash", "border": "#fab387"},
                     {"badge": "Step 149", "title": "Secondary Failure", "desc": "Context Saturation in loop", "border": "#fab387"},
                     {"badge": "Step 144", "title": "Primary Bug", "desc": "Reset Margin to NaN 🔴", "border": "#f38ba8", "bg": "#441926", "badge_bg": "#f38ba8"},
                     {"badge": "Step 19", "title": "Upstream Trigger", "desc": "Cloudflare 403 Scrape Block ⚡", "border": "#f9e2af"},
                     {"badge": "Step 18", "title": "Valid Prior Step", "desc": "Healthy execution 🟢", "border": "#a6e3a1"}
                 ]), c07, flags=re.DOTALL)

    # Diagram 3: Linkage Engine
    c07 = re.sub(r'```mermaid\s*flowchart TD\s*subgraph LinkageEngine.*?```',
                 html_mindmap("The 4-Tier Dependency Linker Mechanisms", [
                     {"title": "1. Sequential Flow (i-1 ➔ i)", "color": "#89b4fa", "items": ["Maintains conversation dialogue continuity", "Default baseline temporal edge (Weight: 0.85)"]},
                     {"title": "2. Message-Reply Handoff", "color": "#a6e3a1", "items": ["Direct agent-to-agent communication", "Matched when recipient == next agent (Weight: 0.90)"]},
                     {"title": "3. Entity & State Lineage", "color": "#fab387", "items": ["AST regex extraction of variable names", "Matches DB tables, function names, and URLs (Weight: 0.95)"]},
                     {"title": "4. Task Instruction Flow", "color": "#f9e2af", "items": ["Connects User/Coordinator goal to sub-agents", "Immutable task constraints (Weight: 1.00)"]}
                 ]), c07, flags=re.DOTALL)

    # Diagram 4: Cache Lookup
    c07 = re.sub(r'```mermaid\s*graph TD\s*Step\["Execution Step Turn s_i"\].*?```',
                 html_flowchart("Deterministic SHA256 Evaluation Caching Flow", [
                     {"badge": "Step", "title": "Execution Turn s_i", "desc": "Goal + Context + Payload", "border": "#89b4fa"},
                     {"badge": "Hash", "title": "SHA256 Fingerprint", "desc": "SHA256(Model || Prompt)", "border": "#cba6f7"},
                     {"badge": "Lookup", "title": "SQLite Cache DB", "desc": "Key-value hash index", "border": "#f9e2af"},
                     {"badge": "Hit / Miss", "title": "Verdict Dispatch", "desc": "Hit: <1ms ($0) | Miss: LLM query", "border": "#a6e3a1"}
                 ]), c07, flags=re.DOTALL)

    # Diagram 5: 3-Tier Blame
    c07 = re.sub(r'```mermaid\s*graph TD\s*T1\["⚡ 1\. Upstream Trigger.*?```',
                 html_mindmap("The 3-Tier Blame Hierarchy", [
                     {"title": "⚡ 1. Upstream Trigger (The Provocation)", "color": "#f9e2af", "items": ["Environmental scraping block (HTTP 403 Forbidden)", "Missing API keys or rate-limit saturation", "Non-deterministic external network drops"]},
                     {"title": "🔴 2. Primary Root Cause (The Bug)", "color": "#f38ba8", "items": ["State tree corruption (overwriting value with NaN)", "Destructive SQL queries (DROP TABLE)", "Off-by-one logic errors or hallucinated tool parameters"]},
                     {"title": "🟠 3. Secondary Breakdown & Symptom", "color": "#fab387", "items": ["Context window saturation in endless recovery loops", "Recursion limit exceeded", "Final crash / Pydantic schema validation error"]}
                 ]), c07, flags=re.DOTALL)

    # Diagram 6: System Hardening
    c07 = re.sub(r'```mermaid\s*flowchart LR\s*subgraph HardeningLayers.*?```',
                 html_mindmap("System Hardening & Production Safeguards", [
                     {"title": "1. Token Budgeting", "color": "#89b4fa", "items": ["Truncates turns to ≤4k tokens", "Preserves head & tail to prevent OOM"]},
                     {"title": "2. SHA256 Caching", "color": "#a6e3a1", "items": ["~65% token cost reduction", "Zero cost repeat benchmark evaluations"]},
                     {"title": "3. Storage Fallback", "color": "#fab387", "items": ["Gracefully falls back: Redis ➔ Mongo ➔ SQLite", "Works 100% offline out-of-the-box"]},
                     {"title": "4. Structural Validation", "color": "#f9e2af", "items": ["Guarantees acyclicity in DAG", "Auto-repairs malformed LLM JSON verdicts"]}
                 ]), c07, flags=re.DOTALL)
    p07.write_text(c07, encoding="utf-8")

    # 4. Note 08
    p08 = notes_dir / "08 - Beginner Friendly Prerequisite & Concepts Guide.md"
    c08 = p08.read_text(encoding="utf-8")
    c08 = re.sub(r'```mermaid\s*flowchart TD\s*subgraph Level1.*?```',
                 html_mindmap("Multi-Agent Systems Prerequisite Roadmap", [
                     {"title": "Level 1: AI & Agent Basics", "color": "#89b4fa", "items": ["What is an LLM & Prompt Engineering?", "What is a Multi-Agent System (MAS)?", "How Agents communicate via turns & tools"]},
                     {"title": "Level 2: The Core Problem", "color": "#f38ba8", "items": ["Cascading Errors (Error propagation)", "Why naive LLMs blame symptoms instead of bugs", "The Context Window explosion trap"]},
                     {"title": "Level 3: Neuro-Symbolic Solution", "color": "#a6e3a1", "items": ["Directed Acyclic Graphs (DAGs) in NetworkX", "Backward Causal Traversal (Backtracking)", "Deterministic SHA256 Prompt Caching"]}
                 ]), c08, flags=re.DOTALL)
    p08.write_text(c08, encoding="utf-8")

    # 5. Note 10
    p10 = notes_dir / "10 - Why Enterprise MNCs Fail at Multi-Agent Debugging.md"
    c10 = p10.read_text(encoding="utf-8")
    c10 = re.sub(r'```mermaid\s*mindmap\s*root\(\(Why MNCs Struggle With MAS Debugging\)\).*?```',
                 html_mindmap("Why Enterprise MNCs Struggle with Multi-Agent Debugging", [
                     {"title": "1. The Monolithic LLM-as-a-Judge Trap", "color": "#f38ba8", "items": ["Context window attention decay (>50k tokens)", "Lost-in-the-middle phenomenon on long swarms", "Recency bias: blaming whoever crashed last"]},
                     {"title": "2. Flat Event Streams vs Causal DAGs", "color": "#89b4fa", "items": ["Datadog/CloudWatch only show flat chronological logs", "No semantic causal linkage between non-adjacent steps", "Debugging requires 4+ hours of manual reading"]},
                     {"title": "3. Silent Semantic Drift", "color": "#fab387", "items": ["Agents fail without throwing syntax exceptions", "Errors look like polite valid English while data is corrupt", "Compounding numerical and logical decay"]}
                 ]), c10, flags=re.DOTALL)
    p10.write_text(c10, encoding="utf-8")

    # 6. Note 11
    p11 = notes_dir / "11 - Post-Hoc Attribution vs AGI & Neuro-Symbolic AI.md"
    c11 = p11.read_text(encoding="utf-8")
    c11 = re.sub(r'```mermaid\s*graph TD\s*subgraph BigTechMove.*?```',
                 html_flowchart("The Frontier AI Paradigm Shift (2024–2026)", [
                     {"badge": "Old Paradigm", "title": "Monolithic LLM", "desc": "One giant forward pass. Context decay on 100 turns.", "border": "#f38ba8"},
                     {"badge": "New Paradigm", "title": "Neuro-Symbolic Search", "desc": "Step-wise verification (PRMs), Graph of Thoughts, Backtracking.", "border": "#a6e3a1"},
                     {"badge": "Our Solution", "title": "Causal Attribution Engine", "desc": "Applies backward causal DAG search to debug multi-agent swarms.", "border": "#89b4fa"}
                 ]), c11, flags=re.DOTALL)
    c11 = re.sub(r'```mermaid\s*mindmap\s*root\(\(The 4 AGI Frontiers Beyond Attribution\)\).*?```',
                 html_mindmap("The 4 AGI Frontiers Beyond Attribution", [
                     {"title": "1. Generative Synthesis vs Diagnosis", "color": "#89b4fa", "items": ["Diagnosis is verification; Generation is search over infinite spaces", "Attribution tells you what broke; AGI knows what to invent"]},
                     {"title": "2. Open-World Grounding", "color": "#a6e3a1", "items": ["Real-world robotics and physical embodiment", "Navigating unstructured environments beyond text"]},
                     {"title": "3. Continual Online Learning", "color": "#fab387", "items": ["Self-updating neural weights without catastrophic forgetting", "Dynamic epistemic updating"]},
                     {"title": "4. Autonomous In-Situ Self-Correction", "color": "#cba6f7", "items": ["In-flight backtracking before committing real-world actions", "Self-repairing agent swarms"]}
                 ]), c11, flags=re.DOTALL)
    p11.write_text(c11, encoding="utf-8")

    # 7. Note 12
    p12 = notes_dir / "12 - Exhaustive Analysis of All 12 Research Papers (2025-2026).md"
    c12 = p12.read_text(encoding="utf-8")
    c12 = re.sub(r'```mermaid\s*graph TD\s*subgraph ResearchLineage.*?```',
                 html_flowchart("Evolution of Multi-Agent Failure Attribution Research", [
                     {"badge": "ICML 2025", "title": "Zhang et al. (Who&When)", "desc": "Identified the problem; LLM judge scored only 14.2% step accuracy", "border": "#f38ba8"},
                     {"badge": "2025", "title": "MAST & AgenTracer", "desc": "Temporal hierarchy and execution trees; struggled on non-linear loops", "border": "#fab387"},
                     {"badge": "2025–2026", "title": "TRAIL & CHIEF", "desc": "Introduced graph concepts but suffered from heavy LLM latency", "border": "#f9e2af"},
                     {"badge": "Proposed", "title": "Our Neuro-Symbolic Engine", "desc": "Causal DAG + SHA256 Caching + Backward Traversal (95%+ accuracy)", "border": "#a6e3a1", "bg": "#1e3a2f"}
                 ]), c12, flags=re.DOTALL)
    p12.write_text(c12, encoding="utf-8")

    # 8. Note 13
    p13 = notes_dir / "13 - Deep Analysis of Survey Papers & Why Root Cause Attribution is Intractably Hard.md"
    c13 = p13.read_text(encoding="utf-8")
    c13 = re.sub(r'```mermaid\s*mindmap\s*root\(\(The 4 Fundamental Barriers of MAS Attribution\)\).*?```',
                 html_mindmap("The 4 Fundamental Barriers of Multi-Agent Attribution", [
                     {"title": "1. Emergent Social Entanglement", "color": "#f38ba8", "items": ["Sycophancy: Agent B blindly validates Agent A's corrupted data", "Role drift and derailment over 100 turns", "Multi-agent circular consensus traps"]},
                     {"title": "2. Silent Semantic Drift", "color": "#fab387", "items": ["Zero-exception failures: all Python code runs with returncode 0", "Data looks grammatically valid while values are mathematically broken", "Errors cascade invisibly until final validation crash"]},
                     {"title": "3. The Graph Tracer Trap", "color": "#f9e2af", "items": ["Using LLMs to generate graph edges creates hallucinated causal links", "Spurious cycles and false dependencies ruin topological sorting"]},
                     {"title": "4. Exponential Trace Search Space", "color": "#89b4fa", "items": ["N=150 turns across 10 agents yields astronomical combinations", "Monolithic LLM prompt exceeds 128k tokens with severe attention drop"]}
                 ]), c13, flags=re.DOTALL)
    p13.write_text(c13, encoding="utf-8")

    # 9. Note 14
    p14 = notes_dir / "14 - Real-World Impact, Industry Utility & Viva Defense.md"
    c14 = p14.read_text(encoding="utf-8")
    c14 = re.sub(r'```mermaid\s*graph TD\s*A\["Capstone Project Evaluation"\].*?```',
                 html_mindmap("Capstone Project Scoring & Viva Defense Architecture", [
                     {"title": "1. Literature Rigor", "color": "#89b4fa", "items": ["12 Top-tier papers surveyed (ICML, NeurIPS, EMNLP)", "Identified the 14.2% baseline accuracy gap"]},
                     {"title": "2. Algorithmic Contribution", "color": "#a6e3a1", "items": ["Directed Acyclic Graph (DAG) construction", "Backward Causal Traversal with ancestral isolation"]},
                     {"title": "3. Working Full-Stack System", "color": "#cba6f7", "items": ["FastAPI REST backend with async task queue", "Streamlit interactive DAG visualization (Pyvis)"]},
                     {"title": "4. Enterprise Market Value", "color": "#fab387", "items": ["'Sentry for Agentic AI'", "Resolves multi-agent crashes in <50ms instead of 4h"]}
                 ]), c14, flags=re.DOTALL)
    p14.write_text(c14, encoding="utf-8")

    # 10. Note 15
    p15 = notes_dir / "15 - The Neuro-Symbolic Reality - Heuristics vs LLMs in Causal Attribution.md"
    c15 = p15.read_text(encoding="utf-8")
    c15 = re.sub(r'```mermaid\s*graph LR\s*subgraph TheTwoLayers.*?```',
                 html_mindmap("The Neuro-Symbolic Separation of Concerns", [
                     {"title": "Layer 1: Structural Causality (Who passed data to whom?)", "color": "#89b4fa", "items": ["Best solved by GRAPH THEORY (NetworkX)", "100% deterministic, zero hallucinations, microsecond execution", "Prevents cycle creation and models true information lineage"]},
                     {"title": "Layer 2: Semantic Verification (Did this step make a mistake?)", "color": "#a6e3a1", "items": ["Best solved by LLM STEP JUDGES (Llama-3.2 / Gemini)", "Evaluates reasoning validity against task constraints", "Cached with SHA256 prompt hashing for zero token waste"]}
                 ]), c15, flags=re.DOTALL)
    p15.write_text(c15, encoding="utf-8")

    # 11. Note 16
    p16 = notes_dir / "16 - Commercialization Blueprint & Enterprise Exit Strategy.md"
    c16 = p16.read_text(encoding="utf-8")
    c16 = re.sub(r'```mermaid\s*graph LR\s*subgraph MarketTrajectory.*?```',
                 html_flowchart("The 4-Step Commercial & Acquisition Playbook", [
                     {"badge": "Step 1", "title": "Open-Source SDK", "desc": "GitHub + PyPI + arXiv Research Paper", "border": "#89b4fa"},
                     {"badge": "Step 2", "title": "Seed Funding", "desc": "YC / AI Grant / a16z ($1.5M–$3M)", "border": "#a6e3a1"},
                     {"badge": "Step 3", "title": "Enterprise Cloud SaaS", "desc": "B2B Subscriptions ($99–$2.5k/mo)", "border": "#cba6f7"},
                     {"badge": "Step 4", "title": "Strategic Acquisition", "desc": "Sold to Google, Microsoft, or Datadog", "border": "#f38ba8", "bg": "#441926"}
                 ]), c16, flags=re.DOTALL)
    p16.write_text(c16, encoding="utf-8")

    # 12. Note 17
    p17 = notes_dir / "17 - The Market Maturity Curve & Enterprise Product Scope.md"
    c17 = p17.read_text(encoding="utf-8")
    c17 = re.sub(r'```mermaid\s*flowchart TD\s*subgraph CurrentHacks.*?```',
                 html_mindmap("How Enterprises Currently Deal with Multi-Agent Crashes", [
                     {"title": "1. Brute-Force Retry & Restart", "color": "#f38ba8", "items": ["Throw away the 100-step run and re-run with higher temperature", "Burns $5–$20 per failure and takes 10+ minutes"]},
                     {"title": "2. Over-Constrained Supervisor Loops", "color": "#fab387", "items": ["Adding multiple LLM critic agents", "Creates endless critique loops and context saturation"]},
                     {"title": "3. Manual Log Reading", "color": "#89b4fa", "items": ["Senior engineers spend 3–4 hours reading 50k tokens of JSON", "Unscalable and prone to human misattribution"]}
                 ]), c17, flags=re.DOTALL)
    c17 = re.sub(r'```mermaid\s*mindmap\s*root\(\(The Enterprise Product Scope\)\).*?```',
                 html_mindmap("The 3 Pillars of the Enterprise Commercial Moat", [
                     {"title": "1. Robust Natural Language Lineage", "color": "#89b4fa", "items": ["Zero-code auto-instrumentation via OpenTelemetry", "AST-based entity tracking without human regex", "Co-reference resolution across asynchronous message queues"]},
                     {"title": "2. Closed-Loop Time-Travel Self-Healing", "color": "#a6e3a1", "items": ["State checkpointing at each execution turn", "Rollback memory state to Step 143 (before NaN bug)", "Auto-patch prompt and resume without restarting Steps 1-142"]},
                     {"title": "3. Enterprise Infrastructure & Scale", "color": "#cba6f7", "items": ["ClickHouse / Kafka streaming at 100,000 events/sec", "SOC2 Type II, HIPAA compliance, automated PII redaction", "VPC and on-premise air-gapped deployment"]}
                 ]), c17, flags=re.DOTALL)
    p17.write_text(c17, encoding="utf-8")

    # 13. Note 19
    p19 = notes_dir / "19 - Embedding HTML, CSS & Custom Diagrams in Obsidian.md"
    c19 = p19.read_text(encoding="utf-8")
    c19 = re.sub(r'```mermaid.*?graph LR\s*S0\["Step 0: Coordinator.*?```',
                 html_flowchart("High-Contrast Theme-Safe Pipeline Showcase", [
                     {"badge": "Step 0", "title": "Coordinator", "desc": "Initial Goal 🟢", "border": "#a6e3a1"},
                     {"badge": "Step 1", "title": "SearchAgent", "desc": "403 Forbidden ⚡", "border": "#f9e2af"},
                     {"badge": "Step 2", "title": "ExtractorAgent", "desc": "Vague Range ⚠️", "border": "#fab387"},
                     {"badge": "Step 3", "title": "WriterAgent", "desc": "Reset to NaN 🔴", "border": "#f38ba8", "bg": "#441926"},
                     {"badge": "Step 4", "title": "QATester", "desc": "ValidationError 🟠", "border": "#fab387"}
                 ]), c19, flags=re.DOTALL)
    p19.write_text(c19, encoding="utf-8")

    # Mirror all updated files to Notes/Notes/
    for md_file in notes_dir.glob("*.md"):
        dest = notes_notes_dir / md_file.name
        shutil.copy2(md_file, dest)

    print("All 14 notes updated with beautiful HTML/CSS components in both directories!")

if __name__ == "__main__":
    transform_all_notes()
