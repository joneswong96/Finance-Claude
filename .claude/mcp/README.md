# MCP Servers

This folder documents the Model Context Protocol (MCP) servers configured for the Finance-Claude team. Servers are registered in `.mcp.json` at the project root and auto-approved via `enableAllProjectMcpServers: true` in `.claude/settings.json`. They are available to all agents at runtime.

## Configured Servers

| Server | Package | Purpose | Primary Users |
|--------|---------|---------|---------------|
| `brave-search` | `@modelcontextprotocol/server-brave-search` | Web research: news, filings context, analyst reports | research-analyst, compliance-officer |
| `sqlite` | `@modelcontextprotocol/server-sqlite` | Local market data warehouse | data-engineer |
| `fetch` | `@modelcontextprotocol/server-fetch` | Structured HTTP requests to Tiingo, FRED, SEC EDGAR | data-engineer, quant-analyst, risk-manager |

## Quick Setup

1. Copy the environment template and fill in your keys:
   ```
   cp .env.example .env
   ```
   API keys must go in `.env` — never in CLAUDE files or committed to the repo.

2. Install the MCP servers globally (or let `npx` fetch them on first use):
   ```
   npm install -g @modelcontextprotocol/server-brave-search
   npm install -g @modelcontextprotocol/server-sqlite
   npm install -g @modelcontextprotocol/server-fetch
   ```
   The `settings.json` configuration uses `npx -y` so manual installation is optional; servers will be downloaded automatically on first invocation if not already installed.

3. Verify your `.env` contains the required keys:
   ```
   BRAVE_API_KEY=...
   FRED_API_KEY=...
   TIINGO_API_KEY=...
   DB_PATH=./data/finance.db   # optional, defaults to ./data/finance.db
   ```

## Server Documentation

- [brave-search.md](./brave-search.md) — Brave Search API
- [sqlite.md](./sqlite.md) — SQLite local warehouse
- [fetch.md](./fetch.md) — Generic HTTP fetch
- [fred.md](./fred.md) — FRED macroeconomic data (uses fetch server)
