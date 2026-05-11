# Indicator Readings Framework

Standardised interpretation rules for all technical agents (`day-trade-analyst`, `chart-analyst`, `signal-tracker`). Every agent uses these definitions identically — no local overrides.

---

## RSI (Relative Strength Index, period 14)

### Zone Definitions

| RSI Range | Label | Meaning |
|-----------|-------|---------|
| > 75 | **Extreme Overbought** | Strong upward momentum, but exhaustion risk. Counter-trend shorts become viable at key S/R. |
| 60–75 | **Overbought** | Trend is bullish. Do not fade; look for longs on pullbacks only. |
| 50–60 | **Bullish Neutral** | Moderate bullish pressure. Trend continuation setups preferred. |
| 40–50 | **Bearish Neutral** | Moderate bearish pressure. Trend continuation shorts preferred. |
| 25–40 | **Oversold** | Trend is bearish. Do not fade; look for shorts on bounces only. |
| < 25 | **Extreme Oversold** | Strong downward momentum, exhaustion risk. Counter-trend longs viable at key S/R. |

### Divergence Rules

**Bearish divergence (short signal):** Price makes a higher high, RSI makes a lower high.
- Must span ≥3 candles on the analysis timeframe
- Only actionable at resistance (order block, swing high, VWAP +1σ)
- Stronger if also visible on the next HTF

**Bullish divergence (long signal):** Price makes a lower low, RSI makes a higher low.
- Must span ≥3 candles on the analysis timeframe
- Only actionable at support (order block, swing low, VWAP −1σ)
- Stronger if also visible on the next HTF

### RSI as Bias Signal

- RSI crossing 50 upward on H4 or H1: bullish shift (+1 bias point)
- RSI crossing 50 downward on H4 or H1: bearish shift (−1 bias point)
- RSI 55–65 on M15 while price is pulling back: trend is healthy, pullback entry valid
- RSI >70 on M15 at point of entry: skip entry — momentum is extended, risk/reward deteriorates

---

## MACD (12, 26, 9)

### Signal Definitions

| Signal | Condition | Weight |
|--------|-----------|--------|
| **Bullish cross** | MACD line crosses above signal line | Medium — early trend signal |
| **Bearish cross** | MACD line crosses below signal line | Medium — early trend signal |
| **Histogram expansion** | Histogram bars growing in one direction | Strong — momentum is accelerating |
| **Histogram contraction** | Histogram bars shrinking (still same side) | Caution — momentum fading, possible reversal |
| **Zero-line cross** | MACD line crosses zero | Strong — trend change on that timeframe |
| **Divergence** | Price new H/L, MACD histogram fails to confirm | Strong reversal signal (use with RSI divergence) |

### MACD as Bias Signal

- MACD histogram positive and expanding on H4: bullish bias (+1)
- MACD histogram negative and expanding on H4: bearish bias (−1)
- MACD histogram direction (H1): confirms or contradicts H4; same direction = +1, opposite = −1
- Do NOT act on MACD cross alone on M5 — too noisy. Use as confluence only.

### MACD for Entry Timing

- Histogram turning from negative to less-negative (first bar shrink): early long signal inside demand zone
- Histogram turning from positive to less-positive: early short signal inside supply zone
- Zero-line cross on M15 aligned with zone: strong confluence confirmation

---

## EMA (Exponential Moving Average)

### Standard Periods Used

| Period | Timeframe Context | Role |
|--------|-------------------|------|
| EMA 20 | M5, M15, H1, H4 | Short-term trend direction, dynamic S/R |
| EMA 50 | M15, H1, H4 | Intermediate trend, pullback target |
| EMA 200 | D1, H4 | Long-term trend bias, major institutional level |

### EMA Order (Trend Signal)

- **Bullish stack:** EMA20 > EMA50 > EMA200 → all timeframes aligned bullish
- **Bearish stack:** EMA20 < EMA50 < EMA200 → all timeframes aligned bearish
- **Mixed:** Any other order → no clear trend bias from EMAs

### EMA as Dynamic Support/Resistance

- Price at EMA20 (M15) in a trending market: high-probability bounce setup
- Price at EMA50 (M15): deeper pullback, still tradable if trend intact
- Price at EMA200 (D1): major level — expect reaction, often a reversal
- EMA cluster (two or more EMAs within 2pts of each other): treat as a zone, not a line

### EMA Cross Signals

| Cross | Timeframe | Strength |
|-------|-----------|----------|
| EMA20 crosses EMA50 | H4 | Strong trend change signal |
| EMA20 crosses EMA50 | H1 | Moderate trend change |
| EMA20 crosses EMA50 | M15 | Entry signal (use as confluence) |
| EMA20 crosses EMA50 | M5 | Noise — use as confirmation only, not standalone |

---

## Bollinger Bands (Period 20, 2σ)

### Zone Definitions

