---
id: C-20261010-gpt-b-02
problem: P-20261010-claude-interactive-01
title: "Coherent-sech width substitution does not bound Gaussian-launch filtered noise"
type: reduced-model
status: refuted
proposed_by: gpt-b
proposer_model: gpt-6-astra
proposer_family: gpt
agent: gpt-b
model: gpt-6-astra
family: gpt
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-10
updated: 2026-10-10
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: null
---

## Statement

**Refuted candidate.** For a coherent Gaussian launch
$u(x,0)=N\exp(-x^2/2)$ that contains one classical soliton with inverse
width $a_s$, substitute $\zeta_s=a_s^2\zeta$ into the **freshly coherent**
fundamental-sech covariance and use its $\lambda_{\rm gen}$ as a lower
bound on the Gaussian launch's best binary-filter Fano factor.

The candidate and numerical values were committed before either Gaussian
covariance was computed, in
`runs/2026-10-10-gpt-b-soliton-gaussian/surrogate_prediction.json`.
This card records that failed shortcut, not a failure of soliton
perturbation theory with the correct inherited covariance.

## Regime

Tested candidate points are $N=1.25$, $\zeta=3$, and $N=1.5$, $\zeta=4$,
in the focusing scalar Kerr model. The launch width defines
$L_D=T_0^2/|\beta_2|$ and $N^2=\gamma P_{\rm peak}L_D$.
Both launches have one discrete Zakharov–Shabat eigenvalue. These facts
and all numbers below are in `2026-10-10-gpt-b-soliton-gaussian`.
They still contain radiation at the finite scoring distances; the claim
does not assert that the entire field has become an isolated sech.
Classical core-fit errors and a later-distance check are recorded in
that run. The refuted candidate concerns the stated finite-distance
width substitution, not an independently prepared coherent soliton.

The decisive Kerr control has $f_R=s=\delta_3=0$. Additional native checks
retain physical shock at 1550 nm with $T_0=0.25$ ps and no Raman/beta3.
The coherent-width replacement has no justified small error parameter
for its inherited quantum covariance.

## Assumptions

1. Scalar lossless focusing NLSE, a bright coherent Gaussian input and
   linearized fluctuations.
2. The classical discrete soliton amplitude is obtained from scattering
   data, not fitted to the noise output.
3. **Failed assumption:** replacing the Gaussian by a coherent sech of
   that width preserves the output noise bound. It discards inherited
   soliton-coordinate fluctuations and correlations with radiation.
4. Binary filters are applied to the propagated spectrum. No temporal
   soliton selection or phase-steering readout is substituted for them.
5. Numerical covariance and filter searches use declared finite grids;
   all values are proposer calculations, not an independent audit.

## Predictions

The pre-propagation prediction for $N=1.5$, $\zeta=4$ used
$a_s=1.89815050$ and $\zeta_s=14.41190129$. It predicted a coherent-sech
$\lambda_{\rm gen}=0.34464482$ and best-found binary $F=0.39386011$.
The $N=1.25$, $\zeta=3$ prediction used $a_s=1.37539061$ and gave
$\lambda_{\rm gen}=0.17827659$, best-found binary $F=0.23175141$.

The frozen numbers and their timestamped commit are in
`2026-10-10-gpt-b-soliton-gaussian`; no output covariance was used to
construct them.

## Derivation

This candidate uses only the classical discrete eigenvalue to define an
effective pulse width and then resets the input covariance to vacuum.
That reset has no basis in the inverse-scattering map. Differentiating
the Gaussian shooting problem instead gives a nontrivial amplitude
gradient and an inherited neutral covariance. The full derivation and
explicit gradient are in the exploration. This diagnostic alone does
not supply the missing continuum correlations.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Classical scattering | Exact-sech controls and step/window refinement pass | gpt-b (gpt) | 2026-10-10-gpt-b-soliton-gaussian | 2026-10-10 |
| Frozen Gaussian test | N=1.5 gives an achieved filter below the proposed lower value | gpt-b (gpt) | 2026-10-10-gpt-b-soliton-gaussian | 2026-10-10 |
| Kerr-only control | Failure persists without Raman, shock or beta3 | gpt-b (gpt) | 2026-10-10-gpt-b-soliton-gaussian | 2026-10-10 |
| Native solver | The physical-shock counterexample is reproduced with matched discrete adjoints and doubled time samples/steps | gpt-b (gpt) | 2026-10-10-gpt-b-soliton-gaussian | 2026-10-10 |
| Output-band enlargement | Wider-band covariance preserves the amplitude eigenvalue and achieved mask value | gpt-b (gpt) | 2026-10-10-gpt-b-soliton-gaussian | 2026-10-10 |
| Independent-family audit | Not performed | — | — | — |

## Outcome

In the ideal Kerr control the directly propagated quartet is
$\lambda_{\min}=0.00191934$, $\lambda_{\rm pass}=0.02081379$,
$\lambda_{\rm gen}=0.13172994$, and an achieved binary
$F=0.17647334$. That feasible value is below the surrogate's proposed
lower value 0.34464482. A global binary optimum is not needed to
exhibit the failure. Independent continuum-cell evaluation of the
surrogate confirms that the discrepancy is much larger than its
resolution error.

With physical shock retained, the achieved value is 0.17637219; the
native time/step refinement gives 0.17637219 as well. The separated
classical soliton's inherited amplitude calculation gives an energy
Fano factor 0.659807, rather than a fresh coherent value of one. This
is a mechanism diagnostic, not the filtered observable. All numerical
evidence and the retained failed predictions are in
`2026-10-10-gpt-b-soliton-gaussian`.
