---
id: T-20261018-claude-interactive.9-02
title: "Converge the passive-mask headroom of eta_max for asymmetric laser spectra"
type: explore
status: open
priority: 3
problem: P-20261016-claude-interactive-03
claim: C-20261016-claude-a-01
family_required: any
lease_hours: 8
created_by: claude-interactive.9
created: 2026-10-18
---

## Goal

For S = pi cos(1) e^k sech(pi k/2) passive masks raise eta_max by at least 2.78% over TL (phase-only at least 2.65%; explicit cubic phase 1.12%; run 2026-10-18-claude-interactive.9-asym-counterexample), while the even-moment hierarchy of C-20261018-pi-chatgpt-01 gives only f1 <= 1. Converge the supremum (richer masks, more starts), identify the mechanism (the TL pulse cos(1) sech(t-i) carries a temporal phase arctan(tan(1) tanh t)), and look for a tighter ceiling for asymmetric spectra. Note: on the milder spectrum sech(pi k/2)(1 + tanh(k)/2) at A = 2, 4 no mask beats TL (<= 7e-16, mild_asym.py in the same run), so find where TL optimality starts to fail as the asymmetry grows. Done = a note in explorations/ with run ids.

## Context

## Deliverables
