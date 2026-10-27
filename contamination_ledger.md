# Research Contamination Ledger

*Ledger Initialization: October 17, 2026*  
*Purpose: Explicit documentation of data exposure events, parameter calibration dependencies, and threats to out-of-sample validity.*

---

## 1. Documented Information Leaks & Contamination Events

1. **Prior Calibration on S&P 500 Futures (`ES`) Across Full Calendar Horizon (October 2025 to October 2026):**
   * Multiple parameter sensitivity scripts (stop-loss distances, time-window restrictions, and profit-lock mechanisms) were iteratively calibrated on the ES contract over the identical calendar year.
2. **Prior Inspection of Nasdaq-100 Futures (`NQ`) Contract (December 2025 to March 2026):**
   * Institutional sweep thresholds (`SweepRatio = 0.08`, absolute volume floor = 20) were refined on October 17 following an initial exploratory run yielding low execution frequency.
3. **Pre-Registration Parameter Exposure:**
   * Sharpe ratio and Sortino ratio ranges derived from exploratory optimization logs were inspected prior to formal protocol registration.
4. **Cross-Asset Market Regime Correlation:**
   * Equity index dynamics between NQ and ES exhibit strong contemporaneous correlation; parameter adaptations on ES informed NQ threshold choices.
5. **A Posteriori Formulation of Session Risk Caps:**
   * The daily profit target cap ($750) and loss cap ($700) were selected after preliminary runs; formalization within prop-firm evaluation constraints was documented a posteriori.

---

## 2. Protocol Governance & Execution Incidents

1. **Inspection of Intermediate Quarterly Outcomes:**
   * Intermediate results for Q2 and Q3 were inspected by the researcher prior to the finalization of the formal evaluation protocol.
2. **Contamination Classification of Horizon Q4 2025 (`NQ DEC25`):**
   * Due to early exploratory parameter adjustments on October 17, the `NQ DEC25` window (October 21, 2025 to December 18, 2025) is classified as development / in-sample and evaluated separately from forward verification sets.
3. **P&L Header Exposure Incident:**
   * The researcher inadvertently inspected the summary P&L header and first 14 trade records of Q2 during integration verification. Strict automated parsing isolation was subsequently instituted.

---

## 3. Maintenance Fixes & Hash Continuity Log

* **Fix F7 (Session Management Continuity):** Restored single protected instantiation of intraday session iterators in `FlowX_Institutional_NQ_v1.cs`. All runs executed prior to F7 were voided and excluded from official performance records.
* **Fix F8 (Diagnostic Funnel Export):** Relocated diagnostic funnel telemetry export before the zero-trade guard clause. Verified zero impact on signal logic, bracket orders, or execution pricing. SHA-256: `7cd50df15ee1489573cc106606d5cc001762460bd151a1476cac936768e4ca9a`.
* **Fix F9 (UI Designtime Logging Guard):** Added guard clause to protect diagnostic outputs from non-executing design-time instances. Zero modification to strategy logic. SHA-256: `9f3664c3651899aad6bba8d565af4a57301b71e279ee2cc280f37deaf6164489`.

---

## 4. Methodological Status & Out-of-Sample Requirement

Because of the documented exploratory exposures and cross-asset calibration history, all reported in-sample performance metrics (+28.20% net return, 3.23 Sharpe ratio, 77.78% win rate) are designated as **Development / In-Sample Incubation**. 

Independent empirical validation requires execution across unexamined historical horizons (e.g., pre-October 2025 quarterly contracts via an independent data provider) under frozen evaluation parameters.
