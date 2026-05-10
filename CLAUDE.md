# Finance-Claude: 8-Person Sub-Agent Team

This project uses Claude Code's sub-agent system to simulate a professional finance team. Eight specialized agents collaborate under a master orchestrator to handle the full investment workflow.

## The Team

| Agent | Role | When to Use |
|-------|------|-------------|
| `orchestrator` | **Master brain** — decomposes tasks, delegates to specialists, synthesizes results | Start here for any complex or multi-step task |
| `research-analyst` | Fundamental analysis, qualitative investment thesis, sector research | Company/sector deep dives, earnings analysis, macro research |
| `quant-analyst` | Backtesting, factor models, statistical analysis, systematic signals | Any math/stats/code-driven analysis or strategy research |
| `portfolio-manager` | Portfolio construction, asset allocation, trade decisions | Rebalancing, performance review, new position sizing |
| `risk-manager` | VaR, stress testing, market/credit/liquidity risk, risk limits | Pre-trade risk checks, scenario analysis, limit monitoring |
| `compliance-officer` | KYC/AML, regulatory filings, suitability, audit trails | Any client-facing or regulatory output requiring sign-off |
| `data-engineer` | Data pipelines, ETL, database queries, data quality | Fetching/processing market data, building data models |
| `report-writer` | Research reports, performance summaries, investor memos | Any polished written output for internal or external use |

## How to Use

For simple single-domain tasks, Claude Code picks the right agent automatically from each agent's `description` field.

For complex multi-step tasks, always start with the **orchestrator**:

```
"Orchestrate a full investment analysis on TSLA and give me a trade recommendation"
"Orchestrate a quarterly investor report for our equity fund"
"Use the quant-analyst to backtest a momentum strategy on S&P 500 stocks"
```

## Standard Workflow Sequences

**Full investment analysis:**
```
orchestrator → data-engineer → [research-analyst + quant-analyst] → risk-manager → portfolio-manager → report-writer
```

**New position onboarding:**
```
orchestrator → data-engineer → research-analyst → quant-analyst → risk-manager → compliance-officer → portfolio-manager
```

**Quarterly investor report:**
```
orchestrator → data-engineer → [portfolio-manager + risk-manager] → report-writer → compliance-officer
```

**Regulatory filing:**
```
orchestrator → data-engineer → compliance-officer → report-writer
```

## Agent Files

All agent definitions live in `.claude/agents/`. Each file defines the agent's persona, responsibilities, and decision framework.

The `orchestrator` agent contains the full delegation and sequencing logic, including when to run agents in parallel vs. series.
