---
id: P-20261016-claude-interactive.7-01
title: "Quantum state of Rayleigh–Jeans-thermalized light in multimode fibre: coherent, dephased and condensed CW inputs"
status: candidate
priority: 2
literature_state: open
novelty_confidence: medium
target_quantity: "The quantum state of a CW multimode fibre field after Kerr thermalization: its reduced and joint photon-number statistics (mode-resolved g2 and cross-correlations, condensate number distribution), mean fields and phase coherence, Gaussian covariance and squeezing, and purity and entanglement. Given as functions of z/L_kin, z/z_E (scrambling), photons per mode per coherence cell, mode count and condensate fraction, for coherent and dephased-coherent inputs, in the non-condensed and condensed Rayleigh-Jeans regimes."
model: "Scalar (one polarization) multimode Kerr propagation in the spatial (monochromatic) approximation, quantized per temporal coherence cell: H = sum_p eps_p n_p - (g/2) sum S_pqrs a_p^+ a_q^+ a_r a_s, g = gamma*hbar*omega/tau. Weak intra-group random linear coupling as in real fibres. Extensions: vector Kerr and two polarizations, L_z, ideal-GRIN collective modes, dispersion and walk-off coupling the cells, Raman."
oracle_ready: partial
last_audited: null
audited_by: [claude]
proposed_by: PI
provenance:
  agent: claude-interactive.7
  model: claude-opus-5-5
  family: claude
claims: [C-20261016-claude-interactive.7-01, C-20261016-claude-interactive.7-02, C-20261016-claude-interactive.7-03, C-20261018-claude-interactive.7-01, C-20261018-claude-interactive.7-02, C-20261018-claude-interactive.7-03]
results: [R-0007, R-0008, R-0009, R-0010]
---

## Target quantity

**The PI's question (2026-10-16).** Consider nonlinear thermalization of a multimode fibre field into the Rayleigh–Jeans (RJ) equilibrium, in the sense of Picozzi, Wu, Christodoulides and others. What is the quantum-mechanical state of the thermalized field? Three cases:
- (a) a coherent-state input;
- (b) a dephased coherent-state input;
- (c) a condensed classical RJ state: all photons in the fundamental, and weak excitations above the condensate.

The PI asked for continuous-wave (CW) excitation, analytical work first, and simulation checks later.

**Current answer (provisional, 2026-10-16; first family; toy, exact-GRIN-tensor and linearized models; details in the exploration note):**
1. **Never a grand-canonical thermal state.** Each coherence cell keeps the input's Poisson photon number. A coherent input stays globally pure, so single-mode "thermal" mixedness is entanglement.
2. **(a) Coherent input.**
   - Up to a scrambling length $z_E=\min[\sqrt{\ln2\,n/\mathcal A},\ \ln(n/c)/2\lambda_1]$ (C-02; tested with the exact GRIN tensor), the state is a pure, strongly multimode-squeezed Gaussian on a reproducible, RJ-looking speckle.
   - Mode-resolved photon counting can see part of that squeezing.
   - $z_E\sim100$ m–1 km in typical GRIN conditions, so metre-scale experiments are in this regime.
   - **Shot to shot at experimental photon numbers** (run `…-grin-shot-statistics`; 15 GRIN modes, one condensed launch). With a quiet laser at $n=10^{10}$ a fixed launch repeats to $g^{(2)}-1\sim10^{-8}$ for $z\le75L_{\rm NL}$, against 0.87 for thermal light. The noise is Gaussian: output variances scale with the input noise until $z_E(n/F_{\rm in})$. Technical noise decides when shots look thermal: about $150L_{\rm NL}$ for 0.5% per-mode noise, while 1% common-mode jitter gives 0.34 at $100L_{\rm NL}$. Phases redrawn on every shot give the Dirichlet law within about $30L_{\rm NL}$.
3. **(b) Dephased input.** A thermal mixture from the kinetic length on, independent of photon number.
4. **After thermalization with weak disorder.** Fock-diagonal reduced states with polytope (B-spline) statistics. In the condensed case they are exactly Dirichlet: $g^{(2)}=2-2/M$, a closed-form condensate variance, and a sign change of the condensate–mode correlation (C-01). **Ensembles** (note §6.10): over 12 disorder realizations and 12 launch draws per $E'$, $\langle I_0\rangle$ stays within 0.003–0.007 (SD) of the Dirichlet value, $g^{(2)}$ is 1.85–1.87 and ${\rm Var}\,I_0$ 0.96–1.01 of Dirichlet. The statistics self-average. All of this assumes the coupling stays inside degenerate groups (the literature's weak disorder) and that the disorder is strong enough to break the extra invariants within the fibre.
5. **Without disorder.** A generalized Gibbs ensemble fixed by the resonant Kerr energy, which remembers the input phases (C-03). In the GRIN model, aligned phases condense less than random ones. **Ensembles** (note §6.10): with Kerr alone the endpoint is launch-specific. Twelve random-phase draws per $E'$ end 0.03–0.04 below RJ on average, with seven to eight times the spread, and an all-LP11 launch never leaves LP11 (12 of 12).
6. **(c) Condensed limits.**
   - All photons in the fundamental: a pure Kerr-squeezed state with tiny Bogoliubov dressing; nothing thermalizes.
   - Few excitation quanta above a large condensate: exact diagonalization shows they do *not* thermalize. The quasiparticle number is frozen to $O(1/N)$, so the state keeps the input's excitation configuration. Bose–Einstein partition statistics (antibunched at $Q=1$) are what ergodic dynamics would give, but it is not ergodic. Truncated Wigner fails here too, by heating the vacuum.
   - **Squeezing the equilibrated condensate afterwards** (note §6.8; run `…-condensate-kerr-squeezability`; claims C-20261018-claude-interactive.7-02 and -03). Before scrambling it keeps its phase (quantum phase variance $10^{-8}$–$10^{-6}$ rad$^2$ at $n=10^{10}$) and near-shot-noise intensity noise. What limits direct Kerr squeezing is its mixedness $\nu$ from entanglement with the cloud: best $\approx0.95(\nu^4/\bar n_0)^{1/3}$. Over 12 disorder realizations that is −23.4 ± 1.9, −13.2 ± 2.5 and −6.8 ± 2.3 dB at $\bar n_0=10^{10}$ and $z=10$, 50, 100 $L_{\rm NL}$, with no useful squeezing at 200 in 9 of 12 (note §6.10; one realization gave −22, −11, −4.5). The condensate's own squeezing out of the fibre varies more: −8 to −10 dB on average at $f_0\approx0.85$, $z=10$–50, SD about 3 dB. After scrambling the condensate is Fock-diagonal and Kerr leaves it unchanged. A balanced, self-referenced (Sagnac) squeezer rejects all of this down to the pump's relative power spread squared (−26 dB for the Dirichlet condensate).

