# Brave Search MCP Server

**Package:** `@modelcontextprotocol/server-brave-search`  
**Primary users:** research-analyst, compliance-officer

## Purpose

Provides real-time web search via the Brave Search API. Used for pulling current news, earnings context, regulatory announcements, analyst report summaries, and background research on companies or counterparties.

## Setup

1. Obtain a Brave Search API key from [brave.com/search/api](https://brave.com/search/api/).
2. Add the key to `.env`:
   ```
   BRAVE_API_KEY=your_key_here
   ```
3. The server is registered in `.mcp.json` and launched automatically via `npx`:
   ```json
   "brave-search": {
     "command": "npx",
     "args": ["-y", "@modelcontextprotocol/server-brave-search"],
     "env": {
       "BRAVE_API_KEY": "${BRAVE_API_KEY}"
     }
   }
   ```

No additional installation is required beyond setting the environment variable.

## Tools Exposed

### `brave_web_search`

General web search returning ranked results with titles, URLs, and snippets.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | yes | Search query |
| `count` | integer | no | Number of results (default: 10, max: 20) |
| `offset` | integer | no | Pagination offset |

### `brave_local_search`

Location-aware search for businesses, addresses, and local entities. Less relevant for finance workflows but available for counterparty/broker address lookups.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | yes | Search query |
| `count` | integer | no | Number of results (default: 5) |

## Example Workflows

### research-analyst: pulling earnings context

Before writing an investment memo the research-analyst uses `brave_web_search` to gather recent coverage:

```
Query: "TSLA Q1 2026 earnings analyst reaction site:reuters.com OR site:bloomberg.com"
Query: "Tesla delivery numbers Q1 2026"
Query: "TSLA SEC 10-Q 2026 filing"
```

Results are used to supplement SEC filing data retrieved via the fetch server, providing qualitative market sentiment not available in structured data feeds.

### compliance-officer: counterparty due diligence

```
Query: "Acme Capital Management regulatory action FINRA SEC enforcement 2024 2025"
Query: "Acme Capital AML sanctions OFAC"
```

Results feed into KYC/AML screening as a supplementary open-source intelligence layer alongside structured compliance databases.

### research-analyst: monitoring macro news

```
Query: "Federal Reserve interest rate decision May 2026"
Query: "CPI inflation data April 2026 BLS"
```

Used to contextualize quantitative macro data pulled from FRED before the quant-analyst runs factor models.
