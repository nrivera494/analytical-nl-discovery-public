---
id: C-20261010-claude-a-03
problem: P-20261010-claude-interactive-01
title: "Parity bound: for a parity-symmetric problem every binary (or non-negative) spectral filter on a bin set B has F ≥ (λ_odd + λ_even)/2, which decays far more slowly than λ_gen"
type: bound
status: proposed
proposed_by: claude-a
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-10
updated: 2026-10-10
solver_commit: null
result: null
---

## Statement

**Setting.** The problem is parity-symmetric if the bin covariance $V^{\rm amp}$ (local amplitude quadratures of the spectral bins, shot noise 1) commutes with $\omega\to-\omega$ about the carrier. This holds for:
- a coherent input whose field is even in $t$, so unchirped with even intensity;
- propagated by dynamics invariant under $t\to-t$: Kerr with even-order dispersion only, scalar.

Raman, self-steepening and $\beta_3$ break it.

Let $\lambda_{\rm odd}$ and $\lambda_{\rm even}$ be the smallest eigenvalues of $V^{\rm amp}$ on the odd and even bin combinations. $\lambda_{\rm gen}=\min(\lambda_{\rm odd},\lambda_{\rm even})$.

**Claim (rigorous within linearized theory).** Let $B$ be a parity-symmetric set of spectral bins. For every filter supported on $B$ with non-negative transmissions $T_i\ge0$, binary filters included,
$$F[T]\;\ge\;F_{\rm par}(B)\equiv\begin{cases}\tfrac12(\lambda_{\rm odd}+\lambda_{\rm even}),&\lambda_{\rm odd}\le\lambda_{\rm even}\\ \lambda_{\rm even},&\text{otherwise,}\end{cases}$$
with the eigenvalues taken on $B$.

**Choice of $B$ matters.**
- Admitting very dark bins with arbitrary weight lowers $\lambda_{\rm even}$ strongly, and hence $F_{\rm par}$. At $\Phi=20$: $F_{\rm par}=0.152$, 0.144, 0.061 for $B=\{\bar n\ge10^{-6},10^{-9},10^{-12}\,\bar n_{\max}\}$ (`grid_check2.json`).
- A binary filter gives such bins only weight $\sqrt{\bar n_i}$, so they change $F$ by at most about $2\lVert V^{\rm amp}\rVert\,(\sum_{i\notin B}\bar n_i/\sum_{i\in B}T_i\bar n_i)^{1/2}$.
- Linearization also requires $\bar n_i\gg1$ in every bin used. So $B$ is bounded below physically by the photon number per bin. For a pulse of about $10^9$ photons spread over about $10^3$ bright bins, $10^{-6}\bar n_{\max}$ is about 10 photons.
- All numbers below use $B=\{\bar n\ge10^{-6}\bar n_{\max}\}$. This is the same set the binary filters were optimized on.

**Proof sketch.**
1. The readout weights $y=T\sqrt{\bar n}$ are non-negative.
2. Split $y$ into even and odd parts: $|y_e|^2-|y_o|^2=\sum_iy_iy_{\bar\imath}\ge0$, where $\bar\imath$ is the mirror bin.
3. $V^{\rm amp}$ has no even–odd cross terms, so $F=(y_e^{\mathsf T}V^{\rm amp}y_e+y_o^{\mathsf T}V^{\rm amp}y_o)/|y|^2$.
4. Minimize $\lambda_{\rm odd}f+\lambda_{\rm even}(1-f)$ over the odd fraction $f\le\tfrac12$.

**Consequence in the dispersionless Kerr case.**
- $\lambda_{\rm odd}=\lambda_{\rm gen}\approx1.3/\Phi^2$ is the momentum mode (C-20261010-claude-a-02).
- $\lambda_{\rm even}$ on $B$ falls much more slowly than $\lambda_{\rm gen}$. It oscillates between 0.09 and 0.57 for $2\le\Phi\le60$ (`lam_gen_dense.json`).
- Its average over windows of $\Phi$ drifts down: 0.34 ($\Phi=2$–10), 0.23 (10–20), 0.20 (20–30), 0.16 (30–45), 0.12 (45–60). That is roughly $\Phi^{-1/2}$, against $\Phi^{-2}$ for $\lambda_{\rm gen}$.
- The values for $\Phi\ge44$ come from a grid whose $\lambda_{\rm gen}$ is not converged in bin threshold, so they are indicative only.
- So a non-negative filter can use at most half of the strongly squeezed momentum mode. $F_{\rm par}$ is 0.045–0.26 for $7\le\Phi\le60$, while $\lambda_{\rm gen}$ falls as $\Phi^{-2}$.

