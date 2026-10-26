---
agent: claude-interactive.23
model: claude-opus-5-5
family: claude
date: 2026-10-20
task: T-20261020-claude-interactive-05
orchestrator: claude-interactive
base: "PR #91, task/T-20261020-claude-interactive-03"
cards: [P-20261020-gpt-g-02, P-20261020-gpt-g-03]
status: complete
---

# Cross-family novelty review of the three gpt-g thermalization cards

This is the Claude-family (second-family) literature review of the three candidate cards filed by gpt-g (gpt-6-astra) in PR #91 for the PI's request of 2026-10-20 ("longstanding problems in optical thermalization … only stuff where novelty could be argued as high"). The review is adversarial: for each card I tried to find prior work that solves it, or reduces it to a modest adaptation of known theory. It is a literature assessment. No derivation, simulation or run was made, and no number in this document comes from a run.

## Summary

No card is killed: two independent searches found no prior solution of any of the three targets. Two cards meet the PI's bar ("novelty could be argued as high") and one does not.

| Card | Verdict | Decisive source | Change on the card |
|---|---|---|---|
| P-20261020-gpt-g-02, Hamiltonian DNLS breather coarsening | **Novelty lowered from high to medium.** Open; stays candidate. | Iubini et al., PRL 122, 084102 (2019), with Iubini, Politi and Politi (2017). The mechanism, a fitted exponential exchange rate and the predicted logarithmic coarsening are already published. | novelty_confidence high → medium; audited_by [gpt, claude]. Additions, marked; the "high provisional novelty" sentence marked superseded. |
| P-20261020-gpt-g-03, nonlinear Anderson spreading | **Audited.** Open; high novelty defensible for a controlled or rigorous result on the standard chain. | De Roeck, Giacomin, Hannani and Huveneers (Nonlinearity 2026) cover only the chain without linear hopping. De Roeck, Huveneers and Prośniak (CMP 2025) state their technique fails for NLS. Basko (2011) already has a heuristic sub-power law. | candidate → audited; audited_by [gpt, claude]. Additions, marked: the NLS obstacle; Cong–Shi–Zhang; Aubry 2023; platform numbers; sharper first targets. |

**Quotations.** All eight longstanding-evidence quotations I checked on the cards are verbatim. A ninth (Iubini et al. 2013) is confirmed in substance by the 2012 arXiv preprint, arXiv:1203.4162v1, which reads "a convergence" where the card's published-manuscript quotation reads "a final convergence". I did not access the published manuscript. The paraphrased statements I checked are accurate: Baldovin et al. 2021, Giachello et al. 2025 Appendix B, Giusfredi et al. 2026, Iubini et al. 2017, De Roeck et al. 2024.

**Lab tests and tractability.** The three cards differ much more on these than on novelty:
- **-01** has a working optical platform. The Lille loop records the full field, from which both the DOS and $S(k)$ can be extracted.
- **-02** and **-03** cannot reach their asymptotic questions in any optical experiment found. Their lab tests are limited to local mechanisms.
- **-03** is also the hardest to make progress on. A heuristic answer exists (Basko 2011), and the rigorous route has a named obstacle and an active competing group.

## Method and independence

1. I read AGENTS.md, `docs/WORKFLOW.md`, and, on each card, only the front matter, Target quantity, Signal of hidden simplicity, Longstanding evidence, Analytical foothold, Assumptions, Oracle, Lab test and "How a solution would be recognized" sections.
2. I then ran my own kill search before opening gpt-g's "Claimed and partial resolutions"/"Resolution audit", "Kill search", "Sharpest statement of the gap" and "Risks and must-reads" sections, its review document or its search log. Three helper subagents (claude-interactive.23.1, .23.2, .23.3; claude-opus-5-5), one per card, searched the web in parallel. They were told not to open any file in the repository, so their searches were not anchored on gpt-g's notes either. I am responsible for every statement below; where a statement rests only on a helper's reading, it says so.
3. I re-read the decisive primary sources myself from arXiv full texts (downloaded to the data directory, not committed) and checked every quotation the cards use as longstanding evidence. For Iubini et al. (2013) I could check only the 2012 arXiv preprint, whose wording differs by one word (see card -02).
4. Only then did I read gpt-g's review and the remaining card sections and compare (section "Comparison with gpt-g's search").

The branch of the Claude scout (task/T-20261020-claude-interactive-04) was not read.

## P-20261020-gpt-g-02: condensation time and coarsening of breathers in the isolated Hamiltonian DNLS

**Verdict: open, but novelty is medium, not high. Lower `novelty_confidence` from high to medium and leave the card `candidate` (audited_by gpt, claude).**

The deciding sources are Iubini, Chirondojan, Oppo, Politi and Politi, PRL 122, 084102 (2019), arXiv:1811.05798v3, and Iubini, Politi and Politi, J. Stat. Mech. (2017) 073201, arXiv:1701.08636v2. I read both in full text. Together they already contain:
- the mechanism (an adiabatic invariant that freezes tall breathers);
- the key quantitative input, fitted;
- the predicted macroscopic law.

### (a) Longstanding evidence

The card's quotations from Rumpf (2004), Politi et al. (2022, Sec. 6) and Iubini and Politi (2025, conclusion) are verbatim. Its descriptions of Giachello et al. (2025, Appendix B), Giusfredi et al. (2026, introduction) and the 2021 review are accurate.

The Iubini et al. (2013) sentence, which the card quotes from the Strathclyde manuscript, appears in the 2012 arXiv preprint (arXiv:1203.4162v1) with "a convergence" in place of "a final convergence". The same preprint's abstract already says convergence takes astronomical times, slowed further by coarsening. Two remarks:
- **Rumpf (2004)** cautions that thermalization "may have extremely long transients". That is a caution, not a statement that a question is open.
- **The 2017 paper has the strongest direct statement.** It says the problem of determining the macroscopic relaxation law to the single-breather state "is still open". The card cites the 2017 paper but not this sentence; I have added it.

