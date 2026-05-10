# Finance-Claude: 8-Person Sub-Agent Team

A Claude Code project that simulates a professional finance team. Eight specialized agents collaborate under a master orchestrator.

## The Team

Agents are split into two tiers. **Tool agents** gather information and output structured briefs. **Actioner agents** consume those briefs and make decisions. Actioners never re-gather information a tool agent already produced.

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

### Actioner Agents — decision makers
| Agent | Role |
|-------|------|
| `portfolio-manager` | Allocation, trade decisions, rebalancing |
| `risk-manager` | VaR, stress tests, limit approvals |
| `compliance-officer` | KYC/AML, regulatory filings, sign-off |
| `report-writer` | Polished written output |

### Research Gate
Before commissioning any tool agent, the orchestrator scores the request on **materiality × novelty**. Low on both → skip research, use cached knowledge. High on either → proceed. The research-analyst applies a further depth gate internally: Shallow Scan → Standard Analysis → Deep Dive (triggered only by specific anomaly signals called "Why Triggers").

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

## MCP Servers

Nine MCP servers are configured in `.mcp.json` and auto-approved via `enableAllProjectMcpServers` in `.claude/settings.json`. See `.claude/mcp/` for full documentation.

| Server | Package | Primary Users |
|--------|---------|---------------|
| `brave-search` | `@modelcontextprotocol/server-brave-search` | research-analyst, compliance-officer |
| `sqlite` | `@modelcontextprotocol/server-sqlite` | data-engineer |
| `fetch` | `@modelcontextprotocol/server-fetch` | data-engineer, quant-analyst, risk-manager |
| `perplexity` | `@perplexityai/mcp-server` | research-analyst, quant-analyst, orchestrator |
| `playwright` | `@playwright/mcp` | research-analyst, data-engineer, compliance-officer |
| `firecrawl` | `firecrawl-mcp` | research-analyst, data-engineer, compliance-officer |
| `glif` | `glif-mcp-server` | report-writer, research-analyst |
| `chrome` | `@modelcontextprotocol/server-puppeteer` | data-engineer, research-analyst, compliance-officer |
| `polymarket` | GitHub: caiovicentino/polymarket-mcp-server | research-analyst, risk-manager, quant-analyst |

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
    ├── mcp/                       # MCP server docs
    │   ├── README.md
    │   ├── brave-search.md
    │   ├── fetch.md
    │   ├── fred.md
    │   ├── sqlite.md
    │   ├── perplexity.md
    │   ├── playwright.md
    │   ├── firecrawl.md
    │   ├── glif.md
    │   ├── chrome.md
    │   └── polymarket.md
    └── hooks/
        └── block-large-data-files.sh
```
