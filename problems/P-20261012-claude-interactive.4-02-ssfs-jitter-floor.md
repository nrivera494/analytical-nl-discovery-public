---
id: P-20261012-claude-interactive.4-02
title: Fluctuation–dissipation floor on the frequency jitter of soliton self-frequency-shift conversion
status: parked
priority: 2
literature_state: partial
novelty_confidence: low
target_quantity: A lower bound, or a refutation of a positive lower bound, for the final frequency-centroid variance
  at prescribed Raman shift and conversion efficiency within an explicitly restricted family of silica-fiber dispersion
  profiles and launch pulses, including deterministic transport of distributed noise.
model: Scalar silica propagation with a specified passive Raman response and its consistent quantum/thermal Langevin
  spectrum; coherent input and explicitly defined soliton-band centroid measurement. Begin with a single adiabatic
  fundamental soliton and lossless propagation; bound profile variations, bandwidth, peak power and length before
  adding fission, loss and shock corrections.
oracle_ready: partial
last_audited: '2026-10-13'
audited_by:
- claude
- gpt
proposed_by: claude-interactive.4
provenance:
  agent: claude-interactive.4
  model: claude-fable-5-1
  family: claude
claims: []
results: []
review_provenance:
  agent: gpt-a
  model: gpt-6-astra
  family: gpt
  verdict: open, narrowed
  concurrence: pending
  review: docs/review-2026-10-13-gpt-a-frequency-conversion-novelty.md
---

> **Merged into P-20261016-claude-interactive-03** (Raman-soliton efficiency–shift(–jitter) frontier) by PI decision on 2026-10-16. That card carries this card's premises and its GPT audit in its "Merged cards" section. Continue the work there; this card is kept for its history and is not worked on separately.

## Target quantity

**GPT verdict: open, narrowed.** Raman drift and quantum/thermal noise already share a published microscopic model; frequency-coordinate diffusion is already explicit. A design-independent floor does not follow from this local relation. Keep **candidate** while a restricted optimization problem is specified and Claude reviews the changed gap.

Retain $J=N_{\rm ph}\sigma_\Omega^2T_0/|\Delta\Omega|$, but specify whether $N_{\rm ph}$ is the launched or detected soliton photon number, the centroid estimator, output spectral window, conditioning on soliton survival and the reference duration $T_0$. Use the same definition for every design. Bound the admissible dispersion profiles, pulse bandwidth, peak power, length and output efficiency. Unlimited design freedom is not an assumption under which a positive universal floor has been established.

## Premise check

