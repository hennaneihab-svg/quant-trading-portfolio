# Quantitative Research Trial Registry

*Registry Initialization: October 17, 2026*  
*Scope: Cross-instrument exploratory optimization runs and strategy trial accounting.*

---

## 1. Exploratory Trial Accounting (Strict Lower Bound)

To correct for multiple testing bias and data snooping under the Deflated Sharpe Ratio (DSR; Bailey & López de Prado, 2014) framework, all exploratory backtest iterations and parameter evaluations conducted prior to protocol freeze are systematically recorded:

* **S&P 500 Futures (`ES`):**
  * `optimization_log_es.csv`: 211 distinct parameter and rule combinations (291 evaluated runs).
  * `optimization_runs_summary.csv`: 326 distinct parameter combinations (352 evaluated runs).
  * Informal exploratory iterations and prior stop-loss sensitivity tests: multiple unlogged iterations.
  * **ES Subtotal:** ≈ 537 distinct evaluated parameter combinations.

* **Nasdaq-100 Futures (`NQ`):**
  * `optimization_log.csv` (Historical NQ parameter grid): 72 distinct parameter combinations (73 runs).
  * `optimization_runs_nq_summary.csv`: 2 distinct combinations (3 runs).
  * **NQ Exploratory Subtotal:** 74 distinct parameter combinations.

* **Pre-Registered NQ Strategy Variant (`NQ-v1`):**
  * 1 frozen pre-registered strategy specification (`prereg_NQ_v1.md`).

### Registry Summary
* **Total Evaluated Trials Retained for DSR Benchmark:** At least \(N \ge 612\) trials (537 ES + 74 exploratory NQ + 1 pre-registered NQ-v1).
* **Methodological Implication:** The nominal annualized Sharpe ratio of 3.23 must be evaluated against this multi-trial search space. Unobserved informal exploratory trials imply that 612 represents a strict lower bound.

---

## 2. Technical Validation Runs & Incubation Status (October 17, 2026)

### Technical Integration Run (December 19, 2025 to March 18, 2026) — Plumbing Verification (Non-Judged)
* **Objective:** Verification of tick data ingestion, 24-hour electronic trading hours continuity (~1,380 one-minute bars/session), and execution friction accounting ($3.80 round-trip commission and 1-tick slippage).
* **Status:** Integration verified; performance metrics non-judged and excluded from official evaluation.
* **Frozen Code Hash (SHA-256) (`FlowX_Institutional_NQ_v1.cs`):**  
  `9f3664c3651899aad6bba8d565af4a57301b71e279ee2cc280f37deaf6164489`  
  *(Prior maintenance hashes: post-F8 `7cd50df15ee1489573cc106606d5cc001762460bd151a1476cac936768e4ca9a`, post-F7 `f70d9b7358619bf8e5a211790edeb83921c2086e9fad7e26638c25d73ffbb0ed`)*
* **Run Execution Hash (SHA-256):**  
  `165cae9caecf9151054d22ceffdfc889a18aa4d2b477d2e6081501fb4baccc98`
* **Diagnostic Funnel Hash (SHA-256):**  
  `a4473999dbfbf47d3deb34c15dd327ff7f5f6fe9583d8e80e5353331aa1216d9`

---

## 3. Pre-Registered Evaluation Infrastructure (Frozen Prior to Testing)

* **Statistical Evaluation Suite (`validation/eval_combine_50k_suite.py`):**  
  SHA-256: `fa24f532b9dd6a939f3443037e51af6efd5d78599fe0c10be6a30e8c63a865dc`
* **Tick Data Completeness Verification Script (`validation/verify_data_completeness_r7.py`):**  
  SHA-256: `4f89b11e3c8bb05f4cf7083aa5cdb60edd3b951f4b32a52dd5847cc08c35255e`
* **Verification Protocol:** Scripts were tested and validated exclusively on synthetic trade series (`--test-synthetic`), preventing test data contamination.

---

## 4. Formal Protocol Evaluation Aggregate

### Non-Overlapping Horizon (April 01, 2026 to October 16, 2026)
* **Raw Execution Record SHA-256:**  
  `e6e9b466186b72d2be4aa7cebfeb13e018698bf4caea386242c1beff3d937a09`
* **Evaluation Suite Hash SHA-256:**  
  `fa24f532b9dd6a939f3443037e51af6efd5d78599fe0c10be6a30e8c63a865dc`
* **Gate Results:**
  * **Gate 1 (Account Pass Rate \(\ge 50\%\)):** **53.8%** (14/26 setups) -> **PASSED**
  * **Gate 2 (Null Model Permutation Test, \(p < 0.05\) & Real > 95th Percentile):** Real PnL $5,982.40 vs 95th percentile $3,812.40, \(p = 0.0050\) (99.5th percentile) -> **PASSED**
  * **Gate 3 (Expectancy Under Stress at \(1.5\times\) Friction):** **+$226.29 / setup** (+$108.15 / execution leg) -> **PASSED**
  * **Gate 4 (Outlier Resilience; Profit Excluding Top 3 Setups):** **+$3,900.20** net profit -> **PASSED**
* **Methodological Conclusion:**  
  **4/4 Gates Passed -> PROVISIONAL PASS. Strategy is NOT VALIDATED.**  
  *Justification:* The test dataset was subject to cross-instrument parameter exposure (ES parameters evaluated across the calendar year) and intermediate Q2 performance reports were inspected by the researcher prior to protocol execution. Full empirical validation remains conditional upon independent out-of-sample data.
