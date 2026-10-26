---
id: C-20261016-claude-b-01
problem: P-20261016-claude-interactive-01
title: "TOD-only fission-burst dispersive-wave yield: ln(eta_DW) = -d_*/delta3 + p ln(delta3) + c, with d_* the narrowest analyticity strip of the unperturbed NLSE evolution (0.3747 for the N=2 sech, against the ejected-soliton strip value pi/(2(2N-1)) = 0.5236)"
type: asymptotic-solution
status: refuted
proposed_by: claude-b
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: gpt-a
verifier_family: gpt
audited_by: gpt-a
auditor_family: gpt
created: 2026-10-16
updated: 2026-10-16
solver_commit: null
result: null
---

## Statement

**System.** A transform-limited pulse is launched into a lossless fibre with anomalous dispersion and third-order dispersion. The model is Roy, Bhadra and Agrawal (2009), Eqs. 1–2:
$$iu_\xi+\tfrac12u_{\tau\tau}+N^2|u|^2u=i\delta_3u_{\tau\tau\tau},\qquad \delta_3=\frac{\beta_3}{6|\beta_2|T_0},\qquad u(0,\tau)=u_{\rm in}(\tau).$$
Here $u_{\rm in}$ is $\mathrm{sech}\,\tau$ or $e^{-\tau^2/2}$. The Fourier convention is $u=\frac1{2\pi}\int\hat ue^{-iw\tau}dw$, with $w=(\omega-\omega_0)T_0$.

**Definitions.**
- $u_0(\xi,\tau)$ is the $\delta_3=0$ NLSE solution from the same launch.
- $d(\xi)$ is the width of its analyticity strip in complex $\tau$: the distance from the real axis to the nearest singularity. Equivalently, it is the exponential decay rate of $|\hat u_0(\xi,w)|$ as $w\to\infty$.
- $d_*=\min_{0\le\xi\le\xi_f}d(\xi)$.
- $\eta_{\rm DW}$ is the fraction of launched photons found at $w\ge w_z=1/(6\delta_3)$ at $\xi_f$, after removing the field within $|\tau|<15$ with a smooth gate (tanh edges, width 1).
  - In the tested regime (exponentially small yields), the solitons stay near $\tau=0$. Widening the gate to 20 changes $\eta_{\rm DW}$ by less than $10^{-4}$ relative.
  - In the large-yield regime the solitons recoil and drift, so this fixed gate is not a valid DW measure there (see C-20261016-claude-b-02).

**Claim.** As $\delta_3\to0$ at fixed launch, $N$ and $\xi_f$,
$$\ln\eta_{\rm DW}=-\frac{d_*}{\delta_3}+p\ln\delta_3+c+o(1),\qquad\text{so}\quad \lim_{\delta_3\to0}\delta_3\ln\eta_{\rm DW}=-d_*.$$
The prefactor exponent $p$ is measured at $-2.9$ to $-3.4$ for the launches tested.

**Exact anchor.** For the $N=2$ sech launch, the Satsuma–Yajima breather has poles at $\cosh2\tau=\sqrt3|\sin2\xi|-1$. Hence
$$d(\xi)=\tfrac12\arccos(\sqrt3|\sin2\xi|-1),\qquad d_*=\tfrac12\arccos(\sqrt3-1)=0.374664\ \ (\xi_*=\pi/4).$$

**Relation to Roy, Bhadra and Agrawal (2009).**

*What Eq. 6 is.*
- A perturbative estimate of the NSR **spectral-peak level** $p_d=P_d/P_0$, not an integrated yield.
- It applies the Akhmediev–Karlsson single-soliton result to the shortest ejected soliton, of amplitude $\eta=2N-1$. Its exponent $\pi/(2(2N-1)\delta_3)$ is $2w_{\rm DW}$ times the ejected-soliton strip value $\pi/(2\eta)$.
- Its stated validity is $(2N-1)\delta_3\ll1$, and Roy et al. call it doubtful near −15 dB.

*How Roy et al. validated it.* Against simulations of their full model: Raman with $f_R=0.245$ and a two-component response, plus self-steepening; sech launch, $T_0=50$ fs, $\xi=4$.
- In their Fig. 3(b) the Eq. 6 line "falls quite close" to the full-model data.
- In Fig. 4(b) it agrees well at $\delta_3=0.02$ and reasonably at 0.03 up to $N=3$, and it breaks down for $(2N-1)\delta_3\gtrsim0.15$.

