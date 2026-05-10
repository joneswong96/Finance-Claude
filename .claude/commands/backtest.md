---
description: Run a quantitative backtest on a strategy
argument-hint: <strategy description>
---

Use the `quant-analyst` agent to backtest the following strategy: **$ARGUMENTS**

Required outputs:
1. **Strategy specification** — universe, signal, rebalancing frequency, position sizing
2. **Backtest results** with realistic transaction costs:
   - CAGR, Sharpe ratio, Sortino, max drawdown, Calmar ratio
   - Year-by-year return table
   - Equity curve vs. benchmark
3. **Robustness checks** — in-sample vs. out-of-sample, parameter sensitivity, regime analysis
4. **Risk review** — pass results to `risk-manager` for capacity and tail-risk assessment

Flag any look-ahead bias, survivorship bias, or unrealistic assumptions explicitly.
