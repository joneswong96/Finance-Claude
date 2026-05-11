# Finance-Claude: 10-Person Sub-Agent Team

A Claude Code project combining a professional finance team with live TradingView technical analysis. Ten specialized agents collaborate under a master orchestrator, connected to TradingView Desktop via MCP.

## The Team

Agents are split into two tiers. **Tool agents** gather information and output structured briefs to the shared workspace. **Actioner agents** consume those briefs and make decisions. Actioners never re-gather information a tool agent already produced.

### Meta
| Agent | Role |
|-------|------|
| `orchestrator` | **Master brain** — gates research, delegates, broadcasts briefs, synthesizes |

### Tool Agents — information gatherers
| Agent | Output Brief |
|-------|-------------|
| `data-engineer` | Data Package: cleaned, validated datasets |
| `research-analyst` | Research Brief: qualitative thesis, fundamentals, why-triggers |
| `quant-analyst` | Quant Brief: signals, backtest results, statistical anomalies |
| `chart-analyst` | Zone Brief: supply/demand zones scored 0–100 via TradingView |

### Actioner Agents — decision makers
| Agent | Role |
|-------|------|
| `signal-tracker` | Monitors zones for precise entry timing — fires ENTRY_SIGNAL |
| `portfolio-manager` | Allocation, trade decisions, rebalancing |
| `risk-manager` | VaR, stress tests, limit approvals |
| `compliance-officer` | KYC/AML, regulatory filings, sign-off |
| `report-writer` | Polished written output |

### Research Gate
Before commissioning any tool agent, the orchestrator scores the request on **materiality × novelty**. Low on both → skip research, use cached knowledge. High on either → proceed. The research-analyst applies a further depth gate internally: Shallow Scan → Standard Analysis → Deep Dive (triggered only by specific anomaly signals called "Why Triggers").

## TradingView MCP

Connected via `.mcp.json` → local server at `C:/Users/jones.wong/tradingview-mcp/src/server.js`.
TradingView Desktop must be running with CDP enabled before starting a chart analysis session.

## Slash Commands

| Command | What It Does |
|---------|--------------|
| `/analyze TSLA` | Full fundamental investment analysis |
| `/scan XAUUSD` | Scan TradingView for active supply/demand zones |
| `/watch XAUUSD LONG 2048.5 2041.0` | Monitor a zone and fire entry signal when confirmed |
| `/backtest <strategy>` | Quant backtest with full performance & risk metrics |
| `/risk-check AAPL 1000 buy` | Pre-trade risk review |
| `/quarterly-report Q1 2026` | Quarterly investor report (full team) |
| `/compliance-review <doc>` | Compliance sign-off on a document |

## Standard Workflow Sequences

**Full investment analysis (with cross-debate):**
```
orchestrator spawns:
  1. data-engineer                           → writes workspace/{ID}/01_data.md
  2. research-analyst + quant-analyst        → write 03a + 03b (parallel, read 01)
  3. research-analyst + quant-analyst        → write 04a + 04b rebuttals (parallel, read each other)
  4. orchestrator                            → writes 04c synthesis
  5. risk-manager                            → writes 05_risk.md
  6. portfolio-manager                       → writes 06_portfolio.md
  7. report-writer                           → writes 07_memo.md
```

**Technical trade signal:**
```
/scan → chart-analyst → signal-tracker → risk-manager → portfolio-manager
```

**Combined conviction trade (fundamental + technical):**
```
[GATE] → data-engineer → [research-analyst + quant-analyst + chart-analyst] (parallel)
       → signal-tracker → risk-manager → portfolio-manager → report-writer
```

**Quarterly investor report:**
```
orchestrator → data-engineer → [portfolio-manager + risk-manager] → report-writer → compliance-officer
```

## Shared Workspace Protocol

Every multi-agent analysis writes to `workspace/{TICKER}_{YYYYMMDD}/`. Agents communicate through files — not through the orchestrator. Workspace files are gitignored (ephemeral analysis output).

## Zone Analysis Framework

`chart-analyst` and `signal-tracker` use `skills/zone-analysis.md` as their shared framework. Zones scored 0–100; Grade A (75+) primary watch, Grade B (50–74) secondary, below 50 discarded.

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
2. Ensure `C:/Users/jones.wong/tradingview-mcp/src/server.js` is accessible
3. Copy `CLAUDE.local.md.example` → `CLAUDE.local.md` and fill in personal overrides
4. Put API keys in `.env` (gitignored)
5. Start Claude Code — MCP connects automatically

## Project Structure

```
Finance-Claude/
├── CLAUDE.md
├── CLAUDE.local.md.example
├── .gitignore
├── .mcp.json                      # 11 MCP server configs
└── .claude/
    ├── settings.json
    ├── agents/
    │   ├── orchestrator.md
    │   ├── chart-analyst.md
    │   ├── signal-tracker.md
    │   ├── research-analyst.md
    │   ├── quant-analyst.md
    │   ├── portfolio-manager.md
    │   ├── risk-manager.md
    │   ├── compliance-officer.md
    │   ├── data-engineer.md
    │   └── report-writer.md
    ├── commands/
    │   ├── scan.md
    │   ├── watch.md
    │   ├── analyze.md
    │   ├── backtest.md
    │   ├── risk-check.md
    │   ├── quarterly-report.md
    │   └── compliance-review.md
    ├── mcp/                       # MCP server docs
    ├── skills/
    │   └── zone-analysis.md
    ├── output-styles/
    │   └── memo.md
    └── hooks/
        └── block-large-data-files.sh
```
