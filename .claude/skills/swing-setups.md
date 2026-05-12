# Swing Trade Setup Framework

Used by: `chart-analyst` (SWING MODE), `risk-manager` (SWING mode), `portfolio-manager` (SWING execution)

---

## Three Setup Types

### 1. Trend Pullback (最常見)

Price is in a W1 uptrend and has pulled back to a D1 demand zone. Best risk-adjusted setup.

**Entry conditions (ALL must be true):**
- W1 trend intact: EMA20 > EMA50, series of higher highs and higher lows
- D1 demand zone Grade B+ (score ≥50)
- D1 RSI reset to 40–55 range (not oversold, not overbought — pullback only)
- MACD turning upward or histogram contracting on D1
- H4 shows CHoCH bullish or BOS bullish at the demand zone boundary
- H1 entry trigger: bullish engulfing candle, pin bar, or close above H1 resistance

**Batch:** 60% first entry / 40% second entry (on zone re-test or deeper pullback)
**Min R:R:** 2:1

---

### 2. Breakout Continuation

Price breaks a key D1 resistance after testing it ≥2 times. Momentum setup.

**Entry conditions (ALL must be true):**
- D1 resistance level tested ≥2× previously (structural significance confirmed)
- Breakout candle closes ABOVE resistance with volume ≥40% above 20D average
- H4 shows BOS above the resistance level
- H1 close above resistance = confirmation candle (wait for this, do not chase the breakout candle itself)
- RSI D1 < 75 (not parabolic)

**Entry:** H1 close above the former resistance (now new support)
**Batch:** 70% first entry / 30% second (on first pullback to former resistance)
**Min R:R:** 2:1

---

### 3. RSI Divergence ⚠️ (Counter-trend — use sparingly)

Price makes a new low but RSI makes a higher low. Shows exhaustion of selling pressure.

**Entry conditions (ALL must be true):**
- D1 RSI bullish divergence: price lower low, RSI higher low
- Stochastic D1 < 25 (oversold confirmation)
- Price at a key D1 S/R level (not mid-air)
- NO earnings within 10 days (binary event risk too high for this setup)
- W1 trend is either sideways or recently reversed (do NOT use in a strong D1 downtrend)

**Entry:** Single entry (not batched — divergence timing is inherently imprecise)
**Batch:** 100% single entry
**Min R:R:** 2:1

---

## Structural Stop-Loss Rules

**LONG trades:**
- SL = 3–5% below the D1 zone distal edge (the further edge of the demand zone from current price)
- Alternative anchor: 3–5% below the last significant W1 swing low
- Use whichever gives a tighter structural level (less distance = better R:R)

**SHORT trades:**
- SL = 3–5% above the D1 zone proximal edge (the nearer edge of the supply zone)
- Alternative anchor: 3–5% above the last significant W1 swing high

**NEVER use point-based stops for swing trades.** Points-based stops are for scalps (M5/M15 timeframe). Swing stops must reference structure.

**Examples:**
- Stock at $100, D1 zone distal at $92.50 → SL at $90 (3.2% below distal). NOT "SL = $93.50 = -6.5pts"
- Stock at $100, D1 zone distal at $88 → SL at $85.50 (3.1% below distal)

If structural SL produces R:R < 2:1, the setup does not qualify. Do not tighten SL artificially to force R:R.

---

## Take-Profit Rules

**TP1 (Primary target):** Next significant D1 resistance level above entry
**TP2 (Extension):** W1 swing high or measured move target

**On reaching TP1:**
- Close 60% of position
- Move SL to breakeven on remaining 40%
- Trail remaining 40% toward TP2

**Time exit:** If neither SL nor TP1 is hit within 4 weeks from entry, close the entire position. Thesis has failed to play out.

---

## Volume Rules

| Condition | Meaning |
|-----------|---------|
| Up days with above-average volume | Institutional accumulation — bullish |
| Down days with below-average volume | Healthy pullback — continuation likely |
| Down days with above-average volume | Distribution — reduce size or skip |
| Breakout on below-average volume | False breakout risk — wait for volume confirmation |

**Volume threshold for breakout confirmation:** Close ≥40% above the 20-day average volume on the breakout candle.

---

## Holding Period

| Scenario | Action |
|----------|--------|
| TP1 hit | Close 60%, trail 40% |
| SL hit | Full close, record the setup, move on |
| Neither after 4 weeks | Close 100% — thesis expired |
| Earnings < 3 days away | Close 100% before earnings if in profit; do not hold through binary event |

---

## Setup Scoring (used by chart-analyst in SWING MODE)

Each swing setup candidate is scored before outputting SWING_ZONE_SIGNAL:

| Factor | Max | Notes |
|--------|-----|-------|
| Zone freshness | 30 | Never tested = 30, once tested = 20, twice = 10, 3+ = discard |
| Zone origin strength | 25 | Explosive departure = 25, strong = 15, gradual = 5 |
| Timeframe alignment | 20 | W1+D1+H4 align = 20, D1+H4 only = 10, D1 only = 5 |
| Volume confirmation | 15 | Clear accumulation pattern = 15, neutral = 5, distribution = 0 |
| Indicator confluence | 10 | RSI in range + MACD turning = 10, one = 5, neither = 0 |

**Total max: 100**
- 75–100: Grade A — execute with full standard size
- 50–74: Grade B — execute with half size or skip unless other conditions are exceptional
- Below 50: discard

---

## Hard Rules (NO exceptions)

1. **R:R ≥ 2:1** — if structural SL makes R:R worse than 2:1, skip the setup
2. **Earnings gate:**
   - Earnings < 5 days away → NO-GO (skip entirely)
   - Earnings 5–14 days away → half-size only
   - Earnings ≥ 15 days away → full size permitted
3. **ADV ≥ 1M shares** — do not enter stocks with less than 1M average daily volume
4. **No M15/M5 entries** — swing trades use D1 zones, H4 triggers, H1 confirmation only
5. **Never force an entry** — if the zone hasn't been reached, wait or move on
