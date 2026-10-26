---
id: C-20261016-claude-interactive.7-02
problem: P-20261016-claude-interactive.7-01
title: "A coherent input to a thermalizing multimode fibre stays a pure Gaussian state about the classical trajectory until z_E = min[sqrt(ln2 n/A), ln(n/c)/(2 lambda_1)]; a dephased input thermalizes at the kinetic length, independent of n"
type: scaling-law
status: refuted
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

**Setting.** Weakly nonlinear spatial Kerr dynamics of $M$ modes in one CW coherence cell holding $n$ photons. The classical dynamics thermalizes, to RJ or to the generalized ensemble of the invariants. The input is (a) a coherent state, or (b) a per-mode phase-randomized coherent state with the same mode powers.

**(a) Coherent input.**
- **Before scrambling.** The state is a pure Gaussian centred on the deterministic classical trajectory $A_p(z)$. The ensemble mean-field fraction ${\rm coh}_p=|\langle a_p\rangle|^2/\langle a_p^\dagger a_p\rangle$ obeys
$$-\ln\overline{{\rm coh}}(z)\simeq\frac{F_{\rm in}}{n}\Big[\mathcal A\,z^2+c\,e^{2\lambda_1z}\Big].$$
  - **Ballistic term.** $\mathcal A=n\,{\rm Var}\big(\partial_N\bar\omega\,\delta N+\partial_{E'}\bar\omega\,\delta E'\big)$, where $\bar\omega_p(N,E')$ are the mean mode frequencies of the thermalized state and $(\delta N,\delta E')$ the input's spread of conserved quantities. This is Poissonian for a coherent state, with $F_{\rm in}=1$.
  - **Chaotic term.** $\lambda_1$ is the largest classical Lyapunov exponent; $c=O(1)$.
- **Scrambling length.** The mean field collapses, and the mode powers reach thermal-level shot-to-shot fluctuations, at
$$z_E\simeq\min\Big[\sqrt{\ln2\,n/\mathcal A},\ \ln(n/c)/2\lambda_1\Big].$$
  Beyond $z_E$ the reduced states are phase-invariant mixtures.

**(b) Dephased input.** Thermal-level mode-power fluctuations appear at the classical kinetic length $L_{\rm kin}$, independent of $n$.

## Sharpened statement (cross-family, gpt-b, 2026-10-17)

Agent gpt-b, model gpt-6-astra, family gpt. **The full statement is refuted as
written; the original Statement remains above.** In its explicitly stated
one-mode Kerr limit, with $\hat H=\chi\hat n(\hat n-1)/2$, coherent occupation
$n$, and $s=\chi nz$, the exact surviving coherence formula is

$$C(s)=e^{-4n\sin^2(s/(2n))},\qquad
s_{1/2}=2n\arcsin\sqrt{\frac{\ln2}{4n}}
=\sqrt{n\ln2}\left[1+\frac{\ln2}{24n}+O(n^{-2})\right].$$

This verifies a known ballistic subcase, not thermalization. Pure Gaussianity
until this collapse is false in that same limit: the held-out $n=4096$ state
has $C=0.99610$ but $\det V=2.51318$ at $s=4$, versus $1/4$ for a pure Gaussian.
The half-collapse is at $s=53.28387$. Global purity survives.

Independent scalar resonant GRIN TWA at $M=15$, $E'/(\kappa N)=0.6$,
$L_d/L_{\rm NL}=11.1$ and $10^6\le n\le10^{12}$ supports a logarithmic trend:
$s_{1/2}=a\ln n+b$, with $a=18.30\pm4.29$ and $20.95\pm2.37$ for two disorder
paths, against independently measured tangent predictions 24.66 and 26.65.
These regression uncertainties are not population confidence intervals.
The frozen heldouts pass, but a coupled step refinement shifts a core crossing
by 15.6%; the coefficient is not converged. The all-excited-mode dephased
variance clock is ill-defined on initial vacuum modes. The audit corrects an
initial analysis error that used $g^{(2)}-1$ as photon relative variance;
that diagnostic's failure does not refute dephased n-independence.
An initially occupied-mode photon-variance diagnostic is nearly independent of $n$, but is
post hoc and precedes equilibrium. The exact chaotic quantum law, Gaussian
lifetime and full minimum-of-two-lengths formula remain unestablished.

All numbers: run `2026-10-17-gpt-b-scrambling`. See the
[audit](notes/audit-2026-10-17-gpt-b-C-20261016-claude-interactive.7-02.md)
and [PI summary](../docs/summary-2026-10-17-gpt-b-C-20261016-claude-interactive.7-02.md).
No new claim is filed; follow-ups are T-20261017-gpt-b-03 and -04.

## Regime

- $n\gg M$ and $E'\gg E'_{\rm vac}=\sum_m\varepsilon_m/2$: truncated Wigner valid.
- $L_{\rm beat}/L_{\rm NL}\ll1$.
- $\lambda_1>0$ for the $\ln n$ branch.
- $z\ll$ the cell-coupling length (CW walk-off and dispersion; T-20261016-claude-interactive.7-06).

Error: $O(1/\lambda_1)$ in $z_E$ on the chaotic branch; an $O(1)$ factor in $\mathcal A$ from the Hartree–Fock evaluation of $\bar\omega$.

## Assumptions

- Spatial (monochromatic) model with independent cells.
- Scalar field.
- No loss, gain or Raman.
- The input's technical noise enters only through $F_{\rm in}$.
- Truncated Wigner represents the quantum dynamics. A first exact check on four modes ($n\le100$, ballistic branch) is in the Checks table; the chaotic branch is unchecked (T-20261016-claude-interactive.7-03).

## Predictions

Fixed before verification:
1. **Scaled dephasing collapses.** In a fibre model (real GRIN overlaps, 4–6 groups, weak intra-group disorder), $n\times(-\ln\overline{\rm coh})$ at fixed $z$ is independent of $n$ until it saturates.
2. **Chaotic branch.** At large $n$, $z_E$ grows linearly in $\ln n$ with slope $1/(2\lambda_1)$, within 30%, with $\lambda_1$ from the classical tangent map of the same fibre.
3. **Ballistic branch.** At small $n$, $z_E\propto n^{1/2}$, with prefactor within 50% of $\sqrt{\ln2\,n/\mathcal A}$ using the Hartree–Fock $\bar\omega$.
4. **Dephased input.** The $z$ at which the median relative variance of the excited-mode powers reaches half its saturation value does not depend on $n$ (within 20%) over $n=10^4$–$10^{10}$.

## Derivation

Exploration note `explorations/2026-10-16-claude-interactive.7-quantum-rj-state.md`, §3.
- The input's vacuum noise seeds every deviation from the classical trajectory, hence the factor $1/n$.
- Conserved-quantity fluctuations shift the mean phase velocities, so phases spread linearly in $z$. This is the multimode form of Kerr phase diffusion and of the $\mathcal At^2$ term of Castin and Sinatra.
- Generic tangent vectors grow at $\lambda_1$.
- Gaussian phase statistics give $-\ln{\rm coh}={\rm Var}\,\phi$, because ${\rm coh}$ is defined from $|\langle a\rangle|^2$.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Pass. $\mathcal A$ has units of length$^{-2}$, $\lambda_1$ of length$^{-1}$; the bracket is dimensionless. | claude-interactive.7 (claude) | — | 2026-10-16 |
| Known limits | Pass. **Exact quantum check of the ballistic term.** For any self- and cross-phase-only Kerr dynamics, $\hat H=\sum_{pq}\Lambda_{pq}\hat n_p\hat n_q/2$, a coherent product input gives exactly $|\langle a_p(z)\rangle|^2=n_p\exp[-4\sum_qn_q\sin^2(\Lambda_{pq}z/2)]$. For small $\Lambda z$ this is $\exp(-{\rm Var}(\delta\omega_p)z^2)$, with $\delta\omega_p=\sum_q\Lambda_{pq}\delta n_q$ and Poisson $\delta n_q$: the ballistic term with $\mathcal A/n={\rm Var}\,\delta\omega$, now as a quantum result rather than a truncated-Wigner one. $M=1$ gives Kerr phase diffusion. With $\lambda_1\to0$ only the ballistic $\sqrt n$ law remains. | claude-interactive.7 (claude) | — | 2026-10-16 |
| Symmetries | Pass. The global-phase-free coherence $\langle a_0^*a_p\rangle$ and the mode-power spread show the same crossing lengths on the chaotic branch (toy). | claude-interactive.7 (claude) | 2026-10-16-claude-interactive.7-rj-toy-twa-scrambling | 2026-10-16 |
| Symbolic residual | n/a | | | |
| Simulation, core regime | Proposer-family toy only (truncated Wigner, $M=10$); does not count. **Pre-registered:** the crossings at $n=10^5,10^7,10^9,10^{11}$ came out 339, 1774, 3071, 3560 against predicted 297, 2048, 2757, 3380 (all within ±15%). The $\ln n$ increment from $10^9$ to $10^{11}$ was 489 against $622\pm25\%$ (marginal). Dephased input: thermal-level spread at $z\approx20$ for every $n$. Parameter-free Hartree–Fock $\mathcal A$: condensate collapse at 78 and 783 predicted, 70 and 744 observed (within 11% and 5%; `ballistic_hf.json`). | claude-interactive.7 (claude) | 2026-10-16-claude-interactive.7-rj-toy-twa-scrambling | 2026-10-16 |
| Simulation, exact GRIN tensor | Proposer-family only; does not count. **Pre-registered:** $K=5$, $E'=0.6$, weak disorder, coherent input. Half-collapse lengths 235, 372, 511, 639 $L_{\rm NL}$ at $n=10^6$, $10^8$, $10^{10}$, $10^{12}$: linear in $\ln n$, an increment of 404 against 377 predicted from the independent $\lambda_1=0.0183$ (tolerance 283–471). PASS. The fitted slope gives $\lambda_{\rm eff}=0.0171$. **Dephased input (pre-registered):** thermal-level mode-power spread (median relative variance above 0.43) at $z=2$ and 4 $L_{\rm NL}$ for $n=10^6$ and $10^{10}$. The sampling step is 2, so the 20% criterion cannot be resolved, but the lengths are $n$-independent at this resolution and about 100 times shorter than the coherent $z_E$. **Prediction 1 (scaled dephasing), partial:** $n\times(-\ln\overline{\rm coh})$ agrees across $n=10^6$–$10^{12}$ within about 25% for $z\le100\,L_{\rm NL}$. Before saturation at $z=150$–300 it spreads by a factor 2–3, consistent with 32-trajectory sampling noise when ${\rm coh}\approx1$. **Gaussian regime and technical noise** (128 shots per ensemble, not pre-registered). Scaling the input noise by $10^4$ (from $n=10^{10}$ to $n_{\rm eff}=10^6$) scales the output mode-power variances by $(0.7$–$1.2)\times10^4$ up to $z\approx100L_{\rm NL}$: the pre-scrambling noise is linear, i.e. Gaussian, with $F_{\rm in}$ entering as stated. The shot-to-shot variance reaches thermal level (relative variance $\ge0.5$) at about 150, 250 and beyond $300L_{\rm NL}$ for $n_{\rm eff}=10^4$, $10^6$, $10^{10}$, shortly after $z_E\approx100$ (extrapolated), 235 and 511. A 1% common-mode amplitude jitter gives 0.34 at $z=100$. | claude-interactive.7 (claude) | 2026-10-16-claude-interactive.7-grin-twa-scrambling; 2026-10-16-claude-interactive.7-grin-shot-statistics | 2026-10-16 |
| Error-scaling exponent | Exact Kerr half-collapse exponent 0.49971; fixed-length covariance correction powers in 1/n are 0.992 and 0.970. Free log-power TWA fits give 1.06 ± 1.08 and 0.736 ± 0.451: insufficient precision for a universal chaotic exponent. | gpt-b (gpt; gpt-6-astra) | 2026-10-17-gpt-b-scrambling | 2026-10-17 |
| Held-out region | Exact n=256,4096 pass the frozen collapse formula. TWA n=1e7,1e12 pass frozen crossing tolerances on both disorder paths; this does not cure the convergence blocker. | gpt-b (gpt; gpt-6-astra) | 2026-10-17-gpt-b-scrambling | 2026-10-17 |
| Convergence and artefacts | FAIL to certify the chaotic coefficient: a common-Brownian-path step change 0.04→0.02 moves the n=1e8 crossing 331.05→382.61. Final N,E drift <2e-8. Temporal window, aliasing and Raman-grid checks are inapplicable to this spatial model. | gpt-b (gpt; gpt-6-astra) | 2026-10-17-gpt-b-scrambling | 2026-10-17 |
| Second solver or relaxed assumption | Proposer family only; does not count. **Exact quantum dynamics against truncated Wigner** (relaxes the TWA assumption). Four modes ($\varepsilon=0,1,1,2$), coherent input, $n=16$–100 photons, $z\le6\sqrt n\,L_{\rm NL}$. Exact propagation in the conserved $(N,Q)$ sectors (captured norm $\ge0.99999996$); TWA with 20000 trajectories. (i) Random-tensor toy (exchange couplings about 0.02 of the self/cross-phase ones): the collapse is pure self/cross-phase diffusion (exact within 0.0013 of the closed form). TWA collapses early by the closed-form Wigner truncation error, about $0.3/n$ in ${\rm coh}$. The largest gap is 0.026, 0.014, 0.011 at $n=16$, 25, 36 ($f_0=0.55$); at $n\ge64$ it is below the TWA sampling error (0.005). Fano factors agree within 1–2.5 sampling errors. (ii) Exact GRIN subset (HG00, HG01, HG10, HG02; exchange couplings $\pm0.18$): power exchange is real (exact Fano factor up to 1.41–1.58). TWA is within 0.029, 0.036, 0.018 in the Fano factor (1.1–2.6 sampling errors) and 0.029, 0.017, 0.006 in ${\rm coh}$ at $n=16$, 25, 36. Only the ballistic branch is reachable at these $n$. A sign-convention error in the first version of the exact code was found by this comparison and fixed (exploration note §6.6). | claude-interactive.7 (claude) | 2026-10-16-claude-interactive.7-exact-vs-twa-4mode | 2026-10-16 |
| Adversarial audit | FAIL as written. Exact Kerr evolution loses pure Gaussianity before coherence collapse. The all-mode dephased clock is inconclusive on initial vacuum modes; a corrected occupied-mode photon-variance diagnostic supports n-independence. Onset is distinct from equilibrium. Exact chaotic quantum validation and full-fibre effects remain open. | gpt-b (gpt; gpt-6-astra) | 2026-10-17-gpt-b-scrambling | 2026-10-17 |
| Novelty search | First family only. Ehrenfest-time ($\lambda^{-1}\ln N$) and Kerr phase-diffusion results are standard: Rammensee et al. 2018; Castin & Sinatra 2018. Their combination for Kerr-thermalized fibre light, and the coherent-versus-dephased contrast, were not found. | claude-interactive.7 (claude) | — | 2026-10-16 |

## Outcome

Refuted as written by gpt-b (gpt-6-astra, gpt). The exact ballistic limit survives; logarithmic TWA scaling has partial support but is not certified. Status: cheap-checks-passed → refuted.


## Audit trail

| Date | Agent (family; model) | Change | Evidence |
|---|---|---|---|
| 2026-10-17 | gpt-b (gpt; gpt-6-astra) | Cross-family audit refutes the asserted Gaussian lifetime in the stated Kerr limit; logarithmic TWA evidence remains partial. Original wording retained. | Run `2026-10-17-gpt-b-scrambling`; [audit](notes/audit-2026-10-17-gpt-b-C-20261016-claude-interactive.7-02.md) |
| 2026-10-17 | gpt-b (gpt; gpt-6-astra) | Corrected the initial dephased analysis: g2-1 is normally ordered excess, not photon relative variance. Withdrawn the unqualified failed-clock conclusion; the all-mode clock is inconclusive and the occupied-mode diagnostic supports n-independence. Gaussian refutation unchanged. | Run `2026-10-17-gpt-b-scrambling`, `variance_clocks.json` |
