# Fetch MCP Server

**Package:** `@modelcontextprotocol/server-fetch`  
**Primary users:** data-engineer, quant-analyst, risk-manager

## Purpose

Provides structured HTTP requests to external data APIs used in the team's data pipelines. The data-engineer uses it to ingest daily price data from Tiingo, macroeconomic series from FRED, and filing data from SEC EDGAR. No API key is required at the server level; keys are passed per-request via headers sourced from `.env`.

## Setup

No API key is needed to register the server. External service keys are supplied in request headers at call time.

The server is registered in `.claude/settings.json`:

```json
"fetch": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-fetch"]
}
```

Keys for downstream services belong in `.env`:

```
TIINGO_API_KEY=your_tiingo_key
FRED_API_KEY=your_fred_key
```

## Tools Exposed

### `fetch`

Execute an HTTP request and return the response body.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | yes | Full URL to request |
| `method` | string | no | HTTP method: `GET`, `POST`, etc. (default: `GET`) |
| `headers` | object | no | Key-value map of request headers |
| `body` | string | no | Request body for POST/PUT requests |

## Example Requests

### Tiingo -- daily adjusted prices

Fetch the last 30 days of adjusted OHLCV data for a ticker:

```json
{
  "url": "https://api.tiingo.com/tiingo/daily/TSLA/prices?startDate=2026-04-10&endDate=2026-05-10&resampleFreq=daily",
  "method": "GET",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Token ${TIINGO_API_KEY}"
  }
}
```

Response is a JSON array of `{date, open, high, low, close, adjClose, volume}` objects. The data-engineer inserts results into the `prices` table via the sqlite server.

### Tiingo -- ticker metadata

```json
{
  "url": "https://api.tiingo.com/tiingo/daily/TSLA",
  "method": "GET",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Token ${TIINGO_API_KEY}"
  }
}
```

Returns name, description, exchange, and start/end date coverage.

### FRED -- single series

Fetch the last 12 observations of a FRED series (see `fred.md` for series IDs):

```json
{
  "url": "https://api.stlouisfed.org/fred/series/observations?series_id=FEDFUNDS&limit=12&sort_order=desc&api_key=${FRED_API_KEY}&file_type=json",
  "method": "GET"
}
```

### SEC EDGAR -- full-text search

Search for 10-K filings mentioning a company:

```json
{
  "url": "https://efts.sec.gov/LATEST/search-index?q=%22Tesla%2C+Inc%22&dateRange=custom&startdt=2026-01-01&enddt=2026-05-10&forms=10-K",
  "method": "GET",
  "headers": {
    "User-Agent": "FinanceClaude research@example.com"
  }
}
```

SEC EDGAR requires a descriptive `User-Agent` header per their access policy.

### SEC EDGAR -- company facts (XBRL)

Fetch structured financial data for a company by CIK:

```json
{
  "url": "https://data.sec.gov/api/xbrl/companyfacts/CIK0001318605.json",
  "method": "GET",
  "headers": {
    "User-Agent": "FinanceClaude research@example.com"
  }
}
```

Returns all XBRL-tagged facts (revenue, EPS, shares outstanding, etc.) across all filings.
