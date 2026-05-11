---
description: Scan TradingView for active supply/demand zones across one or more symbols
argument-hint: <SYMBOL> [SYMBOL2 SYMBOL3 ...]
---

Use the `chart-analyst` agent to scan for active supply and demand zones on: **$ARGUMENTS**

The chart-analyst should:
1. Connect to TradingView via MCP (`pane_list` → `pane_focus` → `pine_tables`)
2. Run the zone identification protocol (top-down, multi-timeframe)
3. Score every candidate zone using the confluence scoring system in `skills/zone-analysis.md`
4. Output all zones scoring ≥60 in structured `ZONE_SIGNAL` format
5. Pass ACTIVE zones to `signal-tracker` for entry timing monitoring

If multiple symbols are provided, scan each in sequence and rank by confluence score descending.

Final output: a ranked list of active zones with direction, score, and current status.
