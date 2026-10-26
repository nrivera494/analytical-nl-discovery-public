---
date: 2026-10-16
agent: claude-interactive.7
model: claude-opus-5-5
family: claude
task: T-20261016-claude-interactive.7-01
duration_min: 215
---

## Did

- Created problem card P-20261016-claude-interactive.7-01 on the PI's request (chat, 2026-10-16). The question: the quantum state of multimode fibre light after Kerr thermalization to RJ, for coherent and dephased-coherent CW inputs, in the non-condensed and condensed regimes.
- **Literature.** Two helper agents (claude-interactive.7.1 and .7.2, claude-opus-5-5) ran first-family searches: quantum aspects of optical thermalization, quantum chaos and truncated Wigner (TWA) validity, condensate statistics and phase. Their search strings are condensed in the Search log section below. This session checked three items directly:
  - Vardi, Ramos & Kottos (abstract);
  - Birk et al. (CLEO 2023; search result only);
  - Bianchi, Hackl & Yokomizo (abstract).
- **Derivation.** Wrote the analytic framework in `explorations/2026-10-16-claude-interactive.7-quantum-rj-state.md`:
  - exact invariants and their consequences;
  - the pre- and post-scrambling structure for coherent input, and the kinetic route for dephased input;
  - the polytope (microcanonical) ensemble in closed form, with the exact Dirichlet law in the condensed regime;
  - quantum corrections and the TWA vacuum-energy criterion;
  - the fully condensed limit.
- **Checks of the closed forms.** Independent Monte Carlo, run `2026-10-16-claude-interactive.7-rj-polytope-mc`.
- **Toy model.** Built a resonant toy model (random overlap tensor, GRIN-like degenerate groups, optional intra-group disorder) to test the dynamics:
  - run `…-rj-toy-thermalization`: 18 single-trajectory cases;
  - run `…-rj-toy-twa-scrambling`: truncated-Wigner ensembles at photons-per-cell $n=10^4$–$10^{11}$, with the predictions for the second set written down before it finished.
  - run `…-rj-toy-gge`: generalized-Gibbs (GGE) tests with four predictions written down before their runs, plus the linear-response formula;
  - run `…-grin-lyapunov`: the exact GRIN Kerr tensor ($K=5$) and CW sideband growth rates.
  - run `…-grin-gaussian-state`: the exact linearized quantum state (tangent-map covariance) before scrambling.
- Registered claim C-20261016-claude-interactive.7-01 (condensed-regime Dirichlet statistics) at cheap-checks-passed.
- Created tasks -02 to -06.
- **After a 30-minute pause requested by the PI** (17:03–17:34 EDT; not counted as working time):
  - run `…-exact-vs-twa-4mode`: exact quantum dynamics against truncated Wigner on four modes, $n=16$–100;
  - **PI request (chat, about 17:50): look at large $n$, where the physics is closer to Gaussian, and at statistics closer to existing thermalization experiments.** Run `…-grin-shot-statistics`: shot-to-shot mode-power statistics at $n=10^{10}$ with quantum-limited and technical input noise, and with phases redrawn per shot. Note §6.7, card and C-01/C-02 updated; task -12 created.

## Search log (first family, 2026-10-16)

Strings are condensed. Hits are named on the card, with access levels.

**Helper claude-interactive.7.1** (quantum aspects; chaos and TWA; experiments):
- "quantum optical thermodynamics multimode Kerr thermalization quantum state"
- "quantum Rayleigh-Jeans thermalization light photon statistics"
- "quantum noise beam self-cleaning multimode fiber"
- "optical thermodynamics quantum fluctuations photon number statistics Bose-Einstein correction"
- "thermalization of quantum light ... entanglement Christodoulides"
- "quantum thermalization photonic lattice Kerr coherent state Bose-Hubbard waveguide array"
- "Kottos Vardi quantum thermalization microcanonical"
- "Picozzi quantum fluctuations RJ condensation BE crossover"
- "quantum kinetic equation photons multimode fiber spontaneous four-wave mixing"
- "squeezing OR entanglement 'beam self-cleaning' OR 'optical thermalization'"
- "'Fan O. Wu' quantum thermalization", then the Birk et al. title
- "'entanglement entropy' 'optical thermalization'"
- "'quantum Rayleigh-Jeans'"
- "photon statistics speckle shot-to-shot fluctuations mode power"
- "Kerr beam self-cleaning relative intensity noise transfer"
- "beam self-cleaning pulse-to-pulse stability reproducibility"
- "g2 HBT multimode fiber nonlinear"
- "Lyapunov exponent multimode fiber Kerr chaos"
- Rammensee and Tomsovic titles
- "Bose-Hubbard trimer quantum chaos coherent state Ehrenfest time"
- "quantum noise amplification chaotic Ehrenfest time log N"
- Popescu–Short–Winter and Goldstein titles
- "eigenstate thermalization Bose-Hubbard classical limit"
- "truncated Wigner long-time thermalization vacuum noise modes particles"
- Polkovnikov and Berges–Gasenzer titles
- "Brewczyk Gajda Rzazewski classical fields"

