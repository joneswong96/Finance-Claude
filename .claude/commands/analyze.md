---
description: Full investment analysis on a ticker (orchestrates the full team)
argument-hint: <TICKER> [horizon]
---

Spawn the `orchestrator` agent to run a full investment analysis on **$ARGUMENTS**.

The orchestrator will manage the entire workflow autonomously:
1. Create a shared workspace at `workspace/{TICKER}_{DATE}/`
2. Spawn `data-engineer` to gather and write all data to the workspace
3. Spawn `research-analyst` and `quant-analyst` **in parallel** — each reads the data file directly
4. Run a **cross-debate round** — each analyst reads the other's output and writes a rebuttal
5. Orchestrator writes a synthesis resolving all disagreements
6. Spawn `risk-manager` — reads the synthesis directly from the workspace
7. Spawn `portfolio-manager` — reads risk assessment directly from the workspace
8. Spawn `report-writer` — reads all workspace files and produces the final memo

The orchestrator returns the final memo plus a list of any unresolved team disagreements.
