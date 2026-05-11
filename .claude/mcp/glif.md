# Glif MCP Server

**Package:** `glif-mcp-server`  
**Repo:** https://github.com/glifxyz/glif-mcp-server  
**Primary users:** report-writer, research-analyst

## Purpose

Glif lets agents run AI workflows ("glifs") hosted on glif.app — composable pipelines that chain models, image generators, and tools. In a finance context, use it to generate charts, infographic summaries, or visual portfolio snapshots by calling pre-built or custom glifs without writing new pipelines.

## Setup

1. Obtain an API token from [glif.app/settings](https://glif.app/settings).
2. Add to `.env`:
   ```
   GLIF_API_TOKEN=your_token_here
   ```
3. Registered in `.mcp.json`:
   ```json
   "glif": {
     "command": "npx",
     "args": ["-y", "glif-mcp-server"],
     "env": { "GLIF_API_TOKEN": "${GLIF_API_TOKEN}" }
   }
   ```

## Tools Exposed

### `run_glif`

Execute a glif by its ID with input variables and return the output.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | yes | Glif ID from glif.app |
| `inputs` | object | yes | Key-value inputs for the glif |

### `list_featured_glifs`

Return a curated list of featured glifs available on the platform.

### `search_glifs`

Search glif.app for glifs matching a keyword.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | yes | Search terms |

### `get_glif`

Fetch metadata and input schema for a specific glif.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | yes | Glif ID |

## Example Workflows

### report-writer: generate a portfolio chart image

Find a glif that renders a pie or bar chart, pass portfolio weights as inputs, and embed the returned image URL in the investor report.

```
Tool: search_glifs
Query: "portfolio allocation chart"

Tool: run_glif
id: <found glif id>
inputs: { "labels": "TSLA,AAPL,MSFT,Cash", "values": "25,30,35,10" }
```

### report-writer: executive summary visual

Run a glif that formats a text summary as a polished infographic for inclusion in client-facing decks.

### research-analyst: sentiment visualization

Pass a list of news headlines to a sentiment-scoring glif and get back a simple visual heatmap or score card.
