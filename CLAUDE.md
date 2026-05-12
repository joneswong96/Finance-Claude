# Finance-Claude: 3-Track Trading System

A Claude Code project combining a professional finance team with live TradingView technical analysis. Eleven specialized agents collaborate under a master orchestrator, supporting three trading tracks: intraday day trade, stock swing trade, and ETF 定投/DCA.

**System role:** Analyst and advisor. The system produces analysis, entry prices, and alert levels. The user executes manually on their own platforms (IC Markets, IBKR, Futu).

## Three Tracks

| Track | Type | Instruments | Hold | Platform | Commands |
|-------|------|-------------|------|----------|----------|
| **1** | Day Trade | XAUUSD, NQ, ES, HK50 | Intraday | IC Markets | `/scan`, `/watch` |
| **2** | Stock Swing | Lead stocks (AAPL, NVDA, JPM…) | 2 days–4 weeks | IBKR / Futu | `/screen`, `/swing` |
| **3** | ETF 定投 (DCA) | CSPX, VWRA, 2800.HK | Months–years | IBKR + Futu | `/dca` |

## The Team

Agents are split into two tiers. **Tool agents** gather information and output structured briefs to the shared workspace. **Actioner agents** consume those briefs and make decisions. Actioners never re-gather information a tool agent already produced.

### Model Routing (cost optimization)

| Model | Agents | Rationale |
|-------|--------|-----------|
| **Opus** | orchestrator, research-analyst, portfolio-manager | Judgment, expert thesis, investment decisions |
| **Sonnet** | data-engineer, quant-analyst, chart-analyst, day-trade-analyst, signal-tracker, risk-manager, report-writer, compliance-officer, dca-manager | Data gathering, calculations, structured templates |

### Meta
| Agent | Model | Role |
|-------|-------|------|
| `orchestrator` | Opus | **Master brain** — gates research, delegates, broadcasts briefs, synthesizes |

### Tool Agents — information gatherers
| Agent | Model | Output Brief |
|-------|-------|-------------|
| `data-engineer` | Sonnet | Data Package: cleaned, validated datasets |
| `research-analyst` | Opus | Research Brief: qualitative thesis, fundamentals, why-triggers |
| `quant-analyst` | Sonnet | Quant Brief: signals, backtest results, statistical anomalies |
| `chart-analyst` | Sonnet | Zone Brief: macro zones (方向偏向) + SNR ladder (scalp) OR SWING_ZONE_SIGNAL (swing, W1→D1→H4→H1) |
| `day-trade-analyst` | Sonnet | Day-Trade Brief: Grade A/B intraday entries (LONG + SHORT) with entry/SL/TP drawn on TradingView — activates via `/scan` |
| `dca-manager` | Sonnet | DCA Brief: this month's buy amounts, volatility multipliers, alert price levels — activates via `/dca` |

### Actioner Agents — decision makers
| Agent | Model | Role |
|-------|-------|------|
| `signal-tracker` | Sonnet | Monitors zones for precise entry timing — fires ENTRY_SIGNAL |
| `portfolio-manager` | Opus | Allocation, trade decisions, rebalancing |
| `risk-manager` | Sonnet | VaR, stress tests, limit approvals |
| `compliance-officer` | Sonnet | KYC/AML, regulatory filings, sign-off |
| `report-writer` | Sonnet | Polished written output |

### Research Gate
Before commissioning any tool agent, the orchestrator scores the request on **materiality × novelty**. Low on both → skip research, use cached knowledge. High on either → proceed. The research-analyst applies a further depth gate internally: Shallow Scan → Standard Analysis → Deep Dive (triggered only by specific anomaly signals called "Why Triggers").

## Cost Budget

Each agent has a turn limit and output token budget enforced in its definition:

| Agent | Max Turns | Output Budget | Approx Cost |
|-------|-----------|---------------|-------------|
| orchestrator | — | — | ~$0.75 |
| data-engineer | 5 | 800 tokens | ~$0.30 |
| research-analyst | 6 (shallow: 3) | 1,000 tokens | ~$2.18 |
| quant-analyst | 5 | 800 tokens | ~$0.33 |
| chart-analyst | 6 (deep: 8) | 1,000 tokens | ~$0.30 |
| day-trade-analyst | 8 | 1,200 tokens | ~$0.40 |
| signal-tracker | 4 | 600 tokens | ~$0.15 |
| risk-manager | 4 | 800 tokens | ~$0.23 |
| portfolio-manager | 3 | 800 tokens | ~$0.98 |
| report-writer | 3 | 1,500 tokens | ~$0.26 |
| compliance-officer | 3 | 600 tokens | ~$0.15 |

