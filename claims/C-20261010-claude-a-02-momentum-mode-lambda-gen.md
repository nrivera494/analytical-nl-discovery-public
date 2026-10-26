---
id: C-20261010-claude-a-02
problem: P-20261010-claude-interactive-01
title: "The optimal weighted spectral readout of a self-phase-modulated pulse is nearly the photon-number centroid: λ_gen ≤ ⟨ω²⟩_in/⟨ω²⟩_out, tight to 0.81–0.99"
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
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: null
---

## Statement

**Readout.** Bin-resolved photon counting of the output spectrum with real post-detection weights $g(\omega)$. Its best Fano factor is $\lambda_{\rm gen}$, the smallest generalized eigenvalue of $(\Sigma,\mathrm{diag}\,\bar n)$, which equals $\lambda_{\min}(V^{\rm amp})$.

**1. Bound (rigorous within linearized theory).** Assume:
- coherent input;
- dynamics that conserve photon number and momentum: Kerr plus any linear dispersion $\beta(\omega)$, scalar field. Two polarizations with frequency-independent birefringence (no walk-off) also qualify, with $\langle\cdot\rangle$ summed over both polarizations.

The weights $g=\omega-c$ measure the photon-number spectral centroid, whose variance is conserved. Hence
$$\lambda_{\rm gen}\;\le\;\lambda_P\equiv\min_c\frac{\langle(\omega-c)^2\rangle_{\rm in}}{\langle(\omega-c)^2\rangle_{\rm out}},$$
where $\langle\cdot\rangle$ is the photon-weighted average over the classical input and output spectra. It needs only one mean-field propagation.

Dispersionless closed forms, with $I_1=\int(\sqrt p)'^2$ and $I_2=\int p\,p'^2$:
$$\lambda_P=\frac{I_1}{I_1+\Phi^2I_2}=\begin{cases}\big(1+\tfrac{4}{3\sqrt3}\Phi^2\big)^{-1}&\text{Gaussian }p=e^{-t^2/T_0^2}\\[2pt]\big(1+\tfrac{32}{35}\Phi^2\big)^{-1}&\text{sech, }p=\mathrm{sech}^2(t/T_s)\end{cases}$$