The question has been open since at least 2004 (Rumpf) and explicitly since 2017. It is longstanding.

### (b) Kill search

Not killed. Helper .23.2 searched:
- the arXiv API (all of Iubini's 2012–2026 entries, keyword queries);
- Semantic Scholar forward citations of Mithun et al. 2018, Iubini et al. 2019, Iubini et al. 2013 and Rasmussen et al. 2000;
- about 20 web queries.

Neither of us found a derivation, from the closed Hamiltonian dynamics above $h=2a^2$, of a late-time $n_b(t)$ law or a condensation-time distribution. No rigorous arrest or ergodicity theorem for this regime turned up either. The closest work:
- **Iubini et al. (2019).** One breather on a *positive-temperature* background held by reservoirs at the chain ends ($N=31$, per helper .23.2).
  - Fitted adiabatic-invariant diffusion $D\approx e^{-\gamma b}$ with $\gamma=1.13\pm0.09$, and an exponential lifetime.
  - A rough first-hopping estimate that might grow super-exponentially with $b$, which the authors themselves say is only qualitative.
  - The conclusion that in an isolated chain condensation "proceeds through a practically unobservable logarithmic coarsening", citing the 2017 paper.
- **Iubini, Politi and Politi (2017).** Stochastic surrogates with an imposed amplitude-dependent coupling. Power-law couplings give power-law coarsening. Exponentially small coupling gives freezing, and their Sec. 4 says it predicts logarithmic coarsening in that regime.
- **Politi, Politi and Iubini (2022).** A unidirectional-coupling model: the background drives the breather and does not feel it.
  - Adiabatic invariant from canonical perturbation theory in $1/b$.
  - Fitted $D\propto e^{-cb}$ with $c\simeq1.07$, and a Lévy toy model with tail exponent 2.2 that matches the distribution of invariant changes (checked by me in the full text).
  - The events that change the invariant are unidentified.
- **Iubini and Politi (2025).** Open (Langevin-reservoir) setups: negative-temperature states are metastable, with $\tau\approx e^{\lambda|T|}$. The rate $\lambda$ is derived only for a stochastic non-interacting model; for the DNLS it is semi-phenomenological (helper).
- **Iubini et al. (2013).** Isolated chain, $N=4096$, up to $t\sim10^7$: a quasi-stationary multibreather state with no visible coarsening (helper, full text).
- **Neighbouring.** None gives a Hamiltonian coarsening or first-passage law.
  - Numerics: Kalish, Fittipaldi de Castro and Benalcazar, arXiv:2512.07774 (Dec 2025; abstract read by me), a dynamical order parameter for the nonergodic transition; Archilla, Bajārs and Flach (2025).
  - Bath-coupled stochastic models: Giusfredi et al. (2025), which obtains $N_b\sim\sqrt{\ln t}$ with baths; Ebrahimi, Drossel and Just (2025, 2026).
  - Rigorous single-breather metastability with boundary dissipation: Eckmann and Wayne (2018, 2020); Cuneo, Eckmann and Wayne (2017).
  - Lowest-order breather–phonon channels, which vanish for large breathers: Johansson and Aubry (2000); Johansson (2001).

### (c) Novelty if solved

The card's expected answer is already in the literature as a prediction, and its key ingredient has been measured numerically. Plugging the fitted exponential exchange rate into the 2017 surrogate framework gives logarithmic coarsening. Helper .23.2 reached the same "modest adaptation" reading independently. For the condensation-time half, a Kramers estimate over the microcanonical large-deviation landscape (Gradenigo et al. 2021), with the kinetic prefactor suppressed by the invariant as in Iubini and Politi (2025), gives an exponential, memoryless first-passage law. That too is a standard adaptation.

What remains genuinely open:
1. a first-principles rate, and jump-size law, for the events that change the invariant, with backreaction and both conservation laws (Politi et al. 2022 call this "still an open problem");
2. whether the Markov closure behind logarithmic coarsening holds in the isolated chain;
3. whether stability is Nekhoroshev-like (super-exponential), which would mean genuine arrest;
4. the order of limits, given the finite-size strip above the infinite-temperature line.

A result on items 1–2 is a "new result with clear precedent" in the same field, which is level 3 (medium) on the repository's novelty anchors (`docs/RANKING_RUBRIC.md`). It would be high only if it overturned the prediction (for example, a positive arrest probability or a non-logarithmic law), or if it were a rigorous bound. Neither can be presumed beforehand. gpt-g's own review lists the main risk as "stochastic surrogates and reservoir escape laws already exist", and I agree. I think that risk is larger than the card's "high" allows: the surrogate already predicts this card's answer, and that prediction is not recorded on the card.

### (d) Foothold

The card's first target (a conditional rate and size distribution of invariant-changing events with backreaction, in a microcanonical background) is exactly the problem Politi et al. (2022) could not solve. It is meaningful, but probably not achievable in a session or two. A sharper first target is to derive the exponent $c$ in $D\propto e^{-cb}$ from first principles, as follows.
- Use the 2022 unidirectional model, where a fitted value ($c\simeq1.07$) and a matching Lévy toy model with tail exponent 2.2 exist (both checked in the full text).
- Use a multi-phonon resonance estimate. The lowest-order channels vanish (Johansson 2001), so the order of the first open channel grows with $b$.
- Decide whether the rate is exponential or super-exponential in $b$ (the 2019 paper's rough dimer argument suggests the latter).

This is checkable with a small integrator, gives a usable scaling law, and is a prerequisite for both the coarsening and the arrest questions. Adding backreaction comes next; dimer-mediated jumps need two-way coupling.

### (e) Optical relevance and lab test

Weak, for the reasons below. Platform numbers are from helper .23.2:
- **Coarsening is out of reach.** Iubini et al. (2019) call it practically unobservable even in simulation.
- **Waveguide arrays.** Femtosecond-written arrays (Kirsch et al., Nat. Phys. 2025, DOI 10.1038/s41567-024-02736-1) have a 37-site domain and about 2–3 coupling lengths over 100 mm.
- **Fibre loops.** 2D fibre-loop meshes (Marques Muniz et al., Sci. Rep. 2019) have about $100\times100$ sites, with data shown to step 60. The Science 2023 negative-temperature experiment did not report breather condensation (abstract only, both scouts).
- **Discrete-time lattices.** Moorcroft et al., arXiv:2511.08355 (abstract only, helper), argue that discrete-time lattices with weak nonlinearity relax to infinite temperature. A fibre-loop mesh then realizes a different (Floquet) problem, a point the card already makes.
- **Multicore fibres** with 7–19 cores are far from a thermodynamic chain.

At most, a single-breather exchange law at moderate $\gamma P_b/J$ could be tested.

### (f) Fit with the repository

The oracle is missing, but a symplectic DNLS integrator is small. Rare-event statistics need long runs and little memory. There is no overlap with existing cards.

**Changes made on the card:**
- novelty_confidence high → medium (status stays candidate);
- audited_by [gpt] → [gpt, claude], following earlier cards where the second family reviewed without auditing;
- last_audited 2026-10-20;
- a marked second-family subsection (the 2019 and 2017 predictions, the 2017 open statement, additional neighbours, platform numbers, sharper first target);
- the card's "high provisional novelty" sentence marked as superseded;
- an audit-trail row.

## P-20261020-gpt-g-03: asymptotic spreading versus arrest in the local-Kerr nonlinear Anderson chain

**Verdict: open, and high novelty is defensible for a controlled or rigorous result on the standard model. Set to `audited` (audited_by gpt, claude).** Three caveats go on the card:
- a heuristic sub-power law in the card's regime is not new (Basko 2011);
- the rigorous route has a known obstacle and a likely competitor;
- the optical lab cannot reach the asymptotic question.

### (a) Longstanding evidence

The card's three quotations are verbatim and its description of De Roeck, Huveneers and Prośniak (2024) is accurate; I checked each in the arXiv full text:
- Pikovsky and Shepelyansky (2008);
- Fishman, Krivolapov and Soffer (2012), Sec. 5.1, item (i);
- De Roeck, Huveneers and Prośniak (2024): a KG equilibrium-decorrelation theorem, with the warning that numerics may not reach the long-time behaviour;
- De Roeck, Giacomin, Hannani and Huveneers (arXiv:2502.02344v1, the only arXiv version; Nonlinearity 39, 045002 (2026), confirmed in Crossref).

The question has been open since at least 2008. As of 2026 it is contested four ways:
- numerical power laws (Flach and coworkers);
- a derived sub-power law (Basko 2011);
- a threshold scenario (Milovanov and Iomin);
- arrest (Aubry 2023, arXiv:2212.05771; full text read by helper .23.3, abstract by me).

### (b) Kill search

Not killed. Helper .23.3 ran:
- OpenAlex forward-citation screens since 2023 of nine anchor papers;
- arXiv author queries for Huveneers, Hannani, Giacomin, De Roeck and Prośniak;
- keyword queries.

Neither the helper nor I found a result for the chain with linear hopping $J>0$ as $t\to\infty$. The closest work:
- **De Roeck, Giacomin, Hannani and Huveneers (2026).** Theorem 1: almost surely, $M(t)\ge e^{-2(\ln t)^{3/4}}$ for $t\ge t^*$, for any finite energy.
  - Model: on-site harmonic disorder with *purely quartic* nearest-neighbour coupling. This is the atomic limit: the harmonic (linear) hopping is switched off. The DNLS version (Remark 2) has $H=\sum\omega_x|\psi_x|^2+\tfrac g4|\psi_x-\psi_{x+1}|^4$.
  - Their light-cone Lemma 1 uses an energy current bounded by $C(H_{x-1}^2+H_x^2)$. That bound has no analogue when the hopping is linear.
  - The authors write that they are "confident that this approach extends to a broader class" of systems and leave it for future work. OpenAlex lists no citing work yet (helper).
- **De Roeck, Huveneers and Prośniak, CMP 406, 155 (2025), arXiv:2308.11243** (full text, passage read by me). It controls KG equilibrium decorrelation beyond the atomic limit.
  - It states that the approach "would thus not have worked if we had considered the nonlinear Schrödinger equation".
  - The reason: DNLS small denominators are combinations of Anderson eigenvalues, whose correlations are not controlled beyond pairs.
  - This is the decisive evidence that a rigorous linear-hopping result is not a modest adaptation. It is not on gpt-g's card.
- **Cong, Shi and Zhang, J. Stat. Phys. (2021), arXiv:2006.04332**, with Cong, Shi and Wu (2024) for $\mathbb Z^d$ (helper .23.3, theorem statement; abstract read by me). These are the only rigorous results for the linear-hopping DNLS itself: localization with probability close to 1, for small hopping and small nonlinearity, up to finite times super-polynomial in $1/\varepsilon$. They say nothing about $t\to\infty$. Not on gpt-g's card.
- **Basko, Ann. Phys. 326, 1577 (2011)**, Eq. (3.8) (full text, read by me). For the strongly disordered linear-hopping chain at small density, $L(t)\sim\exp\{[(\ln t)/C']^{1/3}\}$.
  - $C'$ is only bounded, and the exponent $p$ in his Eq. (3.6) is only bounded too ($1/2\le p\le3$).
  - gpt-g's card already records this and says re-deriving the form would not be novel. I agree.

### (c) Novelty if solved

High for:
- a rigorous bound on the standard chain, for example a sub-power lower bound on $p_{\max}$, which would rule out asymptotic power-law dilution;
- a controlled law;
- a decision between arrest and slow spreading.

All three would settle a question open for 18 years in mathematical physics and nonlinear waves. Medium for a heuristic derivation that reproduces Basko's form, unless it fixes his constants or decides arrest against spreading.

One point sharpens gpt-g's card, which says "Extending a bound mechanically is not the full target". On my reading, a sub-power bound on the maximum for the standard chain would by itself be a high-novelty result: it would contradict the numerical power laws as an asymptotic description. This agrees with gpt-g's review, which counts "a bound that rules out one of the competing asymptotes" as consequential. Two facts bear on how hard it is:
- De Roeck, Huveneers and Prośniak (2025) identify the obstacle;
- De Roeck et al. (2026) expect to extend their method, so this route has a competitor.

### (d) Foothold

The card's first target is the distribution of action-transfer times out of a resonant cluster, with backreaction. It refines Basko's programme. It is meaningful but probably not achievable in a session or two. Two sharper first targets, one for each route:
- **Rigorous route.** Quantify, for 1D Anderson eigenmodes within one localization volume, the probability that $|E_\nu+E_\mu-E_\kappa-E_\lambda|<\delta$. That probability is exactly the small-denominator correlation that De Roeck, Huveneers and Prośniak (2025) say blocks the NLS case. Then decide numerically whether a Minami-type bound is plausible for quadruples. This is session-scale, needs only exact diagonalization, and says whether the 2026 maximum bound can be lifted to linear hopping.
- **Physics route.** Compute Basko's undetermined $C'$ and $p$ (his Eq. (3.6)) for one disorder strength. That turns his functional form into a quantitative prediction for long-time numerics, for example nonlinear quantum-walk maps (Vakulchyk et al. 2019) or GPU DNLS runs.

### (e) Optical relevance and lab test

Weak for the asymptotic question, as the card concedes. Platform facts from helper .23.3:
- **Waveguide arrays.** Lahini et al. (2008) used 99 AlGaAs waveguides on 5 mm samples (full text, helper). The coupling length is not given, so the number of coupling lengths cannot be computed.
- **Fibre loops.** In Vatnik et al. (2017), experiment and theory agree up to 80–120 round trips on about 104 positions (linear, no Kerr). Helper .23.3 found no nonlinear disordered fibre-loop experiment.
- **Reach of experiments.** Vakulchyk et al. (2019) state that experiments cannot reach even a thousandth of their computational horizon.
- **Transverse-Anderson fibres.** The observed nonlinearity is thermal and nonlocal (Leonetti et al. 2014), so they do not realize this model.

A lab can test mechanism-level predictions, such as cluster-transfer statistics or density-resolved decorrelation, and nothing asymptotic. The problem sits at the edge of "optical thermalization": the spreading is driven by chaotic thermalization inside the packet, and optics is one of several platforms.

### (f) Fit with the repository

The oracle is a small dedicated integrator. Simulations cannot verify an asymptotic statement (De Roeck et al. 2024), so the sim-verified gate fits poorly. A rigorous bound would need a cross-family proof audit instead. No overlap with existing cards.

**Changes made on the card:** status candidate → audited; audited_by [gpt] → [gpt, claude]; last_audited 2026-10-20; novelty_confidence high, unchanged; a marked second-family subsection (the CMP 2025 NLS limitation, Cong–Shi–Zhang, Aubry 2023, platform numbers, the value of a maximum bound, sharper first targets); audit-trail row.

## Comparison with gpt-g's search

I read gpt-g's skipped card sections and its review only after the three Claude searches were complete. The two searches agree on the core literature of all three cards: each family independently located and read the decisive 2019–2026 papers. The verdicts differ only on -02.

### Found by the Claude search and not by gpt-g

**-01:**
- **Girotti, Grava, McLaughlin and Najnudel, arXiv:2411.17036.** A rigorous paper that does compute "correlation functions" of random fNLS soliton sets. It looks like a resolution until the ensemble is checked: the norming constants are deterministic, and the correlations are of the fluctuations about a deterministic limit.
- **Doyon's explicit Euler-scale formula for arbitrary local fields (2018).** Together with the observation that it gives nothing for the U(1)-charged field. gpt-g made the same distinction using Koch, Caux and Bastianello's density correlators.
- **The ballistic-fluctuation phase-correlation method of Del Vecchio Del Vecchio, Kormos, Doyon and Bastianello (PRL 131, 263401 (2023)).** A possible large-$s$ template, and why it does not apply directly.
- **A caveat on Agafontsev–Zakharov (2015).** Their low-$k$ $|k|^{-0.66}$ region may be a box-scale effect.

**-02:**
- **The explicit prediction of logarithmic coarsening in Iubini et al. (2019), with the 2017 mechanism behind it.** This is the basis of the novelty downgrade. gpt-g's table summarizes the 2019 paper as identifying exponentially slow exchange, but does not record the predicted law.
- **The 2017 sentence that the macroscopic relaxation law "is still open".** A stronger longstanding statement than Rumpf's.
- **The numbers of Iubini et al. (2013):** $N=4096$, up to $t\sim10^7$, no visible coarsening.
- **Further neighbours:**
  - Kalish, Fittipaldi de Castro and Benalcazar (arXiv:2512.07774);
  - Johansson and Aubry (2000) and Johansson (2001), on the vanishing lowest-order channels;
  - the rigorous metastability papers of Eckmann, Wayne, Cuneo and Caballero, and De Roeck and Huveneers (2015);
  - Gotti, Iubini and Politi (2021, 2024);
  - Hannani and Olla.
- **Platform numbers:**
  - Kirsch et al. 2025, about 2–3 coupling lengths;
  - Marques Muniz et al. 2019, about $100\times100$ sites;
  - Moorcroft et al. (arXiv:2511.08355) on discrete-time lattices relaxing to infinite temperature.

**-03:**
- **De Roeck, Huveneers and Prośniak (CMP 2025): their technique fails for NLS.** gpt-g read this paper's introduction and theorem but did not record the limitation. It is the main evidence that a rigorous linear-hopping result is not a modest adaptation.
- **Cong, Shi and Zhang (2021) and Cong, Shi and Wu (2024).** The only rigorous long-time localization results for the linear-hopping DNLS itself.
- **Aubry's (2023) arrest conjecture.**
- **Recent numerics:**
  - Cheong et al., Chaos (2026);
  - Many Manda et al. (2023);
  - Kati, Yu and Flach (2020).
- **Platform numbers:**
  - Lahini 2008: 99 sites, 5 mm;
  - Vatnik 2017: agreement up to 80–120 round trips;
  - Vakulchyk 2019: experiments reach less than a thousandth of the computational horizon;
  - Leonetti 2014: thermal, nonlocal nonlinearity in transverse-Anderson fibres.

### Found by gpt-g and not by the Claude search

**-01:**
- Sun, Yu and Feng (2025), periodic-box nonlinear spectra; abstract only for both families, and a PI download task exists (T-20261020-gpt-g-02).
- Saha and Dubessy (2025).
- Grava et al. (arXiv:2606.08321), elliptic-background inverse scattering.
- Ballew, Bilman and Trogdon (2025), KdV primitive potentials.
- The October 2026 v2 revision of Charnay et al.
- Full-text reading of Koch, Caux and Bastianello (Claude: abstract only).
- The photonic GGE paper (arXiv:2503.16526) was found by both.

**-02:**
- Rumpf (2008).
- Das et al. (2026), dephasing-induced relaxation.
- Kabat et al. (2026), optical nonideal Rayleigh–Jeans thermodynamics.
- Full texts of Onorato et al. (2022), Ebrahimi, Drossel and Just (2025) and Kati et al. (2026), where the Claude helper had abstracts.
- gpt-g also flagged Rumpf 2007/2009 and the Science 2023 paper as PI downloads.

**-03:**
- Full texts of Flach, Krimer and Skokos (2009) with its erratum, Mafi and Ballato (2021), and Milovanov and Iomin (2025) (Claude: abstracts).
- The Laptyeva, Ivanchenko and Flach (2014) review.
- gpt-g's assessment of the self-screening section of Milovanov and Iomin (2025), which the Claude search did not audit.

None of the items found only by gpt-g changes a Claude verdict. None of the items found only by Claude kills a card; the 2019/2017 prediction lowers -02.

## Source ledger

**Read by me.** Access is mine.

| Source | DOI / arXiv | Access (by me unless marked) | Used for |
|---|---|---|---|
| Agafontsev & Zakharov, Nonlinearity 28, 2791 (2015) | [10.1088/0951-7715/28/8/2791](https://doi.org/10.1088/0951-7715/28/8/2791), arXiv:1409.4692v7 | full text (abstract and quoted passage) | -01 longstanding evidence; quote verified |
| Suret, Randoux, Gelash, Agafontsev, Doyon & El, PRE 109, 061001 (2024) | [10.1103/PhysRevE.109.061001](https://doi.org/10.1103/PhysRevE.109.061001), arXiv:2304.06541 | full text (open-questions passage) | -01 longstanding evidence; quote verified |
| Charnay, Escoubet, Copie, Randoux, Bonnemain, Bastianello & Suret, PRL 137, 097202 (2026) | arXiv:2601.21085 | full text (abstract, introduction, setup) | -01: GHD intensity (conserved-density) correlations; lab platform |
| Girotti, Grava, McLaughlin & Najnudel (2024), LLN and CLT for random sets of fNLS solitons | arXiv:2411.17036 | full text (abstract, introduction, Theorems 2.7–2.8 statements) | -01: rigorous correlations of fluctuations about a deterministic limit; different ensemble |
| Pelinovsky, Shurgalina, Sergeeva, Talipova, El & Grimshaw, Phys. Lett. A 377, 272 (2013) | [10.1016/j.physleta.2012.11.037](https://doi.org/10.1016/j.physleta.2012.11.037) | not accessed (Crossref metadata; repository unreachable from this machine) | -01: precedent for two-soliton "elementary act" statistics (moments, KdV) |
| Rumpf, PRE 69, 016618 (2004) | [10.1103/PhysRevE.69.016618](https://doi.org/10.1103/PhysRevE.69.016618), arXiv:nlin/0312058 | full text (quoted passage) | -02 longstanding evidence; quote verified |
| Iubini, Politi & Politi, J. Stat. Mech. (2017) 073201 | arXiv:1701.08636v2 | full text (abstract, Secs. 1, 4–5) | -02: stochastic surrogates; imposed amplitude-dependent coupling; exponential coupling gives logarithmic coarsening |
| Iubini, Chirondojan, Oppo, Politi & Politi, PRL 122, 084102 (2019) | [10.1103/PhysRevLett.122.084102](https://doi.org/10.1103/PhysRevLett.122.084102), arXiv:1811.05798v3 | full text | -02: deciding source for lowering novelty |
| Baldovin, Iubini, Livi & Vulpiani, Phys. Rep. 923, 1 (2021) | [10.1016/j.physrep.2021.03.007](https://doi.org/10.1016/j.physrep.2021.03.007), arXiv:2103.12572 | full text (DNLS dynamics section) | -02: open problems stated; logarithmic coarsening predicted without direct evidence |
| Iubini & Politi, Chaos Solitons Fractals 147, 110954 (2021) | [10.1016/j.chaos.2021.110954](https://doi.org/10.1016/j.chaos.2021.110954) | abstract only | -02: Lyapunov spectra with a breather; neighbouring |
| Politi, Politi & Iubini, J. Stat. Mech. (2022) 043206 | [10.1088/1742-5468/ac650e](https://doi.org/10.1088/1742-5468/ac650e), arXiv:2201.02529 | full text (quoted passage, Sec. 6) | -02 longstanding evidence; quote verified |
| Iubini & Politi, PRL 134, 097102 (2025) | [10.1103/PhysRevLett.134.097102](https://doi.org/10.1103/PhysRevLett.134.097102), arXiv:2406.15140 | full text | -02: open-setup metastable lifetime solved; multibreather generalization open; quote verified |
| Giachello, Iubini, Livi & Gradenigo, J. Stat. Mech. (2025) 113101 | [10.1088/1742-5468/ae17ab](https://doi.org/10.1088/1742-5468/ae17ab) (Crossref-checked), arXiv:2503.14364v2 | full text (abstract, App. B) | -02 longstanding evidence; statement verified |
| Giusfredi, Iubini, Politi & Politi, J. Stat. Mech. (2026) 053201 | [10.1088/1742-5468/ae625e](https://doi.org/10.1088/1742-5468/ae625e) (Crossref-checked), arXiv:2511.09206v3 | full text (abstract, introduction) | -02: mean-field metastable state; asymptotic state called effectively unachievable |
| Eckmann & Wayne, "Breathers as metastable states for the discrete NLS equation" (2018) | arXiv:1710.10999 | abstract only | -02: rigorous drift rate for a weakly damped few-site chain; building block |
| De Roeck & Huveneers, "Asymptotic localization of energy in non-disordered oscillator chains", CPAM (2015) | arXiv:1305.5127 | abstract only (search-engine summary) | -02: non-perturbative transport in DNLS-like chains; building block |
| De Roeck & Huveneers, "Glassy dynamics in strongly anharmonic chains of oscillators", C. R. Physique (2019) | [10.1016/j.crhy.2019.08.007](https://doi.org/10.1016/j.crhy.2019.08.007), arXiv:1904.07742 | abstract only | -02/-03: review of chaotic-spot transport near the atomic limit |
| Pikovsky & Shepelyansky, PRL 100, 094101 (2008) | [10.1103/PhysRevLett.100.094101](https://doi.org/10.1103/PhysRevLett.100.094101), arXiv:0708.3315 | full text (quoted passage) | -03 longstanding evidence; quote verified |
| Fishman, Krivolapov & Soffer, Nonlinearity 25, R53 (2012) | [10.1088/0951-7715/25/4/R53](https://doi.org/10.1088/0951-7715/25/4/R53), arXiv:1108.2956 | full text (Sec. 5.1 open problems) | -03 longstanding evidence; quote verified |
| De Roeck, Huveneers & Prośniak, PRE 109, 044207 (2024) | [10.1103/PhysRevE.109.044207](https://doi.org/10.1103/PhysRevE.109.044207), arXiv:2308.10572 | full text (abstract, introduction) | -03: KG decorrelation theorem; numerics may not reach asymptotics |
| Iubini, Franzosi, Livi, Oppo & Politi (2012 preprint of NJP 15, 023032 (2013)) | arXiv:1203.4162v1 | full text (passage and abstract) | -02: wording of the card's 2013 quotation |
| Aubry (2023); Cong, Shi & Zhang (2021); Moorcroft et al. (2025); Johansson (2001) | arXiv:2212.05771; arXiv:2006.04332; arXiv:2511.08355; nlin/0012064 | abstract only (me; helpers read the first two further) | -03 and -02 neighbours, as described |
| De Roeck, Giacomin, Hannani & Huveneers, Nonlinearity 39, 045002 (2026) | [10.1088/1361-6544/ae56ad](https://doi.org/10.1088/1361-6544/ae56ad) (Crossref-checked), arXiv:2502.02344v1 | full text of arXiv v1 (introduction, Sec. 2, Theorem 1, Remarks 1–2, Lemma 1) | -03: closest rigorous result; atomic-limit model only |
**Read by the helpers only.** These were located and read by a helper, with the access level that helper reported; I did not read them myself unless the table above says so.

| Source | DOI / arXiv | Access (helper) | Used for |
|---|---|---|---|
| El & Tovbis, PRE 101, 052207 (2020) | arXiv:1910.05732 | full text, keyword level (.23.1) | -01: averages of conserved densities only |
| Gelash & Agafontsev, PRE 98, 042210 (2018) | arXiv:1804.00652 | abstract only (.23.1) | -01: numerical spectra |
| Koch, Caux & Bastianello, J. Phys. A 55, 134001 (2022) | [10.1088/1751-8121/ac53c3](https://doi.org/10.1088/1751-8121/ac53c3), arXiv:2110.14574 | abstract only (.23.1) | -01: GHD of the attractive classical NLS |
| Del Vecchio Del Vecchio, Bastianello, De Luca & Mussardo, SciPost Phys. 9, 002 (2020) | arXiv:2002.01423 | abstract only (.23.1) | -01: defocusing GGE one-point functions |
| Del Vecchio Del Vecchio, Kormos, Doyon & Bastianello, PRL 131, 263401 (2023) | arXiv:2305.10495 | abstract only (.23.1) | -01: ballistic phase correlations (sine-Gordon) |
| Doyon, SciPost Phys. 5, 054 (2018) | arXiv:1711.04568 | abstract only (me) | -01: Euler-scale correlations of local fields |
| Gkogkou, Mazzuca & McLaughlin, J. Nonlinear Waves (2025) | arXiv:2502.14749 | abstract only (.23.1) | -01: deterministic elliptic-wave limit |
| Schmidt, Erne, Nowak, Sexty & Gasenzer, NJP 14, 075005 (2012) | arXiv:1203.3651 | abstract only (.23.1) | -01: dark-soliton (defocusing) momentum spectra; neighbouring |
| Iubini, Franzosi, Livi, Oppo & Politi, NJP 15, 023032 (2013) | arXiv:1203.4162 | full text (.23.2) | -02: isolated-chain numerics, no visible coarsening |
| Iubini, Politi & Politi, J. Stat. Phys. 154, 1057 (2014) | arXiv:1308.4870 | full text (.23.2) | -02: stochastic coarsening baseline |
| Gotti, Iubini & Politi, PRE 103, 052133 (2021); Fluct. Noise Lett. (2024) | arXiv:2010.11138; arXiv:2301.07546 | abstract only; full text (.23.2) | -02: finite-size thresholds; stochastic coarsening |
| Giusfredi, Iubini, Politi & Politi, J. Stat. Mech. (2025) 053203 | arXiv:2503.04461 | abstract only (.23.2) | -02: $N_b\sim\sqrt{\ln t}$ in a stochastic model with baths |
| Gradenigo, Iubini, Livi & Majumdar, J. Stat. Mech. (2021) 023201 | arXiv:1910.07461 | abstract only (.23.2) | -02: equilibrium condensation, finite-size strip |
| Mithun, Kati, Danieli & Flach, PRL 120, 184101 (2018) | arXiv:1712.03375 | abstract only (.23.2) | -02: weakly nonergodic dynamics |
| Kalish, Fittipaldi de Castro & Benalcazar (2025) | arXiv:2512.07774 | full text (.23.2); abstract (me) | -02: numerical order parameter for nonergodicity |
| Archilla, Bajārs & Flach, Physica D 473, 134551 (2025) | arXiv:2411.06044 | abstract only (.23.2) | -02: breather lifetimes in thermal backgrounds |
| Ebrahimi, Drossel & Just (2025, 2026) | arXiv:2504.12130; arXiv:2512.01448 | abstract only (.23.2) | -02: bath-coupled stochastic DNLS |
| Hannani & Olla | arXiv:2109.01389 | abstract only (.23.2) | -02: rigorous, stochastically perturbed chain |
| Onorato et al., PRE 105, 014206 (2022) | arXiv:2012.10618 | abstract only (.23.2) | -02: weak-wave negative-temperature kinetics |
| Johansson & Aubry, PRE 61, 5864 (2000); Johansson, PRE 63, 037601 (2001) | nlin/0002016; nlin/0012064 | abstract only (.23.2) | -02: lowest-order breather–phonon channels vanish |
| Eckmann & Wayne, CMP (2020); Cuneo, Eckmann & Wayne, Nonlinearity 30 (2017); Caballero & Wayne (2021) | arXiv:1907.12632; arXiv:1702.06464; arXiv:2101.10999 | abstract only (.23.2) | -02: rigorous metastability with dissipation |
| Kirsch et al., Nat. Phys. (2025) | [10.1038/s41567-024-02736-1](https://doi.org/10.1038/s41567-024-02736-1) | full text (.23.2) | -02: waveguide-array platform numbers |
| Marques Muniz et al., Sci. Rep. (2019) | [10.1038/s41598-019-46060-8](https://doi.org/10.1038/s41598-019-46060-8) | full text, PMC (.23.2) | -02: fibre-loop mesh platform numbers |
| Marques Muniz et al., Science 379, 1019 (2023) | [10.1126/science.ade6523](https://doi.org/10.1126/science.ade6523) | abstract only (.23.2; science.org returned 403, not bypassed) | -02: negative optical temperature platform |
| Moorcroft et al. (2025) | arXiv:2511.08355 | abstract only (.23.2) | -02: discrete-time lattices relax to infinite temperature |
| Cong, Shi & Zhang, J. Stat. Phys. (2021); Cong, Shi & Wu, J. Stat. Phys. (2024) | [10.1007/s10955-020-02677-y](https://doi.org/10.1007/s10955-020-02677-y), arXiv:2006.04332; [10.1007/s10955-024-03333-5](https://doi.org/10.1007/s10955-024-03333-5) | theorem statement; metadata only (.23.3) | -03: finite-time rigorous localization with linear hopping |
| De Roeck, Huveneers & Prośniak, CMP 406, 155 (2025) | [10.1007/s00220-025-05336-z](https://doi.org/10.1007/s00220-025-05336-z) (Crossref-checked), arXiv:2308.11243 | full text (.23.3); quoted passage read by me | -03: technique fails for NLS |
| Basko, Ann. Phys. 326, 1577 (2011) | [10.1016/j.aop.2011.02.004](https://doi.org/10.1016/j.aop.2011.02.004), arXiv:1005.5033 | full text, Sec. 3 (me; Eqs. 3.6–3.8) | -03: derived sub-power law |
| Aubry, Springer Proc. Complexity (2023) | [10.1007/978-3-031-37404-3_1](https://doi.org/10.1007/978-3-031-37404-3_1), arXiv:2212.05771 | full text (.23.3); abstract (me) | -03: arrest conjecture |
| Vakulchyk, Fistul & Flach, PRL 122, 040501 (2019) | arXiv:1806.06345 | abstract only (.23.3) | -03: long-time map numerics; experiments' reach |
| Lahini et al., PRL 100, 013906 (2008) | arXiv:0704.3788 | full text (.23.3) | -03: waveguide-array platform numbers |
| Vatnik et al., Sci. Rep. 7, 4301 (2017) | [10.1038/s41598-017-04059-z](https://doi.org/10.1038/s41598-017-04059-z) | full text, Europe PMC (.23.3) | -03: fibre-loop platform numbers |
| Leonetti, Karbasi, Mafi & Conti, PRL 112, 193902 (2014) | arXiv:1407.7990 | abstract only (.23.3) | -03: thermal nonlocal nonlinearity in TAL fibres |
| Cheong et al., Chaos (2026); Many Manda et al., PRB 107, 184313 (2023); Kati, Yu & Flach, SciPost Phys. Core 3, 006 (2020) | [10.1063/5.0310475](https://doi.org/10.1063/5.0310475); arXiv:2212.06235; arXiv:2006.06286 | abstract only (.23.3) | -03: recent numerics |
| Ivanchenko, Laptyeva & Flach, PRL 107, 240602 (2011); Milovanov & Iomin (2012, 2014, 2025) | arXiv:1108.0899; arXiv:1203.3981; arXiv:1406.0665; [10.1103/svxt-wsk7](https://doi.org/10.1103/svxt-wsk7) | abstract only (.23.3) | -03: competing scenarios |

The helpers' full tables (about 100 entries, including sources judged irrelevant) are summarized in the search log below. Sources the helpers could not locate were not cited.

## Search log

All searches ran on 2026-10-20, between 16:58 and 17:25 EDT, before any of gpt-g's kill-search material was read.

**Mine (claude-interactive.23).**
- Downloaded and keyword-searched arXiv full texts (PyMuPDF), to verify quotations and theorem scope: 1409.4692, 2304.06541, nlin/0312058, 2201.02529, 2406.15140, 2103.12572, 2503.14364v2, 2511.09206, 1701.08636, 1811.05798, 0708.3315, 1108.2956, 2308.10572, 2502.02344, 2307.08884, 2605.06306, 2411.17036, 2601.21085, 2411.06922, 1005.5033, 2308.11243.
- Web searches (standard mode):
  - "Pelinovsky Shurgalina two-soliton interaction elementary act of soliton turbulence moments";
  - "Eckmann Wayne Breathers as metastable states for the discrete NLS equation";
  - "De Roeck Huveneers Asymptotic localization of energy in non-disordered oscillator chains";
  - "Iubini 2019 J. Stat. Mech. 094016 discrete nonlinear Schrödinger breathers";
  - "Gotti Iubini Politi Physical Review E 106 054158 2022";
  - "arXiv Iubini Chirondojan Oppo Politi Politi Dynamical freezing of relaxation to equilibrium".
- arXiv abstract pages: 1904.07742, 1710.10999, 2103.11041, 2502.02344, 1711.04568, 2512.07774.
- Crossref API checks of 18 DOIs, all resolved. Semantic Scholar API for the Pelinovsky et al. (2013) record. The open-access copy at nrl.northumbria.ac.uk was unreachable from this machine.

**Helper claude-interactive.23.1 (card -01), about 17 minutes.**
- About 25 web queries on:
  - first-order coherence;
  - GGE $g_1$ for classical and Lieb–Liniger gases;
  - ballistic-fluctuation phase correlations;
  - the analytic long-time MI spectrum;
  - random multisoliton and finite-gap spectra.
- Not done: Google Scholar.

**Helper claude-interactive.23.2 (card -02), about 19 minutes.**
- arXiv API: all of Iubini's 2012–2026 entries; about 30 identifier lookups; keyword queries on DNLS breathers with coarsening, condensation or relaxation, and on negative optical temperature.
- Semantic Scholar forward citations (2021–2026) of Mithun et al. 2018, Iubini et al. 2019, Iubini et al. 2013 and Rasmussen et al. 2000.
- OpenAlex lookups; the Flach group's preprint list.
- About 20 web queries on: logarithmic breather coarsening; non-Gibbs ergodization times; condensation and first-passage times; rigorous DNLS dynamics; breather–background kinetic theory; ZRP coarsening; Rumpf; optical thermodynamics platforms.
- Blocked and not circumvented: science.org (403) and HAL (bot check).

**Helper claude-interactive.23.3 (card -03), about 16 minutes.**
- arXiv abstract and HTML pages; arXiv API author queries for Huveneers, Hannani, Giacomin, De Roeck and Prośniak. No 2025–2026 follow-up of arXiv:2502.02344 to linear hopping was found; OpenAlex lists no citing work of it.
- arXiv keyword queries since 2018 and 2023.
- OpenAlex citing works since 2023 of nine anchors: Flach–Krimer–Skokos 2009, Pikovsky–Shepelyansky 2008, Kopidakis 2008, Laptyeva 2010, Fishman–Krivolapov–Soffer 2012, Basko 2011 and 2014, Cong–Shi–Zhang 2021, De Roeck–Huveneers–Prośniak 2024.
- Europe PMC for Vatnik et al.; an author-hosted PDF of Schwartz et al. 2007.
- Semantic Scholar was rate-limited and not used.

All three helpers worked from the web only and opened no repository file. Downloaded open-access PDFs are in `~/analytical-nl-discovery-data/lit-T-20261020-claude-interactive-05/` and are not committed.

## Tasks created

| Task | Card | Purpose |
|---|---|---|
| [T-20261020-claude-interactive.23-03](../tasks/T-20261020-claude-interactive.23-03-small-denominator-statistics-of-quadrupl.md) | -03 | Small-denominator statistics of quadruples of Anderson eigenvalues, the obstacle to a rigorous linear-hopping bound (explore, p3) |
| [T-20261020-claude-interactive.23-04](../tasks/T-20261020-claude-interactive.23-04-fix-basko-s-undetermined-constants-c-and.md) | -03 | Fix Basko's constants $C'$ and $p$ (derive, p4) |
| [T-20261020-claude-interactive.23-05](../tasks/T-20261020-claude-interactive.23-05-pi-decision-on-p-20261020-gpt-g-02-famil.md) | -02 | PI decision: the families disagree on novelty (human, p2) |
| [T-20261020-claude-interactive.23-06](../tasks/T-20261020-claude-interactive.23-06-close-access-gaps-left-by-the-cross-fami.md) | all | Close the remaining access gaps: Pelinovsky 2013 full text; the published wording of the Iubini 2013 quotation; the Gradenigo strip width in the original; full theorem scopes of Cong–Shi–Zhang and Aubry 2023 (literature, p4) |

gpt-g's existing tasks are not duplicated. These are the PI downloads of Sun 2025, Rumpf 2007/2009 and the Science 2023 paper (T-20261020-gpt-g-02 to -05), and the planning task T-20261020-gpt-g-06.

