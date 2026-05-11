---
description: Scan TradingView for active supply/demand zones across one or more symbols
argument-hint: <SYMBOL> [SYMBOL2 SYMBOL3 ...]
---

Use the `chart-analyst` agent to scan for active supply and demand zones on: **$ARGUMENTS**

The chart-analyst should:
1. Connect to TradingView via MCP and read all loaded indicators including Pine Script output
2. Run the zone identification protocol (top-down: H4 → H1 → M15)
3. Read Pine indicator drawings (CHoCH, BOS, order blocks, equilibrium) at each timeframe
4. Score every candidate zone using the scoring system in the chart-analyst definition
5. Output all zones scoring ≥50 (Grade B+)

After the chart-analyst completes, spawn the signal-tracker on the highest-priority zone to check if an entry signal should fire NOW.

If multiple symbols are provided, scan each in sequence and rank by confluence score descending.

## Final Output Format

After all agents complete, the orchestrator MUST present the final output in this exact structured format. Do not output raw ZONE_SIGNAL blocks — always use this memo format:

````markdown
═══════════════════════════════════════════════════════
  {SYMBOL}  技術掃描  |  {DATE}
═══════════════════════════════════════════════════════

## 掃描結果 (Scan Summary)
─────────────────────────────────────────────────────
  現價       : {PRICE}
  趨勢偏向   : {BULLISH / BEARISH / NEUTRAL}
  活躍區數量  : {N} 個
  最高評分區  : {ZONE_TYPE} {PROXIMAL}–{DISTAL} ({SCORE}/100 {GRADE})
  信號狀態   : {ENTRY_SIGNAL / WATCHING / NO_ACTIVE_ZONE}
─────────────────────────────────────────────────────

## 活躍區域 (Active Zones)
─────────────────────────────────────────────────────
  #  方向     類型     區域範圍              評分   狀態
  ─  ────     ────     ────────              ────   ────
  1  {LONG}   {DEMAND} {PROXIMAL}–{DISTAL}   {XX}   {APPROACHING}
  2  {SHORT}  {SUPPLY} {PROXIMAL}–{DISTAL}   {XX}   {FRESH}
  ...

  [For each zone, one-line note:]
  Zone 1: {origin description + key confluence factors}
  Zone 2: {origin description + key confluence factors}
─────────────────────────────────────────────────────

## SMC 結構 (Smart Money Context)
─────────────────────────────────────────────────────
  [Only if Pine indicators (LuxAlgo, ICT, etc.) are loaded on chart]
  CHoCH      : {location + direction}
  BOS        : {location + direction}
  均衡區      : {Equilibrium level}
  折價/溢價   : 現價在 {DISCOUNT / PREMIUM / EQUILIBRIUM} 區域
  訂單塊      : {order blocks that overlap with detected zones}
─────────────────────────────────────────────────────

## 進場信號 (Entry Signal)
─────────────────────────────────────────────────────
[IF ENTRY_SIGNAL:]
  🟢 進場信號觸發
  方向       : {LONG / SHORT}
  入場價     : {ENTRY_PRICE}
  區域       : {PROXIMAL}–{DISTAL}
  確認因素   : {confirmation factors from signal-tracker}
  信心度     : {XX}%
  🔴 止損    : {SL}  ({-X.X} pts / {-X.X}%)
  🥇 止利 1  : {TP1}  ({+X.X} pts / {+X.X}%)
  🥈 止利 2  : {TP2}  ({+X.X} pts / {+X.X}%)
  R:R        : {X.X}:1
  有效時間   : {validity window}

[IF WATCHING:]
  ⏳ 觀望中
  主要監控區  : {ZONE_TYPE} {PROXIMAL}–{DISTAL} (評分 {XX})
  距離       : {X} pts {above/below} proximal
  等待觸發   : {what signal-tracker is waiting for}
  失效條件   : {invalidation level}

[IF NO_ACTIVE_ZONE:]
  ⚪ 無活躍區域 — 暫不操作
─────────────────────────────────────────────────────

## 指標概覽 (Indicator Summary)
─────────────────────────────────────────────────────
  SMA 20     : {value}  價格{在上方/在下方}
  SMA 80     : {value}  價格{在上方/在下方}
  SMA 150    : {value}  價格{在上方/在下方}
  MACD       : {value}  {bullish/bearish crossover / neutral}
  RSI        : {value}  {overbought / neutral / oversold}
  成交量     : {above/below avg}  {trend}
─────────────────────────────────────────────────────

## Agent 審計 (Agent Audit)
─────────────────────────────────────────────────────
  Agent            關鍵發現                              狀態
  ──────           ────────                              ────
  chart-analyst    {one-line key finding}                 {N zones found}
  signal-tracker   {one-line assessment}                  {ENTRY/WATCHING/INVALID}
─────────────────────────────────────────────────────

## 最終建議
═══════════════════════════════════════════════════════
  {LONG / SHORT / WAIT} — {one crisp sentence in Chinese}
═══════════════════════════════════════════════════════
````
