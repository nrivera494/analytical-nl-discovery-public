---
agent: claude-interactive.22
model: claude-opus-5-5
family: claude
date: 2026-10-20
task: T-20261020-claude-interactive-04
helpers: "claude-interactive.22.1 to .22.4 (claude family; general-purpose subagents, model inherited from the parent session, claude-opus-5-5; web searches only)"
cards: [P-20261020-claude-interactive.22-01, P-20261020-claude-interactive.22-02, P-20261020-claude-interactive.22-03]
---

# Longstanding open problems in optical thermalization: Claude-family scouting review

## Summary

**The request.** The PI asked for longstanding open problems in optical thermalization where novelty could be argued as high.

**What was screened.** 28 candidates against the task's four criteria, each with a kill search:
- the orchestrator's seven seeds S1–S7;
- 21 further candidates N1–N21, most of them found by mining reviews and outlooks.

**Shortlist, ranked.** Three cards are filed; the fourth item has a scoping task instead.

| Rank | Card | Problem | Novelty | Priority |
|---|---|---|---|---|
| 1 | [P-20261020-claude-interactive.22-02](../problems/P-20261020-claude-interactive.22-02-non-gibbs-breather-condensation-coupled-core-fibre.md) | Light above infinite temperature in coupled-core fibre: the isolated-lattice route to non-Gibbs breather condensation | high | 2 |
| 2 | [P-20261020-claude-interactive.22-01](../problems/P-20261020-claude-interactive.22-01-self-cleaning-threshold-length-law.md) | The threshold–length law of Kerr self-cleaning in GRIN fibre | high | 2 |
| 3 | [P-20261020-claude-interactive.22-03](../problems/P-20261020-claude-interactive.22-03-frequency-local-invariant-relaxation-single-mode-fibre.md) | What relaxes the frequency-local invariant of incoherent light near zero dispersion | medium | 3 |
| 4 | no card | Replica-symmetry-breaking signatures in random and mode-locked fibre lasers: what does the overlap measure? | — | task created |

**Seeds that did not survive.**
- Killed:
  - S2 as posed: the ideal-GRIN resonant obstruction to ergodicity is published (Biasi, Evnin & Malomed 2021, 2023);
  - S4: the soliton-plus-background equilibrium is settled (Jordan & Josserand 2000; Rumpf & Newell 2001, 2003; Tolomeo & Weber 2023);
  - N1, the Floquet heating I proposed: it was published in November 2025 (Moorcroft et al., arXiv:2511.08355).
- Parked:
  - S6: no route to self-similar condensation in discrete GRIN, and no observation;
  - S7: the asymptotic question is now held by rigorous sub-power-law results; no fibre experiment can reach the needed times.

**One computation.** Run [`2026-10-20-claude-interactive.22-resonance-kinematics`](../runs/2026-10-20-claude-interactive.22-resonance-kinematics/). It contains:
1. the $\beta_3$ and $\beta_4$ four-wave factorizations;
2. a check that quasi-energy Umklapp channels are open in two-loop fibre lattices, with weight 0.40–0.51 of the normal channels (not converged);
3. a Raman budget: about 25 rad of Kerr phase before stimulated Raman threshold in silica, which limits every quasi-CW test proposed here;
4. the length exponents of published self-cleaning thresholds.

**Not done.** No derivation and no propagation run. Many sources were read only as abstracts; the ledger says which.

## 0. Method

**Criteria.** These are the task's criteria; a candidate is shortlisted only if all four hold.
1. **Longstanding.** One of three things holds:
   - the problem has been stated as open in the literature for years;
   - an experiment–theory discrepancy has persisted without an accepted resolution;
   - it is a named conjecture.

   For each candidate the review gives the earliest explicit statement found, the most recent restatement, and every claimed resolution, with an assessment.
2. **High novelty if solved.** A solution settles a recognized question and is not a modest adaptation of existing theory.
3. **Analytical foothold.** There is a concrete first derivation target.
4. **Testable.** A fibre measurement distinguishes a solution from current explanations, and a numerical check exists.

**Kill search.** For every candidate we looked for 2021–2026 work that solves it, by two routes:
- forward citations of its key papers, from the OpenAlex `cites:` filter, with titles scanned and abstracts read for the hits;
- targeted queries.

**Who did what.** Four helpers ran the searches in parallel, one per cluster:
- .22.1: GRIN and multimode fibre;
- .22.2: lattices;
- .22.3: single-mode fibre and coherent structures;
- .22.4: lasers, plus mining the reviews.

I re-read the passages that the shortlisted cards rest on myself, and say so where I did. Every other access level is the helper's and is labelled as such.

**Rules followed.**
- Legitimate sources only: arXiv, publisher landing pages, author and institutional repositories, and the OpenAlex, Crossref and Semantic Scholar APIs.
- No sign-in. Captchas at opg.optica.org and a bot challenge at hal.science were met and not bypassed; other copies were used where they existed.
- Open-access PDFs went to `~/analytical-nl-discovery-data/lit-T-20261020-claude-interactive-04/`, outside git.
- Quotations are under 15 words, at most one per source, and only from text that was read.
- The other scout's branch was not read.

**Process error.** One request by helper .22.1, its first curl to arXiv, carried the user's e-mail address in the User-Agent header, against the session's instructions. Later requests used a generic header. Recorded in the log.

## 1. Long list

| Id | Candidate | Verdict | Deciding source |
|---|---|---|---|
| S1 | Self-cleaning rate paradox in GRIN fibre, sharpened to the threshold–length law | **shortlist → card -01** | Ferraro et al., Physica D 481, 134758 (2025), §2.5; Garnier et al., PRA 100, 053835 (2019) |
| S2 | Ideal GRIN as a resonant system: invariants, GGE, ergodicity | **kill as posed**; residue folded into -01 | Biasi, Evnin & Malomed, PRE 104, 034210 (2021) and PRE 108, 034204 (2023) |
| S3 | Negative-temperature (non-Gibbs) breather localization of the DNLS in fibre | **shortlist → card -02** | Iubini & Politi, PRL 134, 097102 (2025); Kabat et al., PRL 137, 103803 (2026) |
| S4 | Soliton fraction and radiation temperature of focusing multimode light | **kill** | Jordan & Josserand, PRE 61, 1527 (2000); Tolomeo & Weber, arXiv:2306.07697 |
| S5 | Thermalization of incoherent light in single-mode fibre with degenerate four-wave resonances | **shortlist → card -03** | Vassilev, CMP 406, 293 (2025); Picozzi et al., Phys. Rep. 542, 1 (2014), §6.2 |
| S6 | Universal self-similar condensation and non-thermal fixed points in multimode fibre | **park** | Ferraro et al. 2025, §2.3.7; Zanaglia et al., PRL 136, 053802 (2026) |
| S7 | Nonlinear destruction of Anderson localization: does spreading continue? | **park** (fails criterion 4) | De Roeck, Huveneers & Prośniak, PRE 109, 044207 (2024); Vakulchyk, Fistul & Flach, PRL 122, 040501 (2019) |
| N1 | Floquet (Umklapp) heating against RJ in Kerr fibre-loop lattices | **kill** | Moorcroft et al., arXiv:2511.08355 (2025) |
| N2 | Chaos border (Chirikov/KAM) for thermalization in chaotic multimode fibre | **park** (borderline kill) | Frahm & Shepelyansky, PRL 131, 077201 (2023) |
| N3 | KPZ fluctuations in the DNLS (fibre lattices) | **kill** as longstanding | Mendl & Spohn, J. Stat. Mech. (2015) P08028 |
| N4 | Discrete (mesoscopic) wave turbulence and the self-cleaning onset in step-index fibre | **park** | Garnier et al. 2019, §VI.1; Ermann, Chepelianskii & Shepelyansky, J. Phys. A 59, 055702 (2026) |
| N5 | Replica-symmetry breaking in random and mode-locked fibre lasers | **shortlist (rank 4), no card; scoping task** | Sarkar, Bhaktha & Andreasen, Sci. Rep. 10, 2628 (2020); Tommasi et al., Sci. Rep. 6, 37113 (2016) |
| N6 | Statistical theory of noise-like pulses in fibre lasers | **park** (second tier) | Meng et al., Nat. Commun. 12, 5567 (2021) |
| N7 | Self-starting of passive mode locking as a noise-activated transition | **kill** | Gordon, Gat, Fischer & Kärtner, OE 14, 11142 (2006) |
| N8 | Photon BEC in an Er/Yb fibre cavity | **kill** | Weill et al., OE 29, 27807 (2021); Liu & Xie, Open Phys. (2022) |
| N9 | Wave-turbulent spectral broadening of Raman and random fibre lasers | **kill** | Babin et al., JOSA B 24, 1729 (2007); Churkin et al., Nat. Commun. 6, 6214 (2015) |
| N10 | Laminar–turbulent transition of fibre lasers (directed percolation) | **park** | Turitsyna et al., Nat. Photon. 7, 783 (2013); Faggian et al., PRL 120, 173901 (2018) |
| N11 | FPUT recurrence to thermalization of modulational instability in fibre | **park**, merged into -03 | Vanderhaegen et al., PRA 106, 033519 (2022) |
| N12 | KZ cascades and the 2D-NLS flux-direction puzzle in optics | **kill** for this programme | Baudin et al., EPL 134, 14001 (2021) |
| N14 | Boltzmann against Gibbs entropy at negative optical temperature | **kill** | Buonsante, Franzosi & Smerzi, PRE 95, 052135 (2017) |
| N15 | Lynden-Bell violent relaxation of light | **kill** for fibre | Lovisetto et al., Commun. Phys. 7 (2024) |
| N16 | From prethermal to thermal in 2D fluids of light | **kill** | Duval & Cherroret, PRA 107, 043305 (2023) and PRA 111, L021301 (2025) |
| N17 | Mechanism of Raman beam clean-up in GRIN fibre | **park** | Krupa et al., APL Photonics 4, 110901 (2019) |
| N18 | Rigorous derivation of the wave kinetic equation | **kill** | Deng & Hani, Invent. Math. (2023) |
| N19 | Statistical theory of counter-propagating polarization attraction | **park**, upgradeable | Picozzi et al. 2014, §7.5.1 |
| N20 | Kibble–Zurek defect formation at fibre-laser turn-on | does not qualify | — |
| N21 | Statistical theory of Lugiato–Lefever (fibre-ring) turbulence | **park** | — (no citable open statement found) |

Access levels are in the ledger (§6). Below, "full text (me)" means read by claude-interactive.22; otherwise the helper's access is given.

### S1. Self-cleaning rate paradox (→ card -01)

**Criterion 1 holds.**
- **Earliest.** Aschieri et al., PRA 83, 033838 (2011), full text (me): the simulations show "the thermalization process slows down significantly as the number of modes" increases.
- **Against self-cleaning.** Fusaro et al., PRL 122, 123902 (2019), abstract (me): thermalization is "known to require prohibitive large interaction lengths".
- **2023.** Ferraro, Mangini, Zitelli & Wabnitz, Adv. Phys. X 8, 2228018 (2023), full text (me). The mechanism is "still the subject of a hot debate, and it remains highly controversial". The threshold is called something any theory is unlikely to determine.
- **Most recent.** Ferraro et al., Physica D (2025), full text (me). Of the spatial kinetic theory with weak disorder: "it cannot provide a complete description of the experimental results".

**The only claimed resolution is weak-disorder acceleration** (Fusaro 2019; Garnier 2019). Its authors call it non-quantitative; Garnier 2019 says the theory "cannot provide a quantitative description of the experimental results" (full text, me). It predicts $L_{\rm kin}\propto L_{\rm NL}^2$, and the experiments sit at $L_{\rm NL}/L_d\approx0.1$–0.75 (run). Two published two-length data sets point instead to an onset at a fixed number of nonlinear lengths:
- Krupa 2017 SI, like-with-like criteria: $x$ = 1.0–1.16;
- Pourbeyram 2022: $x\le1.02$, onset at $L\approx7L_{\rm NL}$.

Neither excludes $x=1/2$ at its power resolution (helper .22.1). The other mechanisms fail too:
- Podivilov 2019's parametric threshold does not depend on length;
- Zanaglia 2026's spatiotemporal mechanism is untested CW theory;
- Biasi 2024's coherent condensation concerns solvable sub-manifolds.

**Criteria 2–4 hold.**
- **2.** A predictive law would settle the field's main debate.
- **3.** The beat-averaged resonant GRIN model, with profile splitting and intra-group disorder; routes: resonance-broadened kinetics, Lyapunov mixing, anomalous-correlator closure.
- **4.** A cut-back $P_c(L)$ series with controlled disorder; per-shot against phase-averaged data.

**Kill search** (.22.1).
- Forward citations from 2021: Fusaro 2019 (72), Garnier 2019 (27), Podivilov 2019 (70), Krupa 2017 (401, filtered to 58), Biasi–Evnin–Malomed (16 + 11).
- About 10 queries.
- No derived threshold–length law found.

**Verdict.** Shortlist.

### S2. Ideal GRIN as a resonant system (kill as posed)

**What is already published.**
- Biasi, Evnin & Malomed (PRE 2021, 2023; abstracts, .22.1) show FPU recurrences, persistent breathers and an obstruction to ergodicity in the resonant dynamics of the ideal harmonic trap.
- Ferraro 2025 (full text, me) ties these to the freezing of RJ thermalization in GRIN without disorder.
- The registry claim C-20261016-claude-interactive.7-03 already gives the endpoint without disorder: a GGE of $(N,E_{\rm lin},H_{\rm res})$. It notes that ideal GRIN adds $L_z$, the Kohn mode and the breathing mode.
- Biasi, PRE 110, 034107 (2024) (partial full text, .22.1) gives exact coherent condensation in solvable resonant systems, including the radial harmonic-trap GPE.

**What remains** is the rate and the mechanism that restores ergodicity. That is card -01. A complete invariant set of the continuous resonant equation would be mathematics without a distinct fibre test (criterion 4).

**Kill search** (.22.1).
- Forward citations of Biasi–Evnin–Malomed 2021 and 2023; Faou–Germain–Hani; Gérard–Germain–Thomann.
- Queries on the continuous resonant equation, the lowest-Landau-level equation and GRIN.
- Chabert, Comm. PDE (2024), on rigorous dynamics of the perturbed 2D oscillator NLS, is on the PI download list.

**Verdict.** Kill.

### S3. Non-Gibbs breather condensation (→ card -02)

**Criterion 1 holds; all quotes verified by me unless noted.**
- **Earliest.** Rasmussen et al., PRL 84, 3740 (2000): the infinite-temperature line and breathers above it (not accessed).
- **2013.** Iubini et al., NJP 15, 023032 (2013): "Convergence to such equilibrium states, however, has never been observed".
- **2018.** Mithun, Kati, Danieli & Flach, PRL 120, 184101 (2018), abstract (me). There is weakly non-ergodic dynamics inside the non-Gibbs phase. In its ergodic part the Gibbs distribution must be replaced by an unknown modified one. This is the statistical description card -02 targets.
- **2021.** Baldovin et al., Phys. Rep. 923, 1 (2021): "the dynamical origin of the freezing mechanism is not clear at all".
- **2025.** Iubini & Politi, PRL 134, 097102 (2025), helper .22.2: "has challenged statistical mechanics for a long time". They solve open set-ups only, with lifetime $\tau\approx e^{\lambda|T|}$.
- **2026.** Kabat et al., PRL 137, 103803 (2026): an interacting RJ theory for the Gibbs region only. Non-Gibbs work is "currently in progress".

**Claimed resolutions.**
- Equilibrium: Gradenigo et al. 2021.
- Adiabatic invariant: Iubini 2019; proved for a unidirectional model by Politi 2022.
- Stochastic surrogates: Gotti 2021; Giusfredi 2025.

**No optical experiment in the non-Gibbs region.** The optical negative temperatures of Baudin 2023, Marques Muniz 2023 and Kirsch 2025 all come from a bounded band, on the Gibbs side.

**Criteria 2–4 hold.**
- **2.** A first statistical theory of the isolated route, plus a first optical observation.
- **3.** The multi-breather GGE built on the adiabatic invariant.
- **4.** A 7- or 19-core coupled-core fibre with SLM-randomized phases. The launch geometry alone sets the side of the line: $h/a^2=N/k$ for $k$ lit cores. The test is Raman-limited to about 2.5–22 coupling lengths with ns pulses, more with ps pulses (run).

**Kill search** (.22.2).
- Forward citations from 2021: Rasmussen 2000 (70), Iubini 2013 (30), Iubini 2019 (37), Mithun 2018 (37); 107 unique titles.
- Seven queries.
- No kill.

**Verdict.** Shortlist.

### S4. Soliton plus thermal background (kill)

**The equilibrium is settled.**
- **Physics.** Jordan & Josserand, PRE 61, 1527 (2000) (abstract, .22.3), and Rumpf & Newell, PRL 87, 054102 (2001) and Physica D 184, 162 (2003). The 2003 conclusions were read in full by .22.3.
- **Rigorous.** Chatterjee, CPAM 67, 1737 (2014), and Tolomeo & Weber, arXiv:2306.07697 (accepted in CMP per arXiv), give statistical soliton resolution and the Lebowitz–Rose–Speer transition.
- **Integrable case.** Koch, Caux & Bastianello, arXiv:2110.14574: the attractive NLS thermodynamic limit is purely solitonic.

