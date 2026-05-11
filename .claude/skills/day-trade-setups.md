# Day-Trade Setup Framework

Shared reference for `day-trade-analyst` and `signal-tracker`. Defines the 5 intraday setup types, their required conditions, and precise entry/SL/TP rules.

All setups target **7.5pts as the base TP1**. TP2 is the next opposing key level.

---

## Setup 1 — Zone Pullback (高確信 — Highest Priority)

**What it is:** Price made a strong impulsive move away from a supply or demand zone. It has since returned to that zone. Institutional order flow is expected to defend the zone again.

**Required conditions (ALL must be true):**
1. Origin move was ≥3× the height of the zone itself
2. Zone is fresh or tested ≤1 time and held
3. Zone aligns with HTF bias (at least 2 of 3: D1/H4/H1 agree with direction)
4. Current price is at or inside the zone (proximal ≤ price ≤ distal)

**Entry:** At proximal edge of zone, after M5 confirmation candle
**SL:** 3–5pts beyond distal edge (never inside the zone)
**TP1:** Entry ± 7.5pts
**TP2:** Next opposing Grade A/B zone

**M5 confirmation candles (any one is sufficient):**
- Bullish/bearish engulfing candle with body inside the zone
- Pin bar: wick penetrates distal, body closes back above/below proximal
- Failed breakout: close beyond distal then close back inside zone on same or next candle

**Invalidation:** Any M15 close beyond distal edge

---

## Setup 2 — VWAP Reclaim (趨勢延續)

**What it is:** Price breaks above or below VWAP (intraday institutional fair value), then pulls back and reclaims it with a confirming candle close. Signals resumption of intraday trend.

**Required conditions (ALL must be true):**
1. Price crossed VWAP and closed on the other side (not just a wick)
2. Price pulled back to retest VWAP
3. RSI is in the 38–62 range (not extended — if RSI >70 or <30, skip this setup)
4. MACD histogram supports the direction of the reclaim
5. HTF bias (H4 or H1) agrees with reclaim direction

**Entry:** On the confirming close back above/below VWAP
**SL:** 3pts beyond VWAP on M15 close (VWAP as a line, not a zone)
**TP1:** Entry ± 7.5pts
**TP2:** Next SNR level (order block edge, EMA, swing high/low)

**M5 confirmation candle:**
- Close that reclaims VWAP with ≥50% of candle body on the correct side

**Invalidation:** M15 close back through VWAP in the wrong direction

---

## Setup 3 — EMA Bounce (趨勢回調進場)

**What it is:** Price is in a clear directional trend (HTF EMAs ordered). It pulls back to touch EMA 20 or EMA 50 on M15, then resumes the trend. Classic trend-continuation entry.

**Required conditions (ALL must be true):**
1. Clear trend: H4 EMA20 > EMA50 (for longs) or EMA20 < EMA50 (for shorts)
2. Price has pulled back to touch M15 EMA20 or EMA50 without closing significantly through it
3. RSI has reset toward neutral: 38–55 (for longs), 45–62 (for shorts)
4. MACD is in the trend direction (histogram positive for longs, negative for shorts) OR making a bullish/bearish cross

**Entry:** On M5 rejection candle at the EMA level
**SL:** 3pts beyond the EMA (if price closes M15 through the EMA, setup is broken)
**TP1:** Entry ± 7.5pts
**TP2:** Next swing high/low or key level in trend direction

**M5 confirmation candle:**
- Pin bar with wick through EMA, body closes away from EMA
- Engulfing candle that closes away from EMA

**Invalidation:** M15 candle close through EMA50 (deeper pullback — stand aside)

---

## Setup 4 — Breakout Retest (動量進場)

**What it is:** A key level (previous resistance or support) is broken with a confirmed BOS (Break of Structure). Price then retests the broken level from the other side. The old resistance becomes new support (and vice versa).

**Required conditions (ALL must be true):**
1. A clear level (swing high/low, round number, order block edge) was previously respected ≥2 times
2. Price broke through the level with momentum (strong candle body, ideally with volume)
3. BOS confirmed: M15 structure now shows a higher high (bullish) or lower low (bearish)
4. Price has pulled back to retest the broken level (±3pts tolerance)
5. The retest hold: price touches the level but does NOT close through it (on M5 or M15)

**Entry:** On M5 rejection candle at the retested level
**SL:** 3–5pts beyond the retested level (back through into old territory)
**TP1:** Entry ± 7.5pts
**TP2:** Extension target — measured move or next key level

**M5 confirmation candle:**
- Engulfing candle rejecting from retested level
- Pin bar with wick touching level, body away from level

**Invalidation:** M15 close back through the retested level (breakout was false)

---

## Setup 5 — RSI Divergence (反轉信號 — Counter-Trend)

**What it is:** Price makes a new high or low, but RSI fails to confirm (makes a lower high for bearish divergence, or higher low for bullish divergence). Signals momentum exhaustion and potential reversal. **Always label as ⚠️ COUNTER-TREND — reduce position size.**

**Required conditions (ALL must be true):**
1. Clear divergence: price new H/L, RSI diverges (checked on M15 or H1)
2. Divergence occurs at a key S/R level (order block, round number, swing extreme, VWAP deviation)
3. The divergence spans ≥3 candles (not a one-candle fake)
4. Stochastic is also in overbought (>80) or oversold (<20) zone

**Entry:** On M5 confirmation candle after the divergence point
**SL:** 3pts beyond the extreme price point (the new high/low)
**TP1:** Entry ± 7.5pts
**TP2:** The most recent swing in the reversal direction

**M5 confirmation candle:**
- Bearish engulfing (for short divergence) OR bullish engulfing (for long divergence)
- Pin bar at the extreme

**Invalidation:** Any continuation candle making a new high/low beyond the divergence point
**Note:** If HTF bias opposes this setup, skip it unless RSI divergence is visible on H1 as well.

---

## Setup Priority Order

When multiple setups exist at the same time, prioritise in this order:

1. Zone Pullback (Grade A zone)
2. VWAP Reclaim
3. EMA Bounce
4. Breakout Retest
5. Zone Pullback (Grade B zone)
6. RSI Divergence (counter-trend — lowest confidence)

If two setups of equal priority exist in opposite directions, show both but flag as opposing setups — do not pick one.

---

## Universal Entry Rules (apply to all setup types)

- **Never enter on a wick alone** — wait for a candle body confirmation
- **Entry window:** Once conditions are met, valid for next 3 M5 candles only. After 3 candles, re-evaluate from scratch.
- **Low-liquidity blackout:** No entries between 00:00–02:00 GMT (Asian dead zone, thin order flow)
- **SL placement:** Always beyond the invalidation level — never inside a zone, never at a round number if the zone is beyond it
- **Minimum R:R:** 1:1 (7.5pt SL → 7.5pt TP1). If setup geometry forces SL >10pts for TP1, skip.
- **Counter-trend flag:** Any setup where HTF bias opposes the direction must be labeled ⚠️ COUNTER-TREND
