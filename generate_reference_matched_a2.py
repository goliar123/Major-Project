import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
import numpy as np

def generate_reference_matched_a2():
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

    # Typography setup: clean modern sans-serif matching reference
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Liberation Sans', 'Arial', 'Helvetica']
    plt.rcParams['font.family'] = 'sans-serif'

    # Color Palette from reference image
    BG_CANVAS = "#F8FAFC"
    HEADER_BG = "#0B1D3A"        # Deep midnight navy
    HEADER_SUB = "#38BDF8"       # Cyan accent
    CARD_BG = "#FFFFFF"
    BORDER_LIGHT = "#E2E8F0"
    BORDER_DARK = "#CBD5E1"
    
    TEXT_MAIN = "#0F172A"
    TEXT_MUTED = "#475569"
    TEXT_LIGHT = "#94A3B8"
    
    # Semantic Colors from reference:
    GREEN_CLEAN = "#059669"
    GREEN_BG = "#ECFDF5"
    RED_ROOT = "#DC2626"
    RED_BG = "#FEF2F2"
    AMBER_PROP = "#D97706"
    AMBER_BG = "#FFFBEB"
    CRASH_DARK = "#881337"
    CRASH_BG = "#FFE4E6"
    
    PURPLE_HEADER = "#6D28D9"    # Solution cards header
    PURPLE_CARD_BORDER = "#8B5CF6"
    
    # Solution badges
    BADGE_NEURAL = "#2563EB"     # Blue
    BADGE_SYMBOLIC = "#7C3AED"   # Purple
    BADGE_ENG = "#1E293B"        # Dark slate
    
    # Results bar colors
    BAR_ALL_AT_ONCE = "#CBD5E1"  # Light gray
    BAR_STEP_BY_STEP = "#64748B" # Slate
    BAR_BINARY_SEARCH = "#334155"# Dark slate
    BAR_OURS = "#0D9488"         # Vibrant teal/cyan

    # Background fill
    ax.add_patch(patches.Rectangle((0, 0), 1, 1, facecolor=BG_CANVAS, edgecolor='none', zorder=0))

    def draw_card(x, y, w, h, bg=CARD_BG, border=BORDER_LIGHT, lw=1.2, radius=0.006, zorder=2):
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle=patches.BoxStyle("Round", pad=radius, rounding_size=radius),
            facecolor=bg, edgecolor=border, linewidth=lw, zorder=zorder
        )
        ax.add_patch(box)
        return box

    def draw_circle_num(cx, cy, num, radius=0.010, bg="#1E293B", text_color="#FFFFFF", zorder=4):
        c = patches.Circle((cx, cy), radius, facecolor=bg, edgecolor='none', zorder=zorder)
        ax.add_patch(c)
        ax.text(cx, cy, str(num), ha='center', va='center', fontsize=12, fontweight='bold', 
                color=text_color, zorder=zorder+1)

    # =============================================================
    # 1. HEADER (Deep Midnight Navy)
    # =============================================================
    head_y = 0.880
    head_h = 0.120
    ax.add_patch(patches.Rectangle((0, head_y), 1, head_h, facecolor=HEADER_BG, edgecolor='none', zorder=1))
    
    # Thin cyan accent line below header
    ax.add_patch(patches.Rectangle((0, head_y), 1, 0.003, facecolor="#0284C7", edgecolor='none', zorder=2))

    # Main Title
    ax.text(0.5, 0.962, "Automated Failure Attribution for LLM-Based Multi-Agent Systems", 
            ha='center', va='center', fontsize=26, fontweight='bold', color='#FFFFFF', zorder=3)
    
    # Subtitle
    ax.text(0.5, 0.932, "A Neuro-Symbolic Causal Graph Engine that finds the root cause — not the crash site", 
            ha='center', va='center', fontsize=14, color='#E0F2FE', zorder=3)

    # Authors and Affiliation in header
    meta_y = 0.898
    authors_str = "Rachapalli S Prabhaadhithya  ·  Rathod Ajay  ·  Noel Paul  ·  Talagapu Niranjan"
    guide_str = "Guide: Dr. D. Ushasree  ·  Dept. of CSE, GRIET  ·  Major Project Phase-I, 2026–27"
    ax.text(0.030, meta_y, authors_str, ha='left', va='center', fontsize=10.5, color='#CBD5E1', zorder=3)
    ax.text(0.970, meta_y, guide_str, ha='right', va='center', fontsize=10.5, color='#CBD5E1', zorder=3)

    # Common content bounds
    left_m = 0.025
    right_m = 0.975
    full_w = right_m - left_m

    # =============================================================
    # 2. SECTION 1: THE PROBLEM: Symptom Misattribution
    # =============================================================
    s1_top = 0.850
    draw_circle_num(left_m + 0.012, s1_top - 0.015, 1, radius=0.009, bg="#1E293B")
    ax.text(left_m + 0.028, s1_top - 0.015, "THE PROBLEM: Symptom Misattribution", 
            ha='left', va='center', fontsize=15, fontweight='bold', color=TEXT_MAIN)

    problem_desc = (
        "In multi-agent LLM pipelines an early, silent error is passed downstream as if it were truth, "
        "and the system finally crashes at an agent that did nothing wrong. Monitoring tools and monolithic LLM\n"
        "judges blame the crash site (recency bias)."
    )
    ax.text(left_m + 0.028, s1_top - 0.038, problem_desc, 
            ha='left', va='top', fontsize=10, color=TEXT_MUTED, linespacing=1.3)

    # 6 Step Workflow Cards
    steps_y = 0.690
    step_h = 0.082
    num_steps = 6
    step_w = (full_w - (num_steps - 1) * 0.016) / num_steps

    step_data = [
        ("STEP 0", "Planner", "splits audit into subtasks", GREEN_BG, GREEN_CLEAN, False, None),
        ("STEP 1", "Search Agent", "fetches SEC filings", GREEN_BG, GREEN_CLEAN, False, None),
        ("STEP 2", "Writer Agent", 'margin value → "NaN"', RED_BG, RED_ROOT, True, "ROOT CAUSE"),
        ("STEP 3", "Computation Worker", "carries NaN forward", AMBER_BG, AMBER_PROP, False, None),
        ("STEP 4", "Risk Auditor", "approves the text", AMBER_BG, AMBER_PROP, False, None),
        ("STEP 5", "DB Architect", "Pydantic ValidationError", CRASH_BG, CRASH_DARK, True, "MANIFEST CRASH")
    ]

    # Shared badge for Propagated Symptoms over steps 3 and 4
    prop_x1 = left_m + 3 * (step_w + 0.016)
    prop_x2 = left_m + 4 * (step_w + 0.016) + step_w
    prop_w = prop_x2 - prop_x1
    prop_badge = patches.FancyBboxPatch(
        (prop_x1 + (prop_w - 0.160)/2, steps_y + step_h + 0.008), 0.160, 0.018,
        boxstyle=patches.BoxStyle("Round", pad=0.003, rounding_size=0.003),
        facecolor=AMBER_PROP, edgecolor='none', zorder=3
    )
    ax.add_patch(prop_badge)
    ax.text(prop_x1 + prop_w/2, steps_y + step_h + 0.017, "PROPAGATED SYMPTOMS", 
            ha='center', va='center', fontsize=8, fontweight='bold', color='#FFFFFF', zorder=4)

    for i, (s_num, s_name, s_sub, bg_c, b_c, has_badge, badge_txt) in enumerate(step_data):
        sx = left_m + i * (step_w + 0.016)
        
        # Draw badge above card if present
        if has_badge and badge_txt:
            b_bg = RED_ROOT if "ROOT" in badge_txt else CRASH_DARK
            badge_box = patches.FancyBboxPatch(
                (sx + (step_w - 0.110)/2, steps_y + step_h + 0.008), 0.110, 0.018,
                boxstyle=patches.BoxStyle("Round", pad=0.003, rounding_size=0.003),
                facecolor=b_bg, edgecolor='none', zorder=3
            )
            ax.add_patch(badge_box)
            ax.text(sx + step_w/2, steps_y + step_h + 0.017, badge_txt, 
                    ha='center', va='center', fontsize=8, fontweight='bold', color='#FFFFFF', zorder=4)

        # Step card
        draw_card(sx, steps_y, step_w, step_h, bg=bg_c, border=b_c, lw=1.8, radius=0.006)
        
        # Step text
        ax.text(sx + step_w/2, steps_y + step_h - 0.016, s_num, 
                ha='center', va='center', fontsize=9.5, fontweight='bold', color=b_c)
        ax.text(sx + step_w/2, steps_y + step_h - 0.038, s_name, 
                ha='center', va='center', fontsize=11, fontweight='bold', color=TEXT_MAIN)
        ax.text(sx + step_w/2, steps_y + 0.018, s_sub, 
                ha='center', va='center', fontsize=8.5, color=TEXT_MUTED)

        # Horizontal connecting arrow between steps
        if i < num_steps - 1:
            ax.annotate("", xy=(sx + step_w + 0.014, steps_y + step_h/2), 
                        xytext=(sx + step_w + 0.002, steps_y + step_h/2),
                        arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.8), zorder=3)

    # Backward Causal Traversal Arrow from Step 5 to Step 2
    # Start: Step 5 bottom center; End: Step 2 bottom center
    s5_center_x = left_m + 5 * (step_w + 0.016) + step_w/2
    s2_center_x = left_m + 2 * (step_w + 0.016) + step_w/2
    arrow_y = steps_y - 0.010
    
    ax.annotate("", xy=(s2_center_x, steps_y - 0.003), 
                xytext=(s5_center_x, steps_y - 0.003),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.08", 
                                color=GREEN_CLEAN, lw=2.2, linestyle='--'), zorder=4)
    
    # Label on the green dashed arrow
    mid_x = (s5_center_x + s2_center_x) / 2
    ax.text(mid_x, arrow_y - 0.012, "backward causal traversal from the crash", 
            ha='center', va='center', fontsize=9.5, fontweight='bold', color=GREEN_CLEAN, zorder=5)

    # Two comparison outcome cards below Problem workflow
    sub_y = 0.612
    sub_h = 0.040
    sub_w = (full_w - 0.020) / 2
    
    # Left: Pink failure card
    draw_card(left_m, sub_y, sub_w, sub_h, bg="#FEF2F2", border="#FECACA", lw=1.2)
    ax.text(left_m + 0.015, sub_y + sub_h/2, "✗", ha='center', va='center', fontsize=16, fontweight='bold', color=RED_ROOT)
    ax.text(left_m + 0.035, sub_y + sub_h/2, "Baselines blame Step 5: only 14.2% step-level accuracy (All-at-Once LLM judge)", 
            ha='left', va='center', fontsize=9.5, fontweight='bold', color=RED_ROOT)

    # Right: Green success card
    draw_card(left_m + sub_w + 0.020, sub_y, sub_w, sub_h, bg="#ECFDF5", border="#A7F3D0", lw=1.2)
    ax.text(left_m + sub_w + 0.035, sub_y + sub_h/2, "✓", ha='center', va='center', fontsize=16, fontweight='bold', color=GREEN_CLEAN)
    ax.text(left_m + sub_w + 0.055, sub_y + sub_h/2, "Our engine walks the dependency DAG backward and isolates Step 2 as the true origin", 
            ha='left', va='center', fontsize=9.5, fontweight='bold', color=GREEN_CLEAN)

    # =============================================================
    # 3. SECTION 2: THE SOLUTION: Neuro-Symbolic Causal Graph Engine
    # =============================================================
    s2_top = 0.575
    draw_circle_num(left_m + 0.012, s2_top - 0.015, 2, radius=0.009, bg="#1E293B")
    ax.text(left_m + 0.028, s2_top - 0.015, "THE SOLUTION: Neuro-Symbolic Causal Graph Engine", 
            ha='left', va='center', fontsize=15, fontweight='bold', color=TEXT_MAIN)

    # Legend on the right of Section 2
    legend_y = s2_top - 0.015
    leg_x = right_m - 0.320
    # Blue: Neural
    ax.plot(leg_x, legend_y, 'o', color=BADGE_NEURAL, markersize=8)
    ax.text(leg_x + 0.010, legend_y, "Neural (local LLM)", fontsize=9, color=TEXT_MUTED, va='center')
    # Purple: Symbolic
    leg_x2 = leg_x + 0.115
    ax.plot(leg_x2, legend_y, 'o', color=BADGE_SYMBOLIC, markersize=8)
    ax.text(leg_x2 + 0.010, legend_y, "Symbolic (graph algorithms)", fontsize=9, color=TEXT_MUTED, va='center')
    # Dark Slate: Engineering
    leg_x3 = leg_x2 + 0.135
    ax.plot(leg_x3, legend_y, 'o', color=BADGE_ENG, markersize=8)
    ax.text(leg_x3 + 0.010, legend_y, "Engineering", fontsize=9, color=TEXT_MUTED, va='center')

    # 5 Architecture Solution Cards
    sol_y = 0.355
    sol_h = 0.185
    num_sol = 5
    sol_w = (full_w - (num_sol - 1) * 0.016) / num_sol

    sol_cards = [
        (1, "Trace Segmentation &\nToken Budgeting",
         "Parses AutoGen, LangGraph,\nCrewAI and MetaGPT logs into\nExecutionSteps. 60% head / 30%\ntail retention keeps prompts inside\na 4,096-token budget.",
         BADGE_ENG, "ENGINEERING"),
         
        (2, "Cached Semantic Step\nEvaluation",
         "Local Qwen2.5:7b (Ollama, JSON\nmode) scores each turn in isolation.\nSHA256 cache (memory + SQLite)\nremoves redundant inference;\nMockJudge is the offline fallback.",
         BADGE_NEURAL, "NEURAL"),
         
        (3, "Dependency DAG\nSynthesis",
         "NetworkX DiGraph with sequential\nedges (confidence 0.85) and\nregex-extracted variable data-flow\nedges (confidence 0.95).",
         BADGE_SYMBOLIC, "SYMBOLIC"),
         
        (4, "Backward Causal\nTraversal",
         "Computes the Transitive Ancestor\nClosure of the crash, then blames\nthe earliest anomaly whose parents\nare all clean (Clean-Parent\nInvariant).",
         BADGE_SYMBOLIC, "SYMBOLIC"),
         
        (5, "2D Taxonomy & Visual\nReport",
         "Causal Role × 25+ bug categories,\nshortest causal chain (Dijkstra),\nStreamlit dashboard and FastAPI\nREST endpoints for CI/CD.",
         BADGE_ENG, "ENGINEERING")
    ]

    for idx, (c_num, c_title, c_desc, b_color, b_label) in enumerate(sol_cards):
        cx = left_m + idx * (sol_w + 0.016)
        
        # Outer Card Box
        draw_card(cx, sol_y, sol_w, sol_h, bg=CARD_BG, border=PURPLE_CARD_BORDER, lw=1.5, radius=0.008)
        
        # Top Purple Banner
        banner_h = 0.048
        banner_box = patches.FancyBboxPatch(
            (cx, sol_y + sol_h - banner_h), sol_w, banner_h,
            boxstyle=patches.BoxStyle("Round", pad=0.008, rounding_size=0.008),
            facecolor=PURPLE_HEADER, edgecolor='none', zorder=3
        )
        ax.add_patch(banner_box)
        
        # Number badge in top-left of banner
        num_circle = patches.Circle((cx + 0.016, sol_y + sol_h - banner_h/2), 0.009, 
                                    facecolor='#FFFFFF', edgecolor='none', zorder=4)
        ax.add_patch(num_circle)
        ax.text(cx + 0.016, sol_y + sol_h - banner_h/2, str(c_num), 
                ha='center', va='center', fontsize=9.5, fontweight='bold', color=PURPLE_HEADER, zorder=5)

        # Title in banner
        ax.text(cx + 0.032, sol_y + sol_h - banner_h/2, c_title, 
                ha='left', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF', zorder=4, linespacing=1.1)

        # Card description
        ax.text(cx + 0.012, sol_y + sol_h - banner_h - 0.014, c_desc, 
                ha='left', va='top', fontsize=8.2, color=TEXT_MUTED, linespacing=1.28)

        # Bottom Pill Badge
        badge_box = patches.FancyBboxPatch(
            (cx + 0.012, sol_y + 0.012), 0.080, 0.016,
            boxstyle=patches.BoxStyle("Round", pad=0.002, rounding_size=0.002),
            facecolor=b_color, edgecolor='none', zorder=3
        )
        ax.add_patch(badge_box)
        ax.text(cx + 0.052, sol_y + 0.020, b_label, 
                ha='center', va='center', fontsize=7.5, fontweight='bold', color='#FFFFFF', zorder=4)

        # Arrow connecting cards
        if idx < num_sol - 1:
            ax.annotate("", xy=(cx + sol_w + 0.014, sol_y + sol_h/2), 
                        xytext=(cx + sol_w + 0.002, sol_y + sol_h/2),
                        arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.8), zorder=3)

    # =============================================================
    # 4. BOTTOM ROW: 3 PANELS (Isolation, Results, Outcomes)
    # =============================================================
    bot_y = 0.048
    bot_h = 0.275

    p1_w = 0.305
    p2_w = 0.415
    p3_w = full_w - p1_w - p2_w - 0.030

    p1_x = left_m
    p2_x = p1_x + p1_w + 0.015
    p3_x = p2_x + p2_w + 0.015

    # -------------------------------------------------------------
    # PANEL 3: ROOT-CAUSE ISOLATION
    # -------------------------------------------------------------
    draw_card(p1_x, bot_y, p1_w, bot_h)
    draw_circle_num(p1_x + 0.018, bot_y + bot_h - 0.020, 3, radius=0.008, bg="#1E293B")
    ax.text(p1_x + 0.032, bot_y + bot_h - 0.020, "ROOT-CAUSE ISOLATION", 
            ha='left', va='center', fontsize=12, fontweight='bold', color=TEXT_MAIN)

    # Node chain graph S0 -> S1 -> S2 -> S3 -> S4 -> S5
    node_names = ["S0", "S1", "S2", "S3", "S4", "S5"]
    node_colors = [GREEN_CLEAN, GREEN_CLEAN, RED_ROOT, AMBER_PROP, AMBER_PROP, CRASH_DARK]
    node_y = bot_y + 0.170
    node_spacing = (p1_w - 0.040) / 5
    
    node_coords = []
    for i, (n_name, n_col) in enumerate(zip(node_names, node_colors)):
        nx = p1_x + 0.020 + i * node_spacing
        node_coords.append((nx, node_y))
        
        # Draw node circle
        nc = patches.Circle((nx, node_y), 0.012, facecolor=n_col, edgecolor='none', zorder=4)
        ax.add_patch(nc)
        ax.text(nx, node_y, n_name, ha='center', va='center', fontsize=9, fontweight='bold', color='#FFFFFF', zorder=5)

    # Solid sequential edges
    for i in range(len(node_coords) - 1):
        x1, y1 = node_coords[i]
        x2, y2 = node_coords[i+1]
        ax.annotate("", xy=(x2 - 0.013, y2), xytext=(x1 + 0.013, y1),
                    arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.5), zorder=3)

    # Dashed data-flow edge from S2 to S5 or S4 (curved above)
    s2_x, s2_y = node_coords[2]
    s5_x, s5_y = node_coords[5]
    ax.annotate("", xy=(s5_x - 0.008, s5_y + 0.012), xytext=(s2_x + 0.008, s2_y + 0.012),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.4", 
                                color="#0284C7", lw=1.8, linestyle='--'), zorder=4)

    # Graph details text below
    ax.text(p1_x + p1_w/2, bot_y + 0.125, "Ancestor closure Anc(S5) = {S0 … S4}", 
            ha='center', va='center', fontsize=9, fontweight='bold', color=TEXT_MAIN)
    
    # Legend line
    ax.plot([p1_x + 0.030, p1_x + 0.050], [bot_y + 0.100, bot_y + 0.100], color="#0F172A", lw=1.5)
    ax.text(p1_x + 0.055, bot_y + 0.100, "sequential edge (0.85)", fontsize=7.8, color=TEXT_MUTED, va='center')
    ax.plot([p1_x + 0.165, p1_x + 0.185], [bot_y + 0.100, bot_y + 0.100], color="#0284C7", lw=1.8, linestyle='--')
    ax.text(p1_x + 0.190, bot_y + 0.100, "data-flow (0.95)", fontsize=7.8, color=TEXT_MUTED, va='center')

    # Root cause callout box at bottom of panel 1
    callout_box = patches.FancyBboxPatch(
        (p1_x + 0.012, bot_y + 0.018), p1_w - 0.024, 0.050,
        boxstyle=patches.BoxStyle("Round", pad=0.004, rounding_size=0.004),
        facecolor="#FEF2F2", edgecolor="#FECACA", lw=1.2, zorder=3
    )
    ax.add_patch(callout_box)
    ax.text(p1_x + p1_w/2, bot_y + 0.043, 
            "Earliest anomaly with clean parents → S2 = ROOT CAUSE", 
            ha='center', va='center', fontsize=8.8, fontweight='bold', color=RED_ROOT, zorder=4)

    # -------------------------------------------------------------
    # PANEL 4: RESULTS · ICML 2025 Who&When (184 traces)
    # -------------------------------------------------------------
    draw_card(p2_x, bot_y, p2_w, bot_h)
    draw_circle_num(p2_x + 0.018, bot_y + bot_h - 0.020, 4, radius=0.008, bg="#1E293B")
    ax.text(p2_x + 0.032, bot_y + bot_h - 0.020, "RESULTS · ICML 2025 Who&When (184 traces)", 
            ha='left', va='center', fontsize=12, fontweight='bold', color=TEXT_MAIN)

    # Legend for bar chart
    leg_y = bot_y + bot_h - 0.045
    leg_items = [
        (BAR_ALL_AT_ONCE, "All-at-Once"),
        (BAR_STEP_BY_STEP, "Step-by-Step"),
        (BAR_BINARY_SEARCH, "Binary Search"),
        (BAR_OURS, "Ours")
    ]
    lx = p2_x + 0.045
    for b_c, b_lbl in leg_items:
        ax.add_patch(patches.Rectangle((lx, leg_y - 0.004), 0.012, 0.008, facecolor=b_c, edgecolor='none'))
        ax.text(lx + 0.016, leg_y, b_lbl, fontsize=8, color=TEXT_MUTED, va='center')
        lx += 0.082

    # Grouped Bar Chart
    # Values from reference image:
    # Who: All-at-Once: 53.5, Step-by-Step: 62.1, Binary Search: 68.4, Ours: 85.3
    # When: All-at-Once: 14.2, Step-by-Step: 35.6, Binary Search: 41.7, Ours: 78.3
    chart_bx = p2_x + 0.045
    chart_by = bot_y + 0.045
    chart_bw = p2_w - 0.065
    chart_bh = 0.150

    # Gridlines and Y-ticks
    yticks = [0.25, 0.50, 0.75, 1.00]
    for yt in yticks:
        y_pos = chart_by + yt * chart_bh
        ax.plot([chart_bx, chart_bx + chart_bw], [y_pos, y_pos], color="#E2E8F0", lw=0.8, linestyle=':', zorder=1)
        ax.text(chart_bx - 0.008, y_pos, f"{int(yt*100)}%", ha='right', va='center', fontsize=7.5, color=TEXT_LIGHT)

    # Baseline axis
    ax.plot([chart_bx, chart_bx + chart_bw], [chart_by, chart_by], color="#CBD5E1", lw=1.2, zorder=2)

    group_data = [
        ("Who (agent-level)", [53.5, 62.1, 68.4, 85.3]),
        ("When (step-level)", [14.2, 35.6, 41.7, 78.3])
    ]
    
    gw = chart_bw / 2
    bar_width = 0.022
    bar_gap = 0.004

    for g_idx, (g_title, g_vals) in enumerate(group_data):
        gx = chart_bx + g_idx * gw + (gw - (4 * bar_width + 3 * bar_gap)) / 2
        for b_idx, val in enumerate(g_vals):
            bx = gx + b_idx * (bar_width + bar_gap)
            b_height = (val / 100.0) * chart_bh
            b_color = leg_items[b_idx][0]
            
            # Draw bar
            ax.add_patch(patches.Rectangle((bx, chart_by), bar_width, b_height, 
                                           facecolor=b_color, edgecolor='none', zorder=3))
            
            # Top value label
            ax.text(bx + bar_width/2, chart_by + b_height + 0.003, f"{val:.1f}" if val < 80 else f"{val:.1f}", 
                    ha='center', va='bottom', fontsize=7.5, fontweight='bold', color=TEXT_MAIN, zorder=4)

        # Group label below
        ax.text(gx + 2 * bar_width + 1.5 * bar_gap, chart_by - 0.015, g_title, 
                ha='center', va='top', fontsize=9, fontweight='bold', color=TEXT_MAIN)

    # -------------------------------------------------------------
    # PANEL 5: KEY OUTCOMES (Far Right)
    # -------------------------------------------------------------
    draw_card(p3_x, bot_y, p3_w, bot_h)
    ax.text(p3_x + 0.018, bot_y + bot_h - 0.020, "KEY OUTCOMES", 
            ha='left', va='center', fontsize=12, fontweight='bold', color=TEXT_MAIN)

    # 4 Cyan Metric Cards (2x2 grid)
    outcomes = [
        ("85.3%", "Who accuracy"),
        ("78.3%", "When accuracy"),
        ("−91.2%", "inference latency"),
        ("100%", "cache hit rate")
    ]
    grid_w = (p3_w - 0.036) / 2
    grid_h = 0.065
    
    for idx, (val_txt, lbl_txt) in enumerate(outcomes):
        r = idx // 2
        c = idx % 2
        ox = p3_x + 0.014 + c * (grid_w + 0.008)
        oy = bot_y + bot_h - 0.055 - (r + 1) * grid_h - r * 0.010
        
        # Cyan outline card
        draw_card(ox, oy, grid_w, grid_h, bg="#F0FDFA", border="#0D9488", lw=1.4, radius=0.005)
        ax.text(ox + grid_w/2, oy + grid_h * 0.65, val_txt, 
                ha='center', va='center', fontsize=16, fontweight='bold', color="#0F766E")
        ax.text(ox + grid_w/2, oy + grid_h * 0.28, lbl_txt, 
                ha='center', va='center', fontsize=8, color=TEXT_MUTED)

    # Bottom Pill: 27/27 automated tests pass
    test_pill_y = bot_y + 0.022
    test_pill_h = 0.032
    test_pill = patches.FancyBboxPatch(
        (p3_x + 0.014, test_pill_y), p3_w - 0.028, test_pill_h,
        boxstyle=patches.BoxStyle("Round", pad=0.004, rounding_size=0.004),
        facecolor="#0F172A", edgecolor='none', zorder=3
    )
    ax.add_patch(test_pill)
    ax.text(p3_x + p3_w/2, test_pill_y + test_pill_h/2, "27 / 27 automated tests pass", 
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF', zorder=4)

    # =============================================================
    # 5. FOOTER TEXT
    # =============================================================
    foot_y = 0.018
    ax.text(left_m, foot_y, 
            "Tech stack: Python · Ollama (Qwen2.5:7b) · NetworkX · SQLite · FastAPI · Streamlit", 
            ha='left', va='center', fontsize=8.5, color=TEXT_MUTED)
    ax.text(right_m, foot_y, 
            "Baseline figures as reported for the Who&When benchmark.", 
            ha='right', va='center', fontsize=8.5, color=TEXT_MUTED)

    # =============================================================
    # 6. Save Files
    # =============================================================
    pdf_out = "media/graphical_abstract/Graphical_Abstract_A2_Reference_Matched.pdf"
    png_out = "media/graphical_abstract/Graphical_Abstract_A2_Reference_Matched.png"
    svg_out = "media/graphical_abstract/Graphical_Abstract_A2_Reference_Matched.svg"

    print(f"Rendering vector PDF to {pdf_out}...")
    plt.savefig(pdf_out, format='pdf', dpi=300, facecolor=BG_CANVAS)
    
    print(f"Rendering vector SVG to {svg_out}...")
    plt.savefig(svg_out, format='svg', facecolor=BG_CANVAS)

    print(f"Rendering high-resolution 300 DPI raster PNG to {png_out}...")
    plt.savefig(png_out, format='png', dpi=300, facecolor=BG_CANVAS)

    plt.close()

    # Generate lightweight web preview
    from PIL import Image
    im = Image.open(png_out)
    im.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
    im.save("media/graphical_abstract/preview_reference_web.png")
    print("Reference web preview saved to media/graphical_abstract/preview_reference_web.png")

    print("Reference-Matched A2 Graphical Abstract successfully generated!")

if __name__ == '__main__':
    generate_reference_matched_a2()
