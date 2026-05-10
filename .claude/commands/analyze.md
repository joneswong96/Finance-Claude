---
description: Full investment analysis on a ticker (orchestrates the full team)
argument-hint: <TICKER> [horizon]
---

Use the `orchestrator` agent to run a full investment analysis on **$ARGUMENTS**.

The orchestrator should:
1. Send `data-engineer` to gather price history, fundamentals, and recent filings
2. Run `research-analyst` (qualitative thesis) and `quant-analyst` (factor exposures, statistical signals) in parallel
3. Have `risk-manager` evaluate position sizing and risk impact
4. Get a final recommendation from `portfolio-manager`
5. Have `report-writer` produce a clean investment memo

Final output: a one-page memo with thesis, key metrics, risks, and a clear buy/hold/sell recommendation.
