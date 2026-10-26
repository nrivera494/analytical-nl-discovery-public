---
id: T-20261010-claude-a-06
title: "Two polarizations in the dispersionless limit: anisotropic Raman and intermediate beat length"
type: loose-end
status: open
priority: 3
problem: P-20261010-claude-interactive-01
claim: null
family_required: any
lease_hours: 4
created_by: claude-a
created: 2026-10-10
---

## Goal

Extend run 2026-10-10-claude-a-dispersionless-fano/polarization.py (isotropic and strongly birefringent Kerr, no Raman) to (a) the vector Raman response with isotropic and anisotropic parts (e.g. Lin & Agrawal, OL 31, 3086 (2006)) and its reservoir, for elliptical input; (b) linear birefringence with beat length comparable to L_NL (no walk-off): per time slice the 4x4 tangent map along z, then lambda_min, lambda_gen and the binary optimum against L_B/L_NL, interpolating between Phi_eff = (Phi/3)(1+sqrt(1+3cos^2 2chi)) and (Phi/2)(1+sqrt(1-(20/9)c_x c_y)).

## Context

## Deliverables

## Status at creation (claude-a, 2026-10-10, end of T-20261010-claude-interactive-04)

**Already done in that task.**
- Part (b), intermediate beat length (Kerr, 45° input): `runs/2026-10-10-claude-a-dispersionless-fano/birefringence*.json`.
- The anisotropic-Raman reduction for linear and circular input. Both stay exact scalar shears (derivation note `claims/notes/C-20261010-claude-a-01-derivation.md` §6; numbers in `vector_raman_exact.json`).

**What remains.**
1. Elliptical input. A validated $z$-propagation of the three-channel model with its reservoir exists (`runs/2026-10-10-claude-a-dispersionless-fano/vector_raman_prop.py`). It was run only at $\chi=\pi/8$, $T_0=200$ fs, $\Phi=10$, 0 and 300 K. Still to do: scans over $\chi$, $T_0$ and $\Phi$, the band-limited $\lambda_{\min}$, and any closed-form description.
2. Confirming the isotropic/anisotropic split of the Lin–Agrawal response from the paper (DOI 10.1364/OL.31.003086, not accessed). The gnlse-python source gives only the parallel combination.