**Estimated pipeline costs:**
- `/scan` (day-trade): ~$0.40
- `/watch` (signal + risk + portfolio): ~$1.36
- `/screen` (lead stocks): ~$1.80
- `/swing` (stock swing setup): ~$1.10
- `/dca` (DCA brief): ~$0.20
- `/analyze` (fundamental, no rebuttal): ~$5.00
- `/analyze` (fundamental, with rebuttal): ~$6.70
- `/analyze` (combined): ~$7.00
- `/quarterly-report`: ~$4.50

## TradingView MCP

Connected via `.mcp.json` → local server at `C:/Users/jones.w/tradingview-mcp/src/server.js`.
TradingView Desktop must be running with CDP enabled before starting a chart analysis session.

## Slash Commands

| Track | Command | What It Does |
|-------|---------|--------------|
| **1** | `/scan XAUUSD` | Scan TradingView for Grade A intraday entries |
| **1** | `/watch XAUUSD LONG 2048.5 2041.0` | Monitor a zone and fire entry signal when confirmed |
| **2** | `/screen` | Weekly lead stock hunt — top 5 swing candidates from leading sectors |
| **2** | `/swing NVDA` | Full swing setup: entry/SL/TP/alert levels for a specific stock |
| **3** | `/dca` | This month's DCA buy amounts + alert price levels |
| **3** | `/dca check CSPX` | Spot check: current multiplier for one ETF |
| **3** | `/dca setup` | First-time: configure your ETF roster and base amounts |
| **3** | `/dca log CSPX 2.5 518.40` | Record a purchase for performance tracking |
| **3** | `/dca report` | Performance review: CAGR, P&L, DCA vs lump-sum |
| — | `/analyze TSLA` | Full fundamental investment analysis |
| — | `/backtest <strategy>` | Quant backtest with full performance & risk metrics |
| — | `/risk-check AAPL 1000 buy` | Pre-trade risk review |
| — | `/quarterly-report Q1 2026` | Quarterly investor report (full team) |
| — | `/compliance-review <doc>` | Compliance sign-off on a document |

## Standard Workflow Sequences

**Day trade signal (Track 1):**
```
/scan → day-trade-analyst (D1→H4→H1→M15→M5) → draws on TradingView → saves to analysis_history
/watch SYMBOL DIRECTION PROXIMAL DISTAL → signal-tracker → risk-manager → portfolio-manager
```

**Stock swing trade (Track 2):**
```
/screen → data-engineer (RS screen) → research-analyst (Shallow × 3) → ranked top 5 → saves to analysis_history
/swing TICKER → orchestrator (SWING mission):
  parallel: chart-analyst [SWING MODE W1→D1→H4→H1] + data-engineer [catalyst only]
  → risk-manager [SWING: R:R≥2:1, earnings gate] → portfolio-manager [SWING: batch split]
  → user output with 🔔 alert levels → saves to analysis_history
```

**ETF DCA (Track 3):**
```
/dca → dca-manager → fetches live prices + 200D MA → applies volatility multiplier
     → outputs buy amounts + alert levels → saves to analysis_history
```

**Full investment analysis (fundamental, with conditional cross-debate):**
```
orchestrator spawns:
  1. data-engineer                           → writes workspace/{ID}/01_data.md
  2. research-analyst + quant-analyst        → write 03a + 03b (parallel, read 01)
  3. [REBUTTAL GATE] if directions disagree:
     research-analyst + quant-analyst        → write 04a + 04b rebuttals (parallel)
     if directions agree: skip rebuttals     → saves ~$1.70
  4. orchestrator                            → writes 04c synthesis
  5. risk-manager                            → writes 05_risk.md
  6. portfolio-manager                       → writes 06_portfolio.md
  7. report-writer                           → writes 07_memo.md
```

**Quarterly investor report:**
```
orchestrator → data-engineer → [portfolio-manager + risk-manager] → report-writer → compliance-officer
```

## Shared Workspace Protocol

Every multi-agent analysis writes to `workspace/{TICKER}_{YYYYMMDD}/`. Agents communicate through files — not through the orchestrator. Workspace files are gitignored (ephemeral analysis output).

## Technical Frameworks (Skills)

| File | Used By | What It Covers |
|------|---------|----------------|
| `.claude/skills/zone-analysis.md` | chart-analyst, signal-tracker | Zone scoring, grade boundaries, confluence rules (scalp) |
| `.claude/skills/day-trade-setups.md` | day-trade-analyst, signal-tracker | 5 intraday setup types with entry/SL/TP rules |
| `.claude/skills/swing-setups.md` | chart-analyst (SWING MODE), risk-manager, portfolio-manager | 3 swing setup types, structural SL %, R:R ≥2:1 rules |
| `.claude/skills/indicator-readings.md` | All technical agents | Standardised RSI/MACD/EMA/BB/Stochastic interpretation |