*What they reported about the TOD-only case.* Eq. 6 "deviates considerably" from their data without Raman (Fig. 3b), and Raman lowers the NSR peak by more than 25 dB at $\delta_3=0.02$ (Fig. 2b).

**This claim concerns the TOD-only model and explains that known TOD-only gap.** The compression burst has a narrower strip than the ejected soliton, $d_*<\pi/(2(2N-1))$, so without Raman the burst dominates. The law gives the exponent of the gap as $\delta_3\to0$: $\ln$ of the ratio grows as $[\pi/(2(2N-1))-d_*]/\delta_3$.
- At $N=2$ the strip values are 0.3747 against 0.5236; at $N=3$, 0.1997 against 0.3142.
- **The gap depends strongly on $\delta_3$.** At $N=2$ the TOD-only NSR peak exceeds Eq. 6 by 39.5, 12.8 and −0.4 dB at $\delta_3=0.02$, 0.03 and 0.04 (run 2026-10-16-claude-b-dw-oracle, `summary.json`, `roy_reproduction`). The 40 dB figure is the largest of these, not a typical value.
- **The asymptotic tests lie below Roy et al.'s visibility floor.** The four-point fits ($d_*/\delta_3\gtrsim30$) use integrated yields of $7\times10^{-15}$ to $4\times10^{-9}$ (`yield_g4.json`, `yield_g3.json`, `yield_sech2a.json`, `yield_s3.json`). Their DW spectral peaks lie at or below the −80 dB level Roy et al. take as the threshold for a visible NSR peak:
  - −81 to −128 dB for the Gaussian $N=3$ at $\delta_3=0.0058$–0.0043 (run 2026-10-16-claude-b-dw-oracle, `yield_g3.json`);
  - −92 dB for the sech $N=2$ at $\delta_3=0.010$ (run 2026-10-16-claude-b.7-solver-dwyield).

**With Raman.** Model M1 adds a causal Raman response: $f_R=0.18$, the single-damped-oscillator response with $\tau_1=12.2$ fs and $\tau_2=32$ fs, at $T_0=50$ fs, with no self-steepening. The same law holds with $d_*$ replaced by $d_*^{M1}$, the narrowest blue-side strip of the **Raman-including, TOD-free** evolution.
- Sech $N=2$: $d_*^{M1}=0.4410$.
- Gaussian $N=3$: $d_*^{M1}=0.2346$.

Raman blunts the compression, which widens the strip and lowers the TOD-only burst yield by orders of magnitude.

**Not done:** a comparison with Roy et al.'s own full model ($f_R=0.245$, two-component Raman response, self-steepening). M1 here uses $f_R=0.18$ with the single-damped-oscillator response and no self-steepening. The GPT-family verification (T-20261016-claude-b-01) is to run that comparison.

**Corollary (descriptive, card regime).** For transform-limited Gaussians with $N=3$–8 and $\delta_3=0.01$–0.05, the band yield at $\xi=2$ is a single function of $x=d_*(N)/\delta_3$, with $d_*$ the minimum over $\xi\le2$. This holds even where the yield is not exponentially small (0.0009–0.32).
- Values: $d_*=0.1922$, 0.1191, 0.0725 and 0.0572 for $N=3$, 4, 6 and 8.
- The curve $F(x)$: 0.32 at $x=1.2$; 0.24 at 2; 0.17 at 3.7; 0.11 at 6; 0.052 at 9.6; 0.018 at 11.9; $8.9\times10^{-4}$ at 19.2.
- Spread: median $|\Delta\ln\eta|=0.087$, maximum 0.21. Against Roy's variable $(2N-1)\delta_3$ the spread is 0.117 and 0.68.
- $d_*(5)$, $d_*(6)$ and $d_*(8)$ were predicted from the collapse before being computed (A9, commit f2bcc34) and landed within tolerance: −11%, −9% and +8%.
- The collapse is for **transform-limited** launches. It does not extend to shaped launches at large yield: optimised masks raise $\eta_B$ 1.5× while *increasing* $d_*$ (A10, refuted; see C-20261016-claude-b-02).

The yield is set by the **sharpest compression before the fibre end**. When a non-integrable launch recompresses more sharply later, the exponent changes with fibre length. For the Gaussian at $N=3$, $d=0.2015$ at the first compression ($\xi=0.357$) and $0.1923$ at the second ($\xi=1.103$).

## Regime

The literal small-TOD statement for the fixed gate is **refuted**. The following bounds describe the surviving numerical evidence, rather than restoring the asserted zero-TOD limit.

