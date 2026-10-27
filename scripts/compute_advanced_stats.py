import pandas as pd
import numpy as np
import math
import os

# Set seed for reproducibility
np.random.seed(42)

output_dir = os.path.dirname(os.path.abspath(__file__))
ledger_path = os.environ.get("TRADES_LEDGER", os.path.join(output_dir, "..", "annual_2026_nq_all_trades_ledger.csv"))

# 1. Load official runs
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

# 2. Setup level aggregation (54 setups)
setups = trades.groupby(['Instrument', 'EntryTime', 'Direction']).agg(
    ExitTime=('ExitTime', 'max'),
    SetupPnL=('PnL', 'sum'),
    LegCount=('TradeIndex', 'count'),
    Leg1PnL=('PnL', 'first'),
    Leg2PnL=('PnL', 'last')
).reset_index()

setups['SetupReturnPct'] = (setups['SetupPnL'] / initial_capital) * 100.0
setups['IsWin'] = setups['SetupPnL'] > 0
setups['IsLoss'] = setups['SetupPnL'] < 0

n_setups = len(setups)
setup_wins = setups['IsWin'].sum()
setup_losses = setups['IsLoss'].sum()
setup_win_rate = setup_wins / n_setups * 100.0
setup_mean_pnl = setups['SetupPnL'].mean()
setup_std_pnl = setups['SetupPnL'].std()
setup_mean_ret = setups['SetupReturnPct'].mean()

# 3. Daily returns series
trades['Date'] = trades['ExitTime'].dt.date
daily_pnl = trades.groupby('Date')['PnL'].sum()

# Construct continuous business day series
all_b_days = pd.date_range(start=trades['EntryTime'].min().date(), end=trades['ExitTime'].max().date(), freq='B')
daily_series = pd.Series(0.0, index=all_b_days.date)
for d, v in daily_pnl.items():
    if d in daily_series.index:
        daily_series[d] = v

daily_returns_all = daily_series / initial_capital
daily_returns_active = daily_pnl / initial_capital

def calc_skew(x):
    m = np.mean(x)
    s = np.std(x, ddof=0)
    return np.mean(((x - m) / s)**3) if s > 0 else 0.0

def calc_kurt(x):
    m = np.mean(x)
    s = np.std(x, ddof=0)
    return np.mean(((x - m) / s)**4) if s > 0 else 3.0

mean_daily_all = daily_returns_all.mean()
std_daily_all = daily_returns_all.std()
skew_daily_all = calc_skew(daily_returns_all.values)
kurt_daily_all = calc_kurt(daily_returns_all.values)

mean_daily_act = daily_returns_active.mean()
std_daily_act = daily_returns_active.std()
skew_daily_act = calc_skew(daily_returns_active.values)
kurt_daily_act = calc_kurt(daily_returns_active.values)

# 4. VaR and CVaR calculations
var_hist_95_all = np.percentile(daily_returns_all, 5) * 100.0
cvar_hist_95_all = daily_returns_all[daily_returns_all <= np.percentile(daily_returns_all, 5)].mean() * 100.0
param_var_95_all = (mean_daily_all - 1.644853 * std_daily_all) * 100.0

var_hist_95_act = np.percentile(daily_returns_active, 5) * 100.0
cvar_hist_95_act = daily_returns_active[daily_returns_active <= np.percentile(daily_returns_active, 5)].mean() * 100.0
param_var_95_act = (mean_daily_act - 1.644853 * std_daily_act) * 100.0

# 5. Bootstrap Confidence Intervals (10,000 iterations, unified seed 42)
B = 10000
rf_annual = 0.04
rf_daily = rf_annual / 252.0
T = len(daily_returns_all)

# A. Moving Block Bootstrap for Sharpe Ratio (first, exactly matching chart 4)
np.random.seed(42)
block_len = 5
n_blocks = int(np.ceil(T / block_len))
boot_sharpe_block = []
r_vals = daily_returns_all.values