| Price Location | Meaning |
|----------------|---------|
| At or above upper band (+2σ) | Statistically extended — potential mean reversion short |
| Above midline, approaching upper band | Trend bullish, room to run but watch for expansion stall |
| Near midline (±0.5σ) | Equilibrium — price at mean, direction unclear |
| Below midline, approaching lower band | Trend bearish, room to run |
| At or below lower band (−2σ) | Statistically extended — potential mean reversion long |

### Bollinger Band Signals

**BB Squeeze:** Upper and lower bands converging (band width <50% of recent average). Indicates low volatility, breakout imminent. Direction unknown — wait for candle to commit.

**BB Expansion:** Bands widening after a squeeze. Price direction during first expansion candle is the likely breakout direction. High-momentum entry.

**Walking the Band:** Price repeatedly touching or closing outside the band without reverting to midline. Strong trend — do not fade, only trade with trend.

**Mean Reversion:** Price at extreme band (+2σ or −2σ) at key S/R level. Entry toward midline. Only trade if RSI is also extreme and MACD histogram is contracting.

### Bollinger Bands as Confluence

- Price at upper BB + supply zone + RSI >70: strong short confluence
- Price at lower BB + demand zone + RSI <30: strong long confluence
- Midline rejection (bullish): price bounces off midline in uptrend → continuation
- Midline rejection (bearish): price bounces off midline in downtrend → continuation

---

## VWAP (Volume-Weighted Average Price)

### Role by Session

VWAP resets at the start of each trading session. It represents the fair value at which institutions have transacted on average for the day.

| Price vs VWAP | Intraday Bias |
|---------------|---------------|
| Price > VWAP | Intraday bullish — buyers in control since open |
| Price < VWAP | Intraday bearish — sellers in control since open |
| Price at VWAP | Decision point — watch for reaction direction |

### VWAP as Entry Framework

- **Long above VWAP:** Buy pullbacks to VWAP; target previous high or next supply zone
- **Short below VWAP:** Sell bounces to VWAP; target previous low or next demand zone
- **VWAP cross with reclaim:** Powerful intraday signal (see day-trade-setups.md Setup 2)

### VWAP Deviation Bands (if available)

| Band | Meaning |
|------|---------|
| VWAP + 1σ | First resistance above fair value |
| VWAP + 2σ | Extended above fair value — mean reversion risk |
| VWAP − 1σ | First support below fair value |
| VWAP − 2σ | Extended below fair value — mean reversion risk |

**Note:** VWAP is only meaningful during active sessions (London open to NY close). Disregard VWAP readings during Asian pre-market or after-hours.

---

## Stochastic (14, 3, 3)

### Zone Definitions

| Stochastic Range | Label |
|-----------------|-------|
| > 80 | Overbought |
| 50–80 | Bullish momentum |
| 20–50 | Bearish momentum |
| < 20 | Oversold |

### Stochastic Use Cases

**Primary use:** Confirm RSI divergence signals. If RSI divergence AND Stochastic is extreme (>80 or <20), divergence signal is stronger.

**Secondary use:** In ranging markets (no clear trend), Stochastic crosses in overbought/oversold zones can time entries at S/R levels.

**Do NOT use standalone:** Stochastic generates too many false signals in trending markets. Always require at least one other confluence factor.

### Stochastic Cross Signal

- %K crosses %D upward from below 20: bullish confirmation at support
- %K crosses %D downward from above 80: bearish confirmation at resistance

---

## Volume

### Reading Volume

| Volume Reading | Meaning |
|----------------|---------|
| Volume spike (>2× 20-period average) on up candle | Strong buying pressure, institutional participation |
| Volume spike on down candle | Strong selling pressure |
| Volume spike on reversal candle inside zone | High-conviction zone confirmation |
| Declining volume during pullback | Pullback is corrective — trend likely to continue |
| Rising volume during pullback | Pullback may be impulsive — trend may be reversing |
| Volume below average during breakout | Weak breakout — high false-breakout risk |
| High volume at extreme (new high/low) | Exhaustion / climax — potential reversal |

### Volume as Entry Confluence

- Volume spike on the confirmation candle inside a zone: adds MEDIUM confirmation weight (see signal-tracker.md)
- Volume below MA during price approach to zone: price may continue through — zone less reliable
- Declining volume during zone formation (zone origin): zone is weaker than normal

---

## Indicator Alignment Scoring (for day-trade-analyst)

When scoring Indicator Confluence (0–25 in setup scoring), count the number of indicators aligned with the setup direction:

| Indicator | Counts as "aligned" for LONG when... | Counts as "aligned" for SHORT when... |
|-----------|--------------------------------------|---------------------------------------|
| RSI (M15) | RSI 38–62 (reset) and rising, or >50 | RSI 38–62 (reset) and falling, or <50 |
| MACD (M15) | Histogram positive or turning positive | Histogram negative or turning negative |
| VWAP | Price above VWAP | Price below VWAP |
| EMA order (M15) | EMA20 > EMA50 | EMA20 < EMA50 |
| BB position (M15) | Price above midline, below upper band | Price below midline, above lower band |

Count: 3 or more → 25 pts | 2 → 15 pts | 1 → 5 pts | 0 → 0 pts