**The fibre version is an adaptation that no source states as open.** It would need a cutoff-free time variable, Raman and, in (2+1)D, collapse. Zitelli's weighted Bose–Einstein fits (Nat. Commun. 15, 1149 (2024)) are phenomenological.

**Kill search** (.22.3).
- Forward citations: Rumpf & Newell (22), Jordan & Josserand (18), Chatterjee (7), Wright 2015 (89), Dyachenko 1992 (104), Picozzi 2014 (109).
- 16 queries.
- What is left: the coarsening rate to one soliton, which belongs with S5.

**Verdict.** Kill.

### S5. Degenerate four-wave resonances in single-mode fibre (→ card -03)

**The degeneracy.** With $\beta_2,\beta_3$ the non-trivial resonances are pairs centred on the zero-dispersion frequency (run). The local invariant $J(\Omega)$ then blocks four-wave thermalization, and the result is anomalous thermalization (Suret 2010; Picozzi 2014 §6.2, full text, me).

**Criterion 1 holds.**
- Picozzi 2014 §6.2.3 (me): the observation of anomalous thermalization "still constitutes an open challenging problem".
- What relaxes $J$ is implicit in the optics literature. The general 1D question is explicit:
  - Onorato et al., Phys. Rep. 1040 (2023): the six-wave kinetic equation is "basically written as a conjecture";
  - Vassilev, CMP 406, 293 (2025): what kinetic theory applies when the four-wave kernel is trivial is an open question.

**Claimed resolutions and near pre-emptions.**
- Barviau 2013: truncated thermalization with $\beta_4$, partial.
- Torres 2026: the vector fibre thermalizes, so a scalar test needs a PM fibre.
- Sutherland & Yim, arXiv:2609.23175 (September 2026): the six-wave coefficient for water-wave Dysthe equations. The closest pre-emption; no kinetics and no fibre model.

**Criteria 2–4.**
- **2.** Medium: the four-wave stage is known.
- **3.** The effective six-wave vertex, and whether it vanishes at first order near the integrable Hirota equation. A 2026 classical framework for weak-integrability-breaking perturbations (Vanovac et al., arXiv:2603.11712, abstract, me; lattice models only) gives a route.
- **4.** The four-wave stage is lab-testable in a PM dispersion-shifted fibre within the Raman budget. The six-wave stage is not, in silica (run).

**Kill search** (.22.3).
- Forward citations: Suret 2010 (11), Michel 2011 (0), Barviau 2013 (6), Suret 2011 (13), Laurie 2012 (37), Lvov & Onorato 2018 (41), Onorato 2015 (80), Picozzi 2014 (109).
- 14 queries.
- No kill.

**Verdict.** Shortlist, medium novelty.

### S6. Self-similar condensation and non-thermal fixed points (park)

- **Background.** The kinetic-condensation collapse is classic: Semikoz & Tkachev; Lacaze et al. 2001; Connaughton et al., PRL 95, 263901 (2005).
- **Not in discrete GRIN.** Ferraro 2025 §2.3.7 (full text, .22.1): spatial discrete GRIN kinetics has no Zakharov-type route and no transient power law.
- **The spatiotemporal law is published.** Zanaglia 2026 predicts $T_{\rm loc}\propto z^{-1/7}$.
- **No observation.** No non-thermal fixed point has been seen in fibre. The non-thermal fixed points of cold atoms (Prüfer, Erne 2018) have no fibre analogue with a measurable exponent and a stated open question.
- **Kill search** (.22.1): forward citations of Sun et al., Nat. Phys. 8, 470 (2012), Connaughton 2005, Chantesana 2019, Prüfer 2018 and Erne 2018; queries. No fibre work.

**Verdict.** Park.

### S7. Nonlinear destruction of Anderson localization (park)

**It is longstanding and named.**
- Fishman, Krivolapov & Soffer, Nonlinearity 25, R53 (2012) (abstract, .22.2): "a highly inconclusive and often contradictory picture".
- Vakulchyk et al. 2019: the question "stands unresolved".
- De Roeck et al. 2024: "numerics may well be unable to capture the long-time behavior".
- Basko 2011 (full text, .22.2) predicts spreading slower than any power law.

**Rigorous results now hold the asymptotics.**
- De Roeck, Huveneers & Prośniak, PRE 109, 044207 (2024) and CMP (2025);
- De Roeck, Giacomin, Hannani & Huveneers, arXiv:2502.02344, for quartic coupling.
- These are for related models. On-site Kerr is not covered: that is a mathematical gap, not a fibre-testable one.

**Criterion 4 fails.** Numerics reach $t=2\times10^{12}$. Vakulchyk et al. 2019 state that experiments reach less than $10^{-4}$ of that horizon. In silica coupled-core fibre the Raman budget allows at most about $25\,C/(\gamma P)$ coupling lengths (run). No fibre experiment can tell $t^{1/3}$ from $e^{(\ln t)^{1/3}}$.

**Kill search** (.22.2).
- Forward citations: Pikovsky–Shepelyansky 2008 (105), Flach 2009 (50), Fishman 2012 (28), Basko 2011 (28), Vakulchyk 2019 (41), Lahini 2008 (269), Vatnik 2017 (42).
- Queries.
- No fibre Kerr-spreading experiment found.

**Verdict.** Park.

### N1. Floquet heating in Kerr fibre-loop lattices (kill)

**The proposal.** I proposed this from the kinematics:
- quasi-energy is conserved only modulo $2\pi$;
- four-wave Umklapp channels are open in the mesh-lattice bands $\cos\theta=\cos\beta\cos Q$ for every $\beta<\pi/2$, including an exactly resonant band-edge quartet;
- their weighted count is 0.40–0.51 of the normal channels at $L$ = 24–60 sites, not converged (run).

**The kill.** Moorcroft, Amo, Copie, Randoux, Suret & Proment, arXiv:2511.08355 (November 2025; full-text passages, .22.2), already show this:
- equipartition at infinite temperature over all bands;
- a prethermal RJ stage;
- a simulation of the lattice of Marques Muniz et al. (Science 2023).

Haldar et al., EPL 144, 63001 (2023), and Pyrialakos et al., PRR 6, 013072 (2024), treat prethermal plateaus. The problem is not longstanding, and its core is published.

**What remains** is a question for the PI: whether the 2023 negative-temperature states were prethermal. The Science supplement is on the download list.

**Verdict.** Kill.

### N2. Chaos border in chaotic multimode fibre (park, borderline kill)

- **The conjecture is withdrawn in effect.** Ermann & Shepelyansky, NJP 15, 123004 (2013), claimed that moderate nonlinearity drives classical lattices to a quantum Gibbs distribution. Frahm & Shepelyansky, PRL 131, 077201 (2023) (full text, .22.2), show that state to be a transient.
- **What remains is a heuristic.** Ermann, Chepelianskii & Shepelyansky, J. Phys. A 59, 055702 (2026), predict RJ condensation in D-shaped fibre above a size-independent chaos border. No experiment exists. A recognized open problem would not be settled by this test.

**Verdict.** Park, borderline kill.

### N3. KPZ in the DNLS (kill as longstanding)

- **The theory.** Kulkarni, Huse & Spohn, PRA 92, 043612 (2015), and Mendl & Spohn (2015): the DNLS has a low-temperature KPZ window that crosses over to diffusion.
- **No open statement.** None restates this as open in 2021–2026.
- **No photonic proposal.** No conservative photonic proposal was found; the KPZ observations are in driven-dissipative polaritons.
- **Testing would be marginal.** A $z=3/2$ against $z=2$ test needs about two decades in time.

**Verdict.** Kill as a longstanding problem.

### N4. Discrete wave turbulence in step-index fibre (park)

**Named open.** Krupa 2019 (APL Photonics) and Ferraro 2025 both note that self-cleaning is not clearly seen in step-index fibre.

**The criterion is standard.**
- Garnier 2019 §VI.1 counts resonances for $M\approx120$: 1376 quasi-resonances (efficiency 4.7) in step-index fibre, against 8,369,504 exact resonances (efficiency 630) in GRIN.
- Ermann et al. (2026) give a chaos border.

**Cleaning has been seen.** Few-mode step-index cleaning has been reported.

**Verdict.** Second tier: park.

### N5. RSB in random and mode-locked fibre lasers (shortlist rank 4, no card)

**The discrepancy.** The intensity-fluctuation overlap distribution $P(q)$ is read as replica-symmetry breaking, that is, as a glass. The same signature appears where no quenched glass exists:
- with disorder averaged out: Tommasi et al. 2016, "a generic feature linked to the random laser threshold";
- with no added disorder: Basak et al. 2016;
- with no random medium: Moura et al., PRL 119, 163902 (2017);
- in a standard mode-locked Yb fibre laser: Alves et al., PRL 132, 093801 (2024);
- with temporal disorder: Chen et al., PRB 113, 184208 (2026).

**Explicit statement.** Sarkar, Bhaktha & Andreasen, Sci. Rep. 10, 2628 (2020) (full text via PMC, .22.4): similar spectral fluctuations "may yield 'false positives' for RSB".

**Foothold.** Closed-form $P(q)$ for non-glassy null models. Helper .22.4's hypothesis, which needs checking: a per-shot common multiplicative factor alone gives peaks at $q=\pm1$. The founding experiments compute $q$ from raw intensities without per-shot normalization, as far as their methods were read.

**Novelty.** High if a null model reproduces the published $P(q)$, low if the experiments already normalize.

**Why no card.**
1. The premise needs a full-text check of the normalization in Ghofraniha 2015, Gomes et al., PRA 94, 011801(R) (2016) (the Er random-fibre-laser paper) and Alves 2024.
2. It is statistical mechanics of light rather than thermalization.

Scoping task created.

### N6. Noise-like pulses (park, second tier)

- **Open statement.** Meng et al., Nat. Commun. 12, 5567 (2021) (abstract, .22.4): "the physics of this regime remains poorly understood".
- **Status.** The mechanisms proposed since Horowitz et al. 1997 are numerical. No analytic statistical theory was found.
- **Risk.** It may be cavity-specific chaos with no universal law.

**Verdict.** Park, second tier.

### N7–N9. Kills on the laser side

- **N7, self-starting of passive mode locking.** Gordon, Gat, Fischer & Kärtner (OE 2006) give a closed-form start-time distribution and claim to resolve "the long standing self starting problem". A slow-gain extension would be modest.
- **N8, photon BEC in an Er/Yb fibre cavity.** No published dispute was found. The 1D sub-linear-dispersion issue is addressed by Weill 2021 and by Liu & Xie 2022.
- **N9, turbulent broadening of Raman and random fibre lasers.** Babin 2007 and Churkin 2015 report agreement with experiment, and no discrepancy statement was found.

**Kill searches** (.22.4): forward citations of the key papers (19–130 citing works each) and queries.

### N10. Laminar–turbulent transition of fibre lasers (park)

- **Open statement.** Turitsyna et al., Nat. Photon. 7, 783 (2013) (abstract): "an open fundamental problem of practical importance".
- **Why park.** A directed-percolation test would adapt Faggian et al., PRL 120, 173901 (2018), who found DP in a delay laser. The absorbing-state assumption is fragile with spontaneous emission present.

**Verdict.** Park.

### N11. FPUT recurrence to thermalization (park, merged into -03)

- **Observed.** Vanderhaegen et al., PRA 106, 033519 (2022), observed an irreversible thermalized state under noise.
- **Onset known.** Wabnitz & Wetzel (2014) give the Floquet onset.
- **Not separate.** The end state is integrable turbulence plus noise. The open part, integrability breaking, is card -03.

**Verdict.** Park, merged into -03.

### N12–N18. Kills

- **N12, Kolmogorov–Zakharov cascades.** A passive fibre has no separated forcing and damping, and the measured multimode fluxes are transient (Baudin et al., EPL 134, 14001 (2021)). The theory of the 2D-NLS flux puzzle is active elsewhere: Skipp, Laurie & Nazarenko 2023; Rosenhaus & Falkovich 2025.
- **N14, Boltzmann against Gibbs entropy at negative temperature.** Buonsante et al. (2017) find Boltzmann thermometry consistent for both signs.
- **N15, Lynden-Bell violent relaxation.** Demonstrated in bulk nonlocal optics (Lovisetto et al. 2024); no fibre route.
- **N16, prethermal to thermal in 2D fluids of light.** Duval & Cherroret (2023, 2025) supply the theory, and the problem overlaps S2.
- **N17, Raman beam clean-up.** Mechanism-level work exists from 2021–2023, so it is parked, not killed.
- **N18, the wave kinetic equation.** Deng & Hani (Invent. Math. 2023) "solves a main conjecture in the theory of wave turbulence".

### N19–N21