- The independently supported finite range is approximately $30\le d_*/\delta_3\le48$ for the specified M0 launches: sech $N=2$ at $\xi_f=2,4$, sech $N=3$ at $\xi_f=2$, Gaussian $N=3$ at $\xi_f=1,2$, and Gaussian $N=4$ at $\xi_f=1$. These are tested cases and endpoints, not a uniform theorem over arbitrary launches or lengths (runs 2026-10-16-gpt-a-dw-law, 2026-10-16-gpt-a-dw-heldout, 2026-10-16-gpt-a-dw-followup).
- M0 retains its stated scalar, lossless, cubic-dispersion, zero-Raman and zero-shock assumptions. The Raman verification covers the frozen M1 Gaussian $N=3$, $\xi_f=2$ grid, approximately $32\le d_*^{M1}/\delta_3\le43$ (runs 2026-10-16-gpt-a-dw-heldout-strips and 2026-10-16-gpt-a-dw-heldout). Roy's full model is a separate numerical extension in the new Checks.
- Radiation isolation requires a measured gate/band stability check. Clearance of a leading ray alone is insufficient. In the original finite-range tests, widening the gate from 15 to 20 is stable; for the new Gaussian $N=3.5$ launch it changes some yields by up to 5.08%, although its exponent still passes (run 2026-10-16-gpt-a-dw-heldout).
- A full-TOD counterexample to the fixed-gate isolation premise occurs already for sech $N=2$, $\xi_f=2.25$, $\delta_3=0.003$: the minimum at $\pi/4$ is unique, the leading ray clears the gate, and the normal-band integral is dominated by core leakage. Step, window and paired finer-grid controls (the grid pair uses a matched coarser step) are recorded in run 2026-10-16-gpt-a-dw-highprecision.
- Sech $N=4$ remains excluded. Longer $N=2$ fibres retain the tested exponent but require renewed measurement checks for later bursts (runs 2026-10-16-gpt-a-dw-heldout and 2026-10-16-gpt-a-dw-length). No general optimized ceiling follows from these checks.

## Assumptions

1. Scalar, single-mode, lossless fibre. The dispersion is exactly cubic ($\beta_4=0$) and the nonlinearity is instantaneous Kerr.
2. No self-steepening; photon number equals $\int|u|^2$. In the core statement there is no Raman response. With Raman (model M1), the same law holds once $d_*$ is computed from the Raman-including TOD-free evolution; see Checks and run 2026-10-16-claude-b-dw-oracle (`h4_*`).
3. Transform-limited, real, even launches, whose $\delta_3=0$ singularities lie on the imaginary axis (checked: pure exponential tails, residual rms $10^{-4}$).
4. The DW photons are those at $w\ge w_z$ outside the gate $|\tau|<15$. Soliton spectral tails are excluded by the gate.
5. Leading-order heuristics: first-order perturbation in $\delta_3$, and Laplace's method in $\xi$ around $\xi_*$. The prefactor is not derived.

## Predictions

These were frozen before the corresponding runs in `explorations/2026-10-16-claude-b-dw-yield-hypotheses.md`: H2b in commit d1b7f71, A1 in 85637bb, A2 in b9067fa, A4 in 3a852dc.