Zones scored 0–100; Grade A (75+) primary, Grade B (50–74) secondary, below 50 discarded.

## HTML Dashboard

Local web dashboard — archives every `/scan`, `/swing`, `/screen`, `/dca` analysis run.

```bash
# One-time setup
pip install fastapi uvicorn

# Start (from Finance-Claude root)
uvicorn dashboard.server:app --host 0.0.0.0 --port 8080 --reload

# Access
# PC:           http://localhost:8080
# Phone/tablet: http://<your-pc-ip>:8080
```

Features: analysis cards with status tracking (ACTIVE / TAKEN / EXPIRED), personal notes, full detail view, filter by command type or symbol. SQLite `analysis_history` table — agents write to it automatically at the end of each command run.

## MCP Servers

6 MCP servers in `.mcp.json` — each with a distinct, non-overlapping purpose:

| Server | Purpose | Primary Users |
|--------|---------|--------------|
| `tradingview` | Live chart access via TradingView Desktop CDP | chart-analyst, signal-tracker |
| `financial-analysis` | Built-in Python tools: DCF, ratios, portfolio math, stock data | data-engineer, quant-analyst, risk-manager, portfolio-manager |
| `sqlite` | Local financial database — cached data, signal logs, trade history | data-engineer, quant-analyst, signal-tracker |
| `fetch` | Lightweight HTTP: SEC EDGAR, FRED, direct API calls | data-engineer, research-analyst, compliance-officer, orchestrator |
| `playwright` | Browser automation for JS-heavy pages and research portals | research-analyst, data-engineer, compliance-officer |
| `polymarket` | Crowd-implied event probabilities (read-only, DEMO_MODE) | research-analyst, quant-analyst, orchestrator |

## Safety & Permissions

- `.claude/settings.json` — pre-approves common Python/git/data commands; denies destructive ones
- `.claude/hooks/block-large-data-files.sh` — blocks large data files and secret patterns
- `.gitignore` — excludes `.env`, secrets, data files, workspace output

## Local Setup

1. Ensure TradingView Desktop is running with CDP enabled
2. Ensure `C:/Users/jones.w/tradingview-mcp/src/server.js` is accessible
3. Copy `CLAUDE.local.md.example` → `CLAUDE.local.md` and fill in personal overrides
4. Put API keys in `.env` (gitignored)
5. Start Claude Code — MCP connects automatically
6. First DCA use: run `/dca setup` to configure your ETF roster
7. Start dashboard: `uvicorn dashboard.server:app --host 0.0.0.0 --port 8080 --reload`

## Project Structure

```
Finance-Claude/
├── CLAUDE.md
├── CLAUDE.local.md.example
├── .gitignore
├── .mcp.json                      # 6 MCP server configs
├── dashboard/
│   ├── server.py                  # FastAPI server (uvicorn dashboard.server:app)
│   └── index.html                 # Single-page dashboard UI
└── .claude/
    ├── settings.json
    ├── agents/
    │   ├── orchestrator.md        # Master brain — SWING + SCREEN mission types added
    │   ├── chart-analyst.md       # Scalp zones (Standard) + SWING MODE (W1→D1→H4→H1)
    │   ├── day-trade-analyst.md
    │   ├── signal-tracker.md
    │   ├── research-analyst.md
    │   ├── quant-analyst.md
    │   ├── portfolio-manager.md   # Scalp execution + SWING execution protocol
    │   ├── risk-manager.md        # SCALP mode + SWING mode
    │   ├── compliance-officer.md
    │   ├── data-engineer.md
    │   ├── report-writer.md
    │   └── dca-manager.md         # NEW — ETF DCA advisor
    ├── commands/
    │   ├── scan.md                # + analysis_history save step
    │   ├── watch.md
    │   ├── screen.md              # NEW — weekly lead stock hunt
    │   ├── swing.md               # NEW — stock swing setup
    │   ├── dca.md                 # NEW — ETF DCA advisory
    │   ├── analyze.md
    │   ├── backtest.md
    │   ├── risk-check.md
    │   ├── quarterly-report.md
    │   └── compliance-review.md
    ├── mcp/                       # MCP server docs
    ├── skills/
    │   ├── zone-analysis.md
    │   ├── day-trade-setups.md
    │   ├── swing-setups.md        # NEW — 3 swing setup types, structural SL rules
    │   └── indicator-readings.md
    ├── output-styles/
    │   └── memo.md
    └── hooks/
        └── block-large-data-files.sh
```
