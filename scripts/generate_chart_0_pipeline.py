import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

fig, ax = plt.subplots(figsize=(13.5, 3.8), dpi=300)
ax.set_xlim(0, 135)
ax.set_ylim(0, 42)
ax.axis('off')

# Background
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#ffffff')

# Colors
c_feed_bg = '#f0f4f8'
c_feed_border = '#3b82f6'
c_eng_bg = '#f8fafc'
c_eng_border = '#0f4c81'
c_logic_bg = '#eff6ff'
c_logic_border = '#1d4ed8'
c_dec_bg = '#fef3c7'
c_dec_border = '#d97706'
c_exec_bg = '#ecfdf5'
c_exec_border = '#059669'
c_rej_bg = '#fef2f2'
c_rej_border = '#dc2626'
c_risk_bg = '#f5f3ff'
c_risk_border = '#7c3aed'
c_audit_bg = '#f0fdf4'
c_audit_border = '#16a34a'

# Box 1: Tick Data Feed
box1 = patches.FancyBboxPatch((2, 14), 16, 16, boxstyle="round,pad=0.8,rounding_size=1.5",
                              facecolor=c_feed_bg, edgecolor=c_feed_border, linewidth=1.5)
ax.add_patch(box1)
ax.text(10, 24, "CME Tick Feed", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1e3a8a')
ax.text(10, 19, "NinjaTrader 8\nLocal tick database", ha='center', va='center', fontsize=7.5, color='#475569')

# Arrow 1 -> 2
ax.annotate('', xy=(22, 22), xytext=(18.8, 22),
            arrowprops=dict(arrowstyle="-|>", color='#64748b', lw=1.5, mutation_scale=12))

# Box 2: Tick Ingestion Engine
box2 = patches.FancyBboxPatch((23, 14), 16, 16, boxstyle="round,pad=0.8,rounding_size=1.5",
                              facecolor=c_eng_bg, edgecolor=c_eng_border, linewidth=1.5)
ax.add_patch(box2)
ax.text(31, 24, "Tick Ingestion", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0f4c81')
ax.text(31, 19, "NinjaScript (C#)\nOnBarUpdate() event", ha='center', va='center', fontsize=7.5, color='#475569')

# Arrow 2 -> 3
ax.annotate('', xy=(43, 22), xytext=(39.8, 22),
            arrowprops=dict(arrowstyle="-|>", color='#64748b', lw=1.5, mutation_scale=12))

# Box 3: Microstructure & Order Flow Logic
box3 = patches.FancyBboxPatch((44, 14), 18, 16, boxstyle="round,pad=0.8,rounding_size=1.5",
                              facecolor=c_logic_bg, edgecolor=c_logic_border, linewidth=1.5)
ax.add_patch(box3)
ax.text(53, 24, "Microstructure Logic", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1d4ed8')
ax.text(53, 19, "VWAP ± 2.0σ Bands\nTick CVD + Sweeps", ha='center', va='center', fontsize=7.5, color='#475569')

# Arrow 3 -> 4
ax.annotate('', xy=(66, 22), xytext=(62.8, 22),
            arrowprops=dict(arrowstyle="-|>", color='#64748b', lw=1.5, mutation_scale=12))

# Box 4: Decision diamond / gate
diamond = patches.Polygon([[74, 32], [82, 22], [74, 12], [66, 22]],
                          closed=True, facecolor=c_dec_bg, edgecolor=c_dec_border, linewidth=1.5)
ax.add_patch(diamond)
ax.text(74, 23.5, "Kill Zone &\nSlope Gate", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#92400e')
ax.text(74, 17.5, "09:50-13:30 ET", ha='center', va='center', fontsize=7.0, color='#78350f')

# Decision Paths
# Valid Setup -> Execution (Right)
ax.annotate('', xy=(88, 22), xytext=(82.5, 22),
            arrowprops=dict(arrowstyle="-|>", color='#059669', lw=1.8, mutation_scale=12))
ax.text(85, 24.5, "Valid", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#059669')

# Filter Reject -> Bottom cooldown
ax.annotate('', xy=(74, 4), xytext=(74, 11.5),
            arrowprops=dict(arrowstyle="-|>", color='#dc2626', lw=1.5, mutation_scale=12))
ax.text(76, 7.5, "Reject", ha='left', va='center', fontsize=7.5, fontweight='bold', color='#dc2626')

box_rej = patches.FancyBboxPatch((66, 0.5), 16, 4.5, boxstyle="round,pad=0.5,rounding_size=1.0",
                                 facecolor=c_rej_bg, edgecolor=c_rej_border, linewidth=1.2)
ax.add_patch(box_rej)
ax.text(74, 2.7, "No Action / Cooldown", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#991b1b')

# Box 5: Dual-Leg Execution
box5 = patches.FancyBboxPatch((89, 14), 18, 16, boxstyle="round,pad=0.8,rounding_size=1.5",
                              facecolor=c_exec_bg, edgecolor=c_exec_border, linewidth=1.5)
ax.add_patch(box5)
ax.text(98, 24, "Dual-Leg Execution", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#047857')
ax.text(98, 19, "Leg 1: Limit TP1 (+10 pts)\nLeg 2: Runner (+25 pts)", ha='center', va='center', fontsize=7.5, color='#475569')

# Arrow 5 -> 6
ax.annotate('', xy=(111, 22), xytext=(107.8, 22),
            arrowprops=dict(arrowstyle="-|>", color='#64748b', lw=1.5, mutation_scale=12))

# Box 6: Intraday Risk Governance
box6 = patches.FancyBboxPatch((112, 14), 21, 16, boxstyle="round,pad=0.8,rounding_size=1.5",
                              facecolor=c_risk_bg, edgecolor=c_risk_border, linewidth=1.5)
ax.add_patch(box6)
ax.text(122.5, 24, "Risk Governance", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#6d28d9')
ax.text(122.5, 19, "Daily Loss Cap ($700)\nDaily Profit Cap ($750)\n1 Loss / Day Cutoff", ha='center', va='center', fontsize=7.5, color='#475569')

# Bottom Banner: Statistical Inference Pipeline
box_inf = patches.FancyBboxPatch((2, 35.5), 131, 5.5, boxstyle="round,pad=0.5,rounding_size=1.2",
                                 facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=1.0)
ax.add_patch(box_inf)
ax.text(67.5, 38.2, "External Statistical Inference Pipeline (Python 3): 10,000 Block Bootstrap | DSR Multiple-Testing Audit | Historical & Parametric VaR / CVaR",
        ha='center', va='center', fontsize=8.2, fontweight='semibold', color='#334155')

plt.tight_layout()
out_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "chart_0_pipeline.png")
plt.savefig(out_file, dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.close()
print("Saved chart_0_pipeline.png successfully.")
