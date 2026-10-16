"""
Converts the remaining mermaid diagrams in Note 18 to HTML/CSS/SVG.
"""
import re
import shutil
from pathlib import Path

p = Path(r"d:\Projects\LLM\Notes\18 - Detailed Dependency Graph Architecture & Specifications.md")
c = p.read_text(encoding="utf-8")

svg_dag = """<div style="background: #181825; border: 1px solid #313244; border-radius: 12px; padding: 20px; margin: 18px 0; color: #cdd6f4; font-family: sans-serif;">
  <div style="font-weight: bold; font-size: 1.05em; color: #89b4fa; margin-bottom: 12px; text-align: center;">🕸️ Information Dependency DAG G = (V, E)</div>
  <svg width="100%" height="150" viewBox="0 0 820 140" xmlns="http://www.w3.org/2000/svg" style="background: #11111b; border-radius: 8px; border: 1px solid #313244;">
    <rect x="20" y="30" width="140" height="75" rx="8" fill="#1e3a2f" stroke="#a6e3a1" stroke-width="2"/>
    <text x="90" y="55" fill="#a6e3a1" font-size="12" font-weight="bold" text-anchor="middle" font-family="sans-serif">Step 0: Coordinator</text>
    <text x="90" y="75" fill="#ffffff" font-size="10" text-anchor="middle" font-family="sans-serif">Score: 1.00</text>
    <text x="90" y="93" fill="#a6e3a1" font-size="10" font-weight="bold" text-anchor="middle" font-family="sans-serif">🟢 NORMAL</text>

    <line x1="160" y1="67" x2="190" y2="67" stroke="#89b4fa" stroke-width="2"/>
    <polygon points="190,67 182,62 182,72" fill="#89b4fa"/>

    <rect x="195" y="30" width="140" height="75" rx="8" fill="#3e341f" stroke="#f9e2af" stroke-width="2"/>
    <text x="265" y="55" fill="#f9e2af" font-size="12" font-weight="bold" text-anchor="middle" font-family="sans-serif">Step 1: SearchAgent</text>
    <text x="265" y="75" fill="#ffffff" font-size="10" text-anchor="middle" font-family="sans-serif">HTTP 403 Block</text>
    <text x="265" y="93" fill="#f9e2af" font-size="10" font-weight="bold" text-anchor="middle" font-family="sans-serif">⚡ TRIGGER (0.20)</text>

    <line x1="335" y1="67" x2="365" y2="67" stroke="#89b4fa" stroke-width="2"/>
    <polygon points="365,67 357,62 357,72" fill="#89b4fa"/>

    <rect x="370" y="30" width="140" height="75" rx="8" fill="#3d271d" stroke="#fab387" stroke-width="2"/>
    <text x="440" y="55" fill="#fab387" font-size="12" font-weight="bold" text-anchor="middle" font-family="sans-serif">Step 2: Extractor</text>
    <text x="440" y="75" fill="#ffffff" font-size="10" text-anchor="middle" font-family="sans-serif">Vague Range</text>
    <text x="440" y="93" fill="#fab387" font-size="10" font-weight="bold" text-anchor="middle" font-family="sans-serif">⚠️ WEAK INPUT (0.60)</text>

    <line x1="510" y1="67" x2="540" y2="67" stroke="#89b4fa" stroke-width="2"/>
    <polygon points="540,67 532,62 532,72" fill="#89b4fa"/>

    <rect x="545" y="25" width="145" height="85" rx="8" fill="#441926" stroke="#f38ba8" stroke-width="3"/>
    <text x="617" y="52" fill="#f38ba8" font-size="13" font-weight="bold" text-anchor="middle" font-family="sans-serif">Step 3: WriterAgent</text>
    <text x="617" y="72" fill="#ffffff" font-size="11" text-anchor="middle" font-family="sans-serif">Reset Margin to NaN</text>
    <text x="617" y="92" fill="#f38ba8" font-size="10" font-weight="bold" text-anchor="middle" font-family="sans-serif">🔴 ROOT CAUSE (0.00)</text>

    <line x1="690" y1="67" x2="710" y2="67" stroke="#89b4fa" stroke-width="2"/>
    <polygon points="710,67 702,62 702,72" fill="#89b4fa"/>

    <rect x="715" y="30" width="95" height="75" rx="8" fill="#3d271d" stroke="#fab387" stroke-width="2"/>
    <text x="762" y="55" fill="#fab387" font-size="12" font-weight="bold" text-anchor="middle" font-family="sans-serif">Step 4</text>
    <text x="762" y="75" fill="#ffffff" font-size="10" text-anchor="middle" font-family="sans-serif">ValidationErr</text>
    <text x="762" y="93" fill="#fab387" font-size="9" font-weight="bold" text-anchor="middle" font-family="sans-serif">🟠 SYMPTOM</text>

    <path d="M 265 30 Q 440 -15 617 25" fill="none" stroke="#f9e2af" stroke-width="1.5" stroke-dasharray="4"/>
    <text x="440" y="15" fill="#f9e2af" font-size="9" text-anchor="middle" font-family="sans-serif">Shared Entity: 'vantage_tech'</text>
  </svg>
</div>"""

