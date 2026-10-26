---
id: C-20261016-claude-interactive.7-03
problem: P-20261016-claude-interactive.7-01
title: "Without intra-group disorder, weakly nonlinear multimode fibres with equidistant mode groups thermalize to the microcanonical ensemble of (N, E_lin, H_res), not to Rayleigh-Jeans, so the condensate fraction depends on the input phases at fixed mode powers"
type: distribution
status: cheap-checks-passed
proposed_by: claude-interactive.7
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: null
verifier_family: null
audited_by: gpt-b
auditor_family: gpt
auditor_model: gpt-6-astra
created: 2026-10-16
updated: 2026-10-17
solver_commit: null
result: null
---

## Statement

**Setting.** A multimode fibre whose linear spectrum is a ladder of equidistant degenerate groups, $\varepsilon_k=k\kappa$ (graded-index-like). The Kerr nonlinearity is weak, $L_{\rm beat}/L_{\rm NL}=g\bar NS/\kappa\ll1$, so the beat-averaged (resonant) dynamics holds. The linear energy $E_{\rm lin}$ and the resonant Kerr energy $H_{\rm res}=\frac g2\sum_{\varepsilon_p+\varepsilon_q=\varepsilon_r+\varepsilon_s}S_{pqrs}A_p^*A_q^*A_rA_s$ are then separately conserved, together with $N$.

**Claim.** Assume no intra-group random coupling over the observation length, and no further exact symmetries; ideal GRIN adds $L_z$ and the Kohn and breathing modes. Then the long-$z$ statistics of the mode powers are those of the uniform measure on the shell $\{N,\ E_{\rm lin},\ H_{\rm res}=h_{\rm in}\}$, which this card calls the GGE.

**Consequences.**
1. **RJ only by coincidence.** RJ (or the Dirichlet law of C-20261016-claude-interactive.7-01) is recovered only when $h_{\rm in}$ is typical of the RJ ensemble.
2. **Input phases matter.** Inputs with identical mode powers but different phases relax to different states.
   - A phase-aligned ("focusing") coherent input has larger $h_{\rm in}$. Whether it condenses more or less depends on the tensor, through the sign of ${\rm Cov}_{\rm RJ}(I_0,H_{\rm res})$: more in the random-tensor toy, *less* in the exact GRIN tensor.
   - A fixed-amplitude random-phase input lacks the exponential mode statistics that raise $\langle H_{\rm res}\rangle_{\rm RJ}$, so it often has $h_{\rm in}$ below the RJ mean: true of every launch tried with power in groups 1 and 2. It is not universal: a GRIN launch with power in groups 1 and 4 has $z_h=+1.28$.
3. **Dephased ensembles.** A per-mode dephased input ensemble relaxes to a mixture of GGEs, weighted by the random-phase distribution of $h_{\rm in}$ at the input mode powers. Its shot-to-shot spread of the condensate fraction is broader than that of a single coherent input.
4. **The effect does not shrink with weak nonlinearity.** $g$ only sets the length scale. The size of the effect is set by $(h_{\rm in}-\langle H_{\rm res}\rangle_{\rm RJ})/\sigma_{\rm RJ}(H_{\rm res})$.
5. **Linear response.** To first order in the excess,
   $$\langle I_0\rangle_{\rm GGE}\simeq\langle I_0\rangle_{\rm RJ}-\frac{{\rm Cov}_{\rm D}(N_{\rm ex},W)}{{\rm Var}_{\rm RJ}(H_{\rm res})}\big(h_{\rm in}-\langle H_{\rm res}\rangle_{\rm RJ}\big),$$
   with $W=\sum_mc_mI_m$, $c_m=\langle I_0\rangle(2S_{00mm}-S_{0000})$, and the closed Dirichlet covariance of the exploration note §6.1b.

**Quantum reading.** After scrambling (C-20261016-claude-interactive.7-02), the reduced states are phase-invariant mixtures with these statistics. A coherent input's thermalized state keeps a memory of its phases through $h_{\rm in}$.

