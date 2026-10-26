---
id: P-20261004-root-01
title: "Minimum noise under spectral filtering in normal dispersion"
status: candidate
priority: 2
literature_state: partial
novelty_confidence: low
target_quantity: "The minimum over input power of the Fano factor behind a fixed spectral bandpass, F_min, and the power P_min where it occurs, as functions of fiber length, pulse width, input chirp and filter edge, for LP01 and coherent LP01+LP02 launches in normally dispersive GRIN fiber — in particular where P_min sits on the classical transfer function (registered runs put the first dip at a fixed in-band fraction for one chirp and one filter, not at the plateau), the length at which a second, plateau-adjacent dip takes over, and the law of the excess-noise flank."
model: "Scalar, then two-mode, GNLSE with normal second-order dispersion over the occupied band, higher-order dispersion, Kerr, self-steepening and causal Raman response; linearized (Gaussian) quantum fluctuations with the matching Raman reservoir."
oracle_ready: partial
last_audited: 2026-10-04
audited_by: [claude]
proposed_by: /root
provenance:
  agent: /root
  model: unknown
  family: gpt
updated_by: claude-b
updated_model: claude-opus-5-5
updated_family: claude
claims: []
results: []
---

## Target quantity

**Readout $D$.** Direct detection of the fiber output after a fixed bandpass $[\omega_a,\omega_b]$, collecting all guided spatial modes unless a mode-resolved count is stated. Definitions of $n_D$ and $F_D=\operatorname{Var}(\hat n_D)/\langle \hat n_D\rangle$ are in the [shared scope](../docs/multimode-squeezing-scope.md).

At fixed fiber, launch and filter, $F_D$ against input power $P$ has a minimum. Derive:

1. **Where the minimum is on the classical transfer function.**
   - Classical baseline: the bright term $T_NG^2$ of the decomposition below vanishes where the transfer slope $G=d\ln n_D/d\ln N$ is zero. That is the plateau of the classical power transfer function, which the Mamyshev-regenerator literature has mapped in normalized variables (below).
   - What the registered map shows ("Length scaling" below), with the archive's chirp and filter:
     - The first dip is not just below the plateau. Over 0.4–2 m it sits at a fixed in-band fraction (0.966–0.974), at about 0.4 of the plateau-onset power.
     - The input chirp moves it at first order.
     - At 5 m a second, deeper dip nearer the plateau takes over as the global minimum.
   - What to derive: $P_{\min}$ as a function of $\zeta=L/L_D$, the soliton-number analogue $N^2=L_D/L_{NL}$, input chirp $C=\mathrm{GDD}/T_0^2$ and edge offset $\Omega_eT_0$ measured from the input spectrum. In particular:
     - why the first dip sits at a fixed in-band fraction, and how that fraction depends on $C$ and $\Omega_eT_0$;
     - at what $\zeta$ and $N$ the second dip takes over.
2. **How deep it is, and why it ends.** $F_{\min}$, through the exact decomposition $F=T_NG^2+F_{\rm shape}+F_{\rm phase}+F_{\rm partition}+F_R$ (archive: `research_runs/2026-09-26_analytics/report.md`). Derive the growth law of $F_{\rm shape}$ with $P$ beyond the minimum; this is the excess-noise flank.
3. **Coherent two-mode launch.** The shift of $P_{\min}$ and $F_{\min}$ for an LP01+LP02 launch with LP02 fraction $p_2$ and walk-off $w=\Delta\beta_1L/T_0$, using the overlap matrix in the shared scope. Also, which of the joint count and the mode-resolved counts reaches the lower $F$.
   - The joint count collects all modes. Since the modes are orthogonal, it is insensitive to noise in the relative intermodal phase, which is the mechanism Sloan et al. identify for spatially resolved detection.
   - Only spatially resolved, unsorted detection converts that phase noise into count noise.

An answer is a scaling law with derived exponents and prefactors, with its error measured against a stated small parameter. A fitted local form is not an answer.

## Signal of hidden simplicity

The figures below come from the archive (`~/Desktop/fall2026_research/ai driven lab work`). They are not registered runs; registering them is T-20261004-root-03.

