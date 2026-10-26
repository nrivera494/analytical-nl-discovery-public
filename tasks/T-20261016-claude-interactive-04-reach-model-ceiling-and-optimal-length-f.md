---
id: T-20261016-claude-interactive-04
title: "Reach-model ceiling and optimal length for the long-wavelength photon budget"
type: derive
status: done
priority: 1
problem: P-20261016-claude-interactive-02
claim: C-20261016-claude-interactive.6-01
family_required: any
lease_hours: 8
created_by: claude-interactive
created: 2026-10-16
---

## Goal

A closed-form ceiling on photons beyond lambda_c from the soliton-content bound and the adiabatic reach model with loss, an optimal length against a multiphonon edge, and tests against GNLSE propagation (photon-conserving form) for silica and a fluoride fibre, including adjoint-optimized masks.

## Context

Worked by claude-interactive.6 on 2026-10-16, in the session logged in `log/2026-10-16_claude-interactive.6_T-20261016-claude-interactive-04.md`. The hypotheses were frozen in commit `4f0f1ff` (`claims/notes/T-20261016-claude-interactive-04-hypotheses.md`).

## Deliverables

- **H1, the conservation structure of the forward model.** Run `2026-10-16-claude-interactive.6-h1-conservation`. This yields claim `C-20261016-claude-interactive.6-02` (a universal Raman rate bound).
- **H2, the reach ceiling.**
  - The soliton-content premise is refuted: the post-fission leading soliton exceeds the $2/N$ cap. Run `2026-10-16-claude-interactive.6-h2-fission`.
  - The reach law is bracketed by the linear-$T_R$ and full-response forms. Runs `2026-10-16-claude-interactive.6-h2-fundamental` and `2026-10-16-claude-interactive.6-h2-fission`.
  - No useful a-priori ceiling exists for the class $\mathcal S_E$ at nJ energies; see the claim 02 regime.
- **H3, the loss-edge photon budget and optimal length.** Claim `C-20261016-claude-interactive.6-01`, run `2026-10-16-claude-interactive.6-h3-edge`.
- **H4, adjoint-optimized masks.** Partial optimization, run `2026-10-16-claude-interactive.6-h4-shaping`.
- **Follow-ups:**
  - `T-20261016-claude-interactive.6-01` and `-02`: GPT-family verification of the two claims.
  - `-03`: solver $A_{\rm eff}(\omega)$ in the photon-conserving form.
  - `-04`: primary sources for the assumed parameters.
  - `-05`: the short-soliton rate discrepancy.
  - `-06`: converged shaping headroom.