**Definitions.**
- **Cells.** In the spatial (monochromatic) model, each temporal coherence cell of duration $\tau$ is an $M$-mode Kerr system with $\bar N=P\tau/\hbar\omega$ photons. Its classical dynamics depends only on $\gamma P$; quantum effects enter as $1/\bar N$.
- **Input (b).** The per-mode phase-randomized coherent state $\otimes_p\sum_n{\rm Poi}(n;|\alpha_p|^2)|n\rangle\langle n|$. This is the random-phase ensemble of wave turbulence, and what an experiment that redraws a diffuser or SLM phase on every shot prepares. A *globally* dephased coherent state is identical to (a) for every number-conserving observable.
- **The state.** "The quantum state" means:
  - the reduced density matrices of one mode and of a few modes;
  - the joint photon-number statistics;
  - the mean fields;
  - the Gaussian covariance before scrambling;
  - global purity and entanglement.

**Answer form.**
- Closed-form reduced states and correlation functions in the post-thermalization regime.
- A length scale, with its scaling law, that separates a pure Gaussian regime from a mixed thermal one.
- Validity domains as bounds on dimensionless groups: $n_{\rm cell}$ (photons per mode per cell); $M$; $L_{\rm beat}/L_{\rm NL}=g\bar NS/\kappa$; $z/L_{\rm kin}$; $z/z_E$; the condensate fraction $f_0$; $E'/E'_{\rm vac}$ (Section 5 of the note).

**Order of work.**
1. Scalar, spatial-only, single cell; generic fibre with weak intra-group disorder, so that only $N$ and $E_{\rm lin}$ are conserved.
2. The scrambling length and the pre-scrambling Gaussian state, with $\lambda$ computed for realistic GRIN and step-index fibres.
3. The condensed regime: Dirichlet statistics, condensate phase coherence, and quantum corrections when excitations are few.
4. Ideal-GRIN collective modes (Kohn, breathing, $L_z$) and the resonant invariant $H_{\rm res}$: generalized-Gibbs corrections.
5. CW coupling between cells (dispersion, walk-off): coherence-cell size, spectral broadening after scrambling, spontaneous four-wave mixing from vacuum.
6. Two polarizations, Raman.

## Signal of hidden simplicity

All of this is in the exploration note `explorations/2026-10-16-claude-interactive.7-quantum-rj-state.md`. These are first-family results, not audited.

**Exact constraints.** The total photon number of each cell keeps the input's Poisson law, so the thermalized state is never grand-canonical. A coherent input stays globally pure, so any thermal-looking mixedness of a mode is entanglement.

**Coherent and dephased inputs take different routes [derived; toy-tested; claim C-02].**
- **Coherent input.** The state is a pure, displaced, multimode-squeezed Gaussian centred on the deterministic classical trajectory. Its mode powers look RJ-distributed across modes and along $z$, but repeat shot to shot. It stays so until
$$z_E\simeq\min\Big[\sqrt{\ln2\,n/\mathcal A},\ \ln(n/c)/2\lambda_1\Big].$$
  - The first, ballistic term comes from the input's shot-noise spread of $N$ and $E'$, which shifts each mode's mean frequency. It is a multimode Kerr phase diffusion. $\mathcal A$ follows in closed form from Hartree–Fock frequencies.
  - The second term is chaotic amplification.
- **Dephased input.** It becomes a phase-averaged displaced thermal state at the kinetic length $L_{\rm kin}$, independent of $n$. Its one-mode intensity law is the Rician law of a complex Ornstein–Uhlenbeck process.
- **Toy check (truncated Wigner, $M=10$).**
  - Four pre-registered collapse lengths at $n=10^5$–$10^{11}$ landed within ±15%.
  - The Hartree–Fock ballistic prediction is within 11%.
  - The dephased input is thermal by $z\approx20$ for every $n$.
  - **Exact GRIN tensor, pre-registered:** the collapse length is linear in $\ln n$ with slope $1/(2\lambda_{\rm eff})$, $\lambda_{\rm eff}=0.0171$ against the independent $\lambda_1=0.0183$ (run `…-grin-twa-scrambling`).
  - **Truncated Wigner against exact quantum dynamics** (four modes, $n=16$–100; run `…-exact-vs-twa-4mode`). The TWA error in the mean-field fraction is about $0.3/n$ (the closed-form Wigner error of Kerr phase diffusion). TWA reproduces the exact condensate Fano factor, including real power exchange in a GRIN subset, within sampling error. This covers the ballistic branch only.
  - The random-tensor toy's $\lambda_1L_{\rm NL}$ is about 0.004, and the exact GRIN tensor's 0.008–0.026 (below). That places $z_E$ for $n\sim10^9$–$10^{10}$ at $10^3$–$3\times10^3L_{\rm NL}$: metre-scale self-cleaning with a quiet laser is then in the pure-Gaussian regime. A full fibre model must check this (T-…-04).

**Closed-form post-thermalization statistics [derived; checked by Monte Carlo; claim C-01].** Take only $N$ and $E_{\rm lin}$ conserved, weak nonlinearity and $n\gg1$. The thermalized intensities are then uniform on a polytope, and their marginals are B-splines (Curry–Schoenberg).

The condensed regime is defined by $E'\le\kappa N$. There the excitations are *exactly* Dirichlet:
- $g^{(2)}=2-2/M$ for every excited mode;
- $g^{(2)}_{mn}=1-1/M$ between excited modes;
- ${\rm Var}\,N_0=T^2D(S_2-S_1^2/D)/(D+1)$, plus the Poisson input spread;
- the condensate–mode covariance changes sign at the harmonic mean of the excitation energies.

For GRIN with $K$ groups, the depletion's relative variance tends to $(\ln K+\gamma_E+\pi^2/6-2)/K^2$: 11% RMS per cell at $K=10$.

The toy reaches these statistics with weak intra-group disorder ($L_d\approx11L_{\rm NL}$). It does not reach them with strong disorder ($L_d\approx L_{\rm NL}$), where inter-group exchange freezes; that failed a pre-registered toy prediction.

**Few excitation quanta: a quantum regime [exact counting; run `…-rj-polytope-mc`].** With $Q=E'/\kappa\lesssim K^3$ quanta above the condensate, the quantum microcanonical statistics are partition counts. In GRIN with $K=10$:
- a first-group mode is antibunched at $Q=1$ ($g^{(2)}=0$), with $g^{(2)}=1.33$, 1.61 and 1.80 at $Q=2$, 5 and 10;
- at $Q=60$ the depletion is 18 against 13 (RJ), and its variance is 7 times the RJ value, because the high modes are frozen out.
This is where truncated Wigner fails. **Exact diagonalization** (run `…-few-quanta-exact`) shows these statistics are not reached for a large condensate: the excitation number freezes (${\rm Var}\,N_{\rm ex}\propto N^{-1.2}$), the quantum counterpart of $\lambda_1\propto1-f_0$.

