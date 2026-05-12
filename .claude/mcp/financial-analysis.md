# financial-analysis MCP

Local Python server (`python -m financial_services`) providing 6 structured finance tools. No API key required. Runs offline.

**Primary users:** `data-engineer`, `research-analyst`, `quant-analyst`, `portfolio-manager`, `risk-manager`

**NOT for:** live forex/commodity prices — use TradingView MCP for XAUUSD, EURUSD, indices, futures

---

## Tool Catalog

### 1. `analyze_stock(ticker)`

Fetches live data from yfinance and returns a full stock snapshot.

**Works for:** US-listed equities (AAPL, TSLA, MSFT, SPY, etc.)
**Does NOT work for:** XAUUSD, EURUSD, BTCUSD, crypto, spot forex — use TradingView instead
**Returns:** current price, day OHLC, 52-week H/L, volume, valuation (P/E, PEG, P/B, EV/EBITDA), financials (margins, ROE, ROA, D/E), analyst consensus, target price, valuation commentary

```python
analyze_stock("AAPL")
analyze_stock("GLD")    # gold ETF (not spot gold — for spot, use TradingView)
analyze_stock("GC=F")   # gold futures via yfinance (data quality varies)
```

**Use case:** data-engineer's first call when given a stock ticker. Feeds the data package in one call.

---

### 2. `assess_portfolio(holdings, risk_free_rate=0.05, fetch_live_prices=True)`

Evaluates a portfolio of stock holdings with live prices.

**holdings format:**
```python
[
  {"ticker": "AAPL", "shares": 100, "avg_cost": 185.50},
  {"ticker": "MSFT", "shares": 50,  "avg_cost": 390.00},
]
```

**Returns:** total market value, total cost basis, unrealised P&L per holding (% and $), allocation % per holding, concentration risk (HHI), risk level (LOW-MODERATE / MODERATE / ELEVATED / HIGH), diversification tips

**Use case:** portfolio-manager uses this to read current portfolio state before making allocation decisions.

---

### 3. `calculate_dcf(cash_flows, discount_rate, terminal_growth_rate, ...)`

Standard 5-year DCF with Gordon Growth Model terminal value.

```python
calculate_dcf(
    cash_flows=[100, 110, 121, 133, 146],   # projected FCF per year ($M)
    discount_rate=0.10,                       # WACC (10%)
    terminal_growth_rate=0.025,               # perpetuity growth (2.5%)
    shares_outstanding=5000,                  # for per-share value
    net_debt=500,                             # net debt ($M)
)
```

**Returns:** PV of FCF per year, terminal value, enterprise value, equity value, intrinsic value per share, notes (sensitivity warnings if terminal value >80% of EV)

**Use case:** research-analyst or quant-analyst for fundamental valuation cross-check.

---

### 4. `calculate_financial_ratios(...)`

Comprehensive ratio calculator from raw income statement + balance sheet data.

**Returns:** liquidity (current, quick, cash ratio), leverage (D/E, interest coverage, net debt/EBITDA), profitability (gross margin, EBIT margin, EBITDA margin, net margin, ROE, ROA, ROIC, FCF margin), efficiency (asset turnover, DSO, inventory turnover), valuation (P/E, P/S, P/B, P/FCF, EV/EBITDA), DuPont decomposition

```python
calculate_financial_ratios(
    revenue=394_328,          # $M
    gross_profit=170_782,
    operating_income=114_301,
    net_income=96_995,
    total_assets=352_583,
    total_liabilities=290_437,
    total_debt=111_088,
    cash_and_equivalents=29_965,
    operating_cash_flow=110_543,
    capital_expenditures=10_959,
    market_cap=3_000_000,
    shares_outstanding=15_441,
)
```

**Use case:** quant-analyst for systematic ratio analysis; research-analyst for financial snapshot table.

---

### 5. `generate_financial_report(company_name, ticker, revenue, net_income, ...)`

Generates a narrative financial report from manually provided figures. Returns strengths, concerns, highlights, and an overall assessment (Strong/Positive/Neutral/Cautious/Weak).

**Use case:** When you have financial data from SEC filings and want a structured narrative output. Rarely needed if `analyze_stock` or `calculate_financial_ratios` can do the job.

---

### 6. `convert_currency(amount, from_currency, to_currency)`

⚠️ **DO NOT USE FOR TRADING OR FX ANALYSIS**

Uses **hardcoded static rates** from late 2024. These rates are wrong and will be increasingly stale over time.

- NEVER use for real FX conversions in a trading context
- NEVER report `convert_currency` output as a live exchange rate
- For FX rates: use `quote_get` via TradingView MCP, or `fetch` to a live FX API

This tool exists only for illustrative/educational purposes.

---

## Usage by Agent

| Agent | Tools to Use | Notes |
|-------|-------------|-------|
| `data-engineer` | `analyze_stock` | First call for any stock ticker. Cache result to sqlite. |
| `research-analyst` | `analyze_stock`, `calculate_dcf` | Get live snapshot, then run DCF with projected figures |
| `quant-analyst` | `calculate_financial_ratios`, `calculate_dcf` | Systematic ratio analysis; DCF valuation |
| `portfolio-manager` | `assess_portfolio` | Read current holdings state before making decisions |
| `risk-manager` | `calculate_financial_ratios` | Ratio analysis for financial risk assessment |
| `chart-analyst` | — | Uses TradingView MCP only |
| `day-trade-analyst` | — | Uses TradingView MCP only |
| `signal-tracker` | — | Uses TradingView + sqlite only |

---

## Error Handling

- If yfinance fails: log the error, proceed with SEC/FRED data via `fetch`
- If ticker not found: note in Data Gaps section, do not retry more than once
- `analyze_stock` on a non-US ticker (e.g., "0700.HK"): data may be sparse — validate key fields before using
- All monetary values returned by the tools are in **USD unless otherwise stated in the response**

---

## Quick Reference

```
analyze_stock("AAPL")             → live price + fundamentals (yfinance)
assess_portfolio(holdings)        → P&L + concentration + allocation
calculate_dcf(fcfs, wacc, tgr)   → enterprise value + intrinsic per share
calculate_financial_ratios(...)   → full ratio suite from raw financials
generate_financial_report(...)    → narrative report from manual inputs
convert_currency(...)             → ⚠️ STATIC RATES — never use for trading
```
