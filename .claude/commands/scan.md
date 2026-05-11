---
description: Scan TradingView for active supply/demand zones across one or more symbols
argument-hint: <SYMBOL> [SYMBOL2 SYMBOL3 ...]
---

Use the `chart-analyst` agent to scan for active supply and demand zones on: **$ARGUMENTS**

The chart-analyst produces TWO layers:
1. **宏觀區域** — H4→H1 macro zones for directional bias
2. **即時 SNR** — M15→M5 support/resistance within ±30pts of current price for 7.5pt scalp entries

The chart-analyst should:
1. Connect to TradingView via MCP and read all loaded indicators including Pine Script output
2. Run the zone identification protocol (top-down: H4 → H1 → M15 → M5)
3. Read Pine indicator drawings (CHoCH, BOS, order blocks, equilibrium) at each timeframe
4. Score macro zones using the scoring system
5. Identify all SNR levels within ±30pts of current price on M5/M15
6. Generate up to 2 trade setups aligned with macro bias (1:1 R:R, 7.5pts SL/TP)

After the chart-analyst completes, spawn the signal-tracker on the highest-priority trade setup to check if entry conditions are met NOW.

If multiple symbols are provided, scan each in sequence.

## Final Output Format — ALL in 繁體中文

After all agents complete, the orchestrator MUST present the final output in this exact format:

````markdown
═══════════════════════════════════════════════════════
  {SYMBOL}  技術掃描  |  {DATE}
═══════════════════════════════════════════════════════

## 掃描結果 (Scan Summary)
─────────────────────────────────────────────────────
  現價       : {PRICE}
  趨勢偏向   : {看漲 / 看跌 / 中性}
  宏觀區數量  : {N} 個
  即時 SNR    : {N} 個（±30pts 範圍內）
  信號狀態   : {可進場 / 觀望中 / 無信號}
─────────────────────────────────────────────────────

## 宏觀區域 (Macro Zones — 方向偏向)
─────────────────────────────────────────────────────
  #  方向    類型     區域範圍         評分    狀態
  ─  ────    ────     ────────         ────    ────
  1  {做空}  {供應}   {PROX}–{DIST}    {XX/A}  {接近中}
  2  {做多}  {需求}   {PROX}–{DIST}    {XX/B}  {未測試}
  ...

  [每個區域一行說明]
  Zone 1: {起源描述 + 匯合因素}
  Zone 2: {起源描述 + 匯合因素}
─────────────────────────────────────────────────────

## SMC 結構 (Smart Money Context)
─────────────────────────────────────────────────────
  [僅當圖表載入 Pine 指標時顯示]
  CHoCH      : {位置 + 方向}
  BOS        : {位置 + 方向}
  均衡區      : {價位}
  折價/溢價   : 現價在 {折價 / 溢價 / 均衡} 區域
  訂單塊      : {與區域重疊的訂單塊}
─────────────────────────────────────────────────────

## 即時 SNR 階梯 (Immediate SNR Ladder)
─────────────────────────────────────────────────────
  現價: {PRICE}

  阻力 (上方):
    R1: {PRICE}  [{來源: SMA/swing high/order block/...}]  強度: {強/中/弱}
    R2: {PRICE}  [{來源}]                                   強度: {強/中/弱}
    ...

  支撐 (下方):
    S1: {PRICE}  [{來源}]                                   強度: {強/中/弱}
    S2: {PRICE}  [{來源}]                                   強度: {強/中/弱}
    ...
─────────────────────────────────────────────────────

## 交易計劃 (Trade Setups — 1:1 R:R, 7.5pts)
─────────────────────────────────────────────────────
[最多 2 個，必須與宏觀偏向一致]

  Setup 1:
  方向       : {做多 / 做空}
  SNR 級別   : {PRICE} ({來源描述})
  入場       : {PRICE}
  🔴 止損    : {PRICE} ({±7.5} pts)
  🥇 止利    : {PRICE} ({±7.5} pts)
  R:R        : 1:1
  信心度     : {高 / 中 / 低}
  原因       : {為什麼這個 SNR + 宏觀偏向支持此交易}
  條件       : {入場前需要什麼 M5 確認}

  Setup 2: [如有]
  ...

[如無符合條件的 Setup:]
  ⚪ 暫無交易機會 — {原因}
─────────────────────────────────────────────────────

## 指標概覽 (Indicator Summary)
─────────────────────────────────────────────────────
  SMA 20     : {value}  價格{在上方/在下方}
  SMA 80     : {value}  價格{在上方/在下方}
  SMA 150    : {value}  價格{在上方/在下方}
  MACD       : {value}  {看漲交叉 / 看跌交叉 / 中性}
  RSI        : {value}  {超買 / 中性 / 超賣}
  成交量     : {高於/低於均值}  {趨勢}
─────────────────────────────────────────────────────

## Agent 審計 (Agent Audit)
─────────────────────────────────────────────────────
  Agent            關鍵發現                          狀態
  ──────           ────────                          ────
  chart-analyst    {一行關鍵發現}                     {N區 + N個SNR}
  signal-tracker   {一行評估}                         {可進場/觀望/失效}
─────────────────────────────────────────────────────

## 最終建議
═══════════════════════════════════════════════════════
  {做多 / 做空 / 觀望} — {一句話繁體中文建議}
═══════════════════════════════════════════════════════
````