**Exact GRIN Kerr tensor** ($K=5$, 15 modes, weak disorder; run `…-grin-lyapunov`; single trajectories, confirmed by the ensembles of note §6.10). The Dirichlet law holds at $f_0=0.61$–0.87:
- $g^{(2)}$ within 1.2%;
- $\langle I_0\rangle$ within 0.6%;
- ${\rm Var}\,I_0$ within 7%.

**Seen directly** (note §6.9; run `…-grin-thermalization-visual`; single trajectories, confirmed for 12 realizations each in note §6.10). Power moves between groups only through Kerr, but RJ is reached only with the weak linear intra-group coupling. With it, a launch with all power in LP11 condenses to $f_0=0.564$ (RJ 0.565) once a vacuum seed grows, at about $100$–$150L_{\rm NL}$. With Kerr alone the same launch never leaves LP11, and the $E'=0.6$ launch ends in a non-RJ generalized Gibbs state.

$\lambda_1L_{\rm NL}=0.008$–0.026 with disorder, and 0.0014–0.025 without. Empirically $\lambda_1L_{\rm NL}\approx0.067(1-f_0)$, from three points, except in the near-integrable, strongly condensed, disorder-free case.

**CW noise band** (same run). Noise growth extends over $|\beta_2|\Omega^2L_{\rm NL}/2\lesssim0.2$ in normal dispersion. With walk-off, intermodal-MI sidebands grow faster than $\lambda(0)$.
- For a 50 µm GRIN fibre at 1064 nm and 10 kW this means cells of about 0.6 ps, $n_{\rm cell}\sim3\times10^{10}$, and $z_E\sim10^2$ m (order of magnitude).
- Metre-scale self-cleaning with a quiet laser would then sit well before scrambling. There the output is a nearly pure multimode Gaussian state on a reproducible speckle, not a thermal mixture.

**Before scrambling, the state is strongly and usefully squeezed [linearized, exact GRIN tensor; run `…-grin-gaussian-state`; filed as claim C-20261018-claude-interactive.7-01, with its Gaussian-validity boundary from run `…-gaussian-validity`].** The Gaussian state from the tangent map is in vacuum units and independent of $n$.
- **Multimode squeezing.** $-24$ dB by $10L_{\rm NL}$. **[Superseded 2026-10-18 by C-20261018-claude-interactive.7-01:** valid only while $\sigma_{\max}^6<0.8\bar n_0$, i.e. to about $z=20$ (−30 dB) at $\bar n_0\approx10^{10}$. Beyond that, the crescent curvature degrades it (truncated Wigner: −31 dB at $z=50$, −21 dB at 100). "−55 to −100 dB by $400L_{\rm NL}$" is withdrawn.**]** −55 to −100 dB by $400L_{\rm NL}$ (ideal).
- **Mode-resolved photon counting with optimal real weights.** It reaches −4 to −9 dB at $10L_{\rm NL}$ and −20 to −27 dB at $400L_{\rm NL}$. **[2026-10-18, C-20261018-claude-interactive.7-01:** unlike quadrature squeezing, this is insensitive to the crescent curvature. Truncated Wigner reproduces it within 0.5 dB at every $z\le100$, even at $n=10^6$. The values beyond $z=100$, including the −20 to −27 dB at $400L_{\rm NL}$, are untested and not part of the claim.**]** That is about −10 dB per decade of length, roughly $\lambda_{\rm gen}\propto1/z$. The quiet combination is mostly the fundamental's photon number, corrected by a weighted sum of higher-order-mode photon numbers. The mechanism has not been derived.
- **The self-cleaned fundamental alone.** Only −1 to −13 dB, and lost once chaos sets in.

So the field that looks RJ-thermalized is, before $z_E$, a multimode squeezed state whose photon-number correlations between modes are far below shot noise.

**Without disorder the endpoint is a generalized Gibbs ensemble that remembers the input phases [toy-tested; claim C-03].**
- The resonant Kerr energy $H_{\rm res}$ is conserved separately from $E_{\rm lin}$. Its effect does not shrink as the nonlinearity weakens, because $g$ only sets the length scale.
- The uniform measure on the $(N,E_{\rm lin},H_{\rm res})$ shell, with no fitted parameter, reproduced the toy's condensate fraction within 0.010 in four pre-registered cases.
- Same mode powers, $K=4$, $E'=0.9$: random phases give 0.422 and aligned phases 0.559, against RJ's 0.517 for both.
- With the exact GRIN tensor (pre-registered): a centre-focused launch gives 0.700 and 0.582 against GGE 0.695 and 0.587 and RJ 0.739 and 0.609. In GRIN, aligned phases condense *less* than random ones. A second launch geometry (groups 1 and 4) gives 0.535 against GGE 0.529 and RJ 0.609. Six pre-registered GGE predictions have passed so far.
- Fixed-amplitude random-phase inputs often have $H_{\rm res}$ below the RJ mean, because they lack the exponential mode statistics: so it is for every launch with power in groups 1 and 2. That is not universal; a GRIN launch with power in groups 1 and 4 sits above it. The GGE predicts both cases.

## Literature state

First-family search, 2026-10-16, by two helper agents (claude-interactive.7.1 and .7.2) plus direct checks. Search strings are in the log entry. Access levels are those of the reader named; "helper" means a helper agent read it and this session did not.