**Helper claude-interactive.7.2** (classical condensation; condensate statistics; phase; Bogoliubov):
- "fluctuations of the condensate fraction Rayleigh-Jeans multimode fiber microcanonical ensemble variance fundamental mode power"
- "quantum noise beam self-cleaning multimode fiber squeezing fundamental mode quantum statistics"
- "quantum thermalization photons graded-index multimode fiber Bose-Einstein distribution quantum regime few photons per mode"
- "'quantum depletion' OR 'Bogoliubov' graded-index multimode fiber quantum fluctuations Kerr condensate"
- "microcanonical ensemble fluctuations Bose-Einstein condensate rigorous limit theorem 2D"
- "condensate phase diffusion classical field two-dimensional harmonic trap microcanonical"
- "classical wave condensation ensemble inequivalence large deviations"
- "vacuum fluctuations quantum noise seed thermalization multimode optical fiber Kerr truncated Wigner"
- "multimode squeezing graded-index multimode fiber Kerr quantum theory"
- title verifications for the condensate and phase-diffusion papers on the card

**Direct searches by claude-interactive.7:**
- arXiv:2409.01422 abstract (Vardi, Ramos & Kottos)
- "Birk Lyubarov Sidorenko Kaminer 'thermalization and entanglement of quantum light' nonlinear multimode": no full paper found
- "Bianchi Hackl Yokomizo linear growth entanglement entropy Kolmogorov-Sinai"
- "multimode fiber thermalization resonant Hamiltonian conserved nonlinear energy generalized Gibbs ensemble condensation input phases graded-index Kerr": no GGE with the resonant Kerr energy found
- "Bienias Pawlowski Gajda Rzazewski 2011 PRA 83 033610": canonical ensemble
- "Choi Lvov Nazarenko probability densities preservation of randomness wave turbulence"

## Found

1. **Exact framing.** Each CW coherence cell keeps the input's Poisson photon-number law, so the thermalized state is never grand-canonical. A coherent input stays globally pure, so the thermal mixedness of any mode is entanglement.
2. **Coherent and dephased inputs differ in route.** Claim C-02.
   - A coherent input is a pure, displaced, multimode-squeezed Gaussian on a deterministic, RJ-looking speckle until
     $$z_E=\min\big[\sqrt{\ln2\,n/\mathcal A},\ \ln(n/c)/2\lambda_1\big].$$
     The first term is ballistic dephasing from the shot-noise spread of the conserved quantities; the second is chaotic amplification.
   - A dephased input reaches thermal statistics at the kinetic length, independent of $n$.
   - Toy evidence (truncated Wigner, $M=10$):
     - four pre-registered collapse lengths ($n=10^5$–$10^{11}$) within ±15%;
     - a parameter-free Hartree–Fock ballistic prediction within 11%;
     - the dephased route independent of $n$.
   - Run `…-rj-toy-twa-scrambling`.