[Corney and Drummond (2001), II; 10.1364/JOSAB.18.000153](https://doi.org/10.1364/JOSAB.18.000153) (**full text**) contains the **frequency-coordinate covariance** directly in preprint Eq. 3.15, before integration into timing jitter. Its analytic treatment neglects deterministic SSFS. [Drummond and Corney (2001), I; 10.1364/JOSAB.18.000139](https://doi.org/10.1364/JOSAB.18.000139) (**full text**), preprint Eqs. 6.11 and 6.16, already relates the dissipative Raman response to the thermal and zero-point noise spectrum. [Kärtner et al. (1994); 10.1364/JOSAB.11.001267](https://doi.org/10.1364/JOSAB.11.001267) (**abstract only**) explicitly treats SSFS and quantized Raman noise in one model. Thus “nobody has written drift and diffusion using one kernel” is superseded.

A lower bound on local diffusion divided by local drift does not automatically bound final variance divided by total shift. Linearized propagation gives
$$\Sigma(L)=\Phi(L,0)\Sigma(0)\Phi(L,0)^\dagger+
\int_0^L\Phi(L,z)D(z)\Phi(L,z)^\dagger\,dz,$$
so deterministic transport $\Phi$ matters. A scalar counterexample to the proposed implication is $x'=v_0-kx$ and $S'=-2kS+(c/N_{\rm ph})(v_0-kx)$. Although the local ratio is $c$, $N_{\rm ph}S(L)/x(L)=c e^{-kL}$. Run **2026-10-13-gpt-a-novelty-premises** checks the formulas against ODE integration. This is a logical test, **not** a demonstrated fiber or quantum counterexample.

Using [Gordon (1986); 10.1364/OL.11.000662](https://doi.org/10.1364/OL.11.000662) (**abstract only**), the shot-noise slope factor equals four only along the fundamental-soliton family with fixed material coefficients, where width varies inversely with energy. It is not automatically the derivative for coherent amplitude noise at fixed launch width. Compute the full input covariance and its transfer; do not subtract correlated contributions as independent variances. Also distinguish the Raman shock time $T_R$ from the inverse Raman resonance frequency: $T_0/T_R$ alone does not specify spectral overlap with the Raman peak.

## Literature state

The complete inherited-source ledger is in [the review](../docs/review-2026-10-13-gpt-a-frequency-conversion-novelty.md).

| Source and identifier | Access | What was checked |
|---|---|---|
| Corney and Drummond (2001), II, [10.1364/JOSAB.18.000153](https://doi.org/10.1364/JOSAB.18.000153) | full text | Direct frequency-coordinate covariance precedes the timing-jitter formula (preprint Eq. 3.15). Analytic treatment neglects deterministic SSFS. |
| Drummond and Corney (2001), I, [10.1364/JOSAB.18.000139](https://doi.org/10.1364/JOSAB.18.000139) | full text | The dissipative Raman susceptibility and thermal/zero-point Langevin spectrum already share a reservoir model (preprint Eqs. 6.11 and 6.16). |
| Kärtner et al. (1994), [10.1364/JOSAB.11.001267](https://doi.org/10.1364/JOSAB.11.001267) | abstract only | Already models SSFS, measured Raman gain and quantum/thermal phonon noise together. The precise projected ratio is unverified without the full text. |
| Kormokar, Shamim and Rochette (2023), [10.1364/JOSAB.478975](https://doi.org/10.1364/JOSAB.478975) | full text | Journal version, arXiv:2301.02945. Interpulse Raman transfer enhances the leading soliton beyond the Raman-independent inverse-scattering energy partition. |
| Shamim, Alamgir and Rochette (2023), [10.1109/JLT.2022.3223802](https://doi.org/10.1109/JLT.2022.3223802) | abstract only | The source of the quoted high-efficiency tuning range. Distinct from the Kormokar fission-efficiency journal paper; pulse compression preserves soliton order. |
| Kormokar, Shamim and Rochette (2021), [10.1364/JOSAB.409240](https://doi.org/10.1364/JOSAB.409240) | full text | Adiabatic, nearly unchirped fundamental-soliton drift including TOD, shock and loss; Sections 2.3–3 derive the reduced law. Section 4.2.2 notes that the ansatz omits dispersive radiation. Not an all-field reach bound or a noise theory. |
| Yang et al. (2021), [10.1038/s41467-021-21658-7](https://doi.org/10.1038/s41467-021-21658-7) | abstract only | Cavity quiet-point noise suppression balances Raman shift and dispersive-wave recoil, with added thermal noise. Relevant precedent for including the dynamical noise transfer. |

The formerly missing fission-efficiency journal paper is [Kormokar, Shamim and Rochette (2023); 10.1364/JOSAB.478975](https://doi.org/10.1364/JOSAB.478975) (**full text**). Its interpulse Raman transfer invalidates use of the Raman-independent fission **energy** partition as a universal photon-efficiency upper bound. The high-efficiency tuning interval attributed vaguely to an associated thesis is directly reported by [Shamim, Alamgir and Rochette (2023); 10.1109/JLT.2022.3223802](https://doi.org/10.1109/JLT.2022.3223802) (**abstract only**), a different paper.

[Yi et al. (2016); 10.1364/OL.41.003419](https://doi.org/10.1364/OL.41.003419) (**full text**) is a driven-cavity analogue. Its [Yi et al. (2016), publisher’s note; 10.1364/OL.41.003722](https://doi.org/10.1364/OL.41.003722) (**full text**) was checked along with the corrected main article: the large-detuning, near-maximum-existence-detuning assumptions restrict quantitative reuse. [Erkintalo, Genty and Dudley (2009); 10.1364/OL.34.002468](https://doi.org/10.1364/OL.34.002468) (**abstract only**) concerns filtered-intensity statistics rather than the proposed centroid quantum floor.

**Searches:** “soliton self-frequency shift quantum frequency jitter”; “Raman soliton drift diffusion”; “Raman soliton fluctuation dissipation frequency”; “Raman soliton Einstein relation”; “soliton frequency variance Raman bound”; “Raman noise and soliton squeezing pdf”; “microcavity quiet point Raman dispersive wave noise”; “Kormokar conversion efficiency journal”.

## Sharpest statement of the gap

Within a stated realizable class of passive silica-fiber profiles, is there a positive lower bound on **final** frequency-centroid variance at fixed shift, length and output soliton efficiency after the full covariance transport is included? If so, what design approaches it; if not, which restoring dynamics or changes of pulse width remove the proposed floor?

The stationary-soliton projection of the known Raman reservoir is a baseline calculation, not a new fluctuation–dissipation principle. What was not located is a theorem or independently validated optimization frontier for this precise restricted final-output problem. Absence of such a source is provisional, particularly until Kärtner 1994 is read in full. A universal $\kappa(\theta,\tau,f_R)$ independent of admissible design has not been justified.

## Conjectures

The original C1 is **superseded**. Its constant-dispersion scaling and its claim about every dispersion profile are separate propositions. Derive and check the first against the published covariance, then assess the second with transported noise in **T-20261013-gpt-a-06**. Fission adds partition and interaction noise and cannot be represented by a fixed inverse-scattering efficiency cap.

## Oracle

The proposal records a partial stochastic/linearized-covariance capability. This audit did not verify the implementation or run stochastic propagation. Before quantitative use, check the symmetrized Raman spectrum, vacuum normalization, selected centroid estimator and time/frequency discretization against the analytic single-soliton baseline. Covariance and stochastic simulations should use the same observable and noise convention.

## Assessment and next step

**Novelty 3/5:** a constrained final-output noise/efficiency frontier could extend known reservoir and soliton-noise theory; the local kernel relation itself is known. **Impact 3/5:** an attainable noise rule would inform source design if the reservoir contribution is experimentally resolvable. Scores are judgments recorded in run **2026-10-13-gpt-a-novelty-literature**.

Claude reconciliation: **T-20261013-gpt-a-02**. Critical full-text closure: **T-20261013-gpt-a-03**. Priority is unchanged.

## Superseded proposal material

The following is retained to preserve the original proposal. Its gap statements, numerical conjectures and access labels are superseded by the current review above; they are not active premises or independently verified numerical evidence.

<details>
<summary>Original proposal, retained for audit</summary>

```yaml
id: P-20261012-claude-interactive.4-02
title: "Fluctuation–dissipation floor on the frequency jitter of soliton self-frequency-shift conversion"
status: candidate
priority: 2
literature_state: partial
novelty_confidence: medium
target_quantity: "The minimum shot-to-shot variance of the centre frequency of a Raman-shifted fundamental soliton at a given self-frequency shift, driven by the quantum and thermal Raman reservoir and by input shot noise, as a lower bound in the soliton photon number, the Raman spectrum and temperature, minimized over input pulse and dispersion profile, together with the trade-off against the photon fraction delivered at the target frequency."
model: "Scalar GNLSE with the measured silica Raman response h_R(t), its symmetrized quantum-thermal Langevin reservoir, Kerr, self-steepening, β2(ω) to third order, optional loss; linearized Gaussian noise about the mean field, or stochastic (Wigner) propagation; coherent input."
oracle_ready: partial
last_audited: null
audited_by: [claude]
proposed_by: claude-interactive.4
provenance:
  agent: claude-interactive.4
  model: claude-fable-5-1
  family: claude
claims: []
results: []
```

### Target quantity

A fundamental soliton of photon number $N_{\rm ph}$ and duration $T_0$ propagates a length $L$ and red-shifts by $\Delta\Omega$ (Gordon's self-frequency shift). Its centre frequency, measured as the spectral centroid of the soliton band, fluctuates shot to shot with variance $\sigma_\Omega^2$. The sources are (i) the Raman reservoir (thermal plus zero-point phonons) acting along the fibre, and (ii) the input photon-number fluctuation transferred through the energy dependence of the shift. Define the dimensionless jitter per unit shift

$$J\equiv\frac{N_{\rm ph}\,\sigma_\Omega^2\,T_0}{|\Delta\Omega|}.$$

**Target.** A lower bound $J\ge\kappa(\theta,\tau,f_R)$ with $\theta=k_BT\,T_0/\hbar$ (classical-to-quantum reservoir parameter; $\theta=1$ at $T_0\approx25$ fs and 300 K) and $\tau=T_0/T_R$, valid for any input pulse and any dispersion profile that produces the shift $\Delta\Omega$ in length $L$, plus the shot-noise transfer term $\sigma_\Omega/|\Delta\Omega|\ge|\partial\ln\Delta\Omega/\partial\ln E|/\sqrt{N_{\rm ph}}$, which is 4 for Gordon's $T_0^{-4}$ law and smaller once the shift saturates. The conjecture behind the bound is that drift and diffusion are moments of the same Raman spectrum, so their ratio is fixed by the reservoir and not by the design.

**Answer form.** $\kappa$ as a closed form in the moments of ${\rm Im}\,\tilde h_R(\Omega)[2n_{\rm th}(\Omega)+1]$ against the soliton spectrum, with limits $\kappa\propto\theta$ (classical reservoir, $\theta\gg1$) and $\kappa\to$ const (zero-point limit); its regime as bounds on $\theta$, $\tau$, $N$ (fission), $\delta_3$ and $s=1/(\omega_0T_0)$; and the three-way frontier among photon efficiency $\eta_{\rm ph}$ (fraction of input photons in the shifted soliton), shift $\Delta\Omega$ and jitter $J$ at fixed $L$.

### Signal of hidden simplicity

- **Drift and diffusion share one kernel.** The mean shift is a first moment of the Raman gain against the intensity spectrum (moment method: Santhanam & Agrawal, Opt. Commun. 222, 413 (2003), DOI [10.1016/S0030-4018(03)01561-X](https://doi.org/10.1016/S0030-4018(03)01561-X), **abstract only**). The reservoir noise projected on the soliton's frequency mode is a zeroth moment of the same gain weighted by $2n_{\rm th}+1$ (Corney & Drummond, below: timing jitter $\langle\Delta\tau^2\rangle=2\mathcal I(t_0)\zeta^3/(3\bar n)$ with $\mathcal I$ the overlap of the pulse spectrum with the Raman fluorescence spectrum). In the classical limit $2n_{\rm th}+1\approx2k_BT/\hbar\Omega$, so the ratio is an Einstein relation with temperature $k_BT$ and "mobility" set by the soliton bandwidth: $J$ should depend on $\theta$ and the Raman line shape only.
- **The $1/N_{\rm ph}$ scaling is already in print** for the reservoir jitter (Corney & Drummond, Eq. 40) and is trivial for the shot-noise transfer. What is missing is the ratio to the shift and its minimization.
- **Classical transfer is known to dominate in practice** (input relative intensity noise times the slope of the shift: Zhou, Xin, Kärtner & Chang, Opt. Lett. 40, 5105 (2015), DOI [10.1364/OL.40.005105](https://doi.org/10.1364/OL.40.005105), **abstract only**), so a floor below it is a design target, not a curiosity: it says how much of the measured jitter a quieter pump can remove.
- No registered run yet; see Oracle.

### Literature state

Searched 2026-10-12 (claude-interactive.4 with helper claude-interactive.4.2): "Raman noise induced frequency jitter soliton self-frequency shift quantum fluctuations spectral diffusion"; "soliton self-frequency shift conversion efficiency limit Raman soliton energy fraction fission photon number"; "timing jitter frequency jitter soliton self-frequency shift source measurement noise Raman soliton relative intensity noise"; "quantum limit fluctuations of soliton self-frequency shift Raman reservoir frequency variance photon number fluctuation-dissipation soliton"; "analytical expression energy conversion efficiency Raman soliton high-order soliton fission interpulse Raman scattering"; title searches. DOIs checked against Crossref; the arXiv full text of Corney & Drummond was read by claude-interactive.4.

Quantum Raman noise on solitons:
- Corney & Drummond, "Quantum noise in optical fibers. II. Raman jitter in soliton communications", JOSA B 18, 153 (2001), DOI [10.1364/JOSAB.18.000153](https://doi.org/10.1364/JOSAB.18.000153), arXiv:quant-ph/9912096. **Full text (arXiv).** Soliton perturbation theory plus phase-space simulations. Bright-soliton Raman timing jitter $\langle[\Delta\tau(\zeta)]^2\rangle_R=2\mathcal I(t_0)\zeta^3/(3\bar n)$ (their Eq. 40), $\mathcal I$ the overlap integral of the pulse spectrum with the Raman fluorescence $[n_{\rm th}(\Omega)+\tfrac12]\alpha^R(\Omega)$ (their Eqs. 7 and 23); thermal and zero-point parts separated. They state that the self-frequency shift is neglected in the analytic calculation and give no relation between the drift and the diffusion. For 500 fs solitons, $\bar n=4\times10^6$, 10 km, Raman jitter exceeds Gordon–Haus jitter by about two.
- Drummond & Corney, "Quantum noise in optical fibers. I. Stochastic equations", JOSA B 18, 139 (2001), DOI [10.1364/JOSAB.18.000139](https://doi.org/10.1364/JOSAB.18.000139), arXiv:quant-ph/9912095. **Full text, sections III and VI** (gpt-b, recorded on P-20261010-claude-interactive-01). Reservoir model used by the solver.
- Kärtner, Dougherty, Haus & Ippen, JOSA B 11, 1267 (1994), DOI [10.1364/JOSAB.11.001267](https://doi.org/10.1364/JOSAB.11.001267). **Abstract only.** Quantized Raman model; Raman noise limits sub-picosecond soliton squeezing.
- Haus & Lai, JOSA B 7, 386 (1990), DOI [10.1364/JOSAB.7.000386](https://doi.org/10.1364/JOSAB.7.000386). **Not accessed.** Linearized soliton quantum theory (no Raman).

Classical shift and jitter:
- Gordon, Opt. Lett. 11, 662 (1986), DOI [10.1364/OL.11.000662](https://doi.org/10.1364/OL.11.000662). **Not accessed.** $d\nu/dz\propto-T_0^{-4}$.
- Santhanam & Agrawal, Opt. Commun. 222, 413 (2003) (above). **Abstract only.** Moment-method shift for arbitrary pulses in both dispersion regimes; saturation with pulse broadening.
- Santhanam & Agrawal, IEEE J. Sel. Top. Quantum Electron. 8, 632 (2002), DOI [10.1109/JSTQE.2002.1016367](https://doi.org/10.1109/JSTQE.2002.1016367). **Abstract only.** Amplifier-noise energy fluctuations converted to Raman-shift fluctuations and timing jitter (classical, seeded by amplified spontaneous emission).
- Zhou et al., Opt. Lett. 40, 5105 (2015) (above). **Abstract only.** Pump relative intensity noise to centre-wavelength and timing jitter of Raman solitons; reduced by shorter, less dispersive fibre.
- Matsuo, Nishizawa, Mori & Goto, Opt. Rev. 7, 317 (2000), DOI [10.1007/s10043-000-0317-1](https://doi.org/10.1007/s10043-000-0317-1). **Abstract only.** Timing jitter about 410 fs rms, intensity noise 0.03% rms, roughly constant over 1600–1750 nm; dominated by the pump.
- Erkintalo, Genty & Dudley, Opt. Lett. 34, 2468 (2009), DOI [10.1364/OL.34.002468](https://doi.org/10.1364/OL.34.002468). **Abstract only.** Input-noise sensitivity of the most red-shifted soliton.

Efficiency:
- Kodama & Hasegawa, IEEE J. Quantum Electron. 23, 510 (1987), DOI [10.1109/JQE.1987.1073392](https://doi.org/10.1109/JQE.1987.1073392). **Not accessed.** Fission partition: the $k$-th soliton holds a fraction $(2N-2k+1)/N^2$ of a sech input's energy.
- Kormokar & Rochette, Optica Advanced Photonics Congress 2022, NpTu4F.7, DOI [10.1364/NP.2022.NpTu4F.7](https://doi.org/10.1364/NP.2022.NpTu4F.7). **Abstract only.** Analytical energy-conversion efficiency of Raman solitons from high-order fission including inter-pulse Raman transfer; 80–85% reported over 1.96–2.14 µm in the associated thesis (McGill, 2025; **abstract only**; journal version not located).
- Chen, Sidorenko, Antonio-Lopez, Amezcua-Correa & Wise, Opt. Lett. 47, 285 (2022), DOI [10.1364/OL.445499](https://doi.org/10.1364/OL.445499), arXiv:2110.12360. **Abstract only.** Hydrogen-filled hollow-core fibre: 240 nJ, 40 fs in; 110 nJ to 20 nJ Raman solitons over 1080–1600 nm.
- Yi, Yang, Yang & Vahala, Opt. Lett. 41, 3419 (2016), DOI [10.1364/OL.41.003419](https://doi.org/10.1364/OL.41.003419). **Abstract only.** Microcavity analogue: Lagrangian formulas for the shift and pump-to-soliton efficiency.
- Bao et al., Nat. Phys. 17, 462 (2021), DOI [10.1038/s41567-020-01152-5](https://doi.org/10.1038/s41567-020-01152-5), arXiv:2003.06685. **Abstract only.** Quantum-limited timing diffusion of microcavity solitons (cognate, not fibre).

**What is solved.** The reservoir timing jitter and its $1/\bar n$, $\zeta^3$ and overlap-integral scaling (Corney & Drummond); the classical transfer of input noise through the shift slope; the fission partition; case-by-case efficiencies. **Not found:** the ratio of reservoir diffusion to the shift it accompanies, any fluctuation–dissipation form, any minimization over input and dispersion profile, and any efficiency–shift–jitter frontier.

### Sharpest statement of the gap

Corney & Drummond give the Raman diffusion of a soliton but neglect the drift; Gordon and the moment method give the drift but not the diffusion. Nobody has written the two as moments of one kernel and asked whether their ratio, $J$, has a design-independent floor. Open: the closed form of $\kappa(\theta,\tau)$; whether $\beta_2(\omega)$ engineering (which changes $T_0$ along the shift) can lower $J$ below the constant-$T_0$ value or only raise it; how fission ($N>1$ inputs, which deliver at most $(2N-1)/N^2$ of the photons to the shifted soliton) adds partition jitter; and the resulting frontier among $\eta_{\rm ph}$, $\Delta\Omega$ and $J$ at fixed $L$. Also open: whether the ratio is universal once the soliton bandwidth overlaps the 13 THz Raman peak ($\tau\lesssim1$), where the shift saturates.

### Conjectures

No claim files yet. The refutable conjecture to register first:

**C1.** For a fundamental soliton with $\tau=T_0/T_R\ge5$, $\theta\ge3$, $f_R=0.18$ and constant $\beta_2$, over any length with $|\Delta\Omega|T_0\le0.5$, the reservoir-driven part of $J$ equals $\kappa_0\,\theta$ with $\kappa_0$ a constant fixed by the silica Raman spectrum, to within 15%, independent of $T_0$, $N_{\rm ph}$ and $L$; and no dispersion profile $\beta_2(z)$ that produces the same $\Delta\Omega$ in the same $L$ gives a smaller value. Refuted by a single stochastic run with $J$ below $0.85\,\kappa_0\theta$ after subtracting the shot-noise transfer, or by a trend of $J$ with $T_0$ at fixed $\theta$.

### Oracle

**Partial.** The solver has single-mode stochastic (Wigner) propagation with the Raman reservoir and the linearized adjoint covariance. Caveats recorded on P-20261010-claude-interactive-01: the default Raman Langevin spectrum halves the zero-point part (T-20261004-gpt-b-02; use the symmetrized spectrum), and the sampled Raman kernel needs time steps of 3 fs or less (T-20261006-claude-interactive-02).

Cheap test: fundamental solitons with $T_0\in\{50,100,200,400\}$ fs at 300 K and 0 K, $L$ up to $5L_D$; compute the centroid variance of the soliton band from the linearized covariance (fast) and from 200 stochastic shots (check); compute $\Delta\Omega$ from the mean field; form $J$ and compare across $T_0$ at fixed $\theta$ (vary $T$ with $T_0$). Then repeat with a linearly increasing $|\beta_2(z)|$ and with $N=1.5$–3 inputs.

Convergence: window large enough that the shed radiation does not wrap; step size such that the centroid variance changes by less than 2%; shot count such that the variance estimate has a standard error below 10%.

Missing: no acoustic (GAWBS) reservoir; no amplifier noise, which the fibre model does not need here.

### Lab test

A tunable soliton source (photonic-crystal or highly nonlinear fibre pumped by a femtosecond oscillator; shifts of 50–200 nm). Record single-shot spectra by dispersive Fourier transform and extract the centroid variance of the Raman soliton at several shifts. Measure the input energy noise and the slope $\partial\Delta\Omega/\partial E$ and subtract the classical transfer. The residual, scaled as $J$, must lie above $\kappa(\theta,\tau)$; cooling the fibre to 77 K changes $\theta$ by a factor 3.9 and is the signature of the reservoir term. A residual below the floor at any shift refutes the bound.

### Risks and must-reads

- **Corney & Drummond's framework may make $\kappa$ a short calculation**, which would make the card's first rung a derivation rather than a discovery; the novelty then rests on the minimization and the frontier. Read their section on the overlap integral in full before deriving.
- **The shot-noise transfer may dominate the reservoir term** for all practical $N_{\rm ph}$, leaving the reservoir floor unmeasurable; the card should then report at which $N_{\rm ph}$ and $\theta$ the two cross.
- **Self-steepening and $\beta_3$** change the shift law and add their own jitter channels; the regime bounds on $s$ and $\delta_3$ are part of the result.
- **Must-reads not accessed:** Gordon (1986); Santhanam & Agrawal (2003) full text; Zhou et al. (2015) full text; Kärtner et al. (1994) full text; the Kormokar–Rochette journal version if it exists.
- Overlap: P-20261004-root-03 and P-20261004-claude-interactive-02 treat collective-coordinate noise of multimode solitons, with frequency jitter as one coordinate; this card is single-mode, sets the drift–diffusion ratio as the target and ties it to conversion. P-20261012-claude-interactive.4-01 supplies the fission and dispersive-wave losses for the efficiency axis.

</details>

## Audit trail


| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-12 | claude-interactive.4 (claude; claude-fable-5-1) | Created as candidate for the PI's frequency-conversion call; literature searched by helper claude-interactive.4.2 and checked against Crossref; Corney & Drummond full text read; no runs yet | Search strings and sources above; task T-20261012-claude-interactive.4-01 |
| 2026-10-13 | gpt-a (gpt; gpt-6-astra) | literature retained partial; novelty confidence → low; added GPT review and revised gap; candidate and priority retained pending Claude concurrence | Cross-family review docs/review-2026-10-13-gpt-a-frequency-conversion-novelty.md; runs 2026-10-13-gpt-a-novelty-literature and 2026-10-13-gpt-a-novelty-premises; follow-ups T-20261013-gpt-a-02, T-20261013-gpt-a-03, T-20261013-gpt-a-06 |
| 2026-10-17 | claude-interactive (claude; claude-opus-5-5) | candidate → parked: merged into P-20261016-claude-interactive-03 (PI decision 2026-10-16); priority unchanged | Task T-20261016-claude-interactive-06, closed in T-20261017-claude-interactive-01; the "Merged cards" section of P-20261016-claude-interactive-03 |
