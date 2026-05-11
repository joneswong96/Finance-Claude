---
description: 15m/5m day trade scan — collects HTF→LTF data, identifies all high-probability entries, draws levels on TradingView
argument-hint: <SYMBOL> [SYMBOL2 SYMBOL3 ...]
---

Use the `day-trade-analyst` agent to run a full day-trade scan on: **$ARGUMENTS**

The day-trade-analyst runs a strict two-phase workflow:

1. **Data collection first** — HTF to LTF in sequence: D1 → H4 → H1 → M15 → M5. All data gathered before any analysis begins.
2. **Single analysis pass** — after all data is collected, one comprehensive pass identifies every high-probability entry setup (LONG and SHORT), scores each, keeps Grade A and B only.
3. **Draw everything on TradingView** — zones, entry lines, SL lines, TP lines, and key HTF levels. Chart is left on M15 for the user to monitor.
4. **Output a tight brief** — Grade A entries only in text (≤400 tokens). The chart is the primary deliverable.

If multiple symbols are provided, scan each in sequence, drawing and outputting for each before moving to the next.

## Final Output Format — ALL in 繁體中文

After the day-trade-analyst completes, present output in this exact format:

````markdown
{SYMBOL}  {DATE}  |  偏向: {看漲/看跌/混合}  |  現價: {PRICE}
作廢線: {INVALIDATION_PRICE}  [{若M15收盤跌穿/升穿即全部進場失效}]

━━ A級進場 ━━

#1 {做多▲ / 做空▼}  進場: {ENTRY_PRICE}  [{設置類型}]
   止損   {SL_PRICE}  ({N.N} pts)
   目標   {TP1_PRICE} / {TP2_PRICE}  (+7.5 / +{N} pts)
   觸發   {一句具體M5確認信號}
   底氣   {≤15字：關鍵匯合點}

#2 {做多▲ / 做空▼}  進場: {ENTRY_PRICE}  [如有]
   ...

圖表已標記所有進場、止損、目標及關鍵水平。
````

If no Grade A entries exist: output `暫無高確信進場機會 — 觀望`

The `/watch` command remains available to activate the signal-tracker on any specific entry level for real-time confirmation monitoring.
