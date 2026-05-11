# Playwright MCP Server

**Package:** `@playwright/mcp`  
**Repo:** https://github.com/microsoft/playwright-mcp  
**Primary users:** research-analyst, data-engineer, compliance-officer

## Purpose

Playwright gives agents full browser automation: navigate to any URL, interact with JavaScript-heavy pages, fill forms, click elements, and extract content that static HTTP fetches cannot reach. Use it for sites that require login, render data client-side, or block bot scrapers.

## Setup

No API key required. Playwright downloads browser binaries on first use.

Registered in `.mcp.json`:
```json
"playwright": {
  "command": "npx",
  "args": ["-y", "@playwright/mcp"]
}
```

Install browsers ahead of time (optional, avoids first-run delay):
```bash
npx playwright install chromium
```

## Tools Exposed

### `browser_navigate`
Navigate to a URL.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | yes | Full URL to navigate to |

### `browser_snapshot`
Capture the current page as an accessibility snapshot (structured text, fast).

### `browser_screenshot`
Capture a full-page screenshot as base64 PNG.

### `browser_click`
Click an element by its accessibility label or CSS selector.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `element` | string | yes | Accessibility label or selector |

### `browser_type`
Type text into a focused input field.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | string | yes | Text to type |

### `browser_evaluate`
Run JavaScript in the page context and return the result.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `expression` | string | yes | JavaScript expression |

## Example Workflows

### research-analyst: scraping gated financial data

Navigate to a broker research portal, log in with stored credentials, and extract a PDF report link — then hand the URL to the `fetch` server for download.

### data-engineer: ingesting dynamic tables

Some financial data sites render tables via JavaScript (e.g., FINRA bond data, CME settlement prices). Use `browser_navigate` + `browser_snapshot` to capture the rendered DOM, then parse the table.

### compliance-officer: OFAC SDN list check

Navigate to the OFAC search UI, fill the name field with `browser_type`, submit, and extract results — useful when the API is unavailable or requires registration.
