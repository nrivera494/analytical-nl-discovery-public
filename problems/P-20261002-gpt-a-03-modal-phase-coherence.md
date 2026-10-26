---
id: P-20261002-gpt-a-03
title: "Modal phase coherence beyond occupation-only beam thermalization"
status: audited
priority: 3
literature_state: partial
novelty_confidence: low
target_quantity: "A finite-length law for low-order modal coherence and its response to phase perturbations and disorder, alongside the modal power distribution."
model: "Passive multimode Kerr propagation with measured modal overlaps and specified random coupling; begin without gain, Raman or soliton formation."
oracle_ready: available
last_audited: 2026-10-04
audited_by: [gpt, claude]
updated_by: claude-b
updated_model: claude-opus-5-5
updated_family: claude
proposed_by: gpt-a
agent: gpt-a
agent_model: unknown
family: gpt
claims: []
results: []
---

## Target quantity

A reduced evolution or response law for off-diagonal modal coherence, together with modal occupations, under a stated averaging protocol. Predict coherence length or response to a calibrated relative-phase perturbation as launch statistics and disorder change. Report the validity domain through nonlinear/disorder/mode-beating lengths and temporal coherence/walk-off ratios.

Distinguish a reproducible phase in one coherent launch, phase memory across repeated launches, and ensemble-averaged coherence. They are different observables. A disorder realization held fixed throughout an experiment is not equivalent to disorder resampled between shots.

## Signal of hidden simplicity

Holographic experiments observe low-order modal phases accompanying a self-cleaned beam whose powers resemble an equilibrium distribution. A small number of phases account for much of the observed beam quality. This suggests a reduced coherence description, but does not establish universal attraction or spontaneous coherence generation from arbitrary incoherent inputs.

## Literature state

