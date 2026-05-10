# Chrome MCP Server

**Package:** `@modelcontextprotocol/server-puppeteer`  
**Primary users:** data-engineer, research-analyst, compliance-officer

## Purpose

Chrome MCP controls a headless Chromium browser via Puppeteer. It is the lower-level counterpart to the Playwright server — use it when you need direct Chrome DevTools Protocol access, fine-grained network interception, or specific Chromium features. Both servers overlap in capability; Chrome MCP is preferred for lightweight page interactions and PDF generation, while Playwright is preferred for cross-browser testing and richer element selectors.

## Setup

No API key required. Puppeteer downloads a compatible Chromium build on first use.

Registered in `.mcp.json`:
```json
"chrome": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
}
```

## Tools Exposed

### `puppeteer_navigate`

Navigate to a URL in the headless browser.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | yes | Full URL to navigate to |

### `puppeteer_screenshot`

Capture a screenshot of the current page or a specific element.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | yes | Label for the screenshot |
| `selector` | string | no | CSS selector to screenshot a specific element |
| `width` | integer | no | Viewport width (default: 1280) |
| `height` | integer | no | Viewport height (default: 720) |

### `puppeteer_click`

Click an element on the page.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `selector` | string | yes | CSS selector |

### `puppeteer_type`

Type text into an input field.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `selector` | string | yes | CSS selector for the input |
| `text` | string | yes | Text to type |

### `puppeteer_evaluate`

Execute JavaScript in the browser context.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `script` | string | yes | JavaScript to execute |

### `puppeteer_select`

Select an option from a `<select>` dropdown.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `selector` | string | yes | CSS selector for the `<select>` |
| `value` | string | yes | Option value to select |

## Example Workflows

### data-engineer: screenshot a chart for the report

Navigate to a TradingView or Yahoo Finance chart page, wait for it to render, then screenshot just the chart element:

```
puppeteer_navigate: https://finance.yahoo.com/chart/TSLA
puppeteer_screenshot: { selector: "#chart-container", name: "tsla_chart" }
```

### data-engineer: scrape a JavaScript-rendered table

Many financial data portals render tables via React or Angular. Use `puppeteer_evaluate` to extract the rendered DOM:

```javascript
// script passed to puppeteer_evaluate
Array.from(document.querySelectorAll('table tbody tr')).map(row =>
  Array.from(row.querySelectorAll('td')).map(td => td.innerText)
)
```

### compliance-officer: download a PDF filing

Navigate to a filing URL, trigger the download via `puppeteer_evaluate` (or use the print-to-PDF DevTools command), then pass the path to the data pipeline.

## Chrome vs. Playwright

| | Chrome (Puppeteer) | Playwright |
|--|-------------------|-----------|
| Engine | Chromium only | Chromium, Firefox, WebKit |
| API style | CSS selectors, JS eval | Accessibility labels + selectors |
| PDF generation | Native (DevTools) | Supported |
| Network interception | Fine-grained | Supported |
| Best for | Lightweight scraping, PDFs | Rich interactions, cross-browser |
