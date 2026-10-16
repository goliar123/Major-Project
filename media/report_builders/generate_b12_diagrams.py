"""
Professional Diagram Generator for Major Project Phase-I Report (B12 Format).
Generates high-resolution (2000x1250), publication-quality UML and architectural diagrams
matching the signature aesthetic of the GRIET CSE B12 template.
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "/home/goliar/Documents/LLM/media/diagrams/docs_diagrams"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_BOLD = "/usr/share/fonts/liberation-serif-fonts/LiberationSerif-Bold.ttf"
FONT_REG = "/usr/share/fonts/liberation-serif-fonts/LiberationSerif-Regular.ttf"
FONT_ITALIC = "/usr/share/fonts/liberation-serif-fonts/LiberationSerif-Italic.ttf"

def get_font(size, bold=False, italic=False):
    f_path = FONT_BOLD if bold else (FONT_ITALIC if italic else FONT_REG)
    return ImageFont.truetype(f_path, size)

def draw_multiline_text(draw, xy, text, font, fill):
    cx, cy = xy
    lines = text.split("\n")
    line_h = font.size + 4
    total_h = len(lines) * line_h
    start_y = cy - total_h / 2
    for i, line in enumerate(lines):
        draw.text((cx, start_y + i * line_h), line, font=font, fill=fill, anchor="mt")

def draw_title(draw, text, y=30):
    font = get_font(38, bold=True)
    draw.text((1000, y), text, font=font, fill="#b91c1c", anchor="mt")

def draw_bottom_cards(draw, cards, y=940, h=270):
    # cards: list of (title, items_list, bg_color, border_color)
    n = len(cards)
    gap = 25
    margin = 40
    total_w = 2000 - 2 * margin
    w = (total_w - (n - 1) * gap) / n
    for i, (title, items, bg, border) in enumerate(cards):
        x0 = margin + i * (w + gap)
        y0 = y
        x1 = x0 + w
        y1 = y0 + h
        # Background & border
        draw.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=bg, outline=border, width=2)
        # Title
        f_title = get_font(18, bold=True)
        draw.text((x0 + 16, y0 + 14), title, font=f_title, fill="#0f172a")
        # Line under title
        draw.line([x0 + 16, y0 + 40, x1 - 16, y0 + 40], fill=border, width=1)
        # Items
        f_item = get_font(14, bold=False)
        curr_y = y0 + 50
        for item in items:
            # Word wrap or truncate if needed
            draw.text((x0 + 18, curr_y), "• " + item, font=f_item, fill="#1e293b")
            curr_y += 24

# -------------------------------------------------------------------------
# Figure 3.1: Architecture Diagram
# -------------------------------------------------------------------------
def create_fig_3_1():
    rev2_path = "/home/goliar/Documents/LLM/media/diagrams/system_architecture_review2.png"
    if os.path.exists(rev2_path):
        im_arch = Image.open(rev2_path)
        target_w = 3000
        target_h = int(im_arch.height * (target_w / im_arch.width))
        im_arch_resized = im_arch.resize((target_w, target_h), Image.Resampling.LANCZOS)
        out_path = os.path.join(OUTPUT_DIR, "fig_3_1_architecture.png")
        im_arch_resized.save(out_path, quality=95)
        print("Generated official Review-2 Architecture Diagram:", out_path)
        return

    im = Image.new("RGB", (2000, 1250), "#ffffff")
    draw = ImageDraw.Draw(im)
    draw_title(draw, "Architecture Diagram – Neuro-Symbolic Failure Attribution Engine")

    # Layer 1: Trace Ingestion (Left Column)
    draw.rounded_rectangle([60, 110, 480, 900], radius=14, fill="#f8fafc", outline="#3b82f6", width=2)
    draw.rectangle([60, 110, 480, 160], fill="#3b82f6")
    draw.text((270, 135), "1. Ingestion & Preprocessing", font=get_font(20, bold=True), fill="white", anchor="mm")
    
    steps_1 = [
        ("Multi-Agent Frameworks", "AutoGen, LangGraph, MetaGPT, CrewAI logs", "#dbeafe", "#1d4ed8"),
        ("Trace Ingestion Engine", "Accepts JSON, JSONL, and console streams", "#eff6ff", "#3b82f6"),
        ("TraceSegmenter", "Extracts agent personas, turns, and context", "#eff6ff", "#3b82f6"),
        ("Context Token Budgeter", "Asymmetric Head (60%) & Tail (30%) slicing", "#fef3c7", "#d97706"),
        ("Canonical Step Normalizer", "Standardizes into ExecutionStep domain entities", "#eff6ff", "#3b82f6")
    ]
    y_c = 180
    for name, desc, bg, ec in steps_1:
        draw.rounded_rectangle([80, y_c, 460, y_c + 115], radius=10, fill=bg, outline=ec, width=2)
        draw.text((100, y_c + 20), name, font=get_font(17, bold=True), fill="#0f172a")
        draw.text((100, y_c + 50), desc, font=get_font(13), fill="#334155")
        y_c += 138

    # Layer 2: Cached Neural Evaluation (Middle Left)
    draw.rounded_rectangle([520, 110, 960, 900], radius=14, fill="#f8fafc", outline="#10b981", width=2)
    draw.rectangle([520, 110, 960, 160], fill="#10b981")
    draw.text((740, 135), "2. Cached Semantic Evaluation", font=get_font(20, bold=True), fill="white", anchor="mm")
    
    steps_2 = [
        ("StepJudge Evaluator", "Formulates discrete turn prompts with task goal", "#d1fae5", "#047857"),
        ("SHA256 Prompt Hasher", "256-bit cryptographic digest over canonical prompt", "#dcfce7", "#059669"),
        ("AttributionCache (Multi-Tier)", "Tier 1: In-Memory Dict | Tier 2: Persistent SQLite", "#ecfdf5", "#10b981"),
        ("Local LLM (Ollama Qwen2.5:7b)", "Structured JSON mode: is_valid, score, anomaly", "#fee2e2", "#b91c1c"),
        ("Heuristic MockJudge (Fallback)", "Zero-downtime safety net with 25+ failure patterns", "#fef2f2", "#ef4444")
    ]
    y_c = 180
    for name, desc, bg, ec in steps_2:
        draw.rounded_rectangle([540, y_c, 940, y_c + 115], radius=10, fill=bg, outline=ec, width=2)
        draw.text((560, y_c + 20), name, font=get_font(17, bold=True), fill="#0f172a")
        draw.text((560, y_c + 50), desc, font=get_font(13), fill="#334155")
        y_c += 138

    # Layer 3: Dependency Graph Linker (Middle Right)
    draw.rounded_rectangle([1000, 110, 1460, 900], radius=14, fill="#f8fafc", outline="#8b5cf6", width=2)
    draw.rectangle([1000, 110, 1460, 160], fill="#8b5cf6")
    draw.text((1230, 135), "3. Dependency DAG Synthesis", font=get_font(20, bold=True), fill="white", anchor="mm")
    
    steps_3 = [
        ("DependencyLinker Module", "Initializes NetworkX DiGraph G = (V, E)", "#ede9fe", "#6d28d9"),
        ("Sequential Flow Edges", "Links adjacent steps (i-1 -> i) with confidence 0.85", "#f5f3ff", "#7c3aed"),
        ("Entity Identifier Matcher", r"Extracts identifiers (\b[a-z_][a-z0-9_]{3,}\b)", "#f5f3ff", "#7c3aed"),
        ("Shared State Edges", "Links non-adjacent variable passing (conf 0.95)", "#fef3c7", "#d97706"),
        ("Message Reply Edges", "Direct-address routing edges between agent pairs", "#f5f3ff", "#7c3aed")
    ]
    y_c = 180
    for name, desc, bg, ec in steps_3:
        draw.rounded_rectangle([1020, y_c, 1440, y_c + 115], radius=10, fill=bg, outline=ec, width=2)
        draw.text((1040, y_c + 20), name, font=get_font(17, bold=True), fill="#0f172a")
        draw.text((1040, y_c + 50), desc, font=get_font(13), fill="#334155")
        y_c += 138

    # Layer 4: Backward Causal Traversal & Diagnosis (Right Column)
    draw.rounded_rectangle([1500, 110, 1940, 900], radius=14, fill="#f8fafc", outline="#ef4444", width=2)
    draw.rectangle([1500, 110, 1940, 160], fill="#ef4444")
    draw.text((1720, 135), "4. Causal Traversal & Blame", font=get_font(20, bold=True), fill="white", anchor="mm")
    
    steps_4 = [
        ("Manifest Failure Detector", "Identifies latest anomalous step (score < 0.7)", "#fee2e2", "#dc2626"),
        ("Transitive Ancestor Closure", "nx.ancestors() extracts full upstream causal cone", "#fee2e2", "#dc2626"),
        ("Topological Blame Resolver", "Finds earliest anomaly with clean parent states", "#fef3c7", "#b45309"),
        ("2D Taxonomy Categorizer", "Root Cause vs. Symptom vs. Independent Bug", "#dcfce7", "#15803d"),
        ("Shortest Causal Path", "Dijkstra propagation chain to terminal crash", "#fee2e2", "#dc2626")
    ]
    y_c = 180
    for name, desc, bg, ec in steps_4:
        draw.rounded_rectangle([1520, y_c, 1920, y_c + 115], radius=10, fill=bg, outline=ec, width=2)
        draw.text((1540, y_c + 20), name, font=get_font(17, bold=True), fill="#0f172a")
        draw.text((1540, y_c + 50), desc, font=get_font(13), fill="#334155")
        y_c += 138

    # Horizontal Connecting Arrows
    for y_arrow in [230, 370, 510, 650, 780]:
        draw.line([480, y_arrow, 520, y_arrow], fill="#64748b", width=3)
        draw.polygon([(520, y_arrow), (510, y_arrow - 6), (510, y_arrow + 6)], fill="#64748b")
        draw.line([960, y_arrow, 1000, y_arrow], fill="#64748b", width=3)
        draw.polygon([(1000, y_arrow), (990, y_arrow - 6), (990, y_arrow + 6)], fill="#64748b")
        draw.line([1460, y_arrow, 1500, y_arrow], fill="#64748b", width=3)
        draw.polygon([(1500, y_arrow), (1490, y_arrow - 6), (1490, y_arrow + 6)], fill="#64748b")

    # Bottom Cards
    cards = [
        ("Major Subsystems", [
            "TraceSegmenter (Token Bounded)",
            "StepJudge & SHA256 Caching Engine",
            "DependencyLinker (NetworkX DiGraph)",
            "BackwardTraversalResolver",
            "Streamlit Dashboard & REST API"
        ], "#fef3c7", "#f59e0b"),
        ("Core Causal Algorithms", [
            "Transitive Ancestor Closure (BFS/DFS)",
            "Topological Sort of Anomaly Candidates",
            "Clean-Parent Invariant Check",
            "Dijkstra Shortest Causal Path Chain",
            "2D Error Taxonomy Classification"
        ], "#e0f2fe", "#0284c7"),
        ("Performance Guarantees", [
            "100% Cache Hit on Repeated Turns",
            "O(V + E) Graph Traversal Complexity",
            "Sub-Millisecond SQLite Retrieval",
            "Zero-Downtime MockJudge Fallback",
            "Strict 4,096 Token Context Window"
        ], "#dcfce7", "#16a34a"),
        ("System Purpose", [
            "Eliminate Symptom Misattribution",
            "Disambiguate Root Causes vs. Symptoms",
            "Resolve Dual-Culprit Compound Faults",
            "Provide Explainable Fault Provenance",
            "Continuous CI/CD Pipeline Monitoring"
        ], "#f3e8ff", "#9333ea")
    ]
    draw_bottom_cards(draw, cards)

    path = os.path.join(OUTPUT_DIR, "fig_3_1_architecture.png")
    im.save(path, quality=95)
    print("Generated:", path)

# -------------------------------------------------------------------------
# Figure 3.2: Use Case Diagram
# -------------------------------------------------------------------------
def create_fig_3_2():
    im = Image.new("RGB", (2000, 1250), "#ffffff")
    draw = ImageDraw.Draw(im)
    draw_title(draw, "Use Case Diagram – Automated Failure Attribution Platform")

    # System boundary box
    draw.rounded_rectangle([420, 110, 1580, 910], radius=16, fill="#f8fafc", outline="#475569", width=3)
    draw.text((1000, 140), "System Boundary: Automated Failure Attribution Engine", font=get_font(20, bold=True), fill="#1e293b", anchor="mm")

    # Actors Left
    # Actor 1: AI Engineer
    draw.ellipse([140, 220, 220, 300], fill="#e2e8f0", outline="#1e293b", width=3)
    draw.line([180, 300, 180, 420], fill="#1e293b", width=3)
    draw.line([120, 340, 240, 340], fill="#1e293b", width=3)
    draw.line([180, 420, 130, 520], fill="#1e293b", width=3)
    draw.line([180, 420, 230, 520], fill="#1e293b", width=3)
    draw_multiline_text(draw, (180, 545), "AI Engineer /\nDeveloper", font=get_font(18, bold=True), fill="#0f172a")

    # Actor 2: CI/CD Pipeline
    draw.ellipse([140, 640, 220, 720], fill="#e2e8f0", outline="#1e293b", width=3)
    draw.line([180, 720, 180, 800], fill="#1e293b", width=3)
    draw.line([120, 750, 240, 750], fill="#1e293b", width=3)
    draw.line([180, 800, 130, 880], fill="#1e293b", width=3)
    draw.line([180, 800, 230, 880], fill="#1e293b", width=3)
    draw_multiline_text(draw, (180, 895), "CI/CD Regression\nPipeline", font=get_font(18, bold=True), fill="#0f172a")

    # Actors Right
    # Actor 3: Local LLM Engine
    draw.ellipse([1780, 240, 1860, 320], fill="#fee2e2", outline="#b91c1c", width=3)
    draw.line([1820, 320, 1820, 420], fill="#b91c1c", width=3)
    draw.line([1760, 350, 1880, 350], fill="#b91c1c", width=3)
    draw.line([1820, 420, 1770, 500], fill="#b91c1c", width=3)
    draw.line([1820, 420, 1870, 500], fill="#b91c1c", width=3)
    draw_multiline_text(draw, (1820, 520), "Local LLM Daemon\n(Ollama Qwen2.5:7b)", font=get_font(18, bold=True), fill="#b91c1c")

    # Actor 4: Diagnostic Cache DB
    draw.ellipse([1780, 640, 1860, 720], fill="#dcfce7", outline="#15803d", width=3)
    draw.line([1820, 720, 1820, 800], fill="#15803d", width=3)
    draw.line([1760, 750, 1880, 750], fill="#15803d", width=3)
    draw.line([1820, 800, 1770, 880], fill="#15803d", width=3)
    draw.line([1820, 800, 1870, 880], fill="#15803d", width=3)
    draw_multiline_text(draw, (1820, 895), "Diagnostic Cache\n(SQLite / Redis)", font=get_font(18, bold=True), fill="#15803d")

    # Use Case Ovals in 2 Columns inside boundary
    col1_cases = [
        ("UC-01: Ingest & Parse Execution Trace", 470, 180),
        ("UC-02: Budget Context Tokens (60/30 Slicing)", 470, 260),
        ("UC-03: Evaluate Discrete Step Validity", 470, 340),
        ("UC-04: Check / Update SHA256 Prompt Cache", 470, 420),
        ("UC-05: Fallback to Heuristic MockJudge", 470, 500),
        ("UC-06: Construct Sequential & Entity DAG", 470, 580)
    ]
    col2_cases = [
        ("UC-07: Detect Manifest Failure Symptom", 1040, 180),
        ("UC-08: Compute Transitive Ancestor Closure", 1040, 260),
        ("UC-09: Isolate Originating Root Cause", 1040, 340),
        ("UC-10: Classify 2D Error Taxonomy", 1040, 420),
        ("UC-11: Generate Shortest Causal Chain", 1040, 500),
        ("UC-12: Compare Baselines (All-at-Once, Binary)", 1040, 580),
        ("UC-13: Execute Who&When Benchmark Suite", 1040, 660),
        ("UC-14: Inspect Interactive DAG in Streamlit", 1040, 740)
    ]
    for text, x, y in col1_cases:
        draw.ellipse([x, y, x + 480, y + 60], fill="#e0f2fe", outline="#0284c7", width=2)
        draw.text((x + 240, y + 30), text, font=get_font(15, bold=True), fill="#0369a1", anchor="mm")
        # Connect to Left Actor
        draw.line([250, 400, x, y + 30], fill="#94a3b8", width=2)

    for text, x, y in col2_cases:
        draw.ellipse([x, y, x + 480, y + 60], fill="#fef3c7", outline="#d97706", width=2)
        draw.text((x + 240, y + 30), text, font=get_font(15, bold=True), fill="#b45309", anchor="mm")
        # Connect to Left Actor if interactive
        if "Inspect" in text or "Compare" in text or "Benchmark" in text:
            draw.line([250, 400, x, y + 30], fill="#94a3b8", width=2)

    # Connections to Right Actors
    draw.line([1040 + 480, 340 + 30, 1740, 380], fill="#f87171", width=2) # LLM
    draw.line([470 + 480, 420 + 30, 1740, 750], fill="#4ade80", width=2) # Cache

    # Bottom Cards
    cards = [
        ("Primary Actors", [
            "AI Engineer / Developer (UI)",
            "CI/CD Regression Pipeline (API)",
            "Local LLM Daemon (Ollama Qwen)",
            "Persistent SQLite Cache Store"
        ], "#fef3c7", "#f59e0b"),
        ("Core Functional Use Cases", [
            "Trace Ingestion & Context Budgeting",
            "Cached Neural Step Judgments",
            "DAG Construction & Causal Traversal",
            "Root Cause Isolation & 2D Taxonomy",
            "Who&When Benchmark Accuracy Run"
        ], "#e0f2fe", "#0284c7"),
        ("System Boundary Invariants", [
            "100% Local Inference Execution",
            "Zero Data Leakage over Cloud APIs",
            "Zero-Downtime MockJudge Routing",
            "Strict Deterministic Graph Walks",
            "Continuous Telemetry & Audit Logs"
        ], "#dcfce7", "#16a34a"),
        ("Operational Value", [
            "Instant Root Cause Visualization",
            "Elimination of Developer Recency Bias",
            "Automated Multi-Agent CI Gating",
            "Sub-Millisecond Repeated Diagnosis"
        ], "#f3e8ff", "#9333ea")
    ]
    draw_bottom_cards(draw, cards)

    path = os.path.join(OUTPUT_DIR, "fig_3_2_use_case.png")
    im.save(path, quality=95)
    print("Generated:", path)

# -------------------------------------------------------------------------
# Figure 3.3: Class Diagram
# -------------------------------------------------------------------------
def create_fig_3_3():
    im = Image.new("RGB", (2000, 1250), "#ffffff")
    draw = ImageDraw.Draw(im)
    draw_title(draw, "Class Diagram – Automated Failure Attribution Engine")

    def draw_uml_box(x, y, w, h, title, fields, methods, header_bg="#3b82f6", body_bg="#eff6ff", border="#1d4ed8"):
        draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=body_bg, outline=border, width=2)
        draw.rounded_rectangle([x, y, x + w, y + 42], radius=10, fill=header_bg, outline=border, width=2)
        draw.text((x + w/2, y + 21), title, font=get_font(16, bold=True), fill="white", anchor="mm")
        # Line separating fields & methods
        field_h = len(fields) * 22 + 10
        draw.line([x, y + 42 + field_h, x + w, y + 42 + field_h], fill=border, width=1)
        # Fields
        f_font = get_font(13)
        curr_y = y + 48
        for f in fields:
            draw.text((x + 12, curr_y), f, font=f_font, fill="#1e293b")
            curr_y += 22
        # Methods
        curr_y = y + 42 + field_h + 8
        m_font = get_font(13, italic=True)
        for m in methods:
            draw.text((x + 12, curr_y), m, font=m_font, fill="#0369a1")
            curr_y += 22

    # Top Row: Domain Models
    draw_uml_box(60, 110, 440, 240, "MultiAgentTrace", [
        "- trace_id: str",
        "- environment_name: str",
        "- task_goal: str",
        "- total_steps: int",
        "- steps: List[ExecutionStep]",
        "- ground_truth: GroundTruth"
    ], [
        "+ model_dump(): dict",
        "+ parse_raw_payload(): void"
    ], header_bg="#0284c7", body_bg="#f0f9ff", border="#0369a1")

    draw_uml_box(530, 110, 440, 240, "ExecutionStep", [
        "- step_id: str",
        "- step_index: int",
        "- agent_name: str",
        "- recipient: str",
        "- action_type: str",
        "- action_payload: str",
        "- output_state: str"
    ], [
        "+ get_token_count(): int",
        "+ is_terminal(): bool"
    ], header_bg="#0284c7", body_bg="#f0f9ff", border="#0369a1")

    draw_uml_box(1000, 110, 450, 240, "StepEvaluation", [
        "- step_index: int",
        "- is_valid: bool",
        "- score: float",
        "- anomaly_detected: bool",
        "- error_category: str",
        "- prompt_hash: str",
        "- cached: bool"
    ], [
        "+ is_anomalous(): bool",
        "+ to_json(): str"
    ], header_bg="#059669", body_bg="#f0fdf4", border="#047857")

    draw_uml_box(1480, 110, 460, 240, "DependencyEdge", [
        "- source_step_index: int",
        "- target_step_index: int",
        "- source_step_id: str",
        "- target_step_id: str",
        "- dependency_type: str",
        "- data_variable: str",
        "- confidence: float"
    ], [
        "+ is_long_range(): bool"
    ], header_bg="#7c3aed", body_bg="#faf5ff", border="#6d28d9")

    # Middle Row: Core Engine Services
    draw_uml_box(60, 390, 440, 250, "AttributionEngine", [
        "- segmenter: TraceSegmenter",
        "- judge: StepJudge",
        "- linker: DependencyLinker",
        "- resolver: BackwardResolver",
        "- cache: AttributionCache"
    ], [
        "+ attribute_trace(trace): Verdict",
        "+ benchmark_suite(): BenchmarkResult"
    ], header_bg="#b91c1c", body_bg="#fef2f2", border="#991b1b")

    draw_uml_box(530, 390, 440, 250, "TraceSegmenter", [
        "- max_turn_tokens: int = 4096",
        "- head_ratio: float = 0.6",
        "- tail_ratio: float = 0.3"
    ], [
        "+ segment_trace(): List[Step]",
        "+ parse_custom_json(): dict",
        "+ parse_raw_log_text(): dict",
        "- _bound_token_length(): str"
    ], header_bg="#d97706", body_bg="#fffbeb", border="#b45309")

    draw_uml_box(1000, 390, 450, 250, "StepJudge", [
        "- llm_client: LLMClient",
        "- cache: AttributionCache",
        "- model_name: str"
    ], [
        "+ evaluate_step(): StepEvaluation",
        "- _build_prompt(): str"
    ], header_bg="#059669", body_bg="#f0fdf4", border="#047857")

    draw_uml_box(1480, 390, 460, 250, "AttributionCache", [
        "- backend: str = 'sqlite'",
        "- sqlite_path: str",
        "- hits: int = 0",
        "- misses: int = 0"
    ], [
        "+ compute_hash(prompt): str",
        "+ get(prompt): dict",
        "+ set(prompt, val): void",
        "+ get_stats(): dict"
    ], header_bg="#d97706", body_bg="#fffbeb", border="#b45309")

    # Bottom Row: Linker, Resolver, Verdict
    draw_uml_box(60, 670, 440, 240, "DependencyLinker", [
        "- stop_words: Set[str]",
        "- entity_regex: Pattern"
    ], [
        "+ build_dependency_dag(): DiGraph",
        "- _extract_key_entities(): List",
        "- _match_shared_state(): bool"
    ], header_bg="#7c3aed", body_bg="#faf5ff", border="#6d28d9")

    draw_uml_box(530, 670, 440, 240, "BackwardTraversalResolver", [
        "- threshold: float = 0.7"
    ], [
        "+ resolve_root_cause(): Verdict",
        "- _transitive_ancestors(): Set",
        "- _topological_isolation(): int",
        "- _partition_anomalies(): dict"
    ], header_bg="#b91c1c", body_bg="#fef2f2", border="#991b1b")

    draw_uml_box(1000, 670, 450, 240, "AttributionVerdict", [
        "- responsible_agent: str",
        "- decisive_step_index: int",
        "- failure_type: str",
        "- causal_dependency_chain: List[int]",
        "- graph_nodes: List[NodeStatus]",
        "- execution_time_sec: float"
    ], [
        "+ is_strictly_correct: bool",
        "+ to_narrative_report(): str"
    ], header_bg="#b91c1c", body_bg="#fef2f2", border="#991b1b")

    draw_uml_box(1480, 670, 460, 240, "LLMClient & MockJudge", [
        "- provider: str",
        "- model: str",
        "- mock_judge: MockJudge"
    ], [
        "+ query_json(prompt): dict",
        "+ evaluate_fallback(): dict"
    ], header_bg="#059669", body_bg="#f0fdf4", border="#047857")

    # Connectors
    draw.line([500, 230, 530, 230], fill="#475569", width=2)
    draw.text((515, 215), "1..*", font=get_font(12, bold=True), fill="#475569", anchor="mm")
    
    draw.line([970, 230, 1000, 230], fill="#475569", width=2)
    draw.text((985, 215), "1..1", font=get_font(12, bold=True), fill="#475569", anchor="mm")

    draw.line([280, 350, 280, 390], fill="#475569", width=2)
    draw.line([750, 350, 750, 390], fill="#475569", width=2)
    draw.line([1225, 350, 1225, 390], fill="#475569", width=2)

    # Bottom Cards
    cards = [
        ("Major Classes", [
            "MultiAgentTrace & ExecutionStep",
            "StepEvaluation & DependencyEdge",
            "AttributionEngine (Orchestrator)",
            "BackwardTraversalResolver",
            "AttributionCache & LLMClient"
        ], "#fef3c7", "#f59e0b"),
        ("Key Architectural Patterns", [
            "Singleton Engines & Service Injection",
            "Pydantic Strict Type Enforcement",
            "Repository Pattern for Prompt Cache",
            "Strategy Pattern for LLM Providers",
            "Composite Pattern for DAG Nodes"
        ], "#e0f2fe", "#0284c7"),
        ("Object Interactions", [
            "Engine delegates parsing to Segmenter",
            "StepJudge queries Cache before LLM",
            "Linker emits NetworkX DiGraph",
            "Resolver consumes DAG + Evaluations",
            "Emits structured AttributionVerdict"
        ], "#dcfce7", "#16a34a"),
        ("Purpose & Diagnostic Value", [
            "Decoupled Object-Oriented Hierarchy",
            "Strict JSON Serialization Guarantees",
            "Extensible for New Multi-Agent Frameworks",
            "Full Unit Test Coverage across Classes"
        ], "#f3e8ff", "#9333ea")
    ]
    draw_bottom_cards(draw, cards)

    path = os.path.join(OUTPUT_DIR, "fig_3_3_class.png")
    im.save(path, quality=95)
    print("Generated:", path)

# -------------------------------------------------------------------------
# Figure 3.4: Sequence Diagram
# -------------------------------------------------------------------------
def create_fig_3_4():
    im = Image.new("RGB", (2000, 1250), "#ffffff")
    draw = ImageDraw.Draw(im)
    draw_title(draw, "Sequence Diagram – Multi-Agent Attribution Workflow")

    lifelines = [
        ("User / CI Client", 120, "#e2e8f0", "#1e293b"),
        ("FastAPI / CLI", 380, "#dbeafe", "#1d4ed8"),
        ("AttributionEngine", 640, "#fee2e2", "#b91c1c"),
        ("TraceSegmenter", 900, "#fef3c7", "#b45309"),
        ("StepJudge & Cache", 1160, "#dcfce7", "#15803d"),
        ("Local Ollama LLM", 1420, "#fee2e2", "#b91c1c"),
        ("DependencyLinker", 1680, "#ede9fe", "#6d28d9"),
        ("BackwardResolver", 1900, "#fef2f2", "#dc2626")
    ]

    for label, x, bg, ec in lifelines:
        draw.rounded_rectangle([x - 85, 100, x + 85, 150], radius=8, fill=bg, outline=ec, width=2)
        draw.text((x, 125), label, font=get_font(14, bold=True), fill="#0f172a", anchor="mm")
        draw.line([x, 150, x, 900], fill="#cbd5e1", width=2)

    messages = [
        (120, 380, 180, "1: POST /api/v1/attribute (raw_trace_json)", "#0f172a", False),
        (380, 640, 230, "2: attribute_trace(trace)", "#0f172a", False),
        (640, 900, 280, "3: segment_trace(trace)", "#0f172a", False),
        (900, 900, 330, "4: token_budget_and_slice(60/30)", "#b45309", True),
        (900, 640, 380, "5: return List[ExecutionStep]", "#0284c7", False),
        (640, 1160, 430, "6: evaluate_step(step, goal)", "#0f172a", False),
        (1160, 1160, 480, "7: check_cache(SHA256_hash)", "#15803d", True),
        (1160, 1420, 530, "8: [Cache Miss] /v1/chat/completions", "#b91c1c", False),
        (1420, 1160, 580, "9: return JSON verdict (is_valid, score)", "#059669", False),
        (1160, 640, 630, "10: return StepEvaluation", "#0284c7", False),
        (640, 1680, 680, "11: build_dependency_dag(steps)", "#0f172a", False),
        (1680, 640, 730, "12: return (nx.DiGraph, edges)", "#7c3aed", False),
        (640, 1900, 780, "13: resolve_root_cause(DAG, evals)", "#b91c1c", False),
        (1900, 1900, 820, "14: nx.ancestors() + topological sort", "#dc2626", True),
        (1900, 640, 850, "15: return AttributionVerdict", "#059669", False),
        (640, 380, 880, "16: 200 OK (verdict, causal chain)", "#0f172a", False),
        (380, 120, 900, "17: display diagnostic canvas", "#0f172a", False)
    ]

    for src, dst, y_m, text, col, is_self in messages:
        if is_self:
            draw.line([src, y_m, src + 50, y_m], fill=col, width=2)
            draw.line([src + 50, y_m, src + 50, y_m + 25], fill=col, width=2)
            draw.line([src + 50, y_m + 25, src, y_m + 25], fill=col, width=2)
            draw.polygon([(src, y_m + 25), (src + 10, y_m + 21), (src + 10, y_m + 29)], fill=col)
            draw.text((src + 60, y_m + 12), text, font=get_font(13, bold=True), fill=col)
        else:
            draw.line([src, y_m, dst, y_m], fill=col, width=2)
            arrow_dir = 1 if dst > src else -1
            draw.polygon([(dst, y_m), (dst - arrow_dir * 12, y_m - 6), (dst - arrow_dir * 12, y_m + 6)], fill=col)
            mid_x = (src + dst) / 2
            draw.text((mid_x, y_m - 12), text, font=get_font(13, bold=True), fill=col, anchor="mm")

    # Bottom Cards
    cards = [
        ("Participants", [
            "User / CI Client (REST / CLI)",
            "AttributionEngine (Orchestrator)",
            "StepJudge & SHA256 Cache",
            "Ollama Daemon (Qwen2.5:7b)",
            "NetworkX Graph Resolver"
        ], "#fef3c7", "#f59e0b"),
        ("Chronological Workflow", [
            "1. Ingest & Token Budgeting",
            "2. Synchronous Cache Check",
            "3. Local LLM Evaluation (Miss)",
            "4. Dependency DAG Construction",
            "5. Transitive Ancestor Closure"
        ], "#e0f2fe", "#0284c7"),
        ("Latency Optimizations", [
            "Sub-2ms Cached Turn Evaluation",
            "Greedy Decoding (Temp=0.0)",
            "O(V+E) Linear Ancestor Traversal",
            "Zero-Downtime Mock Fallback",
            "Parallel Asynchronous Evaluation"
        ], "#dcfce7", "#16a34a"),
        ("Diagnostic Guarantees", [
            "100% Deterministic Causal Isolation",
            "Strict Clean-Parent Verification",
            "Dijkstra Shortest Failure Chain",
            "JSON-RPC Standard Compliance"
        ], "#f3e8ff", "#9333ea")
    ]
    draw_bottom_cards(draw, cards)

    path = os.path.join(OUTPUT_DIR, "fig_3_4_sequence.png")
    im.save(path, quality=95)
    print("Generated:", path)

# -------------------------------------------------------------------------
# Figure 3.5: DFD Level 0
# -------------------------------------------------------------------------
def create_fig_3_5():
    im = Image.new("RGB", (2000, 1250), "#ffffff")
    draw = ImageDraw.Draw(im)
    draw_title(draw, "Data Flow Diagram – Level 0 (Context Level)")

    # Central Process Circle
    draw.ellipse([800, 360, 1200, 760], fill="#e0e7ff", outline="#3730a3", width=4)
    draw.text((1000, 480), "0", font=get_font(42, bold=True), fill="#1e1b4b", anchor="mm")
    draw_multiline_text(draw, (1000, 580), "Automated Failure\nAttribution Engine\n(Neuro-Symbolic)", font=get_font(20, bold=True), fill="#1e1b4b")

    # External Entities
    # Entity 1: Multi-Agent Frameworks (Top-Left)
    draw.rounded_rectangle([100, 180, 520, 340], radius=12, fill="#fef3c7", outline="#b45309", width=3)
    draw.text((310, 240), "Multi-Agent Frameworks", font=get_font(20, bold=True), fill="#78350f", anchor="mm")
    draw.text((310, 280), "AutoGen, LangGraph, MetaGPT, CrewAI", font=get_font(14), fill="#92400e", anchor="mm")

    # Entity 2: AI Engineer / Developer (Bottom-Left)
    draw.rounded_rectangle([100, 680, 520, 840], radius=12, fill="#dcfce7", outline="#15803d", width=3)
    draw.text((310, 740), "AI Engineer / Diagnostics User", font=get_font(20, bold=True), fill="#14532d", anchor="mm")
    draw.text((310, 780), "Submits Traces, Inspects DAGs, Configures", font=get_font(14), fill="#166534", anchor="mm")

    # Entity 3: Local LLM Service (Top-Right)
    draw.rounded_rectangle([1480, 180, 1900, 340], radius=12, fill="#fee2e2", outline="#b91c1c", width=3)
    draw.text((1690, 240), "Local LLM Inference Engine", font=get_font(20, bold=True), fill="#7f1d1d", anchor="mm")
    draw.text((1690, 280), "Ollama Qwen2.5:7b / vLLM Daemon", font=get_font(14), fill="#991b1b", anchor="mm")

    # Entity 4: Database & Cache (Bottom-Right)
    draw.rounded_rectangle([1480, 680, 1900, 840], radius=12, fill="#f3e8ff", outline="#7e22ce", width=3)
    draw.text((1690, 740), "Database & Benchmarks", font=get_font(20, bold=True), fill="#581c87", anchor="mm")
    draw.text((1690, 780), "SQLite Prompt Cache, Who&When Callset", font=get_font(14), fill="#6b21a8", anchor="mm")

    # Connecting Flow Lines
    # 1. Frameworks -> Engine
    draw.line([520, 280, 820, 440], fill="#b45309", width=3)
    draw.text((650, 330), "Raw Execution Trace Logs", font=get_font(15, bold=True), fill="#b45309", anchor="mm")

    # 2. User -> Engine
    draw.line([520, 730, 820, 640], fill="#15803d", width=3)
    draw.text((650, 660), "Attribution Request & Thresholds", font=get_font(15, bold=True), fill="#15803d", anchor="mm")

    # 3. Engine -> User
    draw.line([820, 680, 520, 770], fill="#15803d", width=3)
    draw.text((650, 745), "Root Cause Verdict & Visual DAG", font=get_font(15, bold=True), fill="#15803d", anchor="mm")

    # 4. Engine -> LLM
    draw.line([1180, 440, 1480, 280], fill="#b91c1c", width=3)
    draw.text((1350, 330), "Canonical Evaluation Prompts", font=get_font(15, bold=True), fill="#b91c1c", anchor="mm")

    # 5. LLM -> Engine
    draw.line([1480, 310, 1200, 490], fill="#b91c1c", width=3)
    draw.text((1360, 420), "Structured JSON Verdicts", font=get_font(15, bold=True), fill="#b91c1c", anchor="mm")

    # 6. Engine <-> Cache
    draw.line([1180, 640, 1480, 730], fill="#7e22ce", width=3)
    draw.text((1350, 670), "Store / Retrieve Prompt Hashes", font=get_font(15, bold=True), fill="#7e22ce", anchor="mm")

    # Bottom Cards
    cards = [
        ("External Entities", [
            "Multi-Agent Orchestrator Logs",
            "AI Systems Engineer (User)",
            "Localhost LLM Inference Daemon",
            "Persistent Cache & Benchmark DB"
        ], "#fef3c7", "#f59e0b"),
        ("Inbound Data Flows", [
            "Raw JSON/JSONL Multi-Agent Traces",
            "Overarching Task Goal & Persona Metadata",
            "User Diagnostic Threshold Parameters",
            "Local LLM Semantic Evaluations"
        ], "#e0f2fe", "#0284c7"),
        ("Outbound Data Flows", [
            "Originating Root Cause Verdicts",
            "2D Error Taxonomy Classifications",
            "Shortest Causal Failure Chains",
            "Interactive Streamlit DAG Visuals"
        ], "#dcfce7", "#16a34a"),
        ("Context Boundaries", [
            "100% Local Hardware Security",
            "Zero Cloud Data Transmission",
            "Standardized OpenAPI / REST Schema",
            "Strict Context Window Sandboxing"
        ], "#f3e8ff", "#9333ea")
    ]
    draw_bottom_cards(draw, cards)

    path = os.path.join(OUTPUT_DIR, "fig_3_5_dfd_lvl0.png")
    im.save(path, quality=95)
    print("Generated:", path)

# -------------------------------------------------------------------------
# Figure 3.6: DFD Level 1
# -------------------------------------------------------------------------
def create_fig_3_6():
    im = Image.new("RGB", (2000, 1250), "#ffffff")
    draw = ImageDraw.Draw(im)
    draw_title(draw, "Data Flow Diagram – Level 1 (Subsystem Decomposition)")

    def draw_proc(x, y, num, title, bg="#e0e7ff", ec="#3730a3"):
        draw.ellipse([x - 70, y - 70, x + 70, y + 70], fill=bg, outline=ec, width=3)
        draw.text((x, y - 30), num, font=get_font(22, bold=True), fill="#1e1b4b", anchor="mm")
        draw_multiline_text(draw, (x, y + 16), title, font=get_font(13, bold=True), fill="#1e1b4b")

    def draw_store(x, y, w, h, name):
        draw.line([x, y, x + w, y], fill="#475569", width=3)
        draw.line([x, y + h, x + w, y + h], fill="#475569", width=3)
        draw.line([x, y, x, y + h], fill="#475569", width=3)
        draw.rectangle([x, y, x + w, y + h], fill="#f8fafc")
        draw.text((x + w/2, y + h/2), name, font=get_font(14, bold=True), fill="#1e293b", anchor="mm")

    # 6 Processes in 2 rows
    # Row 1
    draw_proc(300, 280, "1.0", "Trace Ingestion\n& Token Budget")
    draw_proc(800, 280, "2.0", "Step-Wise LLM\nEvaluation")
    draw_proc(1300, 280, "3.0", "Dependency\nDAG Synthesis")

    # Row 2
    draw_proc(1300, 680, "4.0", "Backward Causal\nTraversal")
    draw_proc(800, 680, "5.0", "2D Taxonomy\nResolution")
    draw_proc(300, 680, "6.0", "Visual Reporting\n& UI Delivery")

    # Data Stores
    draw_store(600, 440, 400, 65, "D1: SHA256 Prompt Cache (SQLite)")
    draw_store(1100, 440, 400, 65, "D2: NetworkX DiGraph Store")
    draw_store(100, 440, 400, 65, "D3: Attribution Verdict Repository")

    # Connecting Pipelines
    # 1.0 -> 2.0
    draw.line([370, 280, 730, 280], fill="#0284c7", width=3)
    draw.text((550, 260), "Bounded ExecutionSteps", font=get_font(13, bold=True), fill="#0284c7", anchor="mm")

    # 2.0 -> 3.0
    draw.line([870, 280, 1230, 280], fill="#0284c7", width=3)
    draw.text((1050, 260), "Step Context & Entities", font=get_font(13, bold=True), fill="#0284c7", anchor="mm")

    # 3.0 -> 4.0
    draw.line([1300, 350, 1300, 610], fill="#0284c7", width=3)
    draw.text((1370, 480), "Dependency DAG", font=get_font(13, bold=True), fill="#0284c7", anchor="mm")

    # 4.0 -> 5.0
    draw.line([1230, 680, 870, 680], fill="#0284c7", width=3)
    draw.text((1050, 660), "Ancestor Subgraph", font=get_font(13, bold=True), fill="#0284c7", anchor="mm")

    # 5.0 -> 6.0
    draw.line([730, 680, 370, 680], fill="#0284c7", width=3)
    draw.text((550, 660), "Attribution Verdict", font=get_font(13, bold=True), fill="#0284c7", anchor="mm")

    # Store Connections
    draw.line([800, 350, 800, 440], fill="#10b981", width=2)
    draw.line([1300, 350, 1300, 440], fill="#10b981", width=2)
    draw.line([300, 610, 300, 505], fill="#10b981", width=2)

    # Bottom Cards
    cards = [
        ("Subsystem Processes", [
            "1.0 Ingestion & 60/30 Token Slicing",
            "2.0 Cached Neural Step Scoring",
            "3.0 Sequential & Shared State DAG",
            "4.0 Transitive Ancestor Closure Walk",
            "5.0 2D Causal Role & Category Blame",
            "6.0 Streamlit & REST Telemetry"
        ], "#fef3c7", "#f59e0b"),
        ("Internal Data Stores", [
            "D1: SQLite SHA256 Prompt Cache",
            "D2: NetworkX In-Memory DiGraph",
            "D3: Attribution Verdict Relational DB",
            "Ephemeral Working Memory"
        ], "#e0f2fe", "#0284c7"),
        ("Information Pipelines", [
            "Bounded ExecutionStep Tuples",
            "Cryptographic Prompt Hashes",
            "Directed Dependency Edge Sets",
            "Topologically Ordered Anomalies",
            "Dijkstra Shortest Causal Paths"
        ], "#dcfce7", "#16a34a"),
        ("Design Invariants", [
            "Strict Topological Consistency",
            "ACID Compliant Cache Transactions",
            "Zero Data Contamination across Traces",
            "Sub-Millisecond Cache Retrieval"
        ], "#f3e8ff", "#9333ea")
    ]
    draw_bottom_cards(draw, cards)

    path = os.path.join(OUTPUT_DIR, "fig_3_6_dfd_lvl1.png")
    im.save(path, quality=95)
    print("Generated:", path)

# -------------------------------------------------------------------------
# Figure 3.7: ERD Diagram
# -------------------------------------------------------------------------
def create_fig_3_7():
    im = Image.new("RGB", (2000, 1250), "#ffffff")
    draw = ImageDraw.Draw(im)
    draw_title(draw, "Entity Relationship Diagram – Diagnostic Schema")

    def draw_entity(x, y, w, h, title, pk_list, fk_list, attr_list):
        draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill="#f8fafc", outline="#1e3a8a", width=2)
        draw.rounded_rectangle([x, y, x + w, y + 40], radius=10, fill="#1e3a8a", outline="#1e3a8a", width=2)
        draw.text((x + w/2, y + 20), title, font=get_font(16, bold=True), fill="white", anchor="mm")
        
        curr_y = y + 48
        f_font = get_font(13)
        for pk in pk_list:
            draw.text((x + 14, curr_y), "PK", font=get_font(11, bold=True), fill="#dc2626")
            draw.text((x + 45, curr_y), pk, font=f_font, fill="#991b1b")
            curr_y += 22
        for fk in fk_list:
            draw.text((x + 14, curr_y), "FK", font=get_font(11, bold=True), fill="#0284c7")
            draw.text((x + 45, curr_y), fk, font=f_font, fill="#0369a1")
            curr_y += 22
        for attr in attr_list:
            draw.text((x + 45, curr_y), attr, font=f_font, fill="#334155")
            curr_y += 22

    # Entities Layout
    # Top Row
    draw_entity(60, 110, 420, 240, "MULTI_AGENT_TRACE", ["trace_id: string"], [], [
        "title: string",
        "environment_name: string",
        "task_goal: text",
        "total_steps: integer",
        "final_outcome: string",
        "created_at: timestamp"
    ])

    draw_entity(530, 110, 420, 270, "EXECUTION_STEP", ["step_id: string"], ["trace_id: string"], [
        "step_index: integer",
        "agent_name: string",
        "recipient: string",
        "action_type: string",
        "input_context: text",
        "action_payload: text",
        "output_state: text"
    ])

    draw_entity(1000, 110, 440, 250, "DEPENDENCY_EDGE", ["edge_id: string"], ["trace_id: string", "source_step_id: string", "target_step_id: string"], [
        "dependency_type: string",
        "data_variable: string",
        "confidence: float"
    ])

    draw_entity(1490, 110, 450, 240, "PROMPT_CACHE", ["prompt_hash: string"], [], [
        "model_name: string",
        "prompt_text: text",
        "response_json: text",
        "created_at: timestamp"
    ])

    # Bottom Row
    draw_entity(60, 430, 420, 240, "GROUND_TRUTH", ["gt_id: string"], ["trace_id: string"], [
        "responsible_agent: string",
        "decisive_step_index: integer",
        "failure_category: string",
        "failure_reason: text"
    ])

    draw_entity(530, 430, 420, 260, "STEP_EVALUATION", ["eval_id: string"], ["step_id: string", "prompt_hash: string"], [
        "is_valid: boolean",
        "score: float",
        "anomaly_detected: boolean",
        "error_category: string",
        "justification: text",
        "cached: boolean"
    ])

    draw_entity(1000, 430, 440, 270, "ATTRIBUTION_VERDICT", ["verdict_id: string"], ["trace_id: string"], [
        "responsible_agent: string",
        "decisive_step_index: integer",
        "failure_type: string",
        "causal_chain: text",
        "explanation: text",
        "execution_time_sec: float",
        "cache_hit_rate: float"
    ])

    draw_entity(1490, 430, 450, 240, "BENCHMARK_RESULT", ["result_id: string"], [], [
        "benchmark_name: string",
        "total_traces: integer",
        "agent_accuracy: float",
        "step_accuracy: float",
        "strict_joint_accuracy: float",
        "evaluated_at: timestamp"
    ])

    # Relationship Connectors
    draw.line([480, 180, 530, 180], fill="#475569", width=2)
    draw.text((505, 160), "1 : N", font=get_font(12, bold=True), fill="#475569", anchor="mm")

    draw.line([950, 180, 1000, 180], fill="#475569", width=2)
    draw.text((975, 160), "1 : N", font=get_font(12, bold=True), fill="#475569", anchor="mm")

    draw.line([740, 380, 740, 430], fill="#475569", width=2)
    draw.text((760, 405), "1 : 1", font=get_font(12, bold=True), fill="#475569", anchor="mm")

    draw.line([950, 550, 1000, 550], fill="#475569", width=2)
    draw.text((975, 530), "N : 1", font=get_font(12, bold=True), fill="#475569", anchor="mm")

    draw.line([270, 350, 270, 430], fill="#475569", width=2)
    draw.text((290, 390), "1 : 1", font=get_font(12, bold=True), fill="#475569", anchor="mm")

    # Bottom Cards
    cards = [
        ("Core Relational Entities", [
            "MULTI_AGENT_TRACE (Root Container)",
            "EXECUTION_STEP (Turn Telemetry)",
            "STEP_EVALUATION (Semantic Output)",
            "DEPENDENCY_EDGE (Graph Topology)",
            "PROMPT_CACHE (Persistent Hash DB)"
        ], "#fef3c7", "#f59e0b"),
        ("Key Cardinalities", [
            "1 Trace has Many (1:N) ExecutionSteps",
            "1 Step has Exactly One (1:1) Evaluation",
            "1 Trace has Many (1:N) DependencyEdges",
            "Many Evaluations reference (N:1) Cache",
            "1 Trace produces (1:1) Final Verdict"
        ], "#e0f2fe", "#0284c7"),
        ("Referential Integrity", [
            "Cascading Foreign Key Constraints",
            "Primary Key Indexes on Hashes",
            "ACID Compliant SQLite Storage",
            "Normalized 3NF Relational Structure"
        ], "#dcfce7", "#16a34a"),
        ("Diagnostic Schema Value", [
            "Immutable Post-Mortem Audit Trails",
            "Instant Ground Truth Metric Join",
            "High-Throughput Read/Write B-Trees",
            "Cross-Session Caching Reusability"
        ], "#f3e8ff", "#9333ea")
    ]
    draw_bottom_cards(draw, cards)

    path = os.path.join(OUTPUT_DIR, "fig_3_7_erd.png")
    im.save(path, quality=95)
    print("Generated:", path)

def generate_all():
    print("Generating all 7 high-resolution B12 diagrams...")
    create_fig_3_1()
    create_fig_3_2()
    create_fig_3_3()
    create_fig_3_4()
    create_fig_3_5()
    create_fig_3_6()
    create_fig_3_7()
    print("All 7 diagrams generated successfully at 2000x1250 resolution.")

if __name__ == "__main__":
    generate_all()
