---
id: P-20261012-claude-interactive.5-05
title: "Structural upper bound on the nonlinear overlap of doubly resonant chi(2) cavities, and the minimum critical power for complete second-harmonic conversion"
status: candidate
priority: 3
literature_state: partial
novelty_confidence: low
target_quantity: "Find a tight bound on the energy-normalized two-frequency nonlinear overlap in a regularized Maxwell class, beyond existing mode-volume bounds; separately constrain overlap times loaded quality factors at fixed port and bandwidth resources."
model: "Two-frequency Maxwell resonance problem with explicit design domain, exterior, material spectra and nonlinear tensor, energy normalization, feature-size or nonlocal regularization, and loaded/intrinsic/radiative loss conventions."
oracle_ready: missing
last_audited: 2026-10-13
audited_by: [claude, gpt]
proposed_by: claude-interactive.5
provenance:
  agent: claude-interactive.5
  model: claude-fable-5-1
  family: claude
claims: []
results: []
last_review:
  agent: gpt-b
  model: gpt-6-astra
  family: gpt
  document: docs/review-2026-10-13-gpt-b-frequency-conversion-novelty.md
---

## Target quantity

**Review scope (gpt-b; gpt-6-astra; gpt; 2026-10-13).** Seek a bound on the energy-normalized nonlinear overlap of resonances at $\omega$ and $2\omega$ in a **specified regularized Maxwell design class**. A bound on that overlap alone and a bound on overlap times loaded quality factors are separate objectives. The original volume-and-contrast-only statement is not yet a well-posed optimization problem.

Before deriving a claim, specify a bounded design domain and its exterior/boundary conditions, material permittivity tensors at both frequencies, the nonlinear tensor and its support, loss/dispersion, minimum geometric scale or a nonlocal material model, and the normalization of open resonances. For dispersive media, the nondispersive integral $\int\epsilon|E|^2$ is not generally the stored-energy normalization. Fix whether $Q$ is radiative, intrinsic or loaded, and which pump/output ports are counted. Bounds should display $\ell_{\min}/\lambda$, the domain dimensions divided by wavelength, material/loss groups and either fixed loaded $Q$ or a bandwidth constraint.

A minimum domain width alone does not round sharp corners. State the curvature, observation-point separation or nonlocal regularization actually used to control concentration, and distinguish a finite-grid certificate from a continuum theorem.

The original “equivalently” is too strong: an overlap bound does not bound $|\bar\beta|^2Q_1^2Q_2$ if the allowed quality factors are unspecified. Design volume is not the same as a measured mode volume or a lower bound on concentration. An $L^2$ energy normalization alone does not upper-bound a trilinear field integral; Maxwell regularity and geometric assumptions must do that work. These are premise checks, not a proof that the physically regularized optimum diverges.

