import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#ebebeb'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7

output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(output_dir, exist_ok=True)

# Load ledger
df = pd.read_csv(os.environ.get('TRADES_LEDGER', 'annual_2026_nq_all_trades_ledger.csv'))
official_runs = [
    ('2026-10-17 18:39:27', 'NQ DEC25'),
    ('2026-10-17 17:04:25', 'NQ MAR26'),
    ('2026-10-17 17:16:43', 'NQ JUN26'),
    ('2026-10-17 17:35:51', 'NQ SEP26')
]

dfs = [df[(df['RunTimestamp'] == ts) & (df['Instrument'] == inst)].copy() for ts, inst in official_runs]
trades = pd.concat(dfs, ignore_index=True)
trades['EntryTime'] = pd.to_datetime(trades['EntryTime'])
trades['ExitTime'] = pd.to_datetime(trades['ExitTime'])
trades = trades.sort_values('EntryTime').reset_index(drop=True)

initial_capital = 50000.0
trades['CumPnL'] = trades['PnL'].cumsum()
trades['Equity'] = initial_capital + trades['CumPnL']
trades['Peak'] = trades['Equity'].cummax()
trades['Drawdown'] = trades['Equity'] - trades['Peak']
trades['DrawdownPct'] = trades['Drawdown'] / trades['Peak'] * 100.0

# -------------------------------------------------------------
# CHART 1: Cumulative Equity Curve (Out-of-Sample / Dev Incubation)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

# Plot initial baseline
t_dates = [trades['EntryTime'].iloc[0]] + list(trades['ExitTime'])
equity_curve = [initial_capital] + list(trades['Equity'])

ax.plot(t_dates, equity_curve, color='#0f4c81', linewidth=2.2, label='FlowX Institutional NQ v1 (Net of Comm. & Slippage)')
ax.fill_between(t_dates, initial_capital, equity_curve, color='#0f4c81', alpha=0.08)
ax.axhline(initial_capital, color='#7f8c8d', linestyle=':', linewidth=1.2, label='Initial Capital ($50,000 Base)')

# Shading quarterly contract regimes
contract_spans = [
    ('NQ DEC25', trades[trades['Instrument'] == 'NQ DEC25']['EntryTime'].min(), trades[trades['Instrument'] == 'NQ DEC25']['ExitTime'].max(), '#f8f9fa'),
    ('NQ MAR26', trades[trades['Instrument'] == 'NQ MAR26']['EntryTime'].min(), trades[trades['Instrument'] == 'NQ MAR26']['ExitTime'].max(), '#ffffff'),
    ('NQ JUN26', trades[trades['Instrument'] == 'NQ JUN26']['EntryTime'].min(), trades[trades['Instrument'] == 'NQ JUN26']['ExitTime'].max(), '#f8f9fa'),
    ('NQ SEP26', trades[trades['Instrument'] == 'NQ SEP26']['EntryTime'].min(), trades[trades['Instrument'] == 'NQ SEP26']['ExitTime'].max(), '#ffffff')
]

for label, start, end, color in contract_spans:
    ax.axvspan(start, end, color=color, alpha=0.6, zorder=0)

# Annotations for key milestones
final_equity = trades['Equity'].iloc[-1]
net_profit = trades['CumPnL'].iloc[-1]
ax.scatter([trades['ExitTime'].iloc[-1]], [final_equity], color='#1b7837', s=50, zorder=5)
# Methodological watermark / label (top-left)
ax.text(0.03, 0.94, 'STATUS: Development / In-Sample (N \u2265 612 trials, lower bound)\nBenchmark: Buy-and-Hold N/A',
        transform=ax.transAxes, fontsize=8.5, verticalalignment='top', horizontalalignment='left',
        bbox=dict(boxstyle='square,pad=0.4', facecolor='#fffde7', edgecolor='#ffe082', alpha=0.95),
        color='#795548', fontweight='bold')

# Legend below status box on upper-left
ax.legend(loc='upper left', bbox_to_anchor=(0.03, 0.81), frameon=True, facecolor='white', framealpha=0.9, fontsize=8.5)

# Annotations for key milestones (green box in lower-right empty zone)
ax.annotate(f'Final Equity: ${final_equity:,.2f}\nNet Profit: +${net_profit:,.2f} (+28.20%)\nProfit Factor: 3.15 (108 Trades)',
            xy=(trades['ExitTime'].iloc[-1], final_equity),
            xytext=(0.97, 0.18), textcoords='axes fraction',
            ha='right', va='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#e8f5e9', edgecolor='#81c784', alpha=0.95),
            fontsize=9, fontweight='bold', color='#1b5e20',
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=-0.15', color='#2e7d32', lw=1.2))

ax.set_title('FlowX Institutional NQ v1 — Cumulative Equity Growth ($50,000 Base)', fontsize=12, fontweight='bold', pad=12, color='#2c3e50')
ax.set_xlabel('Date', fontsize=10, fontweight='bold', color='#333333')
ax.set_ylabel('Portfolio Equity (USD)', fontsize=10, fontweight='bold', color='#333333')
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.set_ylim(48500, 66000)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'chart_1_equity_curve.png'), dpi=300)
plt.close()
print("Saved chart_1_equity_curve.png")

# -------------------------------------------------------------
# CHART 2: Underwater Drawdown Plot (%)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)

