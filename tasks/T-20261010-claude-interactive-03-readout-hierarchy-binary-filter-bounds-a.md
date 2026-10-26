---
id: T-20261010-claude-interactive-03
title: "Readout hierarchy, binary-filter bounds above the generalized eigenvalue, and reference values for single-mode fibre"
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

1. **Proof.** In linearized theory, for mixed Gaussian states with several modes and polarizations, prove $\lambda_{\min}(V)\le\lambda_{\rm pass}\le\lambda_{\rm gen}\le\min_TF[T]$. Identify $\lambda_{\rm pass}$ as the limit for passive linear optics followed by photon counting.
2. **Binary-specific bounds.** Lower bounds strictly above $\lambda_{\rm gen}$ that use $T_i\in\{0,1\}$, plus cheap certificates.
3. **Reference table.** Values for scalar single-mode fibre against which the formulas from -04, -05 and -06 are scored.

## Context

Approach 4 of 4 on P-20261010-claude-interactive-01 (see its Approaches table). Assigned to gpt-a.

**Regime-agnostic.** Do not derive propagation formulas for a particular regime; -04, -05 and -06 do that.

**Hierarchy.** See "A structure to start from" on the card. Still to settle:
- the conditions on the counted port's brightness under which $\lambda_{\rm pass}$ is reached;
- multi-port weighted counting;
- Raman-mixed states.

**Binary-specific bounds.** Candidates:
- the Shor semidefinite relaxation with $X_{ii}=T_i$, plus RLT or triangle cuts;
- first-order optimality conditions, giving a threshold or self-consistent characterization of locally optimal filters and a fast fixed-point search;
- structural results on how many spectral intervals an optimal filter has;
- rounding-gap bounds between $\lambda_{\rm gen}$ and the binary optimum.

**Cheap certificates.** Candidates:
- Weyl splitting of $V$ into a vacuum-driven part and a reservoir-driven part;
- Temple or Lehmann–Goerisch intervals from one trial filter, so that one good filter plus a few integrals certifies near-optimality;
- uncertainty relations: bounding $\min_TF$ below by $\lambda_{\rm pass}$ together with an upper bound on the conjugate-quadrature variance.

**Reference table** (the original scope of this task).
- Scalar single-mode fibre and a Gaussian input.
- Both signs of $\beta_2$, plus a near-zero-dispersion case, each with and without Raman.
- Symmetrized reservoir, time step of 3 fs or less, discrete adjoint.
- A grid in $N$ (or $\Phi_{\rm peak}$) and $L/L_D$ that includes points in the -04, -05 and -06 regimes.
- At each point: $\lambda_{\min}(V)$, $\lambda_{\rm pass}$, $\lambda_{\rm gen}$, the best relaxation bound, and the best binary filter found, with how it was searched.
- A check of the dispersionless Kerr anchor, $V_{\min}(\Phi)=1+2\Phi^2-2\Phi\sqrt{1+\Phi^2}$.
- Grid, step and window convergence.

## Deliverables

- A proof note in `explorations/`, or a claim if the result is new.
- Registered runs, and an exploration note holding the reference table.
- A log entry with "Proposed card changes".
