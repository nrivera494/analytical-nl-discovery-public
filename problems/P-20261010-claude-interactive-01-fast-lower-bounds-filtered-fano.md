---
id: P-20261010-claude-interactive-01
title: "Fast, tight lower bounds on filtered Fano factors in nonlinear fibre"
status: candidate
priority: 1
literature_state: unaudited
novelty_confidence: low
target_quantity: "A formula, evaluable much faster than a simulation, that lower-bounds the photon-number Fano factor reachable with any binary spectral filter (mode-selective or not), and with other readouts, at the output of a fibre with general dispersion, self-steepening, polarization, several spatial modes and Raman response, in terms of material, fibre and pulse parameters, with its gap to the simulated optimum stated over a regime."
model: "Multimode, two-polarization GNLSE with Kerr overlap tensor, modal dispersion beta_m(omega) to all orders, self-steepening, causal Raman response (isotropic and anisotropic parts) and its symmetrized thermal reservoir; coherent input; linearized Gaussian quantum noise about the classical mean field; passive binary spectral filter (optionally per mode and polarization) followed by photon counting, or interference with a coherent reference."
oracle_ready: partial
last_audited: null
audited_by: []
proposed_by: PI
provenance:
  agent: claude-interactive
  model: claude-opus-5-5
  family: claude
claims: [C-20261010-claude-a-01, C-20261010-claude-a-02, C-20261010-claude-a-03, C-20261010-claude-b-01, C-20261010-claude-b-02, C-20261010-claude-b-03, C-20261010-gpt-b-01, C-20261010-gpt-b-02, C-20261019-pi-chatgpt-01, C-20261019-claude-interactive.12-01]
results: [R-0012, R-0013, R-0015]
---

## Target quantity

**The PI's question (2026-10-10).** Suppose I launch a Gaussian pulse of given peak power, duration and centre wavelength into a fibre whose index profile $n(r,\lambda)$ and length are known. I then apply whatever spectral filter I like (any wavelength-dependent pattern of 1s and 0s, optionally per mode or polarization) and count photons. What is the best Fano factor, and so the best squeezing, I can expect to see?

The goal is a formula $F_{\rm LB}(\text{material},\text{fibre},\text{pulse})$ such that:
- **It is a lower bound:** $F_{\rm LB}\le\min_{T}F[T]$. It is either rigorous within the stated model, or asymptotically rigorous with a stated error order.
- **It is fast:** closed form, or one-dimensional integrals and small linear algebra, with no propagation of noise. A single deterministic mean-field propagation may be allowed if the formula says so.
- **It is tight:** its gap to the simulated optimum over binary filters is stated (in dB) over a stated regime, including held-out fibres and pulses.

**Inputs.**
- Material: $n_2$, Raman response $h_R(t)$ (isotropic and anisotropic parts), temperature.
- Fibre: the modes and $\beta_m(\omega)$ from $n(r,\lambda)$, Kerr and Raman overlap tensors, birefringence, length $L$.
- Pulse: shape (Gaussian first), $P_0$, $T_0$, $\lambda_0$.

**Order of work.**
1. Scalar single-mode fibre, one polarization, spectral filtering.
2. Add Raman (deterministic delayed response and its reservoir), self-steepening, and general dispersion: both signs of $\beta_2$, $\beta_3$, a dispersion zero.
3. Add polarization: vector Kerr and birefringence.
4. Add several spatial modes, with mode-selective and non-selective filters.
5. Other readout families: interference with a coherent copy of the input (P-20261004-root-03 readout (b)), and mode-resolved weighted counting. This rung also carries the readout subtargets of the superseded P-20261004-root-04: finite coherent references (power, delay, overlap, combiner vacuum), partially transmitting masks and apertures, polarization-resolved collection, and correlated phonon floors.

**PI decisions (2026-10-10, after the card was created).**
- This card supersedes P-20261004-root-04, which stays parked with a pointer here.
- The order of work above is approved. Priority 1; four agents are assigned (see Approaches).
- A useful bound must beat $\lambda_{\min}(V)$, but every result must still say where $\lambda_{\min}(V)$ sits. Its gap to the filter optimum is informative in its own right: it shows whether the field holds squeezing that filtering wastes, and so whether a readout that steers phase into amplitude would be worth building.

