---
id: C-20261010-claude-a-01
problem: P-20261010-claude-interactive-01
title: "Dispersionless λ_min(V): exact Kerr–Raman shear covariance, closed forms, and a √(ΦL/L_D) correction from weak normal dispersion"
type: asymptotic-solution
status: promoted
proposed_by: claude-a
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: "gpt-a (items 1, 2, 3(b), 4, 5; 2026-10-11); pi-chatgpt (item 5, 2026-10-18)"
verifier_family: gpt
audited_by: gpt-e
auditor_family: gpt
created: 2026-10-10
updated: 2026-10-19
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: R-0012
---

## Statement

> **Clean-context adversarial audit (gpt-e, gpt-6-astra, family gpt, 2026-10-19): pass-reduced-regime.** [Report](notes/audit-2026-10-19-gpt-e-C-20261010-claude-a-01.md), run `2026-10-19-gpt-e-weak-dispersion`. This scope controls the audit status of the statements below.
> - Items 1–2 pass in the stated linearized model; a continuum isolated peak gives a spectral infimum, not necessarily an attained eigenmode. The two instantaneous-polarization limits in item 4 pass; intermediate-beat thresholds and delayed vector extensions are not independently audited here.
> - Item 3(b) is a **joint** long-pulse, broad-relative-band, low-physical-frequency limit: $1\ll B=\Omega_bT_0$ while the frequencies used obey $\Omega\tau_{1,2}\ll1$. A fixed scaled band retains localization cost; allowing arbitrarily large physical detuning accesses the electronic Kerr branch. The former finite one-percent regime remains refuted.
> - Item 5 passes as an unrestricted normal-dispersion asymptotic at fixed positive $\Phi$, for a nondegenerate peak (or the stated higher-order-peak generalization). Gaussian phases $\Phi=7,17$ give excess powers 0.501899 and 0.501898; the quartic check at $\Phi=7$ gives 0.667209. Fixed detection bandwidth and a limit uniform as $\Phi\to0$ are excluded. A global continuum lower bound and a uniform brightness bound in the shrinking mode remain open.

> **As verified (family gpt; filed 2026-10-19 by claude-interactive).**
> - **gpt-a's audit** ([gpt-a audit](../docs/review-2026-10-11-gpt-a-highlights-audit.md), run `2026-10-11-gpt-a-highlights-audit-c3`, 2026-10-11) gave these verdicts; they were not recorded on this card until now:
>   - items 1–2: pass, within linearized theory ("minimum" means spectral infimum for an isolated peak on continuous time);
>   - item 3(b): the closed form passes, the limiting approach passes in a reduced regime, and the finite "below 1%" regime **fails** (counterexample at $T_0=200$ fs, $\Phi=10$, 300 K, $\Omega_bT_0=30$: excess 7.50%);
>   - item 4: pass for the isotropic and strong-birefringence models;
>   - item 5: pass with a reduced regime.
> - **GPT 6 Pro** ([review](../docs/review-2026-10-18-pi-chatgpt-similariton-normal-dispersion-verification.md), run `2026-10-18-pi-chatgpt-independent-verification`, 2026-10-18) independently derived item 5 from the full linearized generator and reproduced it with its own solvers:
>   - coefficient $\sqrt{2/3}\,\Phi/\sqrt{1+\Phi^2}$, mode rms width $T_0(y/24)^{1/4}$ at every fixed $\Phi>0$;
>   - peak order $2m$ gives the excess power $m/(m+1)$.
> - **Narrowed:**
>   - item 5 is an asymptotic for the **unrestricted** homodyne covariance at fixed $\Phi>0$ and unrestricted optical bandwidth ($\Omega_bT_0\gg y^{-1/4}$; it fails at fixed bandwidth);
>   - it is a lower bound on passive-filter counting noise, not that noise;
>   - the global continuum lower bound (spectral localization) is unproved;
>   - the card's linearization condition $\Phi/\sqrt{N_{\rm ph}}\ll1$ is not uniform as the mode narrows (the report wrote it as $\Phi\ll N_{\rm ph}$; corrected 2026-10-19 after claude-interactive.19's check).
> - **Refined:** $c_2$ has a closed form, $c_2(\infty)=2\sqrt6/5=0.9798$ (claim C-20261019-pi-chatgpt-01).
> - **False:** the open prediction "exponent 0.50 for any even, smooth pulse". It needs a nondegenerate quadratic maximum, and $e^{-t^4}$ gives 2/3, as stated below.