- **Length scaling.** Unlike the other bullets, this one cites registered runs: `2026-10-04-claude-b.4-pmin-gate-1250`, `2026-10-04-claude-b.4-pmin-length-map` and `2026-10-04-claude-b.4-pmin-convergence` (claude-b.4, T-20261004-claude-interactive-03; details in `explorations/2026-10-04-claude-b.4-pmin-length.md`).
  - *Setting:* 1250 nm, LP01, GIF625, band 1226–1269 nm, input GDD −0.015 ps², oscillator Raman.
  - *Gate:* the archive's three minima are reproduced exactly: 178.3, 142.1 and 118.6 mW at 0.75, 1 and 1.25 m.
  - **The crossover picture fails at both ends over 0.25–5 m.** The picture was exponent 1 at fixed nonlinear phase for short $L$ and 0 for a frozen spectrum at long $L$.
    - The dip shallows and disappears as $L$ falls: $F_{\min}$ = 0.912 at 1 m, 0.950 at 0.6 m and 0.9915 at 0.4 m. At 0.25 m only a weak-power dip of depth 0.0013 remains.
    - This is caused by the assumed input chirp. With the GDD set to 0 (run `2026-10-04-claude-b.4-pmin-gdd0-check`), 0.25 m has a dip with $F=0.925$ at 78 mW, and 1 m one with $F=0.834$ at 43 mW. The unmeasured chirp is therefore a first-order parameter of $P_{\min}(L)$.
    - The local exponent of the first dip is 0.63 between 0.4 and 0.6 m, rises to 0.83 at 1.25–2 m, and is 0.80 between 3 and 5 m. The 3 m dip is flat, so the exponents next to it are poorly fixed.
    - The wave-breaking exponent 2 is not seen.
    - Only the classical plateau onset approaches exponent 0 at long $L$: 0.14 between 3 and 5 m.
  - **Over 0.4–2 m the first dip sits at a fixed point of the classical transfer function**, while $P_{\min}$ changes 3.4-fold:
    - in-band photon fraction 0.966–0.974;
    - $P_{\min}/P_{G025}$ = 0.39–0.41, where $P_{G025}$ is the first power with $G<0.25$;
    - $P_{\min}/P_{G0}$ = 0.32–0.38.

    The bright term is 0.79–0.85 there, and the shape term ends the dip (Raman gives 5–9% of the rising slope). So $P_{\min}$ is not "just below" the plateau: it tracks the plateau at about 0.4 of the onset power. This holds for one filter and one chirp; without chirp the in-band fraction at the dip is 0.94 at 0.25 m and 0.85 at 1 m. T-20261004-claude-b.4-04 tests the rule.
  - **At 5 m a second, deeper dip appears below the plateau:** $F=0.693$ at 114 mW, with $P/P_{G0}=0.74$ and bright term 0.31. Raman is what mainly ends it. The global $P_{\min}(L)$ therefore jumps branch between 3 and 5 m (T-20261004-claude-b.4-01).
  - *Raman model:* with the anisotropic response (same run) every statement above holds. At 0.4–2 m, $P_{\min}$ moves by 0.1–2% and $F_{\min}$ by 0.001–0.007, with $P_{\min}/P_{G025}$ = 0.39–0.41. The 5 m second dip becomes $F=0.780$ at 111 mW.
  - *Convergence:* tested at 0.25, 0.4 and 5 m. Halving the step and Raman spacing changes $F$ by less than $10^{-6}$, and halving the sample spacing changes nothing. Doubling the window changes $F$ by at most $1.1\times10^{-3}$ and $P_{\min}$ by at most 0.13%.
- **Composition of the flank** (`research_runs/2026-09-28_theory_campaign/REPORT.md`). At 1250 nm and 300 mW, $F\approx2.19$ splits into a bright term of 0.30, a Raman term of 0.084 and a shape term of 1.80. The flank is waveform noise, not Raman.
- **Weak-power limit** (`research_runs/2026-09-26_analytics/report.md`). The first-order (Born) slope $dF/dP$ at low power is predicted analytically. Its sign flips when the assumed −0.015 ps² input GDD is compensated (FG025LJA, 1200 nm). Prediction and full calculation agree to about 1%. This is a solved weak-power limit that a theory of the minimum must reproduce.

## Literature state

Reviewed by claude-b on 2026-10-04 (T-20261004-root-02). The earlier entries are by claude-interactive and /root, with access levels updated where claude-b read further.

