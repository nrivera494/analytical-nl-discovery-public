---
id: T-20261016-gpt-a-02
title: "Resolve the residual Roy full-model figure offset"
type: verify
status: open
priority: 2
problem: P-20261016-claude-interactive-01
claim: C-20261016-claude-b-01
family_required: any
lease_hours: 8
created_by: gpt-a
agent: gpt-a
model: gpt-6-astra
family: gpt
created: 2026-10-16
---

## Goal

Resolve or bound the remaining offset between independently converged full-model simulations and Roy et al. Fig. 3(b). Audit the response and shock conventions, spectral-peak normalization and figure extraction. Preserve the published-data limitation if original numerical values are unavailable; do not reinterpret Eq. 6 as an integrated yield.

## Context

Roy, Bhadra and Agrawal, DOI 10.1103/PhysRevA.79.023824, full text accessed
by gpt-a. Runs `2026-10-16-gpt-a-roy-reference`, `2026-10-16-gpt-a-dw-roy`
and `2026-10-16-gpt-a-dw-analysis` give an RMS offset of 1.3724 dB and a
maximum absolute offset of 1.7039 dB over the compared full-model circles.
Peak frequencies agree within 2.61 percent. The sampled Raman kernel
converges to the analytic response at second order; step/grid changes and
the native solver cross-check are much smaller than the residual
(`2026-10-16-gpt-a-dw-convergence`, `2026-10-16-gpt-a-dw-followup`,
`2026-10-16-gpt-a-dw-julia`).

The paper's shock coefficient is 1/(omega0*T0); the PI assignment also
requested the doubled variant. Both are retained in the audit. This offset
does not restore a 40 dB discrepancy in the validated full model.

## Deliverables

- An independently checked convention and normalization ledger.
- Any further parameter-sensitivity or source-data checks, with run ids.
- A quantified residual and a clear distinction between reproducing plotted
  circles and reproducing unavailable numerical source data.
