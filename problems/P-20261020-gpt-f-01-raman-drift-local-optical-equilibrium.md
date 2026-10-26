---
id: P-20261020-gpt-f-01
title: "Raman drift and lifetime of local optical equilibrium in weakly disordered GRIN fibre"
status: audited
priority: 3
literature_state: partial
novelty_confidence: low
target_quantity: "A parameter-derived drift law for the local-RJ multipliers (three global ones only where the joint mode-frequency closure holds; time- or frequency-local spatial multipliers in the picosecond GRIN window) and fixed-band modal fractions of a finite, incoherent ultrashort pulse in weakly disordered GRIN silica fibre, with a quantitative departure criterion and validity length under Raman, imperfect broadband degeneracy and spectral/temporal flux."
model: "Photon-conserving vector multimode GNLSE with modal dispersion, fixed symmetric Kerr/Raman overlap tensors, the physical shock prefactor, and calibrated colored random birefringence; weak non-degenerate leakage and frequency-dependent overlaps are controlled corrections. A local kinetic equilibrium is a hypothesis to test."
oracle_ready: partial
last_audited: 2026-10-20
audited_by: [gpt, claude]
proposed_by: PI
provenance:
  agent: gpt-f
  model: gpt-6-astra
  family: gpt
  date: 2026-10-20
  task: T-20261020-claude-interactive-01
claims: [C-20261020-claude-interactive.21-01]
results: []
---

## Target quantity

For a specified pulse ensemble, fibre, spectral band $B$ and temporal gate $G$, derive the signed evolution of the photon-normalized mode spectrum and the measured band-energy fractions

$$
F_p^{B,G}(z)=
\frac{\int_Gdt\int_Bd\Omega\,(\omega_0+\Omega)n_p(z,t,\Omega)}
{\sum_q\int_Gdt\int_Bd\Omega\,(\omega_0+\Omega)n_q(z,t,\Omega)}.
$$

Here $n_p$ is a coarse-grained local spectrum of photon amplitudes, not a claim that an arbitrary short coherent pulse has a positive stationary Wigner distribution. Begin with a random-phase, weak-wave ensemble with a resolved coherence time $t_c\ll T_{\rm env}$. The first target is a non-condensed local equilibrium, separated from a pole in the RJ denominator. A condensate variable may be added later only after its kinetic coupling and critical slowing have been addressed.

The first answer should be a small ODE system for thermodynamic multipliers in an approximately uniform central temporal gate, with coefficients calculated from measured dispersion, overlap tensors, disorder covariance and the Raman response. Bound the variation of the local multipliers across that gate; averaging distinct local RJ distributions does not generally produce another RJ distribution. If this variation is appreciable, retain $\theta(z,t)$ and its transport terms under P-005. The answer must predict $dF_p^{B,G}/dz$ and the length over which that prediction remains accurate. A separate RJ fit at every distance, an isolated-soliton redshift formula, or a statement that a Raman length is long is insufficient.

### Named physical platform and thermalizing mechanism

Use **weakly perturbed, approximately parabolic, 50-µm-core GRIN silica fibre near 1030–1064 nm**, with normal dispersion, several populated spatial mode groups and both polarizations retained. Pulse durations from the femtosecond to picosecond range and modal decomposition already exist on this platform. Start experimentally with the longer, noise-shaped picosecond pulses if that is where the scale separation can be established. A failure of the required hierarchy for a shorter pulse is a useful outcome.

The thermalizer is **Kerr four-wave exchange between spatial groups, made incoherent by weak, partially decorrelated random birefringence**. It is not linear scrambling alone. A concrete idealized covariance is

$$
C(z)=\bigoplus_j\sum_{\alpha=0}^3\xi_{j\alpha}(z)\sigma_\alpha,\qquad
\langle\xi_{j\alpha}(z)\xi_{k\beta}(z+s)\rangle
=\frac{\sigma_\beta^2}{2}\rho_{jk}\delta_{\alpha\beta}e^{-|s|/\ell_\beta}.
$$

The $\sigma_\alpha$ are Pauli matrices, including the identity; $\rho$ is a positive-semidefinite correlation matrix and must not be assumed fully common to all spatial modes. Define $\Delta\beta=\sigma_\beta^2\ell_\beta$, $L_d=1/\Delta\beta$. In the **spatial discrete-wave limit**, the known scaling is

$$
L_{\rm kin}^{\rm CW}\sim
\frac{L_{\rm NL}^2}{L_d\,\overline{|S_{\rm resonant}|^2}},
\qquad L_{\rm beat}\ll L_d\ll L_{\rm NL},\quad \ell_\beta\ll L_d.
$$