3. **Closed forms after thermalization, when only $N$ and $E_{\rm lin}$ are conserved.** Claim C-01.
   - The intensities are uniform on a polytope, with B-spline marginals.
   - In the condensed regime ($E'\le\kappa N$) the law is exactly Dirichlet: $g^{(2)}=2-2/M$ per excited mode, cross $g^{(2)}=1-1/M$, a closed-form condensate variance (GRIN: $(\ln K+0.222)/K^2$ asymptotically), and a sign change of the condensate–mode covariance.
   - Checked by Monte Carlo (run `…-rj-polytope-mc`).
   - The toy reaches these statistics with weak intra-group disorder.
   - **A pre-registered toy prediction at strong disorder ($\sigma=1$) failed**: inter-group exchange freezes. This is recorded in C-01.
4. **Without disorder the endpoint is not RJ.** Claim C-03.
   - The resonant Kerr energy $H_{\rm res}$ is a third invariant. The microcanonical ensemble on $(N,E_{\rm lin},H_{\rm res})$, with no fitted parameter, predicted the toy's condensate fraction within 0.010 in four pre-registered cases.
   - Same mode powers ($K=4$, $E'=0.9$): random phases give 0.422 and aligned phases 0.559, against RJ's 0.517.
   - So the thermalized state remembers the input phases. This is the classical part of the (a)/(b) difference that survives thermalization.
   - Run `…-rj-toy-gge`.
5. **Small Lyapunov exponents in the condensed toy.** $\lambda_1L_{\rm NL}$ is about 0.002–0.025, placing $z_E$ for $n\sim10^9$ at thousands of $L_{\rm NL}$. If this carries over to real fibres, self-cleaned beams from quiet lasers in metre-scale fibres are pre-scrambling: quantum-mechanically nearly pure Gaussian states, not thermal mixtures.
6. **Quantum corrections.**
   - In the condensed regime, RJ requires excitation quanta $Q\gg K^3$. This coincides, up to an $O(1)$ factor, with the truncated-Wigner validity condition $E'\gg E'_{\rm vac}$.
   - Fewer quanta is a Bose–Einstein (vector-partition) problem in which truncated Wigner heats spuriously.
   - A fundamental-only launch stays a pure Kerr-squeezed state with $O((L_{\rm beat}/L_{\rm NL})^2)$ Bogoliubov depletion.
7. **Real GRIN overlaps** (exact Hermite–Gauss Kerr tensor, $K=5$; run `…-grin-lyapunov`).
   - With weak intra-group disorder, the condensed Dirichlet law holds: $g^{(2)}$ within 1.2%, $\langle I_0\rangle$ within 0.6%, variance within 7%.
   - $\lambda_1L_{\rm NL}=0.008$–0.026.
   - Without disorder, the strongly condensed launches are not RJ.
8. **CW sidebands.**
   - Walk-off *raises* sideband growth above $\lambda(0)$ (intermodal MI); the conjecture that walk-off limits the cell bandwidth is refuted.
   - In normal dispersion, growth extends over $|\beta_2|\Omega^2L_{\rm NL}/2\lesssim0.2$, set by the nonlinear rate rather than $\lambda_1$; that refutes the $\sqrt{\lambda/\beta_2}$ guess too.
   - Order of magnitude for a 50 µm GRIN fibre at 1064 nm and 10 kW: $z_E\sim10^2$ m.
9. **Linear-response GGE** (post hoc). $\Delta\langle I_0\rangle=-[{\rm Cov}_{\rm D}(N_{\rm ex},W)/{\rm Var}_{\rm RJ}(H_{\rm res})](h_{\rm in}-\langle H_{\rm res}\rangle)$, with $c_m=\langle I_0\rangle(2S_{00mm}-S_{0000})$. It is within 0.005–0.017 of the toy, for shifts of 0.02–0.15.
10. **The pre-scrambling quantum state, linearized and exact** (run `…-grin-gaussian-state`).
    - Multimode squeezing grows by Kerr shear, then exponentially.
    - Mode-resolved photon counting with optimal weights reaches −20 to −27 dB at $400L_{\rm NL}$ (ideal), about −10 dB per decade of $z$. The note's conjecture that photon counting cannot see the squeezing is refuted.
    - The self-cleaned fundamental alone is squeezed by only −1 to −13 dB.
    - Single-mode entanglement entropy grows like $\ln z$, then linearly at a rate of order $\lambda_1$.
11. **GGE with the exact GRIN tensor** (run `…-grin-gge`). Pre-registered predictions for a centre-focused, disorder-free launch held: 0.695 and 0.587 predicted, 0.700 and 0.582 observed, RJ 0.739 and 0.609. In GRIN, aligned phases condense *less* than random ones, the opposite sign to the random-tensor toy. A sign statement in the note was wrong and is corrected.
12. **Robustness of photon-counting squeezing.** $\lambda_{\rm gen}(z)$ is nearly the same for $K=4$, 5, 6 (10–21 modes), and appears in the near-integrable case too, so it comes from shear, not chaos. The Lyapunov exponent scales as $\lambda_1L_{\rm NL}\approx0.067(1-f_0)$ (three points). With a degenerate fundamental (two polarizations, no $S_z$ conservation), the Dirichlet law is tilted by $(N-N_{\rm ex})$; Monte Carlo confirms.
13. **Few excitation quanta above a condensate (exact quantum microcanonical counting, GRIN $K=10$).** Antibunched at one quantum. $g^{(2)}$ rises toward 1.96. At $Q=60$ the depletion variance is 7 times the RJ value.
14. **Typical-experiment numbers** (card, Lab test; order of magnitude). $z_E\sim1$ km at 1 kW and $\sim100$ m at 10 kW in 50 µm GRIN fibre, so metre-scale experiments are pre-scrambling.
15. **The scrambling law with the exact GRIN tensor, pre-registered** (run `…-grin-twa-scrambling`). The collapse length is exactly linear in $\ln n$ over $n=10^6$–$10^{12}$. The slope matches $1/(2\lambda_1)$ within 7%: increment 404 against 377 predicted. PASS.
16. **Few quanta above a large condensate do not thermalize** (exact diagonalization in fixed $(N,Q)$ sectors; run `…-few-quanta-exact`). The excitation number is frozen, ${\rm Var}\,N_{\rm ex}\propto N^{-1.2}$, so the partition statistics of item 13 are not reached. This corrects an earlier statement on the card and in the note.
17. **Post-scrambling checks.** Shot-to-shot statistics past $z_E$ equal the Dirichlet law (GRIN TWA). A dephased input is thermal within 2–4 $L_{\rm NL}$, $n$-independent (pre-registered). The collapse is double-exponential in shape, at rate $\approx\lambda_1$ rather than $2\lambda_1$.
18. **C-03 prediction 2 revised before verification** (the sign of the phase effect in GRIN).
19. **A factor-2 error** in the ballistic formula was found and fixed during the session; the corrected prediction is the one quoted.
20. **Truncated Wigner against exact quantum dynamics** (four modes, $n=16$–100; run `…-exact-vs-twa-4mode`; note §6.6).
    - On the ballistic branch the TWA error in the mean-field fraction is $O(1/n)$: measured exponent $-1.08$ ($f_0=0.55$). It equals the closed-form Wigner error of Kerr phase diffusion, about $0.3/n$.
    - The condensate Fano factor agrees within 0.5–2.7 sampling errors, including a GRIN subset with real power exchange (exact Fano up to 1.58).
    - The chaotic branch is out of reach of exact methods here.
    - The comparison exposed a sign-convention error in my first exact code ($e^{-iHz}$ against the TWA codes' convention), which showed as an $n$-independent lag of the Fano dip. Fixed; all cases rerun.
21. **Shot-to-shot statistics at large $n$** (PI request; run `…-grin-shot-statistics`; note §6.7). Exact GRIN tensor, 15 modes, condensed launch, 128 shots per ensemble.
    - With a quiet laser at $n=10^{10}$, a fixed launch repeats to $g^{(2)}-1\sim10^{-8}$ for $z\le75L_{\rm NL}$ and $6\times10^{-3}$ at 300, against 0.867 thermal.
    - The noise is Gaussian: output variances scale with input noise to within $(0.7$–$1.2)\times10^4$ for a $10^4$ change, up to $z\approx100$.
    - Shots look thermal only past $z_E(n/F_{\rm in})$: about 150, 250 and beyond 300 $L_{\rm NL}$ for $n_{\rm eff}=10^4$, $10^6$, $10^{10}$. 1% common-mode jitter gives 0.34 at 100.
    - Phases redrawn per shot give the Dirichlet law within about $30L_{\rm NL}$: 0.80–0.99 against 0.867; condensate $(2.1$–$3.0)\times10^{-3}$ against $2.71\times10^{-3}$.
    - Implication, order of magnitude: in metre-scale experiments ($z\lesssim60L_{\rm NL}$ at 10 kW), RJ occupations describe the ensemble averaged over, not thermal fluctuations of individual shots.
    - **Within one pulse** (`pulse_stats.py`): the resonant dynamics scales as $I_p(z;s)=s\,i_p(sz)$, so the instants of a pulse sample one trajectory over a range of lengths. Across the FWHM the mode fractions vary with relative variance 0.32–0.68 at $z=30$–300, yet two pulses agree to $10^{-4}$ for $z\le100$: a deterministic temporal speckle. Pulse-integrated $f_0$ tends to the RJ value (0.749 against 0.739 at 300).
    - **21 modes ($K=6$)**: the same picture; at the same $E'$ the launch is more condensed ($f_0=0.78$) and scrambles later (thermal at about 200–250 $L_{\rm NL}$ for $n_{\rm eff}=10^4$); random phases give the 21-mode Dirichlet values.
    - **$\lambda_1$ against mode count at fixed $f_0=0.70$** (run `…-grin-lyapunov-modecount`): 0.024, 0.020–0.021, 0.019, 0.016, 0.015–0.016 $/L_{\rm NL}$ for 10, 15, 21, 28, 36 modes. It falls slowly with $M$ and levels off, so the $z_E$ estimates are not optimistic for fibres with more modes (single trajectories; T-...-04).

## Changed

- New files:
  - `problems/P-20261016-claude-interactive.7-01-quantum-state-of-rj-thermalized-light.md` (candidate, priority 2 pending the PI, literature_state open, novelty_confidence medium);
  - claims at cheap-checks-passed: `C-20261016-claude-interactive.7-01` (Dirichlet), `-02` (scrambling), `-03` (GGE);
  - `explorations/2026-10-16-claude-interactive.7-quantum-rj-state.md`;
  - run folders `runs/2026-10-16-claude-interactive.7-{rj-polytope-mc, rj-toy-thermalization, rj-toy-twa-scrambling, rj-toy-gge, grin-lyapunov, grin-gaussian-state, grin-gge, grin-twa-scrambling, few-quanta-exact, exact-vs-twa-4mode, grin-shot-statistics, grin-lyapunov-modecount}`. Raw output is under `~/analytical-nl-discovery-data/<run-id>/`.
- Tasks:
  - T-20261016-claude-interactive.7-01: done.
  - New:
    - -02, literature, not-claude;
    - -03, exact quantum check;
    - -04, Lyapunov exponent in real fibres;
    - -05, GGE and ideal-GRIN invariants;
    - -06, CW cells and TWA bins;
    - -07, -08, -09: verification of C-01, -02, -03, all not-claude.
    - -10: derive the photon-counting squeezing law, any.
    - -11: solver linear intra-group mode coupling, infra, not-claude.
    - -12: shot-to-shot statistics in a realistic experiment model, against published data, any.

## Not verified

- **The toy model is not a fibre**: random overlap tensor, exactly equidistant groups, $M\le15$, Brownian intra-group disorder. Its Lyapunov exponents, its coherence lengths, and the ballistic/chaotic crossover near $n\sim10^7$ need checking with real overlaps (T-...-04).
- **Truncated Wigner is not quantum mechanics.** Every scrambling statement here is a TWA statement. The exact four-mode check (finding 20) covers the ballistic branch at $n\le100$ only; the chaotic branch is unchecked (T-...-03).
- **Shot statistics (finding 21)** come from one 15-mode resonant model with one launch, Brownian disorder and no dispersion or pulse shape. The within-pulse result treats time slices as independent cells (no dispersion or walk-off between them) (T-...-12).
- **Kinetic route for dephased input.** The Rician one-mode law (Ornstein–Uhlenbeck form of the wave-turbulence PDF equation) was checked here by Itô calculus only. The original papers were not accessed.
- **Cell size.** The CW coherence-cell size $\Omega_\lambda$ and the spectral-broadening prediction are conjectures (T-...-06).
- **Novelty.** The Dirichlet law's novelty rests on a first-family search. Possible prior art not accessed: Vardi–Ramos–Kottos (full text), Picozzi & Rica 2012. Bienias et al. 2011 was checked at abstract level only; it is canonical.
- **Literature access.** Many entries on the card were read by the helper agents, not by this session; each is marked "(helper)".

## Loose ends

- T-20261016-claude-interactive.7-02: second-family literature audit, including Birk et al. (CLEO 2023), Vardi–Ramos–Kottos, Bienias et al. 2011, Picozzi & Rica 2012 and Podivilov et al. 2019.
- T-20261016-claude-interactive.7-03: exact quantum check of scrambling and reduced states.
- T-20261016-claude-interactive.7-04: $\lambda_1$ and $z_E$ in real GRIN and step-index fibres.
- T-20261016-claude-interactive.7-05: generalized-Gibbs endpoint with the ideal-GRIN invariants; dependence on disorder strength.
- T-20261016-claude-interactive.7-06: CW cell coupling, spectral broadening, TWA bin and window dependence.
- T-20261016-claude-interactive.7-07, -08, -09: verification of C-01, -02, -03 by another family.
- T-20261016-claude-interactive.7-10: the photon-counting squeezing law of the pre-scrambling state.
- T-20261016-claude-interactive.7-11: solver capability for intra-group disorder; it is missing today.
- T-20261016-claude-interactive.7-12: shot-to-shot mode-power statistics in a realistic experiment model (pulse shape, time-integrated detection, hundreds of modes, measured laser noise), against published data.
