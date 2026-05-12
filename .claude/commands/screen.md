---
description: Weekly lead stock screen — finds top 5 swing trade candidates from leading sectors
argument-hint: (no arguments needed)
---

Use the `orchestrator` agent to run a weekly lead stock screen.

## Mission

`SCREEN` — Find the best swing trade candidates right now. Answer: "What should I trade this week?"

## Orchestrator Instructions

Classify as `SCREEN` mission. Follow the SCREEN execution flow in your instructions.

Workspace: `workspace/SCREEN_{YYYYMMDD}/`

## Screening Criteria (pass to data-engineer)

**Universe filters** (eliminate first):
- Market cap > $5B
- Average daily volume > 1M shares
- Price > $20
- Listed on NYSE or NASDAQ

**Composite scoring formula:**
```
Score = (RS_score × 0.4) + (EPS_rank × 0.3) + (base_quality × 0.2) + (sector_rank × 0.1)
```

Where:
- `RS_score` (0–100): 12-month price performance vs all universe stocks, 85+ = outperforming 85% of stocks
- `EPS_rank` (0–100): EPS growth YoY vs peers; >20% growth = rank 80+
- `base_quality` (0–100): weeks in base (5+wks = 60, 8+wks = 80, 12+wks = 100), tight weekly closes
- `sector_rank` (0–100): sector's 4-week relative performance vs SPY rank among 11 GICS sectors (rank 1 = 100, rank 11 = 0)

**Macro tape gate:**
Before screening, check: Is the Nasdaq in a confirmed uptrend (Follow-Through Day after a low)?
- Confirmed uptrend → proceed with screen
- Distribution / correction → note "CAUTION: tape is not in confirmed uptrend — higher-risk entries"
- Bear market → note "NOT RECOMMENDED: bear market tape — consider only very strong A-grade setups"

## Output Format — ALL in 繁體中文

```markdown
LEAD STOCK SCREEN  |  {DATE}
大盤狀態: {確認上升趨勢 ✅ / 調整中 ⚠️ / 熊市 ❌}

板塊排名 (4週相對強度 vs SPY):
  #1 {Sector}  (+{N}%)  ← 優先做多此板塊
  #2 {Sector}  (+{N}%)
  #3 {Sector}  (+{N}%)
  ── 以下板塊相對偏弱，本週降低優先級 ──
  #4 {Sector}  ({N}%)
  ...

━━ Top 5 候選股 ━━

#1 {TICKER}  [{板塊}]  評分: {N}/100
   RS評分:   {N}/100  (過去12個月跑贏{N}%的股票)
   基本面:   EPS +{N}% YoY | 收入 +{N}% YoY | ROE {N}%
   整固:     底部第{N}週 | {VCP/平底杯/旗形} 形態
   催化劑:   財報 {DATE} ({N}天後) {✅ >14天安全 / ⚠️ 5-14天 / ❌ <5天}
   板塊動力: {板塊ETF} 20日 {+/-N}% vs SPY
   → 下一步: /swing {TICKER}

#2 {TICKER}  [{板塊}]  評分: {N}/100
   ...

#3 {TICKER}  ...
#4 {TICKER}  ...
#5 {TICKER}  ...

━━ 本週不適宜的板塊 ━━
{Underperforming sectors and reason}

━━ 提示 ━━
運行 /swing {TICKER} 獲取特定股票的詳細進場分析
```

## Save to Dashboard

After producing the screen output, save to `analysis_history` SQLite table:

```sql
INSERT OR REPLACE INTO analysis_history
  (run_id, command, ticker, direction, status, grade, summary_md, raw_json, created_at, updated_at)
VALUES (
  'screen_{YYYYMMDD}',
  'screen',
  'MULTI',
  null,
  'ACTIVE',
  null,
  '{full markdown output above}',
  '{json: {top_tickers: [...], sectors: [...], tape: "..."}}',
  datetime('now'),
  datetime('now')
);
```

Use `sqlite` MCP tool to execute this INSERT after the screen output is assembled.
