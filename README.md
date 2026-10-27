# Quantitative Trading & Algorithmic Backtesting Portfolio

**Version / Date:** October 2026  
**Authors:** Yasser REZKI & Ramy Ihab HENNANE (ESE Oran)  
**Academic Target:** MSc in Quantitative Finance / Financial Data Science (2027/2028 Intake)  
**Strategy Focus:** Microstructure Order Flow Imbalances & VWAP Mean Reversion on CME E-mini Nasdaq-100 Futures (`NQ`)  
**Repository URL:** https://github.com/hennaneihab-svg/quant-trading-portfolio (Private Custody)

---

## 1. Executive Summary & Research Scope

This repository contains the empirical backtesting dossier, statistical audit suite, and governance framework for **FlowX Institutional NQ v1**, an algorithmic trading strategy evaluated on CME E-mini Nasdaq-100 index futures (`NQ`) across four quarterly contract cycles (`NQ DEC25`, `NQ MAR26`, `NQ JUN26`, `NQ SEP26`) over 219 business days (48,399 one-minute execution bars within the 09:50–13:30 Eastern Time window).

The strategy exploits order flow absorption signatures—where aggressive market orders fail to generate price continuation beyond statistical intraday volatility envelopes (\(VWAP \pm 2.0\sigma\))—triggering mean-reversion entries filtered by linear regression trend boundaries.

---

## 2. Research Status: Development / In-Sample (NOT VALIDATED)

> **Important Disclosure:**  
> All performance metrics presented in this dossier (+28.20% net return, 3.23 Sharpe ratio, 77.78% paired setup win rate) reflect **development and in-sample incubation data**. The strategy parameters were observed and refined on this calendar horizon.

In accordance with rigorous quantitative research standards (Bailey & López de Prado, 2014; Harvey et al., 2016), the strategy is classified as **NOT EMPIRICALLY VALIDATED** until out-of-sample testing is executed on unexamined historical data under frozen parameters.

Key methodological disclosures:
1. **Multiple Testing Correction:** An exploratory search registry of at least \(N \ge 612\) trials (537 on ES, 74 exploratory on NQ, and 1 pre-registered variant) is disclosed, establishing that the nominal Sharpe ratio is subject to selection bias under the Deflated Sharpe Ratio (DSR) framework.
2. **Trade Classification:** Delta is accumulated via the tick test subset of the Lee & Ready (1991) microstructure framework in the absence of continuous NBBO quotes.
3. **Contamination Documentation:** Prior cross-instrument parameter calibration on S&P 500 futures (`ES`) and intermediate performance inspections are documented in full detail in [`contamination_ledger.md`](contamination_ledger.md).

---

## 3. Repository Structure

```text
.
├── README.md                                    # Research overview, disclosures, and protocol status
├── Quantitative_Trading_Portfolio_Blueprint.md  # Complete research dossier & econometric blueprint
├── Quantitative_Trading_Portfolio_Blueprint.docx# Publication-ready Word document
├── Quantitative_Trading_Portfolio_Blueprint.pdf # Publication-ready PDF document (8 pages)
├── chart_0_pipeline.png                         # Quantitative execution pipeline architecture
├── chart_1_equity_curve.png                     # Cumulative portfolio equity trajectory ($50k base)
├── chart_2_drawdown.png                         # High-water mark underwater drawdown profile (%)
├── chart_3_returns_dist.png                     # Trade PnL distribution & monthly net realizations
├── chart_4_bootstrap_sharpe.png                 # Block-bootstrap Sharpe ratio & expected return distributions
├── trial_registry.md                            # Comprehensive trial registry & DSR parameter accounting
├── contamination_ledger.md                      # Audit of data exposures, fixes, and validity boundaries
└── scripts/
    ├── compute_advanced_stats.py                # VaR/CVaR, block bootstrap, and DSR sensitivity calculations
    ├── generate_chart_0_pipeline.py             # Pipeline architecture vector rendering
    ├── generate_chart_4_bootstrap.py             # Moving block bootstrap (B = 10,000) visualization
    └── generate_portfolio_charts.py             # Portfolio equity curve and risk visualization scripts
```

---

## 4. Frozen Hashes & Out-of-Sample Protocol

To ensure reproducible out-of-sample verification without forward data snooping, the strategy implementation and evaluation scripts were cryptographically locked prior to unexamined data evaluation:

* **Strategy Implementation SHA-256 (`FlowX_Institutional_NQ_v1.cs`):**  
  `9f3664c3651899aad6bba8d565af4a57301b71e279ee2cc280f37deaf6164489`  
  *(Implementation code is maintained in private research custody; available upon formal academic request).*
* **Statistical Evaluation Suite SHA-256 (`eval_combine_50k_suite.py`):**  
  `fa24f532b9dd6a939f3443037e51af6efd5d78599fe0c10be6a30e8c63a865dc`

### Out-of-Sample Verification Gates
Out-of-sample validation requires evaluating pre-2025 CME quarterly contracts (`NQ DEC24`, `NQ MAR25`, `NQ JUN25`, `NQ SEP25`) acquired from an independent institutional data provider against four pre-registered gates:
* **Gate 1 (Account Pass Rate):** Simulated account pass rate \(\ge 50\%\).
* **Gate 2 (Null Permutation Test):** Monte Carlo permutation test with \(p < 0.05\) against null trade distribution.
* **Gate 3 (Friction Stress):** Positive net expectancy under \(1.5\times\) base transaction costs.
* **Gate 4 (Outlier Resilience):** Positive net profit after excluding top 3 winning trade setups.

**Current Out-of-Sample Status:** *Results Pending Data Ingestion.*

---

## 5. Statistical Inference & Empirical Summary

Performance figures reflect the $50,000 initial notional capital over the 219 business days (October 2025 to August 2026), net of $3.80/contract commissions and 1-tick slippage:

* **Cumulative Net Return:** +28.20% (+$14,099.60)
* **Annualized Return (CAGR):** +34.78%
* **Annualized Volatility:** 8.81%
* **Nominal Sharpe Ratio (\(R_f = 4.0\%\)):** 3.23 (95% Moving Block Bootstrap CI: **[0.95, 4.91]**)
* **Calmar Ratio:** 11.52 (CAGR / Peak-Equity Max Drawdown)
* **Maximum Drawdown (Intraday Peak):** -3.02% (-$1,652.80) from running high-water mark
* **Maximum Drawdown (Daily Close):** -2.33% (-$1,432.80) from running high-water mark
* **Paired Setup Win Rate (\(N = 54\)):** 77.78% (95% Bootstrap CI: **[66.67%, 88.89%]**)
* **Profit Factor:** 3.15 ($20,670.80 gross profit / $6,571.20 gross loss)
* **Daily 95% Parametric VaR (Active Days):** -1.18% (-$588.33)
* **Daily 95% Historical CVaR (Active Days):** -1.37% (-$687.00)

---

## 6. Academic Alignment (Curriculum Reference)

* **Econometrics I & II / Practical Time Series Analysis:** Continuous session VWAP formulation, regression slope bounds.
* **Financial Markets & Instruments:** Tick test trade classification (Lee & Ready, 1991), institutional order flow delta.
* **Portfolio Management:** Parametric and historical Value-at-Risk (VaR), Conditional VaR (Expected Shortfall).
* **Statistical Machine Learning / Optimization & Modeling:** Moving block bootstrap resampling (\(B = 10,000\)), Deflated Sharpe Ratio multiple-testing sensitivity grids (Bailey & López de Prado, 2014).

---

## 7. Key References

* Bailey, D. H., & López de Prado, M. (2014). The Deflated Sharpe Ratio: Correcting for selection bias, backtest overfitting, and non-normality. *The Journal of Portfolio Management*, 40(5), 94–107.
* Harvey, C. R., Liu, Y., & Zhu, H. (2016). … and the cross-section of expected returns. *The Review of Financial Studies*, 29(1), 5–68.
* Hasbrouck, J. (2007). *Empirical Market Microstructure: The Institutions, the Economics, and the Econometrics*. Oxford University Press.
* Kyle, A. S. (1985). Continuous auctions and insider trading. *Econometrica*, 53(6), 1315–1335.
* Lee, C. M., & Ready, M. J. (1991). Inferring trade direction from intraday data. *The Journal of Finance*, 46(2), 733–746.
* Lo, A. W. (2002). The statistics of Sharpe ratios. *Financial Analysts Journal*, 58(4), 36–52.
* Mertens, E. (2002). Comments on variance of the IID estimator in Lo (2002). Working paper, University of Basel.
* White, H. (2000). A reality check for data snooping. *Econometrica*, 68(5), 1097–1126.

---

© 2026 Ramy Ihab Hennane & Yasser Rezki. All rights reserved. Provided for academic review.
