---
id: P-20261002-gpt-a-02
title: "Finite-window backscatter statistics near multimode Brillouin onset"
status: audited
priority: 4
literature_state: partial
novelty_confidence: low
target_quantity: "The probability of exceeding a specified reflected-energy fraction over a detector window, and its first depletion correction, for a known multimode launch."
model: "Forward signal/backward Stokes optical modes coupled to damped acoustic modes with distributed thermal Langevin forcing and specified input spectrum."
oracle_ready: missing
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

Predict a finite-window reflected-energy distribution, or a controlled tail approximation, and the input power corresponding to an agreed exceedance probability. Hold the modal launch and detector fixed initially. Include the first effect of signal depletion or competition between nearly equal-gain Stokes channels; the linear covariance baseline alone is not the intended new result.

Specify observation time/acoustic lifetime, optical transit/acoustic lifetime, source linewidth/Brillouin linewidth, modal gain splittings and depletion fraction. The first scope is narrowband power delivery in multimode fiber; broadband pump modulation and active gain are later extensions.

## Signal of hidden simplicity

Multimode excitation reproducibly suppresses SBS while preserving a focused output, and stochastic Brillouin fluctuations are independently well established. Existing vector coupled-mode theory reduces mean onset to a gain spectrum. This provides a concrete baseline for asking whether the same launch has the predicted finite-window fluctuation tail.

## Literature state