for _ in range(B):
    starts = np.random.randint(0, T - block_len + 1, size=n_blocks)
    blocks = [r_vals[s:s+block_len] for s in starts]
    sample_block = np.concatenate(blocks)[:T]
    mean_r = np.mean(sample_block) - rf_daily
    std_r = np.std(sample_block, ddof=1)
    if std_r > 1e-8:
        boot_sharpe_block.append((mean_r / std_r) * np.sqrt(252))
sharpe_block_ci = np.percentile(boot_sharpe_block, [2.5, 97.5])

# B. Setup Level Resampling (second, exactly matching chart 4)
boot_setup_wr = []
boot_setup_mean_dol = []
boot_setup_mean_pct = []

for _ in range(B):
    sample = setups.sample(n=n_setups, replace=True)
    boot_setup_wr.append((sample['SetupPnL'] > 0).mean() * 100.0)
    boot_setup_mean_dol.append(sample['SetupPnL'].mean())
    boot_setup_mean_pct.append(sample['SetupReturnPct'].mean())

setup_wr_ci = np.percentile(boot_setup_wr, [2.5, 97.5])
setup_mean_dol_ci = np.percentile(boot_setup_mean_dol, [2.5, 97.5])
setup_mean_pct_ci = np.percentile(boot_setup_mean_pct, [2.5, 97.5])

# C. Trade Level Resampling
boot_trade_wr = []
n_trades = len(trades)
for _ in range(B):
    sample_t = trades.sample(n=n_trades, replace=True)
    boot_trade_wr.append((sample_t['PnL'] > 0).mean() * 100.0)
trade_wr_ci = np.percentile(boot_trade_wr, [2.5, 97.5])

# D. IID Sharpe Bootstrap
boot_sharpe_iid = []
for _ in range(B):
    sample_r = np.random.choice(daily_returns_all.values, size=T, replace=True)
    mean_r = np.mean(sample_r) - rf_daily
    std_r = np.std(sample_r, ddof=1)
    if std_r > 1e-8:
        boot_sharpe_iid.append((mean_r / std_r) * np.sqrt(252))
sharpe_iid_ci = np.percentile(boot_sharpe_iid, [2.5, 97.5])

# 6. Deflated Sharpe Ratio (Bailey & Lopez de Prado, 2014)
euler_gamma = 0.57721566490153286060651209

