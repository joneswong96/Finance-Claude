# Finance-Claude: 5-Person Sub-Agent Team

This project uses Claude Code's sub-agent system to simulate a professional finance team. Five specialized agents collaborate to handle the full investment workflow.

## The Team

| Agent | Role | When to Use |
|-------|------|-------------|
| `research-analyst` | Market research, fundamental analysis, investment thesis | Company/sector deep dives, earnings analysis, macro research |
| `portfolio-manager` | Portfolio construction, asset allocation, trade decisions | Rebalancing, performance review, new position sizing |
| `risk-manager` | VaR, stress testing, compliance, risk limits | Pre-trade risk checks, scenario analysis, limit monitoring |
| `data-engineer` | Data pipelines, ETL, database queries, data quality | Fetching/processing market data, building data models |
| `report-writer` | Research reports, performance summaries, client memos | Any polished written output for internal or external use |

## How to Use

Claude Code will automatically select the right agent based on your task description. You can also explicitly request an agent:

```
# Let Claude choose
"Analyze Apple's Q4 earnings and give me a buy/sell recommendation"

# Explicit agent selection
"Use the risk-manager agent to run a stress test on my current portfolio"
```

## Typical Workflow

A full investment decision cycle typically flows:

```
data-engineer → research-analyst → risk-manager → portfolio-manager → report-writer
```

1. **data-engineer** fetches and prepares the raw financial data
2. **research-analyst** produces the investment thesis
3. **risk-manager** approves the trade within risk limits
4. **portfolio-manager** executes the allocation decision
5. **report-writer** documents everything for stakeholders

## Agent Files

All agent definitions live in `.claude/agents/`. Each file defines the agent's persona, responsibilities, and decision framework.