- **P1 (sech $N=2$, construction set).** The extrapolated exponent from a four-point fit, $\ln\eta=c+p\ln\delta_3-d/\delta_3$ at the smallest $\delta_3$, is within 4% of 0.37466. Roy's 0.5236 is excluded.
- **P2 (held out, sech $N=3$).** The fitted $d$ is within 4% of 0.1997, computed before the run. The value 0.3142 is excluded.
- **P3 (held out, Gaussian $N=4$, $\xi_f=1$).** The fitted $d$ is within 4% of 0.1322, computed before the run.
- **P4 (Gaussian $N=3$, $\xi_f=2$).** The fitted $d$ is within 4% of $d_*$. A1 recorded $d_*=0.2015$ from a scan truncated at $\xi=1$. The full-length value is 0.1923 (see Outcome).
- **P5 (length test, frozen in A4).** The Gaussian $N=3$ with $\xi_f=1.0$ gives a fitted $d$ within 2% of 0.2015, and at least 2.5% above the $\xi_f=2$ fit.
- **P6 (Raman held out, frozen in A5, commit 6281a3b).** Gaussian $N=3$ in M1, $\xi_f=2$, $\delta_3\in\{0.0055,0.006,0.0066,0.0073\}$. The fitted $d$ is within 4% of $d_*^{M1}=0.2346$ and more than 10% above the M0 fit.
- **P8 (held out, sech $N=4$, frozen in A11).** The A1 four-point fit over $\delta_3\in\{0.0029,0.0032,0.0035,0.0039\}$ gives $d$ within 4% of 0.1342.
- **P7 (shaping acts through $d_*$; frozen in A3, A6 and A7).** The yield ratio of a shaped launch to TL is $\exp(-[d_*^{\rm shaped}-d_*^{\rm TL}]/\delta_3)$ to leading order. Outcomes are in the Checks table and in C-20261016-claude-b-02.
- *Note on wording (added after PI review; the frozen predictions are unchanged).* In P1 and P2, "Roy's 0.5236" and "0.3142" mean the exponent of Roy et al.'s Eq. 6, i.e. the ejected-soliton strip value $\pi/(2(2N-1))$. Excluding it as the TOD-only burst exponent says nothing about Eq. 6's accuracy in the Raman-inclusive regime where Roy et al. validated it.
- **Lab-facing prediction.** In a Raman-free medium, the DW energy at fixed $N$ obeys $\ln E_{\rm DW}\approx-d_*\cdot6|\beta_2|T_0/\beta_3+\dots$. Examples are a noble-gas-filled hollow-core fibre, or a solid-core fibre with $T_0$ long enough that Raman is negligible on the burst time scale. $T_0$ can be varied with $P_0T_0^2$ held fixed. The slope against $T_0$ is set by $d_*$, not by the soliton-strip value $\pi/(2(2N-1))$.

## Derivation

`explorations/2026-10-16-claude-b-dw-singularity-law.md` (heuristic, leading order).

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Dimensionless model; $\delta_3$ in Roy's convention with the factor 6 (verified against Roy Eq. 2, full text) | claude-b (claude) | — | 2026-10-16 |
| Known limits | Exact $N=2$ breather: strip-width fit reproduces $d(\xi)$ to $10^{-4}$. Schemes have orders 2 and 4 against the breather. Roy's TOD-only NSR peak levels reproduced within 1.7 dB ($\delta_3=0.02$–0.1: −23.0, −15.7, −12.8, −10.1, −7.7 dB against my digitisation −22, −14, −12, −10, −6), with peak frequencies within 2% | claude-b (claude) | 2026-10-16-claude-b-dw-oracle | 2026-10-16 |
| Symmetries | Energy conserved to $10^{-12}$. In the law sweeps, momentum $\langle w\rangle$ drifts by less than $10^{-11}$ and the Hamiltonian by less than $10^{-8}$ relative. In the large-$N$ card grid, momentum drifts up to $1.2\times10^{-6}$ and the Hamiltonian up to $1.8\times10^{-6}$ | claude-b (claude) | 2026-10-16-claude-b-dw-oracle | 2026-10-16 |
| Simulation, core regime | P1: fitted $d=0.3788$ (+1.1%), $p=-3.43$ | claude-b (claude) | 2026-10-16-claude-b-dw-oracle | 2026-10-16 |
| Error-scaling exponent | Deviation of the local slope from $d_*$: $\propto\delta_3^{1.19}$ (sech $N=2$), $\delta_3^{1.87}$ (sech $N=3$), $\delta_3^{1.15}$ (Gaussian $N=4$) | claude-b (claude) | 2026-10-16-claude-b-dw-oracle | 2026-10-16 |
| Held-out region | P2: 0.2008 (+0.6%). P3: 0.1323 (+0.1%). P4: 0.1929, which is −4.3% against the A1 value (fails the 4% tolerance) and +0.3% against the full-length minimum found afterwards. P5: see the next row | claude-b (claude) | 2026-10-16-claude-b-dw-oracle | 2026-10-16 |
| Convergence and artefacts | Halving the step changes $\eta_{\rm DW}$ by at most 13% at $\eta\approx10^{-13}$ and by less than 1% for $\eta>10^{-9}$. Gate +5 changes it by less than $10^{-4}$. A second integrator (RK4IP) agrees with Yoshida split-step to between $2\times10^{-7}$ and $3\times10^{-4}$ at moderate yields. On held-out law points it agrees to −1.1% and −0.3% (sech $N=3$, $\delta_3=0.0043$ and 0.0052) and to −2.0% and −0.5% (Gaussian $N=4$, 0.0028 and 0.0034), at yields down to $7\times10^{-15}$. The implied change in the fitted $d$ is below 0.2% (`rk4ip_heldout_*.json`) | claude-b (claude) | 2026-10-16-claude-b-dw-oracle | 2026-10-16 |
| Held out: sech $N=4$ (P8, frozen in A11, commit c415209) | **Refuted as frozen.** The four-point fit gives $d=0.44$ (ill-conditioned) against $d_*=0.1342$ (fine scan: 0.13335 at $\xi=0.235$ and 1.336; next events 0.194–0.200).
- Gated yields at $\delta_3=0.0029$, 0.0032, 0.0035, 0.0039: $3.41\times10^{-12}$, $3.60\times10^{-10}$, $1.21\times10^{-8}$, $1.32\times10^{-7}$.
- Local slopes 0.144, 0.131, 0.082: non-monotone. The two smallest-$\delta_3$ intervals bracket $d_*$ to ±8%, but the yield at 0.0039 is anomalously high.
- Step convergence: at most 0.6% after halving. Gate +5: at most 0.3%.
- At $d_*/\delta_3=34$–46 this launch is not yet in a clean asymptotic regime. A likely cause is a $\delta_3$-dependent number of recompression bursts before TOD-induced fission. Smaller $\delta_3$ is needed.
- **Exploration after the refutation (not frozen)** at $\delta_3=0.0024$ and 0.0026 ($d_*/\delta_3=51$–56; $N_t=131072$):
  - gated yields $1.22\times10^{-16}$ and $1.12\times10^{-14}$;
  - local slopes over $\delta_3=0.0025$–0.0031 are 0.141, 0.144, 0.144, stable but 6–8% above $d_*$;
  - a three-parameter fit on the four smallest $\delta_3$ gives $d=0.128$ (−4%), but with an unusual positive prefactor exponent $p=+5.4$.
  - Consistent with slow convergence to $d_*$, but not decisive | claude-b (claude) | 2026-10-16-claude-b-dw-oracle (`yield_s4*.json`, `dscan_sech4.json`) | 2026-10-16 |
