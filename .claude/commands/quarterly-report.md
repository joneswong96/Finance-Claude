---
description: Generate the quarterly investor report
argument-hint: [quarter] [year]
---

Use the `orchestrator` agent to produce the quarterly investor report for **$ARGUMENTS** (default: most recent completed quarter).

Workflow:
1. `data-engineer` — pull portfolio holdings, prices, benchmark data for the quarter
2. `portfolio-manager` (parallel) — performance attribution: by asset, sector, factor
3. `risk-manager` (parallel) — risk review: realized vol, max drawdown, VaR utilization
4. `report-writer` — compose the report with executive summary, performance section, market commentary, outlook
5. `compliance-officer` — final review: disclosures, benchmark comparison, forward-looking-statement labels

Output: a polished Markdown report ready for client distribution.
