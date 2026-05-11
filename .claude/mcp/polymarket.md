# Polymarket MCP Server

**Repo:** https://github.com/caiovicentino/polymarket-mcp-server  
**Language:** Python (requires local clone + install)  
**Primary users:** research-analyst, risk-manager, quant-analyst

## Purpose

Polymarket is a prediction market platform where participants bet real money on the outcome of events. The crowd-implied probabilities embedded in market prices are a high-signal sentiment indicator — often more accurate than polls or analyst forecasts. Use this server to:

- Query the market-implied probability of any event (Fed rate cuts, election outcomes, company mergers, FDA approvals)
- Cross-reference crowd sentiment against your own fundamental analysis
- Identify divergences between market prices and Polymarket probabilities as potential signals
- Weight tail-risk scenarios by their crowd-implied likelihood in risk models

This server runs in **read-only mode** (`DEMO_MODE=true`) by default. No wallet or on-chain credentials are needed for sentiment analysis.

## Setup

This is a Python package installed from source — not available via `npx`.

```bash
# 1. Clone the repo somewhere on your machine
git clone https://github.com/caiovicentino/polymarket-mcp-server.git ~/tools/polymarket-mcp-server
cd ~/tools/polymarket-mcp-server

# 2. Run the installer (creates a venv automatically)
./install.sh

# 3. Add to .env:
POLYMARKET_PYTHON=~/tools/polymarket-mcp-server/venv/bin/python
```

The `DEMO_MODE=true` env var is already set in `.mcp.json` — no wallet setup needed for read-only use.

**To enable trading** (optional, not required for analysis):
```
DEMO_MODE=false
POLYGON_PRIVATE_KEY=your_private_key_without_0x
POLYGON_ADDRESS=your_polygon_wallet_address
```

## MCP Configuration (`.mcp.json`)

```json
"polymarket": {
  "command": "${POLYMARKET_PYTHON:-python3}",
  "args": ["-m", "polymarket_mcp"],
  "env": {
    "DEMO_MODE": "true",
    "POLYGON_PRIVATE_KEY": "${POLYGON_PRIVATE_KEY}",
    "POLYGON_ADDRESS": "${POLYGON_ADDRESS}"
  }
}
```

Set `POLYMARKET_PYTHON` in `.env` to point to the venv Python after install.

## Key Tools for Sentiment Analysis

The server exposes 45 tools across 5 categories. The most relevant for read-only analysis:

### Market Discovery
| Tool | Description |
|------|-------------|
| `search_markets` | Search by keyword, category, or event name |
| `get_trending_markets` | Top markets by 24h/7d/30d volume |
| `get_crypto_markets` | Crypto-specific prediction markets |
| `get_markets_closing_soon` | Markets near resolution (high-confidence signals) |

### Market Analysis
| Tool | Description |
|------|-------------|
| `get_market_prices` | Real-time YES/NO prices = implied probabilities |
| `get_orderbook` | Full orderbook depth and spread |
| `get_market_history` | Historical price series for a market |
| `get_volume_metrics` | Liquidity, volume, and open interest |
| `compare_markets` | Side-by-side probability comparison across events |
| `get_risk_assessment` | AI-generated risk score for a market |

### Monitoring
| Tool | Description |
|------|-------------|
| `subscribe_price_updates` | WebSocket stream of live probability changes |
| `get_market_resolution` | Final resolved outcome of a closed market |

## Example Workflows

### research-analyst: FDA approval probability for a biotech position

```
search_markets("FDA approval [drug name] 2026")
→ find the relevant market
get_market_prices(market_id)
→ YES price = 0.34 means 34% crowd-implied probability of approval
```

Cross-reference with your analyst model. If you assign 60% and the market says 34%, that's a potential long thesis or a reason to revisit your assumptions.

### risk-manager: weight tail scenarios by crowd probability

```
search_markets("US recession 2026")
get_market_prices(market_id)
→ YES = 0.22 (22% recession probability)

search_markets("Fed rate cut September 2026")
get_market_prices(market_id)
→ YES = 0.61
```

Use these as probability weights when stress-testing portfolio scenarios — more rigorous than arbitrary scenario probabilities.

### quant-analyst: prediction market as a factor

```
get_market_history(market_id, start="2025-01-01")
```

Pull historical probability series and correlate with asset price moves around key events. Use as a leading sentiment factor in factor models.

### research-analyst: election / geopolitical risk

```
get_trending_markets(timeframe="7d")
```

Surface the markets with most volume — a proxy for what macro events the crowd is most focused on — and incorporate into thematic research.

## Polymarket vs. Other Sentiment Sources

| | Polymarket | News Sentiment | Analyst Surveys |
|--|-----------|---------------|-----------------|
| Output | Calibrated probability (0–1) | Positive/negative score | Consensus target |
| Skin in the game | Yes (real money) | No | Partially |
| Speed | Real-time | Near real-time | Quarterly |
| Best for | Event probabilities | Narrative direction | Price targets |

## Safety Notes

- `DEMO_MODE=true` is enforced in the MCP config — no orders can be placed unless you explicitly override it in `.env`
- Never commit `POLYGON_PRIVATE_KEY` or `POLYGON_ADDRESS` — they live only in `.env` (gitignored)
- The block-large-data-files hook will flag any attempt to write private key values to project files
