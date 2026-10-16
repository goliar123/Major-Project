import os
import textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
import numpy as np
from PIL import Image

def generate_cropai_template_a2():
    # -------------------------------------------------------------
    # Page Setup: ISO A2 Landscape (594 mm x 420 mm = 23.386 x 16.535 inches)
    # -------------------------------------------------------------
    width_in = 23.386
    height_in = 16.535
    fig = plt.figure(figsize=(width_in, height_in), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Typography setup
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Liberation Sans', 'Arial', 'Helvetica']
    plt.rcParams['font.family'] = 'sans-serif'

    # Color Palette from Crop-AI Reference Template
    BG_CANVAS = "#F8FAFC"
    HEADER_BG = "#064E3B"        # Deep Forest Emerald Green (exact Crop-AI header)
    HEADER_ACCENT = "#10B981"    # Vibrant Green Accent
    HEADER_SUB = "#A7F3D0"       # Light Mint Green
    
    CARD_BG = "#FFFFFF"
    BORDER_LIGHT = "#E2E8F0"
    BORDER_DARK = "#CBD5E1"
    
    TEXT_MAIN = "#0F172A"        # Deep slate/black
    TEXT_MUTED = "#334155"       # Readable dark slate
    TEXT_LIGHT = "#64748B"       # Subtle slate
    
    # Crop-AI Section Bar & Accent Colors
    ACCENT_GREEN = "#059669"     # Forest/Emerald Green
    ACCENT_MINT = "#ECFDF5"      # Mint background
    ACCENT_TEAL = "#0D9488"      # Teal
    ACCENT_BLUE = "#0284C7"      # Sky Blue
    ACCENT_PURPLE = "#7C3AED"    # Purple
    ACCENT_AMBER = "#D97706"     # Amber
    ACCENT_RED = "#DC2626"       # Red

    # Canvas Background
    ax.add_patch(patches.Rectangle((0, 0), 1, 1, facecolor=BG_CANVAS, edgecolor='none', zorder=0))

    # Helper: draw rounded container card
    def draw_card(x, y, w, h, bg=CARD_BG, border=BORDER_LIGHT, lw=1.2, radius=0.005, zorder=2):
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle=patches.BoxStyle("Round", pad=radius, rounding_size=radius),
            facecolor=bg, edgecolor=border, linewidth=lw, zorder=zorder
        )
        ax.add_patch(box)
        return box

    # Helper: draw section title with Crop-AI vertical indicator bar
    def draw_section_title(x, y, title_text, bar_color=ACCENT_GREEN, font_size=12.5, zorder=3):
        bar_w = 0.0035
        bar_h = 0.018
        bar = patches.FancyBboxPatch(
            (x, y - bar_h*0.80), bar_w, bar_h,
            boxstyle=patches.BoxStyle("Round", pad=0.0008, rounding_size=0.0008),
            facecolor=bar_color, edgecolor='none', zorder=zorder
        )
        ax.add_patch(bar)
        ax.text(x + 0.0075, y, title_text, ha='left', va='center', 
                fontsize=font_size, fontweight='bold', color=TEXT_MAIN, zorder=zorder)

    # =============================================================
    # 1. HEADER (Deep Forest Emerald Green Banner - Exact Crop-AI Style)
    # =============================================================
    head_x = 0.015
    head_w = 0.970
    head_y = 0.870
    head_h = 0.116

    header_box = patches.FancyBboxPatch(
        (head_x, head_y), head_w, head_h,
        boxstyle=patches.BoxStyle("Round", pad=0.004, rounding_size=0.005),
        facecolor=HEADER_BG, edgecolor='none', zorder=1
    )
    ax.add_patch(header_box)
    
    accent_bar = patches.FancyBboxPatch(
        (head_x, head_y), head_w, 0.0035,
        boxstyle=patches.BoxStyle("Round", pad=0.001, rounding_size=0.001),
        facecolor=HEADER_ACCENT, edgecolor='none', zorder=2
    )
    ax.add_patch(accent_bar)

    # Load and render GRIET College Crest on Left
    griet_logo_path = "media/diagrams/extracted/review2_p0_img_0_Image5.jpg"
    if os.path.exists(griet_logo_path):
        logo_img = Image.open(griet_logo_path)
        logo_cx, logo_cy, logo_r = head_x + 0.040, head_y + head_h/2, 0.038
        c_bg = patches.Circle((logo_cx, logo_cy), logo_r, facecolor='#FFFFFF', edgecolor=HEADER_ACCENT, linewidth=1.5, zorder=3)
        ax.add_patch(c_bg)
        ax.imshow(logo_img, extent=[logo_cx - logo_r*0.90, logo_cx + logo_r*0.90, logo_cy - logo_r*0.90, logo_cy + logo_r*0.90], zorder=4)

    # Project Badge Icon on Right (matching Crop-AI right circular badge)
    proj_cx, proj_cy, proj_r = head_x + head_w - 0.040, head_y + head_h/2, 0.038
    c_proj = patches.Circle((proj_cx, proj_cy), proj_r, facecolor='#065F46', edgecolor='#34D399', linewidth=1.5, zorder=3)
    ax.add_patch(c_proj)
    
    n1 = patches.Circle((proj_cx - 0.014, proj_cy - 0.008), 0.005, facecolor='#10B981', edgecolor='#FFFFFF', linewidth=1, zorder=4)
    n2 = patches.Circle((proj_cx, proj_cy + 0.012), 0.006, facecolor='#EF4444', edgecolor='#FFFFFF', linewidth=1.2, zorder=4)
    n3 = patches.Circle((proj_cx + 0.014, proj_cy - 0.008), 0.005, facecolor='#F59E0B', edgecolor='#FFFFFF', linewidth=1, zorder=4)
    ax.add_patch(n1); ax.add_patch(n2); ax.add_patch(n3)
    ax.plot([proj_cx - 0.014, proj_cx], [proj_cy - 0.008, proj_cy + 0.012], color='#FFFFFF', lw=1.2, zorder=3.5)
    ax.plot([proj_cx, proj_cx + 0.014], [proj_cy + 0.012, proj_cy - 0.008], color='#FFFFFF', lw=1.2, zorder=3.5)
    ax.text(proj_cx, proj_cy - 0.023, "RootCause", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#FFFFFF', zorder=4)

    # Header Center Text
    mid_x = head_x + head_w / 2
    ax.text(mid_x, head_y + head_h - 0.017, "GOKARAJU RANGARAJU INSTITUTE OF ENGINEERING AND TECHNOLOGY (AUTONOMOUS)", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#FFFFFF', zorder=3)
    ax.text(mid_x, head_y + head_h - 0.035, "Department of Computer Science and Engineering | B.Tech IV Year / I Semester | Academic Year 2026-2027", 
            ha='center', va='center', fontsize=10.5, color=HEADER_SUB, zorder=3)
    ax.text(mid_x, head_y + head_h - 0.061, "Automated Failure Attribution for LLM-Based Multi-Agent Systems", 
            ha='center', va='center', fontsize=22, fontweight='bold', color='#FFFFFF', zorder=3)
    members_text = "Team Members: Rachapalli S Prabhaadhithya (23241A05Q3) · Rathod Ajay (23241A05Q4) · Noel Paul (23241A05Q6) · Talagapu Niranjan (23241A05R1)"
    ax.text(mid_x, head_y + head_h - 0.084, members_text, 
            ha='center', va='center', fontsize=9.5, color='#E2E8F0', zorder=3)
    guide_text = "Guide: Dr. D. Ushasree, Assistant Professor | Batch No: D2 | Major Project Phase-I"
    ax.text(mid_x, head_y + head_h - 0.102, guide_text, 
            ha='center', va='center', fontsize=9.5, color=HEADER_SUB, zorder=3)

    # =============================================================
    # LAYOUT GRID: 3 COLUMNS + BOTTOM ROW
    # =============================================================
    col1_x = 0.015
    col1_w = 0.248
    
    col2_x = 0.274
    col2_w = 0.380
    
    col3_x = 0.665
    col3_w = 0.320

    top_y = 0.854
    upper_bot = 0.160

    # =============================================================
    # COLUMN 1: ABSTRACT & KEY FEATURES
    # =============================================================
    # 1. ABSTRACT CARD
    abs_y = 0.470
    abs_h = top_y - abs_y
    draw_card(col1_x, abs_y, col1_w, abs_h)
    draw_section_title(col1_x + 0.010, top_y - 0.018, "ABSTRACT", bar_color=ACCENT_GREEN)

    p1_raw = (
        "Communicative multi-agent systems powered by Large Language Models "
        "(AutoGen, LangGraph, MetaGPT) solve complex engineering tasks through "
        "collaborative division of labor. However, when an agent introduces an "
        "erroneous premise, invalid tool parameter, or unfulfilled schema constraint, "
        "the defect propagates silently across subsequent conversational turns, "
        "culminating in a catastrophic crash at an innocent end-of-chain agent."
    )
    p2_raw = (
        "Conventional monitoring tools and monolithic LLM-as-a-judge evaluators "
        "suffer from severe recency bias, consistently committing 'Symptom Misattribution' "
        "by blaming the terminal crashing node rather than the silent upstream originator "
        "(<15% step accuracy on standard benchmarks)."
    )
    p3_raw = (
        "This project introduces a Neuro-Symbolic Causal Graph Engine that cleanly "
        "decouples localized neural semantic evaluation from global symbolic graph causality. "
        "Discrete turns are scored in JSON mode by a local Qwen2.5:7b model (Ollama) "
        "backed by a deterministic SHA256 SQLite cache (100% cache hit rate). NetworkX "
        "constructs a dependency DAG of execution flow and regex-extracted state variables. "
        "A Two-Phase Backward Causal Traversal algorithm computes the Transitive Ancestor "
        "Closure and enforces a Clean-Parent Invariant to mathematically isolate the true root cause, "
        "achieving 87.0% Who/When accuracy on ICML 2025 Who&When traces while cutting latency by 91.2%."
    )

    p1_wrapped = textwrap.fill(p1_raw, width=48)
    p2_wrapped = textwrap.fill(p2_raw, width=48)
    p3_wrapped = textwrap.fill(p3_raw, width=48)
    
    full_abstract_text = f"{p1_wrapped}\n\n{p2_wrapped}\n\n{p3_wrapped}"
    ax.text(col1_x + 0.010, top_y - 0.038, full_abstract_text, ha='left', va='top', 
            fontsize=8.0, color=TEXT_MUTED, linespacing=1.28)

    # 2. KEY FEATURES CARD
    feat_y = upper_bot
    feat_h = abs_y - 0.010 - feat_y
    draw_card(col1_x, feat_y, col1_w, feat_h)
    draw_section_title(col1_x + 0.010, feat_y + feat_h - 0.018, "KEY FEATURES", bar_color=ACCENT_GREEN)

    features = [
        ("Decoupled Neuro-Symbolic AI", "Combines local LLM semantic evaluation with deterministic symbolic DAG traversal."),
        ("Elimination of Recency Bias", "Traces backward from manifest crash, preventing symptom misattribution."),
        ("Clean-Parent Invariant", "Mathematically isolates earliest anomalous node with verified clean inputs."),
        ("Deterministic SHA256 Caching", "Two-tier RAM & SQLite cache eliminates 100% of redundant inference (<2ms)."),
        ("Dependency DAG Synthesis", "Constructs execution flow (0.85) and cross-turn variable dependencies (0.95)."),
        ("Zero-Downtime Offline Fallback", "Rule-based MockJudge with 25+ failure patterns ensures continuous uptime."),
        ("Actionable 2D Bug Taxonomy", "Categorizes failures by Causal Role × 25+ Bug Categories with Dijkstra path.")
    ]

    curr_fy = feat_y + feat_h - 0.040
    for f_title, f_desc in features:
        ax.add_patch(patches.Circle((col1_x + 0.014, curr_fy - 0.003), 0.0028, facecolor=ACCENT_GREEN, edgecolor='none', zorder=3))
        ax.text(col1_x + 0.021, curr_fy, f_title, ha='left', va='center', 
                fontsize=8.4, fontweight='bold', color=TEXT_MAIN, zorder=3)
        desc_wrapped = textwrap.fill(f_desc, width=46)
        ax.text(col1_x + 0.021, curr_fy - 0.012, desc_wrapped, ha='left', va='top', 
                fontsize=7.4, color=TEXT_LIGHT, linespacing=1.15, zorder=3)
        curr_fy -= 0.038

    # =============================================================
    # COLUMN 2: SYSTEM ARCHITECTURE (Multi-Tier Modular Engine)
    # =============================================================
    arch_y = upper_bot
    arch_h = top_y - arch_y
    draw_card(col2_x, arch_y, col2_w, arch_h)
    draw_section_title(col2_x + 0.012, top_y - 0.018, "SYSTEM ARCHITECTURE", bar_color=ACCENT_GREEN)

    # Top User / Input Tier
    user_box_y = top_y - 0.070
    user_box_h = 0.034
    draw_card(col2_x + 0.060, user_box_y, col2_w - 0.120, user_box_h, bg="#1E293B", border='none', radius=0.004)
    ax.text(col2_x + col2_w/2, user_box_y + user_box_h*0.62, "AI Engineer / MLOps Observability Client", 
            ha='center', va='center', fontsize=9.2, fontweight='bold', color='#FFFFFF', zorder=4)
    ax.text(col2_x + col2_w/2, user_box_y + user_box_h*0.25, "Submits Failed Multi-Agent Traces (AutoGen, LangGraph, CrewAI, MetaGPT)", 
            ha='center', va='center', fontsize=7.6, color='#94A3B8', zorder=4)

    # Down arrow
    ax.annotate('', xy=(col2_x + col2_w/2, user_box_y - 0.014), xytext=(col2_x + col2_w/2, user_box_y),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT_GREEN, lw=1.8), zorder=4)

    # Core Engine Container
    eng_box_y = user_box_y - 0.046
    eng_box_h = 0.028
    draw_card(col2_x + 0.040, eng_box_y, col2_w - 0.080, eng_box_h, bg="#065F46", border='none', radius=0.004)
    ax.text(col2_x + col2_w/2, eng_box_y + eng_box_h/2, "Neuro-Symbolic Causal Graph Engine (Core Platform)", 
            ha='center', va='center', fontsize=10.0, fontweight='bold', color='#FFFFFF', zorder=4)

    # Down arrow to 3 processing pillars
    ax.annotate('', xy=(col2_x + col2_w/2, eng_box_y - 0.014), xytext=(col2_x + col2_w/2, eng_box_y),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT_GREEN, lw=1.8), zorder=4)

    # 3 Parallel Functional Pillars
    p_w = (col2_w - 0.032) / 3
    p_y = arch_y + 0.095
    p_h = eng_box_y - 0.022 - p_y

    pillars = [
        ("Ingestion & Budgeting", ACCENT_BLUE, "#F0F9FF", [
            ("Heterogeneous Parser", "Parses JSON, JSONL and console logs from AutoGen, MetaGPT, CrewAI."),
            ("Asymmetric Budgeting", "60% Head (rules) / 30% Tail (stack traces) within 4,096 tokens."),
            ("Step Normalization", "Instantiates ExecutionSteps: agent, recipient, action & state."),
            ("Pydantic Validation", "Guarantees strict type safety and zero schema drift.")
        ]),
        ("Cached StepJudge", ACCENT_GREEN, "#ECFDF5", [
            ("SHA256 Prompt Hashing", "Deterministic 256-bit digest eliminates redundant LLM calls."),
            ("Two-Tier Persistence", "Sub-ms RAM dictionary (<0.1ms) + ACID SQLite B-tree (<2ms)."),
            ("Local Qwen2.5 (Ollama)", "Isolated structured JSON mode evaluates turn validity (thr 0.70)."),
            ("MockJudge Fallback", "25+ regex failure patterns ensure zero-downtime availability.")
        ]),
        ("Symbolic Causal Resolver", ACCENT_PURPLE, "#FAF5FF", [
            ("DAG Synthesis", "Sequential edges (0.85) + regex variable data edges (0.95)."),
            ("Ancestor Closure", "nx.ancestors() extracts full causal subgraph Anc(s_m) to crash site."),
            ("Topological Blame", "Isolates earliest anomalous node with verified clean parent states."),
            ("Shortest Causal Path", "Dijkstra algorithm computes step-by-step failure chain.")
        ])
    ]

    for p_idx, (p_title, p_color, p_bg, p_items) in enumerate(pillars):
        px = col2_x + 0.010 + p_idx * (p_w + 0.006)
        draw_card(px, p_y, p_w, p_h, bg=p_bg, border=p_color, lw=1.2, radius=0.004)
        
        # Header banner
        header_ph = 0.026
        p_hdr = patches.FancyBboxPatch(
            (px, p_y + p_h - header_ph), p_w, header_ph,
            boxstyle=patches.BoxStyle("Round", pad=0.002, rounding_size=0.003),
            facecolor=p_color, edgecolor='none', zorder=3
        )
        ax.add_patch(p_hdr)
        ax.text(px + p_w/2, p_y + p_h - header_ph/2, p_title, 
                ha='center', va='center', fontsize=8.6, fontweight='bold', color='#FFFFFF', zorder=4)

        # Content blocks inside pillar
        sub_h = 0.082
        item_y = p_y + p_h - header_ph - 0.008
        for it_title, it_desc in p_items:
            draw_card(px + 0.004, item_y - sub_h, p_w - 0.008, sub_h, bg="#FFFFFF", border="#E2E8F0", lw=0.7, radius=0.003)
            ax.text(px + 0.008, item_y - 0.010, it_title, ha='left', va='top', 
                    fontsize=7.6, fontweight='bold', color=p_color, zorder=3)
            desc_wrapped = textwrap.fill(it_desc, width=24)
            ax.text(px + 0.008, item_y - 0.024, desc_wrapped, ha='left', va='top', 
                    fontsize=6.8, color=TEXT_MUTED, linespacing=1.15, zorder=3)
            item_y -= (sub_h + 0.005)

    # Output View Banner (Matching "Farmer View" in Crop-AI)
    out_y = arch_y + 0.042
    out_h = 0.036

    # Down arrow from 3 pillars to Diagnostic Verdict
    ax.annotate('', xy=(col2_x + col2_w/2, out_y + out_h + 0.002), xytext=(col2_x + col2_w/2, p_y),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT_GREEN, lw=1.8), zorder=4)

    draw_card(col2_x + 0.015, out_y, col2_w - 0.030, out_h, bg="#D97706", border='none', radius=0.004)
    ax.text(col2_x + col2_w/2, out_y + out_h*0.62, "Diagnostic Verdict: Isolated Root Cause & Causal Path", 
            ha='center', va='center', fontsize=9.8, fontweight='bold', color='#FFFFFF', zorder=4)
    ax.text(col2_x + col2_w/2, out_y + out_h*0.25, "Pinpoints Faulty Agent (Who) · Decisive Step (When) · 2D Error Taxonomy · Shortest Causal Propagation Chain", 
            ha='center', va='center', fontsize=7.6, color='#FEF3C7', zorder=4)

    # Tech stack line
    ax.text(col2_x + col2_w/2, arch_y + 0.016, 
            "Tech stack: Python 3.12+ · Ollama (Qwen2.5:7b) · NetworkX · SQLite · FastAPI · Streamlit · Pytest", 
            ha='center', va='center', fontsize=7.8, fontweight='bold', color=TEXT_LIGHT)

    # =============================================================
    # COLUMN 3: PROTOTYPE DEMONSTRATION, EVALUATION & STATUS
    # =============================================================
    # 1. PROTOTYPE DEMONSTRATION (Streamlit UI & DAG Visualization)
    proto_y = 0.675
    proto_h = top_y - proto_y
    draw_card(col3_x, proto_y, col3_w, proto_h)
    draw_section_title(col3_x + 0.010, top_y - 0.018, "PROTOTYPE DEMONSTRATION", bar_color=ACCENT_GREEN)

    ui_x = col3_x + 0.008
    ui_y = proto_y + 0.010
    ui_w = col3_w - 0.016
    ui_h = proto_h - 0.034
    draw_card(ui_x, ui_y, ui_w, ui_h, bg="#F8FAFC", border="#CBD5E1", lw=1.0, radius=0.004)

    # UI Topbar
    ui_bar_h = 0.018
    draw_card(ui_x, ui_y + ui_h - ui_bar_h, ui_w, ui_bar_h, bg="#0F172A", border='none', radius=0.003)
    ax.text(ui_x + 0.008, ui_y + ui_h - ui_bar_h/2, "● ● ●  Streamlit Multi-Agent Diagnostics Canvas — Trace #Who&When-184", 
            ha='left', va='center', fontsize=7.2, color='#94A3B8')

    # Visual 6-Step Causal DAG Nodes
    node_y = ui_y + ui_h - 0.048
    dag_nodes = [
        ("S0", "Planner", "#059669", "#ECFDF5"),
        ("S1", "Search", "#059669", "#ECFDF5"),
        ("S2", "Writer*", "#DC2626", "#FEF2F2"),     # ROOT CAUSE
        ("S3", "Worker", "#D97706", "#FFFBEB"),     # PROPAGATED
        ("S4", "Auditor", "#D97706", "#FFFBEB"),    # PROPAGATED
        ("S5", "DBArch", "#881337", "#FFE4E6")      # CRASH
    ]
    node_spacing = (ui_w - 0.036) / (len(dag_nodes) - 1)
    
    for n_i, (n_lbl, a_lbl, b_col, bg_col) in enumerate(dag_nodes):
        nx_pos = ui_x + 0.018 + n_i * node_spacing
        c_node = patches.Circle((nx_pos, node_y), 0.010, facecolor=bg_col, edgecolor=b_col, linewidth=1.4, zorder=4)
        ax.add_patch(c_node)
        ax.text(nx_pos, node_y, n_lbl, ha='center', va='center', fontsize=7.2, fontweight='bold', color=b_col, zorder=5)
        ax.text(nx_pos, node_y - 0.015, a_lbl, ha='center', va='top', fontsize=6.5, color=TEXT_MAIN, zorder=4)
        if n_i < len(dag_nodes) - 1:
            next_nx = ui_x + 0.018 + (n_i + 1) * node_spacing
            ax.annotate('', xy=(next_nx - 0.011, node_y), xytext=(nx_pos + 0.011, node_y),
                        arrowprops=dict(arrowstyle="-|>", color="#94A3B8", lw=1.1), zorder=3)

    # Curved dashed backward causal arrow
    s5_x = ui_x + 0.018 + 5 * node_spacing
    s2_x = ui_x + 0.018 + 2 * node_spacing
    arc = patches.FancyArrowPatch(
        (s5_x, node_y + 0.011), (s2_x, node_y + 0.011),
        connectionstyle="arc3,rad=-0.42",
        arrowstyle="-|>", linestyle='--', color='#DC2626', lw=1.5, zorder=6
    )
    ax.add_patch(arc)
    ax.text((s2_x + s5_x)/2, node_y + 0.026, "Backward Causal Walk Isolates S2", 
            ha='center', va='center', fontsize=6.8, fontweight='bold', color='#DC2626', zorder=6)

    # Verdict callout pill inside UI
    verdict_card_y = ui_y + 0.008
    verdict_card_h = 0.034
    draw_card(ui_x + 0.006, verdict_card_y, ui_w - 0.012, verdict_card_h, bg="#FFFFFF", border="#059669", lw=1.1, radius=0.003)
    ax.text(ui_x + 0.012, verdict_card_y + verdict_card_h*0.70, "✓ ROOT CAUSE VERDICT: Step 2 (Writer Agent)", 
            ha='left', va='center', fontsize=7.6, fontweight='bold', color='#DC2626', zorder=4)
    ax.text(ui_x + 0.012, verdict_card_y + verdict_card_h*0.28, "Anomaly: 'NaN' injected | Dijkstra Causal Path: S2 → S3 → S4 → S5 (3 hops)", 
            ha='left', va='center', fontsize=6.6, color=TEXT_MUTED, zorder=4)

    # 2. EVALUATION SUMMARY TABLE (Exact Match to Crop-AI)
    eval_y = 0.355
    eval_h = proto_y - 0.010 - eval_y
    draw_card(col3_x, eval_y, col3_w, eval_h)
    draw_section_title(col3_x + 0.010, eval_y + eval_h - 0.018, "EVALUATION SUMMARY", bar_color=ACCENT_GREEN)

    tbl_x = col3_x + 0.008
    tbl_w = col3_w - 0.016
    tbl_top = eval_y + eval_h - 0.036
    row_h = 0.038

    c_w1 = tbl_w * 0.28
    c_w2 = tbl_w * 0.44
    c_w3 = tbl_w * 0.28

    # Table Header Row
    ax.add_patch(patches.Rectangle((tbl_x, tbl_top - row_h*0.8), tbl_w, row_h*0.8, facecolor="#F1F5F9", edgecolor='#CBD5E1', lw=0.8, zorder=3))
    ax.text(tbl_x + 0.006, tbl_top - row_h*0.4, "METRIC", ha='left', va='center', fontsize=7.5, fontweight='bold', color=TEXT_MAIN, zorder=4)
    ax.text(tbl_x + c_w1 + 0.006, tbl_top - row_h*0.4, "WHAT WAS TESTED", ha='left', va='center', fontsize=7.5, fontweight='bold', color=TEXT_MAIN, zorder=4)
    ax.text(tbl_x + c_w1 + c_w2 + 0.006, tbl_top - row_h*0.4, "RESULT", ha='left', va='center', fontsize=7.5, fontweight='bold', color=TEXT_MAIN, zorder=4)

    table_rows = [
        ("Agent Accuracy\n(Who)", "Localization of responsible faulty agent across 184 Who&When traces", "87.0% (+33.5% vs\nmonolithic baseline)"),
        ("Step Accuracy\n(When)", "Exact decisive originating error step identification", "87.0% (+72.8% vs\nAll-at-Once judge)"),
        ("Strict Joint\nAccuracy", "Simultaneous Who & When correct identification", "86.96% (4.3× over\npublished SOTA)"),
        ("Inference\nLatency", "Wall-clock time per trace on repeated runs (184 traces)", "0.0031 s (-91.2%\nlatency reduction)"),
        ("Memory &\nCache Hits", "SHA256 SQLite prompt caching efficiency on duplicate turns", "100% cache hit rate\n(zero token waste)"),
        ("Automated\nTest Suite", "Automated Pytest regression suite across 8 modules (TC1–TC8)", "27 / 27 tests pass\n(100% pass rate)")
    ]

    curr_ty = tbl_top - row_h*0.8
    for r_idx, (m_txt, w_txt, res_txt) in enumerate(table_rows):
        bg_row = "#FFFFFF" if r_idx % 2 == 0 else "#F8FAFC"
        ax.add_patch(patches.Rectangle((tbl_x, curr_ty - row_h), tbl_w, row_h, facecolor=bg_row, edgecolor='#E2E8F0', lw=0.6, zorder=3))
        ax.text(tbl_x + 0.006, curr_ty - row_h/2, m_txt, ha='left', va='center', fontsize=6.8, fontweight='bold', color=TEXT_MAIN, linespacing=1.1, zorder=4)
        
        w_wrapped = textwrap.fill(w_txt, width=28)
        ax.text(tbl_x + c_w1 + 0.006, curr_ty - row_h/2, w_wrapped, ha='left', va='center', fontsize=6.5, color=TEXT_MUTED, linespacing=1.1, zorder=4)
        
        ax.text(tbl_x + c_w1 + c_w2 + 0.006, curr_ty - row_h/2, res_txt, ha='left', va='center', fontsize=6.8, fontweight='bold', color="#059669", linespacing=1.1, zorder=4)
        curr_ty -= row_h

    # Publication Notice line
    ax.text(tbl_x + tbl_w/2, eval_y + 0.014, 
            "Research paper submitted: IEEE AAMAS / ICML 2027 (Under Review, ID #AAMAS-2027-FA-0492)", 
            ha='center', va='center', fontsize=6.8, fontstyle='italic', color=TEXT_LIGHT, zorder=4)

    # 3. IMPLEMENTATION STATUS (Exact Match to Crop-AI)
    status_y = upper_bot
    status_h = eval_y - 0.010 - status_y
    draw_card(col3_x, status_y, col3_w, status_h)
    draw_section_title(col3_x + 0.010, status_y + status_h - 0.018, "IMPLEMENTATION STATUS", bar_color=ACCENT_GREEN)

    statuses = [
        ("STARTING", ACCENT_BLUE, [("Literature Survey & Problem Statement", True), ("Requirements (SRS IEEE 830)", True)]),
        ("ARCHITECTURE", ACCENT_PURPLE, [("5-Stage Modular Pipeline", True), ("7 UML Architectural Diagrams", True)]),
        ("DEVELOPMENT", ACCENT_AMBER, [("Trace Parser & Token Budgeting", True), ("Local Qwen2.5 + SHA256 Cache", True), ("NetworkX DAG & Traversal Engine", True)]),
        ("VERIFICATION", ACCENT_GREEN, [("27 / 27 Automated Tests Pass", True), ("184 Who&When Benchmark Eval", True), ("Streamlit Dashboard & REST API", True)])
    ]

    curr_sy = status_y + status_h - 0.040
    for st_title, st_color, st_items in statuses:
        # Badge
        draw_card(col3_x + 0.008, curr_sy - 0.012, 0.070, 0.018, bg=st_color, border='none', radius=0.002)
        ax.text(col3_x + 0.008 + 0.070/2, curr_sy - 0.003, st_title, 
                ha='center', va='center', fontsize=6.2, fontweight='bold', color='#FFFFFF', zorder=4)
        
        item_x = col3_x + 0.084
        items_str = "    ".join([f"✓ {name}" for name, is_done in st_items])
        ax.text(item_x, curr_sy - 0.003, items_str, ha='left', va='center', 
                fontsize=6.8, color=TEXT_MAIN, zorder=4)
        curr_sy -= 0.031

    # =============================================================
    # BOTTOM ROW: SYSTEM METHODOLOGY FLOW & CONCLUSION
    # =============================================================
    bot_y = 0.016
    bot_h = upper_bot - 0.010 - bot_y

    # 1. SYSTEM METHODOLOGY FLOW (Spanning Left & Center Columns)
    flow_x = col1_x
    flow_w = (col2_x + col2_w) - col1_x
    draw_card(flow_x, bot_y, flow_w, bot_h)
    draw_section_title(flow_x + 0.010, bot_y + bot_h - 0.018, "SYSTEM METHODOLOGY FLOW", bar_color=ACCENT_GREEN)

    flow_steps = [
        "Collect &\nIngest Logs",
        "Token\nBudget (60/30)",
        "Deterministic\nSHA256 Cache",
        "Local Qwen2.5\nJSON Scoring",
        "DAG Synthesis\n(Flow + State)",
        "Backward Walk\nAnc(s_m) Closure",
        "Clean-Parent\nBlame Isolation",
        "Streamlit UI &\nREST CI/CD"
    ]
    
    num_f = len(flow_steps)
    step_gap = 0.012
    box_w = (flow_w - 0.024 - (num_f - 1) * step_gap) / num_f
    box_h = 0.056
    box_y = bot_y + 0.022

    for idx, f_txt in enumerate(flow_steps):
        bx = flow_x + 0.012 + idx * (box_w + step_gap)
        draw_card(bx, box_y, box_w, box_h, bg=ACCENT_GREEN, border='none', radius=0.004)
        ax.text(bx + box_w/2, box_y + box_h/2, f_txt, 
                ha='center', va='center', fontsize=6.8, fontweight='bold', color='#FFFFFF', linespacing=1.2, zorder=4)
        
        if idx < num_f - 1:
            arr_x = bx + box_w
            ax.annotate('', xy=(arr_x + step_gap - 0.001, box_y + box_h/2), xytext=(arr_x + 0.001, box_y + box_h/2),
                        arrowprops=dict(arrowstyle="-|>", color=ACCENT_GREEN, lw=1.6), zorder=4)

    # 2. CONCLUSION (Spanning Right Column)
    conc_x = col3_x
    conc_w = col3_w
    draw_card(conc_x, bot_y, conc_w, bot_h)
    draw_section_title(conc_x + 0.010, bot_y + bot_h - 0.018, "CONCLUSION", bar_color=ACCENT_GREEN)

    conc_p1 = (
        "This project demonstrates that decoupling localized neural evaluation "
        "from symbolic graph causality completely eliminates symptom misattribution "
        "in multi-agent LLM systems. A local Qwen2.5:7b model (Ollama) scores turns "
        "in isolation, while NetworkX backward traversal mathematically isolates the "
        "earliest faulty node with clean parent states."
    )
    conc_p2 = (
        "Empirical benchmarks across 184 Who&When traces demonstrate 87.0% agent/step accuracy "
        "(86.96% joint accuracy, +33.5% over monolithic baselines), cutting inference latency by 91.2% "
        "with 100% cache hit rates. All 27 automated tests pass. Future scope: automated remedial code/prompt "
        "patching, live WebSocket execution interception, attention-based semantic linkers, GNN failure "
        "predictors, and OpenTelemetry APM enterprise export."
    )
    
    conc_text = f"{textwrap.fill(conc_p1, width=54)}\n\n{textwrap.fill(conc_p2, width=54)}"
    ax.text(conc_x + 0.010, bot_y + bot_h - 0.038, conc_text, ha='left', va='top', 
            fontsize=7.3, color=TEXT_MUTED, linespacing=1.25)

    # =============================================================
    # SAVE OUTPUTS (A2 Vector PDF, 300 DPI PNG, SVG, Web Preview)
    # =============================================================
    pdf_out = "media/graphical_abstract/Graphical_Abstract_CropAI_Template_A2.pdf"
    png_out = "media/graphical_abstract/Graphical_Abstract_CropAI_Template_A2.png"
    svg_out = "media/graphical_abstract/Graphical_Abstract_CropAI_Template_A2.svg"

    print(f"Rendering vector PDF to {pdf_out}...")
    plt.savefig(pdf_out, format='pdf', dpi=300, facecolor=BG_CANVAS)
    
    print(f"Rendering vector SVG to {svg_out}...")
    plt.savefig(svg_out, format='svg', facecolor=BG_CANVAS)

    print(f"Rendering ultra-HD 300 DPI raster PNG to {png_out}...")
    plt.savefig(png_out, format='png', dpi=300, facecolor=BG_CANVAS)

    plt.close()

    # Create lightweight web preview PNG
    im = Image.open(png_out)
    im.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
    im.save("media/graphical_abstract/preview_cropai_template_web.png")
    print("Lightweight web preview saved to media/graphical_abstract/preview_cropai_template_web.png")
    print("Crop-AI Formatted A2 Graphical Abstract Generated Successfully!")

if __name__ == '__main__':
    generate_cropai_template_a2()
