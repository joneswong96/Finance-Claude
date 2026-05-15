# Finance-Claude

A Claude Code project that fields a **12-agent autonomous finance team** connected to live TradingView charts. Three trading tracks — intraday day trade, stock swing trade, and ETF DCA — are supported by agents that collaborate through a shared workspace, debate each other's findings, and produce structured memos with entry plans, warning flags, and a full audit trail.

---

## Three Tracks

| Track | Type | Instruments | Hold | Platform | Commands |
|-------|------|-------------|------|----------|----------|
| **1** | Day Trade | XAUUSD, NQ, ES, HK50 | Intraday | IC Markets | `/scan`, `/watch` |
| **2** | Stock Swing | Lead stocks (AAPL, NVDA, JPM…) | 2 days–4 weeks | IBKR / Futu | `/screen`, `/swing` |
| **3** | ETF 定投 (DCA) | CSPX, VWRA, 2800.HK | Months–years | IBKR + Futu | `/dca` |

---

## The Team

| Tier | Agent | Model | Role |
|------|-------|-------|------|
| Meta | `orchestrator` | Opus | Master brain — gates research, spawns agents, synthesizes |
| Tool | `data-engineer` | Sonnet | Fetches and packages all raw financial data |
| Tool | `research-analyst` | Opus | Senior finance domain expert — moat analysis, expert thesis, hard recommendation |
| Tool | `quant-analyst` | Sonnet | Factor models, backtests, statistical signals |
| Tool | `chart-analyst` | Sonnet | Multi-TF zone analysis + cross-market comparison via TradingView MCP (scored 0–100) |
| Tool | `day-trade-analyst` | Sonnet | Intraday scan (D1→H4→H1→M15→M5) — Grade A/B entries drawn on TradingView |
| Tool | `dca-manager` | Sonnet | ETF DCA advisor — volatility-weighted buy amounts + alert price levels |
| Actioner | `signal-tracker` | Sonnet | Watches zones for entry confirmation, fires ENTRY_SIGNAL |
| Actioner | `risk-manager` | Sonnet | VaR, stress tests, stop levels, position limits |
| Actioner | `portfolio-manager` | Opus | Allocation decision, conviction score, trade plan |
| Actioner | `compliance-officer` | Sonnet | Regulatory sign-off on all client-facing output |
| Actioner | `report-writer` | Sonnet | Bilingual investment memo with score card and audit trail |

**Model routing:** Opus for agents that require expert judgment (orchestrator, research-analyst, portfolio-manager). Sonnet for data gathering, calculations, and structured templates (9 agents). This reduces pipeline cost by ~62%.

**Tool agents** write shared briefs. **Actioner agents** consume those briefs and decide. Actioners never re-gather data.

---

## Slash Commands

```
/scan XAUUSD               Scan TradingView for Grade A intraday entries
/watch XAUUSD LONG 2048.5  Monitor a zone — fires ENTRY_SIGNAL on confirmation
/screen                    Weekly lead stock hunt — top 5 swing candidates
/swing NVDA                Full swing setup: entry/SL/TP/alert levels
/dca                       This month's DCA buy amounts + alert price levels
/dca check CSPX            Spot check: current multiplier for one ETF
/dca setup                 First-time: configure your ETF roster and base amounts
/dca log CSPX 2.5 518.40   Record a purchase for performance tracking
/dca report                Performance review: CAGR, P&L, DCA vs lump-sum
/analyze TSLA              Full investment analysis (fundamental team)
/backtest <strategy>       Quantitative backtest with full performance metrics
/risk-check AAPL 1000 buy  Pre-trade risk review
/quarterly-report Q1 2026  Full quarterly investor report
/compliance-review <doc>   Compliance sign-off on any document
```

---

## MCP Servers (6)

Six servers, each with a non-overlapping purpose. No redundancy.

| Server | What it provides |
|--------|-----------------|
| `tradingview` | Live chart access via TradingView Desktop CDP — candles, indicators, zones |
| `financial-analysis` | Built-in Python tools: DCF, ratios, portfolio P&L, stock data, FX |
| `sqlite` | Local financial database — cached data, signal logs, trade history |
| `fetch` | Lightweight HTTP: SEC EDGAR, FRED, direct API calls |
| `playwright` | Browser automation for JS-heavy research pages and regulatory portals |
| `polymarket` | Crowd-implied event probabilities (read-only, no trading) |

