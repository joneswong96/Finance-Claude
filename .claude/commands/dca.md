---
description: ETF 定投 advisor — computes this month's buy amounts, alert levels, and optional performance reports
argument-hint: [check <TICKER> | setup | log <TICKER> <SHARES> <PRICE> | report]
---

Use the `dca-manager` agent.

## Subcommands

| Invocation | What It Does |
|-----------|-------------|
| `/dca` | Full DCA brief: all ETFs, this month's buy amounts, alert price levels to set |
| `/dca check CSPX` | Spot check one ETF: current multiplier and recommended buy amount |
| `/dca setup` | First-time: configure ETF list, base monthly amounts, target allocations |
| `/dca log CSPX 2.5 518.40` | Record a purchase (shares, price) for performance tracking |
| `/dca report` | Performance review: CAGR, P&L by ETF, DCA vs lump-sum comparison |

## Instructions for dca-manager

Parse the arguments:

- **No arguments** → run full DCA brief
- **`check {TICKER}`** → spot check that ETF
- **`setup`** → run first-time configuration flow
- **`log {TICKER} {SHARES} {PRICE}`** → record purchase
- **`report`** → generate performance report

Arguments: **$ARGUMENTS**

Run the appropriate operation from your instructions. Output in 繁體中文.

After the full DCA brief (`/dca` or `/dca setup`), save to `analysis_history` SQLite table as specified in your instructions.
