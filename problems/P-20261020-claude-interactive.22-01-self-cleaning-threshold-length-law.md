---
id: P-20261020-claude-interactive.22-01
title: "Kerr self-cleaning in GRIN fibre: a quantitative crossover from coherent nonlinear-phase evolution to irreversible modal relaxation"
status: candidate
priority: 2
literature_state: open
novelty_confidence: medium
target_quantity: "A common-criterion onset length and coherent-to-kinetic crossover for a specified quasi-CW launch and measured GRIN disorder; determine the phase-memory and occupation-relaxation lengths rather than presupposing a measured universal inverse-length threshold."
model: "Spatial (quasi-CW, monochromatic) multimode Kerr propagation in a GRIN fibre: beat-averaged resonant model with the exact Hermite–Gauss or measured-profile Kerr tensor; a static deviation from the ideal profile (intra-group splitting delta); weak intra-group random coupling of strength Delta_beta (Garnier et al. 2019 model). Extensions: vector Kerr and polarization disorder; finite bandwidth (spatiotemporal resonances)."
oracle_ready: partial
last_audited: 2026-10-20
audited_by: [claude, gpt]
proposed_by: PI
provenance:
  agent: claude-interactive.22
  model: claude-opus-5-5
  family: claude
claims: []
results: []
last_review:
  agent: gpt-h
  model: gpt-6-astra
  family: gpt
  date: 2026-10-20
  task: T-20261020-claude-interactive-06
---

**Current text added by gpt-h (gpt; gpt-6-astra), 2026-10-20.** Novelty lowered high → medium; status remains candidate. The original scout text is retained below as superseded; the current assessment and source-access ledger are in the [cross-family review](../docs/review-2026-10-20-gpt-h-cross-family-novelty-claude-22-cards.md).

## Target quantity

For a specified modal tensor, launch ensemble and detector criterion, predict the length at which modal occupations approach a stated stationary distribution, together with decay of phase memory. Determine whether these are the same length, and how they depend on power, profile splitting and random linear coupling. Use $L_{\rm NL}=1/(\gamma P)$ and distinguish a clean output image from irreversible equilibration.

The old assertion that no mechanism predicts fixed nonlinear-phase onset is **superseded**. Krupa et al.'s mean-field argument already links length and power (2017 SI p. 5; [DOI:10.1038/nphoton.2017.32](https://doi.org/10.1038/nphoton.2017.32), full text read by gpt-h). Ferraro et al. 2023 explicitly discusses the power-length product ([arXiv:2304.12006](https://arxiv.org/abs/2304.12006), full text). A homogeneous cubic resonant model also has an elementary $\gamma Pz$ rescaling at fixed normalized launch; this alone proves no irreversible rate or RJ endpoint.

## Longstanding evidence

The Aschieri 2011 slow-mode-count passage, Fusaro 2019 long-length motivation, and Ferraro 2023/2025 limitations were checked in primary full text by gpt-h. Their quoted wording in the historical block is accurate, but their scope does not establish a newly unexplained exponent. Identifiers: DOI:10.1103/PhysRevA.83.033838; arXiv:2011.05111; arXiv:2304.12006; arXiv:2505.11299.

The strongest remaining evidence is the 2025 review's incomplete quantitative treatment of mixed coherent–incoherent experiments. It supports a crossover problem, not the blanket absence of a nonlinear-phase mechanism.

## Literature state

Open in the corrected quantitative sense; **novelty confidence medium**, lowered from high by gpt-h. The decisive correction is the original mean-field scaling argument and its explicit treatment in Ferraro 2023. A useful controlled rate theory may remain, but the exponent one or an empirical threshold fit is not independently high novelty.

## Kill search