dd_pct = [0.0] + list(trades['DrawdownPct'])
ax.fill_between(t_dates, dd_pct, 0, color='#d9534f', alpha=0.35, label='Underwater Drawdown (%)')
ax.plot(t_dates, dd_pct, color='#c9302c', linewidth=1.5)
ax.axhline(0, color='#333333', linestyle='-', linewidth=0.8)

# Highlight max drawdown
min_dd_idx = trades['DrawdownPct'].idxmin()
min_dd_date = trades['ExitTime'].iloc[min_dd_idx]
min_dd_val = trades['DrawdownPct'].iloc[min_dd_idx]
min_dd_dol = trades['Drawdown'].iloc[min_dd_idx]

ax.scatter([min_dd_date], [min_dd_val], color='#900', s=45, zorder=5)
ax.annotate(f'Intraday Max Drawdown: {min_dd_val:.2f}% (-${abs(min_dd_dol):,.2f})\nDaily Close Max DD: -2.33% (-$1,432.80)\nMax Duration: 36 Business Days',
            xy=(min_dd_date, min_dd_val),
            xytext=(40, -25), textcoords='offset points',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#fbe9e7', edgecolor='#ffab91', alpha=0.9),
            fontsize=8.5, fontweight='bold', color='#bf360c',
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='#d84315'))

ax.set_title('FlowX Institutional NQ v1 — Underwater Portfolio Drawdown Profile (%)', fontsize=12, fontweight='bold', pad=12, color='#2c3e50')
ax.set_xlabel('Date', fontsize=10, fontweight='bold', color='#333333')
ax.set_ylabel('Drawdown from High-Water Mark (%)', fontsize=10, fontweight='bold', color='#333333')
ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.set_ylim(-4.5, 0.5)
ax.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9, fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'chart_2_drawdown.png'), dpi=300)
plt.close()
print("Saved chart_2_drawdown.png")

# -------------------------------------------------------------
# CHART 3: Returns Distribution & Monthly Breakdown
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=300)

# Subplot A: Trade PnL Histogram showing tail distribution
pnl_wins = trades[trades['PnL'] > 0]['PnL']
pnl_losses = trades[trades['PnL'] < 0]['PnL']

bins = np.linspace(-400, 600, 25)
ax1.hist([pnl_losses, pnl_wins], bins=bins, stacked=True, color=['#e57373', '#81c784'],
         edgecolor='white', linewidth=1.0, label=['Losses (22.2%)', 'Wins (77.8%)'])
ax1.axvline(0, color='#333333', linestyle='--', linewidth=1.0)
ax1.axvline(-320, color='#d32f2f', linestyle=':', linewidth=1.2, label='Fixed Stop-Loss (-$320.00)')
ax1.axvline(200, color='#388e3c', linestyle=':', linewidth=1.2, label='Limit Target 1 (+$200.00)')

ax1.set_title('Trade PnL Distribution (Skewness & Asymmetry)', fontsize=10.5, fontweight='bold', color='#2c3e50')
ax1.set_xlabel('Trade Net PnL (USD)', fontsize=9, fontweight='bold')
ax1.set_ylabel('Frequency (Trade Count)', fontsize=9, fontweight='bold')
def format_trade_pnl(x, pos):
    if x < 0:
        return f'-${abs(x):,.0f}'
    return f'${x:,.0f}'
ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_trade_pnl))
ax1.legend(loc='upper right', fontsize=8, framealpha=0.9)
ax1.text(0.04, 0.70, f'N = 108 Trades\nWin Rate = 77.78%\nProfit Factor = 3.15\nMean Trade = +$130.55\nTrade 95% CVaR = -$328.80',
         transform=ax1.transAxes, fontsize=8, bbox=dict(boxstyle='square,pad=0.3', facecolor='#f5f5f5', edgecolor='#ddd'))

# Subplot B: Monthly Net PnL Breakdown
trades['YearMonth'] = trades['ExitTime'].dt.to_period('M')
monthly_pnl = trades.groupby('YearMonth')['PnL'].sum()
month_labels = [str(m) for m in monthly_pnl.index]
bar_colors = ['#2e7d32' if v > 0 else '#c62828' for v in monthly_pnl.values]

bars = ax2.bar(month_labels, monthly_pnl.values, color=bar_colors, width=0.6, edgecolor='#333333', linewidth=0.5)
ax2.axhline(0, color='#333333', linestyle='-', linewidth=0.8)
ax2.set_title('Monthly Net PnL Realization (USD)', fontsize=10.5, fontweight='bold', color='#2c3e50')
ax2.set_xlabel('Month', fontsize=9, fontweight='bold')
ax2.set_ylabel('Realized Net PnL (USD)', fontsize=9, fontweight='bold')
ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=40, ha='right', fontsize=8)

for bar in bars:
    yval = bar.get_height()
    va = 'bottom' if yval >= 0 else 'top'
    val_str = f"-${abs(yval):,.0f}" if yval < 0 else f"${yval:,.0f}"
    ax2.text(bar.get_x() + bar.get_width() / 2.0, yval + (50 if yval >= 0 else -100),
             val_str, ha='center', va=va, fontsize=7.5, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'chart_3_returns_dist.png'), dpi=300)
plt.close()
print("Saved chart_3_returns_dist.png")