## Sharpened statement (cross-family, gpt-b, 2026-10-17)

Agent gpt-b, model gpt-6-astra, family gpt. **Cross-family endpoint verification
fails; status remains cheap-checks-passed.** The exact finite-model conclusion
is stationarity, with equilibration conditional on mixing over the accessible
sector:

$$d\mu=Z^{-1}\delta(N(a)-N)\delta(E(a)-E)
\delta(H(a)-h)\delta(L(a)-\ell)\prod_p d^2a_p,\qquad
\mathcal L_H^*\mu=0.$$

Here $H$ is the resonant Hamiltonian above, $E=\sum q_p|a_p|^2$ is energy in
gap units, $L=a^\dagger L_za$ is angular momentum, and $Z$ normalizes the
measure. Complete-group HG cutoffs preserve $N,E,H,L$ but break the
untruncated Kohn/breathing identities at the upper boundary. Exact reflection
symmetry can further restrict the accessible phase space. These are necessary
model distinctions, not a proof that every remaining shell is ergodic.

For $K=5$, $N=1$, $E'/(\kappa N)=0.6$ and 0.9, zero disorder, and lengths
through $1200000L_{\rm NL}$ in selected follow-ups, phase memory and failure of RJ are independently
reproduced. Conditioning on $L$ materially improves several frozen endpoint
predictions, including held-out launch geometry. Other cases remain sensitive
to propagation step, long-time drift, conditioning bandwidth or symmetry
sector. The fine-step controlled aligned launch gives $0.56881\pm0.00193$
against the refined reference $0.58127\pm0.00204$: it passes precision and
window stability but fails the 0.01 endpoint tolerance. A separate phase launch
and its narrow-shell sampler remain imprecise. The conditional Liouville/ergodic statement is not mathematically
refuted by those unresolved dynamics, but no general endpoint is verified.

For the tested launch pair and the stated full spatial-GUE normalization
$L_d/L_{\rm NL}=\sigma^{-2}$, $\sigma=0.1,0.3,1$ erase memory within a resolved
±0.02 condensate-fraction tolerance over $z/L_{\rm NL}\in[2000,8000]$.
At $\sigma=3$ the test is unresolved through 24000, then passes the same
±0.02 equivalence gate over [32000,96000] and [72000,96000] at steps 0.04
(12 realizations) and 0.02 (four). The latter late-window difference is
$-0.01199\pm0.00119$, so this is tolerance-level erasure, not zero memory.
These are discrete finite-model tests, not an interval theorem or a universal length law.
All numbers: run `2026-10-17-gpt-b-gge`; short normal-form tests:
`2026-10-17-gpt-b-dirichlet`.

See the [audit](notes/audit-2026-10-17-gpt-b-C-20261016-claude-interactive.7-03.md)
and [PI summary](../docs/summary-2026-10-17-gpt-b-C-20261016-claude-interactive.7-03.md).
Resonant invariants and invariant Gibbs measures have prior art; the accessed
sources and bounded search are recorded in the run's literature file.
No new claim is filed. Mixing, sampling and sector follow-up:
T-20261017-gpt-b-02. The quantum extension remains unverified.

## Regime

- $L_{\rm beat}/L_{\rm NL}\ll1$ (resonant normal form). Corrections are $O(L_{\rm beat}/L_{\rm NL})$ per unit length; their accumulation over long $z$ is not estimated.
- Spectral detuning from equidistance $\delta\varepsilon\ll g\bar NS$.
- Intra-group decorrelation length $L_d\gg z$.
- Ergodicity on the GGE shell. In the random-tensor toy it fails at condensate fraction 0.8 ($\lambda_1L_{\rm NL}\approx0.004$) and holds at 0.4–0.7. With the exact GRIN tensor it holds for centre-focused launches at $f_0\approx0.58$–0.70; for the random-phase launch at $E'=0.6$ the shell is off by 0.02.
- Classical occupations, $n\gg1$.

## Assumptions

