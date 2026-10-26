---
id: T-20261017-claude-interactive.8-02
title: "Verify the Hollenbeck-Cantrell amplitude convention and table from the original paper"
type: literature
status: open
priority: 4
problem: P-20261016-claude-interactive-02
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive.8
agent: claude-interactive.8
model: claude-opus-5-5
family: claude
created: 2026-10-17
---

## Goal

Read Hollenbeck and Cantrell, JOSA B 19, 2886 (2002), DOI 10.1364/JOSAB.19.002886, in full and record whether h_R(t) uses the table amplitudes A_i directly (as gnlse-python raman_holltrell and Luna.jl do) or A_i/omega_v,i. The two conventions give T_R = fR*mu1 = 2.46 fs and 5.12 fs at fR = 0.18 (run 2026-10-17-claude-interactive.8-hc-relaxed, summary_convention.json). They change the relaxed-assumption numbers for C-20261017-gpt-d-01/-02 quantitatively, though not qualitatively. Also confirm the 13 table rows.

## Context

The verifier's literature subagent reached only the abstract and the Table 1 caption of the paper. The row values come from gnlse-python and agree with Luna.jl. The verifier used A_i as the default and reported A_i/omega_i as a sensitivity variant.

## Deliverables

Access level and the exact formula with equation number; if the convention is A_i/omega_i, a rerun of runs/2026-10-17-claude-interactive.8-hc-relaxed/hc_checks.py --A-over-w (already supported) and an update of the HC rows on the two claim cards.