| Length dependence (P5, frozen in A4) | Gaussian $N=3$ with $\xi_f=1.0$: fitted $d=0.2025$, which is within 0.5% of the first-compression value 0.2015 (prediction: within 2%) and 5.0% above the $\xi_f=2$ fit (prediction: at least 2.5%). Confirmed | claude-b (claude) | 2026-10-16-claude-b-dw-oracle | 2026-10-16 |
| Relaxed assumption: Raman | Model M1: $f_R=0.18$, $\tau_1=12.2$ fs, $\tau_2=32$ fs, $T_0=50$ fs, RK4IP, kernel step at most 2.9 fs. The law holds with $d_*$ computed from the **Raman-including** TOD-free evolution. Sech $N=2$: $d_*^{M1}=0.4410$, four-point fit 0.4434 (+0.5%); not a frozen test, because part of the sweep was seen first. Gaussian $N=3$ (held out, P6): fitted $d=0.2358$, +0.5% from $d_*^{M1}=0.2346$ and +22% above M0. Confirmed; step convergence better than $2\times10^{-4}$, gate 20 against 15 identical to $10^{-8}$.
- Second code, FastDifferentiableMMNLO (claude-b.7, same family; run 2026-10-16-claude-b.7-solver-m1gauss):
  - $d=0.23596$, with $p=-2.970$ and fit residuals about $5\times10^{-5}$ in $\ln\eta$, i.e. +0.6% from $d_*^{M1}$;
  - the yields agree with numpy to $10^{-4}$ after correcting both codes to zero Raman kernel step;
  - the step, kernel-step and self-steepening corrections change $d$ by at most $1.2\times10^{-4}$. Raman cuts TL yields by 770× (sech $N=2$, $\delta_3=0.02$) and 215× (Gaussian $N=3$, 0.01) | claude-b (claude) | 2026-10-16-claude-b-dw-oracle | 2026-10-16 |
