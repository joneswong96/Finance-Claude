# FRED MCP Integration

**Server:** `fetch` (`@modelcontextprotocol/server-fetch`)  
**Primary users:** risk-manager, quant-analyst

## Purpose

The FRED (Federal Reserve Economic Data) integration uses the fetch server to pull macroeconomic time series from the St. Louis Fed API. Risk-manager uses these series for macro stress scenarios and yield curve analysis; quant-analyst uses them as factor inputs in return models.

## Setup

Obtain a free API key from [fred.stlouisfed.org](https://fred.stlouisfed.org/docs/api/api_key.html) and add it to `.env`:

```
FRED_API_KEY=your_fred_key
```

The FRED API base URL is `https://api.stlouisfed.org/fred/`. All requests append `&api_key=${FRED_API_KEY}&file_type=json`.

## Key Series

| Series ID | Description | Frequency | Primary Use |
|-----------|-------------|-----------|-------------|
| `GDP` | Real Gross Domestic Product | Quarterly | Growth regime classification |
| `CPIAUCSL` | Consumer Price Index (All Urban) | Monthly | Inflation factor |
| `FEDFUNDS` | Effective Federal Funds Rate | Monthly | Rate environment, discount rate |
| `UNRATE` | Civilian Unemployment Rate | Monthly | Labor market / recession signal |
| `T10Y2Y` | 10-Year minus 2-Year Treasury spread | Daily | Yield curve inversion signal |
| `VIXCLS` | CBOE Volatility Index (VIX) | Daily | Market stress / risk-off regime |

## Example Fetch Calls

### GDP (quarterly)

```json
{
  "url": "https://api.stlouisfed.org/fred/series/observations?series_id=GDP&limit=20&sort_order=desc&api_key=${FRED_API_KEY}&file_type=json",
  "method": "GET"
}
```

Returns the last 20 quarterly observations. Use to classify current growth regime (expansion vs. contraction).

### CPI (monthly inflation)

```json
{
  "url": "https://api.stlouisfed.org/fred/series/observations?series_id=CPIAUCSL&limit=24&sort_order=desc&api_key=${FRED_API_KEY}&file_type=json",
  "method": "GET"
}
```

Returns the last 24 monthly CPI readings. Compute year-over-year percentage change to get the inflation rate used in real return calculations.

### Federal Funds Rate

```json
{
  "url": "https://api.stlouisfed.org/fred/series/observations?series_id=FEDFUNDS&limit=36&sort_order=desc&api_key=${FRED_API_KEY}&file_type=json",
  "method": "GET"
}
```

Used by risk-manager to set the risk-free rate in VaR and Sharpe ratio calculations, and by quant-analyst as a rate-regime factor.

### Unemployment Rate

```json
{
  "url": "https://api.stlouisfed.org/fred/series/observations?series_id=UNRATE&limit=24&sort_order=desc&api_key=${FRED_API_KEY}&file_type=json",
  "method": "GET"
}
```

Used as a leading recession indicator in macro stress scenarios.

### Yield Curve (T10Y2Y)

```json
{
  "url": "https://api.stlouisfed.org/fred/series/observations?series_id=T10Y2Y&limit=252&sort_order=desc&api_key=${FRED_API_KEY}&file_type=json",
  "method": "GET"
}
```

Returns approximately one year of daily yield curve spread data. Values below zero indicate inversion; risk-manager uses this as a key stress scenario trigger.

### VIX (daily)

```json
{
  "url": "https://api.stlouisfed.org/fred/series/observations?series_id=VIXCLS&limit=252&sort_order=desc&api_key=${FRED_API_KEY}&file_type=json",
  "method": "GET"
}
```

Returns approximately one year of daily VIX closes. Used by risk-manager to identify risk-off regimes and scale position sizing recommendations.

## Response Format

All FRED API responses follow this structure:

```json
{
  "observations": [
    {
      "realtime_start": "2026-05-10",
      "realtime_end": "2026-05-10",
      "date": "2026-04-01",
      "value": "5.33"
    }
  ]
}
```

Note: `value` is always a string; cast to float before use. Missing observations are represented as `"."` ; filter these before analysis.
