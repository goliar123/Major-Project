"""
Full transformation script to replace all Mermaid blocks in Obsidian notes with rich, high-contrast, theme-safe HTML & CSS.
"""
import re
from pathlib import Path

BASE_CARD = (
    "background: #181825; border: 1px solid #313244; border-radius: 12px; "
    "padding: 20px; margin: 18px 0; color: #cdd6f4; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;"
)

def build_00_diagram():
    return f'''<div style="{BASE_CARD}">
  <div style="font-weight: bold; font-size: 1.05em; color: #89b4fa; margin-bottom: 14px; text-align: center;">⚡ Automated End-to-End Failure Attribution Pipeline</div>
  <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 8px;">
    <div style="flex: 1 1 140px; background: #1e1e2e; border: 1.5px solid #f38ba8; border-radius: 8px; padding: 12px; text-align: center;">
      <div style="font-size: 0.75em; font-weight: 800; color: #f38ba8; text-transform: uppercase;">Input</div>
      <div style="font-weight: 700; font-size: 0.9em; color: #ffffff; margin-top: 4px;">Failed Multi-Agent Trace</div>
    </div>
    <div style="color: #89b4fa; font-size: 1.3em; font-weight: bold;">➔</div>
    <div style="flex: 1 1 140px; background: #1e1e2e; border: 1.5px solid #89b4fa; border-radius: 8px; padding: 12px; text-align: center;">
      <div style="font-size: 0.75em; font-weight: 800; color: #89b4fa; text-transform: uppercase;">Phase 1</div>
      <div style="font-weight: 700; font-size: 0.9em; color: #ffffff; margin-top: 4px;">Trace Segmentation</div>
    </div>
    <div style="color: #89b4fa; font-size: 1.3em; font-weight: bold;">➔</div>
    <div style="flex: 1 1 140px; background: #1e1e2e; border: 1.5px solid #a6e3a1; border-radius: 8px; padding: 12px; text-align: center;">
      <div style="font-size: 0.75em; font-weight: 800; color: #a6e3a1; text-transform: uppercase;">Phase 2</div>
      <div style="font-weight: 700; font-size: 0.9em; color: #ffffff; margin-top: 4px;">Cached Step Judge</div>
    </div>
    <div style="color: #89b4fa; font-size: 1.3em; font-weight: bold;">➔</div>
    <div style="flex: 1 1 140px; background: #1e1e2e; border: 1.5px solid #cba6f7; border-radius: 8px; padding: 12px; text-align: center;">
      <div style="font-size: 0.75em; font-weight: 800; color: #cba6f7; text-transform: uppercase;">Phase 3</div>
      <div style="font-weight: 700; font-size: 0.9em; color: #ffffff; margin-top: 4px;">Dependency Linker (DAG)</div>
    </div>
    <div style="color: #89b4fa; font-size: 1.3em; font-weight: bold;">➔</div>
    <div style="flex: 1 1 140px; background: #1e1e2e; border: 1.5px solid #fab387; border-radius: 8px; padding: 12px; text-align: center;">
      <div style="font-size: 0.75em; font-weight: 800; color: #fab387; text-transform: uppercase;">Phase 4</div>
      <div style="font-weight: 700; font-size: 0.9em; color: #ffffff; margin-top: 4px;">Backward Causal Traversal</div>
    </div>
    <div style="color: #89b4fa; font-size: 1.3em; font-weight: bold;">➔</div>
    <div style="flex: 1 1 140px; background: #1e1e2e; border: 1.5px solid #f9e2af; border-radius: 8px; padding: 12px; text-align: center;">
      <div style="font-size: 0.75em; font-weight: 800; color: #f9e2af; text-transform: uppercase;">Phase 5</div>
      <div style="font-weight: 700; font-size: 0.9em; color: #ffffff; margin-top: 4px;">Root-Cause Resolution</div>
    </div>
    <div style="color: #89b4fa; font-size: 1.3em; font-weight: bold;">➔</div>
    <div style="flex: 1 1 140px; background: #1e1e2e; border: 1.5px solid #94e2d5; border-radius: 8px; padding: 12px; text-align: center;">
      <div style="font-size: 0.75em; font-weight: 800; color: #94e2d5; text-transform: uppercase;">Output</div>
      <div style="font-weight: 700; font-size: 0.9em; color: #ffffff; margin-top: 4px;">Dashboard & REST API</div>
    </div>
  </div>
</div>'''

def process_file_00(content):
    pattern = r'```mermaid\s*graph LR\s*A\[Failed Multi-Agent Trace\].*?```'
    return re.sub(pattern, build_00_diagram(), content, flags=re.DOTALL)