Unlike $\lambda_{\min}(V)$ and $\lambda_{\rm gen}$, this bound decays slowly with $\Phi$, as the best binary filter does, rather than as $\Phi^{-2}$. Binary-specific bounds from T-20261010-claude-interactive-03 have not been compared yet.
- Best binary: about $\Phi^{-0.21}$ for $\Phi\ge10$.
- $F_{\rm par}$: roughly $\Phi^{-1/2}$ in window averages.
- See the exploration note `explorations/2026-10-10-claude-a-binary-filters-dispersionless.md`.

## Regime

- **Validity.** Linearized theory, any $\Phi$, any parity-symmetric dynamics. The inequality is exact.
- **Numbers.** Reported only for dispersionless Kerr, Gaussian $1\le\Phi\le40$ and sech $\Phi=5,15$, with the bin set $B=\{\bar n\ge10^{-6}\bar n_{\max}\}$ at padding 8.
- **Parity in the computation.** Exact to $3\times10^{-8}$ in commutator norm for the Gaussian, and $10^{-4}$ for the sech grid, whose window is one sample off symmetric.
- **Not covered.** Raman, self-steepening, $\beta_3$, chirped or asymmetric pulses: the bound needs exact parity. Raman changes the binary optimum by under 3% (`binary_relax_raman.json`), so an approximate version may still be informative, but it is not claimed.

## Assumptions

1. Linearized Gaussian noise, coherent input.
2. Parity symmetry as stated. Bins placed symmetrically about the carrier.
3. Filters act on intensity (transmission $T_i\ge0$), followed by photon counting of all transmitted light in one detector.
4. Scalar, single mode. Ideal detection.

## Predictions

- Rigorous: no binary filter supported on $B$ in a parity-symmetric problem ever measures below $F_{\rm par}(B)$. A counterexample in a converged run refutes the claim.
- Gaps to the best binary found (Gaussian, Kerr, dispersionless). The binary values are the best over three methods:
  - nested tabu search (`binary_search4`, `scan_kerr_gaussian.json`) and the continuation runs at $\Phi=12.5$ and 25 (`continuation_kerr.log`), both computed before the bound;
  - the box-relaxation, dithering and tabu searches (`binary_relax*.json`), computed afterwards. Those searches do not use the bound.

| $\Phi$ | 1 | 2 | 3 | 5 | 7 | 10 | 12.5 | 15 | 20 | 25 | 30 | 40 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $F_{\rm par}$ | 0.484 | 0.286 | 0.184 | 0.308 | 0.076 | 0.156 | 0.106 | 0.129 | 0.152 | 0.081 | 0.121 | 0.061 |
| best binary | 0.774 | 0.702 | 0.662 | 0.677 | 0.488 | 0.471 | 0.450 | 0.439 | 0.400 | 0.322 | 0.401 | 0.359 |
| gap (dB) | 2.0 | 3.9 | 5.6 | 3.4 | 8.1 | 4.8 | 6.3 | 5.3 | 4.2 | 6.0 | 5.2 | 7.7 |

  The best binary is the minimum over nested tabu, the box relaxation with dithering and tabu (`binary_relax*.json`), and continuation. The binary values do not depend on the bound.
  - Sech (held-out pulse): $F_{\rm par}=0.146$ and 0.076, best binary 0.756 and 0.452, gaps 7.2 and 7.8 dB ($\Phi=5,15$).
  - Compare $\lambda_{\rm gen}$ against the best binary: 2.3, 4.8, 7.3, 11.8, 13.6, 16.1, 17.5, 19.0, 21.2, 21.9, 24.5, 26.5 dB at the same $\Phi$.
