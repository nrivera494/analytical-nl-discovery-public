---
id: T-20261019-claude-interactive.18-03
title: "Cross-family check of the equality case of the ZS L^p inequality (extremizers are exactly q* up to constant phase, carrier exp(-2i xi t) and delay) and of its corollary that the even-moment chain certifies TL optimality only for integer-order sech lasers"
type: verify
status: open
priority: 3
problem: P-20261016-claude-interactive-03
claim: C-20261018-pi-chatgpt-01
family_required: gpt
lease_hours: 8
created_by: claude-interactive.18
created: 2026-10-19
---

## Goal

A GPT-family agent checks, line by line or by an independent proof, the equality analysis in Appendix A of docs/manuscripts/2026-10-19-phase-shaper-soliton-bounds/main.tex (claude-interactive.18's derivation, not in the verified record), including the a.e.-equality step, the Lipschitz argument that theta stays in (0, pi/2), and the phase computation alpha' = -xi, beta' = xi; and the corollary in Sec. IV A that, for every laser other than an integer-order sech (up to carrier and delay), every even-moment ceiling lies strictly above the TL eigenvalue. Verdict recorded in a short report; if it holds, propose adding it to R-0001/R-0002 through the PI.

## Context

The verified record (R-0001, R-0002, claude-interactive.9's audit) proves that q* attains equality in int|q|^p >= C_p eta^(p-1), not that it is the only extremizer. The manuscript `docs/manuscripts/2026-10-19-phase-shaper-soliton-bounds/` (task T-20261019-claude-interactive.18-01) derives uniqueness up to constant phase, carrier and delay (Appendix A, "Equality") and uses it in Sec. IV A to explain why the asymmetric spectrum of C-20261016-claude-a-01 evades the hierarchy. Both are marked "our derivation" there. A Claude agent wrote them, so the check should come from another family.

## Deliverables

A report (pass, fail or narrowed) committed under `claims/notes/` or `docs/`, a log entry, and, if it passes, a proposal to the PI for wording in R-0001/R-0002.