def process_file_18(content):
    # Diagram 1: DAG
    d1 = f'''<div style="{BASE_CARD}">
  <div style="font-weight: bold; font-size: 1.05em; color: #89b4fa; margin-bottom: 12px; text-align: center;">🕸️ Information Dependency DAG G = (V, E)</div>
  <svg width="100%" height="160" viewBox="0 0 820 150" xmlns="http://www.w3.org/2000/svg" style="background: #11111b; border-radius: 8px; border: 1px solid #313244;">
    <!-- Step 0 -->
    <rect x="20" y="35" width="140" height="75" rx="8" fill="#1e3a2f" stroke="#a6e3a1" stroke-width="2"/>
    <text x="90" y="60" fill="#a6e3a1" font-size="12" font-weight="bold" text-anchor="middle" font-family="sans-serif">Step 0: Coordinator</text>
    <text x="90" y="78" fill="#ffffff" font-size="10" text-anchor="middle" font-family="sans-serif">Score: 1.00</text>
    <text x="90" y="94" fill="#a6e3a1" font-size="10" font-weight="bold" text-anchor="middle" font-family="sans-serif">🟢 NORMAL</text>

    <!-- Arrow 0 -> 1 -->
    <line x1="160" y1="72" x2="190" y2="72" stroke="#89b4fa" stroke-width="2"/>
    <polygon points="190,72 182,67 182,77" fill="#89b4fa"/>

    <!-- Step 1 -->
    <rect x="195" y="35" width="140" height="75" rx="8" fill="#3e341f" stroke="#f9e2af" stroke-width="2"/>
    <text x="265" y="60" fill="#f9e2af" font-size="12" font-weight="bold" text-anchor="middle" font-family="sans-serif">Step 1: SearchAgent</text>
    <text x="265" y="78" fill="#ffffff" font-size="10" text-anchor="middle" font-family="sans-serif">HTTP 403 Block</text>
    <text x="265" y="94" fill="#f9e2af" font-size="10" font-weight="bold" text-anchor="middle" font-family="sans-serif">⚡ TRIGGER (0.20)</text>

    <!-- Arrow 1 -> 2 -->
    <line x1="335" y1="72" x2="365" y2="72" stroke="#89b4fa" stroke-width="2"/>
    <polygon points="365,72 357,67 357,77" fill="#89b4fa"/>

    <!-- Step 2 -->
    <rect x="370" y="35" width="140" height="75" rx="8" fill="#3d271d" stroke="#fab387" stroke-width="2"/>
    <text x="440" y="60" fill="#fab387" font-size="12" font-weight="bold" text-anchor="middle" font-family="sans-serif">Step 2: Extractor</text>
    <text x="440" y="78" fill="#ffffff" font-size="10" text-anchor="middle" font-family="sans-serif">Vague Range</text>
    <text x="440" y="94" fill="#fab387" font-size="10" font-weight="bold" text-anchor="middle" font-family="sans-serif">⚠️ WEAK INPUT (0.60)</text>

    <!-- Arrow 2 -> 3 -->
    <line x1="510" y1="72" x2="540" y2="72" stroke="#89b4fa" stroke-width="2"/>
    <polygon points="540,72 532,67 532,77" fill="#89b4fa"/>

    <!-- Step 3 -->
    <rect x="545" y="28" width="145" height="90" rx="8" fill="#441926" stroke="#f38ba8" stroke-width="3"/>
    <text x="617" y="55" fill="#f38ba8" font-size="13" font-weight="bold" text-anchor="middle" font-family="sans-serif">Step 3: WriterAgent</text>
    <text x="617" y="75" fill="#ffffff" font-size="11" text-anchor="middle" font-family="sans-serif">Reset Margin to NaN</text>
    <text x="617" y="95" fill="#f38ba8" font-size="10" font-weight="bold" text-anchor="middle" font-family="sans-serif">🔴 ROOT CAUSE (0.00)</text>

    <!-- Arrow 3 -> 4 -->
    <line x1="690" y1="72" x2="710" y2="72" stroke="#89b4fa" stroke-width="2"/>
    <polygon points="710,72 702,67 702,77" fill="#89b4fa"/>

    <!-- Step 4 -->
    <rect x="715" y="35" width="95" height="75" rx="8" fill="#3d271d" stroke="#fab387" stroke-width="2"/>
    <text x="762" y="60" fill="#fab387" font-size="12" font-weight="bold" text-anchor="middle" font-family="sans-serif">Step 4</text>
    <text x="762" y="78" fill="#ffffff" font-size="10" text-anchor="middle" font-family="sans-serif">ValidationErr</text>
    <text x="762" y="94" fill="#fab387" font-size="9" font-weight="bold" text-anchor="middle" font-family="sans-serif">🟠 SYMPTOM</text>

    <!-- Long range curved link Step 1 -> Step 3 -->
    <path d="M 265 35 Q 440 -15 617 28" fill="none" stroke="#f9e2af" stroke-width="1.5" stroke-dasharray="4"/>
    <text x="440" y="15" fill="#f9e2af" font-size="9" text-anchor="middle" font-family="sans-serif">Shared Entity: 'vantage_tech'</text>
  </svg>
</div>'''

    content = re.sub(r'```mermaid.*?graph LR\s*subgraph ExecutionDAG.*?```', d1, content, flags=re.DOTALL)

    # Diagram 2: Connection logic
    d2 = f'''<div style="{BASE_CARD}">
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
</div>'''

    content = re.sub(r'```mermaid.*?flowchart TD\s*TurnPair.*?```', d2, content, flags=re.DOTALL)
    return content

print("Transform functions 00 and 18 ready.")
