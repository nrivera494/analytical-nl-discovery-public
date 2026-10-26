---
id: C-20261016-claude-interactive.7-01
problem: P-20261016-claude-interactive.7-01
title: "Condensed Rayleigh–Jeans light has exact Dirichlet mode statistics: every excited mode has g2 = 2 - 2/M"
type: distribution
status: promoted
proposed_by: claude-interactive.7
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: gpt-b
verifier_family: gpt
verifier_model: gpt-6-astra
audited_by: gpt-b
auditor_family: gpt
auditor_model: gpt-6-astra
created: 2026-10-16
updated: 2026-10-19
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: R-0007
---

## Statement

**Setting.** A multimode fibre of $M$ modes with linear energies $\varepsilon_0=0<\kappa\le\varepsilon_m$ ($m=1,\dots,D$, $D=M-1$), measured from the fundamental. Over the observation, the only conserved quantities of the mode powers $I_p$ are the total power $N=\sum_pI_p$ and the excitation energy $E'=\sum_m\varepsilon_mI_m$. The dynamics is ergodic on that shell.

**Claim.** If $E'\le\kappa N$, the thermalized joint law of the excited-mode powers is exactly
$$x_m=\frac{\varepsilon_mI_m}{E'}\sim{\rm Dirichlet}(1,\dots,1)\ \text{on }D\text{ components},\qquad I_0=N-\sum_mI_m .$$
The bound $E'\le\kappa N$ is condensation in the sense used here: mean excitation energy per photon below the first gap. Consequences:
1. **Equipartition and RJ.** $\langle I_m\rangle=T/\varepsilon_m$ with $T=E'/D$: RJ with $\mu=\varepsilon_0$, exact at any $M$.
2. **Autocorrelation.** $g^{(2)}_m=\langle I_m^2\rangle/\langle I_m\rangle^2=2-2/M$ for every excited mode, independent of $\varepsilon_m$ and $E'$. More generally $g^{(k)}_m=k!\,D^k(D-1)!/(D+k-1)!$.
3. **Cross-correlation.** $g^{(2)}_{mn}=1-1/M$ for excited modes $m\ne n$.
4. **Condensate variance.**
$${\rm Var}\,I_0=\Big(\frac{E'}{D}\Big)^2\frac{DS_2-S_1^2}{D+1}+{\rm Var}_{\rm in}N,\qquad S_k=\sum_{m\ge1}\varepsilon_m^{-k}.$$
   The density of $N_{\rm ex}=N-I_0$ is the B-spline with knots $E'/\varepsilon_m$.
5. **Sign change.** ${\rm Cov}(I_0,I_m)=-\dfrac{E'^2}{\varepsilon_m}\dfrac{D/\varepsilon_m-S_1}{D^2(D+1)}$. It is negative below and positive above the harmonic mean $D/S_1$ of the excitation energies.
6. **GRIN, one polarization, $K$ groups.**
   - $D=K(K+1)/2-1$, $S_1=(K-1+H_{K-1})/\kappa$, $S_2=(H_{K-1}+H^{(2)}_{K-1})/\kappa^2$.
   - ${\rm Var}\,N_{\rm ex}/\langle N_{\rm ex}\rangle^2\to(\ln K+\gamma_E+\pi^2/6-2)/K^2$, with relative corrections $O(\ln K/K)$.

**Quantum reading** ($n_m\gg1$). Take photon numbers $n=I-\frac12$ in symmetric order. These are the photon-number statistics of the reduced states, which are diagonal in the Fock basis with zero mean field. They hold:
- across redrawn input phases, for $z\gg L_{\rm kin}$;
- for a fixed coherent input (shot to shot, or cell to cell in CW) only for $z\gg z_E$.

## Sharpened statement (cross-family, gpt-b, 2026-10-17)

Agent gpt-b, model gpt-6-astra, family gpt. **Sim-verified only for the narrowed
scalar classical statement below.** The original proposer Statement is retained.
For flat complex Liouville measure conditioned on fixed power $N$ and fixed
excitation energy $E'$, a single zero-energy ground mode, and positive gaps
$e_j$, the exact regime is $0<E'/(N\min_j e_j)\le1$. With $D=M-1$,

$$x_j=e_jI_j/E'\sim\operatorname{Dirichlet}(1^D),\qquad
g_j^{(2)}=2-\frac2M,$$
$$\operatorname{Var}I_0=\frac{E'^2(DS_2-S_1^2)}{D^2(D+1)},\qquad
\operatorname{Cov}(I_0,I_j)=-\frac{E'^2(D/e_j-S_1)}{e_jD^2(D+1)},
\quad S_r=\sum_j e_j^{-r}.$$

Here $I_j$ is modal power, $I_0=N-\sum_jI_j$, and
$g_j^{(2)}=\langle I_j^2\rangle/\langle I_j\rangle^2$. The sign changes at
$e_j=D/S_1$. This is an exact measure identity, not an ergodicity theorem.
The original added Var(N) is valid only with sharp E' and condensed support
for every sampled N; general input fluctuations require total covariance.
At E'=0 the excited-mode normalized correlations are undefined.

Independent resonant HG dynamics with full intra-group Hermitian Brownian
coupling supports the listed moments at $\sigma=0.3$, where
$L_d/L_{\rm NL}=\sigma^{-2}=11.1$: core $K=5$ with
$E'/(\kappa N)\in\{0.3,0.6,0.9\}$, held-out $K=4,E'/(\kappa N)=0.45$
and $K=6,E'/(\kappa N)=0.75$, in the window $z/L_{\rm NL}\in[2000,8000]$.
These are discrete tested cases, not a claimed bound on all mixing times.
The original 200-phase fixed-length test fails three mode checks. Its
800-phase enlargement passes, and a fresh frozen 400-phase holdout at
$K=6,E'/(\kappa N)=0.5,z/L_{\rm NL}=8000$ passes every moment/sign gate.
That fresh holdout gives mean excited $g^{(2)}=1.8825\pm0.0133$ against
$40/21$, and a condensate-variance ratio $0.934\pm0.097$ (one disorder-cluster SE).

The exact finite-M correction has measured exponent $1.0017\pm0.0021$ and
coefficient $2.0078\pm0.0123$ in independent simplex sampling. Full versus
resonant dynamics gives error powers 0.98–0.99 for
$0.0125\le(\kappa L_{\rm NL})^{-1}\le0.1$ over $z/L_{\rm NL}\le4$ only.
The stronger $\sigma=3$ moment tests become compatible in a later window,
with broad uncertainty; they do not certify a universal physical-fibre
relaxation length. Every number here is in run `2026-10-17-gpt-b-dirichlet`.

The simulations verify these low-order moments, not convergence of the full
joint phase-space density. The quantum reduced-state reading, vector/spin
corollaries, automatic equilibration, and uniform long-length full-fibre error
are excluded from this status. The solver commit records the independent
full-tensor RK4IP cross-check; production uses the independent C/Python
implementation and hashes in run metadata. No solver files were changed.

See the [audit](notes/audit-2026-10-17-gpt-b-C-20261016-claude-interactive.7-01.md)
and [PI summary](../docs/summary-2026-10-17-gpt-b-C-20261016-claude-interactive.7-01.md).
No new claim is filed. Physical-fibre follow-up: T-20261017-gpt-b-01.

## Regime

The small parameters, each with the order of the error it controls:
- $L_{\rm beat}/L_{\rm NL}=g\bar NS/\kappa\ll1$. The Kerr energy shifts the shell. Error $O(g\bar NS/\kappa)$, or $O$ of the Hartree shift of $\varepsilon_m$, which leaves item 2 unchanged.
- $n_m=T/\varepsilon_m\gg1$ for every excited mode. Quantum (Bose–Einstein) corrections are $O(\varepsilon_m/T)$.
- $E'\le\kappa N$: the exact boundary of the Dirichlet form. Above it the marginals are the B-spline formula of the exploration note, §4.
- $z\gg L_{\rm kin}$ (random-phase ensemble), or $z\gg\max(L_{\rm kin},z_E)$ (fixed coherent input).
- Ergodicity on the $(N,E')$ shell. This needs intra-group disorder that breaks the resonant invariant $H_{\rm res}$ and $L_z$, but is weak. In the toy:
  - decorrelation length $L_d=1/\sigma^2\approx11\,L_{\rm NL}$ works;
  - $L_d\approx L_{\rm NL}$ ($\sigma=1$) leaves the inter-group exchange too slow to equilibrate within $2\times10^4L_{\rm NL}$;
  - with no disorder the endpoint is the generalized Gibbs ensemble of C-20261016-claude-interactive.7-03.

  The order of the non-ergodic correction is not known.

## Assumptions

- Spatial-mode (monochromatic) model; each CW coherence cell is independent; no dispersion or walk-off coupling between cells.
- Scalar field, one polarization, so the fundamental is non-degenerate ($\varepsilon_0=0$ for one mode only). Two polarizations make it two-fold degenerate. If the spin $S_z$ is also conserved (isotropic fibre), integrating out the two condensate components leaves the excitations exactly Dirichlet on $D=M-2$ components, and the condensate's circular polarization fluctuates as the excitations' spin, ${\rm Var}\,S_0=(E'/D)^2DS_2/(D+1)$. If only $N$ and $E'$ are conserved (random birefringence), the excitation law is the Dirichlet tilted by $(N-N_{\rm ex})^{d_0-1}$, with $d_0$ the number of degenerate ground modes. Corrections are $O(N_{\rm ex}/N)$, and the condensate's polarization is uniform on the Poincaré sphere. Derived in the exploration note §4; Monte Carlo check `check_degenerate.py`.
- No Raman, no loss, no gain.
- The only invariants are $N$ and $E'$. Intra-group random coupling breaks $H_{\rm res}$, $L_z$, and the ideal-GRIN Kohn and breathing modes. Inter-group coupling is negligible: otherwise $E'$ itself is not conserved, and the endpoint is the $N$-only Dirichlet law with $g^{(2)}=2M/(M+1)$.
- Weak nonlinearity, so the shell is the linear-energy polytope.
- Classical-field (Wigner) limit with $n\gg1$ in every excited mode.
- The input's $E'$ is sharp. Otherwise mix over its distribution: a coherent input has shot-noise spread; a dephased input has the random-phase spread of the Kerr energy, $O(g\bar NS/\kappa)$ relative.

## Predictions

Fixed before verification:
1. **Toy, core regime (failed; see Checks).** Resonant toy model of `runs/2026-10-16-claude-interactive.7-rj-toy-thermalization`, $K=4$ ($M=10$), intra-group disorder $\sigma=1$, dephased launch, $E'\in\{0.3,0.6,0.9\}$. Expect:
   - mean excited-mode $g^{(2)}=1.800$;
   - mean cross $g^{(2)}=0.900$;
   - $\langle I_0\rangle=1-E'S_1/D$ with $S_1=29/6$ and $D=9$;
   - ${\rm Var}\,I_0$ from item 4.
2. **Toy, held-out size.** $K=5$, $\sigma=1$, $E'=0.6$: $g^{(2)}=1.867$, cross 0.933.
3. **Fibre (held out; the real test).** A solver simulation of a GRIN fibre with real overlaps, $K=6$ groups ($M=21$, one polarization), weak intra-group disorder, and an ensemble of at least 200 random input-phase draws at fixed $(N,E')$ with $E'\le\kappa N$. Expect:
   - $g^{(2)}=2-2/21=1.905$ in every excited mode;
   - cross $g^{(2)}=0.952$;
   - ${\rm Var}\,I_0/\langle N_{\rm ex}\rangle^2$ from the finite-$K$ sums of item 6;
   - the covariance sign change between groups 2 and 3 ($D/S_1=20/(5+H_5)\approx2.75\,\kappa$).
4. **Failure mode.** Without disorder, in the resonant regime, items 1–5 fail. In particular $\langle I_0\rangle$ stays below RJ.

## Derivation

Full text in the exploration note `explorations/2026-10-16-claude-interactive.7-quantum-rj-state.md`, §4.

The steps:
1. In intensity variables the microcanonical measure $\delta(\sum I-N)\,\delta(\sum\varepsilon I-E)\prod d^2A$ is uniform on the polytope, because $d^2A=\frac12dI\,d\phi$.
2. Integrate out $I_0$ with the first delta function. This leaves the region $\{I_m\ge0,\ \sum\varepsilon_mI_m=E',\ \sum I_m\le N\}$.
3. If $E'\le\kappa N$, the last constraint is implied by the energy constraint and drops out.
4. The change of variables $x_m=\varepsilon_mI_m/E'$ has a constant Jacobian, so $x$ is uniform on the simplex.
5. The moments of Dirichlet$(1,\dots,1)$ give items 1–5. Item 6 is the GRIN sum.

The single-component law, Beta$(1,D-1)$, is the textbook energy law of one of $D$ classical oscillators at fixed total energy. The point here is that the condensed RJ state maps exactly onto it: the condensate is a particle reservoir at zero energy cost.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Pass. $g^{(2)}$ is dimensionless; ${\rm Var}\,I_0$ has units of $I^2$, since $E'/\varepsilon$ is a power. | claude-interactive.7 (claude) | — | 2026-10-16 |
| Known limits | Pass. $D\to\infty$ gives the exponential (thermal) law, $g^{(2)}\to2$. $D=1$ gives $g^{(2)}=1$: one excited mode with sharp $E'$ has fixed power. Dropping the energy constraint gives the $N$-only Dirichlet$(1^M)$ law, $g^{(2)}=2M/(M+1)$. | claude-interactive.7 (claude) | — | 2026-10-16 |
| Symmetries | Pass. The $x_m$ are exchangeable, so $g^{(2)}$ and the cross $g^{(2)}$ are mode-independent. | claude-interactive.7 (claude) | — | 2026-10-16 |
| Symbolic residual | Pass. Symbolic Dirichlet moments (sympy). An independent rejection sampler on the full $(N,E')$ polytope ($M=6$, GRIN degeneracy, $E'=0.6\kappa N$) agrees with items 1–5 within Monte Carlo error. | claude-interactive.7 (claude) | 2026-10-16-claude-interactive.7-rj-polytope-mc | 2026-10-16 |
| Simulation, core regime | Proposer-family toy only; does not count. Prediction 1 ($\sigma=1$) FAILED; prediction 2 mixed; the $\sigma=0.3$ and non-condensed cases agree. Details in the toy-model record below. | claude-interactive.7 (claude) | 2026-10-16-claude-interactive.7-rj-toy-thermalization | 2026-10-16 |
| Simulation, cross-family narrowed regime | PASS for exact HG weak-disorder low-order moments across independent launches/disorder, held-out sizes and the fresh fixed-length phase ensemble. Strong-disorder compatibility has broad uncertainty; all original failures retained. | gpt-b (gpt; gpt-6-astra) | 2026-10-17-gpt-b-dirichlet | 2026-10-17 |
| Error-scaling exponent | PASS for the narrowed checks. Finite-M deficit exponent 1.0017 ± 0.0021, fitted coefficient 2.0078 ± 0.0123 versus exact 2. Full/resonant short-length error exponents 0.98–0.99; no uniform long-time normal-form bound. | gpt-b (gpt; gpt-6-astra) | 2026-10-17-gpt-b-dirichlet | 2026-10-17 |
| Held-out region | Held-out time ensembles K=4,6 pass. Original 200-phase K=6 test FAILS three individual g2 checks and is retained. Its 800-phase enlargement passes. Fresh frozen E/(kappa N)=0.5, K=6, 400 phases over eight new disorder realizations passes every moment and resolved-sign gate. | gpt-b (gpt; gpt-6-astra) | 2026-10-17-gpt-b-dirichlet | 2026-10-17 |
| Convergence and artefacts | Central ensemble conclusions survive steps 0.04,0.02,0.01. N/E drifts <4e-7 in the long disorder scans; exact tensor quadrature agrees to <1e-15. Deterministic RK4 converges at fourth order. Temporal window, aliasing and Raman-grid checks do not apply to this spatial model. | gpt-b (gpt; gpt-6-astra) | 2026-10-17-gpt-b-dirichlet | 2026-10-17 |
| Second solver or relaxed assumption | Pinned agents Float64 fixed-step RK4IP agrees with independent full-HG DOP853 to 4.90e-9 at step 0.001. Full nonresonant HG, sigma=3 disorder, noncondensed energy and two-ground-mode measures test relaxed assumptions; only short-length averaging errors are controlled. | gpt-b (gpt; gpt-6-astra) | 2026-10-17-gpt-b-dirichlet | 2026-10-17 |
| Adversarial audit | PASS with reduced regime for the scalar classical measure and listed moments. Original short strong-disorder/200-phase predictions fail. Quantum, vector and uniform full-fibre claims remain unverified; no adjoint counterexample optimization or promotion audit completed. | gpt-b (gpt; gpt-6-astra) | 2026-10-17-gpt-b-dirichlet | 2026-10-17 |
| Novelty search | First-family search only. The finite-$M$ microcanonical means may be in Vardi, Ramos & Kottos, arXiv:2409.01422 (abstract only). The mean condensate fraction law with finite-size sums is known (Aschieri et al. 2011; Baudin et al. 2020). Classical-field condensate distributions are published in the canonical ensemble: Witkowska et al. 2009 (hypoexponential); Bienias et al. 2011 (Monte Carlo, abstract only). The microcanonical Dirichlet/B-spline fluctuation law was not found. The single-oscillator Beta law is textbook. The second-family search is task T-20261016-claude-interactive.7-02. | claude-interactive.7 (claude) | — | 2026-10-16 |

## Toy-model record

Run `2026-10-16-claude-interactive.7-rj-toy-thermalization`, `summary.json`.

**Prediction 1 as registered ($\sigma=1$) FAILED** at all three $E'$. For $E'=0.3,0.6,0.9$, dephased launch:
- $\langle I_0\rangle$ = 0.868, 0.650, 0.557 against 0.839, 0.678, 0.517;
- mean $g^{(2)}$ = 1.74, 1.70, 1.67 against 1.80;
- ${\rm Var}\,I_0$ one third to one quarter of the prediction.

The toy is not ergodic at $\sigma=1$ ($\lambda_1\approx0.002$–$0.005$).
**At $\sigma=0.3$, dephased launch, the same predictions hold** (observed with the $\sigma=1$ runs, so not pre-registered). For $E'=0.3,0.6,0.9$:
- $\langle I_0\rangle$ = 0.838, 0.675, 0.518;
- $g^{(2)}$ = 1.77±0.04, 1.82±0.02, 1.81±0.02;
- cross $g^{(2)}$ = 0.904, 0.899, 0.899;
- ${\rm Var}\,I_0$ within 1.4 block standard errors in all three cases (13%, 24% and 3% high).

The focused launch at $\sigma=0.3$ departs more (maximum group-occupation deviation 0.16–0.29); block averages show slow drifts of similar size.
The regime is narrowed accordingly.
**Prediction 2 ($K=5$, $\sigma=1$, $E'=0.6$), registered: mixed.**
- $\langle I_0\rangle$ 0.750 against 0.739;
- cross $g^{(2)}$ 0.938 against 0.933;
- $g^{(2)}$ $1.825\pm0.011$ against 1.867 (2% low);
- ${\rm Var}\,I_0$ 19% low.

**Non-condensed check (weak disorder, $\sigma=0.3$; B-spline marginals, exploration note §4)**: $E'=1.5$ and $2.0$ match the polytope Monte Carlo for $\langle I_0\rangle$ and $g^{(2)}$ within block errors.

**Held-out size at weak disorder ($K=5$, $\sigma=0.3$, $E'=0.6$; added after prediction 2, so not pre-registered).**
- $\langle I_0\rangle$ $0.744\pm0.012$ against 0.739;
- group occupations within 7% of RJ;
- $g^{(2)}$ $1.923\pm0.019$ against 1.867 (3% high);
- ${\rm Var}\,I_0$ 44% high.

The means pass. The fluctuation statistics at $K=5$ are within a few percent ($g^{(2)}$) to tens of percent (variance). Slow population drifts make these single-trajectory estimates uncertain beyond the quoted block errors. An ensemble over input phases, as in prediction 3, is the better test.

**Exact GRIN Kerr tensor** (run `2026-10-16-claude-interactive.7-grin-lyapunov`). Resonant dynamics of an ideal parabolic GRIN fibre, $K=5$ groups (15 Hermite–Gauss modes), weak intra-group disorder $\sigma=0.3$. Observed after the claim was written, so not pre-registered. Dirichlet value in parentheses where it differs by mode count:

| $E'$ | $\langle I_0\rangle$ (RJ) | $g^{(2)}$ (1.867) | cross (0.933) | ${\rm Var}\,I_0$ / Dirichlet | group occupations / RJ |
|---|---|---|---|---|---|
| 0.3 | 0.867 (0.870) | $1.845\pm0.011$ | 0.935 | 0.95 | 0.96–1.08 |
| 0.6 | 0.735 (0.739) | $1.863\pm0.009$ | 0.934 | 0.97 | 0.97–1.07 |
| 0.9 | 0.611 (0.609) | $1.857\pm0.014$ | 0.934 | 0.93 | 0.97–1.01 |

Without disorder the same fibre is far from these values at $E'=0.3$ and $0.6$ (non-ergodic or GGE). **Launch phases:** at $E'=0.6$ two further random launches (seeds 2, 3; `grin_dirichlet_seeds_summary.txt`) give $\langle I_0\rangle$ 0.740 and 0.736, $g^{(2)}$ 1.873 and 1.852, cross 0.933 and 0.935, and ${\rm Var}\,I_0$ 1.43 and $1.48\times10^{-3}$, against 0.739, 1.867, 0.933 and $1.48\times10^{-3}$.

**Quantum reading, shot to shot** (run `2026-10-16-claude-interactive.7-grin-twa-scrambling`). Truncated-Wigner ensembles of a coherent input, exact GRIN tensor, $E'=0.6$, $\sigma=0.3$, past $z_E$. Across trajectories, the excited-mode relative variance is 0.81–0.84 against $(D-1)/(D+1)=0.867$, and the condensate's is 0.0025–0.0029 against 0.0027, for $n=10^6$–$10^{12}$.

**Random phases redrawn per shot** (run `2026-10-16-claude-interactive.7-grin-shot-statistics`; same fibre and launch powers, 128 shots, $n=10^{10}$; not pre-registered). From $z\approx30L_{\rm NL}$ to 300, the launched excited modes' relative variance is 0.80–0.99 against 0.867, the condensate's is $(2.1$–$3.0)\times10^{-3}$ against $2.71\times10^{-3}$, and $\langle f_0\rangle=0.733$–0.743 against 0.739. With 21 modes ($K=6$, Dirichlet $(D-1)/(D+1)=0.905$, $\langle I_0\rangle=0.7815$, relative variance $1.54\times10^{-3}$), the same ensemble gives 0.80–0.95, 0.78, and $(1.1$–$1.9)\times10^{-3}$ for $z\ge50$ (`summary_K6.txt`). A fixed coherent launch reaches the same values only past $z_E(n/F_{\rm in})$; that is C-02's statement.

**Ensembles over disorder realizations and launches** (run `2026-10-17-claude-interactive.7-ensemble-thermalization`, `summary.txt`; pre-registered in `predictions.md`; proposer family, does not count). Exact GRIN tensor, $K=5$, white intra-group disorder $\sigma=0.3$, 12 disorder seeds and 12 launch draws for each $E'$, window $z\in[1000,4000]L_{\rm NL}$:
- $\langle I_0\rangle$ = 0.869 ± 0.003 / 0.871 ± 0.003, 0.740 ± 0.004 / 0.738 ± 0.005, 0.612 ± 0.007 / 0.610 ± 0.005 (disorder seeds / launch draws) at $E'=0.3$, 0.6, 0.9, against 0.870, 0.739, 0.609.
- Excited $g^{(2)}$ 1.847–1.866 (1.867). ${\rm Var}\,I_0$ / Dirichlet 0.96–1.01 on average, with a realization-to-realization range of 0.72–1.30, about the sampling noise of a variance over one 3000-$L_{\rm NL}$ window.
- The spread across realizations is within twice the single-run sampling error in all six ensembles: the statistics self-average.
- An all-LP11 launch (vacuum-seeded) gives $\langle I_0\rangle$ = 0.565 ± 0.006 against 0.566 in 12 of 12 realizations. Centre-focused launches give 0.740 ± 0.005 and 0.607 ± 0.006.
- Post hoc: the fraction of excited-mode samples above three times their RJ mean is 0.0426–0.0440 against the Dirichlet 0.0435.
- Pre-registered T1 fails in one of four cases: one realization's $g^{(2)}$ is 1.790, against a lower tolerance edge of 1.807.
- Without the intra-group coupling the law does not hold, and the endpoint depends on the launch (see C-03).

## Outcome

Verified as sharpened by gpt-b (gpt-6-astra, gpt). Status: cheap-checks-passed → sim-verified for the explicitly narrowed scalar classical statement only. The original full quantum/dynamical interpretation is not certified.

**Promoted (2026-10-19):** `sim-verified` → `promoted`. The sharpened statement (the exact scalar classical measure identity and its moments at the tested parameters) is the promising result [R-0007](../results/promising/R-0007-condensed-rj-dirichlet-statistics/RESULT.md), under the PI's decision of 2026-10-19 that cross-family verified claims become promising results. Gate G5 is open: gpt-b's report is a cross-family verification, not a clean-context adversarial audit (T-20261019-claude-interactive.16-01). The Statement above is unchanged.

## Audit trail

| Date | Agent (family; model) | Change | Evidence |
|---|---|---|---|
| 2026-10-17 | gpt-b (gpt; gpt-6-astra) | Cross-family verification passes the narrowed scalar classical law. Original finite-length and 200-phase predictions are recorded as failed/refuted at their frozen resolution; E'=0 normalized correlations are undefined. The quantum/vector extensions remain unverified. Original proposer wording retained. | Run `2026-10-17-gpt-b-dirichlet`; [audit](notes/audit-2026-10-17-gpt-b-C-20261016-claude-interactive.7-01.md) |
| 2026-10-19 | claude-interactive.16 (claude; claude-opus-5-5) | `sim-verified` → `promoted`: result R-0007 (promising) written for the sharpened statement. Statement unchanged. G5 open (verification, not a clean-context audit). Record slip found: the auditor fields name gpt-b although no audit was completed (T-20261019-claude-interactive.16-06). | results/promising/R-0007-condensed-rj-dirichlet-statistics; task T-20261019-claude-interactive-09 |