This is a specified rate mechanism, with a measurable noise covariance and a calculable collision operator, not a fitted arbitrary “mixing time.” The actual relaxation length is the inverse gap of the linearized collision operator on its non-conserved subspace. **The CW scaling is a benchmark, not an asserted broadband formula.** Frequency-continuous resonances, disorder broadening and additional invariants can change both the gap and the equilibrium. [Fusaro 2019, DOI:10.1103/PhysRevLett.122.123902](https://doi.org/10.1103/PhysRevLett.122.123902), [Garnier 2019, DOI:10.1103/PhysRevA.100.053835](https://doi.org/10.1103/PhysRevA.100.053835), full text of kinetic/model sections.

In a companion control use Hermitian coupling within exactly degenerate symmetry-partner blocks. The repository's spatial-group Brownian model belongs to this class only in its ideal degeneracy limit. Real GRIN groups have unequal propagation curves; their mismatch and non-degenerate leakage must be measured across $B$. For stationary colored coupling, the linear population-transfer rate has the form

$$
\Gamma_{pq}(\Omega)=
2\operatorname{Re}\int_0^\infty
\langle C_{pq}(0,\Omega)C_{qp}(s,\Omega)\rangle
e^{i[\beta_p(\Omega)-\beta_q(\Omega)]s}\,ds.
$$

Its inter-group graph gap and its propagation-energy drift provide separate leakage limits. [Berti 2022, DOI:10.1103/PhysRevLett.129.063901](https://doi.org/10.1103/PhysRevLett.129.063901), full text of the main model, pp. 1–3.

### Governing equations and invariant ledger

The initial envelope model, in a retarded frame and with $\widetilde A(\Omega)=\int A(t)e^{i\Omega t}dt$, is

$$
\begin{aligned}
\partial_z\widetilde A_p
&=iD_p(\Omega)\widetilde A_p
 +i\sum_q C_{pq}(z,\Omega)\widetilde A_q\\
&\quad+i\gamma_0\left(1+\frac{\Omega}{\omega_0}\right)
\mathcal F\!\left[(1-f_R)F_p^K+f_RF_p^R\right],\\
D_p(\Omega)&=\beta_p(\omega_0+\Omega)-\beta_{\rm ref}-\beta_{1,\rm ref}\Omega,\\
F_p^K&=\sum_{qrs}S^K_{pqrs}A_qA_rA_s^*,\\
F_p^R&=\sum_{qrs}S^R_{pqrs}A_q\,[h_R*(A_rA_s^*)].
\end{aligned}
$$

The index $p$ includes polarization. Use the physical vector Kerr and Raman contractions; a scalar tensor or a single scalar response is a declared reduction. An anisotropic response can require several tensors/kernels. The fixed-overlap approximation assumes weak profile dispersion over the populated band. Arbitrarily replacing $\gamma_0(1+\Omega/\omega_0)$ by a measured $\gamma(\Omega)$ is not an acceptable photon-conserving extension.

For $\psi_p=\widetilde A_p/\sqrt{\omega_0+\Omega}$, let

$$
N=\sum_p\int|\psi_p|^2,\quad
P=\sum_p\int\Omega|\psi_p|^2,\quad
\mathcal E=\omega_0N+P,\quad
H_2=\sum_p\int\epsilon_p(\Omega)|\psi_p|^2,\quad \epsilon_p=-D_p.
$$

Integrals here are over the whole modelled physical band; finite-gate and finite-band quantities have flux terms. Overall Fourier and $\hbar$ factors are suppressed consistently.

| Term/assumption | Invariants and qualifications |
|---|---|
| Autonomous instantaneous vector Kerr, physical shock prefactor, symmetric vertex | $N,P,H=H_2+H_4$, hence optical energy $\mathcal E$. The energy-weighted spectral centroid is generally not conserved. Resonant weak-wave kinetics conserves $H_2$ only to its approximation order. |
| Real higher-order dispersion and deterministic walk-off | Same global invariants; resonance geometry, overlap time and attainable distributions change. |
| Passive frequency-preserving Hermitian random coupling | Conserves total occupation at each $\Omega$, hence $N,P,\mathcal E$ in the linear step. Preserves $H_2$ for every input only when $[C,D]=0$ at every frequency. |
| Quasi-degenerate or non-degenerate coupling | Generally changes $H_2$. Smallness must be measured relative to occupied excitation-energy spread, not the carrier-dominated absolute $\sum\beta n$. Even commuting linear noise can spoil nonlinear Hamiltonian conservation or broaden collision resonances. |
| Causal Raman with photon-conserving normalization | Conserves optical $N$ in the closed optical band, but exchanges optical energy with phonons and changes $P$ and generally $H$. A no-shock Raman truncation has a different exact norm and must not be used to infer broadband energy balance. |
| Frequency-dependent profiles/overlaps | Correct canonical, permutation-symmetric four-frequency vertices can retain the conservative invariants. A naive output-frequency prefactor need not. This extension awaits the 2026 normalization paper. |
| Polarization | Total invariants survive a correct conservative tensor. Individual component powers and Stokes/OAM constraints require symmetries that disorder may break. |
| Loss, radiation, spectral or temporal truncation | Add explicit measured flux/sink terms. A detector band is not a closed thermodynamic system. |

### Regime and scale screen

All inequalities below are proposed acceptance conditions, not an assertion that one published experiment satisfies them simultaneously. Published physical scales and illustrative arithmetic are kept separate.

| Group | Source-supported context; proposed validity requirement |
|---|---|
| $L_{\rm beat}/L_{\rm NL}$, $L_d/L_{\rm NL}$, $\ell_\beta/L_d$ | Garnier 2019 reports sub-mm linear scales and nonlinear lengths above roughly 0.1 m. Its Fig. 2 **model benchmarks**, not measured covariances, use $\Delta\beta=2.6$–42 m$^{-1}$ and $\ell_\beta=0.0047$–0.30 m. Convert and test the hierarchy rather than assuming every benchmark is deeply asymptotic. No measured covariance for the PI's fibre is supplied yet. |
| $L_{\rm kin}/L_{\rm NL}$ | Compute from the collision gap. The CW estimate grows as $L_{\rm NL}/L_d$ times a tensor factor. Ratios 10–100 in the registered scale screen are **illustrative assumptions**, not measured pulsed rates. Pourbeyram's short-fibre relaxation cannot calibrate this different disorder model by itself. |
| $1/(\omega_0T_0)$ | For chosen characteristic $T_0=0.1$–5 ps and 1030–1064 nm, the registered run gives approximately $1.1\times10^{-4}$–$5.7\times10^{-3}$. These $T_0$ values are illustrative characteristic times, not an FWHM conversion. Published pulse-duration context: Mangini 2022, 174 fs–7.6 ps, plus its longer-pulse comparison. |
| $T_R/T_0$, $L_{\rm kin}/L_R$ | The specified $f_R=0.18$, $\tau_1=12.2$ fs, $\tau_2=32$ fs response gives $T_R=f_R\int th_R(t)dt=1.462$ fs in the run; thus $T_R/T_0\simeq2.9\times10^{-4}$–$1.46\times10^{-2}$. Other silica response fits change this moment. Require the actual Raman drift ratio $L_{\rm kin}/L_R\ll1$, not just $T_R/T_0\ll1$. Response source: Baudin 2022, DOI:10.1103/PhysRevA.105.013528, full text. |
| $\Delta\Omega/\omega_0$, $\Delta\Omega\,t_c$ | For the illustrative input convention $\Delta\Omega=1/t_c$ with $t_c$ in the preceding range, the fractional bandwidth equals the shock ratios just listed. An evolved spectrum must be measured independently; require $\Delta\Omega/\omega_0\ll1$ for this envelope expansion. The known generalized UPE is the alternative for a larger band. |
| $L_D/L_{\rm NL}$; $L_D=T_{\rm env}^2/\lvert\beta_2\rvert$ | Pourbeyram 2022 reports approximately 0.5 m versus 0.05 m in its strongest-pulse example. That ratio does not establish $L_{\rm kin}\ll L_D$ here. Require pulse/gate evolution to be slow on $L_{\rm kin}$ or retain its flux explicitly. A temporal coherence length $t_c^2/\lvert\beta_2\rvert$ is a separate scale. |
| $L_{\rm kin}/L_{\rm walk}$; $L_{\rm walk}=T_{\rm env}/\max\lvert\beta_{1p}-\beta_{1q}\rvert$ | Require $\ll1$ for the populated interacting groups, or a controlled transport correction. Krupa 2017, DOI:10.1038/nphoton.2017.32, Methods, estimates 12 ps modal broadening over 12 m at 1064 nm; it neglects this for its 900-ps experiment. This gives a concrete source scale to check, not a universal GRIN delay. Ho–Kahn 2011 gives diffusive delays for **strongly mixed** groups; it does not remove inter-group walk-off in this weak-leakage platform. |
| $M$ and participating groups | Literature platforms support tens to roughly a hundred spatial modes near this wavelength; Pourbeyram distinguishes supported from interacting groups, and Garnier uses a 120-spatial-mode benchmark. Resolve the actual participating set and demonstrate modal-cutoff stability. A few-group analytic reduction is not a physical result until this is checked. |
| $t_c/T_{\rm env}$; $L_{\rm kin}/L_{\rm edge}$ | Require $\ll1$ for a local incoherent closure and slow edge flux, respectively. A transform-limited femtosecond pulse need not satisfy either. Source: stationary-wave assumption in Zanaglia 2026 and pulse limitations in Ferraro et al. 2025. |
| Disorder leakage / broadening | Require $L_{\rm kin}/L_H\ll1$, with $L_H=N\Delta\epsilon_{\rm occ}/\lvert\partial_zH_2\rvert_{\rm disorder}$ and a separately controlled occupation-redistribution rate. Evaluate both direct noncommuting coupling and broadened nonlinear resonances. |
| HOD and overlap dispersion | In a perturbative treatment require $\lvert\beta_3\rvert\Delta\Omega/(3\lvert\beta_2\rvert)\ll1$ and a small relative four-frequency-vertex change. Near zero dispersion or mode cutoff use full measured curves; no constant typical value is assumed. Poletti–Horak 2008 and Lægsgaard 2007 motivate these corrections; access limits are below. |
| $W_t=t_c^2/(\lvert\beta_2\rvert L_{\rm NL})$ (added 2026-10-20, claude-interactive.21) | Temporal weak-turbulence parameter. The Raman kinetic equations this card builds on assume $W_t\ll1$: Baudin 2022 requires $L_{\rm lin,2}=2t_c^2/\tilde\beta\ll L_{\rm nl}$, and Xu 2014 and arXiv:2610.23061 require $t_c\ll\tau_0=\sqrt{\beta L_{\rm nl}}$. Zanaglia 2026's simulations start at $W_t=1$–6. For 50-µm GRIN at 1064 nm with effective overlap 0.3, $W_t=21$, 210 and 1470 at $t_c=1$ ps for 1, 10 and 70 kW, and $\sqrt{\lvert\beta_2\rvert L_{\rm NL}}=218$, 69 and 26 fs. Run [2026-10-20-claude-interactive.21-regime-screen](../runs/2026-10-20-claude-interactive.21-regime-screen/summary.json). |
| $R_{\rm ST}=\kappa/(t_c^2\delta\beta)$, $\kappa=\beta_2/2$ (added 2026-10-20) | Spatio-temporal resonances between non-degenerate groups need frequency offsets $\sqrt{\delta\beta/\kappa}$. That is $2\pi\times130$ THz (a 490-nm span) for $\delta\beta=5519$ m⁻¹, so $R_{\rm ST}\le1.5\times10^{-2}$ for every $t_c\ge10$ fs. Same run. |
| $L_{\rm kin}/L_{\rm th}$, $L_{\rm th}=16/(2\gamma f_R\,{\rm max\,Im}\tilde h\,P)$ (added 2026-10-20) | Noise-seeded SRS threshold at the gain peak: $L_{\rm th}\approx31L_{\rm NL}$ for the card's response, at any power. Where Garnier's $L_d\ll L_{\rm NL}$ holds, $L_{\rm kin}/L_{\rm th}=2.7$–400. Require $L_{\rm kin}\ll L_{\rm th}$, or pump–Stokes walk-off $T_{\rm env}/(\lvert\beta_2\rvert\Omega_R)$ (0.74 m per ps of envelope) shorter than $L_{\rm th}$. Same run (`srs`). |
| $R_d=\kappa/(t_c^2\Delta\beta)$ (added 2026-10-20) | Frequency mismatch relative to the disorder width. $R_d\ll1$ (here $t_c\gtrsim200$ fs for the Garnier benchmarks) means the disorder-broadened resonance does not resolve frequency, so the dispersion part of $H_2$ is not a kinetic invariant. Same run. |

The arithmetic of the original rows is in [run 2026-10-20-gpt-f-thermodynamic-ledger](../runs/2026-10-20-gpt-f-thermodynamic-ledger/summary.json). The rows added by claude-interactive.21 cite [run 2026-10-20-claude-interactive.21-regime-screen](../runs/2026-10-20-claude-interactive.21-regime-screen/summary.json). Neither run establishes an experimental hierarchy. Establishing a nonempty parameter window is part of the problem.

### First concrete derivation target

1. *(Superseded for the picosecond window, 2026-10-20, claude-interactive.21; kept for the record.)* ~~Use the known photon-amplitude RJ family on a fixed diagnostic band,
   $n_{\theta,p}=1/(\theta_0+\theta_1\Omega+\theta_2\epsilon_p)$, away from its poles. Check that the proposed fast collision operator has only the intended conserved moments $q=(1,\Omega,\epsilon)$ in this regime. Keep a possible residual resonant invariant as a failure mode.~~
   **Answer, and corrected item 1.** The three-moment null space holds only in a joint regime with $W_t\ll1$ and $R_{\rm ST}\sim1$. That regime does not occur in 50-µm GRIN at 1 µm (regime rows above). For $R_d\ll1$ and $W_t\gg1$, i.e. picosecond pulses, the fast operator conserves the photon number and transverse energy $H_\perp=\sum_p\epsilon^\perp_p\tilde N_p$ of each time slice, or of each frequency when $R_d\gg1$ and $W_t\ll1$. The local equilibrium is a spatial RJ state with multipliers $\theta_{0,2}(t)$ or $\theta_{0,2}(\Omega)$. Use that manifold, with transport in $t$ handled under P-005 where it matters. Exploration note [2026-10-20-claude-interactive.21-raman-parity-selection](../explorations/2026-10-20-claude-interactive.21-raman-parity-selection.md), §2.
2. Derive the Gaussian-ensemble Raman moment sources $F_{R,i}=\sum_p\int_Bq_i\mathcal C_R[n_\theta]_p\,d\Omega$ **with the intermodal tensor and physical frequency factors**. Begin with fixed overlaps and the short-response limit, then compare with the full measured Raman kernel. Recover the scalar optical-energy balance
   $d\mathcal E/dz=-(\gamma T_R/\omega_0)\int(\partial_t|A|^2)^2dt+\cdots$ when that reduction applies.
3. With $Q_i=\sum_p\int_Bq_in_{\theta,p}$ and
   $\chi_{ij}=\sum_p\int_Bq_iq_jn_{\theta,p}^2$, derive
   $-\chi\,\theta'=F_R+F_{\rm disorder}-\Phi_B-\Phi_G$.
   This is a proposed moment projection, not yet a closed prediction: the fluxes and kinetic gap need independent control.
4. Compute the leading non-equilibrium residual from the inverse linearized Kerr operator on the moment-orthogonal subspace. State a norm, a tolerance and a length at which the predicted $F_p^{B,G}$ fails. Obtain a signed modal response; do not assume $F_{01}$ increases.
5. *(Added 2026-10-20, claude-interactive.21.)* **Time-reversal selection rule.** $A(t)\to A(-t)$ maps the model with Raman response $h(t)$, shock $s$ and odd dispersion/walk-off to $h(-t)$, $-s$ and reversed odd terms. For time-symmetric launches, the first-order Raman-gain change of every time-even observable (modal fractions, $F_p^{B,G}$ on a symmetric band and gate) therefore vanishes. The leading terms are Raman × (shock, walk-off, $\beta_3$) and Raman². On a parity-symmetric RJ state the projected drift is a pure frequency boost at fixed modal fractions. Claim [C-20261020-claude-interactive.21-01](../claims/C-20261020-claude-interactive.21-01-time-reversal-selection-rule-raman-modal.md); the first-order closed form and the second-order sign rule are in the exploration note, §3. Item 4's "signed modal response" must be computed at second order in parity-odd parameters. Two pre-registered toy tests (three and four groups, $\le30L_{\rm NL}$; exploration note §6b) gave a first, inconclusive look. Kerr reduced the Raman-driven inter-group frequency offsets by a factor of 2–5 within a few $L_{\rm NL}$ and roughly halved the fundamental's Raman² gain, before the group populations relaxed. Whether full Kerr relaxation changes its $z^2$ growth is open (T-20261020-claude-interactive.21-04).

This target can begin symbolically before a disorder propagator is built. A first result might show that no useful slow manifold exists in a specified femtosecond regime. That is preferable to a fit presented as a thermodynamic law.

### Ultraviolet treatment

The band $B$ is a physical measurement band, with explicitly measured or bounded flux across its edges. It is not the numerical FFT cutoff. A quadratic-dispersion classical RJ tail has finite norm but divergent propagation energy on an unlimited temporal continuum. Use local equilibrium behind an expanding spectral front, following the 2026 baseline, and retain front/gate flux if it competes with Raman. Do not impose a global canonical classical state. If low-occupancy tails require quantum BE physics, hand that extension to the quantum problem.

The finite classical norm refers to photon occupation in this normalization. Formally extending its quadratic RJ tail with the shock energy weight to arbitrarily high positive frequency also gives a divergent optical-energy integral; the narrowband shock approximation is itself invalid there.

In the convention $\epsilon_p=\epsilon_{p,\perp}-\kappa\Omega^2$, normal dispersion $\kappa>0$ favours the negative-temperature branch of the joint continuum theory. Consequently this card promises neither fundamental-mode joint condensation nor a positive temperature for normal-dispersion silica.

## Signal of hidden simplicity

Known Kerr kinetic equations have a small set of collision invariants; known Raman kinetic equations have explicit gain kernels and moment balances. If one operator relaxes rapidly and the other perturbs it slowly, a susceptibility matrix can determine the motion of the multipliers. The hidden-simplicity hypothesis is that the **transverse** Raman residual remains controlled long enough for this low-dimensional prediction to be useful.

This is conditional, not an observation of a new plateau. The registered scale screen shows why the distinction matters: a small Raman correction per nonlinear length can accumulate to order unity by the putative thermalization length.

## Literature state

- **Already solved ingredients:** generalized spatiotemporal kinetics, canonical shock weighting, RJ invariants and local UV cooling in Zanaglia et al., [DOI:10.1103/mqzh-w2gh; arXiv:2506.23536v2](https://arxiv.org/abs/2506.23536), **full text including appendices**. The stationary, non-degenerate-mode derivation is not the present finite-pulse disorder problem.
- **Equilibrium quantum completion and dispersion-sign warning:** Zanaglia et al., [arXiv:2512.07784](https://arxiv.org/abs/2512.07784), **full text, model/equilibrium/discussion sections**. It explicitly identifies disorder and Raman as further issues.
- **Shock thermodynamics is prior work:** Barviau et al., [DOI:10.1103/PhysRevA.79.063840](https://doi.org/10.1103/PhysRevA.79.063840), **abstract only**; derivation also read in Picozzi et al., [DOI:10.1016/j.physrep.2014.03.002](https://doi.org/10.1016/j.physrep.2014.03.002), **full text, selected passages in §§3, 5.4, 6, 7**.
- **Closest Raman kinetic comparator:** Baudin et al., [DOI:10.1103/PhysRevA.105.013528; arXiv:2111.05744](https://arxiv.org/abs/2111.05744), **full text, kinetic derivation and discussion**. Strong all-mode coupling yields a different leading kinetic ordering, not fast Kerr RJ plus weak Raman.
- **Pulse observations and limitations:** Pourbeyram et al., [DOI:10.1038/s41567-022-01579-y](https://doi.org/10.1038/s41567-022-01579-y); Mangini et al., [DOI:10.1364/OE.449187](https://doi.org/10.1364/OE.449187); Ferraro et al., [DOI:10.1016/j.physd.2025.134758; arXiv:2505.11299](https://arxiv.org/abs/2505.11299). **Full text, experiments and relevant theory sections.** Spatial distributions and detector averaging do not prove full pulse equilibrium.
- **Alternative distributions and disorder caveat:** Zitelli et al., [DOI:10.1038/s41467-024-45185-3](https://doi.org/10.1038/s41467-024-45185-3), **full text, entropy/model/experiment sections**; Zitelli, [arXiv:2601.16998](https://arxiv.org/abs/2601.16998), **full text, model/results/discussion**. Their weighted-BE descriptions must be compared, with group degeneracy, radiative/loss channels and flux normalization explicit.
- **Photon normalization beyond constant overlaps:** Bonetti et al., [DOI:10.1364/JOSAB.377891](https://doi.org/10.1364/JOSAB.377891), **full text, conservation/model sections**. Timmerkamp–Fallnich, JOSA B 43(8), 1819 (2026), [DOI:10.1364/JOSAB.603100](https://doi.org/10.1364/JOSAB.603100): ~~not accessed~~ **abstract only** (Crossref publisher metadata, read by claude-interactive.21 on 2026-10-20). The paper gives a multimode NLSE for arbitrary nonlinear dispersion that conserves energy and photon number, tested on two-mode self-steepening and intermodal XPM. It is a model check for the frequency-dependent-overlap extension, not a narrowing of the gap.
- **Regime assumptions of the baselines (second-family check, 2026-10-20, claude-interactive.21; full-text passages).**
  - Baudin 2022 derives its Raman kinetics for $W_t=t_c^2/\lvert\beta_2\rvert L_{\rm NL}\ll1$; so does Xu 2014.
  - Zanaglia 2026 assumes statistically stationary CW input, starts its simulations at $W_t\approx1$–6, and notes that ideal parabolic fibres freeze spatial thermalization unless weak disorder is added.
  - Garnier 2019 is quasi-CW and explicitly excludes femtosecond self-cleaning.
  - Pourbeyram 2022 tests RJ on frequency-integrated mode-group occupancies. At 70 kW and about $30L_{\rm NL}$ it reports SRS spectral asymmetry while the LP01 occupancy keeps its equilibrium value.
- **New (located 2026-10-20):** Zanaglia et al., [arXiv:2610.23061](https://arxiv.org/abs/2610.23061) (16 Oct 2026), **full text, passages**. Local-RJ adiabatic cooling $T^{\rm loc}\sim z^{-1/7}$ and self-polarization of temporally incoherent light in weakly birefringent single-mode fibre, with weak-turbulence condition $t_c\ll\sqrt{\beta L_{\rm nl}}$. No Raman, no random coupling, no spatial modes. It narrows the cooling baseline, not the Raman gap.
- **Barviau 2009 access:** the HAL records hal-00447568 and hal-00449139 are metadata-only notices (HAL API), so no open full text exists there.

The full source ledgers and literal queries are in [the first-family review](../docs/review-2026-10-20-gpt-f-ultrashort-optical-thermodynamics.md) and [the second-family review](../docs/review-2026-10-20-claude-interactive.21-ultrashort-thermo-second-family.md). Priority 3 and low novelty confidence reflect substantial adjacent theory, incomplete access to several normalization/Raman papers, and the unproven scale hierarchy.

## Sharpest statement of the gap

For this specified disorder model and finite band/gate, derive the **coefficient and sign of the Raman-induced change of modal fractions while a local Kerr equilibrium persists**, and quantify when that reduction fails. The literature searches did not locate this combined prediction with controlled residual and boundary flux. A generic kinetic closure for finite envelopes, a known shock RJ formula, and a fitted weighted-BE output distribution are outside the claimed gap.

### Relation to neighbouring cards

- **P-005:** owns finite-envelope kinetic closure and collision/dilution competition. This card takes a justified local collision operator as input and asks for its Raman perturbation/lifetime. If developing that operator is the only new work, consolidate it into P-005. Its status is unchanged.
- **P-010:** owns operational cleaning thresholds and detector-defined crossovers. This card predicts changes of a specified modal distribution, not the cleaning threshold.
- **P-20261016-claude-interactive.7-01:** owns quantum states and counting statistics. This card is classical, high occupation, and makes no inference about purity or thermal photon-number statistics.
- **P-20261002-gpt-a-03/P-013:** retain phase-coherence dynamics and supercontinuum noise, respectively. No new noise claim is made here.

## Conjectures

- [C-20261020-claude-interactive.21-01](../claims/C-20261020-claude-interactive.21-01-time-reversal-selection-rule-raman-modal.md) (`cheap-checks-passed`, claude family; needs non-claude verification):
  - Time-reversal selection rule: for time-symmetric launches, the Raman gain changes time-even observables, including modal fractions, only at second order in parity-odd parameters.
  - The first-order Raman modal photon transfer of a stationary Gaussian multimode field, in closed form, as a functional of the energy spectra.
  - The second-order sign rule.

The projected drift on a time- or frequency-local manifold and the inverse-collision-operator correction remain derivation targets. Their accuracy and physical parameter window are unverified.

## Oracle

**Partial**, at agents-copy solver commit `b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa`.

Present: modal dispersion and walk-off, vector/component overlap tensors, deterministic Kerr and Raman (`AgarwalRaman`, `AnisotropicRaman`), and deterministic multimode self-steepening through the `omega + omega0` nonlinear prefactor in `src/mmgnlse_solver.jl`. The lead that shock exists only in experimental/stochastic backends was incorrect.

Missing: a calibrated colored Hermitian linear-coupling operator, its frequency correlation and vector covariance, a consistent Raman kinetic evaluator, band/gate flux diagnostics, and a general four-frequency overlap vertex. The spectral damping window also requires an interior-band/refinement check before exact continuum invariants are inferred.

The first cheap checks are symbolic moment conservation, the scalar Raman balance, and whether the assumed collision null space/gap is correct. Future propagation checks should vary Raman strength, bandwidth, disorder covariance and group mismatch independently, score held-out launches, and show convergence in temporal window, frequency grid, propagation step and mode count. At least one relaxed assumption must be tested. No such simulation has been performed for this card.

All future solver changes belong in `FastDifferentiableMMNLO-agents`; the original solver repository remains read-only.

## Lab test

Prepare a reproducible ensemble with controlled modal occupations and short temporal coherence, measure the linear disorder covariance/delay statistics at low power, and use fibre cut-backs to obtain frequency-resolved modal energies and the output pulse envelope. Declare the same band and gate before the nonlinear comparison.

A cheap symmetry test comes first (claim C-20261020-claude-interactive.21-01). Launch the same field with spectral phase $+\phi_3\Omega^3$ and $-\phi_3\Omega^3$. The output modal fractions can differ only through parity-odd physics (Raman gain, shock, walk-off, $\beta_3$). For a time-symmetric launch, Raman enters the modal fractions only at second order in those parameters.

The measurable prediction is the **signed slope and length dependence of $F_{01}^{B,G}$ and higher-group fractions**, together with spectral photon-centroid drift, from initial moments and independently calibrated coefficients. Compare this against a frozen-RJ prediction and against direct Raman overlap-gain dynamics. Repeat with changed pulse coherence time and disorder strength. The predicted loss of local equilibrium must track those changes; moving a detector edge must give the separately predicted flux contribution.

## Risks and must-reads

No useful separation may exist for the shortest pulses. For quasi-CW pulses, noise-seeded Stokes generation at 13 THz reaches threshold, at $\approx31L_{\rm NL}$, before weak-disorder Kerr thermalization; the in-band kinetic model omits it unless a noise floor is included (added 2026-10-20). Disorder that accelerates decorrelation may also destroy the conserved propagation energy or suppress inter-group nonlinear exchange. Residual resonant invariants, coherent locking, condensation, Raman solitons and large band flux can require more variables.

The scalar shock RJ formula is already known, and a first-order odd spectral correction may cancel in a symmetric band-integrated modal fraction. Redshift does not imply cooling in optical temperature or increasing fundamental occupation. A unitary linear mixing model cannot move a complete uniform incoherent modal covariance away from itself; reconcile the January 2026 non-uniform-disorder paper before adopting its stationary law.

Full-text priorities: Blow–Wood 1989 (photon/energy balance), Barviau 2009 (shock/HOD equilibrium), Poletti–Horak 2008 and Lægsgaard 2007 (broadband normalization), Antonelli–Mecozzi–Shtaif 2013 (group-averaged Raman tensor), and Timmerkamp–Fallnich 2026 (multimode photon-conserving extension). Access status and download tasks are in the review.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-20 | gpt-f (gpt; gpt-6-astra) | Created one PI-proposed candidate; partial literature, low novelty confidence, no claims or propagation runs | T-20261020-claude-interactive-01 review and source ledger; symbolic run 2026-10-20-gpt-f-thermodynamic-ledger. Second-family review is the existing T-20261020-claude-interactive-02. |
| 2026-10-20 | claude-interactive.21 (claude; claude-opus-5-5) | **Second-family literature check: candidate → audited; audited_by [gpt] → [gpt, claude].** The two families agree on what is open. Priority 3, `literature_state: partial` and `novelty_confidence: low` are unchanged. | [Second-family review](../docs/review-2026-10-20-claude-interactive.21-ultrashort-thermo-second-family.md): primary-source re-reading of every load-bearing statement; 6 own queries plus 71 helper queries; new source arXiv:2610.23061; Barviau 2009 HAL records are metadata-only; Timmerkamp–Fallnich abstract read. |
| 2026-10-20 | claude-interactive.21 (claude; claude-opus-5-5) | **Regime and derivation-target correction; literature bullets added; access levels updated; claim linked.** Added $W_t$, $R_{\rm ST}$, $R_d$ rows. Marked derivation item 1 superseded for the picosecond window and stated the time-/frequency-local null space. Added item 5 (time-reversal selection rule). Updated `target_quantity`. Added the $\pm\phi_3$ symmetry test to the lab section, an SRS-threshold row and risk, and the toy clamp-test summary in item 5. Scope recommendation: a separate card for the coherent femtosecond regime, after scoping (task T-20261020-claude-interactive.21-01). | Runs `2026-10-20-claude-interactive.21-regime-screen`, `2026-10-20-claude-interactive.21-raman-parity` and `2026-10-20-claude-interactive.21-raman-clamp`; exploration note `explorations/2026-10-20-claude-interactive.21-raman-parity-selection.md`; claim C-20261020-claude-interactive.21-01. |