- Mangini et al., *Modal phase-locking in multimode nonlinear optical fibers*, DOI [10.1364/OL.494543](https://doi.org/10.1364/OL.494543) — **full text**, model, phase inference and experiment read. Gives a phase-locking argument under weak nonlinearity and an assumption identifying ensemble-averaged amplitudes with a reproducible realization. A low-mode numerical phase optimization matches the observed spatial profile. It does not calculate a disorder-dependent phase-response rate or generally establish that stationary average occupations imply stationary phases in every realization.
- Ferraro et al., *Wave turbulence, thermalization and multimode locking in optical fibers*, DOI [10.1016/j.physd.2025.134758](https://doi.org/10.1016/j.physd.2025.134758), arXiv:2505.11299 — **full text**, kinetic and phase-locking sections read. Existing population kinetics treats disorder-assisted thermalization; the coherence observations motivate extending that description.
- *Irreversible thermalization vs reversible dynamics mediated by anomalous correlators*, [arXiv:2512.17777](https://arxiv.org/abs/2512.17777) — **full text**, correlator equations and conclusion read. Derives reversible phase-correlation dynamics and an instability criterion for coupled polarization waves. It is a concrete counterexample to assuming occupations always close, but is not a many-spatial-mode coherence law for this experiment.

Searches: `modal phase-locking multimode nonlinear optical fibers`, `modal phase-locking disorder kinetic`, `multimode coherence phase-locking kinetic`, and forward references through the 2025 review and anomalous-correlator work. No controlled finite-length phase-response/disorder crossover for the stated spatial experiment was located. The existing phase argument must be tested, not ignored.

Added in the claude-b review (2026-10-04, T-20261002-gpt-a-05). Helper claude-b.9 or claude-b.10 found these; claude-b checked every DOI against Crossref or the arXiv record. The access levels are the helper's unless marked claude-b. OpenAlex and Semantic Scholar search hit quotas, so forward-citation coverage used Semantic Scholar citation lists, which are incomplete.
- **An explicit coherence law exists, but only in the disorder-dominated regime:** Garnier, Fusaro, Baudin, Michel, Krupa, Millot & Picozzi, PRA 100, 053835 (2019), DOI [10.1103/PhysRevA.100.053835](https://doi.org/10.1103/PhysRevA.100.053835), [arXiv:2011.03918](https://arxiv.org/abs/2011.03918). **Full text, passage read by claude-b**; Fusaro et al., PRL 122, 123902 (2019), DOI [10.1103/PhysRevLett.122.123902](https://doi.org/10.1103/PhysRevLett.122.123902), is the companion.
  - With weak disorder of strength $\Delta\beta$, correlations between different modes ($p\neq q$), and within a mode, take the slaved form $\sim\gamma G_{pq}/(4\Delta\beta-i(\beta_p-\beta_q))$. For $L_d\ll L_{nl}$ they vanish beyond the nonlinear length.
  - The beam partly repolarizes as the condensate forms.
  - This is a reduced, disorder-averaged coherence law, but in the decoherence regime, the opposite of locking.
- **Kinetics with phase (anomalous) correlators, for two waves only:**
  - Guasoni et al., PRX 7, 011025 (2017), DOI [10.1103/PhysRevX.7.011025](https://doi.org/10.1103/PhysRevX.7.011025): incoherent Fermi–Pasta–Ulam recurrences and thermalization mediated by strong phase correlations between two walking-off waves;
  - Picozzi, Opt. Express 16, 17171 (2008), DOI [10.1364/OE.16.017171](https://doi.org/10.1364/OE.16.017171): spontaneous repolarization through thermalization;
  - the anomalous-correlator paper already on this card, now published as Torres et al., PRL 136, 173801 (2026), DOI [10.1103/tgtw-qnyq](https://doi.org/10.1103/tgtw-qnyq).
  - **Abstract only** for the first two.
- **Attractor theory, the two-component and counterpropagating analogue:**
  - Pitois, Picozzi, Millot & Jauslin, EPL 70, 88 (2005), DOI [10.1209/epl/i2004-10469-9](https://doi.org/10.1209/epl/i2004-10469-9): polarization and modal attractors;
  - Guasoni, Kozlov & Wabnitz, JOSA B 29, 2710 (2012), DOI [10.1364/JOSAB.29.002710](https://doi.org/10.1364/JOSAB.29.002710): polarization attraction, including the degradation rate from random birefringence;
  - Turitsyn & Wabnitz, Opt. Commun. 307, 62 (2013), DOI [10.1016/j.optcom.2013.05.061](https://doi.org/10.1016/j.optcom.2013.05.061): stability of the attractors;
  - Ji et al., Nat. Commun. 14, 7704 (2023), DOI [10.1038/s41467-023-42869-0](https://doi.org/10.1038/s41467-023-42869-0): mode attraction and rejection in N-mode counterpropagating Kerr systems.
  - **Abstract only.**
- **Linear random-coupling baselines:**
  - Mecozzi, Antonelli & Shtaif, Opt. Express 20, 11673 (2012), DOI [10.1364/OE.20.011673](https://doi.org/10.1364/OE.20.011673): strong coupling inside a degenerate group gives a Manakov-type equation in which relative phases inside the group drop out;
  - Ho & Kahn, J. Lightwave Technol. 29, 3119 (2011), DOI [10.1109/JLT.2011.2165316](https://doi.org/10.1109/JLT.2011.2165316);
  - Xiao, Essiambre et al., Opt. Express 22, 32039 (2014), DOI [10.1364/OE.22.032039](https://doi.org/10.1364/OE.22.032039): random coupling lowers phase-sensitive intermodal four-wave mixing.
  - **Abstract only.**
- **Experiments on single-launch phases:**
  - Fabert et al., [arXiv:2005.11383](https://arxiv.org/abs/2005.11383): coherent combining of two self-cleaned beams gives stable fringes. The helper reports publication in Sci. Rep. 10, 20481 (2020); not verified.
  - Genty et al., Research Square preprint (2025), DOI [10.21203/rs.3.rs-7750730/v1](https://doi.org/10.21203/rs.3.rs-7750730/v1): single-shot holography of self-cleaning, which the authors describe as deterministic and coherent.
  - Chao, Fang & Yu, PRA 112, 063527 (2025), DOI [10.1103/k453-gplh](https://doi.org/10.1103/k453-gplh): random perturbations barely change the occupations; no phase observable.
  - **Abstract only.**

## Sharpest statement of the gap

Predict what phase/coherence measurements add beyond equilibrium-like powers, with launch memory and averaging explicitly separated. Recover the known reproducible-launch limit, then test its breakdown. P-005 concerns population kinetics and P-010 finite-pulse cleaning thresholds; this card concerns an independently measured coherence response. Merge the cards if one future closure proves to answer all three without a distinct prediction.

**Second-family review (claude-b, 2026-10-04): agreed, and narrowed.**
- **Known:**
  - the disorder-dominated limit, where intermodal coherence is slaved at order $\gamma/\Delta\beta$ and vanishes beyond $L_{nl}$ (Garnier et al. 2019);
  - kinetics with anomalous correlators, and attractor theory, for two-component or counterpropagating systems.
- **The open part:** the weak-disorder, locking regime of co-propagating self-cleaning:
  - a reduced law for low-order modal coherence;
  - its response to a calibrated relative-phase perturbation;
  - the crossover to the known decoherence limit as $\Delta\beta L_{nl}$ grows, with launch memory and ensemble averaging kept separate.
- **Distinctness.** The card is distinct from P-005 (population kinetics) and P-010 (time-averaged cleaning criterion). Keep it.

## Conjectures

None. A stable phase attractor is not assumed in a conservative propagation model.

## Oracle

Modal complex-field propagation is reported available; the external evaluator still needs connection under T-0003. The first cheap comparison would use launches with equal modal powers but different phases and the same disorder realization, followed by a specified ensemble average. Track complex coherence, not only near-field intensity or mode powers.

## Lab test

Program a weak phase perturbation between low-order modes while holding their powers fixed. Measure output modal amplitudes and relative phases holographically over a length/power scan, then repeat with controlled bending or launch randomization. Compare with the existing stationary phase optimization.

## Risks and must-reads

Apparent locking may be preservation of coherent launch memory rather than a new dynamical state. The low-order phase optimization already explains part of the observation, and may leave no useful independent law. A second-family review must compare coherent-wave, polarization-attraction and disorder-dephasing theories before derivation.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-02 | gpt-a (gpt; model unknown) | Added candidate, priority 3 | Measured modal phases plus an explicit ensemble/realization assumption in Mangini 2023; population kinetics and polarization correlator theory leave a narrower spatial coherence-response target |
| 2026-10-04 | claude-b (claude; claude-opus-5-5) | Second-family review (T-20261002-gpt-a-05). Agrees with gpt-a; narrows the open part to the weak-disorder locking regime, since the disorder-dominated decoherence law exists (Garnier et al. 2019); adds anomalous-correlator, attractor and random-coupling literature. candidate → audited; audited_by [gpt] → [gpt, claude]; priority 3, literature_state partial and novelty_confidence low unchanged | Garnier et al. 2019 passage read by claude-b; Crossref/arXiv-checked helper items. Log `log/2026-10-04_claude-b_T-20261002-gpt-a-05.md` |