- Open prediction (with $B=\{\bar n\ge10^{-6}\bar n_{\max}\}$): for dispersionless Kerr with $40<\Phi\le100$, $\lambda_{\rm even}\ge0.05$, so $F_{\rm par}\ge0.025$. Registered at commit cb7ad63 (11:42 EDT).
  - **Tested at 13:06 EDT** (`open_prediction_lameven.json`): $\lambda_{\rm even}=0.097$, 0.070, 0.055 and $F_{\rm par}=0.048$, 0.035, 0.028 at $\Phi=70$, 85, 100. Holds, narrowly at $\Phi=100$.
  - The decay steepens to a local slope of about $-1.6$ between $\Phi=70$ and 100. So the bound weakens at very large $\Phi$, faster than the best binary falls ($\approx\Phi^{-0.2}$).
  - These grids are not converged in $\lambda_{\rm gen}$ at this threshold (section on bin set), so the values hold for the stated $B$ only.

## Derivation

The four steps under Statement. No other ingredient.

The even-sector floor at large $\Phi$ is understood only qualitatively.
- The even analogue of the momentum readout, $g=|\omega|$, has a kink at the frequency that maps onto the pulse peak. It costs $O(\Phi)$ noise (`dither_ramp.json`: $F=13.8$ at $\Phi=10$).
- Smooth even weights cannot cancel the anti-squeezed phase noise at leading order (C-20261010-claude-a-02, Derivation).

No formula for $\lambda_{\rm even}(\Phi)$ is claimed. It oscillates with $\Phi$, as does $\lambda_{\rm gen}/\lambda_P$.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | dimensionless | claude-a (claude) | — | 2026-10-10 |
| Known limits | $\Phi\to0$: $V^{\rm amp}\to I$, $F_{\rm par}\to1$. $\Phi=1$: $F_{\rm par}=0.484$ against $\lambda_{\rm gen}=0.456$ | claude-a (claude) | `2026-10-10-claude-a-dispersionless-fano` (`parity_bound.json`) | 2026-10-10 |
| Symmetries | parity commutator $\le3\times10^{-8}$ (Gaussian), $\le10^{-4}$ (sech) | claude-a (claude) | same | 2026-10-10 |
| Symbolic residual | n/a (the inequality is elementary) | | | |
| Simulation, core regime | $F_{\rm par}\le$ best binary at every point tested: Gaussian $\Phi=1$–40 at padding 8, $\Phi=20$ and 30 at padding 16, and the sech at 5 and 15. No binary found below it | claude-a (claude) | same (`parity_bound.json`, `parity_bound_sech.json`, `scan_kerr_gaussian.json`, `heldout_results.json`) | 2026-10-10 |
| Error-scaling exponent | n/a | | | |
| Held-out region | sech pulse; see Predictions | claude-a (claude) | same | 2026-10-10 |
| Convergence and artefacts | Time step $dt=0.8/\Phi$ vs $0.4/\Phi$: no change. Bin set: strong dependence on the darkness threshold, as stated under Statement ($\Phi=20$, 30, 40 at thresholds $10^{-6}$, $10^{-9}$, $10^{-12}$; `grid_check2.json`). Bin width: padding 16 gives the same $F_{\rm par}$ to 3 digits as padding 8 (0.1518 and 0.1214 at $\Phi=20$, 30). The padding-16 binary optima (0.391, 0.375) respect it, with gaps of 4.1 and 4.9 dB (`parity_pad16.json`) | claude-a (claude) | `2026-10-10-claude-a-dispersionless-fano` | 2026-10-10 |
| Second solver or relaxed assumption | not done | | | |
| Adversarial audit | not done. Binary-specific bounds are the lane of T-20261010-claude-interactive-03 (gpt-a). Its interim tables (unverified WIP, branch at 2a40651) report certificates within 0.001–0.27 dB of their best binary in dispersive cases. Those are much tighter than this bound, so where both apply this bound is likely dominated. There are no dispersionless rows there yet to compare | | | |
| Novelty search | Not searched specifically. Related: Levandovsky, Vasilyev & Kumar, OL 24, 43 (1999), full text read by claude-a.2. They argue that the optimal passive filter (transmission in $[0,1]$) for solitons is even in $\omega$, so momentum drops out; this is consistent with the parity structure here, but they state no bound | claude-a.2 (claude) | — | 2026-10-10 |

## Outcome

Open.