- **N19, counter-propagating polarization attraction (park, upgradeable).**
  - Picozzi et al. 2014 §7.5.1 (full text, .22.4) says that no statistical description of partially polarized beams has yet been developed (paraphrase; this review's one quotation from that source is in S5).
  - Fusaro et al., PRA 99, 043826 (2019), report self-polarization at the fibre mid-point, but give no statistical theory.
  - It is fibre-native, with a kinetic foothold for counter-propagating incoherent waves. Novelty is likely medium.
- **N20, Kibble–Zurek at laser turn-on.** Does not qualify: no open statement.
- **N21, Lugiato–Lefever turbulence.** Parked: no citable open statement.

## 2. Shortlist and ranking

1. **P-…22-02, non-Gibbs breather condensation in coupled-core fibre.**
   - **Strongest longstanding record.** The problem dates from 2000. The leading group restates it as open in 2013, 2021 and 2025, and a second group calls it in progress in 2026.
   - **No optical work at all.** The kill search found no optical experiment and no isolated-lattice theory.
   - **Clean first target:** the multi-breather GGE, checkable by a small DNLS code.
   - **Weaknesses.**
     - Competition from two active groups.
     - The fibre test is Raman-limited: a ns test is confined to the formation stage, so ps pulses are needed for more (run).
2. **P-…22-01, threshold–length law of self-cleaning.**
   - **The most fibre-native.** The open statements come from the leading groups (2019, 2023, 2025). The cut-back experiment that would decide it is cheap and has never been done.
   - **Solver-ready** in the coherent regime.
   - **Weaknesses.**
     - The evidence for $x\approx1$ is weak: two lengths per experiment.
     - A cross-family critic can call it P-010 or P-005 in disguise.
     - Zanaglia 2026 may be offered as the resolution once tested.
3. **P-…22-03, relaxation of the frequency-local invariant.**
   - **Clean structure.** An exact factorization and an infinite family of local invariants.
   - **Open in both optics and mathematics:** Picozzi 2014 for the experiment; Onorato 2023 and Vassilev 2025 for the theory.
   - **Medium novelty.**
     - The four-wave stage is known.
     - The six-wave stage is out of reach in silica.
     - Water waves give a near pre-emption.
4. **RSB in fibre lasers** (no card). Potentially high impact, but the premise needs a full-text check of the methods. Scoping task created.

**Why this order.** -02 is ranked above -01 because its novelty case does not depend on how a weak experimental exponent is read. -01 has the better experiment and oracle. If the PI weights testability over novelty, swap them.

## 3. Relation to the registry and the previous round

- **P-005 and P-010.** "See also" lines were added to both, pointing to -01.
  - P-005 says generic kinetic-rate questions are substantially solved. In the experimental regime $L_{\rm NL}/L_d\lesssim1$ this is not supported. I recommend that the PI or a second family revisit that sentence. I did not change the card.
  - P-010 keeps the finite-pulse and walk-off corrections; -01 owns the quasi-CW law. Merging is the PI's call.
- **P-20261016-claude-interactive.7-01 and C-…7-03.** The endpoint without disorder, and the repository's resonant GRIN code. Card -01 builds on both.
- **P-20261020-gpt-f-01** (Raman drift of local equilibrium, low novelty). No overlap. The Raman budget computed here, $\Lambda\lesssim25$ rad, applies there too.
- **C-20261020-claude-interactive.21-01** (time-reversal selection rule). Unrelated.
- **T-20261020-claude-interactive.21-01** (scoping of the coherent femtosecond regime). Card -01 uses the same Pourbeyram data; coordinate before either becomes a claim.
- **No existing card is the right home** for -02 or -03.

## 4. Corrections to the seeds and brief

- **S1.** Baudin et al. 2023 (arXiv:2309.02215) does not say that cleaning is not RJ thermalization. It reports coherent-launch cleaning driven by an incipient RJ thermalization (abstract, .22.1).
- **S2.** The freezing that Fusaro 2019 reports without disorder is explained in the literature by FPU recurrences and the obstruction to ergodicity (Biasi–Evnin–Malomed; Ferraro 2025 §2.2). The Kohn, breathing and $L_z$ invariants are already noted in C-…7-03.
- **Errors in my brief to helper .22.4, corrected by the helper.**
  - Lima et al., PRA 96, 013834 (2017), is about extreme-value statistics, not RSB.
  - Gomes et al., Sci. Rep. 6, 27987 (2016), is a Nd:YBO₃ powder laser; the Er random-fibre-laser glassy paper is PRA 94, 011801(R) (2016).
  - The Pierangeli et al. Nat. Commun. 8, 1501 (2017) DOI ends in -2.
  - Vodonos et al. 2004 concerns pulse-number quanta, not start-time statistics.
- **Deliancourt et al. 2019,** cited in Ferraro 2023 for the length dependence of the threshold, contains no multi-length data (full text, .22.1).

## 5. Search log

My own searches and checks follow. The helpers' complete per-candidate logs, with every query, API call and outcome including failures, are in Appendices A–D.
- **WebSearch (standard):**
  - `multicore fiber coupled cores optical thermalization Rayleigh-Jeans experiment discrete nonlinear Schrödinger`: Shi, Kottos & Shapiro, PRR 3, 033219 (2021) (gap engineering); APS March Meeting 2024 abstract (one nonlinear core). No non-Gibbs work.
  - `Aceves energy localization nonlinear fiber arrays discrete self-focusing collapse Physical Review Letters 1995`: located PRL 75, 73 (1995).
- **WebFetch:**
  - arXiv:2108.05072, abstract;
  - arXiv:2011.05111, abstract (Fusaro 2019 quote verified).
- **Crossref API:**
  - 10.1103/PhysRevE.69.016618;
  - 10.1103/PhysRevLett.84.3740;
  - 10.1103/PhysRevLett.134.097102;
  - 10.1088/1742-5468/abda26;
  - 10.1103/372m-bnpr;
  - a bibliographic query that located Sci. Rep. 9, 9518 (2019) ("Collapse on the line").

  All resolved.
- **arXiv PDFs downloaded:**
  - 2304.12006, Ferraro 2023: threshold, length and debate passages read;
  - 2012.12110, Pourbeyram 2022: Fig. 4 caption and main-text passages read.
- **Helper copies I re-read** (whitespace-normalized text search):
  - Iubini 2013, Baldovin 2021 and Kabat 2026: arXiv HTML;
  - Ferraro 2025, Garnier 2019, Aschieri 2011, Podivilov 2019 and Picozzi 2014 §6.2: text layers.
- **Failure.** An arXiv export API call for 2011.05111 returned nothing; WebFetch was used instead.
- **Second-pass forward citations** (OpenAlex `cites:` filter, sorted by date, titles keyword-scanned; raw lists in the scratchpad `kill_0*_openalex.json`, not committed):
  - **Card -02, from 2022.** Gradenigo J. Stat. Mech. 2021 (28), Gradenigo EPJE 2021 (23), Mithun 2018 (24), Iubini & Politi 2025 (8), Kabat 2026 (0). Abstracts read: PRB 106, L201110 (2022); Fluct. Noise Lett. (2023) (Gotti, Iubini & Politi); PRE (2026) 10.1103/nfym-zysm. No kill.
  - **Card -01, from 2024.** Pourbeyram 2022 (76), Ferraro 2023 (27), Ferraro 2025 (5), Zanaglia 2026 (3), Mangini 2022 (54), Baudin 2023 (9); 107 unique titles. Abstracts read: Kabat et al. PRA 2025; Li, Ruelle, Ryczkowski & Dudley, CLEO/Europe 2025 (new risk: the pump-wavelength field is never clean); Mangini et al. SPIE 2025; Cirimele et al. EPJ Web Conf. 2026; Labaz & Sidorenko OL 2024. No kill.
  - **Card -03, from 2024.** Vassilev 2025 (1), Suret 2010 (8), Barviau 2013 (4), Picozzi 2014 (53), Onorato Phys. Rep. 2023 (26), Banks 2022 (8); 88 unique titles. Only mathematics or chain papers are relevant. No kill.
- **Third pass, recent preprints.** arXiv API, sorted by submission date, entries since 2025-06 kept:
  - `abs:"discrete nonlinear Schrodinger" AND (abs:"negative temperature" OR abs:breather OR abs:"non-Gibbs" OR abs:"non-Gibbsian")`: no entries since 2025-06.
  - `(abs:"multicore fiber" OR abs:"multi-core fiber" OR abs:"coupled-core") AND (abs:thermalization OR abs:"negative temperature" OR abs:breather)`: nothing relevant.
  - `abs:"self-cleaning" AND (abs:multimode OR abs:"graded-index")`: arXiv:2508.14193 (off-axis beam cleaning) and 2606.06862 (FLASH beam-quality measurement). No rate law.
  - `abs:"six-wave" OR abs:"anomalous thermalization" OR (abs:"third-order dispersion" AND abs:thermalization)`: arXiv:2609.23175 (already listed) and arXiv:2603.11712 (classical weak-integrability-breaking framework; abstract read, cited in card -03).
- **Extended WebSearch queries:**
  - `non-Gibbsian regime discrete nonlinear Schrödinger breathers negative temperature isolated lattice relaxation 2026 arXiv`;
  - `beam self-cleaning graded-index fiber threshold scales inverse fiber length nonlinear length kinetic theory test 2026`.
  - Standard: `"anomalous thermalization" incoherent light zero-dispersion fiber local invariant six-wave relaxation`.
  - No kill. The first led to the Iubini & Politi 2025 abstract, which states the finite-size, isolated-system mechanism now written into card -02.
- **WebFetch of abstracts:** arXiv:2406.15140, 1910.07461, 2511.08355, 2609.23175 and 2603.11712.
- **Mithun et al. 2018,** WebSearch (standard) `Mithun Kati Danieli Flach "Weakly nonergodic dynamics in the Gross-Pitaevskii lattice" arXiv abstract non-Gibbs`, then WebFetch of arXiv:1712.03375. This corrected helper .22.2's title-only description: the paper is about the non-Gibbs phase. Its abstract supplies the 2018 open statement used in card -02.

## 6. Source ledger

### 6.1 Load-bearing sources read by claude-interactive.22

| Source | Identifier | Access (me) | Used for |
|---|---|---|---|
| Ferraro, Mangini, Zitelli & Wabnitz, Adv. Phys. X 8, 2228018 (2023) | arXiv:2304.12006; DOI 10.1080/23746149.2023.2228018 | full text (passages: §1, §3, conclusions) | -01 open statements |
| Ferraro, Baudin, Gervaziev, Fusaro, Picozzi, Garnier et al., Physica D 481, 134758 (2025) | arXiv:2505.11299; DOI 10.1016/j.physd.2025.134758 | full text (passages: §1, §2.2, §2.5, §4) | -01, S2, S6 |
| Garnier, Fusaro, Baudin, Michel, Krupa, Millot & Picozzi, PRA 100, 053835 (2019) | arXiv:2011.03918 | full text (conclusion passage) | -01 |
| Fusaro, Garnier, Krupa, Millot & Picozzi, PRL 122, 123902 (2019) | arXiv:2011.05111 | abstract | -01 |
| Aschieri, Garnier, Michel, Doya & Picozzi, PRA 83, 033838 (2011) | DOI 10.1103/PhysRevA.83.033838 | full text (passage; author-hosted PDF) | -01 earliest |
| Pourbeyram et al., Nat. Phys. 18, 685 (2022) | arXiv:2012.12110; DOI 10.1038/s41567-022-01579-y | full text (Fig. 4 caption, main text) | -01 data |
| Podivilov et al., PRL 122, 103902 (2019) | arXiv:1811.10239 | full text (threshold passage) | -01 |
| Krupa et al., Nat. Photon. 11, 237 (2017), Supplementary Information | DOI 10.1038/nphoton.2017.32 | full text of the SI (power × length passage); main text not accessed | -01 data |
| Mithun, Kati, Danieli & Flach, PRL 120, 184101 (2018) | arXiv:1712.03375 | abstract | -02 (2018 open statement) |
| Gradenigo, Iubini, Livi & Majumdar, J. Stat. Mech. (2021) 023201 | arXiv:1910.07461 | abstract | -02 (transition at the line for large N) |
| Iubini & Politi, PRL 134, 097102 (2025) | arXiv:2406.15140 | abstract | -02 (isolated finite systems; open set-ups) |
| Li, Ruelle, Ryczkowski & Dudley, CLEO/Europe (2025) | DOI 10.1109/cleo/europe-eqec65582.2025.11109609 | abstract (OpenAlex) | -01 risk |
| Iubini, Franzosi, Livi, Oppo & Politi, NJP 15, 023032 (2013) | arXiv:1203.4162 | full text (passages) | -02 |
| Baldovin, Iubini, Livi & Vulpiani, Phys. Rep. 923, 1 (2021) | arXiv:2103.12572 | full text (DNLS section) | -02 |
| Kabat, Mohapatra, Kevrekidis & Kottos, PRL 137, 103803 (2026) | arXiv:2602.13161; DOI 10.1103/372m-bnpr | full text (conclusion, model) | -02 |
| Rasmussen et al., PRL 84, 3740 (2000); Rumpf, PRE 69, 016618 (2004); Iubini & Politi, PRL 134, 097102 (2025); Gradenigo et al., J. Stat. Mech. (2021) 023201; Muniz et al., Sci. Rep. 9, 9518 (2019) | DOIs as cited | Crossref record (access as in the helper ledger) | -02 |
| Picozzi, Garnier, Hansson, Suret, Randoux, Millot & Christodoulides, Phys. Rep. 542, 1 (2014) | DOI 10.1016/j.physrep.2014.03.002 | full text (§1.2, §6.2, §6.2.3; author-hosted PDF) | -03 |
| Aceves et al., PRL 75, 73 (1995) | DOI 10.1103/PhysRevLett.75.73 | bibliographic record | -02 context |
| Shi, Kottos & Shapiro, PRR 3, 033219 (2021) | arXiv:2108.05072 | abstract | search log |

### 6.2 Helper ledgers

Appendices A–D reproduce the four helper ledgers verbatim. Each gives the identifier and the helper's access level for every source it located: about 250 sources in all, including every source cited in §1.

## 7. PI download list (paywalled or blocked must-reads, by card)

**Card -01:**
1. Krupa et al., Nat. Photon. 11, 237 (2017), main text, [DOI:10.1038/nphoton.2017.32](https://doi.org/10.1038/nphoton.2017.32). Does Fig. 4 (cut-back) contain threshold-against-length data?
2. Mangini et al., OL 48, 3677 (2023), [DOI:10.1364/OL.494543](https://doi.org/10.1364/OL.494543): modal phase locking, the coherent-regime evidence.
3. Liu, Wright, Christodoulides & Wise, OL 41, 3675 (2016), [DOI:10.1364/OL.41.003675](https://doi.org/10.1364/OL.41.003675): femtosecond thresholds and any length dependence.
4. Leventoux et al., OL 46, 66 (2021), [DOI:10.1364/OL.411868](https://doi.org/10.1364/OL.411868): time-resolved beam maps.
5. Berti et al., PRL 129, 063901 (2022), [DOI:10.1103/PhysRevLett.129.063901](https://doi.org/10.1103/PhysRevLett.129.063901): strong disorder.
6. Deliancourt et al., OE 27, 17311 (2019), [DOI:10.1364/OE.27.017311](https://doi.org/10.1364/OE.27.017311): open access, but Optica served a captcha. Threshold against number of excited modes.
7. Wright, Wu, Christodoulides & Wise, Nat. Phys. 18, 1018 (2022), published version (the accepted manuscript was read).
8. Chao, Fang & Yu, PRA (2025), [DOI:10.1103/k453-gplh](https://doi.org/10.1103/k453-gplh), and Kabat et al., PRA (2025), [DOI:10.1103/xqyx-g3tn](https://doi.org/10.1103/xqyx-g3tn): rate-theory kill checks.

**Card -02:**
9. Marques Muniz et al., Science 379, 1019 (2023) with its Supplementary Materials, [DOI:10.1126/science.ade6523](https://doi.org/10.1126/science.ade6523). Lattice size, round trips, nonlinear phase per step, and whether conservation of a linear internal energy was assumed. This also answers the N1 question.
10. Rasmussen et al., PRL 84, 3740 (2000); Rumpf, PRE 69, 016618 (2004) and PRE 77, 036606 (2008).
11. Gradenigo et al., EPJE 44, 29 (2021); Mithun et al., PRL 120, 184101 (2018) and PRE 104, 014218 (2021).

**Card -03:**
12. Suret, Randoux, Jauslin & Picozzi, PRL 104, 054101 (2010).
13. Michel et al., Lett. Math. Phys. 96, 415 (2011). An open copy at HAL (hal-00696729) was behind a bot challenge.
14. Sutherland & Yim, arXiv:2609.23175 (open; read in full before any claim).

**Rank-4 item (RSB):**
15. Calvanese Strinati et al., "Optical spin glasses", Adv. Opt. Photon. 18, 421 (2026), [DOI:10.1364/aop.574825](https://doi.org/10.1364/aop.574825).
16. Gomes et al., PRA 94, 011801(R) (2016): the Er random-fibre-laser protocol and its normalization.

**General:**
17. Rumpf & Newell, Physica D 483, 134923 (2025) (publisher returned 403).
18. Fishman, Krivolapov & Soffer, Nonlinearity 25, R53 (2012): its list of specific problems.

One task per card's download group was created (§9).

## 8. Runs

[`runs/2026-10-20-claude-interactive.22-resonance-kinematics`](../runs/2026-10-20-claude-interactive.22-resonance-kinematics/). There is no solver, and every number above that is not from a source comes from these files:
- `summary.json`: the four-wave factorizations, mesh-lattice kinematics and ring counts;
- `convergence_beta45.json`: the Umklapp ratio against ring size $L$ and tolerance;
- `raman_budget.json`:
  - $\phi_{\max}$ = 24.6 rad at 1064 nm and 28.1 rad at 1550 nm;
  - coupled-core limits on $CL$;
  - ps walk-off and dispersion lengths;
  - the S5 regime estimates;
- `threshold_exponents.json`: the length exponents and onset in units of $L_{\rm NL}$ from the published data.

## 9. Loose ends (tasks created)

| Task | What |
|---|---|
| T-20261020-claude-interactive.22-01 | PI downloads for card -01 (§7 items 1–8) |
| T-20261020-claude-interactive.22-02 | PI downloads for card -02, including the Marques Muniz 2023 supplement (§7 items 9–11) |
| T-20261020-claude-interactive.22-03 | PI downloads for card -03 and the Sutherland & Yim pre-emption check (§7 items 12–14) |
| T-20261020-claude-interactive.22-04 | Scope a card on RSB signatures in fibre lasers: a null-model test (rank 4, N5) |
| T-20261020-claude-interactive.22-05 | Revisit P-005's statement that kinetic-rate questions are solved; PI decision on who owns the quasi-CW rate law |
| T-20261020-claude-interactive.22-06 | Cheap oracle for -01: the onset exponent in the resonant GRIN model (after the cross-family review) |
| T-20261020-claude-interactive.22-07 | Cheap oracle for -02: DNLS ensembles above the infinite-temperature line (after the cross-family review) |
| T-20261020-claude-interactive.22-08 | Scope the statistical theory of counter-propagating polarization attraction (parked N19) |

The cross-family novelty reviews already exist: T-20261020-claude-interactive-05 and -06.

## Appendix A. Helper claude-interactive.22.1 (GRIN cluster): kill-search logs, source ledger, process notes

Reproduced from the helper's report (scratchpad, 2026-10-20), headings demoted, otherwise unedited. Access levels are the helper's own. Statements here were not all re-checked by claude-interactive.22; those used in the cards were, as marked there. Text quoted in titles or search strings is not a quotation of a source.

##### C1.4 Kill search log (C1)
- OpenAlex forward citations, 2021 onward, titles scanned:
  - Fusaro 2019 PRL: 72 works. Relevant hits: Zanaglia 2026 PRL; Zanaglia 2026 PRA; Torres et al. 2026 PRL (anomalous correlators); Chao 2025 PRA; Kabat 2025 PRA; Biasi & Gérard 2025 CMP; Biasi 2024 PRE; Baudin 2023 Opt. Commun.; Ferraro 2023 Adv. Phys. X; Mangini 2023 OL; Ramos 2023 Commun. Phys.; Zitelli 2024 Nat. Commun.; Ferraro 2025 review.
  - Garnier 2019 PRA: 27 works. No additional rate resolution.
  - Podivilov 2019 PRL: 70 works. Hits: "Extended self-similarity in multimode optical fiber speckles" (PRE 2026; linear speckle, not relevant); "Near-zero temperature beam expansion" (2026); "High-temperature wave thermalization spoils beam self-cleaning" (OL 2023).
  - Krupa 2017 Nat. Photon.: 401 works, keyword-filtered to 58 titles. No rate-law paper. Hits: "Optical Kinetic Theory of Nonlinear Multimode Photonic Networks" (PRL 132, 193802, 2024; transport, not BSC); "Accelerated Beam Self-Cleaning by Raman Soliton Trapping in Tapered MMF" (JLT 2025; abstract not available).
- WebSearch queries:
  - (extended) `beam self-cleaning graded-index fiber thermalization length kinetic theory "orders of magnitude" longer than fiber length`: led to Adv. Phys. X 2023, Garnier 2019 HTML, Baudin 2023, Ferraro 2025. No new resolution.
  - `Kerr beam self-cleaning threshold power versus fiber length scaling measurement ...`: single-length thresholds only.
  - `beam self-cleaning length dependence cutback measurement ...`: no P_c(L) series found.
  - (extended) `beam self-cleaning occurs within a few nonlinear lengths scaling "nonlinear length" kinetic wave turbulence prediction inconsistent coherent mechanism graded-index`: no paper flags the P^-1 versus P^-2 discrepancy. Found the Krupa preprint arXiv:1603.02972.
  - `"Hydrodynamic 2D turbulence ..." arXiv`; `Pourbeyram ... arXiv`; `Liu Wright Christodoulides Wise "Kerr self-cleaning of femtosecond-pulsed beams ..."`: bibliographic only.

##### C2.4 Kill search log (C2)
- OpenAlex forward citations, 2021 onward:
  - Germain–Hani–Thomann CR I: 23 works. Optics-relevant: only Biasi–Evnin–Malomed 2021 and 2023 and Biasi 2024/2025. Maths: Chabert 2024, Faou–Raphaël 2023, LLL papers.
  - Biasi–Bizoń–Evnin CMP 2019: 14 works. No optics BSC hits.
  - Biasi–Bizoń–Craps–Evnin PRE 2018: 13 works. Same.
  - Biasi–Evnin–Malomed 2021: 16 works. Hits: Zanaglia PRA 2024 and PRL 2026; Baudin 2023; Ferraro 2025.
  - Biasi–Evnin–Malomed 2023: 11 works. Same set.
  - Two failed attempts:
    - Faou–Germain–Hani JAMS: I used the wrong DOI (10.1090/jams/838, which returned Tao's averaged Navier-Stokes paper). Discarded; the arXiv abstract was used instead.
    - Gérard–Germain–Thomann LLL: my guessed DOI 10.1007/s00205-018-1295-0 returned 404 and was not scanned. Crossref rate-limited (HTTP 429) the retry.
- WebSearch queries:
  - `Biasi Evnin Malomed "Obstruction to ergodicity ..."`
  - `Biasi Evnin Malomed "Fermi-Pasta-Ulam phenomena ..."`
  - `Germain Hani Thomann "On the continuous resonant equation for NLS: II ..."`
  - (extended) `continuous resonant equation lowest Landau level multimode fiber beam self-cleaning resonant approximation graded-index`: no CR/LLL–BSC paper.
  - `"generalized Gibbs ensemble" graded-index multimode fiber OR "harmonic trap" ...`: only the 1D-NLS GGE.
  - `Pitaevskii-Rosch breathing mode SO(2,1) symmetry graded-index fiber thermalization ...`: nothing on thermalization.
  - `Ermann Vergini Shepelyansky "Dynamical thermalization of Bose-Einstein condensate in Bunimovich stadium"`: located EPL 111, 50009 (2015) via Crossref; not read.

##### C3.4 Kill search log
- OpenAlex forward citations, 2021 onward:
  - Sun et al. Nat. Phys. 2012: 50 works.
  - Connaughton 2005: 52 works.
  - Chantesana 2019: 49 works; all atomic-gas NTFP, none optical-fibre.
  - Semikoz–Tkachev 1995: 40 works.
  - Optics hits: only the Picozzi/Kottos-group fibre papers, Abuzarli 2022, and "Paraxial fluids of light" (review, 2025, not accessed).
- WebSearch queries:
  - (extended) `self-similar condensation dynamics multimode fiber OR "fluid of light" universal scaling exponents kinetic condensation observation 2022 2023 2024 2025`: ESS in linear MMF speckle (PRE 2026; irrelevant), Zitelli LPOR 2024/25, polariton dynamic scaling z ≈ 2 (arXiv:2605.02397; driven-dissipative, not fibre).
  - `"nonthermal fixed point" OR "non-thermal fixed point" optics photon fluid OR multimode fiber OR paraxial light observation`: none in optics.

##### C4.4 Kill search log
- (extended) `discrete wave turbulence step-index multimode fiber thermalization onset nonlinear broadening mode spacing quasi-resonances frozen turbulence optical`: only Garnier 2019 and Ferraro 2025.
- `Kerr beam self-cleaning step-index multimode fiber observation highly multimode step-index nonlinear beam cleanup`: Mohammadzahery 2021 (×2), Dupiol 2018.
- OpenAlex keyword scan of the Krupa 2017 citers: "Spatial Instability of Fundamental Mode in Step-Index MMF" (2025); "Relative intensity noise ... graded-index and step-index MMF" (OL 2025; not relevant).

#### (b) Source ledger

| id | short citation | access |
|---|---|---|
| arXiv:2505.11299; 10.1016/j.physd.2025.134758 | Ferraro et al., Physica D (2025), WT/thermalization/multimode-locking review | full text |
| arXiv:2304.12006; 10.1080/23746149.2023.2228018 | Ferraro, Mangini, Zitelli, Wabnitz, Adv. Phys. X 8 (2023) | full text |
| 10.1063/1.5119434 | Krupa et al., APL Photonics 4, 110901 (2019) (IRIS PDF) | full text |
| 10.1038/s41567-022-01691-z | Wright, Wu, Christodoulides, Wise, Nat. Phys. 18, 1018 (2022) (NSF PAR copy) | full text |
| 10.1016/j.physrep.2014.03.002 | Picozzi et al., Phys. Rep. 542, 1 (2014) (UCF copy) | full text (partial, keyword-level) |
| arXiv:2011.03918; 10.1103/PhysRevA.100.053835 | Garnier et al., PRA 100, 053835 (2019) | full text |
| arXiv:2011.05111; 10.1103/PhysRevLett.122.123902 | Fusaro et al., PRL 122, 123902 (2019) | abstract only |
| 10.1103/PhysRevA.83.033838 | Aschieri et al., PRA 83, 033838 (2011) (author copy) | full text |
| arXiv:2309.02215; 10.1016/j.optcom.2023.129716 | Baudin et al., Opt. Commun. 545, 129716 (2023) | abstract only |
| arXiv:2506.23536; 10.1103/mqzh-w2gh | Zanaglia et al., PRL 136, 053802 (2026) | abstract + partial full text |
| arXiv:2512.07784; 10.1103/bf7m-chkd | Zanaglia et al., PRA (2026), spatiotemporal equilibrium | abstract only |
| arXiv:2405.06531; 10.1103/PhysRevA.110.063530 | Zanaglia et al., PRA 110, 063530 (2024) | abstract only |
| arXiv:2512.17777; 10.1103/tgtw-qnyq | Torres et al., PRL (2026), anomalous correlators | abstract only |
| arXiv:1811.10239; 10.1103/PhysRevLett.122.103902 | Podivilov et al., PRL 122, 103902 (2019) | abstract + full-text keyword scan |
| arXiv:1908.07745; OFT 53, 101994 | Sidelnikov et al. (2019) | abstract only |
| 10.1038/nphoton.2017.32; arXiv:1603.02972 | Krupa et al., Nat. Photon. 11, 237 (2017): preprint and SI | preprint + SI full text; published main text not accessed |
| arXiv:2012.12110; 10.1038/s41567-022-01579-y | Pourbeyram et al., Nat. Phys. 18, 685 (2022) | full text (arXiv) incl. Fig. 4a image |
| arXiv:2111.08063; 10.1364/OE.449187 | Mangini et al., OE 30, 10850 (2022) | full text |
| arXiv:2205.13385; 10.1109/JLT.2023.3239385 | Ferraro et al., JLT (2023), beam-by-beam cleanup | full text |
| 10.1364/OSAC.2.001089 | Deliancourt et al., OSA Continuum 2, 1089 (2019) (IRIS PDF) | full text |
| 10.1364/OL.494543 | Mangini et al., OL 48, 3677 (2023), modal phase locking | not accessed |
| 10.1103/PhysRevLett.129.063901 | Berti et al., PRL 129, 063901 (2022) | not accessed |
| arXiv:2106.03870; 10.1103/PhysRevE.104.034210 | Biasi, Evnin, Malomed, PRE 104, 034210 (2021) | abstract only |
| arXiv:2304.10308; 10.1103/PhysRevE.108.034204 | Biasi, Evnin, Malomed, PRE 108, 034204 (2023) | abstract only |
| arXiv:2401.15083; 10.1103/PhysRevE.110.034107 | Biasi, PRE 110, 034107 (2024) | full text (partial) |
| 10.1007/s00220-025-05449-5 | Biasi & Gérard, CMP (2025) | abstract only |
| arXiv:1308.6267 | Faou, Germain, Hani (JAMS 2016), CR equation | abstract only |
| arXiv:1501.03760 | Germain, Hani, Thomann, CR I | abstract only |
| arXiv:1502.05643 | Germain, Hani, Thomann, CR II, Anal. PDE 8, 1733 (2015) | abstract only |
| arXiv:2104.09797; 10.1088/1361-6382/ac1b46 | Evnin, CQG (2021) resonant-systems review | full text (keyword scan) |
| arXiv:2006.08206; 10.1353/ajm.2023.a907703 | Faou & Raphaël, Amer. J. Math. (2023) | abstract only |
| 10.1080/03605302.2024.2302017 | Chabert, Comm. PDE (2024) | abstract only |
| arXiv:2503.16526; 10.1103/xz2w-hndp | Bastianello et al., GGE in photonics (PRA 2026) | abstract only |
| arXiv:2005.07280; 10.1364/OE.28.024005 | Hansson et al., OE 28, 24005 (2020) | abstract only |
| arXiv:2508.14193 | Sharma et al. (2025), GRIN rods | abstract only |
| arXiv:2206.02024 | Zhang et al. (2022), self-maintaining effect | abstract only |
| 10.1103/PhysRevA.55.R853 | Pitaevskii & Rosch, PRA 55, R853 (1997) | not accessed (Crossref record) |
| arXiv:2506.06534 | Ermann, Chepelianskii, Shepelyansky, J. Phys. A 59, 055702 (2026) | full text (partial) |
| 10.1209/0295-5075/111/50009 | Ermann, Vergini, Shepelyansky, EPL 111, 50009 (2015) | not accessed |
| 10.1103/PhysRevE.82.056322; arXiv:1006.3631 | L'vov & Nazarenko, PRE 82, 056322 (2010) | abstract only |
| 10.1364/OE.420299 | Mohammadzahery et al., OE 29, 10716 (2021) | abstract only |
| 10.1038/s41598-021-03856-x | Mohammadzahery et al., Sci. Rep. (2021) | abstract only |
| arXiv:1801.03649 | Dupiol et al. (2018), microstructured-fibre Kerr cleaning | abstract only |
| arXiv:1810.05878 | Leventoux et al. (2018/2020), anomalous-dispersion BSC | abstract only |
| 10.1038/s42005-023-01309-7 | Ramos et al., Commun. Phys. (2023) | abstract only |
| 10.1103/PhysRevResearch.6.033114 | Kabat et al., PRR 6, 033114 (2024) | abstract only |
| 10.1103/xqyx-g3tn | Kabat et al., PRA (2025) | abstract only |
| 10.1103/PhysRevLett.132.193802 | Kurnosov et al., PRL 132, 193802 (2024) | abstract only |
| 10.1103/k453-gplh | Chao, Fang, Yu, PRA (2025) | abstract only |
| 10.1038/s41467-024-45185-3 | Zitelli, Mangini, Wabnitz, Nat. Commun. (2024) | abstract only |
| arXiv:2305.03924; 10.1103/PhysRevE.108.064207 | Zhu et al., PRE 108, 064207 (2023) | abstract only |
| arXiv:2203.07399; 10.1103/PhysRevLett.129.100602 | Abuzarli et al., PRL 129, 100602 (2022) | abstract only |
| 10.1103/PhysRevLett.74.3093; 10.1103/PhysRevLett.95.263901; 10.1103/PhysRevA.99.043620; 10.1038/nphys2278 | Semikoz–Tkachev 1995; Connaughton 2005; Chantesana 2019; Sun 2012 | not accessed (citation seeds only) |

#### Process notes
- Blocked and not bypassed: opg.optica.org (captcha) for Deliancourt 2019, obtained instead from Sapienza IRIS; hal.science (Anubis bot challenge) for Aschieri 2011, obtained instead from the author's home page; the nature.com main text of Krupa 2017 (paywall). Crossref returned HTTP 429 on two DOI checks (Gérard–Germain–Thomann LLL; Faou–Germain–Hani JAMS), so those DOIs stay unverified and uncited.
- Semantic Scholar was not used; OpenAlex sufficed.
- **Mistake to flag:** my first curl download (arXiv HTML of 2505.11299) put the user's e-mail address in the User-Agent header as a contact string. This goes against the instruction not to send it to third-party services. All later requests used a generic User-Agent.
- Earlier drafts of this file carried wrong clock times in the working notes and an over-strong reading of the Pourbeyram and Krupa length data (P_c ∝ L^-1). Both are corrected above. The Fig. 4a reading shows that the data do not exclude L^-1/2.

## Appendix B. Helper claude-interactive.22.2 (lattice cluster): kill-search logs and source ledger

Reproduced from the helper's report (scratchpad, 2026-10-20), headings demoted, otherwise unedited. Access levels are the helper's own. Statements here were not all re-checked by claude-interactive.22; those used in the cards were, as marked there. Text quoted in titles or search strings is not a quotation of a source.

###### Kill search for L1. Negative-temperature (non-Gibbs) localization in the DNLS: breather condensation
- OpenAlex forward citations from 2021 on (API `works?filter=cites:<id>,from_publication_date:2021-01-01`). Rasmussen 2000 (W2081887888): 70 citing works. Iubini 2013 NJP (W2112563959): 30. Iubini 2019 PRL (W2901250678): 37. Mithun 2018 PRL (W2796312398): 37. Union: 107 unique titles scanned. Relevant hits are all listed in item 3, plus the 2023 MMF negative-T Rayleigh-Jeans experiment (Baudin et al., PRL 130, 063801, doi:10.1103/physrevlett.130.063801, `not accessed`). None reports an optical experiment in the non-Gibbs (breather) region. None gives a complete theory of isolated-system breather coarsening. An early parallel batch got HTTP 429 from OpenAlex; it was rerun sequentially and succeeded.
- WebSearch (standard): "discrete nonlinear Schrödinger negative temperature breather condensation relaxation time open problem 2024" found Iubini-Politi 2024/25 and a JETC 2025 talk abstract (PDF not parseable, `not accessed`).
- WebSearch (standard): "Gradenigo Iubini Livi Majumdar localization transition ... negative temperatures" found the 2021 J. Stat. Mech. paper and the 2025 "classical entanglement" paper.
- WebSearch (extended): "experimental observation non-Gibbsian negative temperature discrete breathers photonic waveguide array OR fiber loop OR multicore fiber" found no non-Gibbs optical experiment. Hits were the Gibbs negative-T experiments and an integrable NLS breather-gas fibre-loop experiment (PubMed 41236975, not DNLS).
- WebSearch (standard): "\"non-Gibbs\" OR \"beyond the infinite temperature line\" discrete nonlinear Schrödinger optical experiment 2025" found only theory (Cherny, Engl & Flach, PRA 99, 023603 (2019), arXiv:1809.05371, `not accessed`; Johansson & Rasmussen, PRE 70, 066610 (2004), arXiv:cond-mat/0410126, `not accessed`).
- WebSearch (standard): "multicore fiber discrete nonlinear Schrödinger thermalization negative temperature localization experiment coupled-core 2024 2025" found nothing in the non-Gibbs region.
- WebSearch (standard): "Marques Muniz Peschel fiber loop synthetic lattice negative optical temperature ..." found only the Jena press release (`full text`, no parameters given).
- arXiv API (sorted by date): `abs:"negative temperature" AND (abs:"discrete nonlinear Schrödinger" OR abs:DNLS OR abs:breather OR abs:breathers)` returned 9 hits; new ones were Giusfredi et al. 2025/26 and Iubini et al. 2013/14 coarsening. Query `abs:"negative temperature" AND (abs:multicore OR abs:"coupled-core" OR abs:"waveguide array(s)")` returned 1 hit (Lian et al., arXiv:2307.16529, Wiedemann-Franz in waveguide arrays, not relevant). No optical non-Gibbs work found.
- arXiv API (newest first): `abs:"non-Gibbs" OR abs:"non-Gibbsian" OR abs:"infinite temperature line"` returned 30; the only new relevant hit was Kati, Maluckov & Mančić, arXiv:2601.13472, the preprint of the PRE 2026 paper above. `(abs:"Gross-Pitaevskii lattice" OR abs:"Bose-Hubbard") AND abs:"negative temperature" AND abs:breather` returned 0.
- OpenAlex forward citations of Iubini & Politi PRL 2025 (W4408150498, 8), Gradenigo et al. 2021 (W3126816421, 38), Politi et al. 2022 (W4221149523, 5) and Baldovin et al. 2021 (W3138676234, 59); 54 titles new relative to the first set were scanned. New relevant items: Giusfredi et al. 2026 mean-field (above); Baldovin, Gradenigo, Vulpiani & Zanghì, "On the foundations of statistical mechanics", Phys. Rep. (2025), doi:10.1016/j.physrep.2025.05.003, `not accessed`. No optical non-Gibbs experiment, and no Hamiltonian coarsening law.
- WebSearch (standard): "breather coarsening Hamiltonian discrete nonlinear Schrödinger negative temperature logarithmic numerical 2024 2025 2026" found only the 2012-2014 Iubini et al. papers and Ebrahimi et al. (stochastic DNLS).
- WebSearch (standard): "Rumpf entropy localization fiber array OR waveguide array breather 'two conserved quantities' ..." found Rumpf 2004 (no optical-test proposal visible in the abstract).
- Ramos, Kottos & Shapiro, PRX 10, 031024 (2020) (arXiv:1912.10569), `full text` (ar5iv). They explicitly exclude the region: "we do not address the “non-Gibbsian” region".
- WebFetch: arXiv:2409.01422 (Vardi, Ramos & Kottos, "Non-conventional thermal states of interacting bosonic oligomers", `abstract only`). This is microcanonical, non-RJ occupancies in few-mode systems, framed with fibres as motivation. It is a near neighbour of the finite-size optical version and is theory only.
- WebFetch: arXiv:2511.12080 (Kirsch, ..., Szameit, Heinrich & Christodoulides, "Observation of Joule-Thomson photon-gas expansion", `abstract only`): coupled multicore waveguide arrangement, Gibbs regime.
- WebFetch: arXiv:2505.21163 (Ferraro et al., "Negative absolute temperature attractor in a dense photon gas", `abstract only`): step-index MMF below cutoff with a Kerr-driven population inversion. This is a continuous MMF, not a lattice beyond the T=∞ line.

###### Kill search for L2. Nonlinear destruction of Anderson localization: does subdiffusive spreading continue forever?
- OpenAlex forward citations from 2021 on: Pikovsky-Shepelyansky 2008 (W2040358363) 105, Flach et al. 2009 (W2011721894) 50, Fishman et al. 2012 (W2065849454) 28, Basko 2011 (W1982432073) 28; union 146 unique titles scanned. A second batch covered Vakulchyk 2019 (W2808611306, 41), De Roeck 2024 (W4394727739, 2), Lahini 2008 (W1970514171, 269) and Vatnik 2017 (W2645086993, 42, after the DOI was corrected via Crossref to 10.1038/s41598-017-04059-z; the first DOI tried gave 404). About 300 further titles were scanned, mostly by keyword filter. Relevant hits are listed in items 2, 3 and 5.
- arXiv API id_list query for 2502.02344, 1806.06345, 2109.14347 and 2506.06534 returned abstracts and journal refs.
- WebSearch (extended): "experiment nonlinear disordered synthetic photonic lattice fiber loops spreading subdiffusion Kerr Anderson localization destruction" found only linear fibre-loop Anderson localization (Vatnik 2017; Pankov et al., Opt. Express 27, 4424 (2019), doi:10.1364/OE.27.004424, `abstract only`, numerics on random coupling) and an unattributed snippet "$z^{\alpha}$, $0.3<\alpha<0.4$" (source not identified, not used).
- WebSearch (extended): "nonlinear disordered lattice wave packet subdiffusion 'ad infinitum' OR 'slow down' OR 'eventually stops' ... 2023 2024 2025" found De Roeck et al. 2025 (arXiv:2502.02344).
- WebSearch (standard): "'destruction of Anderson localization' nonlinearity open problem review 2024 OR 2025 OR 2026 ..." found the Milovanov 2024 INI talk and arXiv:1703.04011 (Mafi, interplay overview, `abstract only`).

###### Kill search for L3. Floquet (discrete-time) thermalization in Kerr fibre-loop synthetic lattices
- arXiv API: `ti:"negative optical temperature"` found no arXiv version of Marques Muniz et al. 2023.
- arXiv API: `abs:"quantum walk" AND abs:nonlinear AND abs:thermalization` found Di Molfetta et al. 2015.
- arXiv API: `(abs:"mesh lattice" OR abs:"fiber loop" OR abs:"synthetic photonic lattice") AND (abs:thermalization OR abs:thermodynamic OR abs:"Rayleigh-Jeans")` found Dinani et al., "Universal routing of light via optical thermodynamics", Nature Photonics (2025) (arXiv:2511.13968, `abstract only`): a near-zero-temperature condensation experiment in nonlinear time-synthetic mesh lattices, analysed with RJ thermodynamics.
- arXiv API: `Floquet AND nonlinear AND (photonic OR optical) AND (heating OR thermalization OR prethermal)` found **Moorcroft et al. 2025** and Haldar et al.
- OpenAlex forward-citation sets for L1 and L2 (above) supplied Haldar 2023, Malishava-Flach 2022 and Zhang et al. 2025.
- Related fibre-loop theory: Price, Wimmer, Monika, Peschel & Carusotto, PRA 108, 063517 (2023) (arXiv:2206.10956), `abstract only`, hydrodynamics in optical mesh lattices.

###### Kill search for L4. Thermalization threshold (Chirikov / KAM "chaos border") for nonlinear systems with random-matrix linear modes; Shepelyansky's dynamical-thermalization conjecture
- OpenAlex forward citations from 2021 on: Shepelyansky 1993 (W2092542031) 40, Mulansky 2011 (W2073252874) 18, Ermann 2013 (W2119631875) 4; union 55 scanned. Also Frahm-Shepelyansky 2023 (W4317931482): 10 scanned. Hits: Frahm-Shepelyansky 2023 and 2024; Zanaglia et al., PRA 110, 063530 (2024) (RJ to BE bridging, `abstract only`); Lando-Flach 2023; Haldar 2023; the kicked-gas experiments.
- WebSearch (standard): "D-shaped multimode fiber Kerr nonlinearity thermalization Rayleigh-Jeans experiment chaotic fiber 2025 2026" found only the Ermann et al. theory and standard GRIN experiments. **No D-shaped / chaotic-fibre nonlinear thermalization experiment found.**
- arXiv API title search to locate arXiv:2212.11955.

###### Kill search for L5. KPZ / anomalous hydrodynamic fluctuations in the DNLS
- OpenAlex forward citations from 2021 on: KHS 2015 (W1513427699) 23, Mendl-Spohn 2015 (W1900510469) 16; union 33 scanned. No photonic test or proposal.
- WebSearch (extended): "Kardar-Parisi-Zhang scaling discrete nonlinear Schrödinger photonic waveguide array OR fiber loop OR 'fluid of light' proposal observation conservative" found only driven-dissipative polariton KPZ: Fontaine et al., Nature 608, 687 (2022), `not accessed`; Science 2D KPZ in polaritons (doi:10.1126/science.aeb4154, year not checked, `not accessed`); arXiv:2506.10187 and arXiv:2604.15095 (`not accessed`).
- arXiv API: `abs:"Kardar-Parisi-Zhang" AND (NLS OR GP)` (60 results) found only polariton/dissipative work and KHS 2015. `abs:"Kardar-Parisi-Zhang" AND (photonic OR "optical fiber" OR waveguide OR "fiber loop")` found Yzewyn & Wouters, arXiv:2608.17602 (Aug 2026, "KPZ scaling in one-dimensional arrays of photon condensates", driven-dissipative, `not accessed`).
- **No conservative-photonic (waveguide array, multicore or fibre-loop) KPZ proposal or test was found.**

#### (b) Source ledger (id; short citation; access)

**L1**
- 10.1103/PhysRevLett.84.3740; Rasmussen et al. PRL 2000; not accessed
- 10.1103/PhysRevE.69.016618; Rumpf PRE 2004; abstract only
- 10.1103/PhysRevE.77.036606; Rumpf PRE 2008; abstract only
- 10.1088/1367-2630/15/2/023032 (arXiv:1203.4162); Iubini et al. NJP 2013; full text (ar5iv)
- 10.1007/s10955-013-0896-4 (arXiv:1308.4870); Iubini, Politi & Politi J. Stat. Phys. 2014; abstract only
- 10.1103/PhysRevLett.122.084102 (arXiv:1811.05798); Iubini et al. PRL 2019; abstract only
- 10.1103/PhysRevLett.120.184101; Mithun et al. PRL 2018; not accessed
- 10.1103/physreve.104.014218; Mithun et al. PRE 2021; not accessed
- 10.1016/j.physrep.2021.03.007 (arXiv:2103.12572); Baldovin et al. Phys. Rep. 2021; full text (DNLS section and perspectives)
- 10.1088/1742-5468/abda26 (arXiv:1910.07461); Gradenigo et al. J. Stat. Mech. 2021; abstract only
- 10.1140/epje/s10189-021-00046-5 (arXiv:2106.03698); Gradenigo et al. EPJE 2021; abstract only
- 10.1103/physreve.103.052133; Gotti, Iubini & Politi PRE 2021; abstract only
- 10.1007/s10955-021-02870-7; Arezzo et al. J. Stat. Phys. 2022; not accessed
- 10.1088/1742-5468/ac650e; Politi, Politi & Iubini J. Stat. Mech. 2022; abstract only
- 10.1103/physreve.105.014206; Onorato et al. PRE 2022; abstract only
- 10.1103/physrevlett.134.097102 (arXiv:2406.15140); Iubini & Politi PRL 2025; full text (intro and conclusions)
- 10.1088/1742-5468/add1cd; Giusfredi et al. J. Stat. Mech. 2025; abstract only
- 10.1088/1742-5468/ae625e (arXiv:2511.09206); Giusfredi et al. J. Stat. Mech. 2026; abstract only
- 10.1088/1742-5468/ae17ab; Giachello et al. J. Stat. Mech. 2025; abstract only
- 10.1016/j.physd.2025.134551; Archilla, Bajārs & Flach Physica D 2025; abstract only
- 10.1016/j.physd.2025.134905 and 10.1088/1402-4896/ae54df; Ebrahimi, Drossel & Just 2025/2026; abstract only
- 10.1103/nfym-zysm; Maluckov, Mančić, Kevrekidis et al. PRE 2026; abstract only
- 10.1103/372m-bnpr (arXiv:2602.13161); Kabat et al. PRL 137, 103803 (2026); full text (conclusion)
- 10.1103/physrevresearch.6.043282 (arXiv:2409.01422); Vardi, Ramos & Kottos PRR 2024; abstract only
- arXiv:1912.10569; Ramos, Kottos & Shapiro PRX 10, 031024 (2020); full text (passages)
- 10.1126/science.ade6523; Marques Muniz et al. Science 2023; abstract only (publisher page 403; abstract via OpenAlex)
- 10.1103/physrevlett.130.063801 (arXiv:2301.02796); Baudin et al. PRL 2023; not accessed
- arXiv:2511.12080; Kirsch et al. 2025 (Joule-Thomson, multicore waveguides); abstract only
- arXiv:2505.21163; Ferraro et al. 2025; abstract only
- arXiv:1809.05371; Cherny, Engl & Flach PRA 2019; not accessed
- arXiv:cond-mat/0410126; Johansson & Rasmussen PRE 2004; not accessed
- uni-jena.de press release 2023-03-10 ("Hotter than infinity"); full text

**L2**
- 10.1103/PhysRevLett.100.094101; Pikovsky & Shepelyansky PRL 2008; not accessed
- 10.1103/PhysRevLett.102.024101; Flach, Krimer & Skokos PRL 2009; not accessed
- 10.1209/0295-5075/91/50001; Johansson, Kopidakis & Aubry EPL 2010; abstract only
- 10.1016/j.aop.2011.02.004 (arXiv:1005.5033); Basko Ann. Phys. 2011; full text (sec. 3)
- 10.1088/0951-7715/25/4/R53; Fishman, Krivolapov & Soffer Nonlinearity 2012; abstract only
- 10.1088/0951-7715/26/3/837; Huveneers Nonlinearity 2013; abstract only
- arXiv:1407.1441; Laptyeva, Ivanchenko & Flach J. Phys. A 47, 493001 (2014); full text (secs. 2.7, 3, 4 via ar5iv)
- 10.1103/PhysRevLett.122.040501 (arXiv:1806.06345); Vakulchyk, Fistul & Flach PRL 2019; abstract only
- 10.1103/physreve.109.044207 (arXiv:2308.10572); De Roeck, Huveneers & Prośniak PRE 2024; abstract only
- 10.1007/s00220-025-05336-z (arXiv:2308.11243); De Roeck, Huveneers & Prośniak CMP 2025; abstract only
- arXiv:2502.02344; De Roeck, Giacomin, Hannani & Huveneers 2025; abstract only
- 10.1007/s10955-020-02677-y; Cong, Shi & Zhang J. Stat. Phys. 2021; not accessed
- 10.1016/j.jde.2024.12.021; Cong, Shi & Wang JDE; not accessed
- 10.1209/0295-5075/acc19c; Milovanov & Iomin EPL 2023; abstract only
- 10.1103/svxt-wsk7; Milovanov & Iomin PRE 2025; abstract only
- talks.cam.ac.uk/talk/index/219763; Milovanov INI talk 2024; abstract only
- 10.1103/physreva.105.l020202; Mallick & Flach PRA 2022; abstract only
- 10.1103/physreve.111.024122; Lin et al. PRE 2025; abstract only
- 10.1038/s41467-024-49575-5; Ricard, Novkoski & Falcon Nat. Commun. 2024; abstract only
- 10.1103/PhysRevLett.106.230403; Lucioni et al. PRL 2011; abstract only
- 10.1038/s41567-022-01724-7 and 10.1038/s41567-022-01721-w; kicked-gas Nat. Phys. 2022; not accessed
- 10.1103/dyxq-qkmd; Olsen et al. PRL 2025; abstract only
- 10.1038/s41598-017-04059-z; Vatnik et al. Sci. Rep. 2017; abstract only
- 10.1364/OE.27.004424; Pankov et al. Opt. Express 2019; abstract only
- 10.1016/j.chaos.2025.117804; Wen et al. CSF 2025; not accessed
- 10.1016/j.chaos.2024.114511; Cao et al. CSF 2024; not accessed
- 10.1103/PhysRevLett.112.193902; Leonetti et al. PRL 2014; abstract only
- 10.1103/PhysRevLett.100.013906; Lahini et al. PRL 2008; not accessed
- 10.3389/fphy.2021.736774; Mafi & Ballato Front. Phys. 2021; full text (sec. 4.2)
- arXiv:1505.01109; Mafi AOP 2015; full text (sec. 14 opening and conclusion)
- arXiv:1703.04011; Mafi 2017 overview; abstract only

**L3**
- arXiv:2511.08355; Moorcroft et al. 2025; full text (main passages)
- 10.1209/0295-5075/ad1415 (arXiv:2109.14347); Haldar et al. EPL 2023; abstract only
- 10.1103/physrevresearch.6.013072; Pyrialakos et al. PRR 2024; abstract only
- arXiv:1506.04323; Di Molfetta, Debbasch & Brachet PRE 92, 042923 (2015); abstract only
- 10.1063/5.0092032; Malishava & Flach Chaos 2022; abstract only
- 10.1063/10.0036801; Zhang, Lando, Dietz & Flach LTP 2025; abstract only
- arXiv:1802.04910; Howell et al. PRL 122, 010602 (2019); not accessed
- arXiv:2511.13968; Dinani et al. Nat. Photon. 2025; abstract only
- arXiv:2206.10956; Price et al. PRA 108, 063517 (2023); abstract only
- arXiv:1905.03098; Muniz et al. "Collapse on the line"; abstract only

**L4**
- 10.1103/PhysRevLett.70.1787; Shepelyansky PRL 1993; abstract only
- arXiv:1103.2634; Mulansky et al. J. Stat. Phys. 2011; abstract only
- 10.1088/1367-2630/15/12/123004; Ermann & Shepelyansky NJP 2013; abstract only
- 10.1103/physrevlett.131.077201 (arXiv:2212.11955); Frahm & Shepelyansky PRL 2023; full text (passages and Supplementary scaling)
- 10.1103/physreve.109.044201; Frahm & Shepelyansky PRE 2024; abstract only
- 10.1088/1751-8121/ae3ebe (arXiv:2506.06534); Ermann, Chepelianskii & Shepelyansky J. Phys. A 2026; full text (passages)
- 10.1103/physreve.108.l062301; Lando & Flach PRE 2023; abstract only
- 10.1103/physreva.110.063530; Zanaglia et al. PRA 2024; abstract only
- 10.1103/xqyx-g3tn; Kabat et al. PRA 2025; abstract only
- 10.1038/s42005-023-01309-7; Ramos et al. Commun. Phys. 2023; abstract only

**L5**
- 10.1103/PhysRevA.92.043612 (arXiv:1502.06661); Kulkarni, Huse & Spohn PRA 2015; abstract only
- 10.1088/1742-5468/2015/08/P08028; Mendl & Spohn 2015; abstract only
- 10.1103/physreve.104.044136; Chatterjee, Kulkarni & Kundu PRE 2021; abstract only
- 10.1103/2z9s-5d7w; Minami, Nakano & Saito PRL 2026; abstract only
- 10.1103/physrevlett.127.010601; Saito et al. PRL 2021; abstract only
- arXiv:2608.17602; Yzewyn & Wouters 2026; not accessed (title only)
- Fontaine et al. Nature 608, 687 (2022); not accessed

**General**
- arXiv:2305.18215; Onorato et al. Phys. Rep. 1040 (2023); full text (conclusions)
- 10.1038/s41567-022-01691-z; Wright et al. Nat. Phys. 2022; full text (keyword search of the NSF PAR manuscript)
- arXiv:1912.08270; Wu, Hassan & Christodoulides Nat. Photon. 2019; abstract only
- 10.1103/bf7m-chkd; Zanaglia et al. PRA 2026; abstract only

---

## Appendix C. Helper claude-interactive.22.3 (single-mode fibre and coherent structures): forward-citation sets, query log, source ledger

Reproduced from the helper's report (scratchpad, 2026-10-20), headings demoted, otherwise unedited. Access levels are the helper's own. Statements here were not all re-checked by claude-interactive.22; those used in the cards were, as marked there. Text quoted in titles or search strings is not a quotation of a source.

#### 0. Forward-citation sets scanned (OpenAlex, filter `cites:<id>,from_publication_date:2021-01-01`, run 16:16 EDT)

All 18 DOIs resolved on OpenAlex. Counts are 2021–2026 citing works found by OpenAlex (title lists scanned by eye, then keyword-filtered):

| key paper | OpenAlex id | total cites | 2021+ citing works scanned |
|---|---|---|---|
| Rumpf & Newell PRL 87, 054102 (2001), 10.1103/PhysRevLett.87.054102 | W2003799308 | 85 | 22 |
| Jordan & Josserand PRE 61, 1527 (2000), 10.1103/PhysRevE.61.1527 | W1987202682 | 73 | 18 |
| Chatterjee CPAM 67, 1737 (2014), 10.1002/cpa.21501 | W1964424348 | 20 | 7 |
| Suret et al. PRL 104, 054101 (2010), 10.1103/PhysRevLett.104.054101 | W2031596706 | 54 | 11 |
| Laurie et al. Phys. Rep. 514, 121 (2012), 10.1016/j.physrep.2012.01.004 | W1995845519 | 93 | 37 |
| Lvov & Onorato PRL 120, 144301 (2018), 10.1103/PhysRevLett.120.144301 | W2788030188 | 67 | 41 |
| Onorato et al. PNAS 112, 4208 (2015), 10.1073/pnas.1404397112 | W1613019513 | 150 | 80 |
| Picozzi et al. Phys. Rep. 542, 1 (2014), 10.1016/j.physrep.2014.03.002 | W2002085713 | 274 | 109 |
| Dyachenko et al. Physica D 57, 96 (1992), 10.1016/0167-2789(92)90090-A | W2071040200 | 445 | 104 |
| Van Simaeys et al. PRL 87, 033902 (2001), 10.1103/PhysRevLett.87.033902 | W2079967947 | 242 | 85 |
| Mussot et al. Nat. Photon. 12, 303 (2018), 10.1038/s41566-018-0136-1 | W2794915805 | 184 | 128 |
| Pierangeli et al. PRX 8, 041017 (2018), 10.1103/PhysRevX.8.041017 | W2898820416 | 120 | 94 |
| Agafontsev & Zakharov Nonlinearity 28, 2791 (2015), 10.1088/0951-7715/28/8/2791 | W1700452290 | 159 | 74 |
| Walczak et al. PRL 114, 143903 (2015), 10.1103/PhysRevLett.114.143903 | W2293614511 | 206 | (not yet scanned) |
| Zakharov Stud. Appl. Math. 122, 219 (2009), 10.1111/j.1467-9590.2009.00430.x | W2080649718 | 182 | 88 |
| Copie, Randoux & Suret Rev. Phys. 5, 100037 (2020), 10.1016/j.revip.2019.100037 | W2996512020 | 112 | 103 |
| Gelash et al. PRL 123, 234102 (2019), 10.1103/PhysRevLett.123.234102 | W2986995537 | 112 | (not yet scanned) |
| Wright et al. OE 23, 3492 (2015), 10.1364/OE.23.003492 | W2009422710 | 201 | 89 |

Relevant 2021–2026 hits from these sets (abstracts read via OpenAlex abstract field unless noted):
- Chen & Rumpf, PRE 104, 034213 (2021), 10.1103/PhysRevE.104.034213 "Growth or decay of a coherent structure interacting with random waves" (abstract only). Two-subsystem thermodynamic model: soliton grows if its frequency exceeds the chemical potential of Rayleigh–Jeans waves, decays otherwise. Nonintegrable, noncollapsing NLS; not fibre-specific; no soliton-fraction formula from (N, H) in the abstract.
- Colléaux, Skipp, Nazarenko & Laurie, Physica D (2025) 134687, 10.1016/j.physd.2025.134687 "A bound state attractor in optical turbulence" (abstract only). Numerical; nonlocal NLS (Schrödinger–Helmholtz); final state is an oscillating two-soliton bound state in weak waves, "more typical statistical attractor than the single-soliton attractor". No equilibrium theory for soliton fraction.
- Biasi, PRE 110, 034107 (2024), 10.1103/PhysRevE.110.034107; Biasi & Gérard, CMP (2025), 10.1007/s00220-025-05449-5 (abstracts only). Exact coherent condensation/cascade solutions in solvable resonant Hamiltonian systems. Deterministic, not thermal-equilibrium soliton fraction; not fibre.
- Banks, Buckmaster, Korotkevich, Kovačič & Shatah, PRL 129, 034101 (2022), 10.1103/PhysRevLett.129.034101, arXiv:2109.02477 (abstract only). Six-wave kinetic equation verified for quintic NLS in finite boxes. Not the cubic-NLS-with-weak-integrability-breaking problem.
- Torres, Garnier, Zanaglia, Ferraro, Michel, Doya, Fatome, Kibler, Wabnitz, Picozzi & Millot, PRL (2026), 10.1103/tgtw-qnyq, arXiv:2512.17777 "Irreversible thermalization vs reversible dynamics mediated by anomalous correlators" (abstract only; full author list from the arXiv API). Two coherently coupled NLS (polarization in fibre); kinetic equation describes slow irreversible thermalization in one regime; fast reversible anomalous-correlator dynamics in another.
- Vanderhaegen, Szriftgiser, Kudlinski, Conforti, Armaroli & Mussot, PRA 106, 033519 (2022), 10.1103/PhysRevA.106.033519 (abstract only). Experimental observation of noise-driven thermalization of FPUT recurrences with loss compensation; up to 4 recurrences at low noise; irreversible "thermalized state" at high noise. Experimental; abstract gives no theory of the thermalization length.
- Ferraro, Baudin, Gervaziev, Fusaro, Picozzi, Garnier, Millot, Kharenko et al., Physica D (2025) 134758, 10.1016/j.physd.2025.134758 "Wave turbulence, thermalization and multimode locking in optical fibers" (not accessed yet; OpenAlex has no abstract).
- Laurie, Warwick PhD thesis (2010, re-indexed 2026), WRAP 34564 "Six-wave systems in one-dimensional wave turbulence" (abstract only): 1D optical WT is a six-wave process; inverse cascade forms solitons; "wave turbulence life cycle" for soliton–wave coexistence.

### QUERY LOG (all WebSearch calls; mode in brackets; outcome)
---------------------------------------------------------------------
D1
- Q-D1-2 [standard] "soliton resolution conjecture nonintegrable focusing nonlinear Schrödinger equation progress 2023 2024 2025 arXiv": found Kim & Kwon 2408.12843 (integrable CM-DNLS) and Berthoumieu 2603.29906. No resolution for nonintegrable focusing NLS.
- Q-D1-3 [standard] "multimode fiber solitons thermalization statistical mechanics soliton condensation anomalous dispersion graded-index equilibrium theory 2023 2024 2025": found Zitelli NC 2024, Zitelli LPR 2024 preprint, Ferraro 2025. No kill.
- Q-D1-4 [standard] "Tolomeo Weber phase transition invariant measures focusing Schrödinger equation soliton concentration arXiv": found 2306.07697, 2212.00276.
- Q-D1-5 [standard] "Zitelli soliton condensation multimode fiber thermodynamic weighted Bose-Einstein Nature Communications 2024 statistics of modal condensation": confirmed metadata.
- Q-D1-6 [standard] "Picozzi Rica condensation classical optical waves focusing regime soliton "Rayleigh-Jeans" coherent structure entropy": found RJ condensation papers only.
- Q-D1-7 [standard] "infinite volume limit Gibbs measure one-dimensional focusing mass-subcritical nonlinear Schrödinger concentrates single soliton Gaussian background": found Seong–Sosoe 2411.07840 and the Princeton seminar page.
- Q-D1-8 [standard] ""soliton resolution" Gibbs measure focusing nonlinear Schrödinger critical scaling infinite volume Seong Sosoe 2025 arXiv": snippet attributes the work to Forlano–Tolomeo (unverified). No arXiv id.
- Q-D1-9 [standard] ""statistical analogue of soliton resolution" focusing Schrödinger arXiv": no arXiv id found.
- Q-D1-10 [standard] "Rumpf Newell "The competition between wave turbulence and coherent structures" Physica D 2025": Arizona experts-page snippet (MMT, forced–damped).
- Q-D1-11 [standard] "Wright Wu Christodoulides Wise "Physics of highly multimode nonlinear optical systems" Nature Physics 2022 open questions thermalization solitons": no explicit open statement found. The open copy downloaded was the Optica 2022 review instead.
- Q-D1-12 [standard] "multimode soliton thermalization entropy maximization coherent structure plus thermal background graded-index fiber anomalous dispersion theory ...": entropy-maximization experiments (HAL hal-04649357, not opened). No kill.
- Q-D1-13 [extended] "microcanonical equilibrium soliton plus radiation entropy nonintegrable nonlinear Schrödinger soliton mass fraction prediction numerical test saturable quintic 2022 2023 2024 2025": no kill.
- Q-D1-14 [standard] "spatiotemporal multimode soliton thermalization statistical mechanics light bullet condensation graded-index anomalous dispersion "soliton fraction" OR "soliton condensate" theory open question": found 2405.13716, 2605.02511, 2304.09005. No kill.
- Q-D1-15 [standard] "focusing Gibbs measures with harmonic potential Robert Seong Tolomeo Wang arXiv normalizability concentration soliton": found 2212.11386, 2607.11608, 2312.06232.
- Q-D1-16 [standard] "soliton turbulence final state single large soliton nonintegrable NLS long-time statistical equilibrium number of solitons coarsening 2021–2025 Dyachenko Zakharov Pushkarev revisited": only Colléaux 2025 is new.

D2
- Q-D2-1 [extended] "thermalization incoherent light single-mode fiber third-order dispersion integrability breaking thermalization length scaling six-wave kinetic": found pre-2014 papers only.
- Q-D2-3 [extended] ""integrability breaking" "optical fiber" nonlinear Schrödinger thermalization Raman third-order dispersion "generalized Gibbs" prethermalization 2024 2025 2026": found PRR 6, 023083; 2505.11299; 2512.17777. No kill.
- Q-D2-5 [standard] "anomalous thermalization third-order dispersion optical fiber follow-up 2021-2026 nonequilibrium stationary state incoherent waves kinetic "zero dispersion"": found Barviau 2013 author PDF and EPJ WoC 2023. No kill.
- Q-D2-6 [standard] "generalized Gibbs ensemble to thermal crossover fiber optics experiment integrability breaking recirculating loop Suret Randoux Bastianello 2026": found 2503.16526, 2503.13030, 2601.21085. No kill.
- Q-D2-7 [extended] "six-wave kinetic equation near-integrable cubic nonlinear Schrödinger one-dimensional thermalization time scaling Onorato Dematteis Lvov 2023 2024 2025": found Onorato 2023, 2506.02948 (rigorous β-FPUT WKE, not opened) and 2501.10565 (six-wave KE well-posedness). No kill.
- Q-D2-9 [standard] "Picozzi "Optical wave turbulence: Towards a unified nonequilibrium thermodynamic formulation" HAL pdf open access": found the CREOL-hosted PDF (full text read).
- Q-D2-10 [standard] "integrable turbulence higher-order effects third-order dispersion Raman thermalization optical fiber experiment recirculating loop 2023 2024 2025 departure from integrability": found Fache 2025. No kill.
- Q-D2-11 [standard] ""incoherent" light "single-mode fiber" thermalization "Rayleigh-Jeans" Raman self-steepening kinetic equation 2022–2025 "one-dimensional" optical wave turbulence fiber experiment": found the Zanaglia 2024 abstract. No kill.
- Q-D2-13 [standard] ""anomalous thermalization" OR "truncated thermalization" nonlinear Schrödinger 2022–2026 fourth-order dispersion pure-quartic incoherent waves kinetic": nothing new.
- Q-D2-14 [standard] "thermalization time near-integrable continuous nonlinear Schrödinger equation wave turbulence exponent epsilon^-4 six-wave higher-order dispersion numerical study incoherent waves 1D": found 2609.23175 (Sutherland & Yim, partial pre-emption) and 1812.08279.
- Q-D2-15 [standard] "Zanaglia self-polarization thermalization single-mode fiber incoherent light kinetic equation 2025 Picozzi Garnier "self-polarization"": found HAL hal-05434515 (2025 preprint, not accessed).
- Q-D2-16 [standard] "Manakov equation polarization mode dispersion weak integrability breaking thermalization incoherent waves random birefringence fiber statistical": nothing on thermalization.

D3
- Q-D3-1 [extended] "theory thermalization time Fermi-Pasta-Ulam-Tsingou recurrence modulation instability noise optical fiber kinetic equation irreversible scaling noise level Armaroli Conforti Mussot": found 2205.01349 and 1407.1039.
- Q-D3-2 [standard] ""Incoherent Fermi-Pasta-Ulam recurrences and unconstrained thermalization mediated by strong phase correlations" PRX 2017 Guasoni Picozzi": metadata confirmed.

D4
- Q-D4-1 [standard] "two-dimensional nonlinear Schrödinger Kolmogorov-Zakharov spectrum wrong flux direction inverse cascade puzzle optical turbulence 2D NLS direct cascade log correction": found 2501.12451 and rspa 2023.
- Q-D4-2 [standard] "observation Kolmogorov-Zakharov spectrum optical fiber experiment wave turbulence cascade nonlinear optics 2021–2025": no fibre KZ observation (found a random-matrix KZ model 2401.11545, not opened).

D5

APIs and fetches
- OpenAlex: DOI→id for 24 works. Forward sets (`cites:`, ≥2021-01-01) for 21 works: the 16 listed in §0 plus Michel LMP 2011, Barviau 2013, Suret OE 2011, Chen & Rumpf 2021, Michel OL 2010. Abstracts for about 45 DOIs; OA-status lookups.
- arXiv export API: about 30 ids.
- Crossref: about 25 DOI checks.
- Semantic Scholar: 1 call (Rumpf & Newell 2025; abstract null).
- WebFetch: arXiv abstract pages, the arXiv HTML of 2503.16526v2 and 2505.11299v1, the Princeton seminar page and the Lille thesis page.
- Failures:
  - ScienceDirect (S0167278925004002) and SSRN (5243541) returned HTTP 403.
  - The APS "PDF" link for PRA 106, 033519 returned an HTML landing page; I deleted it and used arXiv.
  - WebFetch could not parse the Garnier-site PDF; I extracted it locally instead.
  - No API rate limits were hit.
- Not done (time): forward sets of Walczak 2015 and Gelash 2019; reading Laurie 2012 (arXiv:1110.4644) and Onorato PNAS 2015 in full.

---------------------------------------------------------------------

### (b) SOURCE LEDGER (id | citation | identifier | access)
---------------------------------------------------------------------
Access levels: FT = full text (read or grep-searched; scope noted); AB = abstract only (publisher, arXiv API, OpenAlex abstract field, or search snippet where noted); NA = not accessed (located by metadata only). DOIs were checked on Crossref or OpenAlex unless marked.

**D1, mathematics**
| id | citation | identifier | access |
|---|---|---|---|
| L1 | Chatterjee, "Invariant measures and the soliton resolution conjecture", CPAM 67, 1737 (2014) | 10.1002/cpa.21501; arXiv:1203.4027 | FT (arXiv v3, abstract and introduction) |
| L2 | Tolomeo & Weber, "Phase transition for invariant measures of the focusing Schrödinger equation" (CMP, accepted) | arXiv:2306.07697 | FT (downloaded; abstract and intro grep) |
| L3 | Seong & Sosoe, CLT for focusing $\Phi^4$ measure in infinite volume | arXiv:2411.07840 | AB |
| L4 | Höfer, "A statistical analogue of soliton resolution for the focusing Schrödinger equation", Princeton seminar 2025-09-08 | math.princeton.edu/node/18986 | AB (seminar abstract; paper not located) |
| L5 | Kim & Kwon, soliton resolution for CM-DNLS | arXiv:2408.12843 | AB (WebFetch summary) |
| L6 | Berthoumieu, multi-soliton-like solutions, nonintegrable NLS with nonzero background | arXiv:2603.29906 | AB |
| L7 | Robert, Seong, Tolomeo & Wang, "Focusing Gibbs measures with harmonic potential" | arXiv:2212.11386 | AB |
| L8 | Dinh, Rougerie, Tolomeo & Wang, radial focusing NLS in general traps | arXiv:2312.06232 | AB |
| L9 | Greco & Wang, phase transition for weakly interacting focusing Gibbs measures with harmonic potential | arXiv:2607.11608 | AB |

**D1, physics and fibre**
| id | citation | identifier | access |
|---|---|---|---|
| L10 | Jordan & Josserand, PRE 61, 1527 (2000) | 10.1103/PhysRevE.61.1527; arXiv:chao-dyn/9905023 | AB |
| L11 | Rumpf & Newell, PRL 87, 054102 (2001) | 10.1103/PhysRevLett.87.054102 | AB |
| L12 | Rumpf & Newell, Physica D 184, 162 (2003) | 10.1016/S0167-2789(03)00220-3; arXiv:nlin/0306011 | FT (arXiv; conclusions) |
| L13 | Rumpf & Newell, Physica D 483, 134923 (2025) | 10.1016/j.physd.2025.134923 (SSRN 5243541) | AB (search snippet only; publisher and SSRN returned 403) |
| L14 | Chen & Rumpf, PRE 104, 034213 (2021) | 10.1103/PhysRevE.104.034213 | AB |
| L15 | Colléaux, Skipp, Nazarenko & Laurie, Physica D 477, 134687 (2025) | 10.1016/j.physd.2025.134687; arXiv:2410.12507 | AB |
| L16 | Biasi, PRE 110, 034107 (2024) | 10.1103/PhysRevE.110.034107; arXiv:2401.15083 | AB |
| L17 | Biasi & Gérard, CMP (2025) | 10.1007/s00220-025-05449-5 | AB |
| L18 | Zhang, Zhang & Zhao, exact nonperturbative equilibrium mode statistics | arXiv:2609.24063 | AB |
| L19 | Koch, Caux & Bastianello, GHD of attractive NLS | arXiv:2110.14574 | AB |
| L20 | Zitelli, Mangini & Wabnitz, Nat. Commun. 15, 1149 (2024) | 10.1038/s41467-024-45185-3; arXiv:2306.15995 | AB |
| L21 | Zitelli, Laser Photonics Rev. (2024) | 10.1002/lpor.202400714 | AB |
| L22 | Zitelli, Ferraro, Mangini & Wabnitz, Photonics Res. 9, 741 (2021) | 10.1364/PRJ.419235 | AB |
| L23 | Zanaglia et al., PRA 113, 063533 (2026) | 10.1103/bf7m-chkd; arXiv:2512.07784 | AB |
| L24 | Zanaglia, Garnier, Carusotto, Doya, Michel & Picozzi, PRL 136, 053802 (2026) | 10.1103/mqzh-w2gh; arXiv:2506.23536 | AB |
| L25 | Zhang, Fan, Mei, Steinmeyer & Hu, BEC of an optical thermodynamic system into a solitonic state | arXiv:2405.13716 | AB |
| L26 | Sharma & Pal, refractive-index distribution and MM soliton condensation | arXiv:2605.02511 | AB |
| L27 | Parra-Rivas, Sun & Wabnitz, 3D spatiotemporal solitons in multimode waveguides | arXiv:2304.09005 | AB |
| L28 | Sun, Parra-Rivas, Agrawal, Hansson, Antonelli & Mecozzi, Photonics Res. (2024), multimode-soliton review | 10.1364/PRJ.531393 | AB |
| L29 | Wright, Renninger, Christodoulides & Wise, Optica 9, 824 (2022) | 10.1364/OPTICA.461981 | FT (NSF PAR copy; grep only; no relevant open statement) |
| L30 | Picozzi & Rica, Opt. Commun. 285, 5440 (2012) | 10.1016/j.optcom.2012.07.081 | NA |
| L31 | Ebrahimi, Drossel & Just, Phys. Scr. (2026) and Physica D (2025) 134905 | 10.1088/1402-4896/ae54df; 10.1016/j.physd.2025.134905 | AB |
| L32 | Iubini & Politi, PRL 134, 097102 (2025) | 10.1103/PhysRevLett.134.097102 | AB |

**D2**
| id | citation | identifier | access |
|---|---|---|---|
| L33 | Suret, Randoux, Jauslin & Picozzi, PRL 104, 054101 (2010) | 10.1103/PhysRevLett.104.054101 | AB |
| L34 | Michel, Garnier, Suret, Randoux & Picozzi, Lett. Math. Phys. 96, 415 (2011) | 10.1007/s11005-010-0452-y; HAL hal-00696729 | NA |
| L35 | Michel et al., Opt. Lett. 35, 2367 (2010) | 10.1364/OL.35.002367 | NA |
| L36 | Suret, Picozzi & Randoux, Opt. Express 19, 17852 (2011) | 10.1364/OE.19.017852 | AB |
| L37 | Barviau, Garnier, Xu, Kibler, Millot & Picozzi, PRA 87, 035803 (2013) | 10.1103/PhysRevA.87.035803 | FT (author preprint, skimmed) |
| L38 | Picozzi, Garnier, Hansson, Suret, Randoux, Millot & Christodoulides, Phys. Rep. 542, 1 (2014) | 10.1016/j.physrep.2014.03.002 | FT (CREOL-hosted PDF; grep plus §5.1–5.2, §6.2–6.3, §7.5 read) |
| L39 | Onorato, Lvov, Dematteis & Chibbaro, Phys. Rep. 1040, 1 (2023) | 10.1016/j.physrep.2023.09.006; arXiv:2305.18215 | FT (arXiv; conclusions) |
| L40 | Vassilev, Commun. Math. Phys. 406, 293 (2025) | 10.1007/s00220-025-05455-7 | FT (OA PDF; abstract and intro grep) |
| L41 | Lebel, Roberti, Randoux, Bonnemain, Copie, El & Suret, J. Nonlinear Waves 2, e4 (2026) | 10.1017/jnw.2026.10029 | FT (OA PDF; abstract, intro, results skimmed) |
| L42 | Fache, Copie, Suret & Randoux, PRL 135, 157201 (2025) | 10.1103/hwpr-628r; arXiv:2503.13030 | AB |
| L43 | Bastianello, Tikan, Copie, Randoux & Suret, PRA 113, 013514 (2026) | 10.1103/xz2w-hndp; arXiv:2503.16526 | FT (arXiv HTML v2 discussion via WebFetch) |
| L44 | Charnay, Escoubet, Copie, Randoux, Bonnemain, Bastianello & Suret, PRL 137, 097202 (2026) | 10.1103/sz13-9shg; arXiv:2601.21085 | AB |
| L45 | Bastianello, De Luca & Vasseur, J. Stat. Mech. (2021) 114003 | arXiv:2103.11997 | AB |
| L46 | Durnin, Bhaseen & Doyon, PRL 127, 130601 (2021) | 10.1103/PhysRevLett.127.130601 | AB |
| L47 | Panfil, Gopalakrishnan & Konik, PRL 130, 030401 (2023) | arXiv:2205.06492 | AB |
| L48 | Łebek & Panfil, SciPost Phys. 18, 186 (2025) | arXiv:2410.23209 | AB |
| L49 | Banks, Buckmaster, Korotkevich, Kovačič & Shatah, PRL 129, 034101 (2022) | 10.1103/PhysRevLett.129.034101; arXiv:2109.02477 | AB |
| L50 | Sutherland & Yim, six-wave scattering in Hamiltonian Dysthe equations | arXiv:2609.23175 | AB |
| L51 | Torres, Garnier, Zanaglia, Ferraro, Michel, Doya, Fatome, Kibler, Wabnitz, Picozzi & Millot, PRL 136, 173801 (2026) | 10.1103/tgtw-qnyq; arXiv:2512.17777 | AB |
| L52 | Zanaglia, "Nonequilibrium self-polarisation and light thermalisation in single mode optical fibers", Complex Days 2024 abstract (Univ. Côte d'Azur page) | — | AB (search snippet only) |
| L53 | Fu, Wang, Wang, Zhang & Zhao, PRR 8, 013314 (2026) | arXiv:2508.15566 | AB |
| L54 | Biagetti, Cecile & De Nardis, PRR 6, 023083 (2024) | 10.1103/PhysRevResearch.6.023083 | AB |
| L55 | Pistone, Chibbaro, Bustamante, L'vov & Onorato, Math. Eng. 1, 672 (2019) | arXiv:1812.08279 | AB |
| L56 | Laurie, "Six-wave systems in one-dimensional wave turbulence", PhD thesis, Warwick (2010) | WRAP 34564 | AB |
| L57 | Selim et al., Opt. Lett. (2023) | 10.1364/OL.489165 | AB |
| L58 | Mendonça & Hizanidis, Physics 8, 15 (2026) | 10.3390/physics8010015 | AB |

**D3**
| id | citation | identifier | access |
|---|---|---|---|
| L59 | Wabnitz & Wetzel, Phys. Lett. A 378, 2750 (2014) | 10.1016/j.physleta.2014.07.018; arXiv:1407.1039 | FT (arXiv, skimmed) |
| L60 | Vanderhaegen, Szriftgiser, Kudlinski, Conforti, Armaroli & Mussot, PRA 106, 033519 (2022) | 10.1103/PhysRevA.106.033519; arXiv:2205.01349 | FT (arXiv, skimmed) |
| L61 | Guasoni et al., PRX 7, 011025 (2017) | 10.1103/PhysRevX.7.011025 | AB (search snippet) |

**D4**
| id | citation | identifier | access |
|---|---|---|---|
| L62 | Skipp, Laurie & Nazarenko, Proc. R. Soc. A 479, 20230162 (2023) | 10.1098/rspa.2023.0162 | AB |
| L63 | Rosenhaus & Falkovich, weak and strong turbulence in self-focusing and defocusing media | arXiv:2501.12451 | AB |
| L64 | Bedrossian, Nonlinearity 37, 065007 (2024) | 10.1088/1361-6544/ad3794 | AB |
| L65 | Karailiev et al., PRL 133, 243402 (2024) | 10.1103/PhysRevLett.133.243402 | AB |
| L66 | Baudin, Fusaro, Garnier, Berti, Krupa, Carusotto, Rica, Millot & Picozzi, EPL 134, 14001 (2021) | 10.1209/0295-5075/134/14001; arXiv:2012.02235 | AB |
| L67 | Ferraro et al., Physica D (2025) 134758 | 10.1016/j.physd.2025.134758; arXiv:2505.11299 | AB (arXiv API abstract; WebFetch HTML check for KZ content negative) |

**D5**
| id | citation | identifier | access |
|---|---|---|---|
| L70 | Derevyanko, Low Temp. Phys. (2026) | 10.1063/10.0044111 | AB |

**Seed papers located via OpenAlex, used only for forward-citation sets (all NA)**
- Dyachenko, Newell, Pushkarev & Zakharov, Physica D 57, 96 (1992), 10.1016/0167-2789(92)90090-A
- Van Simaeys et al., PRL 87, 033902 (2001)
- Mussot et al., Nat. Photon. 12, 303 (2018)
- Pierangeli et al., PRX 8, 041017 (2018)
- Agafontsev & Zakharov, Nonlinearity 28, 2791 (2015)
- Walczak, Randoux & Suret, PRL 114, 143903 (2015)
- Zakharov, Stud. Appl. Math. 122, 219 (2009)
- Copie, Randoux & Suret, Rev. Phys. 5, 100037 (2020)
- Gelash et al., PRL 123, 234102 (2019)
- Wright et al., OE 23, 3492 (2015)
- Laurie, Bortolozzo, Nazarenko & Residori, Phys. Rep. 514, 121 (2012) (arXiv:1110.4644)
- Onorato, Vozella, Proment & Lvov, PNAS 112, 4208 (2015)
- Lvov & Onorato, PRL 120, 144301 (2018)

**Named in the task but not located in this session (not cited as evidence)**
- Zakharov, Pushkarev, Shvets & Yan'kov, JETP Lett. 48, 83 (1988)
- Lebowitz, Rose & Speer, J. Stat. Phys. 50, 657 (1988) (known here only through L2's abstract)
- Chatterjee & Kirkpatrick, CPAM (2012)
- Tao's soliton-resolution survey
- Michel et al. OL 2010 (located as L35, not read)
- Nazarenko, *Wave Turbulence* (LNP 825, 2011)
- Bortolozzo et al., JOSA B 26, 2280 (2009)
- Onorato et al., PLA 380, 3173 (2016)
- Vanderhaegen et al., PNAS 2021

---------------------------------------------------------------------

### LAST CHECKS (16:41–16:43): forward sets of the key 2024–2026 open-statement papers
---------------------------------------------------------------------
OpenAlex citing works:

| paper | citing works found | content |
|---|---|---|
| Vassilev 2025 | 1 | FPUT kinetic-equation analysis, JEDP 2026 |
| Fache et al. 2025 | 6 | no kinetic/GHD theory with perturbations |
| Bastianello GGE 2026 | 2 | — |
| Lebel et al. 2026 | 0 | — |
| Colléaux et al. 2025 | 2 | — |

**None answers the D2 open statements.** As of the OpenAlex index on 2026-10-20, nobody has supplied the generalized kinetic/GHD theory with weak non-integrable perturbations that Lebel et al. 2026 call for.

Finished 16:43 EDT. No computation beyond text extraction; memory use trivial.

Files saved by this helper in ~/analytical-nl-discovery-data/lit-T-20261020-claude-interactive-04/ (open-access only; .txt are local text extractions):
- chatterjee_arxiv1203.4027.pdf
- tolomeo_weber_arxiv2306.07697.pdf
- picozzi_physrep2014_creol.pdf
- onorato_physrep2023_arxiv2305.18215.pdf
- garnier_site_beta4.pdf (Barviau et al. PRA 2013 preprint)
- picozzi_garnier_xu_rica_WTformalisms_chapter_garnier_site.pdf (book chapter "Introduction to Wave Turbulence Formalisms for Incoherent Optical Waves"; downloaded but not used)
- vanderhaegen_arxiv2205.01349.pdf
- wabnitz_wetzel_arxiv1407.1039.pdf
- wright_optica2022_nsfpar10347198.pdf (the Optica 9, 824 (2022) review, not the Nat. Phys. one)
- vassilev_cmp2025.pdf
- lebel_jnw2026.pdf
- rumpf_newell_physd2003_nlin0306011.pdf

Other files in that directory were written by sibling helpers and were not read by me.

Addendum (16:43): arXiv API searches for the Höfer statistical-soliton-resolution paper found nothing:
- `au:Hofer AND abs:Gibbs AND abs:soliton` returned 0 results;
- `abs:"soliton resolution" AND abs:Gibbs AND abs:focusing` returned only Krishnan & Ray, "Local limit of the focusing discrete NLS", arXiv:2509.25759 (2025) (abstract only): the infinite-volume local limit of the focusing DNLS Gibbs measure in $d\ge3$, following Dey–Kirkpatrick–Krishnan's phase transition (CMP 2025, 10.1007/s00220-025-05408-0).

The Höfer et al. result therefore stays at seminar-abstract level (ledger L4).

## Appendix D. Helper claude-interactive.22.4 (lasers and review mining): kill-search logs and source ledger

Reproduced from the helper's report (scratchpad, 2026-10-20), headings demoted, otherwise unedited. Access levels are the helper's own. Statements here were not all re-checked by claude-interactive.22; those used in the cards were, as marked there. Text quoted in titles or search strings is not a quotation of a source.

###### Kill search for F1. Replica-symmetry breaking (RSB) and glassiness in random (fibre) lasers
   - OpenAlex forward citations:
     - Ghofraniha et al. Nat. Commun. 6, 6058 (2015): 130 citing works since 2021, all scanned.
     - Antenucci et al. PRL 114, 043901 (2015): 37 citing, scanned.
     - Gradenigo et al. PRR 2, 023399 (2020): 17 citing, scanned.
   - OpenAlex title search: "replica symmetry breaking random laser comment", "intensity fluctuation overlap replica symmetry breaking without glass", "replica symmetry breaking random laser independent modes null model". No comment or rebuttal paper found.
   - WebSearch (extended): `"replica symmetry breaking" random laser intensity fluctuation overlap criticism not genuine glass phase artifact`. No explicit critique found.
   - WebSearch (extended): `random laser "replica symmetry breaking" overlap "pump fluctuations" OR "pump energy fluctuations" OR "common-mode" spurious peaks q=±1 normalization`. Nothing on a common-mode null model.
   - Late: OpenAlex forward citations of Sarkar et al. 2020 [S75], 33 works, titles scanned. No null-model or critique paper. Mostly new "RSB observed in X" papers, plus Parisi's Nobel Lecture "Multiple equilibria", RMP 95, 030501 (2023), doi:10.1103/RevModPhys.95.030501 (not accessed; worth checking how Parisi presents random-laser RSB).
   - Pierangeli et al. Nat. Commun. 8, 1501 (2017): DOI verified by Crossref as 10.1038/s41467-017-01612-2. The DOI given in the brief, ...-0, returns 404 in OpenAlex. Not accessed.

###### Kill search for F2. Self-starting of passive mode locking; photon BEC in an Er/Yb fibre cavity
   - OpenAlex forward citations: Gordon & Fischer 2002, 19 citing since 2021; Vodonos 2004, 7 citing since 2021. All scanned.
   - WebSearch: `self-starting passive mode locking build-up time statistics first-order phase transition theory experiment dispersive Fourier transform noise threshold`; `"self-starting" mode-locked fiber laser buildup time distribution statistics theory Kramers escape entropic barrier experiment 2022 OR 2023 OR 2024 OR 2025`. The second found [S23] via cris.huji.ac.il (bibliographic record and abstract read).

###### Kill search for F3. Wave-turbulent spectral broadening, random-fibre-laser kinetics, laminar-turbulent transition
   - OpenAlex forward citations: [S34] 66 since 2021; [S38] 59; [S37] 38. All scanned.
   - WebSearch: `"directed percolation" "fiber laser" OR "fibre laser" laminar turbulent transition universality`. No fibre-laser DP study found; results were hydrodynamic DP only, e.g. Lemoult et al., Nat. Phys. 12, 254 (2016), arXiv:1510.07868 (not accessed).
   - WebSearch: `Raman fiber laser turbulent spectral broadening theory discrepancy experiment spectrum shape wings "wave turbulence" open problem Babin Churkin`. No discrepancy statement found.

###### Kill search for N1. Physics of noise-like pulses (NLPs) in fibre lasers: is the NLP a statistically stationary, wave-turbulent (thermalized-like) bound state, and what sets its spectral width, spike duration and envelope?
   - OpenAlex forward citations of [S42]: 138 works since 2022, titles scanned with keywords (mechanism, theory, origin, turbulence, statistic, thermodynamic, kinetic). Only numerical or experimental mechanism papers ([S44]; pure-quartic soliton collapse, Chaos Solitons Fractals 2024-2025; build-up studies).
   - WebSearch: `noise-like pulses fiber laser formation mechanism "still" debated OR unclear OR "not fully understood" review physical origin`.
   - WebSearch: `noise-like pulse fiber laser theory "wave turbulence" OR "thermalization" OR "statistical" formation mechanism 2023 2024 2025 explanation unified`.
   - WebSearch (extended): `"noise-like pulse" OR "noise-like pulses" "statistical mechanics" OR "thermodynamic" OR "Rayleigh-Jeans" OR "wave turbulence" theory fiber laser spectrum analytic`.
   - OpenAlex forward citations of [S41]: 73 works since 2022, scanned. Machine-learning analysis (Opt. Express 2022, doi:10.1364/oe.455945), coherence and randomness studies, Q-switched NLPs, "confined turbulence" multi-pulse structures (Chaos Solitons Fractals 2026), numerical rogue-wave mechanisms.
   - Result: no analytic statistical theory of the NLP state found.

###### Kill search for N2. Directed-percolation (DP) universality of the laminar-turbulent transition in long fibre lasers
   - WebSearch: `"directed percolation" "fiber laser" OR "fibre laser" laminar turbulent transition universality`. No fibre-laser DP study found.
   - WebSearch: `"directed percolation" laser OR optical "spatiotemporal intermittency" experiment long-delay semiconductor laser critical exponents`. Found [S45].

###### Kill search for N3. Boltzmann versus Gibbs entropy at negative temperature: a fibre test

###### Kill search for N4. Lynden-Bell violent relaxation / quasi-stationary states in long-range (nonlocal) optical systems

###### Kill search for N5. Prethermal state to true thermalization in 2D fluids of light (BKT precursor)
   - OpenAlex forward citations of [S52]: 22 works, all scanned.
   - WebFetch of the review "Paraxial fluids of light", Glorieux et al., Adv. At. Mol. Opt. Phys. (2025), arXiv:2504.06262 [S56]. The extraction found no explicit open-problem statement on thermalization.

###### Kill search for N6. Raman beam clean-up and its interplay with Kerr self-cleaning in graded-index multimode fibres (corrected after reading the full text)

###### Kill search for N11. Statistical (wave-turbulence) theory of polarization attraction / spontaneous repolarization in counter-propagating fibre geometries
   - WebSearch: `polarization attraction counter-propagating optical fiber statistical description partially polarized wave turbulence kinetic theory incoherent`. Only deterministic or stability analyses: Wabnitz group arXiv:1304.7231; [S72].
   - OpenAlex search (2015+): "polarization attraction partially polarized statistical"; "spontaneous repolarization incoherent wave turbulence counter-propagating". Nothing relevant.
   - Done late (OpenAlex):
     - Forward citations of [S72]: 2 works. Fusaro, Berti, Guasoni, Jauslin, Picozzi & Fatome, PRA 99, 043826 (2019) (abstract only), which reports self-polarization of two uncorrelated partially polarized counter-propagating waves at the fibre mid-point, numerics and experiment, with a geometric degree of polarization. Also A. Fusaro's 2019 PhD thesis (doi:10.70675/c50b3d60z5a15z4c6azb34dzc0dfd1100504; abstract only, truncated), whose repolarization part rests on Hamiltonian singularities.
     - Forward citations since 2017 of the theory paper "Theory of lossless polarization attraction in telecommunication fibers", JOSA B 28, 100 (2011), doi:10.1364/josab.28.000100: 21 works, scanned. Mostly telecom applications and mid-point self-organization (JOSA B 36, 2360 (2019); Opt. Commun. 2023). No kinetic or statistical theory found.
     - Caveat: the thesis full text was not read and may contain partial statistical treatments.

#### (b) Source ledger

"located" = DOI verified via Crossref/OpenAlex/arXiv. Access levels as defined in the header.

| id | citation | DOI / arXiv | access |
|---|---|---|---|
| S1 | Ghofraniha et al., Nat. Commun. 6, 6058 (2015) | 10.1038/ncomms7058; arXiv:1407.5428 | full text partly (methods/overlap definition, via WebFetch of arXiv HTML) |
| S2 | Antenucci, Conti, Crisanti & Leuzzi, PRL 114, 043901 (2015) | 10.1103/PhysRevLett.114.043901 | title/metadata only (forward citations scanned); not accessed |
| S3 | Gradenigo, Antenucci & Leuzzi, PRR 2, 023399 (2020) | 10.1103/PhysRevResearch.2.023399; arXiv:1902.00111 | abstract only |
| S4 | Antenucci, Crisanti & Leuzzi, Sci. Rep. 5, 16792 (2015) | 10.1038/srep16792 | not accessed (DOI verified) |
| S5 | Tommasi, Ignesti, Lepri & Cavalieri, Sci. Rep. 6, 37113 (2016) | 10.1038/srep37113 | abstract only |
| S6 | Basak, Blanco & López, Sci. Rep. 6, 32134 (2016) | 10.1038/srep32134 | abstract only |
| S7 | Moura et al., PRL 119, 163902 (2017) | 10.1103/PhysRevLett.119.163902 | abstract only |
| S8 | Conti, Ghofraniha, Leuzzi & Ruocco, book chapter (2022) | arXiv:2209.03781 | abstract only |
| S9 | Niedda, Gradenigo, Leuzzi & Parisi, SciPost Phys. 14, 144 (2023) | 10.21468/SciPostPhys.14.6.144 | abstract only |
| S10 | Niedda, Leuzzi & Gradenigo, J. Stat. Mech. (2023) 053302 | 10.1088/1742-5468/acd2c4; arXiv:2212.05106 | abstract only |
| S11 | Benedetti & Leuzzi, SciPost Phys. 20, 153 (2026) | 10.21468/SciPostPhys.20.6.153 | abstract only |
| S12 | Câmara et al., PRR 8 (2026) | 10.1103/b3py-tyv8 | abstract only |
| S13 | Calvanese Strinati, Gentilini, Ghofraniha, Pierangeli & Conti, Adv. Opt. Photon. 18, 421 (2026) | 10.1364/aop.574825 | abstract only |
| S14 | Alves et al., PRL 132, 093801 (2024) | 10.1103/PhysRevLett.132.093801; arXiv:2403.02477 | full text (arXiv PDF saved to data dir as arXiv-2403.02477-alves.pdf/.txt; grep of definitions and controls) |
| S15 | Chen et al., Commun. Phys. (2025) | 10.1038/s42005-025-02332-6 | abstract only |
| S16 | Palacios et al., PRA 107, 063510 (2023) | 10.1103/PhysRevA.107.063510 | abstract only |
| S17 | Kroeze et al., Science 389, 1122 (2025) | 10.1126/science.adu7710 | abstract only |
| S18 | Carmona et al., Chaos Solitons Fractals (2026) | 10.1016/j.chaos.2026.119237 | abstract only |
| S19 | Qi et al., Light Sci. Appl. (2024) | 10.1038/s41377-024-01475-5 | abstract only |
| S20 | Lima et al., PRA 96, 013834 (2017) | 10.1103/PhysRevA.96.013834 | abstract only |
| S21 | Haus & Ippen, Opt. Lett. 16, 1331 (1991) | 10.1364/OL.16.001331 | not accessed (DOI verified) |
| S22 | Krausz, Brabec & Spielmann, Opt. Lett. 16, 235 (1991) | 10.1364/OL.16.000235 | not accessed (DOI verified) |
| S23 | Gordon, Gat, Fischer & Kärtner, Opt. Express 14, 11142 (2006) | 10.1364/OE.14.011142 | abstract only |
| S24 | Wu et al., IEEE PTL (2026) | 10.1109/lpt.2026.3678387 | abstract only |
| S25 | Jiang et al., Opt. Lett. (2026) | 10.1364/ol.587533 | abstract only |
| S26 | Chen et al., PNAS (2026) | 10.1073/pnas.2624826123 | abstract only |
| S27 | Kalashnikov & Sorokina, Appl. Sci. 16, 8895 (2026) | 10.3390/app16178895; arXiv:2608.10510 | abstract only |
| S28 | Gordon & Fischer, PRL 89, 103901 (2002) | 10.1103/PhysRevLett.89.103901 | metadata only; not accessed |
| S29 | Gat, Gordon & Fischer, PRE 70, 046108 (2004) | 10.1103/PhysRevE.70.046108; arXiv:cond-mat/0311241 | abstract only |
| S30 | Vodonos et al., PRL 93, 153901 (2004) | 10.1103/PhysRevLett.93.153901 | abstract only |
| S31 | Weill, Bekker, Levit & Fischer, Nat. Commun. 10, 747 (2019) | 10.1038/s41467-019-08527-0 | abstract only (OA PDF exists) |
| S32 | Weill et al., Opt. Express 29, 27807 (2021) | 10.1364/oe.430406 | abstract only |
| S33 | Liu & Xie, Open Phys. (2022) | 10.1515/phys-2022-0031 | abstract only |
| S34 | Turitsyna et al., Nat. Photon. 7, 783 (2013) | 10.1038/nphoton.2013.246; arXiv:1401.0630 | abstract only |
| S35 | Roche et al., PRL 131, 053801 (2023) | 10.1103/PhysRevLett.131.053801 | abstract only |
| S36 | Vasudevan et al., Nat. Commun. (2025) | 10.1038/s41467-025-63044-7 | abstract only |
| S37 | Babin et al., JOSA B 24, 1729 (2007) | 10.1364/JOSAB.24.001729 | abstract only |
| S38 | Churkin et al., Nat. Commun. 6, 6214 (2015) | 10.1038/ncomms7214 | abstract only |
| S39 | Han et al., Laser Photon. Rev. (2024) | 10.1002/lpor.202400122 | abstract only |
| S40 | Ma et al., Laser Photon. Rev. (2025) | 10.1002/lpor.202500421 | abstract only |
| S41 | Meng et al., Nat. Commun. 12, 5567 (2021) | 10.1038/s41467-021-25861-4 | abstract only |
| S42 | Horowitz, Barad & Silberberg, Opt. Lett. 22, 799 (1997) | 10.1364/OL.22.000799 | not accessed (DOI verified; forward citations scanned) |
| S43 | Runge, Aguergaray, Broderick & Erkintalo, Opt. Lett. 38, 4327 (2013) | 10.1364/OL.38.004327 | abstract only |
| S44 | Lang et al., Opt. Express (2023) | 10.1364/oe.508074 | abstract only |
| S45 | Faggian, Ginelli, Marino & Giacomelli, PRL 120, 173901 (2018) | 10.1103/PhysRevLett.120.173901; arXiv:1707.08327 | abstract only |
| S46 | Lemoult et al., Nat. Phys. 12, 254 (2016) | 10.1038/nphys3675 | not accessed (DOI verified) |
| S47 | Buonsante, Franzosi & Smerzi, PRE 95, 052135 (2017) | 10.1103/PhysRevE.95.052135 | abstract only |
| S48 | Marques Muniz et al., Science 379, 1019 (2023) | 10.1126/science.ade6523 | not accessed (DOI verified) |
| S49 | Deng & Hani, Invent. Math. (2023) | 10.1007/s00222-023-01189-2; arXiv:2104.11204 | abstract only |
| S50 | Duval & Cherroret, PRA 107, 043305 (2023) | 10.1103/PhysRevA.107.043305 | abstract only |
| S51 | Duval & Cherroret, PRA 111, L021301 (2025) | 10.1103/PhysRevA.111.L021301 | abstract only (OpenAlex summary) |
| S52 | Abuzarli, Cherroret, Bienaimé & Glorieux, PRL 129, 100602 (2022) | 10.1103/PhysRevLett.129.100602 | abstract only |
| S53 | Krupa et al., APL Photonics 4, 110901 (2019) | 10.1063/1.5119434 | full text of relevant sections (local OA copy saved by a sibling helper; grep of Sec. VII and Raman parts) |
| S54 | Ferraro, Baudin, Gervaziev, Fusaro, Picozzi & Garnier, Physica D (2025) | 10.1016/j.physd.2025.134758; arXiv:2505.11299 | full text, introduction/outline paragraphs (local arXiv text) |
| S55 | Lovisetto, Braidotti, Prizia, Michel, Clamond et al., Commun. Phys. 7 (2024) | 10.1038/s42005-024-01684-9; arXiv:2205.10948 | abstract only |
| S56 | Glorieux et al., "Paraxial fluids of light", Adv. At. Mol. Opt. Phys. (2025) | 10.1016/bs.aamop.2025.04.002; arXiv:2504.06262 | partial full text (WebFetch extraction; no open statements found) |
| S57 | Gomes et al., Sci. Rep. 6, 27987 (2016) (Nd:YBO$_3$ powder random laser) | 10.1038/srep27987 | full text via PMC4904273 (WebFetch extraction: definitions and controls) |
| S75 | Sarkar, Bhaktha & Andreasen, Sci. Rep. 10, 2628 (2020) | 10.1038/s41598-020-59575-2 | full text via PMC7021834 (WebFetch extraction) |
| S76 | Gomes et al., PRA 94, 011801(R) (2016), Er random fibre laser glassy behaviour | 10.1103/PhysRevA.94.011801 | not accessed (title/DOI via OpenAlex) |
| S58 | Pierangeli et al., Nat. Commun. 8, 1501 (2017) | 10.1038/s41467-017-01612-2 (brief's "-0" is wrong) | not accessed |
| S59 | Kirton & Keeling, PRL 111, 100404 (2013) | 10.1103/PhysRevLett.111.100404 | not accessed (DOI verified) |
| S60 | Wright, Wu, Christodoulides & Wise, Nat. Phys. 18, 1018 (2022), "Physics of highly multimode nonlinear optical systems" | 10.1038/s41567-022-01691-z | not accessed (paywalled; no arXiv version found) |
| S61 | Picozzi et al., Phys. Rep. 542, 1 (2014) | 10.1016/j.physrep.2014.03.002 | full text of Sec. 7 (local copy in data dir, file `picozzi_physrep2014_creol.txt`, saved by a sibling helper; source presumably author/CREOL-hosted, provenance to be confirmed by the PI); forward citations since 2023 scanned |
| S62 | Carusotto & Ciuti, RMP 85, 299 (2013) | arXiv:1205.6500 | partial full text (WebFetch extraction; no explicit open problems found) |
| S70 | Baudin et al., PRL 130, 063801 (2023) | 10.1103/PhysRevLett.130.063801 | title only (in citing lists) |
| S71 | Chen, Liu, Wu, Cai, Ren & Xu, PRB 113, 184208 (2026) | 10.1103/qkl6-1xcz | abstract only (APS landing page) |
| S72 | Hamraoui, Guasoni, Picozzi, Assémat, Jauslin & Sugny, PRA 93, 053830 (2016) | 10.1103/PhysRevA.93.053830 | abstract only |
| S65 | Torres, Garnier, Zanaglia, Ferraro, Michel, Doya et al., PRL (2026) | 10.1103/tgtw-qnyq | abstract only |
| S73 | Wright, Renninger, Christodoulides & Wise, Optica 9, 824 (2022) | (DOI not verified by me) | full text grep only (local copy saved by a sibling helper) |

Search-result-only items (not in the table, not accessed): SPIE 11670, 116700K (2021), doi:10.1117/12.2577685; Sci. Rep. 11 (2021), doi:10.1038/s41598-021-01491-0; PRA 108, 063507 (2023), doi:10.1103/PhysRevA.108.063507; Qi et al. Adv. Photon. 8, 014001 (2026), doi:10.1117/1.AP.8.1.014001 (abstract read via OpenAlex; full text fetch returned empty).

