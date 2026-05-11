# Finance-Claude: 10-Person Sub-Agent Team

A Claude Code project combining a professional finance team with live TradingView technical analysis. Ten specialized agents collaborate under a master orchestrator, connected to TradingView Desktop via MCP.

## The Team

| Agent | Role |
|-------|------|
| `orchestrator` | **Master brain** — decomposes tasks, delegates, synthesizes |
| `research-analyst` | Fundamental & qualitative investment analysis |
| `quant-analyst` | Backtesting, factor models, historical signal analysis |
| `chart-analyst` | Supply/demand zone detection via TradingView MCP |
| `signal-tracker` | Monitors zones for precise entry timing — fires ENTRY_SIGNAL |
| `portfolio-manager` | Allocation, trade decisions, rebalancing |
| `risk-manager` | VaR, stress tests, SL/TP/position sizing |
| `compliance-officer` | KYC/AML, regulatory filings, sign-off |
| `data-engineer` | Data pipelines, ETL, signal history logging |
| `report-writer` | Polished written output |

## TradingView MCP

Connected via `.mcp.json` → local server at `C:/Users/jones.wong/tradingview-mcp/src/server.js`.
TradingView Desktop must be running with CDP enabled before starting a chart analysis session.
Run `tv_health_check` to verify connection.

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
  5. risk-manager                            → writes 05_risk.md (reads 04c)
  6. portfolio-manager                       → writes 06_portfolio.md (reads 04c + 05)
  7. report-writer                           → writes 07_memo.md (reads all)
```

**Technical trade signal:**
```
/scan → chart-analyst → signal-tracker → risk-manager → portfolio-manager
```

**Combined conviction trade (fundamental + technical aligned):**
```
orchestrator → [research-analyst + quant-analyst + chart-analyst] (parallel)
             → signal-tracker (waits for zone entry timing)
             → risk-manager → portfolio-manager → report-writer
```

**Quarterly investor report:**
```
orchestrator → data-engineer → [portfolio-manager + risk-manager] → report-writer → compliance-officer
```

## Shared Workspace Protocol

Every multi-agent analysis uses a shared workspace so agents communicate through files, not through the orchestrator:

- **Path**: `workspace/{TICKER}_{YYYYMMDD}/`
- **Each agent** reads its inputs from and writes its outputs to the workspace directory
- **Naming convention**: `01_data.md`, `03a_research.md`, `03b_quant.md`, `04a_research_rebuttal.md`, `04b_quant_rebuttal.md`, `04c_synthesis.md`, `05_risk.md`, `06_portfolio.md`, `07_memo.md`
- **Cross-debate**: after parallel analysis, each analyst reads the other's output and writes a rebuttal before the orchestrator synthesizes
- Workspace files are gitignored (treated as ephemeral analysis output)

## Zone Analysis Framework

The `chart-analyst` and `signal-tracker` agents use `skills/zone-analysis.md` as their shared framework.

- Zones are **areas** (proximal + distal edge), never single lines
- Scored 0–100 across freshness, origin strength, and confluence
- Grade A (75+): primary watch. Grade B (50–74): secondary. Below 50: discard
- Entry requires confirmation inside zone, not just zone touch
- All signals logged by `data-engineer` → `quant-analyst` runs hit-rate analysis → improves future scoring

## Safety & Permissions

- `.claude/settings.json` — pre-approves common Python/git/data commands; denies destructive ones
- `.claude/hooks/block-large-data-files.sh` — blocks large data files and secret patterns
- `.gitignore` — excludes `.env`, secrets, data files, workspace output

## Local Setup

1. Ensure TradingView Desktop is running with CDP enabled
2. Ensure `C:/Users/jones.wong/tradingview-mcp/src/server.js` is accessible
3. Copy `CLAUDE.local.md.example` → `CLAUDE.local.md` and fill in personal overrides
4. Start Claude Code in this directory — MCP connects automatically

## Project Structure

```
Finance-Claude/
├── CLAUDE.md                      # this file
├── CLAUDE.local.md.example
├── .gitignore
├── .mcp.json                      # MCP server configs
└── .claude/
    ├── settings.json
    ├── agents/
    │   ├── orchestrator.md
    │   ├── chart-analyst.md       # TradingView zone detection
    │   ├── signal-tracker.md      # Entry timing
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
    ├── skills/
    │   └── zone-analysis.md       # Shared zone framework
    ├── output-styles/
    │   └── memo.md
    └── hooks/
        └── block-large-data-files.sh
```
