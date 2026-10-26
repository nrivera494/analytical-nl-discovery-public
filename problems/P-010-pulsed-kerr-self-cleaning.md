---
id: P-010
title: "Finite-pulse and walk-off corrections to Kerr beam self-cleaning"
status: audited
priority: 4
literature_state: partial
novelty_confidence: low
target_quantity: "A finite-length cleaning criterion and detector-defined modal distribution versus pulse duration, bandwidth and modal walk-off."
model: "Passive multimode GNLSE in GRIN fiber, initially without Raman or gain; specify launch coherence and disorder."
oracle_ready: available
last_audited: 2026-10-04
audited_by: [gpt, claude]
proposed_by: claude-bootstrap
updated_by: claude-b
updated_model: claude-opus-5-5
updated_family: claude
claims: []
results: []
---

## Target quantity

Predict a specified core-mode energy fraction at a fixed fiber length and detector bandwidth/time gate, and the input power required to cross an agreed cleaning criterion. Give the crossover with pulse duration/modal-delay spread and nonlinear length/disorder length. A threshold without a length, launch distribution and measured observable is not well-defined.

## Signal of hidden simplicity

Bell-shaped output beams and equilibrium-like modal powers occur for pulses over very different durations. This motivates a crossover law, but does not establish that the entire pulse is monochromatic, temporally uniform or at equilibrium.

## Literature state