**Guiding principle:** Use the best source for the job, then stop. `tradingview` is the only source for chart data. `financial-analysis` is the first call for any calculation. `fetch` covers most data APIs without launching a browser. `playwright` only when a page requires JavaScript execution.

---

## Getting Started

### Prerequisites

- [Claude Code](https://claude.ai/code) installed
- Node.js 18+ (for MCP servers via npx)
- Python 3.11+ (for `financial-analysis` plugin)
- TradingView Desktop (for chart analysis — Windows only)

### Installation

```bash
git clone https://github.com/joneswong96/Finance-Claude.git
cd Finance-Claude

# Install the financial-analysis Python plugin
pip install -e ".[dev]"

# Install dashboard dependencies
pip install fastapi uvicorn
```

### API Keys

Copy `.env.example` to `.env`. The current 6-server stack needs no API keys by default:

```env
# Optional — only needed if you restore removed MCPs
# POLYMARKET_PYTHON=~/tools/polymarket-mcp-server/venv/bin/python
# POLYGON_PRIVATE_KEY=...   # only if using Polymarket in live mode
# POLYGON_ADDRESS=...

# Optional — override the default SQLite database path
# DB_PATH=./data/finance.db
```

`tradingview`, `financial-analysis`, `sqlite`, `fetch`, and `playwright` all require no API keys.
`polymarket` runs in read-only `DEMO_MODE=true` — no keys needed for market queries.

### Local overrides

```bash
cp CLAUDE.local.md.example CLAUDE.local.md
# Fill in machine-specific context (your positions, watchlist, etc.)
```

---

## TradingView MCP Setup

TradingView Desktop must be running with **Chrome DevTools Protocol (CDP)** enabled before chart analysis will work.

### Windows (recommended)

```bat
scripts\launch_tv_debug.bat
```

### Mac / Linux

```bash
bash scripts/launch_tv_debug.sh
```

These scripts launch TradingView Desktop with CDP on port 9222 and verify the MCP server can connect.

### Manual launch

```bat
"C:\Program Files\WindowsApps\TradingView.Desktop_3.1.0.7818_x64__n534cwy3pjxzj\TradingView.exe" --remote-debugging-port=9222
```

Then start Claude Code — the `tradingview` MCP server connects automatically via `.mcp.json`.

### Verify connection

Once Claude Code is open, run:
```
/scan XAUUSD
```
If chart-analyst returns zone data, TradingView MCP is working.

---

## HTML Dashboard

Local web dashboard — archives every `/scan`, `/swing`, `/screen`, `/dca` analysis run.

```bash
# Start (from Finance-Claude root)
uvicorn dashboard.server:app --host 0.0.0.0 --port 8080 --reload

# Access
# PC:           http://localhost:8080
# Phone/tablet: http://<your-pc-ip>:8080
```

Features: analysis cards with status tracking (ACTIVE / TAKEN / EXPIRED), personal notes, full detail view, filter by command type or symbol. SQLite `analysis_history` table — agents write to it automatically at the end of each command run.

The dashboard reads `DB_PATH` from the environment (fallback: `./data/finance.db`), matching the `sqlite` MCP server config in `.mcp.json`.

---

## How Analyses Work

### Day trade (`/scan` + `/watch`)

```
/scan → day-trade-analyst (D1→H4→H1→M15→M5) → draws entries on TradingView → saves to analysis_history
/watch SYMBOL DIRECTION PROXIMAL DISTAL → signal-tracker → risk-manager → portfolio-manager
```

### Stock swing (`/screen` + `/swing`)

```
/screen → data-engineer (RS screen) → research-analyst (Shallow ×3) → ranked top 5
/swing TICKER → chart-analyst [SWING MODE W1→D1→H4→H1] + data-engineer [catalyst]
             → risk-manager [R:R≥2:1, earnings gate] → portfolio-manager [batch split]
             → output with 🔔 alert levels → saves to analysis_history
```

### ETF DCA (`/dca`)

```
/dca → dca-manager → fetches live prices + 200D MA → applies volatility multiplier
     → outputs buy amounts + alert levels → saves to analysis_history
```

### Fundamental analysis (`/analyze`)

```
[Research Gate] → data-engineer (01_data.md)
              → research-analyst + quant-analyst in parallel (03a + 03b)
              → [Rebuttal Gate] if directions disagree:
                  cross-debate rebuttals (04a + 04b)
                  if agree: skip rebuttals (saves ~$1.70)
              → orchestrator synthesis (04c) with named warning flags
              → risk-manager (05_risk.md)
              → portfolio-manager (06_portfolio.md)
              → report-writer (07_memo.md) ← final output
```

### Research Gate

Before any research is commissioned, the orchestrator scores the request:
- **High materiality OR high novelty** → proceed
- **Low on both** → skip, use cached knowledge, flag assumption

Inside research, the analyst runs: **Shallow Scan** (default) → **Standard Analysis** → **Deep Dive** (triggered by Why Triggers: >2σ deviation, conflicting signals, crowd divergence >15pp).

### Estimated costs per command

| Command | Pipeline | Approx Cost |
|---------|----------|-------------|
| `/scan XAUUSD` | day-trade-analyst | ~$0.40 |
| `/watch` | signal-tracker + risk + PM | ~$1.36 |
| `/screen` | data + research ×3 | ~$1.80 |
| `/swing NVDA` | chart + data + risk + PM | ~$1.10 |
| `/dca` | dca-manager only | ~$0.20 |
| `/analyze TSLA` (consensus) | Full pipeline, rebuttals skipped | ~$5.00 |
| `/analyze TSLA` (debate) | Full pipeline, rebuttals triggered | ~$6.70 |
| `/risk-check` | risk-manager only | ~$0.23 |
| `/quarterly-report` | data → PM + risk → writer → compliance | ~$4.50 |

Costs are estimates based on Opus ($15/$75 per M tokens) and Sonnet ($3/$15 per M tokens) pricing.

---

## Output Format

The final memo includes:
- **Score card** — 0-100 composite score, grade, market regime, win-rate probability, named warning flags
- **Trade plan** — batched entry prices + amounts (BUY) or liquidation schedule (SELL), stop-loss, two-stage take-profit
- **Investment thesis** — bull/base/bear scenarios with probabilities and targets
- **Agent audit trail** — every agent's key finding and verdict in one table
- **Unresolved disagreements** — never silently resolved

---

## Project Structure

```
Finance-Claude/
├── README.md
├── CLAUDE.md                        # Team rules (loaded by all agents)
├── CLAUDE.local.md.example          # Template for personal overrides
├── .mcp.json                        # 6 MCP server definitions
├── .gitignore
├── pyproject.toml
│
├── dashboard/
│   ├── server.py                    # FastAPI dashboard server
│   └── index.html                   # Single-page dashboard UI
│
├── scripts/
│   ├── launch_tv_debug.bat          # Windows: launch TradingView with CDP
│   └── launch_tv_debug.sh           # Mac/Linux equivalent
│
├── src/financial_services/          # Built-in Python MCP plugin
│   ├── __init__.py
│   ├── __main__.py
│   ├── server.py
│   └── tools/
│       ├── stock.py                 # analyze_stock, generate_financial_report
│       ├── valuation.py             # calculate_dcf, calculate_financial_ratios
│       ├── portfolio.py             # assess_portfolio
│       └── calculators.py           # compound_interest, loan_amortization, FX
│
├── workspace/                       # Ephemeral analysis output (gitignored)
│   └── .gitkeep
│
└── .claude/
    ├── settings.json                # Permissions + hooks
    ├── agents/                      # 12 sub-agent definitions
    ├── commands/                    # 10 slash command definitions
    ├── mcp/                         # MCP server documentation
    │   └── financial-analysis.md   # Tool catalog for financial-analysis MCP
    ├── skills/
    │   ├── zone-analysis.md         # Zone scoring framework (scalp)
    │   ├── day-trade-setups.md      # 5 intraday setup types
    │   ├── swing-setups.md          # 3 swing setup types, structural SL rules
    │   └── indicator-readings.md    # Standardised RSI/MACD/EMA/BB/Stochastic
    ├── output-styles/
    │   └── memo.md
    └── hooks/
        └── block-large-data-files.sh
```

---

## Safety

- **Permissions** — `.claude/settings.json` pre-approves safe commands; blocks `rm -rf`, force push, secret reads
- **Hook** — `.claude/hooks/block-large-data-files.sh` blocks files >50MB and known secret patterns
- **Gitignore** — excludes `.env`, credentials, data files, workspace output

---

## Disclaimer

For educational and analytical purposes only. Nothing here constitutes investment advice. Always consult a qualified financial advisor. Live data from Yahoo Finance and other sources may be delayed or inaccurate. Currency rates in the financial-analysis plugin are static reference values — never use them for trading or real FX conversions.
