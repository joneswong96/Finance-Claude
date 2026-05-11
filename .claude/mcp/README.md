# MCP Servers

This folder documents the Model Context Protocol (MCP) servers configured for the Finance-Claude team. Servers are registered in `.mcp.json` at the project root and auto-approved via `enableAllProjectMcpServers: true` in `.claude/settings.json`. They are available to all agents at runtime.

## Configured Servers

| Server | Package | Purpose | Primary Users |
|--------|---------|---------|---------------|
| `brave-search` | `@modelcontextprotocol/server-brave-search` | Web research: news, filings context, analyst reports | research-analyst, compliance-officer |
| `sqlite` | `@modelcontextprotocol/server-sqlite` | Local market data warehouse | data-engineer |
| `fetch` | `@modelcontextprotocol/server-fetch` | Structured HTTP requests to Tiingo, FRED, SEC EDGAR | data-engineer, quant-analyst, risk-manager |
| `perplexity` | `@perplexityai/mcp-server` | AI-synthesized research answers with citations | research-analyst, quant-analyst, orchestrator |
| `playwright` | `@playwright/mcp` | Browser automation for JS-heavy and gated sites | research-analyst, data-engineer, compliance-officer |
| `firecrawl` | `firecrawl-mcp` | Clean content extraction and bulk site crawling | research-analyst, data-engineer, compliance-officer |
| `glif` | `glif-mcp-server` | AI workflow pipelines: chart generation, visuals | report-writer, research-analyst |
| `chrome` | `@modelcontextprotocol/server-puppeteer` | Headless Chrome: screenshots, PDF, JS scraping | data-engineer, research-analyst, compliance-officer |
| `polymarket` | GitHub: caiovicentino/polymarket-mcp-server | Crowd-implied event probabilities from prediction markets | research-analyst, risk-manager, quant-analyst |

## Quick Setup

1. Copy the environment template and fill in your keys:
   ```
   cp .env.example .env
   ```
   API keys must go in `.env` — never in CLAUDE files or committed to the repo.

2. All servers launch automatically via `npx -y` on first use — no global install needed.

3. Verify your `.env` contains the required keys:
   ```
   BRAVE_API_KEY=...
   PERPLEXITY_API_KEY=...
   FIRECRAWL_API_KEY=...
   GLIF_API_TOKEN=...
   FRED_API_KEY=...
   TIINGO_API_KEY=...
   POLYMARKET_PYTHON=~/tools/polymarket-mcp-server/venv/bin/python
   DB_PATH=./data/finance.db   # optional, defaults to ./data/finance.db
   ```
   Playwright, Fetch, and Chrome require no API keys.
   Polymarket requires a local clone + install (see [polymarket.md](./polymarket.md)) but no API key for read-only mode.

## Server Documentation

- [brave-search.md](./brave-search.md) — Brave Search API
- [sqlite.md](./sqlite.md) — SQLite local warehouse
- [fetch.md](./fetch.md) — Generic HTTP fetch
- [fred.md](./fred.md) — FRED macroeconomic data (uses fetch server)
- [perplexity.md](./perplexity.md) — Perplexity AI search
- [playwright.md](./playwright.md) — Playwright browser automation
- [firecrawl.md](./firecrawl.md) — Firecrawl web extraction
- [glif.md](./glif.md) — Glif AI workflow pipelines
- [chrome.md](./chrome.md) — Chrome/Puppeteer headless browser
- [polymarket.md](./polymarket.md) — Polymarket crowd-implied event probabilities