| Collapse (A9, frozen) | Predicted from the $N=3$–4 collapse curve, then computed: $d_*(5)$ 0.10±20% → 0.0885; $d_*(6)$ 0.080±15% → 0.0725; $d_*(8)$ 0.053±15% → 0.0572. The last is a narrow dip at $\xi=1.652$, converged on two grids; the 3-point median alone gave 0.066. $d_*(10)$ not determined (the strip fit failed on the $N_t=16384$ grid). **Confirmed for $N=5,6,8$.** Caveat: the A9 basis used $d_*(4)=0.1317$ ($\xi\le1$) instead of 0.1191 ($\xi\le2$) | claude-b (claude) | 2026-10-16-claude-b-dw-oracle (`dstar_card_*.json`, `dstar_fine_N8.json`, `collapse.json`, `fig_collapse.png`) | 2026-10-16 |
| Second solver | FastDifferentiableMMNLO at b9fa957 (fixed-step RK4IP, Julia), run by subagent claude-b.7: same family, a second code, not an independent verification. Smooth-gate yields for sech $N=2$ at $\delta_3=0.010,0.012,0.014,0.016,0.020,0.025,0.030$: $1.499\times10^{-10}$, $4.419\times10^{-8}$, $2.350\times10^{-6}$, $4.296\times10^{-5}$, $1.7600\times10^{-3}$, $1.0773\times10^{-2}$, $2.6480\times10^{-2}$. These agree with the numpy oracle to within 0.2%. Its local slopes are 0.341, 0.334, 0.325, 0.297. The $\beta_3$ convention was checked to $1.2\times10^{-6}$ in phase. Roy check: NSR −23.36, −15.60, −12.84, −10.07, −7.70 dB; $\Delta\nu_dT_0$ 4.06, 2.89, 2.26, 1.65, 1.14. Raman (M1) yields agree within 1%, with second-order convergence in the kernel step. A hard gate at $|\tau|<8$ leaks soliton tails ($4\times10^{-9}$ to $10^{-8}$); only the smooth gate is used for the law | claude-b.7 (claude) | 2026-10-16-claude-b.7-solver-dwyield | 2026-10-16 |
| Independent units and limits | Exact N=2 strip is 0.37473443; the card's printed decimal is slightly inaccurate. Fourier amplitude versus power and the factor 6 in TOD were checked. Roy's paper uses shock 1/(omega0 T0); the requested doubled variant was also run. | gpt-a (gpt) | 2026-10-16-gpt-a-gate-null; 2026-10-16-gpt-a-roy-reference; 2026-10-16-gpt-a-dw-roy | 2026-10-16 |
| Independent core and frozen tests | P1 fitted d=0.379059; P2=0.201960; P3=0.133598; P4=0.194046; exact-grid P5=0.203646; P6=0.235957. These pass their stated tolerances. P4 is 3.70% below its original truncated-strip anchor, so this audit does not repeat that original tolerance failure. P8 fails again and remains excluded. | gpt-a (gpt) | 2026-10-16-gpt-a-dw-law; 2026-10-16-gpt-a-dw-heldout; 2026-10-16-gpt-a-dw-followup; 2026-10-16-gpt-a-dw-analysis | 2026-10-16 |
| Independent held-out predictions | New sech N=2 yield log-errors are at most 0.00340; new Gaussian N=3.5 errors are at most 0.00681. Both pass the frozen 0.10 tolerance. The latter needs a gate-stability qualification. | gpt-a (gpt) | 2026-10-16-gpt-a-dw-law; 2026-10-16-gpt-a-dw-heldout; 2026-10-16-gpt-a-dw-analysis | 2026-10-16 |
| Independent error scaling | Frozen-grid local-slope error powers: 1.159 (sech 2), 1.146 (sech 3), 1.130 (Gaussian 4), 1.142 and 1.123 (Gaussian 3, lengths 1 and 2), 1.076 (M1 Gaussian 3), against predicted 1. These are finite-interval estimates. | gpt-a (gpt) | 2026-10-16-gpt-a-dw-analysis | 2026-10-16 |
| Independent numerical artefacts | Step, window and grid tests pass in the original finite range. Yoshida and RK4IP agree. The pinned Julia solver matches the independent model; its window changes resolved yields by at most 1.7e-11 relative. The sampled Raman response converges at order 2.000. Physical photon and envelope norms are distinguished. | gpt-a (gpt) | 2026-10-16-gpt-a-dw-convergence; 2026-10-16-gpt-a-dw-followup; 2026-10-16-gpt-a-dw-julia; 2026-10-16-gpt-a-dw-analysis | 2026-10-16 |
| Roy full model, independent extension | Fig. 3(b) circles reproduced approximately: RMS 1.3724 dB, maximum 1.7039 dB. Independent blue strip about 0.4655; only p,c fitted. Observable peaks at TOD 0.016–0.03 have RMS error 0.400 dB for the calibrated strip law versus 8.022 dB for parameter-free Eq. 6. The 39.49 dB TOD-only gap at 0.02 becomes 7.67 dB in the full model. Both descriptions fail in the saturation range. | gpt-a (gpt) | 2026-10-16-gpt-a-dw-roy; 2026-10-16-gpt-a-roy-reference; 2026-10-16-gpt-a-dw-strips; 2026-10-16-gpt-a-dw-analysis | 2026-10-16 |
| Long fibres and descriptive collapse | N=2 exponents at lengths 8 and 12 remain within tolerance. New N=5 finite-yield points pass the frozen collapse spread, but this is not a ceiling. | gpt-a (gpt) | 2026-10-16-gpt-a-dw-length; 2026-10-16-gpt-a-dw-convergence; 2026-10-16-gpt-a-dw-analysis | 2026-10-16 |
| Independent GPT audit | **Fail as written.** At N=2, xi=2.25, TOD=0.003, the fixed gate gives 2.635600e-45, versus 2.309832e-47 for separated radiation: factor 114. The unique minimum precedes the fibre end and the core remains inside the gate. All three endpoint controls pass 1%. The recompression-end diagnostic has local rates near 0.125–0.127 for the claimed observable, versus 0.367 for separated radiation and d*=0.3747. The finite-range radiation result survives; the literal fixed-gate claim does not. | gpt-a (gpt) | 2026-10-16-gpt-a-dw-highprecision; 2026-10-16-gpt-a-gate-null | 2026-10-16 |
| Novelty search | Mine was cursory. gpt-b's review (T-20261016-claude-b-08, PR #49): **partly published**. Compression-localised emission and pole-controlled radiation of fundamental cores are known; the minimum-strip exponent for an evolving breather was not found (medium confidence). See the novelty notes below | claude-b (claude); gpt-b (gpt) | — | 2026-10-16 |
| Independent literature review | **Partly published.** Fundamental-core complex-pole radiation is established (Wai–Chen–Lee, DOI 10.1103/PhysRevA.41.426; Karpman, DOI 10.1103/PhysRevE.47.2073; full text). Compression-region emission and oscillating higher-order-soliton radiation are established (Austin et al., DOI 10.1364/OE.14.011997; Driben–Yulin–Efimov, DOI 10.1364/OE.23.019112, arXiv:1505.02716; full text). The specific evolving-strip **integrated-yield limit was not found**, at medium confidence. [Report and access/search ledger](../docs/review-2026-10-16-gpt-b-dw-singularity-novelty.md), committed before any proposer derivation/log/history was read. No verification or status promotion; access and asymptotic-observable follow-ups are T-20261016-gpt-b-06 and T-20261016-gpt-b-07. | gpt-b (gpt; gpt-6-astra) | — (literature only) | 2026-10-16 |

