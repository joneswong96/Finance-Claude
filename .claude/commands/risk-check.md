---
description: Pre-trade risk review for a proposed position
argument-hint: <ticker> <size> [side]
---

Use the `risk-manager` agent to perform a pre-trade risk check on the proposed trade: **$ARGUMENTS**

The risk-manager must report:
1. **Incremental VaR** — change in portfolio 1-day 95% VaR if executed
2. **Limit checks** — position limit, sector concentration, leverage, liquidity
3. **Liquidity assessment** — position size vs. ADV, expected exit time
4. **Stress test** — P&L impact under historical scenarios (2008, 2020 COVID, 2022 rate shock)
5. **Verdict** — APPROVE / APPROVE-WITH-CONDITIONS / REJECT, with reasoning

If APPROVE, hand off to `portfolio-manager` for execution. If REJECT, explain what would need to change.