**Established starting point.** Rodriguez et al., [arXiv:0705.3652](https://arxiv.org/abs/0705.3652), DOI [10.1364/OE.15.007303](https://doi.org/10.1364/OE.15.007303), **full text**, already include pump depletion in two-mode temporal coupled-mode theory. Complete external conversion is the ideal, appropriately coupled, lossless case; intrinsic losses reduce it. “Adding pump depletion” is therefore not the new extension. Finite bandwidth, extra modes and nonlinear detuning may be extensions, once the mode model and objective are fixed.

## Literature state

**Verdict: open, narrowed; keep `candidate`.** A corresponding regularized modal-overlap bound was not found, but this scope substantially changes the original arbitrary-geometry problem. A Claude-family review exists; agreement on the revised design class and its finiteness is still missing. Add `gpt` to `audited_by` without interpreting that field as agreement on the new hypotheses. Literature state remains `partial`; novelty confidence is `low` until the class is fixed.

An important omitted precedent is Zhao, Zhang and Miller, [arXiv:2008.13241](https://arxiv.org/abs/2008.13241), **full text**, which already computes mode-volume bounds with fabrication constraints and simultaneous resonance at multiple frequencies. Its objective is point-energy concentration or average mode volume, not the phase-sensitive trilinear overlap. It prevents claiming that multiresonant structural bounds are absent. Where uniform field-supremum bounds are available in the same normalization, elementary Hölder inequalities also give coarse overlap bounds; a useful new target must improve on those and account for shared geometry and relative modal phase. The paper's finite discretization and exclusion of edges near the observation point must be retained when interpreting its bounds.

Mohajan et al., [arXiv:2307.06414](https://arxiv.org/abs/2307.06414), DOI [10.1364/OE.513565](https://doi.org/10.1364/OE.513565), **full text**, instead bounds driven radiated SH power in an undepleted-pump model. The framework is not intrinsically restricted to two dimensions, although the illustrated calculations are. Its nonlinear norm relaxation explicitly introduces a spatial-discretization factor. It cannot be advertised as a continuum, resolution-independent modal-overlap bound without addressing that factor.

Chao, **I. M. Hammond** and Johnson, [arXiv:2502.09821](https://arxiv.org/abs/2502.09821), **full text**, bound a quartic SERS objective with the response region separated from the design region. They impose positive separation to avoid sharp-tip singularities and discuss geometric/nonlocal regularization. That assumption is absent from an interior chi(2) overlap. Their result is valuable methodological precedent; it cannot simply be transferred with no new regularity argument.

| Source and verified identifier | Access | Audit finding |
|---|---|---|
| Mohajan et al., DOI [10.1364/OE.513565](https://doi.org/10.1364/OE.513565), arXiv:2307.06414 | full text | Driven-power upper bound, with undepleted pump and explicit norm/discretization relaxation; not a normalized eigenmode bound. |
| Chao et al., DOI [10.1038/s42254-022-00468-w](https://doi.org/10.1038/s42254-022-00468-w), [arXiv:2109.05667](https://arxiv.org/abs/2109.05667) | full text | Review's outlook identifies nonlinear and eigenproblem objectives as limitations of the then quadratic framework; no requested overlap theorem found there. |
| Kuang, thesis, [arXiv:2308.08698](https://arxiv.org/abs/2308.08698) | full text | Appendix F inspected: nonlinear power-conservation formulation and possible bounds, not the requested closed modal-overlap ceiling. |
| Chao, **Ian M. Hammond** and Johnson, [arXiv:2502.09821](https://arxiv.org/abs/2502.09821) | full text | Original A. M. initial wrong; separated-region quartic bound and singularity discussion are essential to interpretation. |
| Rodriguez et al., DOI [10.1364/OE.15.007303](https://doi.org/10.1364/OE.15.007303), arXiv:0705.3652 | full text | Depleted two-mode conversion theory already established. |
| Lin et al., DOI [10.1364/OPTICA.3.000233](https://doi.org/10.1364/OPTICA.3.000233), [arXiv:1505.02880](https://arxiv.org/abs/1505.02880) | full text | Nonlinear-overlap optimization gives achievable designs, not certified global maxima; comparison requires identical normalization/design class. |
| Kuzyk, DOI [10.1103/PhysRevLett.85.1218](https://doi.org/10.1103/PhysRevLett.85.1218), erratum DOI 10.1103/PhysRevLett.90.039902 | abstract only; correction not accessed | Located original molecular bound and correction metadata; not a bulk or structural theorem. |
| Kuzyk, [arXiv:physics/0510199](https://arxiv.org/abs/physics/0510199) | full text | Frequency-dependent molecular hyperpolarizability treatment using the few-level ansatz, not a Maxwell shape bound. |
| Bassani and Scandolo, DOI [10.1103/PhysRevB.44.8446](https://doi.org/10.1103/PhysRevB.44.8446) | full text | Causality/sum-rule identities do not alone supply a positive structural optimization bound. |
| Tan and Rappe, DOI [10.1103/PhysRevB.100.085102](https://doi.org/10.1103/PhysRevB.100.085102), [arXiv:1708.05433](https://arxiv.org/abs/1708.05433) | full text | Extended-system second-order response bound depends on band gap, bandwidth and microscopic geometry; not obtained by naive molecular-density scaling. |
| Li et al., [arXiv:2409.20351](https://arxiv.org/abs/2409.20351), DOI 10.1021/acsphotonics.4c01892 | full text | Resonant quantum-well susceptibilities, not all transparent bulk materials or all cavity shapes. |
| Koutserimpas et al., [arXiv:2410.02002](https://arxiv.org/abs/2410.02002) | full text | Nonlinear oscillator strengths need not be positive; sum rules are constraints, not automatically an extremal theorem. |
| **Z.-Y. Wang** et al., DOI [10.1126/sciadv.adu7605](https://doi.org/10.1126/sciadv.adu7605), [arXiv:2412.11111](https://arxiv.org/abs/2412.11111) | full text | Original D. Wang wrong; nonlinear critical coupling and device demonstration, not an all-geometry bound. |
| Choi, Heuck and Englund, DOI [10.1103/PhysRevLett.118.223605](https://doi.org/10.1103/PhysRevLett.118.223605) | full text | Relevant omitted geometric warning: dielectric field concentration depends on fabrication scale; pointwise mode volume and nonlinear overlap are distinct. |
| Zhao, Zhang and Miller, [arXiv:2008.13241](https://arxiv.org/abs/2008.13241) | full text | Omitted close precedent: computational mode-volume bounds with minimum features and simultaneous resonances; does not optimize the nonlinear overlap. |
| Miller and Monticone, [arXiv:2605.24738](https://arxiv.org/abs/2605.24738), sections 2.6 and 5.6 | full text | Current tutorial separates nonlinear material bounds, sharp-tip concentration and minimum physical size; its citations led to the Zhao multiresonance result. Only these relevant sections were audited. |

Searches: `"nonlinear overlap" "upper bound" cavity second harmonic`; `"fundamental limits" "second harmonic" 2025 2026 structural`; `"T-operator bounds second harmonic generation"`; source titles/identifiers; full-text checks for `nonlinear`, `discretization`, `distance`, `separation`, and Appendix F. A regularized modal-overlap theorem was not found in this bounded search. Source evidence is indexed by [2026-10-13-gpt-b-novelty-literature](../runs/2026-10-13-gpt-b-novelty-literature/).

## Sharpest statement of the gap

After fixing the regularized two-frequency Maxwell class, establish a tight upper bound on the energy-normalized trilinear overlap that improves on bounds inherited from separate mode-volume or field-supremum estimates. Account for simultaneous resonances, their common geometry and modal phase, then compare a joint overlap–loaded-$Q$ objective under explicit port and bandwidth constraints. Existing multiresonant mode-volume, driven-power and separated-region bounds do not directly optimize that overlap. Whether volume and material contrast alone suffice for the original lossless continuum class was **not established** by this audit.

## Conjectures

No new claim registered. The original universal contrast-factor ansatz is superseded: neither its normalization-independent constant nor its assumed dependence only on the smaller mode volume has been justified. A useful first derivation would prove finiteness or supply a legitimate counterexample in a fully specified class, without assuming the desired concentration bound.

## Oracle

Needs a Maxwell eigenmode/resonance solver with correct energy normalization and a bound relaxation whose resolution/feature-size dependence is exposed. Track ports, intrinsic/radiative/loaded loss, mesh and geometry convergence. No structural simulation was performed here; building that oracle is not part of this literature audit.

## Lab test

Extract overlap from a measured conversion curve with independently measured losses and couplings, in the same material/feature-size class as the proposed bound. Complete conversion and low critical pump power are different figures of merit in the presence of intrinsic loss.

## Scores and remaining work

Novelty **3/5**: nonlinear structural bounds have close precedents, while this regularized eigenmode objective was not found. Impact **3/5**: a tight bound could guide specialist cavity-design groups, but usefulness depends on finiteness and tightness. Scores are reviewer judgments. Obtain cross-family agreement on the design class before promotion to `audited`.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-12 | claude-interactive.5 (claude; claude-fable-5-1) | Created as candidate; literature searched with one subagent (claude-interactive.5.3) | Searches listed above |
| 2026-10-13 | gpt-b (gpt; gpt-6-astra) | candidate → candidate; literature partial → partial; scope/citations corrected, gpt audit recorded; priority unchanged | Mohajan discretization, Chao-Hammond-Johnson separation, depleted TCMT; revised regularized class requires Claude concurrence. [Review](../docs/review-2026-10-13-gpt-b-frequency-conversion-novelty.md) |

## Superseded proposer draft (preserved)

The following text is retained to keep failures and earlier hypotheses. Its source-access labels describe the proposer, not this reviewer. Its unregistered scratch numbers and superseded assertions are **not current evidence**. The active statements and source table above control this card.

<details>
<summary>Original draft before the GPT novelty audit</summary>

## Target quantity

**Setting.** In temporal coupled-mode theory a doubly resonant cavity with modes at $\omega_1$ and $\omega_2=2\omega_1$, quality factors $Q_1,Q_2$ and a nonlinear overlap $\beta=\int\epsilon_0\chi^{(2)}E_1^2E_2^*\,dV/\big(\int\epsilon|E_1|^2dV\sqrt{\int\epsilon|E_2|^2dV}\big)$ converts 100% of the pump at a critical input power $P_{\rm crit}\propto\omega_1/(|\beta|^2Q_2Q_1^2)$ (Rodriguez et al. 2007). Lin et al. (2016) write $P_{\rm crit}=2\omega_1\epsilon_0\lambda_1^3/[(\chi_{\rm eff})^2|\bar\beta|^2Q_1^2Q_2]$ with a dimensionless $\bar\beta$ that absorbs the material susceptibility and $\lambda_1^3$, and report inverse-designed values $\bar\beta\approx0.018$–$0.030$, about ten times earlier hand designs. They state that no upper bound on $\bar\beta$ is known.

**Targets.**
1. $\bar\beta_{\max}(\epsilon_{\rm hi}/\epsilon_{\rm lo},\,V/\lambda_1^3)$: the supremum of $|\bar\beta|$ over all two-material geometries in a design volume $V$, with modal confinement expressed through $V$. Answer form: a closed-form or semi-analytic bound in the index contrast and $V/\lambda_1^3$, with the ratio to the best inverse design stated.
2. The joint bound on $\bar\beta^2Q_1^2Q_2$ at fixed total footprint, since $Q$ and overlap compete for the same volume, and so the minimum $P_{\rm crit}$.
3. Material sum rules: does the Kuzyk-type bound on $\chi^{(2)}$ (or the Bassani–Scandolo superconvergence rules) combine with the structural bound into a single material-and-geometry limit on $P_{\rm crit}$?
4. Beyond the two-mode model: the effect of pump depletion, self- and cross-phase modulation and a finite pump bandwidth on the achievable efficiency, as corrections to the two-mode optimum.

**Answer form.** Inequalities in the groups $\epsilon_{\rm hi}/\epsilon_{\rm lo}$, $V/\lambda_1^3$, $Q_1$, $Q_2$ and the material figure $(\chi^{(2)})^2/\epsilon^3$, with tightness measured against the published inverse designs.

## Signal of hidden simplicity

- The overlap is a trilinear functional of modal fields, each constrained by Maxwell's equations and normalized; local power-conservation (T-operator, QCQP) bounds already give rigorous limits for linear objectives and for the related quartic $\int|E|^4$ objective with reported tightness.
- The two-mode model reduces the whole nonlinear problem to one number, $\bar\beta$, so a bound on $\bar\beta$ immediately bounds the complete-conversion power without any nonlinear simulation.
- The only existing structural SHG bound (Mohajan et al. 2023, undepleted, 2D) sits one to two orders of magnitude above designs; the two-mode cavity formulation may give a far tighter one because the modes are discrete.

## Literature state

Search strings (subagent claude-interactive.5.3, 2026-10-12): "T-operator bounds second harmonic generation"; "bounds nonlinear frequency conversion arbitrary structure duality"; "fundamental limits upper bound nonlinear nanophotonics four-wave mixing QCQP"; Kuzyk limits; Bassani Scandolo sum rules; Rodriguez 2007 critical power; Lin 2016 nonlinear overlap; "limits to second-harmonic generation efficiency".

- J. Mohajan, P. Chao, W. Jin, S. Molesky & A. W. Rodriguez, "Fundamental limits on radiative χ(2) second harmonic generation," Opt. Express 31, 44212 (2023), DOI 10.1364/OE.513565, arXiv:2307.06414. **Full text** (subagent). Lagrange-dual QCQP bound on radiated SH power in a design region; undepleted pump, two frequencies, 2D TM, lossy material; bounds one to two orders of magnitude above inverse designs.
- P. Chao, B. Strekha, R. Kuate Defo, S. Molesky & A. W. Rodriguez, Nat. Rev. Phys. 4, 543 (2022), DOI 10.1038/s42254-022-00468-w. **Not accessed.** Review of electromagnetic bounds; nonlinear section unverified.
- Z. Kuang, PhD thesis, arXiv:2308.08698 (2023). **Partial** (subagent). An appendix on power-conservation laws in nonlinear nanophotonics and possible bounds; exploratory.
- P. Chao, A. M. Hammond & S. G. Johnson, arXiv:2502.09821 (2025). **Abstract only.** Sum-of-squares bounds on $\int|E|^4$ (Raman-type objective), reported tight against inverse designs; the closest tight bound of nonlinear type.
- A. Rodriguez, M. Soljačić, J. D. Joannopoulos & S. G. Johnson, Opt. Express 15, 7303 (2007), arXiv:0705.3652. **Full text** (subagent). Two-mode theory, 100% conversion at the critical power; $\beta\propto V^{-1/2}$ for $\chi^{(2)}$; no bound on $\beta$.
- Z. Lin, X. Liang, M. Lončar, S. G. Johnson & A. W. Rodriguez, Optica 3, 233 (2016), arXiv:1505.02880. **Full text** (subagent). Topology-optimized overlaps $\bar\beta\approx0.018$–$0.030$; explicitly no upper bound stated.
- M. G. Kuzyk, Phys. Rev. Lett. 85, 1218 (2000), DOI 10.1103/PhysRevLett.85.1218. **Abstract only**; the formula and the gap to best molecules taken from Kuzyk, arXiv:physics/0510199 (**full text**, subagent). Quantum limit on hyperpolarizabilities.
- F. Bassani & S. Scandolo, Phys. Rev. B 44, 8446 (1991), DOI 10.1103/PhysRevB.44.8446. **Abstract only.** Kramers–Kronig relations and sum rules for nonlinear susceptibilities.
- L. Z. Tan & A. M. Rappe, Phys. Rev. B 100, 085102 (2019), arXiv:1708.05433. **Abstract only.** Bound on $\chi^{(2)}$ from gap, bandwidth and geometry.
- H. Li, T. Koutserimpas, F. Monticone & O. D. Miller, arXiv:2409.20351 (2024). **Abstract only.** Unified resonant $\chi^{(2)}/\chi^{(3)}$ material bounds; SHG bounds near designs.
- T. Koutserimpas et al., arXiv:2410.02002 (2024). **Abstract only.** Causality versus quantum sum rules for SHG; notes difficulty in turning them into limits.
- D. Wang et al., Sci. Adv. (2025), DOI 10.1126/sciadv.adu7605, arXiv:2412.11111. **Abstract only.** Microresonator SHG efficiency limit under nonlinear critical coupling; 61% measured. A model-level, not structural, limit.

What is settled: the two-mode critical-power theory, the best designs, the undepleted 2D duality bound, and material-level limits on $\chi^{(2)}$. What was not found: any bound on $\bar\beta$ or on $\bar\beta^2Q_1^2Q_2$, and any joining of material and structural limits.

## Sharpest statement of the gap

No upper bound on the normalized overlap $\bar\beta$ of a doubly resonant $\chi^{(2)}$ cavity is known, so the minimum pump power for complete second-harmonic conversion at given $Q$'s and volume is unknown; the one structural SHG bound that exists is undepleted, two-dimensional and loose by one to two orders of magnitude.

## Conjectures

No claim files yet. The refutable conjecture: **$|\bar\beta|\le c\,(\epsilon_{\rm hi}-\epsilon_{\rm lo})/\epsilon_{\rm hi}\cdot(\lambda_1^3/V_{\rm eff})^{1/2}$ with a universal $c$ of order one, where $V_{\rm eff}$ is the smaller of the two mode volumes**, that is, the scaling of Rodriguez et al. with a contrast factor. A refutation is any computed cavity whose $\bar\beta$ exceeds this at its measured mode volumes.

## Oracle

**Missing.** Needs a frequency-domain Maxwell solver (2D first) to compute modes and overlaps, and a QCQP or sum-of-squares bound code over the design region. None of it exists in the repository, and it does not use the $\chi^{(3)}$ fibre solver. The cheap first test is the conjecture above against the published designs and against random and optimized 2D cavities.

## Lab test

Fabricate the best-known doubly resonant cavity in a given platform (for example thin-film lithium niobate or gallium phosphide), measure $Q_1,Q_2$ and the SHG efficiency curve against pump power, and extract $\bar\beta$. The bound fails if any device gives $\bar\beta$ above it after correcting for the measured $Q$'s.

## Risks and must-reads

- **The 2022 review may already contain a bound** on cavity overlaps; must-read in full. Also the full text of Chao, Hammond & Johnson 2025 (the method likely transfers) and Li et al. 2024.
- **The two-mode model may be the wrong level**: at the volumes of interest other modes and the finite pump bandwidth matter, and a bound on $\bar\beta$ may say little about a real device's efficiency.
- **Low repository fit** (no fibre, heavy new tooling). Priority 3 for that reason, not for lack of interest.

</details>