**Novelty notes.**

*gpt-b's review* (`docs/review-2026-10-16-gpt-b-dw-singularity-novelty.md`, branch `task/T-20261016-claude-b-08`, PR #49, not yet merged). Verdict: **partly published**. The access levels below are gpt-b's unless stated otherwise.
- **Emission concentrated at maximum compression, before the solitons separate, is published:**
  - Austin et al. (2006), DOI 10.1364/OE.14.011997 (full text, gpt-b). Compression-region integrated DW energy and recoil-corrected frequencies.
  - Demircan, Pietrzyk & Bandelow (2007), DOI 10.34657/2265 (full text, gpt-b).
  - Driben, Yulin & Efimov (2015), DOI 10.1364/OE.23.019112, arXiv:1505.02716 (full text, gpt-b). Radiation from oscillating higher-order solitons, with phase matching of the radiation comb.
- **Pole-controlled exponentially small radiation is published for fundamental-soliton cores:**
  - Wai, Chen & Lee (1990), DOI 10.1103/PhysRevA.41.426 (full text, gpt-b);
  - Karpman (1993), DOI 10.1103/PhysRevE.47.2073 (full text, gpt-b; abstract only by me);
  - Akhmediev & Karlsson (1995), DOI 10.1103/PhysRevA.51.2602 (full text, gpt-b);
  - Moston-Duggan, Porter & Lustri (2023), DOI 10.1007/s00332-022-09834-5, arXiv:2203.08407 (full text, gpt-b). PDE-level exponential asymptotics about a sech core.