**Quantum aspects of optical thermalization.**
- Birk, Lyubarov, Ruimy, Even-Tzur, Wu, Cohen, Segev, Kaminer & Sidorenko, "Thermalization and Entanglement of Quantum Light in a Nonlinear Multimode System", CLEO 2023, paper FTh4B.2, DOI [10.1364/CLEO_FS.2023.FTh4B.2](https://doi.org/10.1364/CLEO_FS.2023.FTh4B.2). Reports multimode entanglement arising during thermalization. **Abstract only** (one sentence). No full paper was found; it may answer part of this card and is the top must-read.
- Zanaglia, Garnier, Michel, Doya, Ferraro, Wabnitz, Carusotto & Picozzi, [arXiv:2512.07784](https://arxiv.org/abs/2512.07784) (journal reference given on arXiv: PRA 113, 063533 (2026); not checked).
  - Derives a quantum NLSE and a quantum kinetic equation with spontaneous terms, which relaxes to a spatio-temporal Bose–Einstein law; RJ fails where occupations fall below about 1.
  - Treats mean occupations only. No density matrix, $g^{(2)}$, purity, or distinction between coherent and random-phase inputs.
  - **Full text of the quantum sections (helper).**
- Chiocchetta, Larré & Carusotto, EPL 115, 24002 (2016), DOI [10.1209/0295-5075/115/24002](https://doi.org/10.1209/0295-5075/115/24002), [arXiv:1605.01870](https://arxiv.org/abs/1605.01870). Quantum Boltzmann equation for paraxial Kerr light, relaxing to Bose–Einstein. **Full text (helper).**
- Chahrour, Özdemir, Busch, El-Ganainy & Perez-Leija, [arXiv:2511.15100](https://arxiv.org/abs/2511.15100). Quantum probe light in a waveguide array, driven by a classical chaotic Kerr field through cross-phase modulation, relaxes to RJ- or Boltzmann-like occupations. The quantum state of the intense field itself is not treated. **Full text (helper).**
- Zanaglia et al., [arXiv:2405.06531](https://arxiv.org/abs/2405.06531). Cutoff Bose–Einstein interpolation between RJ and Bose–Einstein; states that fibre experiments are in the RJ limit. **Partial (helper).**
- Larré & Carusotto, PRA 92, 043802 (2015), [arXiv:1412.5405](https://arxiv.org/abs/1412.5405). Bogoliubov theory of a cavityless quantum fluid of light; the natural starting point for case (c). **Abstract only (helper).**
- Sloan et al., [arXiv:2509.03482](https://arxiv.org/abs/2509.03482). Linearized multimode-fibre quantum noise: input vacuum propagated through the classical Jacobian. This is the pre-scrambling regime of this card; the paper does not say when linearization fails. **Full text of the theory section (helper).**
- Vardi, Ramos & Kottos, [arXiv:2409.01422](https://arxiv.org/abs/2409.01422) (journal reference PRR 6, 043282 (2024) as given by the helper; not checked). Microcanonical occupations of few-mode bosonic oligomers, non-monotonic and away from RJ/BE (ensemble inequivalence). **Abstract only** (read here). It may already contain the finite-$M$ microcanonical *means* of Section 4 of the note; the fluctuation statistics there were not found in it.

**Experiments.** All RJ observations found are pulse averages or averages over speckle realizations:
- Pourbeyram et al., Nat. Phys. 18, 685 (2022), DOI [10.1038/s41567-022-01579-y](https://doi.org/10.1038/s41567-022-01579-y). About $10^{10}$ pulses per distribution; a 14-realization speckle test. **Full text including SI (helper).**
- Baudin et al., PRL 130, 063801 (2023), [arXiv:2301.02796](https://arxiv.org/abs/2301.02796). 2×300 per-realization modal decompositions in a 45-mode fibre: a possible ready-made test of the fluctuation predictions. **Full text of methods (helper).**
- Baudin et al., PRL 125, 244101 (2020), [arXiv:2007.11950](https://arxiv.org/abs/2007.11950). 2000 realizations. **Full text of methods (helper).**
- Fabert et al., Sci. Rep. 10, 20481 (2020), DOI [10.1038/s41598-020-77505-0](https://doi.org/10.1038/s41598-020-77505-0). Self-cleaned beams from two fibres stay mutually coherent. **Abstract only (helper).**
- Moussa et al., Sci. Rep. 11 (2021), DOI [10.1038/s41598-021-96753-2](https://doi.org/10.1038/s41598-021-96753-2). Self-cleaned output is reproducible under fibre squeezing. **Full text passage (helper).**
- No shot-to-shot photon or intensity statistics of thermalized output at a fixed input, no CW experiment, and no noise-transfer (RIN) study of self-cleaning were found.

**Disorder (random linear mode coupling) and thermalization in GRIN fibres** (added 2026-10-17 on the orchestrator's review of PR #55; read by claude-interactive.7 through a fetch tool's extraction of the HTML full text, not line by line):
- Fusaro, Garnier, Krupa, Millot & Picozzi, PRL 122, 123902 (2019), DOI [10.1103/PhysRevLett.122.123902](https://doi.org/10.1103/PhysRevLett.122.123902), [arXiv:2011.05111](https://arxiv.org/abs/2011.05111). **Full text (ar5iv).**
  - Random coupling inside degenerate subspaces only: the two polarizations of each mode, with correlation length $l_\beta$; coupling of non-degenerate modes is quenched because $\beta_0l_\beta\gg1$.
  - Effective strength $\Delta\beta=\sigma_\beta^2l_\beta$, in the regime $L_{\rm disor}=1/\Delta\beta\ll L_{\rm nl}$ (their simulation: $L_{\rm disor}\approx0.4$ m, $L_{\rm nl}\approx1$ m, $l_\beta\approx30$ cm).
  - A discrete kinetic equation with rate $\propto\gamma^2/\Delta\beta$ relaxes to RJ, faster than the disorder-free kinetic equation by about $\Delta\beta/\beta_0$.
  - Without disorder, a 120-mode GRIN simulation shows coherent, quasi-reversible power exchange and no condensation ("freezes the thermalization").
  - Single disorder realizations; 13 m experiments at 19 kW with condensate fractions up to about 60%.
- Garnier, Fusaro, Baudin, Michel, Krupa, Millot & Picozzi, PRA 100, 053835 (2019), [arXiv:2011.03918](https://arxiv.org/abs/2011.03918). **Full text (ar5iv).**
  - The longer version: Ornstein–Uhlenbeck polarization disorder; $\Delta\beta=2.6$–42 m$^{-1}$ with $l_\beta=30$–0.47 cm in simulations, i.e. $L_d$ about 2–40 cm, "consistent with" 10–20 m beam-cleaning experiments; the physical values are not measured.
  - In the disorder-free GRIN fibre only about 41 efficient resonances exist, and the mode locking freezes thermalization.
  - Single realizations with $z$-window averaging.
- Berti, Baudin, Fusaro, Millot, Picozzi & Garnier, PRL 129, 063901 (2022), [arXiv:2207.08680](https://arxiv.org/abs/2207.08680). **Full text (arXiv HTML).**
  - "Strong" disorder couples non-degenerate modes (induced experimentally by stress). It drives relaxation toward equipartition of power, which competes with RJ.
  - RJ condensation survives as an out-of-equilibrium stage when the inter-group relaxation is slower than RJ thermalization.
  - 64-realization ensembles, piecewise-constant Ornstein–Uhlenbeck coupling, 46 modes.
- Ferraro et al., [arXiv:2505.11299](https://arxiv.org/abs/2505.11299) (2025 review). Random mode coupling "can assist" beam self-cleaning; weak disorder accelerates RJ condensation. **Abstract only.**
- Torres et al., PRL 136, 173801 (2026), [arXiv:2512.17777](https://arxiv.org/abs/2512.17777). Reversible dynamics mediated by anomalous correlators against irreversible thermalization, in coupled NLS systems; not specific to GRIN disorder. **Abstract only.**
- Found by search, **not accessed**: Baudin et al., "Rayleigh-Jeans thermalization vs beam cleaning in multimode optical fibers", [arXiv:2309.02215](https://arxiv.org/abs/2309.02215); "Non-uniform modal power distribution caused by disorder in multimode fibers", [arXiv:2601.16998](https://arxiv.org/abs/2601.16998).
- **Relation to this card.** §6.9 of the note (RJ needs weak linear intra-group coupling; Kerr alone gives a generalized Gibbs state or nothing) is consistent with Fusaro et al. and Garnier et al., and was anticipated by them. It differs in three ways:
  - the coupling acts on the degenerate spatial modes of a scalar field rather than on polarization;
  - it is white in $z$;
  - the original strength ($L_d\approx11L_{\rm NL}$) is weaker than the nonlinearity, where theirs is stronger.
  Note §6.10 tests the ensemble, strength and correlation-length dependence.

**Quantum chaos and thermalization of coherent states.**
- Cosme & Fialko, PRA 90, 053602 (2014), [arXiv:1408.4186](https://arxiv.org/abs/1408.4186). Truncated Wigner against exact diagonalization for a 4-mode, 40-boson Bose–Hubbard system: relaxed one-mode states are thermal and match the diagonal ensemble. **Full text (helper).**
- Qiao, Großmann, Schlagheck & Lando, PRL 135, 060404 (2025), [arXiv:2410.06039](https://arxiv.org/abs/2410.06039). Bose–Hubbard rings: quantum relaxation is much faster than truncated Wigner at strong interaction, and the two agree at weak interaction. **Full text (helper).**
- Rammensee, Urbina & Richter, PRL 121, 124101 (2018), [arXiv:1805.06377](https://arxiv.org/abs/1805.06377). Out-of-time-order correlators grow until $\lambda^{-1}\ln N$, then saturate. **Abstract only (helper).**
- Silvestrov & Beenakker, PRE 65, 035208 (2002), [arXiv:nlin/0111042](https://arxiv.org/abs/nlin/0111042). Ehrenfest-time scaling. **Abstract only (helper).**
- Typicality: Popescu, Short & Winter, Nat. Phys. 2, 754 (2006), [arXiv:quant-ph/0511225](https://arxiv.org/abs/quant-ph/0511225), and Goldstein et al., PRL 96, 050403 (2006). **Abstract only (helper).**
- Phase-random ensembles: Nakata, Turner & Murao, PRA 86, 012301 (2012), [arXiv:1111.2747](https://arxiv.org/abs/1111.2747). **Abstract only (helper).**

**Validity of truncated Wigner.**
- Sinatra, Lobo & Castin, J. Phys. B 35, 3599 (2002), DOI [10.1088/0953-4075/35/17/301](https://doi.org/10.1088/0953-4075/35/17/301), [arXiv:cond-mat/0201217](https://arxiv.org/abs/cond-mat/0201217). The Wigner ensemble heats to a classical equilibrium fed by vacuum noise; it requires many more particles than modes. **Full text of the validity sections (helper).**
- Polkovnikov, Ann. Phys. 325, 1790 (2010), [arXiv:0905.3384](https://arxiv.org/abs/0905.3384). **Partial (helper).**

**Classical optical condensation: means known, fluctuations not derived.**
- Connaughton, Josserand, Picozzi, Pomeau & Rica, PRL 95, 263901 (2005), DOI [10.1103/PhysRevLett.95.263901](https://doi.org/10.1103/PhysRevLett.95.263901), [arXiv:cond-mat/0502499](https://arxiv.org/abs/cond-mat/0502499).
  - Condensate fraction law with a UV cutoff, and classical Bogoliubov pair correlations.
  - No fluctuation theory and no ensemble discussion.
  - **Full text (helper).**
- Aschieri, Garnier, Michel, Doya & Picozzi, PRA 83, 033838 (2011), DOI [10.1103/PhysRevA.83.033838](https://doi.org/10.1103/PhysRevA.83.033838).
  - Truncated 2D parabolic potential: $n_0/N=1-(E-E_0)/(NV_0/2)$. This is the large-$K$ limit of the Dirichlet mean here.
  - Its Fig. 4 shows the simulated spread of $n_0/N$ with no theory for it.
  - **Full text (helper).**
- Baudin et al. 2020 (above). Finite-size critical energy with $\rho=\sum_{p\ne0}(p_x+p_y)^{-1}$, the same sum as $S_1$ here. Heat capacity $C_V=M$ when condensed. No fluctuation theory. **Full text (helper).**
- Zanaglia et al., PRA 110, 063530 (2024), [arXiv:2405.06531](https://arxiv.org/abs/2405.06531). Bose–Einstein with a cutoff of $G$ groups: quantum limit $N\ll G^2$, RJ limit $N\gg G^2$. Means only. **Full text (helper).**
- Picozzi et al., Phys. Rep. 542, 1 (2014), DOI [10.1016/j.physrep.2014.03.002](https://doi.org/10.1016/j.physrep.2014.03.002). Wave-turbulence equilibrium is microcanonical. It cites Picozzi & Rica, Opt. Commun. 285, 5440 (2012), DOI [10.1016/j.optcom.2012.07.081](https://doi.org/10.1016/j.optcom.2012.07.081) (**not accessed**), for numerically observed condensate fluctuations. **Keyword-searched full text (helper).**

**Condensate number statistics in closed Bose systems.**
- Holthaus, Kalinowski & Kirsten, Ann. Phys. 270, 198 (1998), DOI [10.1006/aphy.1998.5852](https://doi.org/10.1006/aphy.1998.5852), [arXiv:cond-mat/9804171](https://arxiv.org/abs/cond-mat/9804171). **Full text (helper).**
  - The canonical-minus-microcanonical identity $\langle\delta N_{\rm ex}\delta E\rangle^2/\langle\delta^2E\rangle$.
  - For the 2D isotropic ideal Bose gas without cutoff: $\langle\delta^2N_{\rm ex}\rangle_{\rm cn}=(T/\hbar\omega)^2[\ln(T/\hbar\omega)+\gamma+1+\zeta(2)]$. The RJ result here has the same form, with the hard cutoff $K$ in place of $T/\hbar\omega$. This is a consistency check, not prior art for the cutoff case.
- Grossmann & Holthaus, PRE 54, 3495 (1996), DOI [10.1103/PhysRevE.54.3495](https://doi.org/10.1103/PhysRevE.54.3495), and PRL 79, 3557 (1997), DOI [10.1103/PhysRevLett.79.3557](https://doi.org/10.1103/PhysRevLett.79.3557). Navez et al., PRL 79, 1789 (1997), DOI [10.1103/PhysRevLett.79.1789](https://doi.org/10.1103/PhysRevLett.79.1789). Microcanonical ground-state statistics via partitions, and the Maxwell-demon ensemble. **Abstract only / not accessed (helper).**
- Witkowska, Gajda & Rzążewski, PRA 79, 033631 (2009), [arXiv:0901.1769](https://arxiv.org/abs/0901.1769). Classical fields with a cutoff, but the *canonical* distribution of $N_{\rm ex}$ (hypoexponential). The microcanonical B-spline law of this card was not found there. **Full text (helper).**
- Kruk et al., Rep. Prog. Phys. 88, 106401 (2025), [arXiv:2502.10880](https://arxiv.org/abs/2502.10880). Review. It cites a closed-form 1D classical-field distribution by Bienias, Pawłowski, Gajda & Rzążewski, PRA 83, 033610 (2011), DOI [10.1103/PhysRevA.83.033610](https://doi.org/10.1103/PhysRevA.83.033610), [arXiv:1008.3277](https://arxiv.org/abs/1008.3277). That paper is classical-field Monte Carlo for a 1D harmonic trap in the *canonical* ensemble (abstract only, read here), so not the microcanonical B-spline or Dirichlet law. **Kruk et al.: full text (helper).**
- Chatterjee & Diaconis, J. Phys. A 47, 085201 (2014), [arXiv:1306.3625](https://arxiv.org/abs/1306.3625). Canonical 2D-trap fluctuations are rigorously $O(n^{-1/2}\sqrt{\log n})$; the microcanonical case is left open. **Full text, automated summary (helper).**

**Phase of an isolated condensate.**
- Sinatra, Witkowska & Castin, PRA 75, 033616 (2007), [arXiv:cond-mat/0610644](https://arxiv.org/abs/cond-mat/0610644), and PRA 80, 033614 (2009), [arXiv:0907.1025](https://arxiv.org/abs/0907.1025). Castin & Sinatra, C. R. Physique 19, 316 (2018), [arXiv:1803.03168](https://arxiv.org/abs/1803.03168).
  - ${\rm Var}\,\theta=\mathcal At^2+2\int_0^t(t-\tau)\,{\rm Re}\,C_{\rm mc}\,d\tau$, with $\mathcal A_{\rm Pois}=\bar N(\partial_N\mu)^2$ for a Poisson atom number.
  - Ergodicity is assumed, in anisotropic traps.
  - **Full text (2018) / automated summary (helper).**
- Castin, Les Houches lecture notes, [arXiv:cond-mat/0105058](https://arxiv.org/abs/cond-mat/0105058). Collapse time $1/(|\chi|\sqrt N)$. **Full text (helper).**

**Number-conserving Bogoliubov theory and pair squeezing.**
- Castin & Dum, PRA 57, 3008 (1998). Gardiner, PRA 56, 1414 (1997). **Not accessed.**
- Kocharovsky et al., Adv. At. Mol. Opt. Phys. 53, 291 (2006), [arXiv:cond-mat/0605507](https://arxiv.org/abs/cond-mat/0605507). **Automated summary (helper).**

**Entanglement growth in unstable quadratic systems.** Bianchi, Hackl & Yokomizo, JHEP 03 (2018) 025, [arXiv:1709.00427](https://arxiv.org/abs/1709.00427). Gaussian-state entanglement entropy grows linearly at the subsystem Kolmogorov–Sinai rate. **Abstract only** (read here).

## Sharpest statement of the gap

No paper located here gives, for a Kerr-thermalized multimode optical field, the reduced or joint quantum state beyond mean occupations. That includes photon-number distributions and correlations, mean field and phase coherence, purity, and squeezing. Nor does any paper separate coherent from random-phase inputs, or give the length at which a coherent input's state stops being a pure Gaussian about the classical trajectory.
- Quantum kinetic theories (Zanaglia et al. 2026; Chiocchetta et al. 2016) give Bose–Einstein *means*, and assume random phases, so they cannot separate inputs (a) and (b).
- Linearized multimode noise theory (Sloan et al. 2025) is the pre-scrambling regime, without its limit.
- Bose–Hubbard quantum-chaos work (Cosme & Fialko 2014; Rammensee et al. 2018) has the right ingredients at $N/M\sim10$. It has not been applied at the optical scale ($N/M\sim10^5$–$10^9$, with fibre degeneracies and disorder) or in the condensed RJ regime.

The one item that may cover part of the gap is Birk et al. (CLEO 2023), seen as a one-line abstract only.

## Conjectures

Registered claims, all at cheap-checks-passed, with proposer-family toy evidence only:
- **C-20261016-claude-interactive.7-01.** Exact Dirichlet statistics of the condensed RJ regime. Valid with weak intra-group disorder. A pre-registered toy prediction at strong disorder failed, and is recorded in the claim.
- **C-20261016-claude-interactive.7-02.** Two-channel scrambling length of a coherent input ($\sqrt n$ ballistic, $\ln n$ chaotic), against the $n$-independent kinetic route of a dephased input.
- **C-20261016-claude-interactive.7-03.** Without disorder, a generalized Gibbs endpoint fixed by $(N,E_{\rm lin},H_{\rm res})$, which remembers the input phases.

Not yet claims (exploration note):
- the double-exponential form of the mean-field collapse. Tested with the exact GRIN tensor: the shape is double-exponential, but at rate $\approx\lambda_1$, not $2\lambda_1$; the $n$-scaling of $z_E$ does follow $1/(2\lambda_1)$;
- ~~photon counting cannot reach the Lyapunov squeezing~~ (refuted by the linearized-state run). Replacement conjecture: mode-resolved photon counting reaches $\lambda_{\rm gen}\approx c/(z/L_{\rm NL})$ before scrambling (T-…-10);
- linear entanglement growth at the Kolmogorov–Sinai rate;
- for CW, the band that dominates noise growth. The first guess $\Omega_\lambda\sim\lambda/\Delta\beta_1$ is contradicted: walk-off opens intermodal-MI sideband gain above $\lambda(0)$ (§6.4 of the note). Spectral broadening after $z_E$ follows from whichever band dominates;
- ~~the Bose–Einstein (vector-partition) statistics of few-quantum excitations above a condensate~~. Exact diagonalization shows they are not reached for a large condensate: the excitations stay frozen (run `…-few-quanta-exact`).

## Approaches

| Task | Lane | Family |
|---|---|---|
| T-20261016-claude-interactive.7-02 | Second-family literature audit, including the Birk et al. full paper and the condensate-fluctuation literature | not-claude |
| T-20261016-claude-interactive.7-03 | Exact quantum check (small $M$, $N\le60$, sector-by-sector Krylov) of scrambling, the TWA scrambling law and the reduced states; the dephased-input route | any |
| T-20261016-claude-interactive.7-04 | Lyapunov spectrum and $z_E$ for realistic GRIN and step-index fibres with intra-group disorder, using the solver's multimode spatial model | any |
| T-20261016-claude-interactive.7-05 | GGE with $H_{\rm res}$ and the ideal-GRIN collective modes: what a disorder-free fibre thermalizes to, and its input-phase dependence | any |
| T-20261016-claude-interactive.7-06 | Cell coupling in CW: the sideband (intermodal MI) band that dominates noise growth, spectral broadening after $z_E$, and the bin and window dependence of TWA | any |
| T-20261016-claude-interactive.7-07 | Verify C-01 in a GRIN fibre model (Dirichlet statistics, weak disorder) | not-claude |
| T-20261016-claude-interactive.7-08 | Verify C-02 with stochastic multimode simulations ($z_E$ against $\ln n$ and $\sqrt n$) | not-claude |
| T-20261016-claude-interactive.7-09 | Verify C-03 in a GRIN fibre model (GGE endpoint, input-phase memory) | not-claude |
| T-20261016-claude-interactive.7-10 | Derive and test the photon-counting squeezing law $\lambda_{\rm gen}(z)$ of the pre-scrambling state, with the solver's linearized covariance, loss and Raman | any |
| T-20261016-claude-interactive.7-11 | Solver: opt-in linear intra-group mode coupling (disorder), or a segmented-propagation recipe, for -07 and -09 | not-claude |
| T-20261016-claude-interactive.7-12 | Shot-to-shot mode-power statistics in a realistic experiment model (pulse shape, time-integrated detection, hundreds of modes, measured laser noise), against published data; first look in note §6.7 | any |

## Oracle

**Partial.**
- **Pre-scrambling Gaussian state.** The solver's linearized covariance (adjoint contraction) gives it directly, for the multimode model with Kerr overlaps.
- **Truncated Wigner.** The stochastic multimode GNLSE with symmetric vacuum noise covers the post-scrambling regime only when every simulated mode and frequency bin is far above vacuum: $E'\gg E'_{\rm vac}=\sum_m\varepsilon_m/2$ per cell, summed over bins (note, §5). It fails in the weak-excitation condensed regime and for long CW windows. Every TWA result must report its dependence on the number of bins and on the window.
- **Exact quantum dynamics.** Sector-by-sector Krylov propagation for $M\le6$ and $N\lesssim60$ is cheap. In the condensed regime the resonant Hamiltonian conserves $N$ and $E'$, so a fixed $(N,Q)$ sector is small for any $N$ and can be diagonalized exactly (run `…-few-quanta-exact`). These are the only oracles for the few-excitation regime and for whether quantum relaxation follows TWA.
- **Missing.**
  - No ready scripts for ensemble statistics of mode powers at fixed $z$.
  - **The solver has no linear mode coupling.** Its multimode linear operator is mode-diagonal (`solver/src/mmgnlse_solver.jl`), so intra-group disorder must be emulated: segment the propagation and apply random block unitaries between segments. Otherwise it needs adding (T-…-11). Vacuum (Wigner) shot noise (`ShotNoise`, `stochastic_ensemble`) and the linearized adjoint covariance are available.
  - CW (long-window) multimode runs cost more than pulsed ones.
  - The toy in this session is not the solver; its runs are cheap checks only.

## Lab test

All of these use a quiet single-frequency laser (shot-noise-limited amplitude, any linewidth), a GRIN fibre and mode-resolved detection (a photonic lantern or mode demultiplexer).
- **Shot-to-shot reproducibility of the output mode powers** for a fixed input, against fibre length (cut-back) or power, compared with the same measurement under redrawn input phases.
  - Prediction: a fixed input is reproducible to the amplified-quantum-noise level for $z<z_E$, while redrawn phases give thermal statistics beyond $L_{\rm kin}$.
  - Technical noise of the laser shortens $z_E$ by $\ln(F_{\rm in})/2\lambda_1$; common-mode phase noise does not.
- **Time-resolved $g^{(2)}(0)$ of single higher-order modes** in the condensed regime, in a fibre with weak intra-group mode coupling (C-01's regime). After thermalization, with phases redrawn per shot or beyond $z_E$, expect $2-2/M$ and the condensate–mode correlation sign change.
- **Existing data.** The 2×300 per-realization modal decompositions of Baudin et al. (2023) could test the condensate-fraction fluctuations at fixed $(N,E)$ without a new experiment.
- **Mode-resolved photon-number squeezing of the thermalizing field.** A quiet laser, a short GRIN fibre ($z\ll z_E$) and a photonic lantern with balanced photon counting. With weights computed from the classical trajectory, look for sub-shot-noise mode-power combinations, beyond what the total-power and $E'$ conservation laws give. Prediction: $\lambda_{\rm gen}$ improving by about 10 dB per decade of $z/L_{\rm NL}$ until loss or Raman noise limits it. Most of the weight is on the fundamental's photon number.
- **Kerr squeezing of the self-cleaned condensate** (note §6.8). Filter the fundamental after a short GRIN fibre and use it to pump a balanced fibre Sagnac squeezer, with the local oscillator from the bright port. Prediction: performance close to a coherent pump, floor $\approx(\delta P/P)^2$. A direct single-mode Kerr stage needs a realization-dependent nonlinear phase for −10 dB. Ensemble medians are 0.2 rad at $z=10$ and 13 rad at $z=50L_{\rm NL}$ for $f_0\approx0.85$, with ranges 0–6 and 0–136 rad, and 7 and 53 rad for $f_0\approx0.6$–0.77 (1.4 rad for a coherent pump). It fails beyond about $200L_{\rm NL}$. **[Superseded:** "2–22 rad … at $z=10$–$50L_{\rm NL}$", from one realization.**]** A local oscillator taken from the laser before the fibre cannot work: 1% laser amplitude jitter already gives 0.2–0.9 rad of condensate phase jitter at $z=10$–$50L_{\rm NL}$.
- **Input-phase memory (C-03).** Use an SLM to launch the same modal powers with different relative phases: random, and aligned to focus. In a short, low-disorder GRIN fibre, the output condensate fraction should differ between the two by the amount the $(N,E_{\rm lin},H_{\rm res})$ ensemble predicts. RJ predicts no difference. In the exact-GRIN-tensor model the centre-focused launch condenses *less*: 0.700 against 0.732 at $E'=0.6$ and 0.582 against 0.610 at $E'=0.9$. The random-tensor toy has the opposite sign and a 0.14 difference. Intra-group disorder erases the difference once the fibre is longer than a few disorder lengths; in the GRIN model it is gone for $L_d\lesssim100\,L_{\rm NL}$. Lengthening the fibre, or adding controlled mode scrambling, should remove it.

**Numbers for a typical experiment (order of magnitude).** 50 µm GRIN fibre at 1064 nm, $\gamma\approx6\times10^{-4}$ W$^{-1}$m$^{-1}$, normal dispersion, weak intra-group disorder, $f_0\approx0.7$. Values from the note §6.4–6.5.
- **1 kW:** $L_{\rm NL}\approx1.7$ m; noise cells about 2 ps with $n_{\rm cell}\sim1\times10^{10}$ photons; $z_E\sim1$ km.
- **10 kW:** $L_{\rm NL}\approx0.17$ m; cells about 0.6 ps with $n_{\rm cell}\sim3\times10^{10}$; $z_E\sim100$ m.
- **Metre-scale fibres are therefore pre-scrambling**, with a quiet laser and ignoring Raman.
- **Shot-to-shot mode-power statistics at a fixed launch** (note §6.7; run `…-grin-shot-statistics`; 15 modes, $f_0\approx0.74$). At $z\le60L_{\rm NL}$ (1–10 m at 10 kW) the relative variance of an excited mode's power across shots is about $10^{-8}$ with a quiet laser, and at most about $5\times10^{-2}$ with 0.5–1% laser noise. Thermal light has 0.87. So RJ occupations measured there describe the ensemble an experiment averages over (SLM phases, pulses, the power profile within a pulse), not thermal shot-to-shot fluctuations. Shot-resolved, mode-resolved detection at a fixed launch tests this directly. With phases redrawn on every shot, the same detection should give the Dirichlet values within about $30L_{\rm NL}$. **Within a pulse:** because the resonant Kerr dynamics scales as $I_p(z;s)=s\,i_p(sz)$, the instants of one pulse sample one trajectory over a range of lengths. In the 15-mode model the mode fractions vary across the pulse's FWHM with relative variance 0.3–0.7 at $z=30$–$300L_{\rm NL}$ (peak), yet two pulses agree to $10^{-4}$ for $z\le100$. Time-resolved, mode-resolved detection should see this deterministic temporal speckle; pulse-integrated detection averages it to RJ-like means. **More modes:** at fixed $f_0=0.70$, $\lambda_1L_{\rm NL}$ falls from 0.024 (10 modes) to about 0.015–0.016 (28–36 modes; run `…-grin-lyapunov-modecount`), so fibres with many modes need not scramble faster.
- **Ideal photon-counting squeezing.** At $z=1$–10 m and 10 kW ($z/L_{\rm NL}\approx6$–60) the linearized state gives $\lambda_{\rm gen}\approx-4$ to −14 dB. A detection efficiency $\eta$ bounds what is seen to $10\log_{10}[\eta\lambda_{\rm gen}+1-\eta]$: −8.7 dB at best for $\eta=0.9$.
- **Dirichlet statistics.** For two polarizations and $K=10$ groups with $S_z$ conserved, the excited modes have $g^{(2)}=2-2/(M-1)$ with $M=110$, i.e. 1.98. Deviations from 2 are small; the condensate-fraction variance and the sign change of the condensate–mode correlation are the more sensitive tests.

## Risks and must-reads

- **Must-reads.**
  - The full Birk et al. work, if it exists.
  - The full text of Vardi, Ramos & Kottos (2024).
  - Wave-turbulence probability-density theory, for the dephased route: Choi, Lvov & Nazarenko, Phys. Lett. A 332, 230 (2004), DOI [10.1016/j.physleta.2004.09.062](https://doi.org/10.1016/j.physleta.2004.09.062), [arXiv:math-ph/0409071](https://arxiv.org/abs/math-ph/0409071) (abstract only); and Nazarenko's book.
  - The fibre literature on disorder-assisted condensation (Fusaro et al.; Sidelnikov et al. "Random mode coupling assists Kerr beam self-cleaning"). Neither was located in this session.
- **The toy is not a fibre.** The random-tensor toy and the exact-GRIN run share the resonant approximation, exactly equidistant groups, $M\le15$, Brownian intra-group disorder and single trajectories. The small Lyapunov exponents and the $H_{\rm res}$ obstruction need a full GNLSE model with realistic disorder and more modes (task -04).
- **Ergodicity is assumed** for every post-scrambling statement. Ideal GRIN has extra exact invariants (Kohn, breathing, $L_z$), and the resonant regime adds $H_{\rm res}$.
- **Disorder model** (note §6.10). The scalar, white, intra-group disorder of the simulations is the literature's weak-disorder class. The original strength ($L_d\approx11L_{\rm NL}$) is 30–500 times weaker than published estimates. At realistic strength the 15-mode model thermalizes in about $10^3L_{\rm NL}$, so its relaxation lengths, not its endpoints, are model-specific. Polarization and inter-group coupling are absent (T-20261017-claude-interactive.7-03).
- **Laser technical noise** may make $z_E$ short in practice. The "pure Gaussian" regime then becomes a classical-noise statement. Note §6.7 quantifies it for 15 modes: shots look thermal past $z_E(n/F_{\rm in})$, about $150L_{\rm NL}$ for 0.5% per-mode noise.
- **Possibly uninteresting.** If $\lambda L_{\rm NL}=O(1)$ in real fibres and the input noise is large, every experiment is post-scrambling and the quantum state is just the classical microcanonical ensemble. The remaining content would then be the Dirichlet statistics and the truncated-Wigner validity criterion.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-16 | claude-interactive.7 (claude; claude-opus-5-5) | Created as candidate on PI instruction; literature_state open after a first-family search; priority 2 pending PI decision | PI request in chat, 2026-10-16; exploration note and runs cited above |
| 2026-10-17 | claude-interactive.7 (claude; claude-opus-5-5) | Ensembles over disorder realizations and launches, and validity of the quenched disorder model (PI request via the orchestrator). Thermalization endpoints self-average with weak disorder; Kerr-only endpoints are launch-specific. The own-squeezing numbers were single-realization and atypical (superseded; the ensemble is 2–3 dB more squeezed, SD about 3 dB). The original disorder strength is unrealistic; at realistic strength relaxation is 6–20 times slower. Disorder literature (Fusaro et al. 2019, Garnier et al. 2019, Berti et al. 2022) added. | Note §6.10; runs `2026-10-17-claude-interactive.7-ensemble-thermalization`, `-disorder-model-scan`, `-ensemble-squeezing`; predictions frozen in commit 1e377a7 |
| 2026-10-18 | claude-interactive.7 (claude; claude-opus-5-5) | Squeezing results filed as claims C-20261018-claude-interactive.7-01 (pre-scrambling squeezing: photon counting robust, quadrature squeezing bounded by curvature), -02 (the condensate's own squeezing, ensemble values) and -03 (Kerr squeezability: $(\nu^4/\bar n_0)^{1/3}$, Fock-diagonal no-go, Sagnac floor). Each has a GPT verify task (T-20261018-claude-interactive.7-02, -03, -04). "−55 to −100 dB by 400 $L_{\rm NL}$" withdrawn. | Run `2026-10-18-claude-interactive.7-gaussian-validity` (predictions frozen in commit 363ab078); PI request via the orchestrator |
| 2026-10-19 | claude-interactive.16 (claude; claude-opus-5-5) | Promising results R-0007 (C-20261016-claude-interactive.7-01), R-0008, R-0009 and R-0010 (C-20261018-claude-interactive.7-01, -02, -03) added under the PI's decision of 2026-10-19; each states the claim as sharpened by gpt-b. Status, priority and literature_state unchanged. G5 (clean-context audit) open for all four (T-20261019-claude-interactive.16-01). The Current answer and Conjectures sections are still stale (T-20261018-claude-interactive.11-02). | results/promising/R-0007-condensed-rj-dirichlet-statistics, R-0008-early-multimode-squeezing-curvature, R-0009-condensate-squeezing-covariance-identity, R-0010-displaced-thermal-kerr-squeezing-no-go; task T-20261019-claude-interactive-09 |
