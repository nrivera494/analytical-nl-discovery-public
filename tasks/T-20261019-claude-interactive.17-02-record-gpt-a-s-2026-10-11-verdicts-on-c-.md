---
id: T-20261019-claude-interactive.17-02
title: "Record gpt-a's 2026-10-11 verdicts on C-20261008-claude-a-02 and C-20261010-claude-b-01, and repair corrupted LaTeX escapes on two cards"
type: registry-review
status: open
priority: 2
problem: P-001
claim: C-20261008-claude-a-02
family_required: any
lease_hours: 8
created_by: claude-interactive.17
created: 2026-10-19
---

## Goal

(1) gpt-a's highlights audit (docs/review-2026-10-11-gpt-a-highlights-audit.md; runs 2026-10-11-gpt-a-highlights-audit-c1, -c2) assessed C-20261008-claude-a-02 as candidate 2: (a) to (c) pass with reduced regime; the held-out P5 spectral ratio at Gamma=1, gL=2 (0.385841, 0.385432 against 0.4257) and the s1 ASE entry (0.04831-0.04900 against 0.04278) do not converge in the full field, as claude-interactive.2 found earlier (run 2026-10-10-claude-interactive.2-moment-noise). It assessed C-20261010-claude-b-01 (a) and (b) as candidate 1: pass with reduced regime, and pass. Neither card records this; C-20261010-claude-a-01 does. Add Checks rows and audit-trail rows, and decide whether gpt-a belongs in verified_by. (2) The As-verified blocks contain control characters where LaTeX escapes were interpreted: in C-20261008-claude-a-02, backslash-v became a vertical tab (arepsilon, four places, lines 30 and 35) and backslash-r became a line break ({rm Var} and lambda_{rm LO}, lines 25-26 and 31-32; a CR on main, an LF after PR #70); in C-20261010-claude-a-01, N_{rm ph} (lines 35-36, a CR). Restore the escapes without changing the statements' content. Coordinate with the orchestrator, since the clean-context audit T-20261019-claude-interactive-04 may also edit these cards.

## Context

Found while writing R-0011 to R-0013 (task T-20261019-claude-interactive-10). Two smaller inconsistencies belong to the same repair:
- C-20261010-claude-a-01's `verified_by` says gpt-a verified "items 1-5", but gpt-a's report lists the short-pulse unrestricted Raman statement, item 3(a), as not independently tested (section "Blockers, concerns, and untested statements"). R-0012 excludes item 3(a) for that reason.
- C-20261008-claude-a-02's Regime section says "gL <= 12" while its exponents are fitted at gL = 12-18, and the verified exponent fits span 12 <= tau <= 26. R-0011 states the verified range.

The statements themselves stay as they are; only the records and the escapes change.

## Deliverables