- Liu et al., *Kerr self-cleaning of femtosecond-pulsed beams in graded-index multimode fiber*, DOI [10.1364/OL.41.003675](https://doi.org/10.1364/OL.41.003675) — **abstract only**. Experimental femtosecond self-cleaning with agreement from nonlinear propagation simulations. Pulsed self-cleaning is not merely a hypothetical extension of CW theory.
- Mangini et al., *Statistical mechanics of beam self-cleaning in GRIN multimode optical fibers*, DOI [10.1364/OE.449187](https://doi.org/10.1364/OE.449187), arXiv:2111.08063 — **full text**, model, experiment and temporal/spectral discussion read. Derives equilibrium modal occupations under a monochromatic approximation and tests them using pulsed experiments. It does not derive the finite-length temporal approach to equilibrium or a walk-off-dependent threshold. Replace the seed assertion that pulsed observations are only empirically fitted with this more precise distinction.
- Ferraro et al., *Wave turbulence, thermalization and multimode locking in optical fibers*, [arXiv:2505.11299](https://arxiv.org/abs/2505.11299) — **full text**, kinetic limits and pulsed/phase-coherence sections read. Gives existing spatial kinetic descriptions and discusses the limits of a purely population-based picture.
- Zanaglia et al., *Spatio-temporal thermalization and adiabatic cooling of guided light waves*, DOI [10.1103/mqzh-w2gh](https://doi.org/10.1103/mqzh-w2gh), arXiv:2506.23536 — **full text**, main kinetic construction and regime read. A joint spatial/temporal kinetic theory now exists for statistically stationary incoherent waves. This prevents claiming joint space-frequency kinetics itself as the missing result; finite envelopes and launch walk-off remain distinct.

Searches: exact Liu and Mangini titles, `pulsed Kerr beam self cleaning temporal bandwidth walk off theory`, and forward developments through the 2025 review and 2026 spatiotemporal theory. No detector-defined finite-pulse crossover law was located in that search.

Added in the claude-b review (2026-10-04, T-20261002-gpt-a-04). Helper claude-b.7 found most of these; claude-b checked every DOI against Crossref and read the two quoted passages itself.
- Baudin, Garnier, Fusaro, Michel, Krupa, Millot & Picozzi, Opt. Commun. 545, 129716 (2023), DOI [10.1016/j.optcom.2023.129716](https://doi.org/10.1016/j.optcom.2023.129716), [arXiv:2309.02215](https://arxiv.org/abs/2309.02215). **Full text, conclusion passage read by claude-b.** The purely spatial model captures the 400 ps experiments, but "a quantitative description … would require a detailed analysis of the temporal averaging effect inherent to the pulsed regime". This states the card's gap explicitly.
- Zitelli, Laser Photonics Rev. 19, 2400714 (2024), DOI [10.1002/lpor.202400714](https://doi.org/10.1002/lpor.202400714), [arXiv:2404.00480](https://arxiv.org/abs/2404.00480). **Full text, passage read by claude-b.**
  - Chromatic dispersion is "the most detrimental effect" for the thermodynamic description. The pulse broadens beyond $L_D=T_0^2/\beta_2$, and the state-equation error can exceed 5%, so "fibre length is therefore limited to few meters".
  - This is the closest published criterion: qualitative, an empirical error metric, and no modal walk-off.
- Krupa et al., Nat. Photon. 11, 237 (2017), DOI [10.1038/nphoton.2017.32](https://doi.org/10.1038/nphoton.2017.32). **Abstract only** (claude-b); per the helper's reading of arXiv:1603.02972, quasi-CW is justified only by modal-dispersion broadening (about 12 ps) ≪ the 900 ps pulse.
- Podivilov et al., PRL 122, 103902 (2019), DOI [10.1103/PhysRevLett.122.103902](https://doi.org/10.1103/PhysRevLett.122.103902): an analytic threshold from an integrable three-mode model under the quasi-CW assumption. **Bibliographic record only** (claude-b); full text per helper.
- Garnier, Fusaro, Baudin, Michel, Krupa, Millot & Picozzi, PRA 100, 053835 (2019), DOI [10.1103/PhysRevA.100.053835](https://doi.org/10.1103/PhysRevA.100.053835): kinetic theory of condensation with weak disorder. Per the helper's full-text reading it is restricted to sub-nanosecond pulses with walk-off and dispersion neglected. **Bibliographic record only** (claude-b).
- Leventoux et al., OL 46, 66 (2021), DOI [10.1364/OL.411868](https://doi.org/10.1364/OL.411868): picosecond time-resolved 3D beam maps show nonlinear mode coupling within a single pulse; the bell-shaped beam is a time average. **Bibliographic record only.**
- Ferraro, Mangini, Zitelli & Wabnitz, "On spatial beam self-cleaning from the perspective of optical wave thermalization in multimode graded-index fibers," [arXiv:2304.12006](https://arxiv.org/abs/2304.12006). The helper reports publication in Adv. Phys. X (2023); the journal version was not verified. Per the helper's full-text reading, it argues that camera time-averaging replaces ensemble averaging, so fitted thermodynamic parameters should not depend on pulse duration, citing Mangini 2022 from 174 fs to 7.6 ps. **Not read by claude-b.**
- Pourbeyram et al., Nat. Phys. 18, 685 (2022), DOI [10.1038/s41567-022-01579-y](https://doi.org/10.1038/s41567-022-01579-y): thermalization to Rayleigh–Jeans with 200 fs pulses over 0.5–2.5 m. **Bibliographic record only** (claude-b); helper read the main text (no criterion).

## Sharpest statement of the gap

A finite-envelope, finite-length correction predicting when the established spatial equilibrium description is a useful approximation to what a detector measures. P-005 owns general kinetic closure; this card owns the experimentally operational self-cleaning criterion. Do not create separate claims for the same closure in both cards.

**Second-family review (claude-b, 2026-10-04): agreed.**
- The theory side is either spatial-only, with an explicit quasi-CW assumption (Podivilov 2019; Garnier 2019; Baudin 2023), or spatiotemporal for stationary incoherent waves (Zanaglia).
- The nearest operational statements are qualitative:
  - modal-dispersion broadening ≪ pulse width (Krupa 2017);
  - $L\lesssim$ a few $L_D$ from a state-equation error metric (Zitelli 2024);
  - duration independence of the fitted parameters (Ferraro, Mangini).
- Baudin et al. (2023) name the temporal-averaging analysis as what a quantitative description still needs.
- **The open quantity:** a derived criterion in $T_0$, $L_D$, the modal delay spread and $L_{NL}$, predicting when the time-integrated modal distribution matches the spatial equilibrium.

## Conjectures

None.

## Oracle

Modal propagation is reported available; actual evaluator integration is tracked separately. Test duration and walk-off scans at fixed spatial launch, including time-resolved and integrated modal diagnostics. Check mode truncation and temporal-window convergence before identifying a threshold.

## Lab test

Stretch a pulse while holding its spatial launch and chosen peak-power or energy control fixed and stated. Measure modal powers both spectrally resolved and integrated. A theory must predict which comparison changes the observed cleaning threshold.

## Risks and must-reads

Spatial equilibrium fits can hide temporal segregation. A clean near-field spot is not by itself a coherent single-mode pulse. Full-text comparison of the new joint kinetic theory against the chosen finite-envelope closure remains necessary before derivation.

**See also** (claude-interactive.22, 2026-10-20): [P-20261020-claude-interactive.22-01](P-20261020-claude-interactive.22-01-self-cleaning-threshold-length-law.md) owns the quasi-CW threshold–length law $P_c(L)$ and its mechanism; this card keeps the finite-pulse and walk-off corrections to it.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-01 | claude-bootstrap (claude) | Created as unaudited candidate | Additional-candidates list, literature audit Oct 2026 |
| 2026-10-02 | gpt-a (gpt; model unknown) | Retained candidate; unaudited → partial; narrowed target | Pulsed equilibrium tests and stationary joint kinetics already exist; residual finite-envelope/walk-off prediction is distinct |
| 2026-10-04 | claude-b (claude; claude-opus-5-5) | Second-family review (T-20261002-gpt-a-04). Agrees with gpt-a on what is open; adds quasi-CW theory papers, Zitelli's dispersion-length limit and Baudin's explicit statement of the temporal-averaging gap. candidate → audited; audited_by [gpt] → [gpt, claude]; priority 4, literature_state partial and novelty_confidence low unchanged | Baudin et al. 2023 and Zitelli 2024 full-text passages; Crossref records for the rest; helper claude-b.7 search. Log `log/2026-10-04_claude-b_T-20261002-gpt-a-04.md` |
