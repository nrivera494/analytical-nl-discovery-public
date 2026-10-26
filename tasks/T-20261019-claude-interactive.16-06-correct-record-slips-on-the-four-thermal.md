---
id: T-20261019-claude-interactive.16-06
title: "Correct record slips on the four thermalization claim cards: auditor fields naming gpt-b although no audit was done, and the 'largest error 0.218 dB' wording on C-20261018-claude-interactive.7-03"
type: loose-end
status: open
priority: 3
problem: P-20261016-claude-interactive.7-01
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive.16
created: 2026-10-19
---

## Goal

Found while writing R-0007 to R-0010. Fix the card and audit-note values against the run files, and set the auditor fields to reflect that gpt-b's reports are verifications. Do not change any Statement or status.

## Context

Found while writing R-0007 to R-0010 (log/2026-10-19_claude-interactive.16_T-20261019-claude-interactive-09.md) and corrected by the number check of claude-interactive.16.1.

**Slips:**
1. **Auditor fields, all four cards** (C-20261016-claude-interactive.7-01, C-20261018-claude-interactive.7-01, -02, -03). The front matter has audited_by: gpt-b, auditor_family: gpt and auditor_model: gpt-6-astra. gpt-b's reports are verifications, not clean-context audits, and the claims were never audited, as each card's Outcome says. Remove the auditor fields, or set them when T-20261019-claude-interactive.16-01 completes. The manuscript README, item 8, noted this for the first card only.
2. **C-20261018-claude-interactive.7-03: "largest error 0.218 dB".** The Checks row ("largest error0.218 dB") and gpt-b's audit note ("the largest error is 0.218 dB") call 0.218 dB the largest error of the nine held-out cases. The run maximum is 0.21732 dB (runs/2026-10-18-gpt-b-kerr-exact/summary.json, original_displaced_thermal_prediction.max_abs_error_dB), which rounds to 0.217.

**Not slips** (listed so nobody "fixes" them):
- "within 0.218 dB" in the sharpened statement and the PI summary is a valid bound.
- "within 0.176 dB" for the extracted condensates is a valid bound on the maximum 0.17549 dB.
- "below 1.3e-7 dB" on C-20261018-claude-interactive.7-01 is a valid bound on 1.216e-7 dB.
- The audit's f0 = 0.415 is the correct rounding of 0.4148.

The manuscript README (item 7) lists the last three as slips; that is for the manuscript refresh, T-20261018-claude-interactive.11-05. The original Statements carry superseded proposer-family values next to gpt-b's; that is by rule, and they must stay.

## Deliverables

- Card and note fields corrected, with an audit-trail row on each card.
- No Statement or status changed.
