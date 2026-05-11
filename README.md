# Finance-Claude

A Claude Code project that fields a **10-person autonomous finance team** connected to live TradingView charts. Agents collaborate through a shared workspace, debate each other's findings, and produce structured investment memos with entry plans, warning flags, and a full audit trail.

---

## The Team

| Tier | Agent | Model | Role |
|------|-------|-------|------|
| Meta | `orchestrator` | Opus | Master brain — gates research, spawns agents, synthesizes |
| Tool | `data-engineer` | Sonnet | Fetches and packages all raw financial data |
| Tool | `research-analyst` | Opus | Senior finance domain expert — moat analysis, expert thesis, hard recommendation |
| Tool | `quant-analyst` | Sonnet | Factor models, backtests, statistical signals |
| Tool | `chart-analyst` | Sonnet | Multi-TF zone analysis + cross-market comparison via TradingView MCP (scored 0–100) |
| Actioner | `signal-tracker` | Sonnet | Watches zones for entry confirmation, fires ENTRY_SIGNAL |
| Actioner | `risk-manager` | Sonnet | VaR, stress tests, stop levels, position limits |
| Actioner | `portfolio-manager` | Opus | Allocation decision, conviction score, trade plan |
| Actioner | `compliance-officer` | Sonnet | Regulatory sign-off on all client-facing output |
| Actioner | `report-writer` | Sonnet | Bilingual investment memo with score card and audit trail |

**Model routing:** Opus for agents that require expert judgment (orchestrator, research-analyst, portfolio-manager). Sonnet for data gathering, calculations, and structured templates (7 agents). This reduces pipeline cost by ~62%.

**Tool agents** write shared briefs. **Actioner agents** consume those briefs and decide. Actioners never re-gather data.

---

## Slash Commands

```
/analyze TSLA              Full investment analysis (fundamental team)
/scan XAUUSD               Scan TradingView for supply/demand zones
/watch XAUUSD LONG 2048.5  Monitor a zone — fires ENTRY_SIGNAL on confirmation
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
```

### API Keys

Copy `.env.example` to `.env`. The current 6-server stack needs no API keys by default:

```env
# Optional — only needed if you restore removed MCPs
# POLYMARKET_PYTHON=~/tools/polymarket-mcp-server/venv/bin/python
# POLYGON_PRIVATE_KEY=...   # only if using Polymarket in live mode
# POLYGON_ADDRESS=...
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

This script launches TradingView Desktop with CDP on port 9222 and verifies the MCP server can connect.

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

## How Analyses Work

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

### Technical analysis (`/scan` + `/watch`)

```
chart-analyst → multi-TF cascade (H4→H1→M15), zones scored 0-100
             → optional: cross-market comparison (Deep Research mode)
signal-tracker → waits for confirmation inside zone → ENTRY_SIGNAL
risk-manager → approves SL/size
portfolio-manager → executes
```

All analysis files land in `workspace/{TICKER}_{YYYYMMDD}/` and are gitignored.

### Research Gate

Before any research is commissioned, the orchestrator scores the request:
- **High materiality OR high novelty** → proceed
- **Low on both** → skip, use cached knowledge, flag assumption

Inside research, the analyst runs: **Shallow Scan** (default) → **Standard Analysis** → **Deep Dive** (triggered by Why Triggers: >2σ deviation, conflicting signals, crowd divergence >15pp).

### Estimated costs per command

| Command | Pipeline | Approx Cost |
|---------|----------|-------------|
| `/scan XAUUSD` | chart-analyst → signal-tracker → risk → PM | ~$0.65 |
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
├── scripts/
│   ├── launch_tv_debug.bat          # Windows: launch TradingView with CDP
│   └── launch_tv_debug.sh           # Mac/Linux equivalent
│
├── src/financial_services/          # Built-in Python MCP plugin
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
    ├── agents/                      # 10 sub-agent definitions
    ├── commands/                    # 7 slash command definitions
    ├── mcp/                         # MCP server documentation
    ├── skills/
    │   └── zone-analysis.md         # Shared zone scoring framework
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

For educational and analytical purposes only. Nothing here constitutes investment advice. Always consult a qualified financial advisor. Live data from Yahoo Finance and other sources may be delayed or inaccurate. Currency rates in the financial-analysis plugin are static reference values.
