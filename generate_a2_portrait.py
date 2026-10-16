import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
import numpy as np

def generate_a2_portrait():
    # -------------------------------------------------------------
    # Page Setup: ISO A2 Portrait (420 mm x 594 mm = 16.535 x 23.386 inches)
    # -------------------------------------------------------------
    width_in = 16.535
    height_in = 23.386
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

    def draw_card(x, y, w, h, bg=CARD_BG, border=BORDER_COLOR, lw=1.5, radius=0.006, zorder=2):
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle=patches.BoxStyle("Round", pad=radius, rounding_size=radius),
            facecolor=bg, edgecolor=border, linewidth=lw, zorder=zorder
        )
        ax.add_patch(box)
        return box

    # -------------------------------------------------------------
    # 1. HEADER BANNER (Top)
    # -------------------------------------------------------------
    header_y = 0.905
    header_h = 0.095
    ax.add_patch(patches.Rectangle((0, header_y), 1, header_h, facecolor=CRIMSON, edgecolor='none', zorder=1))
    ax.add_patch(patches.Rectangle((0, header_y), 1, 0.003, facecolor=GOLD, edgecolor='none', zorder=2))

    ax.text(0.5, 0.982, "GOKARAJU RANGARAJU INSTITUTE OF ENGINEERING AND TECHNOLOGY", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#FDE68A', zorder=3, family='sans-serif')
    ax.text(0.5, 0.967, "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING  |  MAJOR PROJECT (PHASE-1)  |  2026-2027", 
            ha='center', va='center', fontsize=9, color='#E2E8F0', zorder=3, family='sans-serif')

    ax.text(0.5, 0.942, "AUTOMATED FAILURE ATTRIBUTION FOR LLM-BASED MULTI-AGENT SYSTEMS", 
            ha='center', va='center', fontsize=17, fontweight='bold', color='#FFFFFF', zorder=3)
    ax.text(0.5, 0.922, "A Graph-Causal Diagnostic Engine with Deterministic SHA-256 Prompt Caching & Backward Dependency Traversal", 
            ha='center', va='center', fontsize=10, style='italic', color='#F1F5F9', zorder=3)

    # Metadata badges in header
    ax.text(0.04, 0.910, "BATCH: B12", ha='left', va='center', fontsize=8.5, fontweight='bold', color='#FDE68A', family='sans-serif', zorder=3)
    ax.text(0.13, 0.910, "STUDENTS: R. S. Prabhaadhithya (Q3) • R. Ajay (Q4) • N. Paul (Q6) • T. Niranjan (R1)", 
            ha='left', va='center', fontsize=8, color='#FFFFFF', family='sans-serif', zorder=3)
    ax.text(0.96, 0.910, "GUIDE: Dr. D. Ushasree, Assistant Professor, Dept. of CSE", 
            ha='right', va='center', fontsize=8, fontweight='bold', color='#FDE68A', family='sans-serif', zorder=3)

    # Content margins
    cx = 0.030
    cw = 0.940

    # =============================================================
    # SECTION 1: THE MULTI-AGENT FAILURE CRISIS (Top Zone)
    # =============================================================
    s1_y = 0.655
    s1_h = 0.235
    draw_card(cx, s1_y + s1_h - 0.030, cw, 0.030, bg=CRIMSON, border=CRIMSON_DARK, zorder=3)
    ax.text(cx + 0.015, s1_y + s1_h - 0.015, "01 | THE MULTI-AGENT FAILURE CRISIS (THE PROBLEM)", 
            ha='left', va='center', fontsize=11, fontweight='bold', color='#FFFFFF', zorder=4)
    ax.text(cx + cw - 0.015, s1_y + s1_h - 0.015, "CASCADING DEFECTS & BASELINE COLLAPSE", 
            ha='right', va='center', fontsize=8.5, fontweight='bold', color='#FDE68A', family='sans-serif', zorder=4)

    # Left Box: Cascading Steps Diagram
    card1_w = 0.540
    draw_card(cx, s1_y, card1_w, s1_h - 0.035)
    ax.text(cx + 0.012, s1_y + s1_h - 0.045, "Cascading Error Propagation Across Agent Steps", 
            fontsize=10.5, fontweight='bold', color=TEXT_DARK)
    ax.text(cx + 0.012, s1_y + s1_h - 0.060, 
            "A latent defect introduced early by an upstream agent compounds silently until a downstream crash occurs.", 
            fontsize=8.5, color=TEXT_MUTED)

    steps_data = [
        ("Step 2: Planner", "Latent Defect: Hallucinates invalid API argument 'auth'", AMBER_BG, AMBER_ACCENT, "ROOT CAUSE"),
        ("Step 5: Coder", "Error Propagation: Implements logic trusting flawed argument", CARD_BG, BORDER_COLOR, "Propagated"),
        ("Step 9: Reviewer", "Blind Approval: Passes code without static execution tests", CARD_BG, BORDER_COLOR, "Propagated"),
        ("Step 14: Executor", "MANIFEST CRASH: TypeError: unexpected keyword 'auth'", RED_BG, RED_ACCENT, "CRASH (Victim)")
    ]
    by = s1_y + s1_h - 0.095
    for i, (stitle, sdesc, sbg, sbd, sbdg) in enumerate(steps_data):
        draw_card(cx + 0.012, by, card1_w - 0.024, 0.028, bg=sbg, border=sbd, lw=1.2)
        ax.text(cx + 0.020, by + 0.018, stitle, fontsize=8.5, fontweight='bold', color=TEXT_DARK)
        ax.text(cx + 0.020, by + 0.007, sdesc, fontsize=7.5, color=TEXT_MUTED)
        
        badge_c = AMBER_ACCENT if "ROOT" in sbdg else (RED_ACCENT if "CRASH" in sbdg else TEXT_MUTED)
        ax.text(cx + card1_w - 0.020, by + 0.014, sbdg, fontsize=7.5, fontweight='bold', color=badge_c, ha='right', family='sans-serif')
        
        if i < len(steps_data) - 1:
            ax.annotate("", xy=(cx + 0.035, by - 0.005), xytext=(cx + 0.035, by),
                        arrowprops=dict(arrowstyle="->", color=RED_ACCENT, lw=1.5))
        by -= 0.034

    # Backtrack Arrow
    ax.annotate("True Root Cause: Step 2 (12 steps prior)",
                xy=(cx + card1_w - 0.060, s1_y + s1_h - 0.095 + 0.014),
                xytext=(cx + card1_w - 0.080, s1_y + 0.025),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.4", 
                                color=AMBER_ACCENT, lw=1.8, linestyle='--'),
                fontsize=7.5, fontweight='bold', color=AMBER_ACCENT, ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.2", fc="#FFFBEB", ec=AMBER_ACCENT, lw=0.8))

    # Right Box: Naive Baseline Failure
    card2_w = cw - card1_w - 0.015
    draw_card(cx + card1_w + 0.015, s1_y, card2_w, s1_h - 0.035, bg=RED_BG, border=RED_ACCENT)
    ax.text(cx + card1_w + 0.025, s1_y + s1_h - 0.045, "Why Naive LLM Judges Fail", 
            fontsize=10.5, fontweight='bold', color=RED_ACCENT)
    
    # 2 Stat cards inside
    draw_card(cx + card1_w + 0.025, s1_y + 0.095, (card2_w - 0.030)/2, 0.085, bg='#FFFFFF', border=RED_ACCENT)
    ax.text(cx + card1_w + 0.025 + (card2_w - 0.030)/4, s1_y + 0.155, "14.2%", fontsize=20, fontweight='bold', color=RED_ACCENT, ha='center')
    ax.text(cx + card1_w + 0.025 + (card2_w - 0.030)/4, s1_y + 0.130, "Step Accuracy", fontsize=8, fontweight='bold', color=TEXT_DARK, ha='center')
    ax.text(cx + card1_w + 0.025 + (card2_w - 0.030)/4, s1_y + 0.110, "Fails 86% of trials", fontsize=7, color=TEXT_MUTED, ha='center')

    draw_card(cx + card1_w + 0.025 + (card2_w - 0.030)/2 + 0.010, s1_y + 0.095, (card2_w - 0.030)/2 - 0.010, 0.085, bg='#FFFFFF', border=RED_ACCENT)
    ax.text(cx + card1_w + 0.025 + 3*(card2_w - 0.030)/4, s1_y + 0.155, "26.1%", fontsize=20, fontweight='bold', color=RED_ACCENT, ha='center')
    ax.text(cx + card1_w + 0.025 + 3*(card2_w - 0.030)/4, s1_y + 0.130, "Joint Accuracy", fontsize=8, fontweight='bold', color=TEXT_DARK, ha='center')
    ax.text(cx + card1_w + 0.025 + 3*(card2_w - 0.030)/4, s1_y + 0.110, "Both Agent & Step", fontsize=7, color=TEXT_MUTED, ha='center')

    # Reasons
    ax.text(cx + card1_w + 0.025, s1_y + 0.075, "1. Severe Recency Bias: Blames Step 14 (victim).", fontsize=7.5, fontweight='bold', color=TEXT_DARK)
    ax.text(cx + card1_w + 0.025, s1_y + 0.050, "2. Context Dilution: 100+ turns exceed prompt budget.", fontsize=7.5, color=TEXT_MUTED)
    ax.text(cx + card1_w + 0.025, s1_y + 0.025, "3. Symptom Misattribution: Cannot trace causal history.", fontsize=7.5, color=TEXT_MUTED)

    # =============================================================
    # SECTION 2: THE GRAPH-CAUSAL ENGINE (Middle Zone)
    # =============================================================
    s2_y = 0.365
    s2_h = 0.275
    draw_card(cx, s2_y + s2_h - 0.030, cw, 0.030, bg=NAVY, border=NAVY_LIGHT, zorder=3)
    ax.text(cx + 0.015, s2_y + s2_h - 0.015, "02 | THE GRAPH-CAUSAL ATTRIBUTION PIPELINE (METHODOLOGY)", 
            ha='left', va='center', fontsize=11, fontweight='bold', color='#FFFFFF', zorder=4)
    ax.text(cx + cw - 0.015, s2_y + s2_h - 0.015, "DAG RECONSTRUCTION & BACKWARD TRAVERSAL", 
            ha='right', va='center', fontsize=8.5, fontweight='bold', color=GOLD, family='sans-serif', zorder=4)

    # Left: Pipeline + Mathematical Models
    m_left_w = 0.460
    draw_card(cx, s2_y, m_left_w, s2_h - 0.035)
    ax.text(cx + 0.012, s2_y + s2_h - 0.045, "4-Stage Causal Attribution Stack", 
            fontsize=10.5, fontweight='bold', color=TEXT_DARK)
    
    pipe_boxes = [
        ("1. Ingestion & Budgeting", "Standardizes Pydantic ExecutionSteps (≤4096 tokens)."),
        ("2. SHA-256 Prompt Cache", "O(1) hash lookup (<1.5ms); eliminates redundant LLM calls."),
        ("3. Causal DAG Builder", "Infers message, temporal & state mutation dependencies."),
        ("4. Backward Traversal", "Backtracks along causal closure Anc(m) to earliest defect.")
    ]
    py = s2_y + s2_h - 0.080
    for title, desc in pipe_boxes:
        draw_card(cx + 0.012, py, m_left_w - 0.024, 0.026, bg=BLUE_BG, border=BLUE_ACCENT, lw=1)
        ax.text(cx + 0.020, py + 0.016, title, fontsize=8, fontweight='bold', color=BLUE_ACCENT)
        ax.text(cx + 0.020, py + 0.006, desc, fontsize=7, color=TEXT_MUTED)
        py -= 0.031

    # Formulas in left card
    ax.text(cx + 0.012, s2_y + 0.080, "Mathematical Invariants & Formulations:", fontsize=8.5, fontweight='bold', color=TEXT_DARK)
    ax.text(cx + 0.015, s2_y + 0.055, r"• $e = (u, v) \in E_{\mathrm{dag}} \Rightarrow \mathrm{time}(u) < \mathrm{time}(v)$ [Acyclicity]", fontsize=8, color=CRIMSON)
    ax.text(cx + 0.015, s2_y + 0.035, r"• $k_{\mathrm{cache}} = \mathrm{SHA256}( \mathrm{prompt} \parallel \mathrm{agent} \parallel \mathrm{payload} )$ [<1.5ms]", fontsize=8, color=CRIMSON)
    ax.text(cx + 0.015, s2_y + 0.015, r"• $s^* = \arg\min_{s \in \mathrm{Anc}(m)} \{ \mathrm{idx}(s) \mid \mathrm{anomalous}(s) = \mathrm{True} \}$", fontsize=8, color=CRIMSON)

    # Right: The Causal DAG Network Diagram
    m_right_w = cw - m_left_w - 0.015
    draw_card(cx + m_left_w + 0.015, s2_y, m_right_w, s2_h - 0.035)
    ax.text(cx + m_left_w + 0.025, s2_y + s2_h - 0.045, "Causal DAG & Ancestor Closure Anc(m)", 
            fontsize=10.5, fontweight='bold', color=TEXT_DARK)
    ax.text(cx + m_left_w + 0.025, s2_y + s2_h - 0.060, 
            "Non-causal branches (S3, S7) are pruned, reducing complexity from O(N) to O(|Anc(m)|).", 
            fontsize=8, color=TEXT_MUTED)

    # Diagram nodes in portrait
    gx_base = cx + m_left_w + 0.030
    p_dag_nodes = {
        "S1": (gx_base + 0.030, s2_y + 0.120, "S1: User\nGoal", CARD_BG, BORDER_COLOR, TEXT_DARK),
        "S2": (gx_base + 0.120, s2_y + 0.170, "S2: Planner\n(Root Defect)", AMBER_BG, AMBER_ACCENT, AMBER_ACCENT),
        "S3": (gx_base + 0.120, s2_y + 0.070, "S3: WebSearch\n(Unrelated)", "#F1F5F9", BORDER_COLOR, "#94A3B8"),
        "S5": (gx_base + 0.220, s2_y + 0.170, "S5: Coder\n(Propagated)", BLUE_BG, BLUE_ACCENT, TEXT_DARK),
        "S7": (gx_base + 0.220, s2_y + 0.070, "S7: DocGen\n(Unrelated)", "#F1F5F9", BORDER_COLOR, "#94A3B8"),
        "S9": (gx_base + 0.310, s2_y + 0.170, "S9: Reviewer\n(Propagated)", BLUE_BG, BLUE_ACCENT, TEXT_DARK),
        "S14": (gx_base + 0.380, s2_y + 0.120, "S14: Exec\n(Crash!)", RED_BG, RED_ACCENT, RED_ACCENT)
    }
    p_dag_edges = [
        ("S1", "S2", True), ("S1", "S3", False),
        ("S2", "S5", True), ("S3", "S7", False),
        ("S5", "S9", True), ("S9", "S14", True),
        ("S7", "S14", False)
    ]
    for u, v, is_c in p_dag_edges:
        p1 = p_dag_nodes[u]
        p2 = p_dag_nodes[v]
        ec = RED_ACCENT if is_c else "#CBD5E1"
        elw = 1.8 if is_c else 0.9
        ax.annotate("", xy=(p2[0]-0.020, p2[1]), xytext=(p1[0]+0.020, p1[1]),
                    arrowprops=dict(arrowstyle="->", color=ec, lw=elw, linestyle='-' if is_c else '--'))

    for k, (nx, ny, nlbl, nbg, nbd, ntc) in p_dag_nodes.items():
        draw_card(nx - 0.028, ny - 0.024, 0.056, 0.048, bg=nbg, border=nbd, lw=1.6 if k in ["S2", "S14"] else 1.0)
        ax.text(nx, ny, nlbl, ha='center', va='center', fontsize=7, fontweight='bold', color=ntc)

    draw_card(cx + m_left_w + 0.025, s2_y + 0.015, m_right_w - 0.025, 0.028, bg="#F8FAFC", border=BORDER_COLOR)
    ax.text(cx + m_left_w + 0.035, s2_y + 0.029, "RED ARROWS: Causal Closure Anc(m) = {S2, S5, S9, S14}", 
            fontsize=7.5, fontweight='bold', color=CRIMSON, family='sans-serif')
    ax.text(cx + cw - 0.015, s2_y + 0.029, "S3, S7 Pruned (Zero Evaluation Cost)", 
            fontsize=7.5, color=TEXT_MUTED, ha='right', family='sans-serif')

    # =============================================================
    # SECTION 3: EMPIRICAL VALIDATION & RESULTS (Bottom Zone)
    # =============================================================
    s3_y = 0.080
    s3_h = 0.270
    draw_card(cx, s3_y + s3_h - 0.030, cw, 0.030, bg=EMERALD, border="#047857", zorder=3)
    ax.text(cx + 0.015, s3_y + s3_h - 0.015, "03 | EMPIRICAL VALIDATION & SYSTEM DELIVERABLES (RESULTS)", 
            ha='left', va='center', fontsize=11, fontweight='bold', color='#FFFFFF', zorder=4)
    ax.text(cx + cw - 0.015, s3_y + s3_h - 0.015, "ICML 2025 WHO&WHEN BENCHMARK & PYTEST VERIFIED", 
            ha='right', va='center', fontsize=8.5, fontweight='bold', color='#A7F3D0', family='sans-serif', zorder=4)

    # Left: 4 Big Metrics
    r_left_w = 0.380
    draw_card(cx, s3_y, r_left_w, s3_h - 0.035)
    ax.text(cx + 0.012, s3_y + s3_h - 0.045, "Who&When Benchmark Performance", 
            fontsize=10.5, fontweight='bold', color=TEXT_DARK)

    r_kpis = [
        ("86.96%", "Joint Attribution Acc", "+60.87% over baseline", EMERALD),
        ("91.30%", "Agent Localization", "21 / 23 benchmarks", BLUE_ACCENT),
        ("0.44 s", "Traversal Latency", "Sub-second execution", TEXT_DARK),
        ("14.2x", "Cache Speedup", "< 1.5ms hit latency", AMBER_ACCENT)
    ]
    for idx, (num, lbl, sub, col) in enumerate(r_kpis):
        r = idx // 2
        c = idx % 2
        kx = cx + 0.012 + c * ((r_left_w - 0.032)/2 + 0.008)
        ky = s3_y + s3_h - 0.085 - r * 0.065
        draw_card(kx, ky, (r_left_w - 0.032)/2, 0.058, bg='#F8FAFC', border=BORDER_COLOR)
        ax.text(kx + 0.008, ky + 0.034, num, fontsize=16, fontweight='bold', color=col)
        ax.text(kx + 0.008, ky + 0.018, lbl, fontsize=8, fontweight='bold', color=TEXT_DARK)
        ax.text(kx + 0.008, ky + 0.006, sub, fontsize=7, color=TEXT_MUTED)

    draw_card(cx + 0.012, s3_y + 0.012, r_left_w - 0.024, 0.045, bg=EMERALD_BG, border=EMERALD)
    ax.text(cx + 0.020, s3_y + 0.042, "27 / 27 UNIT TESTS PASSED (100%)", fontsize=9.5, fontweight='bold', color=EMERALD)
    ax.text(cx + 0.020, s3_y + 0.024, "Total test execution: 1.84s across 9 modules (pytest v8.3)", fontsize=7.5, color=TEXT_MUTED)

    # Middle: Accuracy Bar Chart
    r_mid_w = 0.310
    draw_card(cx + r_left_w + 0.015, s3_y, r_mid_w, s3_h - 0.035)
    ax.text(cx + r_left_w + 0.025, s3_y + s3_h - 0.045, "Joint Accuracy Comparison", 
            fontsize=10.5, fontweight='bold', color=TEXT_DARK)

    p_bars = [
        ("Naive LLM\nJudge", 26.09, RED_ACCENT),
        ("Step-by-Step\nEvaluation", 43.48, "#94A3B8"),
        ("Binary\nSearch", 65.22, BLUE_ACCENT),
        ("Our Causal\nEngine", 86.96, EMERALD)
    ]
    p_chart_y = s3_y + 0.040
    p_chart_h = 0.130
    p_bw = 0.045
    p_gap = (r_mid_w - 0.050 - 4 * p_bw) / 3

    for i, (bname, bval, bcol) in enumerate(p_bars):
        bx = cx + r_left_w + 0.025 + i * (p_bw + p_gap)
        nh = (bval / 100.0) * p_chart_h
        ax.add_patch(patches.Rectangle((bx, p_chart_y), p_bw, nh, facecolor=bcol, edgecolor='none', zorder=3))
        ax.text(bx + p_bw/2, p_chart_y + nh + 0.005, f"{bval:.1f}%", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color=bcol)
        ax.text(bx + p_bw/2, p_chart_y - 0.008, bname, ha='center', va='top', fontsize=7, color=TEXT_DARK, linespacing=1.1)

    ax.plot([cx + r_left_w + 0.020, cx + r_left_w + r_mid_w - 0.020], [p_chart_y, p_chart_y], color=BORDER_COLOR, lw=1.2)

    # Right: Deliverables & UI
    r_right_w = cw - r_left_w - r_mid_w - 0.030
    draw_card(cx + r_left_w + r_mid_w + 0.030, s3_y, r_right_w, s3_h - 0.035)
    ax.text(cx + r_left_w + r_mid_w + 0.040, s3_y + s3_h - 0.045, "Delivered Interfaces", 
            fontsize=10.5, fontweight='bold', color=TEXT_DARK)
    deliv_text = (
        "• agent-trace CLI:\n"
        "  Full CLI with diagnose, benchmark\n"
        "  and log-watch modes.\n\n"
        "• FastAPI REST Server:\n"
        "  8 documented endpoints with\n"
        "  interactive Swagger API docs.\n\n"
        "• Streamlit UI Dashboard:\n"
        "  PyVis network visualizer with\n"
        "  interactive causal path triage.\n\n"
        "• Dockerized Stack:\n"
        "  One-click container setup."
    )
    ax.text(cx + r_left_w + r_mid_w + 0.040, s3_y + s3_h - 0.065, deliv_text, 
            fontsize=7.5, color=TEXT_MUTED, va='top', linespacing=1.2)

    # -------------------------------------------------------------
    # 4. FOOTER BANNER (Bottom)
    # -------------------------------------------------------------
    footer_y = 0.015
    footer_h = 0.055
    ax.add_patch(patches.Rectangle((0, footer_y), 1, footer_h, facecolor=NAVY, edgecolor='none', zorder=1))
    ax.add_patch(patches.Rectangle((0, footer_y + footer_h - 0.002), 1, 0.002, facecolor=GOLD, edgecolor='none', zorder=2))

    f_p_w = cw / 4
    for idx, (title, desc) in enumerate([
        ("Causal Provenance", "Replaces monolithic prompting with formal DAG ancestor closures."),
        ("Token Boundedness", "Strict ≤4096-token segmentation eliminates context dilution."),
        ("Deterministic Cache", "SHA-256 prompt hashing guarantees <1.5ms lookups with 14.2x speedup."),
        ("Empirically Verified", "86.96% Joint Accuracy on Who&When benchmark (27/27 tests passed).")
    ]):
        fx = cx + idx * f_p_w
        ax.text(fx, footer_y + 0.034, f"0{idx+1} | {title.upper()}", fontsize=8.5, fontweight='bold', color=GOLD, family='sans-serif', zorder=3)
        ax.text(fx, footer_y + 0.014, desc, fontsize=7, color='#E2E8F0', family='sans-serif', zorder=3)

    # -------------------------------------------------------------
    # 5. Save Outputs
    # -------------------------------------------------------------
    pdf_out = "media/graphical_abstract/Graphical_Abstract_A2_Portrait.pdf"
    png_out = "media/graphical_abstract/Graphical_Abstract_A2_Portrait.png"
    svg_out = "media/graphical_abstract/Graphical_Abstract_A2_Portrait.svg"

    print(f"Rendering vector PDF to {pdf_out}...")
    plt.savefig(pdf_out, format='pdf', dpi=300, facecolor=BG_CANVAS)
    
    print(f"Rendering vector SVG to {svg_out}...")
    plt.savefig(svg_out, format='svg', facecolor=BG_CANVAS)

    print(f"Rendering high-resolution 300 DPI raster PNG to {png_out}...")
    plt.savefig(png_out, format='png', dpi=300, facecolor=BG_CANVAS)

    plt.close()
    print("A2 Portrait Graphical Abstract successfully created!")

if __name__ == '__main__':
    generate_a2_portrait()
