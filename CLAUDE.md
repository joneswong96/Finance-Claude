# Finance-Claude: 8-Person Sub-Agent Team

A Claude Code project that simulates a professional finance team. Eight specialized agents collaborate under a master orchestrator.

## The Team

| Agent | Role |
|-------|------|
| `orchestrator` | **Master brain** — decomposes tasks, delegates, synthesizes |
| `research-analyst` | Fundamental & qualitative investment analysis |
| `quant-analyst` | Backtesting, factor models, statistical analysis |
| `portfolio-manager` | Allocation, trade decisions, rebalancing |
| `risk-manager` | VaR, stress tests, market/credit/liquidity risk |
| `compliance-officer` | KYC/AML, regulatory filings, sign-off |
| `data-engineer` | Data pipelines, ETL, market data |
| `report-writer` | Polished written output |

## Slash Commands

Quick triggers for the standard workflows. Type these in Claude Code:

| Command | What It Does |
|---------|--------------|
| `/analyze TSLA` | Full investment analysis on a ticker |
| `/backtest <strategy>` | Quant backtest with full performance & risk metrics |
| `/risk-check AAPL 1000 buy` | Pre-trade risk review |
| `/quarterly-report Q1 2026` | Quarterly investor report (full team) |
| `/compliance-review <doc>` | Compliance sign-off on a document |

## Output Styles

- `memo` — Analyst memo format: TL;DR, key points, analysis, risks, recommendation. Set via `/output-style memo`.

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

**New position onboarding:**
```
orchestrator → data-engineer → research-analyst → quant-analyst → risk-manager → compliance-officer → portfolio-manager
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

## Safety & Permissions

- `.claude/settings.json` — pre-approves common Python/git/data commands; denies destructive ones (`rm -rf`, `git push --force`, secret reads)
- `.claude/hooks/block-large-data-files.sh` — blocks writing large data files (>50MB) and known-secret patterns
- `.gitignore` — excludes `.env`, `*.local.*`, `data/`, `*.csv`, `*.parquet`, etc.

## Local Setup

1. Copy `CLAUDE.local.md.example` → `CLAUDE.local.md` (gitignored) and fill in your machine-local context
2. Put real API keys in `.env` (also gitignored), never in CLAUDE files
3. Sub-agents will pick up both `CLAUDE.md` (team rules) and `CLAUDE.local.md` (your overrides)

## Project Structure

```
Finance-Claude/
├── CLAUDE.md                      # this file: team rules, shared context
├── CLAUDE.local.md.example        # template for personal overrides
├── .gitignore                     # blocks secrets and data files
└── .claude/
    ├── settings.json              # permissions + hook registry
    ├── agents/                    # 8 sub-agents
    │   ├── orchestrator.md
    │   ├── research-analyst.md
    │   ├── quant-analyst.md
    │   ├── portfolio-manager.md
    │   ├── risk-manager.md
    │   ├── compliance-officer.md
    │   ├── data-engineer.md
    │   └── report-writer.md
    ├── commands/                  # slash commands
    │   ├── analyze.md
    │   ├── backtest.md
    │   ├── risk-check.md
    │   ├── quarterly-report.md
    │   └── compliance-review.md
    ├── output-styles/
    │   └── memo.md
    └── hooks/
        └── block-large-data-files.sh
```