**Quantum noise of filtered pulses, single mode:**
- König, Spälter, Shumay, Sizmann, Fauster & Leuchs, "Fibre-optic photon-number squeezing in the normal group-velocity dispersion regime," J. Mod. Opt. 45, 2425 (1998), DOI [10.1080/09500349808230495](https://doi.org/10.1080/09500349808230495). **Abstract only** (claude-b, OpenAlex).
  - Content: experimental photon-number squeezing by spectral filtering in normal dispersion. The filter function was optimized and the power dependence of the noise reduction measured. Best result 1.2 ± 0.2 dB (2.6 dB inferred for perfect detection).
  - So the existence of a filtered-noise minimum against power in normal dispersion is established experimentally.
  - It has 9 citing works in OpenAlex; none, by title, is a theory of the minimum's location.
- Nishizawa, Horio, Mori, Goto & Yamane, Jpn. J. Appl. Phys. 38, 1961 (1999), DOI [10.1143/JJAP.38.1961](https://doi.org/10.1143/JJAP.38.1961). **Abstract only**: the publisher's PDF link returned a bot-check page, which was not bypassed.
  - Content: numerical linearized quantum analysis of photon-number squeezing with fiber plus bandpass filter, in both time and frequency domains. It attributes filtered squeezing to the interaction of SPM and GVD.
- Nishizawa et al., Jpn. J. Appl. Phys. 39, 5842 (2000), DOI [10.1143/JJAP.39.5842](https://doi.org/10.1143/JJAP.39.5842): the same approach in anomalous dispersion. Noise against input power is periodic; 23 dB reduction of fiber-laser noise, slightly below shot noise. **Abstract only.**
- Takeoka, Fujishima & Kannari, OL 26, 1592 (2001), DOI [10.1364/OL.26.001592](https://doi.org/10.1364/OL.26.001592): adaptive spectral-phase pre-shaping to optimize filtered photon-number squeezing; more than −8 dB predicted for a sech input. **Abstract only.**
- Sizmann & Leuchs, "The optical Kerr effect and quantum optics in fibers," Prog. Opt. 39 (1999), DOI [10.1016/S0079-6638(08)70392-5](https://doi.org/10.1016/S0079-6638(08)70392-5). Review. **Not accessed** (no abstract in OpenAlex).
- Opatrný, Korolkova & Leuchs, [arXiv:quant-ph/0204131](https://arxiv.org/abs/quant-ph/0204131): few-mode description of pulse correlations. **Abstract only.**
- Uddin et al., "Noise-immune quantum correlations of intense light," Nat. Photon. 19, 751 (2025), DOI [10.1038/s41566-025-01677-2](https://doi.org/10.1038/s41566-025-01677-2); [arXiv:2311.05535](https://arxiv.org/abs/2311.05535). **Full text (arXiv v4)**, main text; the supplement was not read.
  - Content: 185 fs pulses in **anomalous**-dispersion single-mode fiber at 1560 nm, beyond the fundamental soliton (Raman soliton), with a programmable spectral filter. From an input 10 dB above shot noise they reach 4 dB below it. Low-noise filters sit on the red side of the Raman soliton and have gaps.
  - Method: "quantum sensitivity analysis", $(\Delta X)^2=\sum_iF_i|\partial X/\partial\alpha_i|^2$. Noise immunity comes from number-conserving four-wave mixing.
  - Not covered: normal dispersion, a fixed bandpass, or $P_{\min}(L)$.
- Rivera, Uddin, Sloan & Soljačić, Nanophotonics 14, 1857 (2025), DOI [10.1515/nanoph-2024-0634](https://doi.org/10.1515/nanoph-2024-0634): output-noise theory for nonlinear dynamics seeded by Gaussian states; supercontinuum seeded with squeezed vacuum. **Abstract only.**
- Ng, Yanagimoto, Jankowski, Fejer & Mabuchi, [arXiv:2307.05464](https://arxiv.org/abs/2307.05464): a self-consistent multimode Gaussian-state split-step method that goes beyond linearization. **Abstract only.** This is a possible second oracle for testing linearization near strong squeezing.

**Classical transfer function (SPM in normal dispersion plus offset filter, the Mamyshev regenerator):**
- Provost, Finot, Mukasa, Petropoulos & Richardson, "Design scaling rules for 2R-optical self-phase modulation-based regenerators," Opt. Express 15, 5100 (2007), DOI [10.1364/OE.15.005100](https://doi.org/10.1364/OE.15.005100). **Abstract only**: the HAL copy returned a bot check, which was not bypassed.
  - Content: a global design map in normalized variables for SPM in normal dispersion followed by an offset filter, identifying the operating conditions for optimum noise rejection (the transfer-function plateau).
  - Relevance: this is the classical counterpart of part 1. P-007 cites it too.
- Finot & Rochette, "From signal processing of telecommunication signals to high pulse energy lasers: the Mamyshev regenerator case," Nanophotonics (2025), DOI [10.1515/nanoph-2024-0712](https://doi.org/10.1515/nanoph-2024-0712). **Full text** (Europe PMC XML), keyword-scanned.
  - Content: the plateau of the transfer function needs normal dispersion. Design rules come from systematic simulations (Provost 2007; Striegler & Schmauss, JLT 24, 2835 (2006), not accessed). The regenerator's performance has been linked to optical wave breaking (Anderson, Desaix, Lisak & Quiroga-Teixeiro, JOSA B 9, 1358 (1992), not accessed).
  - Not covered: quantum noise or squeezing.
- Finot, Kibler, Provost & Wabnitz, JOSA B 25, 1938 (2008), DOI [10.1364/JOSAB.25.001938](https://doi.org/10.1364/JOSAB.25.001938): temporal and spectral role of wave breaking in normal-dispersion continuum formation. **Abstract only.**

**Multimode:**
- Sloan et al., [arXiv:2509.03482](https://arxiv.org/abs/2509.03482). **Full text** of the main paper (claude-b).
  - Content: wavefront shaping and spatial (pixel or DMD) filtering of a multimode fiber output give pixel noise 12 dB below linear attenuation, near shot noise. Simulations of the optimization are near-CW. The dominant excess-noise mechanism is input power noise converted into relative intermodal phase noise by SPM and XPM.
  - Not covered: spectral bandpass readout, an LP01+LP02 launch, and $P_{\min}$. It therefore **does not cover part 3** (see the note in the target).

**Searches** (claude-b, 2026-10-04):
- OpenAlex: "photon-number squeezing normal dispersion spectral filtering fiber", "amplitude squeezing self-phase modulation spectral filtering normal dispersion", "wave breaking normal dispersion fiber noise spectral filtering", "design scaling rules 2R self-phase modulation regenerators", "Mamyshev regenerator transfer function analytical".
- Forward citations of König et al. 1998 (9 works) and of Provost et al. 2007 (99 works, titles screened for noise, quantum or scaling).
- The searches by claude-interactive listed in the audit trail.

## Sharpest statement of the gap

**Known:**
- Normal-dispersion filtered photon-number squeezing, with a power-dependent minimum, has been measured (König et al. 1998) and computed numerically (Nishizawa et al. 1999).
- The classical transfer-function plateau of SPM followed by an offset filter, where the bright term $T_NG^2$ vanishes, has scaling rules in normalized variables, linked to wave breaking (Provost et al. 2007; Finot & Rochette 2025).

**Not found:**
- an analytical law for the quantum minimum $P_{\min}(L)$ and where it sits on the classical transfer function;
- the depth $F_{\min}$ set by the shape, phase and partition terms;
- the growth law of the excess-noise flank;
- any of these for a two-mode launch.

These statements report a bounded search; they do not prove absence.

**First test, run.** The review's first test was whether $P_{\min}$ tracks the classical plateau computed from the same model. It has been run for one chirp and one filter ("Length scaling" above).
- The first dip sits at a fixed in-band fraction, not at the plateau.
- That fraction is a classical quantity, but the rule changes when the assumed chirp is removed.
- The second dip at 5 m sits closer to the plateau.

So part 1 is not settled as purely classical, and neither the location rule nor the branch switch is derived.

**Related cards.**
- P-007: same regenerator physics, but in a closed oscillator.
- P-001: normal-dispersion noise of a passively expanding parabolic pulse. Beyond wave breaking, the pulse here can approach that regime.

## Conjectures

None registered.

## Oracle

The solver (`solver/`, FastDifferentiableMMNLO) and the archive's Julia scripts cover scalar and axisymmetric radial modes with linearized noise and a matched Raman reservoir.
- Registered: the 1250 nm LP01 gate and length map (runs under "Length scaling").
- Not registered: the archive's other runs, including the 1200 nm and two-mode ones (T-20261004-root-03).

Cheap tests:
- $P\to0$ gives $F=1$.
- The Born slope reproduces the archive's verified values.
- Collecting all frequencies with Raman off gives $F=1$, by photon conservation.
- The classical plateau power ($G=0$) and $P_{\min}$ come from the same runs; report their ratio against $L$. This is done for 0.25–5 m at 1250 nm, where the ratio is 0.32–0.38 at 0.4–2 m.

Convergence must be checked over time window, step and radial-mode count separately.

## Lab test

**Cut-back.** Use a fixed edge filter and a fixed launch.
- Measure the input chirp first, since the map shows it moves $P_{\min}$ at first order.
- Measure $P_{\min}$ and the classical transfer function (output power against input power behind the filter) at five or more lengths between 0.25 and 5 m.
- Compare with the registered map: the in-band fraction at the first dip, the ratio $P_{\min}/P_{G0}$, and the length at which the second dip takes over.
- Then scan the edge position and the input chirp at one length.

**Part 3.** Use mode-resolved counts (mode sorter or photonic lantern) for a 70/30 launch.

Plot output power (blue, left axis) and noise in dB (red, right axis) against input power.

## Risks and must-reads

- **The location may still be classical.** The first dip sits at a fixed in-band fraction, which is a classical quantity. If one classical variable fixes the dip across chirps and edges, part 1 is a regenerator design rule. Read the Provost et al. full text before deriving part 1 (T-20261004-claude-b-02 lists it with the other gated texts).
- **No simple law may exist.** Beyond wave breaking, $F_{\min}$ may depend on fine structure at the pulse edges.
- **The input chirp is an assumption, and it acts at first order.** The archive assumed −0.015 ps²; it was never measured. Setting it to 0 restores a dip at 0.25 m and moves the 1 m dip from 143 to 43 mW (run `2026-10-04-claude-b.4-pmin-gdd0-check`). Every prediction must carry the chirp as a parameter.
- **Raman model spread.** The two Raman response models differ by about 0.09 in $F$ at the best 1200 nm setting (0.655 against 0.747, same report). Any prediction of $F_{\min}$ must carry that model spread.
- **GAWBS floor.** GAWBS sets a floor in the detection RF band (see P-20261004-claude-interactive-02).

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-04 | /root (gpt) | Created as priority-2 candidate; literature unaudited | PI request; primary-source abstract intake; archived campaign read; independent review T-20261004-root-02 |
| 2026-10-04 | claude-interactive (claude; claude-opus-5-5) | Rewritten on PI instruction to one target, the minimum noise under spectral filtering in normal dispersion; unaudited → partial | PI's four-problem set in chat, 2026-10-04; archive length scaling and noise decomposition; targeted search ("photon-number squeezing normal group-velocity dispersion", "König Zielonka Sizmann normal dispersion squeezing", "photon-number squeezing multimode graded-index fiber spatial modes Kerr quantum noise spectral filtering", "Spatial noise dynamics in nonlinear multimode fibers"). Not a completed audit |
| 2026-10-04 | claude-b (claude; claude-opus-5-5) | Claude-family review (T-20261004-root-02). Added the classical Mamyshev-regenerator literature as the counterpart of part 1, with the target refocused on the offset of $P_{\min}$ from the transfer-function plateau. Sloan et al. read in full: it does not cover part 3. Added a third reference exponent (wave breaking, 2) and the fit-leverage caveat. Status, priority, literature_state (partial) and novelty_confidence (low) unchanged | Full texts: Uddin et al. (arXiv v4); Sloan et al.; Finot & Rochette 2025. Abstracts: König et al. 1998; Nishizawa et al. 1999/2000; Provost et al. 2007; Takeoka et al. 2001; Finot et al. 2008. Log `log/2026-10-04_claude-b_T-20261004-root-02.md` |
| 2026-10-04 | claude-b.4 (claude; claude-opus-5-5; subagent of claude-b) | "Length scaling" bullet replaced with registered runs. $P_{\min}(L)$ map at 0.25–5 m (T-20261004-claude-interactive-03): the crossover hypothesis fails at both ends; the first dip sits at a fixed in-band fraction over 0.4–2 m; a second dip below the plateau appears at 5 m; the dip's disappearance at short length is caused by the assumed input chirp. The next bullet's "(same report)" was spelled out, because the replaced bullet held that reference. No other section, and no status, changed | Runs `2026-10-04-claude-b.4-pmin-gate-1250`, `-pmin-length-map`, `-pmin-convergence`, `-pmin-gdd0-check`; `explorations/2026-10-04-claude-b.4-pmin-length.md`; log `log/2026-10-04_claude-b.4_T-20261004-claude-interactive-03.md` |
| 2026-10-04 | claude-b (claude; claude-opus-5-5) | Card brought in line with the registered $P_{\min}(L)$ map of T-20261004-claude-interactive-03. The "Length scaling" bullet, the flank bullet's reference and the claude-b.4 row above are copied verbatim from that task's branch. Target, part 1, gap statement, oracle, lab test and the chirp risk revised. The review's plateau hypothesis (first dip just below the plateau) is false in its strong form: the first dip sits at a fixed in-band fraction, at about 0.4 of the plateau-onset power, and the input chirp acts at first order. Status, priority, literature_state and novelty_confidence unchanged | Runs `2026-10-04-claude-b.4-pmin-gate-1250`, `2026-10-04-claude-b.4-pmin-length-map`, `2026-10-04-claude-b.4-pmin-convergence`, `2026-10-04-claude-b.4-pmin-gdd0-check`; `explorations/2026-10-04-claude-b.4-pmin-length.md` |