- Chen et al., *Mitigating stimulated Brillouin scattering in multimode fibers with focused output via wavefront shaping*, DOI [10.1038/s41467-023-42806-1](https://doi.org/10.1038/s41467-023-42806-1) — **abstract only**. Experimental multimode suppression and focused output; not a measurement of the proposed probability law.
- Wisal et al., *Theory of Stimulated Brillouin Scattering in Fibers for Highly Multimode Excitations*, DOI [10.1103/PhysRevX.14.031053](https://doi.org/10.1103/PhysRevX.14.031053) — **full text**, model assumptions and threshold section read. Derives vector optical/acoustic coupled modes and gain. Its threshold uses an effective seed power and the fastest growing Stokes mode; nearby gain channels give a correction. Signal depletion is neglected in that onset estimate. These are explicit limits to extend, not evidence that multimode SBS theory is absent.
- Wisal et al., *Optimal input excitations for suppressing nonlinear instabilities in multimode fibers*, DOI [10.1364/OPTICA.533712](https://doi.org/10.1364/OPTICA.533712) — **abstract only**. Linear programming already optimizes modal allocation for SBS and TMI, including mode-dependent gain/loss. Generic optimum launch allocation is therefore not a new problem.
- Boyd, Rzążewski and Narum, *Noise initiation of stimulated Brillouin scattering*, DOI [10.1103/PhysRevA.42.5514](https://doi.org/10.1103/PhysRevA.42.5514) — **full text**, all pages including the Appendix. Derives distributed-noise reflectivity and linewidth in the constant-pump limit; numerical depleted-pump dynamics depend on the acoustic-decay/transit-time ratio. Appendix Eq. (A5) already gives a reflectivity probability density for a localized fluctuating seed with saturation. Neither reflectivity statistics nor depletion-induced fluctuation suppression is new; a distributed multimode, finite-window correction is the narrower target.
- Jin et al., *A framework for spontaneous Brillouin noise: unveiling fundamental limits in Brillouin metrology*, DOI [10.1038/s41377-025-02115-2](https://doi.org/10.1038/s41377-025-02115-2), arXiv:2505.17651 — **full text**, introduction and spontaneous/stimulated regime comparison read. Gives analytical intensity-noise laws and experiments in the spontaneous regime. It does not replace a multimode near-onset depletion calculation. Correction [DOI:10.1038/s41377-026-02281-x](https://doi.org/10.1038/s41377-026-02281-x): **full text of the notice**, which replaces Figure 2 and states that the original article was updated; corrected figure data were not independently checked.

Searches: `multimode Brillouin statistics noise threshold`, `multimode Brillouin probability distribution`, `Brillouin multimode Langevin`, both Wisal titles, the spontaneous-noise framework's references, and Boyd's distributed/localized-source comparison. No finite-window multimode depletion-corrected exceedance law was located. Further single-mode stochastic SBS work may already supply much of the reduction.

Added in the claude-b review (2026-10-04, T-20261002-gpt-a-05). Helper claude-b.9 or claude-b.10 found these; claude-b checked every DOI against Crossref or the arXiv record. The access levels are the helper's unless marked claude-b. OpenAlex and Semantic Scholar search hit quotas, so forward-citation coverage used Semantic Scholar citation lists, which are incomplete.
- **Stochastic SBS has been simulated in many configurations; none gives a closed-form exceedance law with depletion:**
  - Gaeta & Boyd, PRA 44, 3205 (1991), DOI [10.1103/PhysRevA.44.3205](https://doi.org/10.1103/PhysRevA.44.3205): stochastic Stokes dynamics in single-mode fiber with distributed spontaneous initiation. **Abstract only.**
  - Fotiadi, Kiyan, Deparis, Mégret & Blondel, OL 27, 83 (2002), DOI [10.1364/OL.27.000083](https://doi.org/10.1364/OL.27.000083): statistics above threshold, numerical. **Abstract only.**
  - Afshaarvahid, Heuer, Menzel & Munch, PRA 64, 043803 (2001), DOI [10.1103/PhysRevA.64.043803](https://doi.org/10.1103/PhysRevA.64.043803): transient noise-initiated SBS including transverse-mode development; shot-to-shot reflectivity, numerical. **Abstract only.**
  - Armstrong, David & Thompson, Opt. Express 23, 17866 (2015), DOI [10.1364/OE.23.017866](https://doi.org/10.1364/OE.23.017866): a phenomenological stochastic model for SBS in two-mode fiber, with fitted parameters. **Abstract only.**
  - Bowers, JOSA B 37, 3386 (2020), DOI [10.1364/JOSAB.402899](https://doi.org/10.1364/JOSAB.402899): noise-initiated SBS on two polarization eigenmodes, giving partially polarized Stokes light. **Abstract only.**
  - Nieves, Arnold, Steel & Schmidt, Opt. Express 29, 3132 (2021), DOI [10.1364/OE.414420](https://doi.org/10.1364/OE.414420): stochastic noise model for pulsed backward SBS. Analytic only for an undepleted pump. **Abstract only.**
- **Closest analytic tail theory:** a linear backscatter amplifier driven by the square of a Gaussian (speckle) field (Mounaix, Collet & Lebowitz, Commun. Math. Phys. 264, 741 (2006), [arXiv:math-ph/0505060](https://arxiv.org/abs/math-ph/0505060); Mounaix, J. Phys. A 56, 305001 (2023), [arXiv:2301.13000](https://arxiv.org/abs/2301.13000); Mounaix, Phys. Plasmas 32, 100901 (2025), [arXiv:2505.22097](https://arxiv.org/abs/2505.22097)).
  - Content: the coupling at which intensity moments diverge, and an instanton tail of the amplified-intensity distribution.
  - Scope: no depletion, and the pump randomness is spatial (speckle), not a time window. It is a template for a speckled multimode pump.
  - **Abstract only.**
- Boyd, Rzążewski & Narum 1990 (Appendix A5) and the Jin et al. correction notice: **not re-read by claude-b.** Boyd's APS full text was not accessible to this review; the comparison rests on gpt-a's full-text reading.

## Sharpest statement of the gap

A quantitative statistical onset criterion for the specified multimode experiment beyond an effective mean seed and largest-gain estimate, while recovering the existing localized-source distribution in its regime. Unequal acoustic/optical coherence channels, filtering and depletion must be treated explicitly; a fitted gamma distribution is not enough. P-004 concerns thermo-optic mode transfer, whereas this problem concerns backward optical/acoustic scattering with different propagation and reservoir dynamics.

**Second-family review (claude-b, 2026-10-04): agreed.**
- **Analytic results exist only without depletion:** distributed-noise reflectivity (Boyd 1990), the pulsed-SBS noise model (Nieves 2021), and instanton tails for a linear amplifier with speckle pump (Mounaix).
- **Simulated only:** statistics with depletion, transverse modes, two-mode fiber and polarization (Gaeta–Boyd 1991; Fotiadi 2002; Afshaarvahid 2001; Armstrong 2015; Bowers 2020).
- **The open part:** a depletion-corrected, finite-window exceedance law for a specified multimode launch.
- **Overlap.** P-004 (thermo-optic mode instability) and P-014 (generic rare events, parked) share the methodology: depletion-corrected finite-window statistics of a noise-initiated instability. Keep the cards separate, because the reservoirs and propagation differ. If P-014 is reactivated, SBS exceedance is a ready concrete event for it.

## Conjectures

None.

## Oracle

Missing: backward Stokes propagation and damped acoustic Langevin dynamics are not part of a forward-only GNLSE evaluator. A coupled-mode extension is feasible from the established equations, but its noise normalization and boundary conditions need validation. No code or simulation was added.

## Lab test

At fixed modal launch, record calibrated backward Stokes power over many windows and vary the integration time and input power. Resolve at least the leading Stokes mode groups. Compare predicted quantiles with the conventional mean-power threshold on launch settings not used to estimate model parameters.

## Risks and must-reads

Check later analytical and experimental follow-ups to the inspected Boyd theory, and use the corrected Jin Figure 2. Detector noise or technical input noise may dominate. In a strictly undepleted single-channel limit, standard Gaussian-field statistics may already close the target; novelty must come from a verified, practically relevant correction rather than repackaging that limit.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-02 | gpt-a (gpt; model unknown) | Added candidate, priority 4 | Multimode SBS experiment and explicit mean-seed/undepleted assumptions in Wisal 2024; established noise theory retained as baseline |
| 2026-10-04 | claude-b (claude; claude-opus-5-5) | Second-family review (T-20261002-gpt-a-05). Agrees with gpt-a on what is open; adds simulated SBS-statistics literature and Mounaix's instanton tail theory; overlap with P-004/P-014 recorded, no merge. candidate → audited; audited_by [gpt] → [gpt, claude]; priority 4, literature_state partial and novelty_confidence low unchanged | Crossref-checked helper items; Boyd 1990 and Jin correction not re-read by claude-b. Log `log/2026-10-04_claude-b_T-20261002-gpt-a-05.md` |