c = re.sub(r'```mermaid.*?graph LR\s*subgraph ExecutionDAG.*?```', svg_dag, c, flags=re.DOTALL)

cards_conn = """<div style="background: #181825; border: 1px solid #313244; border-radius: 12px; padding: 20px; margin: 18px 0; color: #cdd6f4; font-family: sans-serif;">
  <div style="font-weight: bold; font-size: 1.05em; color: #89b4fa; margin-bottom: 12px;">🔗 The 4 Edge Connection Typology (Dependency Linker)</div>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 12px;">
    <div style="background: #1e1e2e; border-top: 3px solid #89b4fa; border-radius: 8px; padding: 14px;">
      <div style="font-weight: bold; color: #89b4fa; margin-bottom: 4px;">1. data_flow (Weight: 0.85)</div>
      <div style="font-size: 0.85em; color: #cdd6f4;">Sequential dialogue continuity: Connects turn <code>i-1</code> to <code>i</code>.</div>
    </div>
    <div style="background: #1e1e2e; border-top: 3px solid #a6e3a1; border-radius: 8px; padding: 14px;">
      <div style="font-weight: bold; color: #a6e3a1; margin-bottom: 4px;">2. message_reply (Weight: 0.90)</div>
      <div style="font-size: 0.85em; color: #cdd6f4;">Explicit recipient handoffs when <code>step_u.recipient == step_v.agent_name</code>.</div>
    </div>
    <div style="background: #1e1e2e; border-top: 3px solid #fab387; border-radius: 8px; padding: 14px;">
      <div style="font-weight: bold; color: #fab387; margin-bottom: 4px;">3. shared_state (Weight: 0.95)</div>
      <div style="font-size: 0.85em; color: #cdd6f4;">AST entity reuse: variables, DB tables, function names across non-adjacent steps.</div>
    </div>
    <div style="background: #1e1e2e; border-top: 3px solid #f9e2af; border-radius: 8px; padding: 14px;">
      <div style="font-weight: bold; color: #f9e2af; margin-bottom: 4px;">4. instruction (Weight: 1.00)</div>
      <div style="font-size: 0.85em; color: #cdd6f4;">Top-level task goals & initial prompt constraints injected by Coordinator.</div>
    </div>
  </div>
</div>"""

c = re.sub(r'```mermaid.*?flowchart TD\s*TurnPair.*?```', cards_conn, c, flags=re.DOTALL)
p.write_text(c, encoding="utf-8")

# Mirror to Notes/Notes/
dest = Path(r"d:\Projects\LLM\Notes\Notes\18 - Detailed Dependency Graph Architecture & Specifications.md")
shutil.copy2(p, dest)
print("Note 18 successfully converted to HTML/CSS/SVG!")