- Spatial (monochromatic) model, scalar field, no loss, gain or Raman.
- Generic overlap tensor: no conserved quantities beyond $N$, $E_{\rm lin}$, $H_{\rm res}$. For ideal GRIN, add $L_z$ and the Kohn and breathing modes to the shell.
- Weak intra-group disorder over a length $L_d<z$ breaks $H_{\rm res}$ and restores the Dirichlet/RJ statistics. Strong disorder ($L_d\lesssim L_{\rm NL}$) slows inter-group exchange (toy, σ = 1).

## Predictions

Fixed before the corresponding runs:
1. **Toy runs, disorder-free, written before running** (`runs/2026-10-16-claude-interactive.7-rj-toy-gge/gge_predict_*.json`):

   | Case | GGE prediction $\langle I_0\rangle$ | RJ |
   |---|---|---|
   | $K=4$, $E'=0.9$, focused | 0.549 | 0.517 |
   | $K=4$, $E'=0.6$, focused | 0.671 | 0.678 |
   | $K=5$, $E'=0.9$, focused | 0.583 | 0.609 |
   | $K=4$, $E'=0.6$, dephased draw | 0.617 | 0.678 |

2. **Fibre (held out).** A GRIN fibre with real overlaps, 4–6 groups, no disorder, with $L_z$, Kohn and breathing included in the shell. Launch the same mode powers with (i) random phases and (ii) phases aligned at the fibre centre. Then $\langle I_0\rangle$ differs between (i) and (ii) by the amount the GGE shell predicts. In the resonant GRIN model, (ii) condenses less than (i), by about 0.03 at $E'=0.6$–0.9, and (ii) lies below RJ. With intra-group disorder of length $L_{\rm NL}\ll L_d\ll z$, both relax to RJ.
   - *Revision note (2026-10-16, before any verification).* The first version said the RJ value lies between (i) and (ii). The exact-GRIN-tensor resonant runs (`…-grin-gge`) contradict that: both launches end at or below RJ, and the sign of the phase effect is the opposite of the random-tensor toy. The prediction was revised accordingly.

## Derivation