**A structure to start from.** These are standard relations in linearized theory; they need checking in this setting.
- **The readout as a quadrature.** For a binary filter $T_i\in\{0,1\}$ over spectral (and mode) bins with mean photon numbers $\bar n_i$ and photon-number covariance $\Sigma$, $F[T]=T^{\mathsf T}\Sigma T/T^{\mathsf T}\bar n$. Because $T_i^2=T_i$, the denominator equals $T^{\mathsf T}\mathrm{diag}(\bar n)T$.
- **Generalized-eigenvalue bound.** It follows that $\min_TF[T]\ge\lambda_{\rm gen}$, the smallest generalized eigenvalue of $(\Sigma,\mathrm{diag}\,\bar n)$. That is the optimum over arbitrary real weights on the bins.
- **Smallest-eigenvalue bound.** In the bright-field linearization, filtered photon counting measures the amplitude quadrature with a local oscillator equal to the filtered mean field. Hence $\lambda_{\rm gen}\ge\lambda_{\min}(V)$, the smallest eigenvalue of the output quadrature covariance (shot noise = 1), taken over all modes.
- **Chain.** So $\lambda_{\min}(V)\le\lambda_{\rm gen}\le\min_TF[T]$. Both bounds need the linearized covariance, which costs about one adjoint-type computation. That is far cheaper than optimizing filters, but it is not yet a fast formula.
- **Readout hierarchy (to be proved; T-20261010-claude-interactive-03).**
  - $\lambda_{\rm gen}=\lambda_{\min}(V^{\rm amp})$, where $V^{\rm amp}$ is $V$ restricted to the local amplitude quadratures, one per bin, each with its local-oscillator phase equal to the local mean phase. It is the limit for bin-resolved counting with real post-detection weights.
  - Let $\lambda_{\rm pass}$ be the smallest eigenvalue of $V$ restricted to the hyperplane orthogonal to one direction, the global phase quadrature $i\bar\alpha$ of the mean field.
  - Photon counting on one output port of any passive linear network (an interferometer, or a spectral phase followed by a time gate) measures a quadrature in that hyperplane, and every direction in it can be reached. So $\lambda_{\rm pass}$ is the limit for passive linear optics plus counting, a self-homodyne readout. By interlacing it lies between the two smallest eigenvalues of $V$, so it usually sits close to $\lambda_{\min}(V)$.
  - Together: $\lambda_{\min}(V)\le\lambda_{\rm pass}\le\lambda_{\rm gen}\le\min_TF[T]$. The orchestrator checked this on one random six-mode covariance (a scratch check, not a run); it needs a proof.
- **What the gaps mean.**
  - A large ratio $\lambda_{\rm gen}/\lambda_{\rm pass}$ means the squeezing sits in local phase quadratures. Only a readout that rotates phase into amplitude reaches it; a spectral phase followed by a filter in the same bins does not change the bin counts.
  - A large ratio $\min_TF/\lambda_{\rm gen}$ means binary weights lose; weighted multi-pixel counting would recover it.
- **Required reporting.** Every candidate formula, and every computed point used to score one, reports $\lambda_{\min}(V)$, $\lambda_{\rm gen}$ and the best binary filter found, and $\lambda_{\rm pass}$ where it is cheap. Give the gaps in dB and say how the binary search was done.
- **What the formula should do.** Bound $\min_TF$ from below more tightly than $\lambda_{\min}(V)$, analytically, and state how far it sits below what a filter can reach.

**One closed-form anchor.** In the dispersionless scalar Kerr limit each time slice is a single-mode Kerr medium. The linearized shear $X_2\to X_2+2\Phi X_1$ gives minimum quadrature variance $V_{\min}(\Phi)=1+2\Phi^2-2\Phi\sqrt{1+\Phi^2}\approx1/(4\Phi^2)$. Taking the slice at the peak gives $\lambda_{\min}(V)=V_{\min}(\Phi_{\rm peak})$, with $\Phi_{\rm peak}=\gamma P_0L$.

Spectral filtering has to turn that phase–amplitude correlation into photon-number correlation. It can do so through dispersion, or through the filter itself, which mixes differently chirped instants. How well it does is not known. The gap between $V_{\min}(\Phi_{\rm peak})$ and the best filter is therefore itself a target. Raman noise grows with propagation and should impose a floor; a trade-off between Kerr shear and Raman noise suggests a scaling form, but none is claimed here.

