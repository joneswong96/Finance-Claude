# Perplexity MCP Server

**Package:** `@perplexityai/mcp-server`  
**Repo:** https://github.com/perplexityai/modelcontextprotocol  
**Primary users:** research-analyst, quant-analyst, orchestrator

## Purpose

Perplexity provides AI-powered search that returns synthesized, cited answers rather than raw web links. It excels at deep research questions — summarizing analyst consensus, explaining macro trends, or investigating company news — without requiring follow-up page scraping.

## Setup

1. Obtain an API key from [perplexity.ai](https://www.perplexity.ai/settings/api).
2. Add to `.env`:
   ```
   PERPLEXITY_API_KEY=your_key_here
   ```
3. Registered in `.mcp.json`:
   ```json
   "perplexity": {
     "command": "npx",
     "args": ["-y", "@perplexityai/mcp-server"],
     "env": { "PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}" }
   }
   ```

## Tools Exposed

### `perplexity_search`

Submit a natural-language query and receive a cited, synthesized answer.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | yes | Research question or search query |
| `model` | string | no | Perplexity model (default: `sonar`) |

Models: `sonar` (fast), `sonar-pro` (deeper reasoning), `sonar-deep-research` (full report).

## Example Workflows

### research-analyst: earnings context

```
Query: "What is the analyst consensus on Tesla Q1 2026 earnings and guidance?"
Model: sonar-pro
```

Returns a synthesized summary with citations, saving time vs. scraping multiple sites.

### quant-analyst: factor research

```
Query: "What academic papers support momentum as a factor in US equities since 2020?"
Model: sonar-deep-research
```

### research-analyst: macro regime

```
Query: "What is the current Fed rate outlook for H2 2026 based on recent FOMC statements?"
Model: sonar
```

## Perplexity vs. Brave Search

| | Perplexity | Brave Search |
|--|-----------|-------------|
| Output | Synthesized answer + citations | Raw ranked links + snippets |
| Best for | Deep research questions | Targeted URL discovery |
| Speed | Slower (LLM reasoning) | Fast |
| Cost | Per-token | Per-query |
