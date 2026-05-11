# Firecrawl MCP Server

**Package:** `firecrawl-mcp`  
**Primary users:** research-analyst, data-engineer, compliance-officer

## Purpose

Firecrawl extracts clean, structured content from any webpage — bypassing JavaScript rendering, ads, and boilerplate — and returns markdown or structured JSON. It handles anti-bot measures, pagination, and bulk crawls. Use it when you need clean article text, table data, or a full site crawl without writing custom scrapers.

## Setup

1. Obtain an API key from [firecrawl.dev](https://firecrawl.dev).
2. Add to `.env`:
   ```
   FIRECRAWL_API_KEY=your_key_here
   ```
3. Registered in `.mcp.json`:
   ```json
   "firecrawl": {
     "command": "npx",
     "args": ["-y", "firecrawl-mcp"],
     "env": { "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}" }
   }
   ```

## Tools Exposed

### `firecrawl_scrape`

Scrape a single URL and return clean markdown or structured data.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | yes | URL to scrape |
| `formats` | array | no | `["markdown"]`, `["html"]`, or `["extract"]` |
| `onlyMainContent` | boolean | no | Strip nav/footer/ads (default: true) |

### `firecrawl_crawl`

Crawl an entire site or section and return all pages as markdown.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | yes | Starting URL |
| `maxDepth` | integer | no | Link depth limit (default: 2) |
| `limit` | integer | no | Max pages to crawl (default: 10) |

### `firecrawl_extract`

Extract specific structured fields from a page using a schema.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | yes | URL to extract from |
| `schema` | object | yes | JSON schema describing fields to extract |
| `prompt` | string | no | Natural language extraction instruction |

### `firecrawl_search`

Search the web and return scraped content of top results (search + scrape in one call).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | yes | Search query |
| `limit` | integer | no | Number of results (default: 5) |

## Example Workflows

### research-analyst: clean earnings press release

```
Tool: firecrawl_scrape
URL: https://ir.tesla.com/news-releases/news-release-details/tesla-vehicle-production-deliveries-...
formats: ["markdown"]
```

Returns clean text without the investor relations site chrome — ready to feed directly into the research memo.

### data-engineer: bulk SEC filing text

```
Tool: firecrawl_crawl
URL: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=TSLA&type=10-K
maxDepth: 1
limit: 5
```

Retrieves 10-K filing index pages in bulk for downstream parsing.

### research-analyst: extract key metrics

```
Tool: firecrawl_extract
URL: https://stockanalysis.com/stocks/tsla/financials/
schema: { "revenue": "number", "netIncome": "number", "eps": "number" }
prompt: "Extract the most recent annual revenue, net income, and EPS"
```