**Answer form.** A formula with its regime as bounds on dimensionless groups:
- $\Phi_{\rm peak}$, $L/L_D$ and $N^2=L_D/L_{NL}$;
- $f_R$, the thermal occupation at the Raman frequencies, and $T_R/T_0$;
- $1/(\omega_0T_0)$ for self-steepening, and $\beta_3$ through $\delta_3$;
- the mode count and overlap matrix, modal walk-off $\delta_m$, and birefringence beat length against $L_{NL}$;
- linearization validity: nonlinear phase spread $\Phi/\sqrt{N_{\rm ph}}\ll1$.

Report the gap to the simulated optimum.

## Signal of hidden simplicity

- **Few groups.** In linearized theory the Fano factor does not depend on photon number. It depends only on dimensionless groups (P-20261004-root-03, Find), so a formula in a few groups is plausible.
- **Raman sets the floor in the computed LP01 cases.** At 1550 nm in GIF625 over 20 m, the archive's coherent-reference readout gives $F=0.0323$ (oscillator Raman) and $0.0529$ (anisotropic Raman). The Raman reservoir accounts for 61% and 74% of $F$; a fixed bandpass gives 0.370 and 0.415 (runs `2026-10-04-claude-b.1-prepared-sech-readout-20m`, `2026-10-04-claude-b.1-bandpass-1546-1553-20m`).
- **The optimal binary filter is structured.** In the solver's squeezing notebook (anomalous dispersion, 0.22 ps soliton), the optimal binary filter reaches about −5.3 dB on a converged grid. Most residual noise comes from input vacuum on the Raman Stokes side (run `2026-10-05-claude-interactive-raman-stochastic`, `convergence/`). A bound built from a few spectral regions may capture it.
- **Multimode adds little at second order.** For common-filter photon counting the multimode launch differs from LP01 only at second order in the overlap defect (C-20261008-claude-b-01, proposed). That suggests the multimode bound may reduce to the scalar one plus a small, structured correction for non-selective filters.

## Literature state

