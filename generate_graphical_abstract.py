import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
import numpy as np

def generate_a2_graphical_abstract():
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
    plt.rcParams['font.serif'] = ['Liberation Serif', 'DejaVu Serif', 'Times New Roman']
    plt.rcParams['font.sans-serif'] = ['Liberation Sans', 'DejaVu Sans', 'Arial']
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['mathtext.fontset'] = 'cm'

    # Color Palette: Causal Clarity
    BG_CANVAS = "#F8FAFC"
    CARD_BG = "#FFFFFF"
    BORDER_COLOR = "#CBD5E1"
    CRIMSON = "#800000"
    CRIMSON_DARK = "#5B0000"
    GOLD = "#D4AF37"
    NAVY = "#0F172A"
    NAVY_LIGHT = "#1E293B"
    TEXT_DARK = "#0F172A"
    TEXT_MUTED = "#475569"
    EMERALD = "#059669"
    EMERALD_BG = "#ECFDF5"
    RED_ACCENT = "#DC2626"
    RED_BG = "#FEF2F2"
    AMBER_ACCENT = "#D97706"
    AMBER_BG = "#FFFBEB"
    BLUE_ACCENT = "#2563EB"
    BLUE_BG = "#EFF6FF"

    # Fill canvas background
    ax.add_patch(patches.Rectangle((0, 0), 1, 1, facecolor=BG_CANVAS, edgecolor='none', zorder=0))

    # Helper: draw rounded card
    def draw_card(x, y, w, h, bg=CARD_BG, border=BORDER_COLOR, lw=1.5, radius=0.008, zorder=2):
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle=patches.BoxStyle("Round", pad=radius, rounding_size=radius),
            facecolor=bg, edgecolor=border, linewidth=lw, zorder=zorder
        )
        ax.add_patch(box)
        return box

    # -------------------------------------------------------------
    # 1. HEADER BANNER (Institutional & Project Branding)
    # -------------------------------------------------------------
    header_y = 0.885
    header_h = 0.115
    ax.add_patch(patches.Rectangle((0, header_y), 1, header_h, facecolor=CRIMSON, edgecolor='none', zorder=1))
    ax.add_patch(patches.Rectangle((0, header_y), 1, 0.004, facecolor=GOLD, edgecolor='none', zorder=2))

    # Institutional Text
    ax.text(0.5, 0.978, "GOKARAJU RANGARAJU INSTITUTE OF ENGINEERING AND TECHNOLOGY", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#FDE68A', zorder=3,
            family='sans-serif')
    ax.text(0.5, 0.960, "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING  |  MAJOR PROJECT WORK (PHASE-1)  |  ACADEMIC YEAR 2026-2027", 
            ha='center', va='center', fontsize=10.5, color='#E2E8F0', zorder=3, family='sans-serif')

    # Main Title
    ax.text(0.5, 0.932, "AUTOMATED FAILURE ATTRIBUTION FOR LLM-BASED MULTI-AGENT SYSTEMS", 
            ha='center', va='center', fontsize=22, fontweight='bold', color='#FFFFFF', zorder=3)
    ax.text(0.5, 0.908, "A Graph-Causal Diagnostic Engine with Deterministic SHA-256 Prompt Caching & Backward Dependency Traversal", 
            ha='center', va='center', fontsize=12.5, style='italic', color='#F1F5F9', zorder=3)

    # Metadata badges in header
    meta_y = 0.892
    ax.text(0.04, meta_y, "BATCH: B12", ha='left', va='center', fontsize=9.5, fontweight='bold', 
            color='#FDE68A', family='sans-serif', zorder=3)
    ax.text(0.14, meta_y, "STUDENTS: R. S. Prabhaadhithya (23241A05Q3)  •  R. Ajay (23241A05Q4)  •  N. Paul (23241A05Q6)  •  T. Niranjan (23241A05R1)", 
            ha='left', va='center', fontsize=9, color='#FFFFFF', family='sans-serif', zorder=3)
    ax.text(0.96, meta_y, "PROJECT GUIDE: Dr. D. Ushasree, Assistant Professor, Dept. of CSE", 
            ha='right', va='center', fontsize=9, fontweight='bold', color='#FDE68A', family='sans-serif', zorder=3)

    # -------------------------------------------------------------
    # 2. MAIN 3-COLUMN LAYOUT
    # -------------------------------------------------------------
    col_y = 0.090
    col_h = 0.780
    col_w = 0.306
    col1_x = 0.020
    col2_x = 0.347
    col3_x = 0.674

    # =============================================================
    # COLUMN 1: THE MULTI-AGENT FAILURE DILEMMA (Problem)
    # =============================================================
    # Column Title Banner
    c1_banner = draw_card(col1_x, col_y + col_h - 0.045, col_w, 0.045, bg=CRIMSON, border=CRIMSON_DARK, zorder=3)
    ax.text(col1_x + 0.015, col_y + col_h - 0.0225, "01 | THE MULTI-AGENT FAILURE CRISIS", 
            ha='left', va='center', fontsize=13, fontweight='bold', color='#FFFFFF', zorder=4)
    ax.text(col1_x + col_w - 0.015, col_y + col_h - 0.0225, "THE PROBLEM", 
            ha='right', va='center', fontsize=9.5, fontweight='bold', color='#FDE68A', family='sans-serif', zorder=4)

    # Card 1A: Cascading Error Propagation (The Needle-in-a-Haystack Dilemma)
    draw_card(col1_x, 0.535, col_w, 0.285)
    ax.text(col1_x + 0.012, 0.805, "Cascading Error Propagation Across Agent Steps", 
            ha='left', va='top', fontsize=12, fontweight='bold', color=TEXT_DARK)
    ax.text(col1_x + 0.012, 0.785, 
            "In collaborative multi-agent systems (AutoGen, MetaGPT, LangGraph), a single faulty\n"
            "reasoning step compounds silently across subsequent turns, resulting in late crashes.",
            ha='left', va='top', fontsize=9.5, color=TEXT_MUTED, linespacing=1.3)

    # Cascading step boxes
    steps_data = [
        ("Step 2: Planner", "Latent Defect: Introduces invalid argument 'auth'", AMBER_BG, AMBER_ACCENT, "ROOT CAUSE"),
        ("Step 5: Coder", "Error Propagation: Implements API assuming signature is valid", CARD_BG, BORDER_COLOR, "Propagated"),
        ("Step 9: Reviewer", "Blind Approval: Validates logic without execution check", CARD_BG, BORDER_COLOR, "Propagated"),
        ("Step 14: Executor", "MANIFEST CRASH: TypeError: unexpected keyword 'auth'", RED_BG, RED_ACCENT, "MANIFEST FAILURE")
    ]
    box_y = 0.730
    for i, (title, desc, bg_c, b_c, badge) in enumerate(steps_data):
        draw_card(col1_x + 0.015, box_y, col_w - 0.030, 0.040, bg=bg_c, border=b_c, lw=1.5)
        ax.text(col1_x + 0.025, box_y + 0.026, title, fontsize=10, fontweight='bold', color=TEXT_DARK)
        ax.text(col1_x + 0.025, box_y + 0.010, desc, fontsize=8.5, color=TEXT_MUTED)
        
        # Badge
        badge_color = AMBER_ACCENT if "ROOT" in badge else (RED_ACCENT if "MANIFEST" in badge else TEXT_MUTED)
        ax.text(col1_x + col_w - 0.025, box_y + 0.020, badge, fontsize=8, fontweight='bold', 
                color=badge_color, ha='right', va='center', family='sans-serif')
        
        # Arrow down
        if i < len(steps_data) - 1:
            ax.annotate("", xy=(col1_x + 0.040, box_y - 0.006), xytext=(col1_x + 0.040, box_y),
                        arrowprops=dict(arrowstyle="->", color=RED_ACCENT, lw=1.8))
        box_y -= 0.048

    # Causal Backtrack Arrow Annotation
    ax.annotate("True Causal Origin: Step 2\n(12 turns before symptom)",
                xy=(col1_x + col_w - 0.070, 0.730 + 0.020),
                xytext=(col1_x + col_w - 0.080, 0.586),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.4", 
                                color=AMBER_ACCENT, lw=2.2, linestyle='--'),
                fontsize=8.5, fontweight='bold', color=AMBER_ACCENT, ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.3", fc="#FFFBEB", ec=AMBER_ACCENT, lw=1))

    # Card 1B: The Collapse of Naive LLM-as-a-Judge
    draw_card(col1_x, 0.280, col_w, 0.245)
    ax.text(col1_x + 0.012, 0.510, "Why Naive LLM-as-a-Judge Fails (14.2% Accuracy)", 
            ha='left', va='top', fontsize=12, fontweight='bold', color=RED_ACCENT)
    ax.text(col1_x + 0.012, 0.490, 
            "Evaluating entire 100+ turn traces in a single prompt causes catastrophic diagnostic failure:",
            ha='left', va='top', fontsize=9.5, color=TEXT_MUTED)

    # 3 Failure Pillars
    f_pillars = [
        ("1. Severe Recency Bias", "Naive judges systematically blame the final agent that crashed (Step 14) rather than the upstream agent that introduced the defect (Step 2)."),
        ("2. Context Saturation & Cost", "Passing 50+ agent turns exceeds LLM attention capacity, triggering hallucinations, lost needles, and exorbitant API token costs."),
        ("3. Symptom Misattribution", "Downstream agents fail legitimately due to upstream garbage data; traditional prompts cannot distinguish victims from culprits.")
    ]
    py = 0.450
    for title, desc in f_pillars:
        ax.text(col1_x + 0.015, py, title, fontsize=9.5, fontweight='bold', color=TEXT_DARK)
        ax.text(col1_x + 0.015, py - 0.015, desc, fontsize=8.5, color=TEXT_MUTED, linespacing=1.2)
        py -= 0.045

    # Card 1C: Quantitative Baseline Flaw
    draw_card(col1_x, 0.090, col_w, 0.180, bg=RED_BG, border=RED_ACCENT)
    ax.text(col1_x + 0.015, 0.252, "STATE-OF-THE-ART BASELINE COLLAPSE (WHO&WHEN)", 
            fontsize=10, fontweight='bold', color=RED_ACCENT, family='sans-serif')
    
    # 2 Mini Stat Boxes
    draw_card(col1_x + 0.015, 0.110, 0.130, 0.125, bg='#FFFFFF', border=RED_ACCENT)
    ax.text(col1_x + 0.080, 0.200, "14.2%", fontsize=26, fontweight='bold', color=RED_ACCENT, ha='center')
    ax.text(col1_x + 0.080, 0.165, "Step Localization", fontsize=9, fontweight='bold', color=TEXT_DARK, ha='center')
    ax.text(col1_x + 0.080, 0.145, "Naive LLM Judge fails 86% of the time", fontsize=7.5, color=TEXT_MUTED, ha='center')

    draw_card(col1_x + 0.155, 0.110, 0.135, 0.125, bg='#FFFFFF', border=RED_ACCENT)
    ax.text(col1_x + 0.222, 0.200, "26.1%", fontsize=26, fontweight='bold', color=RED_ACCENT, ha='center')
    ax.text(col1_x + 0.222, 0.165, "Joint Accuracy", fontsize=9, fontweight='bold', color=TEXT_DARK, ha='center')
    ax.text(col1_x + 0.222, 0.145, "Fails to pinpoint both agent & step", fontsize=7.5, color=TEXT_MUTED, ha='center')

    # =============================================================
    # COLUMN 2: THE GRAPH-CAUSAL ATTRIBUTION ENGINE (Methodology)
    # =============================================================
    c2_banner = draw_card(col2_x, col_y + col_h - 0.045, col_w, 0.045, bg=NAVY, border=NAVY_LIGHT, zorder=3)
    ax.text(col2_x + 0.015, col_y + col_h - 0.0225, "02 | THE GRAPH-CAUSAL DIAGNOSTIC ENGINE", 
            ha='left', va='center', fontsize=13, fontweight='bold', color='#FFFFFF', zorder=4)
    ax.text(col2_x + col_w - 0.015, col_y + col_h - 0.0225, "OUR METHODOLOGY", 
            ha='right', va='center', fontsize=9.5, fontweight='bold', color=GOLD, family='sans-serif', zorder=4)

    # Card 2A: 4-Stage Architectural Pipeline
    draw_card(col2_x, 0.655, col_w, 0.165)
    ax.text(col2_x + 0.012, 0.805, "4-Stage Causal Diagnostic Pipeline", 
            ha='left', va='top', fontsize=12, fontweight='bold', color=TEXT_DARK)

    p_stages = [
        ("1. Trace Segmentation", "Normalizes diverse logs into Pydantic steps (≤4096 tokens)."),
        ("2. SHA-256 Cache", "O(1) hash lookup (<1.5ms); eliminates redundant LLM calls."),
        ("3. Causal DAG Builder", "Constructs NetworkX DAG across message, state & time flows."),
        ("4. Backward Traversal", "Backtracks from crash along Anc(m) to pinpoint root defect.")
    ]
    sx = col2_x + 0.012
    sw = (col_w - 0.036) / 2
    for idx, (title, desc) in enumerate(p_stages):
        r = idx // 2
        c = idx % 2
        px = sx + c * (sw + 0.012)
        py = 0.730 - r * 0.065
        draw_card(px, py, sw, 0.058, bg=BLUE_BG, border=BLUE_ACCENT, lw=1)
        ax.text(px + 0.008, py + 0.042, title, fontsize=9, fontweight='bold', color=BLUE_ACCENT)
        ax.text(px + 0.008, py + 0.012, desc, fontsize=7.5, color=TEXT_MUTED, linespacing=1.2)

    # Card 2B: Visual Directed Acyclic Graph & Ancestor Closure
    draw_card(col2_x, 0.285, col_w, 0.360)
    ax.text(col2_x + 0.012, 0.632, "Causal Dependency Graph (DAG) & Ancestor Closure", 
            ha='left', va='top', fontsize=12, fontweight='bold', color=TEXT_DARK)
    ax.text(col2_x + 0.012, 0.612, 
            "Extracting Causal Ancestor Closure Anc(m) prunes parallel noise and guarantees\n"
            "that only steps with direct causal provenance to the crash are evaluated.",
            ha='left', va='top', fontsize=9, color=TEXT_MUTED, linespacing=1.2)

    # Drawing the Causal DAG Nodes & Edges manually for perfect crisp vector art
    # Graph canvas bounds: x in [col2_x + 0.02, col2_x + col_w - 0.02], y in [0.34, 0.58]
    dag_nodes = {
        "S1": (col2_x + 0.050, 0.460, "S1: User\nGoal", CARD_BG, BORDER_COLOR, TEXT_DARK),
        "S2": (col2_x + 0.120, 0.530, "S2: Planner\n(Root Defect)", AMBER_BG, AMBER_ACCENT, AMBER_ACCENT),
        "S3": (col2_x + 0.120, 0.390, "S3: WebSearch\n(Unrelated)", "#F1F5F9", BORDER_COLOR, "#94A3B8"),
        "S5": (col2_x + 0.185, 0.530, "S5: Coder\n(Propagated)", BLUE_BG, BLUE_ACCENT, TEXT_DARK),
        "S7": (col2_x + 0.185, 0.390, "S7: DocGen\n(Unrelated)", "#F1F5F9", BORDER_COLOR, "#94A3B8"),
        "S9": (col2_x + 0.245, 0.530, "S9: Reviewer\n(Propagated)", BLUE_BG, BLUE_ACCENT, TEXT_DARK),
        "S14": (col2_x + 0.285, 0.460, "S14: Exec\n(Crash!)", RED_BG, RED_ACCENT, RED_ACCENT)
    }

    # Edges (u, v, is_causal, label)
    dag_edges = [
        ("S1", "S2", True, "msg"),
        ("S1", "S3", False, "msg"),
        ("S2", "S5", True, "state"),
        ("S3", "S7", False, "state"),
        ("S5", "S9", True, "msg"),
        ("S9", "S14", True, "msg"),
        ("S7", "S14", False, "dep")
    ]

    for u, v, is_c, lbl in dag_edges:
        p1 = dag_nodes[u]
        p2 = dag_nodes[v]
        edge_c = RED_ACCENT if is_c else "#CBD5E1"
        edge_lw = 2.2 if is_c else 1.0
        edge_style = '-' if is_c else '--'
        ax.annotate("", xy=(p2[0]-0.015, p2[1]), xytext=(p1[0]+0.015, p1[1]),
                    arrowprops=dict(arrowstyle="->", color=edge_c, lw=edge_lw, linestyle=edge_style))

    for k, (nx, ny, nlbl, nbg, nbd, ntc) in dag_nodes.items():
        draw_card(nx - 0.022, ny - 0.025, 0.044, 0.050, bg=nbg, border=nbd, lw=1.8 if k in ["S2", "S14"] else 1.0)
        ax.text(nx, ny, nlbl, ha='center', va='center', fontsize=7.5, fontweight='bold', color=ntc)

    # Graph Legend & Callouts
    draw_card(col2_x + 0.015, 0.295, col_w - 0.030, 0.040, bg="#F8FAFC", border=BORDER_COLOR)
    ax.text(col2_x + 0.025, 0.315, "CAUSAL CLOSURE Anc(m) = {S2, S5, S9, S14}", 
            fontsize=8.5, fontweight='bold', color=CRIMSON, family='sans-serif')
    ax.text(col2_x + col_w - 0.025, 0.315, "S3, S7 Pruned (Complexity O(N) -> O(|Anc(m)|))", 
            fontsize=8, color=TEXT_MUTED, ha='right', family='sans-serif')

    # Card 2C: Mathematical Models & Invariants
    draw_card(col2_x, 0.090, col_w, 0.185, bg="#FFFFFF", border=BORDER_COLOR)
    ax.text(col2_x + 0.012, 0.260, "Formal Mathematical Formulations & Invariants", 
            ha='left', va='top', fontsize=11, fontweight='bold', color=TEXT_DARK)

    math_items = [
        ("Causal Precedence Invariant:", r"$e = (u, v) \in E_{\mathrm{dag}} \Rightarrow \mathrm{time}(u) < \mathrm{time}(v)$", "Guarantees acyclicity"),
        ("Deterministic Cache Key:", r"$k_{\mathrm{cache}} = \mathrm{SHA256}( \mathrm{prompt} \parallel \mathrm{agent} \parallel \mathrm{payload} )$", "< 1.5ms O(1) hit"),
        ("Root Cause Attribution:", r"$s^* = \arg\min_{s \in \mathrm{Anc}(m)} \{ \mathrm{idx}(s) \mid \mathrm{anomalous}(s) = \mathrm{True} \}$", "Earliest defect in chain")
    ]
    my = 0.225
    for title, formula, note in math_items:
        ax.text(col2_x + 0.015, my, title, fontsize=8.5, fontweight='bold', color=TEXT_DARK)
        ax.text(col2_x + 0.140, my, formula, fontsize=9.5, color=CRIMSON, va='center')
        ax.text(col2_x + col_w - 0.015, my, f"[{note}]", fontsize=8, color=TEXT_MUTED, ha='right', family='sans-serif')
        my -= 0.040

    # =============================================================
    # COLUMN 3: EMPIRICAL VALIDATION & IMPACT (Results)
    # =============================================================
    c3_banner = draw_card(col3_x, col_y + col_h - 0.045, col_w, 0.045, bg=EMERALD, border="#047857", zorder=3)
    ax.text(col3_x + 0.015, col_y + col_h - 0.0225, "03 | EMPIRICAL VALIDATION & BENCHMARKS", 
            ha='left', va='center', fontsize=13, fontweight='bold', color='#FFFFFF', zorder=4)
    ax.text(col3_x + col_w - 0.015, col_y + col_h - 0.0225, "PROVEN RESULTS", 
            ha='right', va='center', fontsize=9.5, fontweight='bold', color='#A7F3D0', family='sans-serif', zorder=4)

    # Card 3A: Big Metric KPI Grid
    draw_card(col3_x, 0.635, col_w, 0.185)
    ax.text(col3_x + 0.012, 0.805, "Who&When Benchmark Performance (ICML 2025)", 
            ha='left', va='top', fontsize=12, fontweight='bold', color=TEXT_DARK)

    # 4 Big Stat Cards
    kpi_w = (col_w - 0.036) / 2
    kpis = [
        ("86.96%", "Joint Attribution", "+60.87% vs baseline", EMERALD),
        ("91.30%", "Agent Localization", "21 / 23 benchmarks", BLUE_ACCENT),
        ("0.44 s", "Traversal Latency", "Sub-second execution", TEXT_DARK),
        ("14.2x", "Prompt Cache Speedup", "< 1.5ms hit latency", AMBER_ACCENT)
    ]
    for idx, (num, label, sub, col) in enumerate(kpis):
        r = idx // 2
        c = idx % 2
        kx = col3_x + 0.012 + c * (kpi_w + 0.012)
        ky = 0.710 - r * 0.065
        draw_card(kx, ky, kpi_w, 0.058, bg='#F8FAFC', border=BORDER_COLOR)
        ax.text(kx + 0.010, ky + 0.034, num, fontsize=18, fontweight='bold', color=col)
        ax.text(kx + 0.010, ky + 0.018, label, fontsize=8.5, fontweight='bold', color=TEXT_DARK)
        ax.text(kx + 0.010, ky + 0.006, sub, fontsize=7.5, color=TEXT_MUTED)

    # Card 3B: Comparative Accuracy Bar Chart
    draw_card(col3_x, 0.355, col_w, 0.270)
    ax.text(col3_x + 0.012, 0.610, "Attribution Accuracy vs SOTA Baselines", 
            ha='left', va='top', fontsize=12, fontweight='bold', color=TEXT_DARK)
    ax.text(col3_x + 0.012, 0.590, "Joint Attribution Accuracy (Evaluating both Who and When correctly)", 
            ha='left', va='top', fontsize=8.5, color=TEXT_MUTED)

    # Embedded Matplotlib Bar Chart inside the card!
    bar_data = [
        ("Naive LLM Judge\n(All-at-Once)", 26.09, RED_ACCENT),
        ("Step-by-Step\nEvaluation", 43.48, "#94A3B8"),
        ("Binary Search\nBaseline", 65.22, BLUE_ACCENT),
        ("Our Proposed\nCausal Engine", 86.96, EMERALD)
    ]
    chart_y = 0.400
    chart_h = 0.160
    bar_w = 0.045
    spacing = (col_w - 0.050 - 4 * bar_w) / 3

    for i, (name, val, color) in enumerate(bar_data):
        bx = col3_x + 0.025 + i * (bar_w + spacing)
        norm_h = (val / 100.0) * chart_h
        
        # Bar
        ax.add_patch(patches.Rectangle((bx, chart_y), bar_w, norm_h, facecolor=color, edgecolor='none', zorder=3))
        
        # Value text on top
        ax.text(bx + bar_w/2, chart_y + norm_h + 0.006, f"{val:.1f}%", ha='center', va='bottom', 
                fontsize=9.5, fontweight='bold', color=color)
        
        # Label below
        ax.text(bx + bar_w/2, chart_y - 0.008, name, ha='center', va='top', 
                fontsize=7.5, color=TEXT_DARK, linespacing=1.1)

    # Baseline axis line
    ax.plot([col3_x + 0.020, col3_x + col_w - 0.020], [chart_y, chart_y], color=BORDER_COLOR, lw=1.5, zorder=2)

    # Card 3C: Production Readiness & Verification Badge
    draw_card(col3_x, 0.090, col_w, 0.255, bg=EMERALD_BG, border=EMERALD)
    ax.text(col3_x + 0.015, 0.332, "PRODUCTION VERIFICATION & DELIVERABLES", 
            fontsize=10.5, fontweight='bold', color=EMERALD, family='sans-serif')

    # Test Suite Pass Badge
    draw_card(col3_x + 0.015, 0.225, col_w - 0.030, 0.090, bg='#FFFFFF', border=EMERALD, lw=1.5)
    ax.text(col3_x + 0.025, 0.292, "27 / 27 UNIT TESTS PASSED (100%)", 
            fontsize=13, fontweight='bold', color=EMERALD)
    ax.text(col3_x + 0.025, 0.272, "Total execution time: 1.84s across 9 test modules (pytest v8.3)", 
            fontsize=8.5, color=TEXT_MUTED)
    ax.text(col3_x + 0.025, 0.252, 
            "• Parser Validation (TC1-TC2)     • SHA-256 Prompt Cache (TC3-TC4)\n"
            "• DAG Acyclicity & Sort (TC5-TC6)   • Backward Causal Traversal (TC7-TC8)",
            fontsize=8, color=TEXT_DARK, linespacing=1.3)

    # User Interfaces List
    ax.text(col3_x + 0.015, 0.200, "Delivered Operational Artifacts:", 
            fontsize=9.5, fontweight='bold', color=TEXT_DARK)
    artifacts_txt = (
        "1. agent-trace CLI: Command-line tool with diagnose, benchmark & watch commands.\n"
        "2. FastAPI REST Server: 8 production endpoints with interactive Swagger docs.\n"
        "3. Streamlit Visualizer: Interactive PyVis graph inspector with live anomaly triage."
    )
    ax.text(col3_x + 0.015, 0.180, artifacts_txt, fontsize=8, color=TEXT_MUTED, va='top', linespacing=1.3)

    # -------------------------------------------------------------
    # 3. FOOTER BANNER (Key Technical Pillars & Conclusion)
    # -------------------------------------------------------------
    footer_y = 0.015
    footer_h = 0.065
    ax.add_patch(patches.Rectangle((0, footer_y), 1, footer_h, facecolor=NAVY, edgecolor='none', zorder=1))
    ax.add_patch(patches.Rectangle((0, footer_y + footer_h - 0.003), 1, 0.003, facecolor=GOLD, edgecolor='none', zorder=2))

    # 4 Synthesis Pillars in Footer
    foot_w = 0.230
    foot_spacing = (1.0 - 0.040 - 4 * foot_w) / 3
    foot_pillars = [
        ("Causal Provenance", "Replaces heuristic LLM judging with formal DAG ancestor closures Anc(m)."),
        ("Token Boundedness", "Strict ≤4096 token segmentation eliminates context saturation & bloat."),
        ("Deterministic Speed", "SHA-256 caching delivers <1.5ms lookups with 14.2x latency acceleration."),
        ("Empirically Verified", "Achieves 86.96% joint attribution accuracy on ICML Who&When benchmarks.")
    ]
    for idx, (title, desc) in enumerate(foot_pillars):
        fx = 0.020 + idx * (foot_w + foot_spacing)
        ax.text(fx, footer_y + 0.042, f"0{idx+1} | {title.upper()}", 
                fontsize=9.5, fontweight='bold', color=GOLD, family='sans-serif', zorder=3)
        ax.text(fx, footer_y + 0.018, desc, 
                fontsize=8, color='#E2E8F0', family='sans-serif', zorder=3, linespacing=1.2)

    # -------------------------------------------------------------
    # 4. Save High-Definition Outputs
    # -------------------------------------------------------------
    pdf_out = "media/graphical_abstract/Graphical_Abstract_A2_Landscape.pdf"
    png_out = "media/graphical_abstract/Graphical_Abstract_A2_Landscape.png"
    svg_out = "media/graphical_abstract/Graphical_Abstract_A2_Landscape.svg"

    print(f"Rendering vector PDF to {pdf_out}...")
    plt.savefig(pdf_out, format='pdf', dpi=300, facecolor=BG_CANVAS)
    
    print(f"Rendering vector SVG to {svg_out}...")
    plt.savefig(svg_out, format='svg', facecolor=BG_CANVAS)

    print(f"Rendering high-resolution 300 DPI raster PNG to {png_out}...")
    plt.savefig(png_out, format='png', dpi=300, facecolor=BG_CANVAS)

    plt.close()
    print("A2 Landscape Graphical Abstract successfully created!")

if __name__ == '__main__':
    generate_a2_graphical_abstract()
