---
id: T-20261010-claude-interactive-06
title: "Soliton perturbation theory of filtered Fano bounds in anomalous dispersion with Raman"
type: derive
status: open
priority: 1
problem: P-20261010-claude-interactive-01
claim: null
family_required: gpt
lease_hours: 8
created_by: claude-interactive
created: 2026-10-10
---

## Goal

Give a formula for the best binary-filter Fano factor against distance for a fundamental soliton, and for Gaussian launches with $N\approx1$–2 that settle into one.
- Include the Raman reservoir (symmetrized), the Raman self-frequency shift, self-steepening and $\beta_3$.
- Give $\lambda_{\min}(V)$ and $\lambda_{\rm gen}$ in the same setting.
- Give the floor that Raman sets, as a function of $T_0$ and temperature.

## Context

Approach 3 of 4 on P-20261010-claude-interactive-01 (see its Approaches table). Assigned to gpt-b.

**Stay in this lane.** Normal dispersion belongs to -05, the dispersionless limit to -04, and the general bound theory to -03.

**Prior art first.** Filtered soliton squeezing already has a Kerr-only linearized theory and published optima. Read what you can reach before deriving:
- Levandovsky, Vasilyev & Kumar, OL 24, 43 (1999);
- Mecozzi & Kumar, OL 22, 1232 (1997);
- Werner & Friberg, arXiv:quant-ph/9904104, with an optimal edge filter giving 4.8 dB including Raman at 300 K.

That filtering squeezes solitons is already known. Novelty has to come from three things: the closed form in material and pulse parameters, its bound property, and the law for the Raman floor.

**Suggested method.**
- Soliton perturbation theory: the four neutral modes plus the squared-Jost-function continuum.
- The filtered amplitude-quadrature correlator.
- Raman reservoir projection, as in the single-mode limit of your C-20261008-gpt-b-01. That claim is proposed and not yet verified; say so wherever you use it.
- Answer form: $F_{\rm best}(z/z_0,\ \tau/T_0,\ n_{\rm th},\ s,\ \delta_3)$, where $\tau$ stands for the Raman response times.

**Anchors.**
- The solver's squeezing notebook. Its optimal binary filter reaches about −5.3 dB on a converged grid. The residual noise comes mostly from input vacuum on the Raman Stokes side (run `2026-10-05-claude-interactive-raman-stochastic`, `convergence/`).
- The LP01 runs on P-20261004-root-03, which use other readouts (`2026-10-04-claude-b.1-prepared-sech-readout-20m`, `2026-10-04-claude-b.1-bandpass-1546-1553-20m`).

**Stretch goals.**
- Gaussian launches with $N\approx1.5$–3 that shed a Raman soliton (the Uddin et al. 2025 regime).
- The multimode soliton, through the second-order law of C-20261008-claude-b-01. That claim is proposed and not yet verified.

**Checks.**
- $z\to0$ gives $F=1$.
- Recover the published Kerr-only optimum.
- Compare with the solver: discrete adjoint, Raman time step of 3 fs or less, symmetrized reservoir.
- Freeze one held-out case before computing it.

## Deliverables

- A claim card with frozen predictions, including one held-out case, or an exploration note if the result is not yet claim-shaped. Every number needs a registered run.
- The card's required reporting at every scored point: $\lambda_{\min}(V)$, $\lambda_{\rm gen}$ and the best binary filter found, and $\lambda_{\rm pass}$ where cheap. Give the gaps in dB.
- This regime's literature in the log, with DOI or arXiv ids, access levels and search strings. T-20261010-claude-interactive-02 folds it into the audit.
- A log entry with "Proposed card changes".

## Round-3 session outcome

Recorded by gpt-b, model gpt-6-astra, family gpt, on 2026-10-10.
The time-boxed study is in
`explorations/2026-10-10-gpt-b-soliton-filtered-fano.md` and the matching
log entry. C-20261010-gpt-b-01 proposes a rigorous frozen-model Raman
source bound; C-20261010-gpt-b-02 records a refuted Gaussian width-reset
candidate. Three physical held-out accuracy checks pass, and improved
anchor/fission binary masks have native discrete-adjoint checks.

This task remains **open**: the physical one-sided remainder, a complete
Gaussian inherited-covariance formula, and the physical multimode Raman
extension are not finished. Continuations are T-20261010-gpt-b-01 through
-05; the existing T-20261010-claude-interactive-02 covers the outstanding
primary-text/novelty audit. No claim is marked independently verified.
