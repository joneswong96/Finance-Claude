---
description: Watch a specific zone for entry timing and fire a signal when confirmation is met
argument-hint: <SYMBOL> <direction> <proximal> <distal>
---

Use the `signal-tracker` agent to monitor the following zone for entry timing: **$ARGUMENTS**

Format expected: `SYMBOL DIRECTION PROXIMAL DISTAL`
Example: `XAUUSD LONG 2048.5 2041.0`

The signal-tracker should:
1. Confirm the zone is still valid (price has not breached distal edge)
2. Check current price relative to the zone (APPROACHING / INSIDE)
3. Query `data-engineer` for any historical signal data on this zone or nearby levels
4. Begin monitoring for confirmation patterns (phase depends on current price position)
5. Fire an `ENTRY_SIGNAL` block when confirmation threshold is met
6. Immediately pass the signal to `risk-manager` for SL placement and position sizing

The signal-tracker must report status even if no entry is triggered:
`WATCHING | INSIDE_NO_CONFIRM | ZONE_INVALIDATED`
