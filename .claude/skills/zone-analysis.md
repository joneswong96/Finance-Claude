# Zone Analysis Skill — Autonomous Framework

This skill defines how Claude agents identify, score, and act on supply/demand zones.
It is designed for autonomous agent execution, not human advisory.

---

## What Is a Zone

A zone is a **price area** (not a line) where institutional order flow previously caused a significant directional move.
Zones have width. A zone with no width is a level — treat it as low quality.

**Two zone types:**
- **Demand zone** — area where price previously reversed upward sharply; expect buyers to defend on return
- **Supply zone** — area where price previously reversed downward sharply; expect sellers to defend on return

---

## Zone Identification Protocol

### Step 1 — Locate the Origin Candle
Find the candle (or candle cluster) that launched the significant move. The zone is defined by that candle's body range.

- Use the **body** (open-close), not the full wick
- If multiple candles cluster before the move, merge their bodies into one zone
- Minimum move required to validate: 3× the zone's own height

### Step 2 — Classify Zone Quality

Score each zone on three dimensions:

**Freshness (0–40 pts)**
- Never tested since formation: 40
- Tested once, held: 25
- Tested twice, held: 10
- Tested 3+ times or breached: 0 (discard zone)

**Origin Strength (0–35 pts)**
- Price left the zone with a gap or explosive candle (≥2× average candle size): 35
- Strong directional move (1.5–2× average): 20
- Gradual move: 5

**Confluence (0–25 pts)**
- Zone aligns across 2+ timeframes: +15
- High volume at zone origin (above 20-period average): +10

**Total Zone Score = Freshness + Origin Strength + Confluence**

| Score | Grade | Action |
|-------|-------|--------|
| 75–100 | A | Primary watch — full position sizing |
| 50–74  | B | Secondary watch — reduced size |
| 25–49  | C | Monitor only — no entry |
| 0–24   | D | Discard |

---

## Timeframe Hierarchy

Always identify zones top-down:

1. **H4** — defines the dominant directional bias (long or short)
2. **H1** — narrows zone clusters; confirms H4 bias
3. **M15** — pinpoints the entry zone boundary
4. **M5** — used for entry timing confirmation only (never for zone identification)

A zone that appears on H4 AND H1 AND M15 gets maximum confluence score.
A zone that appears only on M5 is invalid for entry — too low quality.

---

## Entry Timing Rules

Zone identification is **not** entry. Entry requires a confirmation event inside or at the edge of the zone.

**Valid confirmation events (any one is sufficient):**
1. Bullish/bearish engulfing candle on M5 with body close inside zone
2. Failed breakout — price wicks through zone, closes back inside
3. Momentum flip — M5 structure shift (lower high → higher high for demand, or inverse)

**Invalid confirmations (do not enter on these):**
- Price merely touching zone boundary
- Single-wick test with no body inside zone
- Confirmation candle forming during low-liquidity period (00:00–02:00 GMT)

**Entry window:**
Once confirmation is detected, entry is valid for the next 3 M5 candles only.
After 3 candles, re-evaluate — the zone may still be valid but timing resets.

---

## Stop Loss Placement

Place SL **beyond the zone**, not at the zone edge:

- Demand zone SL: 3–5 pts below the lowest wick of the zone origin
- Supply zone SL: 3–5 pts above the highest wick of the zone origin

Never place SL inside the zone — it will be hunted.

---

## Take Profit Logic

TP = next opposing zone of Grade B or higher.
If no opposing zone exists within 3× the SL distance, the trade does not meet minimum R:R — do not enter.

Minimum acceptable R:R: 1.5 : 1
Target R:R: 2.5 : 1 or better

---

## Historical Signal Scoring

After each signal, log the outcome:
- Zone grade at entry
- Actual R:R achieved
- Whether confirmation type was correct
- Session (London / New York / Asian)

The quant-analyst uses this log to calculate hit rates by zone grade, session, and confluence level.
These hit rates feed back into zone scoring weights over time.

---

## Output Format (for inter-agent communication)

When chart-analyst identifies a zone, output this structure:

```
ZONE_ID: [symbol]-[timeframe]-[date]-[price_mid]
SYMBOL: XAUUSD
DIRECTION: LONG
ZONE: 2045.0 – 2052.5
GRADE: A (score: 82/100)
  - Freshness: 40 (never tested)
  - Origin strength: 32 (explosive departure)
  - Confluence: 10 (M15 only)
CURRENT_PRICE: 2098.4
DISTANCE_TO_ZONE: 45.9 pts
STATUS: MONITORING
INVALIDATION_PRICE: 2039.5
NEXT_REVIEW: when price < 2075 (within 30pts of zone)
```

When signal-tracker detects entry timing:

```
ENTRY_SIGNAL
ZONE_ID: XAUUSD-M15-20260510-2048
TRIGGER: Bullish engulfing M5 close at 2047.8
ENTRY: 2048.2
SL: 2040.0   (8.2 pts risk)
TP: 2068.7   (20.5 pts reward — next supply zone)
R:R: 2.5:1
CONFIDENCE: 82%
VALID_UNTIL: 3 M5 candles (15 min window)
PASS_TO: risk-manager
```