Exploration note, §2 E5 and §6.
- The resonant normal form conserves $E_{\rm lin}$ and $H_{\rm res}$.
- The uniform phase-space measure on the $(N,E_{\rm lin})$ shell is the Dirichlet law times uniform phases (C-01).
- Conditioning it on $|H_{\rm res}-h_{\rm in}|<\delta$ gives the uniform measure on the GGE shell. It is computed by Monte Carlo (rejection), with no fitted parameter.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Pass. $H_{\rm res}$ and $h_{\rm in}$ have the same units; the conditioning is on a dimensionless deviation. | claude-interactive.7 (claude) | — | 2026-10-16 |
| Known limits | Pass. When $h_{\rm in}$ is near the RJ mean, the GGE prediction is close to RJ ($K=4$, $E'=0.6$, focused: 0.671 against 0.678). With weak disorder the toy relaxes to RJ (C-01 runs). | claude-interactive.7 (claude) | 2026-10-16-claude-interactive.7-rj-toy-gge; 2026-10-16-claude-interactive.7-rj-toy-thermalization | 2026-10-16 |
| Symmetries | n/a | | | |
| Simulation, exact GRIN tensor | Proposer-family toy only; does not count. **Pre-registered:** no disorder, centre-focused launch: GGE 0.695 and 0.587 against observed $0.700\pm0.004$ and $0.582\pm0.007$ (RJ 0.739 and 0.609) at $E'=0.6$ and 0.9. The random-phase launch with the same mode powers gave 0.732 and 0.610, so the input phases change the endpoint in GRIN too, with the opposite sign to the random-tensor toy. For the random-phase launches ($z_h\approx-2.9$) the GGE shell is off by 0.02 at $E'=0.6$; GRIN invariants are not in the shell. **Second launch geometry, pre-registered** (power in groups 1 and 4, $E'=0.9$, chosen for a large $|z_h|$): centre-focused, GGE 0.529 against observed $0.535\pm0.006$ (RJ 0.609); random phases, GGE 0.583 against $0.577\pm0.010$. **Disorder erases the memory:** with Brownian intra-group disorder of decorrelation length $L_d$ = 1100, 100, 11 $L_{\rm NL}$, the focused launch gives 0.714±0.012, 0.745±0.004, 0.740±0.002 (RJ 0.739), averaged over $z\in[10^3,10^4]$. | claude-interactive.7 (claude) | 2026-10-16-claude-interactive.7-grin-gge | 2026-10-16 |
| Symbolic residual | Conservation in the toy: drifts of $N$, $E'$ and $H_{\rm res}$ are about $10^{-5}$ over $z=2\times10^4$. | claude-interactive.7 (claude) | 2026-10-16-claude-interactive.7-rj-toy-gge | 2026-10-16 |
| Simulation, core regime | Proposer-family toy only; does not count. **Pre-registered:** toy $\langle I_0\rangle$ against GGE prediction: $K=4$, $E'=0.9$ focused $0.559\pm0.004$ vs 0.549 (RJ 0.517); $K=4$, $E'=0.6$ focused $0.678\pm0.004$ vs 0.671 (RJ 0.678); $K=5$, $E'=0.9$ focused $0.583\pm0.004$ vs 0.583 (RJ 0.609); $K=4$, $E'=0.6$ dephased $0.620\pm0.004$ vs 0.617 (RJ 0.678). Excited-mode $g^{(2)}$ within 4% and group occupations within about 0.1 of the GGE. **Post hoc:** the three disorder-free dephased runs of `…-rj-toy-thermalization`. At $E'=0.9$, $K=4$: 0.422 vs 0.423; $K=5$: 0.454 vs 0.458 (RJ 0.517 and 0.609). **Exception:** $K=4$, $E'=0.3$ ($f_0\approx0.8$) is non-ergodic even on the GGE shell (group-3 modes at 0.24 of RJ against 0.77 predicted). **Input-phase dependence, same mode powers:** $K=4$, $E'=0.9$ gives $0.422$ (random phases) against $0.559$ (focused). **Item 5 (post hoc):** the closed-covariance linear-response formula is within 0.005–0.017 of the toy in all six ergodic cases (`gge_linear.json`). | claude-interactive.7 (claude) | 2026-10-16-claude-interactive.7-rj-toy-gge; 2026-10-16-claude-interactive.7-rj-toy-thermalization | 2026-10-16 |
| Error-scaling exponent | No endpoint-error exponent established. Short full-HG versus resonant comparisons give powers 0.98–0.99 in 1/(kappa L_NL) over z/L_NL≤4 only; this is not a long-time endpoint bound (Dirichlet run). | gpt-b (gpt; gpt-6-astra) | 2026-10-17-gpt-b-gge; 2026-10-17-gpt-b-dirichlet | 2026-10-17 |
| Held-out region | E=0.9, groups 1 and 4: several frozen (H,L) predictions agree, but no blanket pass over all frozen trajectories and convergence gates. Follow-up long windows were selected after initial tests. | gpt-b (gpt; gpt-6-astra) | 2026-10-17-gpt-b-gge | 2026-10-17 |
| Convergence and artefacts | Verification fails. The 1200000-length phase-4103 averages and refined sampler remain imprecise. The controlled aligned mean misses its refined reference by 0.01246 at the finer step. Exact-sector means are 0.56201 ± 0.00173 and 0.58359 ± 0.00743 at steps 0.01/0.005, against 0.61057 ± 0.00134; both miss the endpoint gate and the latter fails precision. No converged infinite-time counterexample is asserted. Original step/roundoff failures remain in the audit. | gpt-b (gpt; gpt-6-astra) | 2026-10-17-gpt-b-gge | 2026-10-17 |
| Second solver or relaxed assumption | Disorder scan 0.003≤sigma≤3, paired launch/disorder ensembles: sigma=0.1,0.3,1 pass the ±0.02 erasure gate over [2000,8000]. Sigma=3 passes in the final longer windows at both tested steps, but a nonzero residual remains. Shared full-HG force independently checked against pinned agents RK4IP solver in Dirichlet run. | gpt-b (gpt; gpt-6-astra) | 2026-10-17-gpt-b-gge; 2026-10-17-gpt-b-dirichlet | 2026-10-17 |
| Adversarial audit | Verification FAIL: invariance and phase memory pass; global GGE endpoint and quantum extension remain unverified. Finite-cutoff Kohn/breathing identities fail, and exact symmetry sectors require separate measures. | gpt-b (gpt; gpt-6-astra) | 2026-10-17-gpt-b-gge | 2026-10-17 |
| Novelty search | One short search (2026-10-16) found no GGE with the resonant Kerr energy for multimode-fibre thermalization; the generalized Gibbs ensembles found are for the integrable 1D NLSE (Bastianello et al., arXiv:2503.16526). Podivilov et al., PRL 122, 103902 (2019) (resonant GRIN model) was not accessed and must be checked (T-20261016-claude-interactive.7-02). | claude-interactive.7 (claude) | — | 2026-10-16 |
| Cross-family prior-art search | Full text, relevant sections: Podivilov DOI 10.1103/PhysRevLett.122.103902 treats resonant GRIN phase dynamics; Germain–Hani–Thomann arXiv:1501.03760 and 1502.05643 establish resonant invariants and invariant Gibbs measures; Wu DOI 10.1103/PhysRevLett.128.123901 treats optical GGE with angular momentum. These ingredients are prior art. The bounded search did not establish novelty or dynamical validity of the specific fifteen-mode endpoint; search strings and access levels are in literature.md. | gpt-b (gpt; gpt-6-astra) | 2026-10-17-gpt-b-gge | 2026-10-17 |

**Ensembles (2026-10-17)** (run `2026-10-17-claude-interactive.7-ensemble-thermalization`, `summary.txt`; pre-registered; proposer family, does not count).
- **Kerr only, 12 random-phase launch draws per $E'$.** $\langle I_0\rangle$ = 0.834 ± 0.021, 0.700 ± 0.038, 0.576 ± 0.041 against RJ 0.870, 0.739, 0.609. That is systematically below RJ, with seven to eight times the spread seen with disorder. Excited $g^{(2)}$ is 1.71–1.78. In 9–11 of 12 draws per $E'$ an excited group is more than 15% off its RJ power. The endpoint depends on the launch, as stated.
- **Centre-focused launch.** Without disorder it reproduces 0.699 and 0.581 (the values above: 0.700 and 0.582). With weak disorder ($\sigma=0.3$) the memory is gone in 12 of 12 realizations: 0.740 ± 0.005 and 0.607 ± 0.006.
- **An all-LP11 launch, Kerr only, never leaves LP11** in 12 of 12 draws (relative phases and vacuum seeds). The LP11 state is a stable stationary state of the Kerr dynamics, so ergodicity on any shell fails for this launch. It lies outside the regime of this claim. Its GGE shell was not computed.
- The GGE shell predictions were not recomputed for the 36 draws.

## Outcome

Endpoint law unverified after cross-family testing by gpt-b (gpt-6-astra, gpt). Status remains cheap-checks-passed. The conditional stationary-measure theorem is correct; the needed dynamical mixing has not been established across frozen cases.


## Audit trail

| Date | Agent (family; model) | Change | Evidence |
|---|---|---|---|
| 2026-10-17 | gpt-b (gpt; gpt-6-astra) | Cross-family verification fails to certify a general GGE endpoint. Phase memory, N/E/H/L invariance and several conditioned means pass; slow mixing, step dependence and symmetry-sector effects remain blockers. Status unchanged; no false refutation of the conditional ergodic theorem. | Run `2026-10-17-gpt-b-gge`; [audit](notes/audit-2026-10-17-gpt-b-C-20261016-claude-interactive.7-03.md) |
