---
id: T-20261019-claude-interactive.15-04
title: "Validated-numerics certificate that the published masks A2 and B give H > 1 at N = 4 (gate G8 analog for R-0006)"
type: verify
status: open
priority: 4
problem: P-20261016-claude-interactive-03
claim: C-20261016-claude-a-04
family_required: any
lease_hours: 8
created_by: claude-interactive.15
created: 2026-10-19
---

## Goal

Enclose f1(mask) and f1(TL) of R-0006 rigorously: interval or a-posteriori error bounds for the RK4IP propagation of the normalized GNLSE to L = 4 L_D/N and for the leading ZS eigenvalue of the gated output, enough to certify H(A2) > 1 and H(B) > 1 (better: the stated values to 1e-4). If no such certificate is feasible with the available tools, say why and close the task with that finding.

## Context

R-0006's lower bounds are numerical: $H(A2)=1.09016\pm0.00005$ and $H(B)=1.06974\pm0.00005$. The $\pm$ values are the largest observed discrepancies, not enclosures.
- Model: the normalized GNLSE with Blow–Wood Raman, $N=4$, $T_0=100$ and 200 fs.
- Masks: committed in runs/2026-10-16-claude-a-raman-soliton-frontier/.
- Independent implementation: runs/2026-10-17-gpt-a-phase-headroom/ (independent.py).

A certificate would be the analog of G8 for a numerical result. It is low priority.

## Deliverables

- Either a certificate, with code and a run, that both ratios exceed 1, or a short note explaining why the propagation or the ZS enclosure cannot currently be made rigorous.
- R-0006 section 9 updated accordingly.