**2. Raman (dispersionless, with the thermal reservoir).** Momentum is no longer conserved. The centroid readout still bounds $\lambda_{\rm gen}$:
$$\lambda_{\rm gen}\le\lambda_{P,R}=\frac{I_1+\Phi^2D_R+\tfrac\Phi2f_RS_R}{I_1+\Phi^2I_{2,R}},$$
with
- $I_{2,R}=\int p\,(\hat Rp')^2$;
- $D_R=\int p\,[(\hat R^{\mathsf T}-\hat R)p']^2$;
- $S_R=\int\tfrac{d\omega}{2\pi}\tilde H|\widetilde{p'}|^2$.

For long pulses, with $T_0\gg\tau_{1,2}$ and $\Phi\hbar/(k_BT\,T_0)\ll1$:
$$\lambda_{P,R}\to\lambda_{\rm th}=\frac{I_1+\tfrac\Phi2f_R\tilde H(0)\int p'^2}{I_1+\Phi^2I_2}\;\xrightarrow{\Phi\gg1}\;\frac{f_R\tilde H(0)}{2\Phi}\,\frac{\int p'^2}{I_2}.$$
For the Gaussian at 300 K this is $0.211/\Phi$, with $\int p'^2/I_2=3^{3/2}/2^{3/2}=1.837$.

**Temperature.** $\tilde H(0)\propto T$, so the thermal part of $\lambda_{\rm th}$ is linear in $T$. At $T_0=1$ ps, $\Phi=10$:
- $\lambda_{\rm gen}=0.0119$, 0.0167, 0.0217, 0.0319 at 0, 77, 150, 300 K, which is 0.92–0.95 of $\lambda_{\rm th}$.
- Its excess over 0 K is $6.3$–$6.7\times10^{-5}$ per K, linear in $T$ to 6%. The formula's slope is $6.9\times10^{-5}$ per K (`scan_raman_temperature.json`).

**Raman-model dependence.** The numbers above use Blow–Wood with $f_R=0.18$. Lin–Agrawal-type kernels ($f_R=0.245$, with the Boson-peak term $h_b$, $\tau_b=96$ fs) put more reservoir noise inside the SPM band. At $\Phi=10$ with linear input:
- $T_0=200$ fs, 300 K: $\lambda_{\rm gen}=0.0611$, against 0.0323, a factor 1.9.
- $T_0=1$ ps, 300 K: 0.0373 against 0.0319.
- At 0 K: 0.0170 and 0.0120, against 0.0137 and 0.0119.

The bound $\lambda_{\rm gen}\le$ (grid centroid readout) holds in all 12 rows. Circular input (exact reduction, C-20261010-claude-a-01 item 4) gives $\lambda_{\rm gen}=0.028$ and 0.085 at 200 fs (0 K, 300 K) and 0.021 and 0.064 at 1 ps (`vector_raman_exact.json`).

**3. Tightness (numerical evidence).**
- Kerr: $\lambda_{\rm gen}/\lambda_P\in[0.81,0.996]$ for $1\le\Phi\le40$ (0.988–0.991 at $\Phi=50$), for every bin threshold tested ($10^{-6}$ to $10^{-12}$ of $\max\bar n$). It oscillates with $\Phi$; the largest deficits are at $\Phi=1$ and 7 (0.81 and 0.82).
- At a fixed threshold of $10^{-9}$ the ratio rises: 0.89 ($\Phi=10$), 0.94 (20), 0.96 (30), 0.98 (40).
- Admitting darker bins lowers it slightly. With threshold $10^{-12}$ it is 0.932, 0.952, 0.978 and 0.988 at $\Phi=20$, 30, 40 and 50 (`grid_check2.json`, `open_prediction_phi50.json`).
- So the deficit keeps shrinking at large $\Phi$, roughly as $\Phi^{-1.5}$ to $\Phi^{-2}$ with oscillations. That is consistent with $\lambda_{\rm gen}/\lambda_P\to1$, but no proof or clean exponent is claimed.
- Only $g\propto\omega-c$ cancels the anti-squeezed phase noise. A kink in $g$ at the frequency that maps onto the pulse peak costs $O(\Phi)$: the weights $|\omega|$ and $\omega\Theta(\omega)$ give $F=13.8$ and $6.9$ at $\Phi=10$.

**4. Wasted squeezing.**
- Kerr: $\lambda_{\rm gen}/\lambda_{\min}(V)\to4I_1/I_2$. That is $3\sqrt3=5.20$ (7.2 dB) for the Gaussian, $35/8=4.375$ (6.4 dB) for the sech and 6.84 (8.4 dB) for the flat-top $e^{-t^4}$.
- Thermal Raman regime: the ratio falls to about $\int p'^2/I_2=1.84$ (2.6 dB) against the band-limited $\lambda_{\min}$ of C-20261010-claude-a-01 item 3(b).

**5. Robustness.**
- **Weak dispersion.** The dispersionless $\lambda_{\rm gen}$ holds within 2% for $x=\Phi^2L/L_D\le0.1$, both signs. With dispersion, $\lambda_{\rm gen}/\lambda_P(\beta_2)\in[0.85,0.96]$ for every normal-dispersion point up to $x=3$ and every anomalous point up to $x=0.3$; here $\lambda_P(\beta_2)$ uses the actual output spectrum.
- **Self-steepening.** $\lambda_{\rm gen}$ is even in $s=1/\omega_0T_0$. $|\Delta\lambda_{\rm gen}/\lambda_{\rm gen}|\le2.3\%$ for $\Phi s\le0.1$.
- **Polarization.** Isotropic fibre with linear or circular input reduces to the scalar case with $\Phi_{\rm eff}$ from C-20261010-claude-a-01 item 4.

## Regime

- **Linearization:** $\Phi/\sqrt{N_{\rm ph}}\ll1$.
- **Bins:** fully resolved spectrum. Bins narrower than the inverse time window, all bins with $\bar n>10^{-6}\max\bar n$ kept (convergence checked at $10^{-9}$ and $10^{-12}$).
- **Item 1:** any $\Phi$ and any linear dispersion (rigorous). The tightness of item 3 is asserted only for $L/L_D=0$ and $1\le\Phi\le40$, with bins down to between $10^{-6}$ and $10^{-12}$ of $\max\bar n$.
- **Item 2:** $T_0\in[50,1000]$ fs, $T\in\{0,300\}$ K, $\Phi\in[5,20]$; also 77 and 150 K at $T_0=1$ ps, $\Phi=10$.
  - The bound is rigorous.
  - The long-pulse form is within 7% of $\lambda_{\rm gen}$ for $T_0\ge200$ fs at 300 K.
  - At $T_0=50$ fs, $\lambda_{\rm gen}$ is 0.23–0.75 of $\lambda_{P,R}$. A $\{1,\omega,\omega^2,\omega^3\}$ weight basis is needed there.
- **Item 5:** $x\le0.1$ (both signs), $\Phi s\le0.1$.

## Assumptions

1. Linearized Gaussian noise about the classical mean field. Coherent input.
2. Scalar field, single polarization (except as stated in item 5), single spatial mode.
3. Item 1: momentum- and number-conserving dynamics. This excludes Raman, self-steepening, loss and frequency-dependent $\gamma$.
4. Items 2–4: dispersionless model of C-20261010-claude-a-01 (Blow–Wood $h_R$, $f_R=0.18$, symmetrized $\coth$ reservoir).
5. Unchirped, even input intensity in the closed forms. The general bound needs neither.
6. Ideal detection, no GAWBS.

## Predictions

Frozen in `runs/2026-10-10-claude-a-dispersionless-fano/HELDOUT.md` before computing: commits dc191b0 and ebeb0b7 (sech pulse), 98430d6 ($\beta_3$), 7398320 with its correction 7ea70c7 (thermal formula at a new $T_0$), and 0475fdd (flat-top).

| Held-out case | Prediction | Result | Run |
|---|---|---|---|
| sech, Kerr, $\Phi=5$ | $\lambda_{\rm gen}\in[0.8,1.0]\times0.04192$ | 0.03544 (0.845 $\lambda_P$) | `heldout_results.json` |
| sech, Kerr, $\Phi=15$ | $\in[0.8,1.0]\times0.004838$ | 0.004660 (0.963) | same |
| sech, Raman 300 K, $T_s=188.9$ fs, $\Phi=5$ | $\le\lambda_{P,R}=0.08197$ and $\ge0.04099$ | 0.07440 (0.908) | same |
| sech, Raman 300 K, $\Phi=15$ | $\le0.01941$ and $\ge0.00970$ | 0.01810 (0.933) | same |
| Raman, Blow–Wood, Gaussian $T_0=500$ fs, $\Phi=15$, 150 K and 300 K (frozen at commits 7398320 and 7ea70c7) | $\lambda_{\rm gen}\le\lambda_{P,R}$; $\lambda_{\rm gen}/\lambda_{\rm th}\in[0.88,1.00]$ | 0.982 and 0.985; bound holds | `heldout_thermal.json` |
| Flat-top $e^{-t^4}$, Kerr, $\Phi=5$ and 15 (frozen at commit 0475fdd) | $\lambda_{\rm gen}/\lambda_P\in[0.80,1.00]$, $\lambda_P=0.064008$ and 0.007541 from the 1D integrals | 0.954 and 0.976; grid centroid readout equals $\lambda_P$ to $10^{-4}$ | `heldout_flattop_lamgen.json` |
| Kerr + $\beta_2$ + $\beta_3$ (parity broken), $\Phi=5,10$, $\delta_3=\pm0.01,\pm0.05$ (frozen at commit 98430d6) | $\lambda_{\rm gen}\le\lambda_P(\beta_2,\beta_3)$, ratio in [0.75, 1.0] | all 16 inside; ratio 0.827–0.909; grid centroid readout equals $\lambda_P$ to 2e-05 | `momentum_beta3.json` |

Open predictions:
- For any Kerr + $\beta(\omega)$ fibre and any coherent input, no real-weighted spectral readout is ever found below $\langle\omega^2\rangle_{\rm in}/\langle\omega^2\rangle_{\rm out}$ times $(1-\epsilon)$, where $\epsilon$ is the numerical tolerance. A violation in a converged run refutes item 1.
- Dispersionless Kerr, $\Phi=50$, with bin threshold $10^{-9}$ and time step $\le0.4/\Phi$: $\lambda_{\rm gen}/\lambda_P\in[0.9,1]$. Registered at commit ac94f7e (11:56 EDT).
  - **Tested at 13:04 EDT:** 0.9908 ($dt=0.4/\Phi$), 0.9908 ($0.3/\Phi$), 0.9884 (threshold $10^{-12}$). Passed (`open_prediction_phi50.json`).
  - When registering it I knew the threshold-$10^{-6}$ value at $\Phi=50$ (1.006, unconverged). No converged value existed.

## Derivation

`claims/notes/C-20261010-claude-a-01-derivation.md`, section 3.

**Item 1.**
- Coherent input: $\mathrm{Var}(\sum_\omega g\,n)=\sum g^2\bar n_{\rm in}$ for $g=\omega-c$.
- Under number- and momentum-conserving dynamics that sum is invariant, so its output variance is unchanged. Its shot-noise reference is $\sum g^2\bar n_{\rm out}$.
- $\lambda_{\rm gen}$ is the minimum of this ratio over all real $g$.

**Dispersionless case, directly.** The quadrature noise of the centroid readout is $\int(\sqrt p)'Y_{\rm in}$, plus a term in $X_{\rm in}$ that cancels for Kerr because $K^{\mathsf T}(\sqrt p)'=\bar\phi'\sqrt p$. The Raman case keeps the antisymmetric part $(\hat R^{\mathsf T}-\hat R)p'$ and the reservoir.

**Why only $g\propto\omega$.** By stationary phase, each output frequency $\omega$ comes from instants with $\omega_{\rm inst}(t)=\omega$.
- Cancelling the $O(\Phi)$ anti-squeezed term at each instant requires $g-\omega g'=0$.
- At $\omega=0$ the contributing instant is the peak, which is the brightest and has the largest chirp rate. A kink there acts over a Fresnel zone $|\bar\phi''|^{-1/2}$ and costs $O(\Phi)$.
- The note's earlier statement, that independent slopes on the two sides are allowed, is refuted by `dither_ramp.json` and corrected there.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | ratios of spectral moments; $\tilde H(0)$ dimensionless | claude-a (claude) | — | 2026-10-10 |
| Known limits | $\Phi\to0$: $\lambda_P\to1$. $f_R\to0$: $\lambda_{P,R}\to\lambda_P$. The grid momentum value equals $\lambda_{P,R}$ to 0.3% for $T_0\le200$ fs at $\Phi\le10$, and to 6% on the coarsest grid ($T_0=1$ ps, $dt=40$ fs, $\Phi=20$) | claude-a (claude) | `2026-10-10-claude-a-dispersionless-fano` (`raman_momentum_compare.json`) | 2026-10-10 |
| Symmetries | Parity: $V^{\rm amp}$ commutes with $\omega\to-\omega$ to $3\times10^{-8}$ (Kerr, $\Phi\le40$), and the optimum is odd. Time reversal makes the self-steepening corrections even in $s$ | claude-a (claude) | same (`parity_bound.json`, `scan_selfsteep.json`) | 2026-10-10 |
| Symbolic residual | $I_1,I_2$ closed forms: Gaussian $\sqrt\pi/2$ and $2\sqrt\pi/3^{3/2}$; sech $2/3$ and $64/105$ (hand integration) | claude-a (claude) | — | 2026-10-10 |
| Simulation, core regime | Kerr Gaussian, $\Phi=1,2,3,5,7,10,15,20,30$: $\lambda_{\rm gen}/\lambda_P$ = 0.807, 0.944, 0.974, 0.903, 0.825, 0.894, 0.965, 0.942, 0.985. Raman: $\lambda_{\rm gen}\le\lambda_{P,R}$ in all 18 cases | claude-a (claude) | same (`scan_kerr_gaussian.json`, `raman_momentum_compare.json`) | 2026-10-10 |
| Error-scaling exponent | Not established. $1-\lambda_{\rm gen}/\lambda_P$ oscillates. Over $\Phi$-windows its maximum is 0.18 ($\Phi=2$–11), 0.07 (12–21) and 0.04 (22–30) at threshold $10^{-6}$ (`lam_gen_dense.json`), roughly $1/\Phi$. But the large-$\Phi$ part shifts by 1–3% with the threshold, so no exponent is claimed. On converged bins (threshold $10^{-9}$, `lamgen_deficit.json`) the deficit is 6.2% at $\Phi=20$ and $\le2\%$ for $\Phi=35$–80. It oscillates, with an overall fitted slope of $-1.1$, and levels at about 1.1% for $\Phi=60$–80, where the grid's centroid check drifts by up to 0.4%. So the tail is not resolved | claude-a (claude) | `2026-10-10-claude-a-dispersionless-fano` | 2026-10-10 |
| Held-out region | Sech, Kerr and Raman: all four inside the frozen windows. $\beta_3$: all 16 inside, ratio 0.827–0.909 | claude-a (claude) | same (`heldout_results.json`, `momentum_beta3.json`) | 2026-10-10 |
| Convergence and artefacts | Bin threshold $10^{-6}$ vs $10^{-9}$ of $\max\bar n$: $\lambda_{\rm gen}$ changes by 0.6% ($\Phi=10$) and 0.4% ($\Phi=20$). The grid value of the centroid readout equals the closed-form $\lambda_P$ to $10^{-4}$ at $10^{-9}$, but is 0.6–10% high at $10^{-6}$, because that readout needs the far spectral wings (`grid_check_lamgen.json`, `lam_gen_dense.json`). Time step $dt=0.04$ to $0.01\,T_0$: no change in the fifth digit. Raman ($\Phi=10$, 300 K, `raman_dt_convergence.json`): $\lambda_{\rm gen}$ changes by $<0.04\%$ from $dt=8$ to 2 fs ($T_0=200$ fs) and from 40 to 10 fs (1 ps), so bin-averaged kernels need no $dt\le3$ fs. Padding 4 vs 8: $\lambda_{\rm gen}$ agrees to $10^{-4}$ relative. The bound served as an artefact detector: it was violated only at anomalous $x\ge1$ ($\Phi=10,x=1$: 1.26×; $\Phi=5,x=3$: 38×), where the $dt=0.04$ grid does not resolve higher-order-soliton compression. Those points are excluded | claude-a (claude) | same (`scan_kerr_gaussian.json`, `momentum_dispersion.json`) | 2026-10-10 |
| Second solver or relaxed assumption | Relaxed: dispersion (both signs, independent split-step propagator); self-steepening (canonical photon-flux normalization); polarization; Raman (bound holds, tightness weaker). Two polarizations with linear birefringence of any strength (momentum and number still conserved): $\lambda_{\rm gen}\le\lambda_P^{\rm total}$ at all 9 beat lengths, for both polarization-resolved and polarization-insensitive bins, with ratio 0.89–0.94 (`birefringence_Phi10_45deg.json`). The solver (FastDifferentiableMMNLO, discrete adjoint, subagent claude-a.1) reproduces $\lambda_{\rm gen}$ at $\Phi=5$ to 4–8 digits. $x=0$: 0.044606, and the exact map to $3\times10^{-9}$. $x=0.1$: 0.045480 / 0.043639 for the two signs. $x=1$: 0.050661 / 0.033700. These compare with `lin_ssfm.py` values 0.04461, 0.04548 / 0.04364, 0.05066 / 0.0337. The physical shock term at 1550 nm changes it by $6\times10^{-6}$ | claude-a, claude-a.1 (claude) | same (`scan_dispersion.json`, `momentum_dispersion.json`, `scan_selfsteep.json`, `polarization.json`, `birefringence_Phi10_45deg.json`); `2026-10-10-claude-a-solver-dispersion-check` | 2026-10-10 |
| Cross-check with other lanes (unverified WIP) | claude-b's C-20261010-claude-b-02 (normal dispersion) independently states the same bound. Its pure-SPM limit $1/(1+0.770\Phi^2)$ and $\lambda_{\rm gen}$ 0.25–0.93 dB below it ($\Phi=1$–10) agree with this card. Same family, so this is not a verification | claude-a (claude) | branch T-20261010-claude-interactive-05 (8908a17) | 2026-10-10 |
| Adversarial audit | not done | | | |
| Novelty search | Subagent claude-a.2; search strings in the log entry. Not found: a centroid or momentum bound on the optimal weighted spectral readout, the bandwidth-ratio form, or its tightness for SPM (one search in extended mode). Known: linearized soliton theory conserves photon number and momentum (Haus & Lai, JOSA B 7, 386 (1990), abstract only; Levandovsky, Vasilyev & Kumar, OL 24, 43 (1999), full text). Levandovsky et al. argue the optimal passive soliton filter is even in $\omega$. "Momentum squeezing" by an interferometer: Werner, PRL 81, 4132 (1998). Haus & Lai 1990 should still be read in full | claude-a.2, claude-a (claude) | — | 2026-10-10 |

## Outcome

Open.
