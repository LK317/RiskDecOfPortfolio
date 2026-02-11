# Risk Decomposition of a 60/40 Portfolio  
**Factors, Sectors, Stress & Regime Analysis (2003–2024)**

This project analyses the **risk structure of a classic 60/40 portfolio** (60% equities, 40% bonds) using factor models, sector proxies, and regime-based stress analysis.

The objective is not return prediction, but **risk attribution**:
> Where does portfolio risk come from, and how does it change across market regimes?

---

## Key Questions

- How much of 60/40 portfolio risk is driven by market exposure?
- Do style factors (SMB, HML, momentum) materially matter?
- Do sector exposures explain incremental risk?
- When and why does diversification fail?
- How does risk structure change across crises and macro regimes?

---

## Data Sources

All data are sourced from **WRDS / Fama–French** and public indices:

- **Equities:** SPY (S&P 500 ETF)
- **Bonds:** AGG (US Aggregate Bond ETF)
- **Factors:** Fama–French (MKT, SMB, HML) + Momentum
- **Industries:** Fama–French 49 Industry Portfolios (daily)
- **Volatility:** VIX

Sample period: **2003-09-20 to 2024-12-31**

---

## Repository Structure

```text
RiskDecOfPortfolio/
├── data/
│   ├── raw/                # Original WRDS / FF / ETF data
│   └── processed/          # Cleaned & merged datasets
│
├── notebooks/
│   ├── 02_risk_profile.ipynb
│   ├── 03_factor_sector_decomposition.ipynb
│   └── 04_stress_regime_analysis.ipynb
│
├── scripts/
│   └── build_master_dataset.py
│
├── src/
│   ├── config.py
│   └── data/
│       └── load_raw.py
│
├── README.md
└── requirements.txt
```

## Methodology Overview

### Portfolio Construction

The balanced portfolio is constructed as:

$$
P_t = 0.6 \cdot \text{SPY}_t + 0.4 \cdot \text{AGG}_t
$$

where SPY represents U.S. equities and AGG represents U.S. investment-grade bonds.

---

### Factor Model

The baseline factor model is:

$$
P_{60/40,t} = \alpha + \beta_{\mathrm{mkt}} \cdot mktrf_t + \beta_{\mathrm{smb}} \cdot smb_t + \beta_{\mathrm{hml}} \cdot hml_t + \beta_{\mathrm{umd}} \cdot umd_t + \varepsilon_t
$$

This specification captures systematic equity risk, size, value, and momentum effects.

---

### Sector Proxies

Sector exposures are constructed as equal-weighted averages of Fama–French industry portfolios:

- **Tech:** Software, Semiconductors  
- **Financials:** Banks, Insurance, Diversified Finance  
- **Energy:** Oil, Coal, Mining  
- **Industrials:** Machinery, Transport, Aerospace  
- **Consumer:** Food, Retail, Restaurants  
- **Healthcare:** Healthcare, Medical Equipment, Drugs  

These proxies are used for **risk interpretation**, not for trading.

---

### Risk Attribution

Risk attribution is performed using:

- OLS regression
- Approximate variance decomposition:
  


- Rolling betas and correlations
- Regime-specific estimation

---

## Results Summary

### Long-Run Risk Profile

| Portfolio | Ann. Mean | Ann. Vol | Sharpe | Max Drawdown |
|---------|-----------|----------|--------|--------------|
| SPY | 11.8% | 18.6% | 0.63 | −55% |
| AGG | 3.0% | 5.2% | 0.57 | −18% |
| **60/40** | **8.4%** | **11.4%** | **0.74** | **−35%** |

**Interpretation:**  
The 60/40 portfolio sacrifices upside relative to equities but delivers superior risk-adjusted performance.

---

### Factor & Sector Decomposition

Approximate variance contribution (full sample):

| Driver | % of Total Variance |
|------|---------------------|
| **Market (mktrf)** | **~85%** |
| SMB | ~1.0% |
| HML | ~0.2% |
| Consumer | ~0.2% |
| Tech | ~0.1% |
| Industrials | ~0.1% |
| Others | < 0.1% |

**Key Insight:**  
Portfolio risk is overwhelmingly driven by market exposure.  
Factors and sectors improve interpretability but do not dominate risk.

---

### Stress Window Analysis

| Period | SPY Cum | AGG Cum | 60/40 Cum | Key Result |
|-----|-------|-------|-----------|-----------|
| GFC (2008–09) | −37% | +3% | −21% | Bonds hedge equities |
| COVID (2020) | −9% | +3% | −4% | Diversification works |
| 2022 Rate Shock | −18% | −15% | −16% | Diversification fails |

**Interpretation:**  
Diversification is effective in equity-led crises but fragile during inflationary and rate-driven shocks.

---

### Regime-Based Risk Structure

| Regime | R² | Market Variance Share |
|------|----|-----------------------|
| Pre-GFC | 0.90 | ~103% |
| GFC | 0.94 | ~63% |
| QE / Low-vol | 0.97 | ~120% |
| COVID era | 0.97 | ~78% |
| Inflation / Rate Shock | 0.94 | **~146%** |

**Key Insight:**  
When diversification fails, market risk concentration increases.

---

## Core Takeaways

- The 60/40 portfolio is conditionally diversified, not structurally diversified.
- Market exposure dominates risk in all regimes.
- Bonds hedge equity risk only in specific macro environments.
- Risk is regime-dependent and state-dependent.

---

## Limitations

- Linear (OLS) framework
- Approximate variance decomposition
- No transaction costs or rebalancing frictions
- No alternative assets included

---

## Possible Extensions

- Regime-aware dynamic allocation
- Inflation-linked and real-asset hedging
- Tail-risk or expected shortfall decomposition
- International diversification

---



## License

MIT License