Garnier 2019 already studies mixed coherent/incoherent propagation ([arXiv:2011.03918](https://arxiv.org/abs/2011.03918), full relevant text). Its weak-disorder kinetic law is restricted to its assumptions. Podivilov's instability threshold does not by itself fix a finite-length detection threshold ([arXiv:1811.10239](https://arxiv.org/abs/1811.10239), main model read).

Full-text checks of Baudin 2023, Sidelnikov 2019, Leventoux 2021, Mangini 2023, Chao 2025, Kabat 2025, Zitelli and Zanaglia found substantial coherent, disorder and kinetic theory, but no controlled solution of the corrected target. Exact identifiers and access sections are in the review. Liu 2016, DOI:10.1364/OL.41.003675, remains abstract-only for this reviewer; its unexamined details are not negative evidence.

## Sharpest statement of the gap

What quantitatively connects phase-sensitive nonlinear evolution with irreversible occupation relaxation when $\Delta\beta L_{\rm NL}\lesssim1$, for measured disorder and a fixed launch ensemble? Which observable admits a reduced rate with a controlled validity domain? Launch phases and correlations cannot be replaced by mode count and mean energy without justification.

## Analytical foothold and first derivation target

Derive or falsify a phase-correlation/memory closure in one specified modal system, then relate its prediction to an occupation-relaxation criterion. The old choice $\Gamma_{\rm eff}=\max(\Delta\beta,\kappa/L_{\rm NL})$ is an unproved ansatz, not a derived crossover. Static splitting can suppress resonances, and a positive Lyapunov exponent is not a mixing time. These are tests of the proposed route, not established conclusions.

## Dimensionless groups and regime

Retain $D=\Delta\beta L_{\rm NL}$, $\delta L_{\rm NL}$, $L_{\rm beat}/L_{\rm NL}\ll1$, the launch ensemble and normalized linear energy. Quasi-CW reduction requires both modal walk-off and dispersive reshaping small over the observation length. The historical parameter ranges and disorder estimates are exploratory, not measured validity bounds. Raman feasibility depends on the pulse and gain calculation, not a universal fixed Kerr-phase cap.

## Oracle

The propagator needs validated random linear coupling, the actual Kerr tensor and phase-sensitive ensemble diagnostics. Compare phase memory, occupations and detector-defined cleaning under window, step, mode-basis and disorder-sampling convergence. No new evaluator or propagation run was made by this review.

## Lab test

Use a common time-gated modal/phase criterion over several cut-back lengths, fixed launch statistics and measured disorder, tracking power along the fibre.

**Evidence correction.** The Krupa 3 m/12 m comparison uses different short/long diagnostics; its main cut-back is at fixed power. Pourbeyram's 0.5 m endpoint is reached by the highest tested power and therefore bounds a threshold; its ultrashort pulses complicate a monochromatic comparison ([DOI:10.1038/s41567-022-01579-y](https://doi.org/10.1038/s41567-022-01579-y), Fig. 4 read and inspected). These support the literature's nonlinear-phase interpretation, but do not establish a common-criterion exponent with uncertainty that excludes $L^{-1/2}$. The earlier numerical comparisons remain in run 2026-10-20-claude-interactive.22-resonance-kinematics/threshold_exponents.json; no new fit was made.

## Relation to existing cards

P-005 owns joint mode–frequency equilibration; P-010 already includes finite-length detector-defined cleaning thresholds and disorder. This quasi-CW subproblem needs a PI ownership decision before a separate derivation campaign.

## Superseded scout text

<details>
<summary>Original 2026-10-20 scout formulation, superseded by the review above</summary>

This block preserves the initial hypotheses, evidence interpretations and access history. It is not the current card assessment. The changed metadata was:

- Former title: "The threshold–length law of Kerr self-cleaning in GRIN fibre: an onset at fixed accumulated nonlinear phase that no current mechanism predicts"
- Former novelty_confidence: high
- Former last_audited: null
- Former target_quantity: "The onset length L_th of Kerr beam self-cleaning (Rayleigh–Jeans-like modal distribution) of quasi-CW light in GRIN fibre, as a function of power, launch and the perturbations that break the ideal-GRIN obstruction to ergodicity, i.e. the law P_c(L) ~ L^-x and its constant: measured x close to 1 (gamma P_c L roughly constant), against x = 1/2 from weak-disorder wave turbulence, an L-independent parametric threshold, and an L_d-limited (power-independent) onset."

### Superseded: Target quantity

**Definitions.**
- **Onset length** $L_{\rm th}(P)$: the length at which the fundamental-mode occupation (or the mean-square distance to the equilibrium distribution) reaches its plateau value. Use a stated criterion and a stated launch.
- **Threshold** $P_c(L)$: its inverse. Write the result as $P_c\propto L^{-x}$, or equivalently $L_{\rm th}=c\,L_{\rm NL}^{\,y}$ with $L_{\rm NL}=1/(\gamma P)$.

**What the competing pictures predict.**

| Picture | Source | Prediction |
|---|---|---|
| Weak-disorder wave turbulence | Fusaro et al. 2019; Garnier et al. 2019 | $L_{\rm kin}\sim\Delta\beta L_{\rm NL}^2/\bar S^2$, so $x=1/2$ |
| Three-mode parametric instability | Podivilov et al. 2019 | An $L$-independent power threshold, $\sim10$ kW |
| Disorder-limited breakdown of the coherent regime | inferred by this card from Ferraro et al. 2025, §2.2 | Onset at $L\sim L_d$, independent of power once nonlinearity dominates |
| Accumulated nonlinear phase | Krupa et al. 2017 (empirical) | $x=1$, $\gamma P_cL\approx$ const |

**Wanted.**
- A derived $L_{\rm th}/L_{\rm NL}$, giving $x$ and the constant $c$, as a function of:
  - the launch: number of excited modes $M_{\rm exc}$ and normalized energy $u$;
  - the ergodicity-breaking perturbations: profile splitting $\delta$ and disorder $\Delta\beta$.
- The crossovers between the regimes in the table above.
- Which perturbation restores ergodicity in a real fibre.

### Superseded: Longstanding evidence

- **Earliest statement that wave turbulence is too slow.**
  - Aschieri, Garnier, Michel, Doya & Picozzi, PRA 83, 033838 (2011), [DOI:10.1103/PhysRevA.83.033838](https://doi.org/10.1103/PhysRevA.83.033838). This predates the discovery of self-cleaning. Their simulations show "the thermalization process slows down significantly as the number of modes" grows. Full text, passage read by claude-interactive.22 from the author-hosted PDF.
- **First statement framed against self-cleaning.**
  - Fusaro, Garnier, Krupa, Millot & Picozzi, PRL 122, 123902 (2019), [arXiv:2011.05111](https://arxiv.org/abs/2011.05111). The abstract says complete thermalization is "known to require prohibitive large interaction lengths". Access: abstract, read by claude-interactive.22; full-text passages read in the claude-interactive.21 review.
  - The claimed fix is acceleration by weak disorder. This card argues it does not explain the measured length law (below).
- **Empirical law.**
  - Krupa et al., Nat. Photon. 11, 237 (2017), [DOI:10.1038/nphoton.2017.32](https://doi.org/10.1038/nphoton.2017.32); arXiv:1603.02972.
  - The Supplementary Information compares 3 m and 12 m of fibre. It concludes that the product of power and fibre length is the critical parameter.
  - Access: SI full text (helper .22.1). The power-times-length passage was re-read by claude-interactive.22 from the publicly hosted SI PDF. Main text not accessed.
- **Explicit open statements, 2023.**
  - Ferraro, Mangini, Zitelli & Wabnitz, Adv. Phys. X 8, 2228018 (2023), [arXiv:2304.12006](https://arxiv.org/abs/2304.12006). Full text, read by claude-interactive.22.
  - The mechanism of self-cleaning is "still the subject of a hot debate, and it remains highly controversial".
  - The same paper calls the thermalization threshold something any theory would likely be unable to determine, because it is set by disorder.
  - It says the shape of the separatrix $P_c$ (number of excited modes) remains elusive.
  - It states that $P_c$ grows exponentially with the launch angle (Ferraro et al., JLT 2023, [arXiv:2205.13385](https://arxiv.org/abs/2205.13385)) and decreases with fibre length.
- **Most recent restatement, 2025: the deciding source.**
  - Ferraro, Baudin, Gervaziev, Fusaro, Picozzi, Garnier et al., Physica D 481, 134758 (2025), [arXiv:2505.11299](https://arxiv.org/abs/2505.11299). Full text, read by claude-interactive.22.
  - Of the purely spatial kinetic theory with weak disorder: "it cannot provide a complete description of the experimental results".
  - Its §2.5 says this theory agrees with simulations without free parameters only for $L_d\ll L_{\rm NL}$. It also says experiments sit in a mixed coherent–incoherent regime that the theory understands only qualitatively (paraphrase).
  - Without disorder, a phase-sensitive coherent regime with quasi-reversible power exchange tends to freeze RJ thermalization (their §2.2).
  - Recent results have questioned self-cleaning as a pure thermalization process.
  - Time averaging as the origin of the observed RJ agreement is an untested hypothesis (their §4).
- **The other main group.** Wright, Wu, Christodoulides & Wise, Nat. Phys. 18, 1018 (2022), [DOI:10.1038/s41567-022-01691-z](https://doi.org/10.1038/s41567-022-01691-z). Full text of the NSF-PAR accepted manuscript (helper .22.1).
  - They regard the endpoint of self-cleaning as explained by optical thermodynamics.
  - They note that dissipation and disorder correlate with the cleaning rate, but give no rate theory (paraphrase).
- **Correction to the orchestrator's seed.** Baudin et al., Opt. Commun. 545, 129716 (2023), [arXiv:2309.02215](https://arxiv.org/abs/2309.02215) (abstract, helper .22.1) does not say that cleaning is not RJ thermalization. It reports coherent-launch cleaning driven by an incipient RJ thermalization.

**Claimed resolutions and why they do not close the problem.**

| Work | Claim | Why it does not explain $P_c\propto L^{-1}$ |
|---|---|---|
| Fusaro et al. 2019; Garnier et al., PRA 100, 053835 (2019), [arXiv:2011.03918](https://arxiv.org/abs/2011.03918) (full text, helper .22.1 and the claude-interactive.21 review) | Disorder accelerates condensation by $\sim\beta_0/\Delta\beta$ | Predicts $L\propto L_{\rm NL}^2$, so $x=1/2$. Valid only for $L_d\ll L_{\rm NL}$; the experiments sit at $L_{\rm NL}/L_d\approx0.1$–0.75 (see the regime section). Garnier et al. themselves write that their theory and simulations "cannot provide a quantitative description of the experimental results" (full text read by claude-interactive.22). They attribute this to temporal averaging in pulsed experiments; averaging over slices of different power smooths the onset but leaves the per-slice exponent $x=1/2$. The disorder parameters were never measured in the cleaning experiments. |
| Podivilov et al., PRL 122, 103902 (2019), [arXiv:1811.10239](https://arxiv.org/abs/1811.10239) (threshold passage read by claude-interactive.22) | 2D hydrodynamic turbulence; threshold from an integrable three-mode model, $P\sim10$ kW | Length-independent threshold |
| Biasi, Evnin & Malomed, PRE 104, 034210 (2021), [arXiv:2106.03870](https://arxiv.org/abs/2106.03870); PRE 108, 034204 (2023), [arXiv:2304.10308](https://arxiv.org/abs/2304.10308) (abstracts, helper .22.1) | The ideal harmonic-trap resonant dynamics has FPU recurrences and an obstruction to ergodicity | Explains the freezing; says nothing about how fast real fibres thermalize |
| Zanaglia et al., PRL 136, 053802 (2026), [arXiv:2506.23536](https://arxiv.org/abs/2506.23536) (full text per the claude-interactive.21 review) | A temporal continuum overcomes the discrete-mode obstacles; parabolic fibres freeze without disorder | Stationary incoherent CW theory, with thermalization over $10^3$–$5\times10^3L_{\rm NL}$; not a few-$L_{\rm NL}$ law |
| C-20261016-claude-interactive.7-03 (this registry) | Without disorder the endpoint is a GGE of $(N,E_{\rm lin},H_{\rm res})$, not RJ | Endpoint, not rate |
| Biasi, PRE 110, 034107 (2024), [arXiv:2401.15083](https://arxiv.org/abs/2401.15083) (partial full text, helper .22.1); Biasi & Gérard, CMP (2025), [DOI:10.1007/s00220-025-05449-5](https://doi.org/10.1007/s00220-025-05449-5) (abstract) | Exact finite-time coherent condensation in solvable resonant systems, including the radial harmonic-trap GPE; nonlinear optics proposed as a test ground | Solvable sub-manifolds, not generic launches; no rate law; never compared with cleaning data. Partly pre-empts the coherent idea of route 2 below. |
| Ramos et al., Commun. Phys. (2023), [DOI:10.1038/s42005-023-01309-7](https://doi.org/10.1038/s42005-023-01309-7); Chao, Fang & Yu, PRA (2025), [DOI:10.1103/k453-gplh](https://doi.org/10.1103/k453-gplh) (abstracts, helper .22.1) | One-parameter scaling of relaxation rates in disordered lattices; quasi-resonances explain the robustness of cleaning to bending | Not GRIN cleaning rates |

### Superseded: Signal of hidden simplicity

Run `2026-10-20-claude-interactive.22-resonance-kinematics`, `threshold_exponents.json`.

**Pourbeyram et al. 2022.** Nat. Phys. 18, 685 (2022), [arXiv:2012.12110](https://arxiv.org/abs/2012.12110); Fig. 4 caption and main text read by claude-interactive.22.
- Equilibrium is reached at about 52 kW in 0.5 m, and only at the highest power. That makes 52 kW an upper bound on $P_c$.
- The onset is at about 17 kW in 1.5 m.
- Hence $x\le1.02$. Equivalently, the onset is at $L\approx7.3\,L_{\rm NL}$ in 1.5 m, and at most $7.4\,L_{\rm NL}$ in 0.5 m, using the paper's $L_{\rm NL}$.
- The paper: the fundamental-mode occupation "reaches and retains its equilibrium value after propagating a few nonlinear lengths".

**Krupa et al. 2017 SI.** Pairing like criteria at 12 m and 3 m gives $x$ = 1.00–1.16. Pairing all criteria gives 0.74–2.03.

**Status of this evidence.** It is weak.
- Two lengths per experiment, with different criteria.
- Helper .22.1's assessment: at the power-step resolution of either data set, neither excludes $x=1/2$. Pourbeyram's Fig. 4a plotted against $L/L_{\rm NL}$ shows both lengths thermalizing near $L/L_{\rm NL}\approx6$.
- No experiment found reports $x=1/2$.
- No controlled series of $P_c(L)$ at fixed launch with measured disorder exists; helper .22.1 searched for one. If confirmed, $L_{\rm th}=c\,L_{\rm NL}$ with $c\approx7$ (Pourbeyram's definition) is a one-parameter law that none of the mechanisms in the table predicts.

### Superseded: Literature state

Above, plus:
- Mangini et al., OE 30, 10850 (2022), [arXiv:2111.08063](https://arxiv.org/abs/2111.08063): equilibrium theory; uses power tuning as an equivalent of cut-back. Full text (helper .22.1; gpt-f review).
- Deliancourt et al., OSA Continuum 2, 1089 (2019), [DOI:10.1364/OSAC.2.001089](https://doi.org/10.1364/OSAC.2.001089): LP11 self-cleaning at 4–5 kW versus about 1 kW for LP01, in 6–8.3 m. Helper .22.1 found no multi-length series in it, although the 2023 review cites it for the length dependence.
- Ferraro et al., JLT (2023), [DOI:10.1109/JLT.2023.3239385](https://doi.org/10.1109/JLT.2023.3239385): $P_c$ against tilt angle, fitted with an empirical exponential; no fitted parameters given. Full text (helper .22.1); figures not digitized.
- Torres et al., PRL 136, 173801 (2026), [arXiv:2512.17777](https://arxiv.org/abs/2512.17777): reversible anomalous-correlator dynamics against irreversible kinetics in two-wave fibre systems. A phase-sensitive closure, the kind this problem needs. Access per P-005.

### Superseded: Kill search

**Helper claude-interactive.22.1, 2026-10-20** (log in the review, §5).
- **Forward citations from 2021**, OpenAlex:
  - Fusaro 2019: 72 citing works;
  - Garnier 2019: 27;
  - Podivilov 2019: 70;
  - Krupa 2017: 401, keyword-filtered;
  - Biasi–Evnin–Malomed 2021: 16;
  - Biasi–Evnin–Malomed 2023: 11.
- **Queries.** Targeted queries on the self-cleaning threshold, cleaning length against power, cut-back, and the resonant-system and continuous-resonant-equation theory of GRIN.
- **Relevant hits.**
  - In Fusaro 2019's citing set:
    - Zanaglia 2026 (PRL and PRA);
    - Torres 2026;
    - Chao 2025;
    - Kabat 2025;
    - Biasi 2024; Biasi & Gérard 2025;
    - Baudin 2023;
    - Ferraro 2023 and 2025;
    - Mangini, OL 48, 3677 (2023), on phase locking;
    - Ramos 2023;
    - Zitelli 2024.
  - In Podivilov 2019's set: "High-temperature wave thermalization spoils beam self-cleaning", OL (2023).
  - In Krupa 2017's set:
    - "Optical kinetic theory of nonlinear multimode photonic networks", PRL 132, 193802 (2024); about transport, not cleaning;
    - "Accelerated beam self-cleaning by Raman soliton trapping in tapered MMF", JLT (2025); abstract not available.
- **Outcome.**
  - No paper derives an onset length proportional to $L_{\rm NL}$ with a computed constant.
  - No paper flags the $P^{-1}$ against $P^{-2}$ discrepancy. Searched with the extended query `beam self-cleaning occurs within a few nonlinear lengths scaling "nonlinear length" kinetic wave turbulence prediction inconsistent coherent mechanism graded-index`.
  - No paper derives the crossover to the kinetic law.
  - No paper identifies which perturbation restores ergodicity at the measured rate.

**Second pass, claude-interactive.22, 2026-10-20.**
- **Forward citations from 2024**, OpenAlex:
  - Pourbeyram 2022: 76 citing works;
  - Ferraro 2023: 27;
  - Ferraro 2025: 5;
  - Zanaglia 2026 PRL: 3;
  - Mangini 2022: 54;
  - Baudin 2023: 9.

  That is 107 unique titles, scanned by keyword. Abstracts read: Kabat et al., PRA (2025), [DOI:10.1103/xqyx-g3tn](https://doi.org/10.1103/xqyx-g3tn); Mangini et al., SPIE (2025); Cirimele et al., EPJ Web Conf. (2026); Labaz & Sidorenko, OL (2024); Li, Ruelle, Ryczkowski & Dudley, CLEO/Europe (2025).
- **Kabat et al. (2025).** Relaxation rates are tied to supermode correlations in designed networks, not to GRIN cleaning.
- **Other abstracts.** Entropy maximization against power and against length (Mangini 2025); shot-to-shot fluctuations decrease with power (Cirimele 2026).
- **New risk.** Li et al. (CLEO/Europe 2025, [DOI:10.1109/cleo/europe-eqec65582.2025.11109609](https://doi.org/10.1109/cleo/europe-eqec65582.2025.11109609), abstract) made the first real-time, spectrally resolved holography of the output field. They report that the field at the pump wavelength is never clean. The onset criterion of this card must be defined on a stated spectral and temporal gate (see P-010).
- **Outcome.** No derived threshold–length law.

### Superseded: Sharpest statement of the gap

The only quantitative rate theory of GRIN thermalization predicts $L\propto L_{\rm NL}^2$ (weak-disorder wave turbulence). The two published two-length data sets point to $L_{\rm th}\approx c\,L_{\rm NL}$. They sit outside that theory's regime, $L_{\rm NL}/L_d\lesssim1$.

In that regime the ideal fibre is non-ergodic, which the literature calls the coherent, freezing regime. No theory says:
- what restores ergodicity there: profile non-ideality, residual disorder, polarization or bandwidth;
- at what rate it does so;
- hence what $x$ and $c$ are.

### Superseded: Analytical foothold and first derivation target

**First target.** Take the beat-averaged GRIN model with the exact Hermite–Gauss tensor, add a static intra-group splitting $\delta$, and keep $\Delta\beta L_{\rm NL}\lesssim1$. Derive $L_{\rm th}/L_{\rm NL}$ and decide which of these holds:
- (a) it tends to a launch-only constant $c(M_{\rm exc},u)$ once $\delta L_{\rm NL}$ exceeds a threshold, which gives $x=1$;
- (b) it depends on $\delta L_{\rm NL}$, which gives another $x$.

**Routes.**
1. **Self-consistent resonance broadening.** Replace the fixed resonance width of the kinetic equation by $\Gamma_{\rm eff}=\max(\Delta\beta,\ \kappa/L_{\rm NL})$, of the direct-interaction (DIA) type. This gives $L_{\rm th}\sim L_{\rm NL}^2\Gamma_{\rm eff}/\bar S^2$, hence $c=\kappa/\bar S^2$ for $\Delta\beta L_{\rm NL}\ll\kappa$, and a crossover to $x=1/2$ at $\Delta\beta L_{\rm NL}\approx\kappa$.
2. **Chaos on the resonant shell.** Compute the Lyapunov spectrum and the mixing time of the resonant model against $\delta L_{\rm NL}$. The repository's resonant GRIN code gives $\lambda_1$ for $\delta=0$ (runs `2026-10-16-claude-interactive.7-grin-lyapunov*`).
3. **Phase-sensitive kinetics.** Use an anomalous-correlator closure, in the manner of Torres et al. 2026, for the coherent regime.

**Second target.** The angle dependence $P_c(\theta)$, reported as exponential by Ferraro et al. 2023. Split it into:
- the kinetic part, $c(M_{\rm exc})$;
- the equilibrium part: the RJ condensate fraction at $u(\theta)$, which decides whether a clean beam exists at all.

### Superseded: Dimensionless groups and regime

| Group | Meaning | Card's range |
|---|---|---|
| $\Lambda=\gamma PL=L/L_{\rm NL}$ | accumulated nonlinear phase | 1–25 (Raman budget, run `raman_budget.json`) |
| $D=\Delta\beta L_{\rm NL}=L_{\rm NL}/L_d$ | disorder against nonlinearity; kinetic theory needs $D\gg1$ | 0.01–10 |
| $\tilde\delta=\delta L_{\rm NL}$ | profile-induced intra-group splitting against nonlinearity | 0.01–10 |
| $B=L_{\rm beat}/L_{\rm NL}$, $L_{\rm beat}=2\pi/\beta_0$ | validity of beat averaging | $\ll1$ (about $10^{-3}$–$10^{-2}$) |
| $M_{\rm exc}$, $u$ | launch: number of excited modes; normalized linear energy | 5–100; any |
| $L\,\Delta\beta_1/T_0$; $L/L_D$ | modal walk-off against pulse length; dispersion | $\ll1$ (quasi-CW) |

Illustrative position of the experiments, with $L_d=0.4$ m from Fusaro's estimate (not measured in these fibres): $D\approx0.13$ (Pourbeyram, top energy) and $D\approx0.75$ (Krupa, 2.5 kW). Run `threshold_exponents.json`.

### Superseded: Conjectures

None filed. Working hypothesis: route 1 with $\kappa=O(1)$ in the regime $D\ll1<\tilde\delta$.

### Superseded: Oracle

- **Cheap test.** The resonant GRIN model of runs `2026-10-16-claude-interactive.7-*`, with the exact tensor and 15–55 modes. Add a static $\delta$ and the intra-group random coupling already used in `2026-10-17-claude-interactive.7-disorder-model-scan`. Measure $L_{\rm th}$ against $P$ at fixed launch, and fit $x$ and $c$. Then scan $D$ and $\tilde\delta$. CPU and memory are small.
- **The solver.** FastDifferentiableMMNLO checks the full, non-beat-averaged multimode GNLSE with a measured index profile, quasi-CW or pulsed. It has **no random linear mode coupling**, so $D>0$ needs either the beat-averaged code or a solver extension (`docs/SOLVER.md`). Hence `partial`.
- **Numerical artefacts to rule out.** Mode-basis truncation; step size; the definition of the onset criterion (report $x$ under two criteria).

### Superseded: Lab test

**Measurement.**
- A cut-back $P_c(L)$ series at five or more lengths between 0.3 and 30 m.
- One GRIN fibre, fixed launch (offset and tilt), sub-ns pulses (quasi-CW).
- Disorder characterized: polarization beat length and correlation length.
- Repeat on the same fibre with the disorder raised deliberately: tighter coiling, twist or microbending.

**What distinguishes the pictures.**

| Picture | $x$ | Effect of raising disorder |
|---|---|---|
| Coherent-regime law (hypothesis) | 1 | Moves the crossover to lower power; $c$ unchanged while $D\ll1$ |
| Weak-disorder wave turbulence | 1/2 | Changes the prefactor |
| Parametric threshold | 0 | — |
| $L_d$-limited onset | A step at $L\approx L_d$ | — |

**Second measurement.** Per-shot data against data averaged over random phases (SLM or diffuser). This separates the GGE endpoint (C-20261016-claude-interactive.7-03) from RJ.

### Superseded: How a solution would be recognized

1. A formula for $L_{\rm th}/L_{\rm NL}$ as a function of $(M_{\rm exc},u,\tilde\delta,D)$, with the measured exponent $x$ reproduced by resonant-model numerics within 0.1 on launches not used to build it.
2. The constant $c$ predicted to within 30% without fitting.
3. The crossover to $x=1/2$ located correctly when $D$ is scanned.
4. The beat-averaging error shrinking linearly in $B$.
5. Consistency with the published two-length data: $x\approx1$, onset $\approx7L_{\rm NL}$ in Pourbeyram's definition.

### Superseded: Relation to existing cards

- **P-010.** Finite-pulse and walk-off corrections to the cleaning criterion. Those corrections sit on top of the quasi-CW law asked for here; this card does not own them.
- **P-005.** It says generic kinetic-rate questions are substantially solved. This card disputes that for the experimental regime $D\lesssim1$; a See-also line has been added there.
- **P-20261016-claude-interactive.7-01 / C-…7-03.** The $D=\tilde\delta=0$ endpoint. This card asks for the rate and the mechanism.
- **P-20261002-gpt-a-03.** Modal phase coherence; coherence preservation during cleaning is related.
- **T-20261020-claude-interactive.21-01.** Scoping of the coherent femtosecond regime; its Pourbeyram data overlap with this card. Coordinate before either becomes a claim.

### Superseded: Risks and must-reads

- **The empirical $x\approx1$ may not survive** a controlled series. The two data sets use different criteria and two lengths each, and Pourbeyram's pulses are femtosecond, so spatiotemporal effects enter. If $x=1/2$ is measured, the card reduces to testing Garnier 2019, a modest task.
- **Main kill risk.** Zanaglia et al. 2026 (PRL and PRA): spatiotemporal quasi-resonances that greatly outnumber the spatial ones. If the Picozzi group tests this against measured cleaning lengths, it may be presented as the resolution. As published it is CW theory and simulation, with thermalization over $10^3L_{\rm NL}$ and more.
- **Cross-family objection to expect:** that this is P-010 or P-005 in disguise. The answer is in the section above. The PI should decide whether to merge.
- **Must-reads:**
  - the Krupa 2017 main text (paywalled);
  - Liu et al., OL 41, 3675 (2016);
  - Leventoux et al., OL 46, 66 (2021);
  - the full texts of Biasi–Evnin–Malomed 2021 and 2023;
  - Wright et al., Nat. Phys. 18, 1018 (2022) (paywalled).

</details>

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-20 | claude-interactive.22 (claude; claude-opus-5-5) | Created as candidate on the PI's request for longstanding high-novelty thermalization problems; literature_state open; novelty high (explicit 2019, 2023 and 2025 statements; first-family kill search negative for a derived threshold–length law); priority 2 pending PI decision | `docs/review-2026-10-20-claude-interactive.22-longstanding-optical-thermalization.md`; run `2026-10-20-claude-interactive.22-resonance-kinematics` |
| 2026-10-20 | gpt-h (gpt; gpt-6-astra) | Novelty lowered high → medium; status remains candidate. Current scientific text replaced; superseded scout text retained. | Krupa 2017 SI p. 5, DOI:10.1038/nphoton.2017.32; Ferraro 2023, arXiv:2304.12006 (full text); [review](../docs/review-2026-10-20-gpt-h-cross-family-novelty-claude-22-cards.md) |
