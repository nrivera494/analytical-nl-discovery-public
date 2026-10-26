---
id: T-20261019-claude-interactive.20-02
title: "Record hygiene for the amplifier-similariton results: stale R-0011 pointer to R-0014, R-0014 brightness example and low-gain ratio range, raw-only values in R-0011, stale P-001 narrative, superseded verify task T-20261008-claude-a-03"
type: loose-end
status: done
priority: 3
problem: P-001
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive.20
created: 2026-10-19
---

## Goal

Propose, for the PI's approval, corrections to six stale or inconsistent statements found while writing docs/manuscripts/2026-10-19-amplifier-noise-bounds (README, Discrepancies items 1-4, 7, 8). No verdict changes.

## Context

Found by claude-interactive.20 while writing the manuscript (README, "Discrepancies" items 1-4, 7, 8):
1. `results/promising/R-0011-*/RESULT.md` (header bullet and section 9) still says that C-20261019-pi-chatgpt-02 is "still under Claude-family verification" (T-20261019-claude-interactive-03). It was verified by claude-interactive.13 and is now R-0014.
2. `results/promising/R-0014-*/RESULT.md`, regime table, row $\Phi_{NL}^2/N_0$: the values $3\times10^{-6}$, 0.17, $2\times10^7$ at $\tau=4$, 12, 26 "for a 500 pJ seed" divide $\Phi_{NL}^2$ at $\varepsilon_0=0.05$, $\Gamma=\sqrt{18}$ (run `2026-10-19-claude-interactive.13-similariton-lo-verification`) by that seed's $N_0=2.6\times10^9$; the seed has $\varepsilon_0=0.067$, $\Gamma=4.8$ (run `2026-10-08-claude-a-amp-sim-checks`). On the asymptote with its own parameters the leading-order formula gives about 0.09 at $\tau=12$. Same order; reword or recompute.
3. `problems/P-001-*.md`: the Conjectures section lists only C-20261004-claude-a-01 and C-0001, and the 2026-10-04 update says the amplifier case is untouched. Bring the narrative in line with the frontmatter (claims C-20261008-claude-a-01/-02, -gpt-a-01/-02, C-20261019-pi-chatgpt-02; results R-0011, R-0014).
4. `tasks/T-20261008-claude-a-03-*` (verify C-20261008-claude-a-02, p1, open) looks superseded by GPT 6 Pro's verification and gpt-e's audit; only P1-P6 items outside the narrowed result remain. Ask the PI whether to close or narrow it.
5. R-0014's regime table ("Below about 8 the (i) prefactor ratio is only 0.86-1.11") and claude-interactive.13's audit note: the committed checkpoints of run `2026-10-19-claude-interactive.13-similariton-lo-verification` (`reduced_summary.json`, `ratio_i_at`) give 0.766, 0.855, 0.935 at $\tau=2$, 4, 6 for $\Gamma=1$; state the case the range refers to, or widen it.
6. R-0011 section 5 quotes full-NLSE values at $\varepsilon_0=0.1$ (0.3317394, 0.03153063) and the core 0.2779053 that are not in the committed files of run `2026-10-18-pi-chatgpt-independent-verification`; commit a small summary of them (from the raw results at the run's raw_location) or mark them as raw-only.
Results files change only through a PR the PI approves.

## Deliverables

A PR with the proposed edits (results edits flagged for the PI), audit-trail rows, a log entry.

## Outcome

Items 1, 2, 5 corrected in PR #86; item 4 (T-20261008-claude-a-03) cancelled there; item 3 (P-001 narrative) and item 6 (raw-only R-0011 values, now committed as r0011_tau4_extract.json) in this PR.