**Setting.**
- Model: scalar, single polarization, single spatial mode, no dispersion:
  $$\partial_zA=i\gamma A\,(R*|A|^2)+iA\,\Gamma_R,\qquad R=(1-f_R)\delta+f_Rh_R .$$
- Input: a coherent pulse $A_0=\sqrt{P_0\,p(t)}$, with $\Phi=\gamma P_0L$.
- Output: amplitude and phase quadratures in the frame of the mean phase, normalized so shot noise is 1.
- $\lambda_{\min}(V)$ is the smallest eigenvalue of the output covariance over all modes.

**1. Exact covariance.** $|A|^2$ is $z$-invariant, so within linearized theory:
$$V=\begin{pmatrix}I&K^{\mathsf T}\\K&I+KK^{\mathsf T}+N\end{pmatrix},\quad K=2\Phi\sqrt p\,\hat R\sqrt p,\quad N=2\Phi f_R\sqrt p\,\hat H\sqrt p,$$
$$\tilde H(\omega)=2|\mathrm{Im}\,\tilde h_R(\omega)|\coth\frac{\hbar|\omega|}{2k_BT}.$$
$\hat R$ and $\hat H$ are convolutions. $N$ is fixed by unitarity, $[N_R(t),N_R(t')]=-2i[K(t,t')-K(t',t)]$, plus thermal equilibrium.

**2. Closed form without a reservoir** ($N=0$, which includes $f_R=0$):
$$\lambda_{\min}(V)=V_{\min}\big(\sigma_{\max}(K)/2\big),\qquad V_{\min}(\Phi)=1+2\Phi^2-2\Phi\sqrt{1+\Phi^2}.$$
For Kerr this gives $\lambda_{\min}(V)=V_{\min}(\Phi)$ for every pulse shape, which is the card's anchor, now shown to be exact.

**3. Raman with its reservoir.**
- (a) Over all modes, $\lambda_{\min}(V)\le V_{\min}((1-f_R)\Phi)$. That value is reached by modes at the peak modulated beyond the Raman band, where the delayed response and its noise vanish. Two families of modes compete:
  - Short pulses ($T_0=50$ fs, 0 and 300 K, $\Phi=5$–20): equality holds to 0.5%.
  - Long pulses at low temperature: slow modes at the peak see the full shear $2\Phi p$ with little reservoir noise (at 0 K, $\tilde H\propto|\omega|$ near 0) and do better. At $T_0=200$ fs, 0 K, $\Phi=5$: $\lambda_{\min}=0.01352$, below $V_{\min}(4.1)=0.01445$. In the long-pulse 0 K limit they approach $V_{\min}(\Phi)$.
- (b) Restrict to modes inside a band $|\omega|\le\Omega_b$ around the pulse's own spectrum. For long pulses ($T_0\gg\tau_{1,2}$), $T>0$ and $\Omega_bT_0\gg1$, $\lambda_{\min}$ tends to the single-slice value
  $$\lambda_{\min}\begin{pmatrix}1&2\Phi\\2\Phi&1+4\Phi^2+2\Phi f_R\tilde H(0)\end{pmatrix}\simeq\frac{1}{4\Phi^2}+\frac{f_R\tilde H(0)}{2\Phi},\qquad \tilde H(0)=\frac{4k_BT}{\hbar}\big|\partial_\omega\mathrm{Im}\,\tilde h_R(0)\big| .$$
  For Blow–Wood at 300 K, $\tilde H(0)=1.276$. The thermal reservoir changes the large-$\Phi$ law from $\Phi^{-2}$ to $\Phi^{-1}$, with coefficient $f_R\tilde H(0)/2=0.115$.
  For continuous waves this change of law is known (Voss, Köprülü & Kumar 2006; Shapiro & Boivin 1995; see Checks, Novelty). What is claimed here is the pulsed, band-limited form and its approach from finite $T_0$.

**4. Two polarizations, Kerr.**
- Isotropic fibre with input ellipticity angle $\chi$: $\lambda_{\min}=V_{\min}(\Phi_{\rm eff})$ with $\Phi_{\rm eff}=\tfrac\Phi3\big(1+\sqrt{1+3\cos^22\chi}\big)$.
- Strong linear birefringence without walk-off, input power fractions $c_x,c_y$ on the axes: $\Phi_{\rm eff}=\tfrac\Phi2\big(1+\sqrt{1-\tfrac{20}{9}c_xc_y}\big)$.
- Intermediate beat length, 45° linear input. The crossover between $\Phi_{\rm eff}=\Phi$ and $5\Phi/6$ is controlled by $b=\Delta\beta/(\gamma P_0)=2\pi L_{NL}/L_B$ alone, to within 1% for $\Phi=5$, 10 and 20. It is numerical, with no closed form:
  - within 1% of the isotropic value for $b\le0.03$ ($L_B\gtrsim200\,L_{NL}$);
  - within 0.5% of the strong-birefringence value for $b\ge5$ ($L_B\lesssim1.3\,L_{NL}$);
  - not monotone in between, with oscillations set by the beat phase $b\Phi$.
- **Delayed vector response** (isotropic kernel $a$, anisotropic $b$; derivation note §6). Linear input stays an exact scalar shear with $(1-f_R)\delta+f_R(a+b)$. Circular input stays an exact scalar shear with $\tfrac23(1-f_R)\delta+f_R(a+b/2)$, so items 1–3 apply with those kernels.
  - Lin–Agrawal-type kernels, $\Phi=10$, 0 K, $T_0=200$ fs and 1 ps (`vector_raman_exact.json`): $\lambda_{\min}=0.0052$ and 0.0032 (linear); 0.0090–0.0091 and 0.0059–0.0060 (circular).
  - Elliptical input is not an exact shear, so it is not part of this claim. A validated $z$-propagation at $\chi=\pi/8$ (`vector_raman_prop.json`) is reported in the log entry.

**5. Weak normal dispersion** ($\beta_2>0$, Kerr). Let $y=\Phi L/L_D=\gamma P_0\beta_2L^2/T_0^2$. Then
$$\frac{\lambda_{\min}(V)}{V_{\min}(\Phi)}-1=\frac{\Phi^{3/2}}{\sqrt{1+\Phi^2}}\sqrt{\tfrac13|p''(0)|\,\beta_2L}\;\big[1+c_2\sqrt y+O(y)\big],\qquad c_2\simeq1.0 .$$
*[Refined 2026-10-19: closed form $c_2(\Phi)$, $c_2(\infty)=2\sqrt6/5$ (C-20261019-pi-chatgpt-01).]*
For the Gaussian $p=e^{-t^2/T_0^2}$ the prefactor is $\sqrt{2/3}\,\Phi/\sqrt{1+\Phi^2}$ times $\sqrt y$.

**General peak shape.** If $1-p\simeq\kappa|t/T_0|^{2m}$ near the peak, the same argument gives $e_{2m}\,q^{m/(m+1)}(A\kappa)^{1/(m+1)}$. Here $q=\tfrac13\tfrac{\Phi^2}{\sqrt{1+\Phi^2}}\beta_2L$ (in units of $T_0$), $A=2\Phi/\sqrt{1+\Phi^2}$, and $e_2=1$, $e_4=1.06036$.
- For the flat-top $p=e^{-(t/T_0)^4}$ this is $0.64226\,\tfrac{\Phi}{\sqrt{1+\Phi^2}}\,y^{2/3}$: exponent 2/3, not 1/2.
- It was frozen before computing (held-out, below).

The small parameter is $y=x/\Phi$, not $x=\Phi^2L/L_D$. For smooth, generic peaks the dependence on it is a square root. So $\lambda_{\min}(V)$ is the first quantity to leave the dispersionless value: 1% at $y\approx1.5\times10^{-4}$.

With anomalous dispersion, $\lambda_{\min}(V)$ has no dispersionless limit. It falls far below $V_{\min}(\Phi)$ for any $\beta_2<0$, through modulation-instability squeezing of dark sidebands, by an amount set by the grid bandwidth. *[Narrowed 2026-10-19 (GPT 6 Pro): in the frozen continuous-wave model the optimum is resolved at detuning $a=-\Phi$ with $\lambda=e^{-2\Phi}$; further grid bandwidth does not set it. This is not a pulsed anomalous-dispersion theorem.]*

## Regime

- **Linearization:** $\Phi/\sqrt{N_{\rm ph}}\ll1$.
- **Items 1–4:** $L/L_D=0$, no self-steepening, single spatial mode. Item 2 is exact there.
- **Audited item 3(b):** take the joint ordering $1\ll\Omega_bT_0$ with $\Omega_b\tau_{1,2}\ll1$, at fixed positive phase and temperature, rather than sending pulse duration to infinity at a fixed scaled band. This explicit ordering supersedes an interpretation of the old long-pulse sentence as a single unrestricted limit. Run `2026-10-19-gpt-e-weak-dispersion`.
- **Item 3(b):** asserted for $T_0\ge200$ fs, $T=300$ K, $5\le\Phi\le20$ (Blow–Wood, $f_R=0.18$), with $\Omega_bT_0\gtrsim30$: then the excess over the slice value is below 1%. *[Refuted (gpt-a, 2026-10-11, run `2026-10-11-gpt-a-highlights-audit-c3`): 7.50% at $T_0=200$ fs, $\Phi=10$, $\Omega_bT_0=30$.]*
  - The default band I used, $\Omega_b=1.2\max|\bar\phi'|+3/t_{\rm rms}$, gives $\Omega_bT_0\approx1.03\Phi+4.2$. It costs 17%, 7% and 2% at $\Phi=5$, 10 and 20.
  - That cost does not shrink with $T_0$, because the long-pulse problem is self-similar in $T_0$. It does shrink with the band: $\propto(\Omega_bT_0)^{-1.7}$, down to a floor of 0.6% at $\Omega_bT_0\ge44$ (`band_cost_check.json`, $T_0=5$ ps, $\Phi=10$).
- **Item 5:** $10^{-6}\le y\le10^{-2}$ and $2\le\Phi\le40$, Gaussian and sech pulses.
  - The error of the leading term is $O(y^{1/2})$ relative, with measured coefficient $c_2\simeq1.0$. At $y=0.1$ the leading term is 27% low.
  - The flat-top form was tested for $10^{-6}\le y\le10^{-2}$ at $\Phi=10$ and 3. Its relative error is about 1.2% at $y=10^{-3}$ and 5.4% at $y=10^{-2}$.
- **Excluded:**
  - $\lambda_{\min}(V)$ with self-steepening. It is set by dark modes at the grid cut-off and depends on the grid (run below).
  - Anomalous dispersion.
- **Physical caveat for 3(a).** The far-detuned modes that reach $V_{\min}((1-f_R)\Phi)$ see the fibre's real dispersion. They leave the dispersionless regime once $\beta_2\Omega^2L\gtrsim1$, so 3(b) is the physically relevant value.

## Assumptions

1. Linearized Gaussian quantum noise about the classical mean field. Coherent input, with no excess laser noise.
2. Scalar field, one polarization (except item 4), one spatial mode.
3. No dispersion, except $\beta_2$ alone in item 5. No $\beta_3$ and no dispersion of $\gamma$.
4. No self-steepening.
5. Raman: Blow–Wood single damped oscillator ($\tau_1=12.2$ fs, $\tau_2=32$ fs), $f_R=0.18$. Parallel (isotropic) response only; anisotropic Raman is absent in item 4.
   Item 4 also assumes a fully symmetric, instantaneous $\chi^{(3)}$ tensor ($d=1$ in the Tanaś–Kielich notation). For general $d$ the same eigenvalue calculation gives $\Phi_{\rm eff}=\Phi[1+\sqrt{1+(4d^2-1)\cos^22\chi}]/(1+2d)$; this was checked by hand, with no run.
6. Raman noise: symmetrized $\coth$ reservoir, in thermal equilibrium at temperature $T$.
7. No GAWBS or acoustic noise, no loss, no detector inefficiency.
8. Mean field unchirped, with an even intensity profile.
9. $\lambda_{\min}$ is taken over all modes on the time grid, except in 3(b), which is band-limited as stated.

## Predictions

Frozen before computation in `runs/2026-10-10-claude-a-dispersionless-fano/HELDOUT.md`: commits dc191b0 and ebeb0b7 (10:42 and 11:01 EDT), 3a46f26 (11:24 EDT), 326c335 (11:56 EDT), and 7398320 with correction 7ea70c7 (12:53 EDT).

| Held-out case | Prediction | Result | Run |
|---|---|---|---|
| sech, Kerr, $\Phi=5$ | $V_{\min}(5)=0.009805$ | 0.0098049 | `heldout_results.json` |
| sech, Kerr, $\Phi=15$ | $V_{\min}(15)=0.001109$ | 0.0011086 | same |
| sech, Raman 300 K, $T_s=188.9$ fs, $\Phi=5$ | in [0.009805, 0.03162] | 0.015275 | same |
| sech, Raman 300 K, $\Phi=15$ | in [0.001109, 0.008681] | 0.0018404 | same |
| Item 3(b), Blow–Wood, Gaussian $T_0=500$ fs, $\Phi=15$, 150 and 300 K (frozen at 7398320; 7ea70c7 corrected only the hand-evaluated slice values) | band-limited $\lambda_{\min}$ / slice in [1.00, 1.15] | 1.051 and 1.041 | `heldout_thermal.json` |
| Item 5, Gaussian $\Phi=2$, $10^{-5}\le y\le10^{-3}$ | (measured excess)/(formula) in [0.97, 1.06] | 1.0032–1.0314 | `lam_min_dispersion.json` |
| Item 5, Gaussian $\Phi=40$ | same window | 1.0031–1.0306, all inside | same |
| Item 5, sech $\Phi=10$ | same window | 1.0029–1.0289, all inside | `lam_min_dispersion_sech.json` |
| Item 5, flat-top $e^{-t^4}$, $\Phi=10$ and 3 (frozen at 11:56 EDT, commit 326c335) | exponent in [0.64, 0.69] over $10^{-6}\le y\le10^{-4}$; ratio in [0.95, 1.08] for $y\le10^{-3}$ | exponent 0.6669 ($\Phi=10$) and 0.6668 ($\Phi=3$); ratios 1.0001–1.012 and 1.0001–1.0123; all inside; $dt=0.005$ agrees with 0.01 | `lam_min_dispersion_flattop.json` |

The two Raman intervals were wide: the Kerr anchor below and the thermal slice above. They test only the ordering.

Open predictions, not yet tested:
- For $\beta_2>0$ at fixed $\Phi$, the measured exponent of $\lambda_{\min}/V_{\min}-1$ against $y$ is $0.50\pm0.01$ for any even, smooth pulse. *[False as worded (GPT 6 Pro, 2026-10-18): true for a nondegenerate quadratic maximum; $e^{-t^4}$ gives 2/3.]*
- Item 3(b) at $T_0=5$ ps comes within 5% of the single-slice value at $\Phi=10$, 300 K (registered at cb7ad63, with the default band). **Refuted** at 13:08 EDT: the ratio is 1.0686 (`open_prediction_5ps.json`; 1.0684 on a grid twice as fine).
  - Cause: the band cutoff, not slow convergence in $T_0$. With a band 1.5, 2 and 3 times wider the excess is 1.5%, 0.8% and 0.6% (`band_cost_check.json`).
  - The statement of 3(b) and its regime were corrected accordingly.

## Derivation

`claims/notes/C-20261010-claude-a-01-derivation.md`, sections 1, 2 and 5.

**Item 2.** $V_0=SS^{\mathsf T}$ with $S=\begin{pmatrix}I&0\\K&I\end{pmatrix}$. The singular-value decomposition of $K$ reduces it to $2\times2$ blocks $\begin{pmatrix}1&\sigma\\\sigma&1+\sigma^2\end{pmatrix}$.

**Item 5: harmonic-oscillator balance.**
- A continuous-wave sideband at detuning $\Omega$ evolves under $G=\begin{pmatrix}0&-a\\a+2g&0\end{pmatrix}$ with $a=\beta_2\Omega^2/2$. To first order in $a$ its best squeezing is $V_{\min}(\Phi)\big[1+\tfrac23\,aL\,\Phi^2/\sqrt{1+\Phi^2}\big]$.
- A mode of temporal width $\tau$ at the peak sees $\Phi p$. Since $d\ln V_{\min}/d\Phi=-2/\sqrt{1+\Phi^2}$, it pays $\tfrac{\Phi}{\sqrt{1+\Phi^2}}|p''(0)|t^2$.
- Minimizing $\langle\alpha t^2+b\Omega^2\rangle$ over modes gives the ground-state energy $\sqrt{\alpha b}$, which is the stated prefactor.
- The optimal mode has $\langle t^2\rangle^{1/2}=T_0(y/24)^{1/4}$ for the Gaussian at large $\Phi$. This sets the grid needed: $dt\le0.01\,T_0$ for $y\ge10^{-6}$.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Items 1–5 dimensionless; $\tilde H(0)$ from $k_BT/\hbar$ times a time | claude-a (claude) | — | 2026-10-10 |
| Known limits | $P\to0$ gives $V=I$. $f_R=0$ recovers the card's Kerr anchor exactly, $\lambda_{\min}=V_{\min}(\Phi)$ to $10^{-12}$ for $\Phi=1$–30 | claude-a (claude) | `2026-10-10-claude-a-dispersionless-fano` (`scan_kerr_gaussian.json`) | 2026-10-10 |
| Symmetries | $V+i\Omega\succeq0$ (min eigenvalue $\ge-4\times10^{-12}$) with Raman at 0 and 300 K; reservoir commutator fixed by unitarity | claude-a (claude) | same (`symplectic_min` in `scan_raman_gaussian*.json`, `scan_kerr_gaussian.json`) | 2026-10-10 |
| Symbolic residual | not done (no CAS script) | | | |
| Simulation, core regime | An independent linearized split-step propagator (`lin_ssfm.py`) at $\beta_2=0$ reproduces $V$ to $10^{-13}$. Raman 3(a): grid $\lambda_{\min}=V_{\min}(0.82\Phi)$ within 0.5% at $T_0=50$ fs ($\Phi=5,10,20$). 3(b), band-limited at 300 K: $T_0=1$ ps gives 0.03714 and 0.01471 against slice values 0.03162 and 0.01376 ($\Phi=5,10$); $T_0=200$ fs gives 0.00682 against 0.00632 ($\Phi=20$). Item 4: $\lambda_{\min}=V_{\min}(\Phi_{\rm eff})$ to machine precision for linear, $\chi=\pi/8$ and circular input, and for birefringent fibre at 45° and on axis ($\Phi=10$) | claude-a (claude) | same (`scan_raman_gaussian.json`, `polarization.json`) | 2026-10-10 |
| Error-scaling exponent | Item 5: fitted exponent of the excess against $y$ over $10^{-6}$–$10^{-4}$ is 0.5019, 0.5018, 0.5018, 0.5018 at $\Phi=2,5,10,20$. (measured)/(leading) − 1 = 0.0010, 0.0031, 0.0098, 0.031, 0.094 at $y=10^{-6},10^{-5},10^{-4},10^{-3},10^{-2}$, nearly independent of $\Phi$. That is $c_2\sqrt y$ with $c_2\simeq1.0$. Diagnosis of $c_2$ (`c2_symbol_model.json`, `c2_reshaping_check.json`): (i) the local-symbol model, with the exact CW sideband formula to all orders and the exact local $V_{\min}(\Phi p)$, gives about 0.47. (ii) The rest comes from dispersive reshaping of the mean field. Analytically $\partial_zp(0,z)=-2\beta_2\Phi z$, so $\langle p(0,z)\rangle_z=1-y/3$, confirmed numerically. Together they reproduce $\lambda_{\min}$ to $3\times10^{-5}$ relative at $y=10^{-4}$ and $3\times10^{-3}$ at $y=10^{-2}$, over-correcting slightly. No closed form for $c_2$ is claimed | claude-a (claude) | same (`lam_min_dispersion.json`) | 2026-10-10 |
| Held-out region | Sech, Kerr and Raman: all four inside the frozen windows. Item 5: Gaussian $\Phi=2$ and 40 and sech $\Phi=10$ all inside. The flat-top test of the mechanism (exponent 2/3, predicted before computing) passed at $\Phi=10$ and 3 | claude-a (claude) | same (`heldout_results.json`, `lam_min_dispersion*.json`) | 2026-10-10 |
| Convergence and artefacts | Item 5: $dt=0.02,0.01,0.005\,T_0$ agree to 4 digits for $y\ge10^{-6}$; $dt=0.04$ is under-resolved below $y=3\times10^{-6}$. Input-subspace cut $|t|\le0.6,1,2\,T_0$ and $n_z=200,400$ agree, and the restricted computation matches the full $2n\times2n$ matrix to $4\times10^{-12}$. Raman: kernels bin-averaged exactly over each time bin. $\Phi=10$, 300 K (`raman_dt_convergence.json`): band-limited $\lambda_{\min}$ changes by $<0.04\%$ from $dt=8$ to 2 fs ($T_0=200$ fs) and from 40 to 10 fs ($T_0=1$ ps). The full-grid $\lambda_{\min}$ falls with $dt$ (0.00401, 0.00374, 0.00370 at $T_0=200$ fs) toward $V_{\min}(0.82\Phi)=0.00369$, as item 3(a) states. Hence the band-limited 3(b) | claude-a (claude) | same (`lam_min_dispersion*.json`, `raman_dt_convergence.json`) | 2026-10-10 |
| Second solver or relaxed assumption | Relaxed assumptions: dispersion (item 5, both signs), self-steepening, two polarizations, and birefringence of any strength (`birefringence_lammin.json`; 4×4 RK4 tangent map per slice; symplectic defect $\le2\times10^{-7}$; the limits $b=0$ and $b=100$ reproduce $V_{\min}(\Phi)$ and $V_{\min}(5\Phi/6)$ to 4 digits). Second solver: FastDifferentiableMMNLO, discrete adjoint (subagent claude-a.1; $S$ built row by row and checked against finite differences to $10^{-8}$; Gaussian, $\Phi=5$). (i) $\beta_2>0$, $x=0.1$ ($y=0.02$): $\lambda_{\min}=0.011060$, against 0.011072 from item 5 with $c_2$ and 0.01106 from `lin_ssfm.py`; the most-squeezed mode has rms width 0.17 ps, against the predicted $T_0(y/24)^{1/4}=0.170$ ps. (ii) $x=1$: 0.014568 vs 0.01457. (iii) $\beta_2=0$: the solver's full-$V$ $\lambda_{\min}$ is corrupted by its fixed anti-alias window in the nonlinear step (0.0048 against the exact 0.0098); restricted to $|\omega|\le60$ rad/ps it agrees with the exact map to $10^{-8}$ (task T-20261010-claude-a-07). (iv) Anomalous: the most-squeezed mode is a modulation-instability sideband pair at $\sqrt{2\gamma P_0/|\beta_2|}$, as stated in item 5 | claude-a, claude-a.1 (claude) | `2026-10-10-claude-a-dispersionless-fano`; `2026-10-10-claude-a-solver-dispersion-check` | 2026-10-10 |
| Cross-check with other lanes (unverified WIP) | claude-b's semiclassical $\Lambda(Z)$ (C-20261010-claude-b-01; $y=Z^2$) gives $4Z^2\Lambda=1.09$ at $Z=0.1$, against 1.089 measured here at $y=0.01$. gpt-a's solver pilot gives $\lambda_{\min}=0.171572883$ at $\Phi=1$, against $(\sqrt2-1)^2$ | claude-a (claude) | branches T-20261010-claude-interactive-05 (8908a17), -03 (2a40651) | 2026-10-10 |
| Adversarial audit | **Pass-reduced-regime**, [report](notes/audit-2026-10-19-gpt-e-C-20261010-claude-a-01.md). Independent full-grid tangent optimization, exact Raman covariance and two Jones limits; Gaussian/flat-top powers, fixed-band gap, small-phase nonuniformity. Grid/window/step checks and unchanged-solver RK4IP contractions. Intermediate/delayed vector extensions are outside this audit | gpt-e (gpt; gpt-6-astra) | `2026-10-19-gpt-e-weak-dispersion` | 2026-10-19 |
| Novelty search | Subagent claude-a.2, about 54 search strings (log entry, Literature). Findings by item: item 2 for Kerr is known (Kitagawa & Yamamoto 1986, single mode; time-slice SPM: Joneckis & Shapiro 1993, Kärtner, Joneckis & Haus 1992; abstracts only). The $\Phi^{-2}\to\Phi^{-1}$ change of item 3(b) is known for CW (Voss, Köprülü & Kumar, JOSA B 23, 598 (2006), arXiv:quant-ph/0410214, full text targeted; Shapiro & Boivin, OL 20, 925 (1995), abstract only); our pulsed, band-limited coefficient has not been mapped onto theirs. Item 4 is partially known (Tanaś–Kielich two-mode Hamiltonian, in arXiv:1110.4602 Sec. 4.3). Item 5 was not found; CW modulation-instability squeezing is known (Potasek & Yurke 1987) | claude-a.2, claude-a (claude) | — | 2026-10-10 |
| Independent verification, items 1, 2, 3(b), 4, 5 (item 3(a) not tested by another family) | gpt-a's audit: items 1–2 pass; 3(b) finite regime fails (7.50%); 4 passes for two models; 5 passes with a reduced regime, fitted exponents 0.50186–0.50192 at $\Phi=2$, 5, 10, 20 | gpt-a (gpt) | `2026-10-11-gpt-a-highlights-audit-c3` | 2026-10-11 |
| Independent derivation, item 5 | Derived from the full linearized generator (Duhamel at first order). An exact effective-oscillator minimum $b\|f'\|^2+\alpha\|xf\|^2\ge\sqrt{b\alpha}$ gives the stated coefficient and the localized Gaussian mode. Global continuum lower bound not proved | pi-chatgpt (gpt) | `2026-10-18-pi-chatgpt-independent-verification` | 2026-10-18 |
| Simulation, item 5 | Eighth-order finite differences with DOP853 mean and tangent. Excess powers 0.501914 and 0.501899 (Gaussian, $\Phi=3$, 10), 0.667219 (quartic), 0.750317 (sextic); width powers 0.250240, 0.250148, 0.166609, 0.124926. At $\Phi=3$, $y=10^{-4}$ a separate fourth-order Fourier symplectic solver agrees to $1.1\times10^{-11}$ relative | pi-chatgpt (gpt) | `2026-10-18-pi-chatgpt-independent-verification` | 2026-10-18 |
| Counterexamples | Fixed optical bandwidth: the excess cannot vanish as stated (relative lower gap about $\pi^2\Phi/(16SB^2)$); the "any even, smooth pulse" prediction fails for $e^{-t^4}$ | pi-chatgpt (gpt) | `2026-10-18-pi-chatgpt-independent-verification` | 2026-10-18 |
| Reproduction before filing | The Fourier cross-check is rerun on a second platform: 0.0265400309069 ($7\times10^{-13}$ relative). Oscillator constants agree to $4\times10^{-12}$; the symbolic $c_2(\Phi)$ is identical | claude-interactive (claude) | `2026-10-19-claude-interactive-gpt6pro-quick-repro` | 2026-10-19 |
| Novelty search, item 5 | The nonanalytic correction, its Gaussian coefficient, the localization scale and the peak-order generalization were not found. Kerr squeezing, covariance-mode optimization, filtering bounds (Opatrný–Korolkova–Leuchs 2002) and the harmonic mechanism (Simon 1983) are established | pi-chatgpt (gpt) | — | 2026-10-18 |

## Outcome

**Audited, narrowed (2026-10-19).** Clean-context report committed before access to prior research material; the controlling scope is the audit block above. Independent runs reproduce the leading localization law and retain the Raman finite-regime refutation.
- **Items 1, 2, 3(b) and 4:** gpt-a (family gpt) verified them on 2026-10-11 with the verdicts above. The finite-band 1% regime of 3(b) is refuted. Item 3(a) has not been tested by another family (task T-20261010-claude-a-01).
- **Item 5:** gpt-a and GPT 6 Pro (family gpt) each verified it independently, in the narrowed form above.
- **Audit:** gpt-e completed the separate clean-context audit in task T-20261019-claude-interactive-04. Continuum/brightness estimates and the vector extensions remain follow-up work.

**Promoted (2026-10-19).** Items 1, 2, 3(b) (closed form and limiting approach, without the refuted finite-band regime), 4 (isotropic and strong-birefringence models) and 5 (as narrowed) are promising result [R-0012](../results/promising/R-0012-weak-normal-dispersion-lambda-min/RESULT.md), on the PI's decision to promote every cross-family verified claim. Item 3(a), item 4's intermediate-beat-length and vector-Raman parts, and the closed form of $c_2$ (C-20261019-pi-chatgpt-01) are not part of it. G5 is open.

**Audit recorded on the result (2026-10-19).** gpt-e's clean-context audit (pass with reduced regime) closes gate G5 of R-0012, whose Adversarial audit section gives the signed-off scope.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-19 | gpt-e (gpt; gpt-6-astra) | Clean-context pass-reduced-regime; sim-verified → audited. Explicit joint Raman ordering, fixed-positive-phase and unrestricted-readout scope; untested vector extensions excluded from sign-off | [Audit](notes/audit-2026-10-19-gpt-e-C-20261010-claude-a-01.md); run `2026-10-19-gpt-e-weak-dispersion` |
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Recorded gpt-a's 2026-10-11 verdicts and GPT 6 Pro's item-5 verification. Status proposed → sim-verified (narrowed). Superseded or refuted wording marked inline | Runs `2026-10-11-gpt-a-highlights-audit-c3`, `2026-10-18-pi-chatgpt-independent-verification`, `2026-10-19-claude-interactive-gpt6pro-quick-repro`; [gpt-a audit](../docs/review-2026-10-11-gpt-a-highlights-audit.md); [review](../docs/review-2026-10-18-pi-chatgpt-similariton-normal-dispersion-verification.md) |
| 2026-10-19 | claude-interactive.17 (claude; claude-opus-5-5), task T-20261019-claude-interactive-10, on the PI's promotion decision | Status sim-verified → promoted; result R-0012 (promising tier). Statement unchanged; G5 (clean-context audit, T-20261019-claude-interactive-04) still open | [R-0012](../results/promising/R-0012-weak-normal-dispersion-lambda-min/RESULT.md); PI decision of 2026-10-19 recorded in T-20261019-claude-interactive-07 |
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5) | Merged gpt-e's audit (PR #76) with the promotion to R-0012: status stays promoted, audited_by gpt-e; G5 of R-0012 set to met | PR #76; claims/notes/audit-2026-10-19-gpt-e-C-20261010-claude-a-01.md |
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5) | Corrected the brightness condition in the verified block to the card's own $\Phi/\sqrt{N_{\rm ph}}\ll1$ (the report had written $\Phi\ll N_{\rm ph}$); found by the 2026-10-19 manuscripts | Task T-20261019-claude-interactive-15 |
