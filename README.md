# Financial Services MCP Plugin for Claude Code

A production-quality [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that adds financial analysis capabilities to Claude Code. Built with the `mcp` Python library and `yfinance` for live market data.

## Features

| Tool | Description |
|------|-------------|
| `analyze_stock` | Live stock analysis: P/E, EPS, 52-week range, market cap, analyst consensus, valuation commentary |
| `calculate_dcf` | Discounted Cash Flow valuation with terminal value and per-share intrinsic value |
| `assess_portfolio` | Portfolio value, allocation %, unrealised P&L, concentration risk assessment |
| `calculate_financial_ratios` | Full ratio suite: liquidity, leverage, profitability, efficiency, valuation, DuPont |
| `generate_financial_report` | Structured company report with strengths, concerns, and overall assessment |
| `convert_currency` | Currency conversion across 19 currencies (USD, EUR, GBP, JPY, CAD, AUD, CHF, and more) |
| `compound_interest` | Future value calculator with periodic contributions and year-by-year breakdown |
| `loan_amortization` | Monthly payment, full amortization schedule, and extra-payment savings analysis |

## Quick Start

### Prerequisites

- Python 3.11+
- [Claude Code](https://claude.ai/code) installed

### Installation

```bash
# Clone the repository
git clone https://github.com/joneswong96/Finance-Claude.git
cd Finance-Claude

# Install with pip (editable mode recommended for development)
pip install -e ".[dev]"

# Or install normally
pip install .
```

### Running the server manually

```bash
# Via module
python -m financial_services

# Via installed entry point
financial-services-mcp
```

### Automatic registration with Claude Code

The `.claude/settings.json` file is already configured to register this plugin:

```json
{
  "mcpServers": {
    "financial-analysis": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "financial_services"]
    }
  }
}
```

Claude Code will pick this up automatically when you open the project directory.

## Tool Reference

### `analyze_stock`

Fetches live data from Yahoo Finance.

```
analyze_stock(ticker: str) -> dict
```

**Example:** `analyze_stock("AAPL")`

Returns: company info, price data (current, 52-week range, volume), valuation metrics (P/E, PEG, EV/EBITDA), financials (margins, ROE, ROA), analyst targets, and valuation commentary.

---

### `calculate_dcf`

```
calculate_dcf(
    cash_flows: list[float],      # e.g. [100, 110, 121, 133, 146]
    discount_rate: float,          # e.g. 0.10 (10% WACC)
    terminal_growth_rate: float,   # e.g. 0.025 (2.5%)
    growth_rate: float = 0.0,      # auto-expand single FCF at this rate
    shares_outstanding: float | None = None,
    net_debt: float = 0.0,
) -> dict
```

Returns: PV of each FCF period, terminal value, enterprise value, equity value, and optional intrinsic value per share.

---

### `assess_portfolio`

```
assess_portfolio(
    holdings: list[dict],   # [{"ticker": "AAPL", "shares": 10, "avg_cost": 150.0}, ...]
    risk_free_rate: float = 0.05,
    fetch_live_prices: bool = True,
) -> dict
```

Each holding optionally accepts `current_price` to override live lookup.

Returns: total market value, cost basis, unrealised P&L, per-holding allocation %, concentration HHI, risk level (LOW-MODERATE / MODERATE / ELEVATED / HIGH).

---

### `calculate_financial_ratios`

Accepts any combination of income statement and balance sheet line items:

```
calculate_financial_ratios(
    revenue, gross_profit, operating_income, ebitda, net_income,
    interest_expense, depreciation_amortization,
    total_assets, current_assets, cash_and_equivalents, inventory,
    accounts_receivable, total_liabilities, current_liabilities,
    total_debt, shareholders_equity,
    operating_cash_flow, capital_expenditures,
    market_cap, share_price, shares_outstanding, earnings_per_share,
) -> dict
```

Returns categorised ratios: liquidity, leverage, profitability, efficiency, valuation, DuPont.

---

### `generate_financial_report`

```
generate_financial_report(
    company_name: str,
    ticker: str | None = None,
    revenue, net_income, total_assets, total_liabilities,
    shareholders_equity, current_assets, current_liabilities,
    ebitda, free_cash_flow, revenue_growth_rate,
    industry, fiscal_year,
) -> dict
```

Returns a structured report with key ratios, financial summary, strengths, highlights, concerns, and an overall assessment (Strong / Positive / Neutral / Cautious / Weak).

---

### `convert_currency`

```
convert_currency(
    amount: float,
    from_currency: str,   # e.g. "USD"
    to_currency: str,     # e.g. "EUR"
    show_all_rates: bool = False,
) -> dict
```

Supported: USD, EUR, GBP, JPY, CAD, AUD, CHF, CNY, INR, MXN, SGD, HKD, NZD, SEK, NOK, DKK, ZAR, BRL, KRW.

> **Note:** Rates are static reference values for demonstration. Use a live FX feed in production.

---

### `compound_interest`

```
compound_interest(
    principal: float,
    annual_rate: float,         # e.g. 0.07 (7%)
    years: float,
    compounds_per_year: int = 12,
    additional_contribution: float = 0.0,
    contribution_timing: str = "end",  # or "beginning"
) -> dict
```

Returns: future value, total contributions, total interest earned, effective annual rate, year-by-year growth table.

---

### `loan_amortization`

```
loan_amortization(
    principal: float,
    annual_rate: float,           # e.g. 0.065 (6.5%)
    term_months: int,             # e.g. 360 for 30 years
    extra_monthly_payment: float = 0.0,
    origination_fee: float = 0.0,
) -> dict
```

Returns: monthly payment, total interest, APR estimate, actual payoff timeline, full month-by-month schedule, and extra-payment interest savings.

## Project Structure

```
Finance-Claude/
├── pyproject.toml
├── README.md
├── .claude/
│   └── settings.json          # MCP server registration for Claude Code
└── src/
    └── financial_services/
        ├── __init__.py
        ├── __main__.py        # Enables: python -m financial_services
        ├── server.py          # FastMCP server with all tool registrations
        └── tools/
            ├── __init__.py
            ├── stock.py       # analyze_stock, generate_financial_report
            ├── valuation.py   # calculate_dcf, calculate_financial_ratios
            ├── portfolio.py   # assess_portfolio
            └── calculators.py # compound_interest, loan_amortization, convert_currency
```

## Dependencies

| Package | Purpose |
|---------|---------|
| `mcp[cli]>=1.0.0` | MCP server framework |
| `yfinance>=0.2.40` | Live stock data from Yahoo Finance |
| `pydantic>=2.0.0` | Data validation |

## Disclaimer

This plugin is for educational and analytical purposes only. The financial analysis tools do not constitute investment advice. Stock prices, analyst ratings, and financial data fetched via yfinance are subject to change. Always consult a qualified financial advisor before making investment decisions.

Currency conversion rates are static and for demonstration only — not suitable for real financial transactions.