def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def norm_ppf(p):
    if p <= 0.0:
        return -999.0
    if p >= 1.0:
        return 999.0
    a = [-39.69683028665376, 220.9460984245205, -275.9285104469687, 138.3577518672690, -30.66479806614716, 2.506628277459239]
    b = [-54.47609879822406, 161.5858368580409, -155.6989798598866, 66.80131188771972, -13.28068155288572]
    c = [-0.007784894002430293, -0.3223964580411365, -2.400758277161838, -2.549732539343734, 4.374664141464968, 2.938163982698783]
    d = [0.007784695709041462, 0.3224671290700398, 2.445134137142996, 3.754408661907416]
    plow = 0.02425
    phigh = 1.0 - plow
    if p < plow:
        q = math.sqrt(-2.0 * math.log(p))
        return (((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1.0)
    elif p > phigh:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        return -(((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1.0)
    else:
        q = p - 0.5
        r = q * q
        return (((((a[0]*r + a[1])*r + a[2])*r + a[3])*r + a[4])*r + a[5])*q / (((((b[0]*r + b[1])*r + b[2])*r + b[3])*r + b[4])*r + 1.0)

sr_ann_hat = (mean_daily_all - rf_daily) / std_daily_all * np.sqrt(252)

def compute_dsr(N, sigma_sr_ann, sr_ann, gamma3, gamma4, T_obs):
    if N <= 1:
        sr_star_ann = 0.0
    else:
        term1 = (1.0 - euler_gamma) * norm_ppf(1.0 - 1.0 / N)
        term2 = euler_gamma * norm_ppf(1.0 - 1.0 / (N * math.e))
        sr_star_ann = sigma_sr_ann * (term1 + term2)
    
    sr_star_daily = sr_star_ann / math.sqrt(252)
    sr_daily = sr_ann / math.sqrt(252)
    
    denom = math.sqrt((1.0 - gamma3 * sr_daily + (gamma4 - 1.0) / 4.0 * (sr_daily**2)) / (T_obs - 1.0))
    z = (sr_daily - sr_star_daily) / denom
    dsr_pvalue = norm_cdf(z)
    return sr_star_ann, z, dsr_pvalue

# Sensitivity grid
N_trials_list = [74, 300, 612]
sigma_sr_list = [0.50, 1.00, 1.50, 2.00]

dsr_results = []
for n_t in N_trials_list:
    for s_sr in sigma_sr_list:
        sr_star, z_score, dsr_val = compute_dsr(n_t, s_sr, sr_ann_hat, skew_daily_all, kurt_daily_all, T)
        dsr_results.append({
            'N_Trials': n_t,
            'Sigma_SR': s_sr,
            'SR_Hurdle_Ann': round(sr_star, 2),
            'Z_Score': round(z_score, 2),
            'DSR': round(dsr_val, 4)
        })
dsr_df = pd.DataFrame(dsr_results)

# 7. Write comprehensive report
report_path = os.path.join(output_dir, "statistical_inference_report.txt")
with open(report_path, "w", encoding="utf-8") as f:
    f.write("========================================================================================\n")
    f.write("STATISTICAL INFERENCE & TAIL-RISK AUDIT REPORT\n")
    f.write("Strategy: FlowX Institutional NQ v1 | Evaluation Sample: 2025-10-28 to 2026-08-28\n")
    f.write("========================================================================================\n\n")
    
    f.write("1. SAMPLE STRUCTURE & SIZING:\n")
    f.write(f"- Total Calendar Days: 304 | Business Days (Observations T): {T}\n")
    f.write(f"- Active Trading Days with Executions: {len(daily_pnl)} ({len(daily_pnl)/T*100:.1f}%)\n")
    f.write(f"- Inactive Days (Zero Return): {T - len(daily_pnl)} ({(T - len(daily_pnl))/T*100:.1f}%)\n")
    f.write(f"- Total Executed Trades: {n_trades} legs\n")
    f.write(f"- Total Paired Trading Setups: {n_setups} setups\n\n")

    f.write("2. VALUE-AT-RISK (VaR 95%) & CONDITIONAL VaR (CVaR 95%):\n")
    f.write("A. All 219 Business Days (Unconditional Portfolio Series):\n")
    f.write(f"   - Mean Daily Return: {mean_daily_all*100:.4f}% (${mean_daily_all*initial_capital:.2f})\n")
    f.write(f"   - Daily Std Dev:     {std_daily_all*100:.4f}% (${std_daily_all*initial_capital:.2f})\n")
    f.write(f"   - Skewness:          {skew_daily_all:.4f}\n")
    f.write(f"   - Pearson Kurtosis:  {kurt_daily_all:.4f}\n")
    f.write(f"   - Historical VaR (95%):  {var_hist_95_all:.2f}% (${var_hist_95_all*initial_capital/100:.2f})\n")
    f.write(f"   - Historical CVaR (95%): {cvar_hist_95_all:.2f}% (${cvar_hist_95_all*initial_capital/100:.2f})\n")
    f.write(f"   - Parametric VaR (95%):  {param_var_95_all:.2f}% (${param_var_95_all*initial_capital/100:.2f})\n")
    f.write("   * NOTE: The historical VaR 95% on all days (-0.03% / -$12.76) is an artifact\n")
    f.write("     caused by 178 inactive days (81.3% zero-return days). The 5th percentile falls\n")
    f.write("     at the boundary of inactive days, suppressing the empirical loss threshold.\n\n")

    f.write("B. Active Trading Days Only (N = 41 Active Sessions):\n")
    f.write(f"   - Mean Daily Return: {mean_daily_act*100:.4f}% (${mean_daily_act*initial_capital:.2f})\n")
    f.write(f"   - Daily Std Dev:     {std_daily_act*100:.4f}% (${std_daily_act*initial_capital:.2f})\n")
    f.write(f"   - Skewness:          {skew_daily_act:.4f}\n")
    f.write(f"   - Pearson Kurtosis:  {kurt_daily_act:.4f}\n")
    f.write(f"   - Historical VaR (95%):  {var_hist_95_act:.2f}% (${var_hist_95_act*initial_capital/100:.2f})\n")
    f.write(f"   - Historical CVaR (95%): {cvar_hist_95_act:.2f}% (${cvar_hist_95_act*initial_capital/100:.2f})\n")
    f.write(f"   - Parametric VaR (95%):  {param_var_95_act:.2f}% (${param_var_95_act*initial_capital/100:.2f})\n\n")

    f.write("3. STATISTICAL INFERENCE & BOOTSTRAP CONFIDENCE INTERVALS (B = 10,000):\n")
    f.write(f"- Paired Setup Win Rate (N = 54): {setup_win_rate:.2f}%\n")
    f.write(f"  * 95% Bootstrap CI: [{setup_wr_ci[0]:.2f}%, {setup_wr_ci[1]:.2f}%]\n")
    f.write(f"- Paired Setup Expected PnL (USD): ${setup_mean_pnl:.2f}\n")
    f.write(f"  * 95% Bootstrap CI: [${setup_mean_dol_ci[0]:.2f}, ${setup_mean_dol_ci[1]:.2f}]\n")
    f.write(f"- Paired Setup Expected Return (% of Capital): {setup_mean_ret:.3f}%\n")
    f.write(f"  * 95% Bootstrap CI: [{setup_mean_pct_ci[0]:.3f}%, {setup_mean_pct_ci[1]:.3f}%]\n")
    f.write(f"- Trade Leg Win Rate (N = 108): {trades['PnL'].gt(0).mean()*100:.2f}%\n")
    f.write(f"  * 95% Bootstrap CI: [{trade_wr_ci[0]:.2f}%, {trade_wr_ci[1]:.2f}%]\n")
    f.write(f"- Annualized Sharpe Ratio (Rf = 4.0%): {sr_ann_hat:.2f}\n")
    f.write(f"  * 95% IID Bootstrap CI:   [{sharpe_iid_ci[0]:.2f}, {sharpe_iid_ci[1]:.2f}]\n")
    f.write(f"  * 95% Block Bootstrap CI (Block=5d): [{sharpe_block_ci[0]:.2f}, {sharpe_block_ci[1]:.2f}]\n\n")

    f.write("4. DEFLATED SHARPE RATIO (DSR) SENSITIVITY GRID:\n")
    f.write("Methodology: Bailey & Lopez de Prado (2014, Journal of Portfolio Management)\n")
    f.write(f"Baseline: Nominal Annualized Sharpe = {sr_ann_hat:.2f} | T = {T} days | Daily Skew = {skew_daily_all:.3f} | Daily Kurt = {kurt_daily_all:.3f}\n\n")
    f.write(dsr_df.to_string(index=False))
    f.write("\n\n")
    f.write("SENSITIVITY ANALYSIS:\n")
    f.write("The cross-trial dispersion parameter sigma_SR is not directly observable; the values evaluated represent sensitivity hypotheses.\n")
    f.write("For N = 612 trials:\n")
    for _, row in dsr_df[dsr_df['N_Trials'] == 612].iterrows():
        f.write(f"- sigma_SR = {row['Sigma_SR']:.2f}: SR* = {row['SR_Hurdle_Ann']:.2f}, Z = {row['Z_Score']:.2f}, DSR = {row['DSR']:.4f}\n")
    f.write("When trial dispersion increases from 0.50 to 1.50 or higher, the DSR drops from 0.9607 to 0.0649 or lower.\n")
    f.write("This sensitivity indicates that statistical confidence depends on the unobserved variance across the historical trial space.\n")

# Save CSV of DSR grid
dsr_df.to_csv(os.path.join(output_dir, "dsr_sensitivity_grid.csv"), index=False)