Not yet audited. Starting points, with identifiers and access levels as recorded on other cards:
- **Optimal and scalar filtering.**
  - Levandovsky, Vasilyev & Kumar, OL 24, 43 (1999), [DOI:10.1364/OL.24.000043](https://doi.org/10.1364/OL.24.000043): analytic amplitude-quadrature correlator with the continuum, numerically optimized filter. **Abstract only.**
  - Werner & Friberg, [arXiv:quant-ph/9904104](https://arxiv.org/abs/quant-ph/9904104): optimal filter edge and 4.8 dB filtered squeezing with Raman at 300 K. **Full text, skimmed** (claude-b, P-20261004-root-03).
  - Mecozzi & Kumar, OL 22, 1232 (1997), [DOI:10.1364/OL.22.001232](https://doi.org/10.1364/OL.22.001232): linearized theory of spectrally filtered solitons. **Not accessed.**
- **Experiments.**
  - Friberg et al., PRL 77, 3775 (1996), [DOI:10.1103/PhysRevLett.77.3775](https://doi.org/10.1103/PhysRevLett.77.3775). **Abstract only.**
  - Spälter et al., PRL 81, 786 (1998), [DOI:10.1103/PhysRevLett.81.786](https://doi.org/10.1103/PhysRevLett.81.786): spectral photon-number correlations. **Abstract only.**
  - König et al., J. Mod. Opt. 45, 2425 (1998), [DOI:10.1080/09500349808230495](https://doi.org/10.1080/09500349808230495): photon-number squeezing in normal dispersion. **Abstract only.**
  - Nishizawa et al., Jpn. J. Appl. Phys. 38, 1961 (1999), [DOI:10.1143/JJAP.38.1961](https://doi.org/10.1143/JJAP.38.1961). **Abstract only.**
- **Raman and polarization limits.**
  - Kärtner, Dougherty, Haus & Ippen, JOSA B 11, 1267 (1994), [DOI:10.1364/JOSAB.11.001267](https://doi.org/10.1364/JOSAB.11.001267): Raman noise limits squeezing of sub-picosecond solitons. **Abstract only.**
  - Corney & Drummond, [arXiv:quant-ph/9912096](https://arxiv.org/abs/quant-ph/9912096). **Full text** (gpt-b).
  - Drummond & Corney, JOSA B 18, 139 (2001), [DOI:10.1364/JOSAB.18.000139](https://doi.org/10.1364/JOSAB.18.000139), preprint [arXiv:quant-ph/9912095](https://arxiv.org/abs/quant-ph/9912095): Hamiltonian and stochastic fibre equations with Raman reservoirs. **Full text, sections III and VI** (gpt-b, arXiv version).
  - Corney et al., [arXiv:quant-ph/0603280](https://arxiv.org/abs/quant-ph/0603280) (PRL 97, 023606 (2006)): polarization squeezing in fibre with Raman and acoustic noise. **Abstract only.**
- **Pulsed modes and dispersion.**
  - Doerr, Shirasaki & Khatri, JOSA B 11, 143 (1994), [DOI:10.1364/JOSAB.11.000143](https://doi.org/10.1364/JOSAB.11.000143): dispersion can enhance pulsed Kerr squeezing. **Abstract only.**
  - Opatrný, Korolkova & Leuchs, [arXiv:quant-ph/0204131](https://arxiv.org/abs/quant-ph/0204131): few nonmonochromatic modes represent pulsed Gaussian correlations. **Abstract only.**
- **Multimode and general theory.**
  - Sloan et al., [arXiv:2509.03482](https://arxiv.org/abs/2509.03482): multimode-fibre quantum noise. **Full text of the main paper** (claude-b, gpt-b).
  - Uddin et al., Nat. Photon. 19, 751 (2025), [DOI:10.1038/s41566-025-01677-2](https://doi.org/10.1038/s41566-025-01677-2): noise-immune quantum correlations of intense light. **Abstract only.**
  - Rivera, Uddin, Sloan & Soljačić, Nanophotonics 14, 1857 (2025), [DOI:10.1515/nanoph-2024-0634](https://doi.org/10.1515/nanoph-2024-0634): a general theory of the quantum noise produced by nonlinear dynamics from Gaussian states. **Abstract only.** The PI flagged it in `docs/references.md` as relevant to this problem.

## Sharpest statement of the gap

To be established by the literature audit. Working hypothesis: optimal filters and squeezing limits are known numerically for specific cases (scalar solitons and normal-dispersion pulses, sometimes with Raman), and first-principles simulations exist. What is not known is a fast, general, provably lower-bounding formula in material, fibre and pulse parameters that also covers self-steepening, general dispersion, polarization and several modes, with a stated gap to the reachable optimum.

## Conjectures

None registered.

## Approaches (round 3, from 2026-10-10)

Four agents, four hours each. They split by method and regime, and their results meet at shared limits so that each can check another.

| Task | Agent | Regime | Method | Cross-checks |
|---|---|---|---|---|
| T-20261010-claude-interactive-04 | claude-a | Dispersionless, $\Phi_{\rm peak}^2L/L_D\ll1$; scalar, then two polarizations | Exact linearized solution: without dispersion the intensity is $z$-invariant, so the noise map is a nonlocal Kerr–Raman shear plus Raman phase noise. Then explicit spectral kernels and large-$\Phi$ stationary-phase asymptotics. | Kerr anchor; short-length limit of -05 |
| T-20261010-claude-interactive-05 | claude-b | Normal dispersion, $N\gg1$, before and after optical wave breaking | Semiclassical dispersive hydrodynamics. Fluctuations are carried along characteristics. With a monotone chirp a spectral band is a time gate whose edges move with the local frequency noise. | Dispersionless limit (-04); registered P-20261004-root-01 runs; passive parabola (C-20261004-claude-a-01) |
| T-20261010-claude-interactive-06 | gpt-b | Anomalous dispersion, $N\approx1$–2; Raman soliton as a stretch | Soliton perturbation theory: four neutral modes plus continuum. Raman reservoir and self-frequency shift, self-steepening and $\beta_3$ projected onto them. | Published Kerr-only and 300 K results; the notebook optimum; P-20261004-root-03 |
| T-20261010-claude-interactive-03 | gpt-a | Any | Proves the readout hierarchy. Builds binary-specific bounds above $\lambda_{\rm gen}$ (relaxations that use $T_i^2=T_i$), cheap certificates, and a reference table for scoring the others. | Scores -04, -05 and -06 |

T-20261010-claude-interactive-02 (literature audit) stays open. Each agent records the literature of its own regime, and those notes feed the audit.

## Oracle

**Available.** The solver covers:
- the multimode, two-polarization GNLSE (dense or CP overlaps) with self-steepening and isotropic and anisotropic Raman;
- the linearized covariance by adjoint contraction. Use `adjoint_mode=:discrete_rk4ip`, the default once agents' PR #2 merges and the pin moves.

From one covariance, compute $\lambda_{\min}(V)$, $\lambda_{\rm gen}$, and a heuristic optimum over binary filters (greedy or annealed search). The gaps between the three measure how tight each bound is. Every candidate formula is scored against them on held-out fibres and pulses.

**Missing or caveated.**
- The default Raman Langevin spectrum halves the zero-point part (T-20261004-gpt-b-02). Use the symmetrized spectrum.
- The sampled Raman kernel needs time steps of 3 fs or less (T-20261006-claude-interactive-02).
- Stochastic Raman propagation is single-mode only.
- There is no acoustic (GAWBS) reservoir.
- Multimode Raman noise needs the local spatial correlations described in C-20261008-gpt-b-01 (proposed).

## Lab test

- **Single-mode.** A Gaussian pulse at known $P_0$, $T_0$, $\lambda_0$ in single-mode fibre, then a programmable binary spectral mask (pulse shaper) and balanced detection against shot noise. Compare the best measured Fano factor against $F_{\rm LB}$ while sweeping power and length.
- **Multimode.** Repeat in a few-mode GRIN fibre with non-selective and mode-selective (photonic-lantern) filtering.
- **The bound fails if** any measurement, corrected for detection efficiency, falls below it.

## Risks and must-reads

- **The rigorous bounds may be loose.** $\lambda_{\min}(V)$ can sit far below what any filter reaches, because phase-quadrature squeezing is not accessible by filtering. Then tightness has to come from a filter-specific argument, and a "fast and tight" formula may exist only piecewise in regime.
- **Linearization limits.** It fails when the nonlinear phase spread $\Phi/\sqrt{N_{\rm ph}}$ is not small, and in strongly noise-amplifying regimes (modulation instability, soliton fission) where Gaussian theory may still hold but the optimal filter becomes fragile.
- **Missing physics.** Acoustic (GAWBS) and classical laser excess noise are outside the model. Excess input noise is an extension (Uddin et al. 2025); this card assumes a coherent input.
- **Must-reads not yet located here.** The single-mode Kerr squeezing limit (Kitagawa–Yamamoto); later first-principles fibre-squeezing simulations by Corney, Drummond and co-workers.
- **Overlap with other cards.**
  - P-20261004-root-04 (parked) asked for criteria connecting multimode covariance to filter-accessible intensity squeezing. This card supersedes it (PI, 2026-10-10); its readout subtargets are in rung 5.
  - P-20261004-root-01 (normal-dispersion filtering map) and P-20261004-root-03 (multimode launches) are regime-specific cases this formula should recover.
  - P-001 has a matched-local-oscillator, profile-limited result for parabolic pulses.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-10 | claude-interactive (claude; claude-opus-5-5) | Created as candidate on PI instruction; literature unaudited | PI request in chat, 2026-10-10; starting structure and anchors from runs cited above; literature as recorded on P-20261004-root-01, P-20261004-root-03 and P-001 |
| 2026-10-10 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Priority 2 → 1; supersedes P-20261004-root-04; $\lambda_{\min}(V)$ kept as a required diagnostic; readout hierarchy added as a statement to prove; four approach tasks assigned | PI messages in chat, 2026-10-10 |
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Claims list completed from the claim files (it omitted several). Recorded GPT 6 Pro's independent verification (run `2026-10-18-pi-chatgpt-independent-verification`): C-20261010-claude-a-01 (with gpt-a's 2026-10-11 audit) and C-20261010-claude-b-01 → sim-verified (narrowed); new claim C-20261019-pi-chatgpt-01. Status, priority and literature_state unchanged | [review](../docs/review-2026-10-18-pi-chatgpt-similariton-normal-dispersion-verification.md); task T-20261019-claude-interactive-01 |
| 2026-10-19 | claude-interactive.17 (claude; claude-opus-5-5), task T-20261019-claude-interactive-10, on the PI's promotion decision | Added promising results R-0012 (C-20261010-claude-a-01: dispersionless closed forms and the weak-normal-dispersion $\sqrt{\Phi L/L_D}$ law) and R-0013 (C-20261010-claude-b-01: $\lambda_{\min}=\Lambda(Z)/N^2$ in strong normal dispersion). Status, priority, literature_state and novelty_confidence unchanged | [R-0012](../results/promising/R-0012-weak-normal-dispersion-lambda-min/RESULT.md), [R-0013](../results/promising/R-0013-strong-normal-dispersion-lambda-over-n2/RESULT.md) |
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Result R-0015 added (promising; from C-20261019-pi-chatgpt-01). Status unchanged | Task T-20261019-claude-interactive-14 |
