import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

np.random.seed(42)

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.dirname(os.path.abspath(__file__)))
ledger_path = os.path.abspath(os.path.join(script_dir, "..", "..", "os.environ.get('TRADES_LEDGER', 'annual_2026_nq_all_trades_ledger.csv')"))

df = pd.read_csv(ledger_path)
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

# Setup aggregation
setups = trades.groupby(['Instrument', 'EntryTime', 'Direction']).agg(
    SetupPnL=('PnL', 'sum')
).reset_index()
setups['SetupReturnPct'] = (setups['SetupPnL'] / initial_capital) * 100.0
n_setups = len(setups)

# Daily returns
trades['Date'] = trades['ExitTime'].dt.date
daily_pnl = trades.groupby('Date')['PnL'].sum()
all_b_days = pd.date_range(start=trades['EntryTime'].min().date(), end=trades['ExitTime'].max().date(), freq='B')
daily_series = pd.Series(0.0, index=all_b_days.date)
for d, v in daily_pnl.items():
    if d in daily_series.index:
        daily_series[d] = v
daily_returns_all = daily_series / initial_capital

# Bootstrap
B = 10000
rf_daily = 0.04 / 252.0
T = len(daily_returns_all)

# Moving block bootstrap (block length = 5 days)
block_len = 5
n_blocks = int(np.ceil(T / block_len))
boot_sharpe_block = []
r_vals = daily_returns_all.values

for _ in range(B):
    starts = np.random.randint(0, T - block_len + 1, size=n_blocks)
    blocks = [r_vals[s:s+block_len] for s in starts]
    sample_block = np.concatenate(blocks)[:T]
    m = np.mean(sample_block) - rf_daily
    s = np.std(sample_block, ddof=1)
    if s > 1e-8:
        boot_sharpe_block.append((m / s) * np.sqrt(252))

# Setup return bootstrap
boot_setup_pct = []
for _ in range(B):
    sample = setups.sample(n=n_setups, replace=True)
    boot_setup_pct.append(sample['SetupReturnPct'].mean())

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), dpi=300)

# Panel A: Sharpe ratio
sharpe_ci = np.percentile(boot_sharpe_block, [2.5, 97.5])
ax1.hist(boot_sharpe_block, bins=40, color='#1f77b4', alpha=0.7, edgecolor='white', linewidth=0.8)
ax1.axvline(3.23, color='#d62728', linestyle='-', linewidth=1.5, label='Nominal Estimate (3.23)')
ax1.axvline(sharpe_ci[0], color='#2ca02c', linestyle='--', linewidth=1.2, label=f'95% CI Lower ({sharpe_ci[0]:.2f})')
ax1.axvline(sharpe_ci[1], color='#2ca02c', linestyle='--', linewidth=1.2, label=f'95% CI Upper ({sharpe_ci[1]:.2f})')
ax1.set_title('Block-Bootstrap Annualized Sharpe Distribution (B=10,000)', fontsize=10, fontweight='bold', color='#2c3e50')
ax1.set_xlabel('Annualized Sharpe Ratio (Rf = 4.0%)', fontsize=9, fontweight='bold')
ax1.set_ylabel('Frequency', fontsize=9, fontweight='bold')
ax1.legend(loc='upper right', fontsize=8)
ax1.text(0.04, 0.70, f'T = 219 Days\nBlock Size = 5 Days\nSpread = {sharpe_ci[1]-sharpe_ci[0]:.2f}\nSmall-Sample Dispersion Disclosed',
         transform=ax1.transAxes, fontsize=8, bbox=dict(boxstyle='square,pad=0.3', facecolor='#f9f9f9', edgecolor='#ddd'))

# Panel B: Setup Return Expectancy
setup_ci = np.percentile(boot_setup_pct, [2.5, 97.5])
ax2.hist(boot_setup_pct, bins=40, color='#ff7f0e', alpha=0.7, edgecolor='white', linewidth=0.8)
ax2.axvline(0.522, color='#d62728', linestyle='-', linewidth=1.5, label='Mean Expectancy (+0.522%)')
ax2.axvline(setup_ci[0], color='#2ca02c', linestyle='--', linewidth=1.2, label=f'95% CI Lower (+{setup_ci[0]:.3f}%)')
ax2.axvline(setup_ci[1], color='#2ca02c', linestyle='--', linewidth=1.2, label=f'95% CI Upper (+{setup_ci[1]:.3f}%)')
ax2.set_title('Bootstrap Paired Setup Expected Return Distribution', fontsize=10, fontweight='bold', color='#2c3e50')
ax2.set_xlabel('Setup Expected Return (% of $50,000 Capital)', fontsize=9, fontweight='bold')
ax2.set_ylabel('Frequency', fontsize=9, fontweight='bold')
ax2.xaxis.set_major_formatter(ticker.PercentFormatter(decimals=2))
ax2.legend(loc='upper right', fontsize=8)
ax2.text(0.04, 0.70, f'N = 54 Setups\nMean = +$261.10/setup\nCI: [+{setup_ci[0]:.3f}%, +{setup_ci[1]:.3f}%]\nFinite-Sample Bounds Disclosed',
         transform=ax2.transAxes, fontsize=8, bbox=dict(boxstyle='square,pad=0.3', facecolor='#f9f9f9', edgecolor='#ddd'))

plt.tight_layout()
chart_path = os.path.join(output_dir, 'chart_4_bootstrap_sharpe.png')
plt.savefig(chart_path, dpi=300)
plt.close()