- **The evolving-strip diagnostic itself is established:** Sulem, Sulem & Frisch (1983), DOI 10.1016/0021-9991(83)90045-1 (abstract only, gpt-b).
- **Closest method in another equation:** McCue et al. (2026), DOI 10.1017/jnw.2026.10033, arXiv:2509.07397 (full text, gpt-b; abstract only by me). Complex singularities and dispersive waves in KdV. Its multiplier can vanish while the poles remain, so a nonzero coupling must be shown for the NLS case.

*What gpt-b did not find* (medium confidence): the specific limit $\lim\delta_3\ln\eta_{\rm DW}=-\min_{\xi\le\xi_f}d(\xi)$ for an evolving breather.

*Obligations gpt-b lists for verification:*
- show the coupling is nonzero;
- control coherent contributions from several poles or compression events;
- bound gate contamination as $\delta_3\to0$;
- keep spectral peak, flux and band integral distinct.

*My own reading:* Roy et al. 2009, DOI 10.1103/PhysRevA.79.023824 (**full text**; Eqs. 1–6, Figs. 1–4); Ciret et al., arXiv:1805.05175 (abstract only by me).

## Outcome

Status cheap-checks-passed, by the proposer's family only.
- Confirmed within tolerance: P1, P2, P3, P5 and P6.
- **Refuted: P8** (sech $N=4$, A11). The fit procedure fails, with non-monotone local slopes at $d_*/\delta_3=34$–46.
- P4 failed its frozen number (−4.3% against 4%). The failure was traced to a truncated $d_*$ scan; with the full-length minimum the deviation is +0.3%, but that agreement was found after the result.
- P7: see C-20261016-claude-b-02. GDD (A3): 11 of 12 points within a factor 2 at $\delta_3=0.01$. The cubic-phase test (A6) was refuted because its $d_*$ input was a fit outlier. The corrected prediction (A7), frozen before the held-out result, is confirmed at $\delta_3=0.006$: 0.701 measured against 0.667 predicted.
- A same-family second code (FastDifferentiableMMNLO) agrees to within 0.2%.

Still needed: GPT-family verification (T-20261016-claude-b-01) and the novelty audit (T-20261016-claude-b-08).

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-16 | claude-b (claude; claude-opus-5-5) | Framing of Roy et al. (2009) corrected after PI review: Eq. 6 is a spectral-peak estimate validated against Raman-inclusive simulations; Roy et al. themselves report the TOD-only deviation; the gap is δ3-dependent; the asymptotic regime lies below their visibility floor; the comparison with Roy's full model is not done. Predecessors from gpt-b's novelty review added. No prediction, number, status or regime bound changed. | Orchestrator message on the PI's instruction, 2026-10-16; Roy et al. 2009 full text; `docs/review-2026-10-16-gpt-b-dw-singularity-novelty.md` (branch task/T-20261016-claude-b-08) |
| 2026-10-16 | gpt-a (gpt; gpt-6-astra) | Cross-family verification and adversarial audit completed. Status cheap-checks-passed → refuted for the literal fixed-gate small-TOD statement. Finite-range exponent, frozen tests, full Roy comparison and surviving scope recorded above. The old regime is superseded and retained below. No proposer Statement, Derivation or problem card was rewritten. | Run 2026-10-16-gpt-a-dw-highprecision; [audit](notes/audit-2026-10-16-gpt-a-C-20261016-claude-b-01.md); other independent runs in Checks |

Historical Outcome and “Not done” sentences above describe the proposer-stage card. The new Checks, frontmatter and this audit entry record the current status.

Superseded regime, retained verbatim:

> - Small parameter: $\delta_3/d_*$. The asymptotic form is asserted for $d_*/\delta_3\gtrsim30$; it was tested for $d_*/\delta_3$ from 10 to 47.
> - The relative error of the local slope $-d\ln\eta_{\rm DW}/d(1/\delta_3)$ against $d_*$ is $O(\delta_3)$. The measured exponents are 1.1–1.9.
> - Launches tested: sech with $N=2,3$; Gaussian with $N=3,4$. These pass the frozen four-point procedure.
> - **Sech $N=4$ fails it at $d_*/\delta_3=34$–46** (A11): local slopes are non-monotone, though they bracket $d_*$ within 8%. The onset of the asymptotic regime is launch dependent, and at $N\ge4$ it may need $d_*/\delta_3\gg50$.
> - $\xi_f$ must be long enough for the DW to clear the gate: $(\xi_f-\xi_*)/(4\delta_3)\gtrsim25$.
> - Yields in the tested range run from $10^{-14}$ to $10^{-3}$.
