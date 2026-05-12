---
description: Stock swing trade analysis — specific entry/SL/TP/alert levels for a single ticker
argument-hint: <TICKER>
---

Use the `orchestrator` agent to run a swing trade analysis on: **$ARGUMENTS**

## Mission

`SWING` — Generate a complete swing trade setup for the specified ticker. Answer: "How do I trade this stock right now?"

## Orchestrator Instructions

Classify as `SWING` mission. Follow the SWING execution flow in your instructions.

Workspace: `workspace/{TICKER}_SWING_{YYYYMMDD}/`

Active agents: chart-analyst (SWING MODE), data-engineer (catalyst only), risk-manager (SWING mode), portfolio-manager (SWING execution).

Sleeping: signal-tracker (user sets alerts manually), research-analyst, quant-analyst, report-writer, compliance-officer, dca-manager.

## Execution Flow

1. **Spawn in parallel (background):**
   - `chart-analyst` with `mission=SWING`: runs W1→D1→H4→H1 on `$ARGUMENTS`, outputs `SWING_ZONE_SIGNAL`
   - `data-engineer` (catalyst only, ≤2 turns): fetches earnings date + days remaining, sector ETF 20-day trend vs SPY, outputs `SWING_CATALYST`

2. **After both complete → risk-manager (SWING mode):** reads both blocks, checks R:R ≥2:1 / earnings gate / ADV gate, outputs `SWING_RISK_ASSESSMENT`

3. **After risk-manager → portfolio-manager (SWING execution):** reads `SWING_RISK_ASSESSMENT`, determines batch split, outputs `SWING_EXECUTION_DECISION`

4. **Assemble final output** (orchestrator formats for user — see format below)

5. **Save to dashboard** (see below)

## Final Output Format — ALL in 繁體中文

```markdown
SWING SETUP: {TICKER}  {DATE}  |  偏向: {看漲/看跌}  |  現價: {PRICE}
設置類型: {趨勢回調 / 突破延續 / RSI背離}  |  W1趨勢: {看漲/看跌/橫盤}

━━ 技術結構 ━━
  W1 偏向:   {描述 — EMA位置，高低點結構}
  D1 區域:   {需求/供應}區 {DISTAL}–{PROXIMAL} (評分: {N}/100, {A/B}級)
  H4 觸發:   {CHoCH/BOS信號} @ {PRICE}  |  MACD: {看漲/看跌}
  H1 進場:   {確認蠟燭類型} @ {H1_ENTRY_PRICE}

━━ 催化劑 ━━
  財報日期:  {DATE} ({N}天後  {✅ >14天 / ⚠️ 5-14天 / ❌ <5天})
  板塊動力:  {SECTOR_ETF} 20日 {+/-N}%  vs SPY {+/-N}%  ({同向 ✅ / 背離 ⚠️})

━━ 交易計劃 ━━
  {分2批 / 單次進場} ({第1批N% / 第2批N%})
    第1批:  {PRICE} — {H1觸發確認後}
    第2批:  {PRICE} — {如適用：回測或區域中軸}
  止損:     {PRICE} (-{N}%)  [結構性止損: D1遠端下方{N}%]
  止利段1:  {PRICE} (+{N}%) → 平倉60%，止損移至保本
  止利段2:  {PRICE} (+{N}%) → 追蹤剩餘40%
  R:R:      1:{X.X}
  建議倉位: {N}% of portfolio
  最長持倉: 4週 (到期: {DATE})

🔔 設置提醒  (手動在IBKR / Futu設置價格提醒)
  進場提醒:  {TICKER} @ {H1_ENTRY_PRICE}  (等H1確認蠟燭收盤)
  止損提醒:  {TICKER} @ {SL_PRICE}        (跌穿即出場)
  止利提醒:  {TICKER} @ {TP1_PRICE}       (第1目標，平倉60%)
  作廢提醒:  {TICKER} @ {INVALIDATION}    (D1收盤跌破 → 分析失效)
```

If risk-manager returns NO-GO:
```markdown
SWING NO-GO: {TICKER}  {DATE}
原因: {specific reason from SWING_RISK_ASSESSMENT}

{If earnings gate}: 財報在{N}天後 — 等財報公佈後重新分析
{If R:R < 2:1}: R:R {actual_rr} < 2:1最低要求 — 區域太近，無法進入
{If ADV}: 日均成交量 {ADV}M < 1M門檻 — 流動性不足
```

## Save to Dashboard

After producing the output (GO or NO-GO), save to `analysis_history` SQLite table using the `sqlite` MCP tool:

```sql
INSERT OR REPLACE INTO analysis_history
  (run_id, command, ticker, direction, status, grade, entry_price, sl_price, tp1_price, rr_ratio, summary_md, raw_json, created_at, updated_at)
VALUES (
  'swing_{TICKER}_{YYYYMMDD_HHMMSS}',
  'swing',
  '{TICKER}',
  '{LONG or SHORT}',
  '{ACTIVE if GO, EXPIRED if NO-GO}',
  '{zone_grade from SWING_ZONE_SIGNAL}',
  {h1_entry_price or null},
  {sl_price or null},
  {tp1_price or null},
  {rr_ratio or null},
  '{full markdown output above}',
  '{json with all key fields}',
  datetime('now'),
  datetime('now')
);
```
