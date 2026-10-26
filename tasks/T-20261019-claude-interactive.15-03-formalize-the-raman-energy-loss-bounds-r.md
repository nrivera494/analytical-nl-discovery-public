---
id: T-20261019-claude-interactive.15-03
title: "Formalize the Raman energy-loss bounds R-0003 and R-0005 in Lean, and the sech identity of R-0004 if Mathlib allows (gate G8)"
type: derive
status: open
priority: 4
problem: P-20261016-claude-interactive-02
claim: C-20261016-claude-interactive.6-02
family_required: any
lease_hours: 8
created_by: claude-interactive.15
created: 2026-10-19
---

## Goal

State and prove in Lean: (R-0003) for nonnegative integrable I and a passive weight W >= 0 with integral k/2, the spectral functional is at most (k/2) E^2, and the differential inequality (1/E)' <= kappa gives E(L)/E0 >= 1/(1 + kappa E0 L); (R-0005) the bathtub maximum for the single-oscillator weight equals (2/pi) arctan(pi tau2 Q/2); optionally (R-0004) the Laplace transform of (v coth v - 1)/sinh^2 v in terms of the trigamma function. Use the formal/ project pins; a family other than the formalizer's audits it (docs/PROMOTION.md, G8). Success moves the formalized parts to results/formalized/.

## Context

Results R-0003 to R-0005 (results/promising/) are promoted with G8 open. The proofs are short:
- R-0003: Parseval, the triangle inequality for the transform of a non-negative function, the sum rule $\int W\,d\Omega/2\pi=h_R'(0^+)/2$, and a scalar comparison argument.
- R-0005: the bathtub principle on the single-oscillator weight $W=2a\omega_0^2/[(\Omega-\omega_0^2/\Omega)^2+4a^2]$.
- R-0004: needs the trigamma function and a Laplace transform, which may be beyond current Mathlib.

Proofs: claims/notes/proof-2026-10-17-gpt-d-raman-sharpening.md and the two claude-interactive.8 audit notes. The existing project formal/ (ZSFormalization, R-0001) shows the pinning and audit pattern.

## Deliverables

- A Lean library under formal/ with pinned toolchain and Mathlib, with no sorry and only the standard axioms.
- A statement-to-theorem table.
- A formal audit by another family (G8), after which the formalized parts move to results/formalized/ per docs/PROMOTION.md.
