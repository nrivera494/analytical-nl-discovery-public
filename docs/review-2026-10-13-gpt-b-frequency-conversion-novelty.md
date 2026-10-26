---
agent: gpt-b
model: gpt-6-astra
family: gpt
date: 2026-10-13
task: T-20261013-gpt-b-01
status: complete
stacked_on: "PR #41"
---

# Frequency-conversion novelty audit

All assigned cards retain a narrower open question. The poling trace budget and the comb energy ceiling are established starting points. The quantum and structural cards need explicit resource/design classes before their broad gap statements can be accepted. No card is recommended for demotion as wholly or largely solved after narrowing, but several proposed discovery targets are withdrawn as already known or unsupported.

This is a problem-level literature review, not verification or promotion of a claim. Priorities are unchanged. Earlier text is preserved in a clearly superseded section of each card; its unregistered scratch values are not current evidence. Scores below are reviewer judgments on the narrowed problems using `docs/RANKING_RUBRIC.md`, not simulation outputs.

## Summary

| Card | Verdict | Closest prior work and access | What remains open in this review | Novelty / impact | Recommended status |
|---|---|---|---|---|---|
| [Single-photon Kerr phase, P-20261012-claude-interactive-02](../problems/P-20261012-claude-interactive-02-max-single-photon-kerr-phase.md) | open, narrowed | Shapiro–Razavi, [quant-ph/0612086](https://arxiv.org/abs/quant-ph/0612086); Miller–Monticone, [2605.24738](https://arxiv.org/abs/2605.24738), relevant sections; **full text** | An operational phase–fidelity–bandwidth tradeoff with explicit material, geometry and interaction-time resources; class still needs agreement | 3 / 4 | candidate |
| [Poling, P-20261012-claude-interactive.5-01](../problems/P-20261012-claude-interactive.5-01-poling-sum-rule-efficiency-bandwidth.md) | open, narrowed | Magland, [0903.4363](https://arxiv.org/abs/0903.4363); Phillips et al., [10.1364/OE.21.010139](https://doi.org/10.1364/OE.21.010139); **full text** | Certified finite-length, fabrication-constrained bandwidth frontier; separately, a depleted input-resource bound | 3 / 4 | audited |
| [Kerr comb, P-20261012-claude-interactive.5-02](../problems/P-20261012-claude-interactive.5-02-kerr-comb-efficiency-bound-all-stationary-states.md) | open, narrowed | Yu et al., [10.1038/s41467-022-30774-x](https://doi.org/10.1038/s41467-022-30774-x), supplementary section V; **full text** | Attainability or a strict gap at fixed normalized drive and dispersion, separately for all stationary and stable states | 2 / 3 | audited |
| [Temporal-mode selectivity, P-20261012-claude-interactive.5-03](../problems/P-20261012-claude-interactive.5-03-qfc-single-stage-selectivity-bound.md) | open, narrowed | Reddy et al., [1305.2165](https://arxiv.org/abs/1305.2165) and [1702.05687](https://arxiv.org/abs/1702.05687); **full text** | A theorem or counterexample for the full, unfiltered, uniform first-order single-pass operator class | 3 / 4 | audited |
| [Cavity overlap, P-20261012-claude-interactive.5-05](../problems/P-20261012-claude-interactive.5-05-structural-bound-cavity-chi2-overlap.md) | open, narrowed | Zhao et al., [2008.13241](https://arxiv.org/abs/2008.13241); Mohajan et al., [2307.06414](https://arxiv.org/abs/2307.06414); **full text** | A tight nonlinear-overlap bound beyond concentration estimates in an agreed regularized Maxwell class | 3 / 3 | candidate |

The existing Claude literature reviews explicitly leave the narrowed poling frontier, comb attainability and single-pass selectivity theorem open. That concurrence supports `audited` for those questions. The quantum card was expressly unaudited, and the structural scope now requires agreement on new hypotheses. Adding `gpt` to an audit list does not itself establish that agreement. All active literature states are `partial`; none of these statuses means a result has passed promotion gates.

## P-20261012-claude-interactive-02 — single-photon Kerr phase

The original definition combines probe cross-phase metrology with a conditional quantum gate phase. They need different performance criteria. A gate objective must define its channel, temporal modes, unconditional fidelity, leakage, allowed deterministic pulse corrections and any postselection. Its conditional phase is periodic, so a useful target fixes the desired phase and bounds fidelity or resources. The material and architecture class must also include a finite design region, response kernel, feature regularization and interaction length, delay or storage budget. Input bandwidth alone does not establish an interaction-time upper bound.

The architecture-specific literature is substantial. Shapiro–Razavi's causal continuous-time model, [quant-ph/0612086](https://arxiv.org/abs/quant-ph/0612086), and Gea-Banacloche's multimode model, [0911.4682](https://arxiv.org/abs/0911.4682), were read in **full text**. Their obstructions cannot be extended to every passive dielectric geometry without carrying their assumptions. Brod–Combes, [1604.04278](https://arxiv.org/abs/1604.04278), and Tian–Chen, [2312.10719](https://arxiv.org/abs/2312.10719), **full text**, use discrete emitter-mediated architectures. Heuck–Jacobs–Englund, [1909.05751](https://arxiv.org/abs/1909.05751), **full text**, uses dynamic cavity coupling and classical controls. These are relevant comparisons, but not interchangeable counterexamples inside a strictly passive bulk-Kerr class. Tian–Chen's overlap-amplitude fidelity also differs from an average gate-process fidelity; the reported quantities are indexed in the [source-audit run](../runs/2026-10-13-gpt-b-novelty-literature/).

The omitted direct third-order molecular reference is Kuzyk, [10.1364/OL.25.001183](https://doi.org/10.1364/OL.25.001183), **abstract only**; its correction [10.1364/OL.28.000135](https://doi.org/10.1364/OL.28.000135) was located but **not accessed** beyond metadata. The originally cited [physics/0510199](https://arxiv.org/abs/physics/0510199), **full text**, primarily develops second-order response. Few-level assumptions and sum-rule pathologies matter: [physics/0510002](https://arxiv.org/abs/physics/0510002) and [1306.0937](https://arxiv.org/abs/1306.0937), **full text**, do not establish a general bulk-density ceiling. The known band-gap scaling model, [10.1103/PhysRevLett.65.96](https://doi.org/10.1103/PhysRevLett.65.96), **full text**, is not such a ceiling either.

A particularly useful current cross-check is Miller–Monticone, [2605.24738](https://arxiv.org/abs/2605.24738), **full text**, sections 2.6 and 5.6. It explicitly identifies general nonlinear material bounds incorporating bandwidth as open, while reviewing existing geometric bounds. This supports a constituent subquestion; it does not prove the proposed combination. The card now distinguishes material response, normalized field interaction and channel fidelity. I neither derived a universal phase law nor proved the strictly passive bulk class unbounded.

**Score justification.** Novelty 3: the resource-qualified combination has clear precedents in its constituent fields, without a matching combined result located. Impact 4: a tight operational law could guide several gate platforms, conditional on a useful resource class. Keep `candidate`; Claude concurrence on the revised scope is missing. Follow-ups: [T-20261013-gpt-b-02](../tasks/T-20261013-gpt-b-02-agree-an-operational-resource-class-for-.md) and [T-20261013-gpt-b-07](../tasks/T-20261013-gpt-b-07-resolve-critical-full-text-leads-from-th.md).

## P-20261012-claude-interactive.5-01 — poling bandwidth

The undepleted SFG system is the unitary scattering problem behind established NMR pulse synthesis. Magland's [0903.4363](https://arxiv.org/abs/0903.4363), **full text**, Theorem 1.7.1 supplies the trace formula; Epstein's [10.1016/j.jmr.2003.12.014](https://doi.org/10.1016/j.jmr.2003.12.014), **abstract only**, already presents minimum-energy synthesis. The active card corrects the gauge signs and records, for its mismatch convention,

$$\int_{\mathbb R}-\log(1-\eta)\,d\Delta
=2\pi\kappa^2\int g^2\,dz-8\pi\sum_j\operatorname{Im}\xi_j.$$

The [trace-normalization run](../runs/2026-10-13-gpt-b-novelty-poling-trace/) checks the gauge and a uniform-box scattering potential, including bound states and mismatch-cutoff convergence. At its largest cutoff the maximum absolute tail-corrected discrepancy is about $1.3\times10^{-5}$ for SFG and $1.8\times10^{-5}$ for the uniform OPA log-gain check; inputs and all cutoffs are in that run's summary. The tail correction is asymptotic, not a rigorous numerical error enclosure. These checks audit normalization only; they prove no new arbitrary-profile, depletion or loss theorem.

Three distinctions change the gap. Raw binary poling, a bounded real envelope and a complex effective QPM envelope are different control sets. Phillips–Langrock–Fejer, [10.1364/OE.21.010139](https://doi.org/10.1364/OE.21.010139), **full text**, already uses Fourier-harmonic reductions and convex design. Infinite-sweep adiabatic behavior does not prove a finite raw-binary device saturates the full trace budget. Also, a minimum domain width does not smooth its walls, so higher spectral moments cannot be assumed finite. Finally, depletion and unequal loss invalidate the direct unitary-scattering argument.

The missed neighbouring literature is close. Chern–Wang, [10.1364/JOSAA.19.000772](https://doi.org/10.1364/JOSAA.19.000772), **full text**, combines binary-grating inverse scattering with transfer-matrix optimization. Brenne–Skaar, [10.1109/JLT.2003.808648](https://doi.org/10.1109/JLT.2003.808648), **abstract only**, states necessary and sufficient realizability conditions for a discrete codirectional model. Li–Ruths–Glaser, [10.1038/s41467-017-00441-7](https://doi.org/10.1038/s41467-017-00441-7), **full text of main article**, supplies bounded-amplitude designs through a conditional spin–spring projection; the supplement remains unread. These preclude treating general inverse synthesis or bounded-pulse design as new. They do not, on the inspected evidence, settle the proposed worst-band-error frontier with minimum-domain constraints.

The depletion literature also goes beyond qualitative adiabaticity: Porat–Arie, [1302.3964](https://arxiv.org/abs/1302.3964), **full text**, includes a bandwidth estimate, and Genov et al., [10.1088/2040-8978/16/6/062001](https://doi.org/10.1088/2040-8978/16/6/062001), **full text**, treats composite designs in depleted and pulsed settings. A new claim must compare against those models.

**Score justification.** Novelty 3: an exact fabrication-constrained frontier has strong adjacent precedents, but no matching theorem was found. Impact 4: a tight length–bandwidth–efficiency law would guide several QPM platforms. Mark the narrowed card `audited`. Follow-ups: [T-20261013-gpt-b-04](../tasks/T-20261013-gpt-b-04-formulate-the-constrained-poling-bandwid.md), [T-20261013-gpt-b-07](../tasks/T-20261013-gpt-b-07-resolve-critical-full-text-leads-from-th.md), and [T-20261013-gpt-b-08](../tasks/T-20261013-gpt-b-08-screen-depleted-pulsed-and-lossy-trace-b.md).

## P-20261012-claude-interactive.5-02 — Kerr-comb efficiency

The proposed energy ceiling is correct under the stated uniform-loss normalization, and its physical content is already published. Yu et al., [2109.01280](https://arxiv.org/abs/2109.01280), DOI [10.1038/s41467-022-30774-x](https://doi.org/10.1038/s41467-022-30774-x), **full text**, supplementary section V, explicitly relates an internal ceiling to external coupling. It gives the same squared-coupling limit. Xue et al., [1610.00958](https://arxiv.org/abs/1610.00958), **full text**, supplies the effective nonlinear critical-coupling expression; maximizing it yields the same envelope. This equivalence is the reviewer's algebraic inference, not a claim that Xue solved the global branch optimization.

For a real drive $f$, uniform amplitude decay and strict pump-line exclusion,

$$\eta=\eta_c^2-\frac{4\eta_c^2}{f^2}|a_0-f/2|^2.$$

The [balance run](../runs/2026-10-13-gpt-b-novelty-kerr-balance/) verifies the square completion and transmission form symbolically. It also checks the corresponding identity for several complex pump amplitudes; the general result is a sum of the same scalar identity. Excluding **all** pumped modes preserves the same ceiling for a fixed multimode drive under uniform losses. Reduced duty cycle alone does not raise it. A bounded time-dependent state satisfies the corresponding time-averaged squared-distance expression. These statements concern the norm conserved by the model; broad-spectrum photon flux and physical power cannot be silently interchanged.

Gasmi et al., [2210.09760](https://arxiv.org/abs/2210.09760), **full text**, includes weighted pump-mode power in its dual-pump metric. The balance run shows its weak-drive equal-pump value can be one half while strict power outside the pump support is zero. Thus the original interpretation of that number is invalid. Kondratiev et al., [2209.03707](https://arxiv.org/abs/2209.03707), **full text**, explicitly notes low-drive disagreement of its soliton ansatz with numerical solutions; its formal unity limit does not settle exact attainability.

The surviving question is the fixed-drive, fixed-dispersion supremum over exact stationary states, with stable states treated separately. Gärtner et al., [10.1103/PhysRevA.100.033819](https://doi.org/10.1103/PhysRevA.100.033819), Mandel–Reichel, [1603.02206](https://arxiv.org/abs/1603.02206), and Gasmi et al., [2210.09779](https://arxiv.org/abs/2210.09779), **full text of relevant sections**, provide continuation, a priori or existence results, not that optimization. No new LLE solver or stationary solution was computed. No large-drive gap exponent or maximizing branch was established.

**Score justification.** Novelty 2: the energy envelope and coupling mechanism are known; exact all-branch attainability is a narrower extension. Impact 3: a stable-state frontier could supply a practical specialist design rule. Mark the narrowed card `audited`. Follow-up: [T-20261013-gpt-b-05](../tasks/T-20261013-gpt-b-05-test-fixed-resource-attainability-of-the.md).

## P-20261012-claude-interactive.5-03 — temporal-mode selectivity

For squared singular values $\eta_n$ of the full conversion operator, use $S=\eta_1^2/\sum_n\eta_n$. The dominant-mode fraction $\eta_1/\sum_n\eta_n$ is different from both $S$ and a density-matrix purity. The active class specifies forward-propagating fields at a common input plane, a freely propagating undepleted pump, uniform lossless interaction and first-order group delays, excluding output filtering, cavities, longitudinal control and extra stages. Opposite walk-off in the pump frame is not laboratory counter-propagation. Singular velocity limits require their own operator/trace definitions.

Reddy et al., [1305.2165](https://arxiv.org/abs/1305.2165), **full text**, provides an exact matched-velocity Green kernel and numerical Schmidt spectra. Its omitted [erratum, 10.1364/OE.25.007998](https://doi.org/10.1364/OE.25.007998), **full text**, corrects time arguments. Reddy–Raymer, [1702.05687](https://arxiv.org/abs/1702.05687), **full text**, describes the ceiling as numerically explored. The reported approximate values and their regimes are indexed in the [source-audit run](../runs/2026-10-13-gpt-b-novelty-literature/). I found no global comparison theorem in these papers or the inspected thesis chapters.

The original finite-Hankel/Slepian identification is unproved. A coordinate transformation must carry the integration measure and Heaviside support. Raymer–Banaszek, [2008.09280](https://arxiv.org/abs/2008.09280), **full text**, does derive a Slepian reduction for sequential rectangular time/frequency filters, a different kernel. Quesada–Sipe, [1508.03361](https://arxiv.org/abs/1508.03361), **full text**, explains time ordering but does not turn a finite Magnus truncation into a nonperturbative supremum. The total order-$n$ generator in its scaled $N$-stage construction is proportional to $N^{1-n}$, correcting the draft's $N^{-n}$ statement.

Babel et al., [2608.09346](https://arxiv.org/abs/2608.09346), **full text**, is not an established counterexample. Its normalized finite-basis mode fraction was measured with spectral output filtering in the low-gain regime; high conversion was measured separately through signal depletion. The pump settings, percentages and basis are transcribed with page pointers in the [source-audit run](../runs/2026-10-13-gpt-b-novelty-literature/). Multiplying the two reported headline values would combine different experiments and definitions. The located NIST seminar announcement promises a derivation, but slides or a proof were not obtained; this remains a lead rather than proof of either existence or absence of a theorem.

**Score justification.** Novelty 3: the mechanism, kernel and numerical observations are established, while the all-pump theorem remains unlocated. Impact 4: a certified frontier would determine when extra stages or resonators are necessary. Mark `audited` for the stated uniform class. Follow-up: [T-20261013-gpt-b-06](../tasks/T-20261013-gpt-b-06-audit-the-pulse-gate-operator-reduction-.md).

## P-20261012-claude-interactive.5-05 — doubly resonant overlap

The strongest newly located adjacent result is Zhao–Zhang–Miller, [2008.13241](https://arxiv.org/abs/2008.13241), **full text**, which already bounds dielectric mode volumes with minimum features and simultaneous resonances. The original gap cannot be described as absence of multiresonant structural bounds. Its objective is field concentration or average mode volume, however, not a phase-sensitive nonlinear overlap. Where the same class supplies uniform field-supremum bounds, elementary Hölder inequalities give coarse overlap bounds. Improving those while retaining a common geometry and modal phase is a defensible narrower target.

Other precedents have different objectives and essential regularization. Mohajan et al., [2307.06414](https://arxiv.org/abs/2307.06414), DOI [10.1364/OE.513565](https://doi.org/10.1364/OE.513565), **full text**, bounds driven radiated SH power in an undepleted model, with an explicit spatial-discretization factor in its nonlinear norm relaxation. Its framework is not intrinsically limited to its illustrated dimensionality. Chao–Hammond–Johnson, [2502.09821](https://arxiv.org/abs/2502.09821), **full text**, separates the quartic-response region from the design region to control singularities. Neither immediately gives the interior energy-normalized overlap requested here.

A finite design volume is neither an effective mode volume nor an $L^\infty$ field bound. Domain-width constraints alone do not round corners. Specify material dispersion/tensors, nonlinear support, exterior and port conditions, mode-energy normalization, edge/feature or nonlocal regularization, and continuum versus finite-grid interpretation. An overlap bound alone also does not bound its product with unspecified loaded quality factors. The audit did not prove that volume and contrast alone suffice, or construct a Maxwell counterexample showing they do not.

Rodriguez et al., [0705.3652](https://arxiv.org/abs/0705.3652), DOI [10.1364/OE.15.007303](https://doi.org/10.1364/OE.15.007303), **full text**, already includes depletion in its two-mode conversion theory. Adding depletion is therefore not a new extension of that model. Lin et al., [1505.02880](https://arxiv.org/abs/1505.02880), **full text**, provides achieved designs; their tabulated overlaps are indexed in the [source-audit run](../runs/2026-10-13-gpt-b-novelty-literature/), not reproduced by Maxwell simulation here.

**Score justification.** Novelty 3: structural and multiresonant bounds are close precedents, but the tight regularized overlap objective was not found solved. Impact 3: a tight result could guide specialist cavity design, conditional on finiteness and useful tightness. Keep `candidate` until a Claude reviewer agrees on the revised class. Follow-up: [T-20261013-gpt-b-03](../tasks/T-20261013-gpt-b-03-agree-the-regularized-two-frequency-over.md).

## Citation corrections and access limits

The active cards contain the complete source-by-source access ledger. Specific DOI/arXiv identifiers in the original lists were located; several author attributions, a publication year, and interpretations needed correction.

| Original issue | Correction and evidence |
|---|---|
| Epstein & Magland assigned to arXiv:0903.4363 | The thesis is by **John F. Magland alone**; **full text**. Epstein's separate paper is DOI 10.1016/j.jmr.2003.12.014, **abstract only**. |
| L. Babel; simultaneous headline selectivity and conversion | **Silia Babel**; arXiv:2608.09346, **full text**. Definitions, filtering, basis and pump settings differ. |
| Chen Kerr measurement dated 2017 | Publication is **2018**, DOI 10.1038/s41467-017-02487-z, arXiv:1612.07427, **full text**. It is probe-phase metrology, not a gate demonstration. |
| Incorrect author initials/lists in comb sources | **C. Bao**, DOI 10.1364/OL.39.006126, **abstract only**; Xue, **P.-H. Wang, Y. Xuan, M. Qi, A. M. Weiner**, arXiv:1610.00958, **full text**; **J. Gärtner**, DOI 10.1103/PhysRevA.100.033819, **full text**; **Q.-F. Yang**, DOI 10.1186/s43593-024-00075-5, **full text**; **J. Zang**, arXiv:2401.16740, **full text**. |
| Incorrect poling author list | Xiong's list corrected against arXiv:1609.09221, **full text**; Phillips's coauthor is **L. Gallmann**, DOI 10.1364/JOSAB.30.001551, **abstract only**. |
| A. M. Hammond; D. Wang | **Ian M. Hammond**, arXiv:2502.09821; **Zhi-Yan Wang**, DOI 10.1126/sciadv.adu7605 / arXiv:2412.11111; **full text**, both. |
| Omitted corrections | Reddy DOI 10.1364/OE.25.007998, **full text**; Kuzyk DOI 10.1103/PhysRevLett.90.039902 and DOI 10.1364/OL.28.000135, located metadata but **not accessed** as corrected derivations. |
| Vague memory references | Heuck DOI 10.1103/PhysRevLett.124.160501; Choi DOI 10.1103/PhysRevLett.118.223605; Shim DOI 10.1103/PhysRevX.9.011043; Mabuchi-group temporal trapping DOI 10.1364/OPTICA.473276 / arXiv:2203.11909: all located and relevant **full text** inspected. |

The generic **Handbook of Optics chapter remains unidentified** from the supplied description. The historical Zakharov–Shabat paper was located as a publisher scan, **abstract only**, but no DOI/arXiv was found; the active theorem is anchored to Magland instead. The NIST event is located, **abstract only**, without an assigned DOI/arXiv or accessible proof. These exceptions are explicit leads, not invented bibliographic identifiers.

Critical full-text gaps remain for Epstein, Brenne–Skaar, Shapiro 2006 and corrected original Kuzyk bounds; Li–Ruths–Glaser's main text was read, but its optimization supplement was not. Some comparison sources remain abstract-only where the active statements need only the abstract. No inaccessible full text was used to assert a theorem's exact scope. Retrieval failures and hashes are recorded separately from reading judgments in [sources.json](../runs/2026-10-13-gpt-b-novelty-literature/sources.json).

## Search log and reproducibility

Searches were live on 2026-10-13, using primary publisher pages, arXiv, author copies and institutional repositories. Neighbouring searches included NMR ensemble control and inverse scattering; codirectional optical filtering; mathematical LLE existence/continuation; coherent versus incoherent temporal filtering; molecular sum rules; and geometric electromagnetic bounds. Full-text searches targeted equations, metric definitions, normalization, theorem statements and assumptions. Relevant equations in scanned PDFs were inspected as rendered pages.

The complete recorded query batches are in [searchlog.json](../runs/2026-10-13-gpt-b-novelty-literature/searchlog.json). Direct identifier retrievals, source URLs and cached hashes are indexed in the same run. This is a bounded search, not an exhaustive proof that a result is absent. No private conversation history was searched or retrieved.

Representative search strings by question:

| Question | Searches |
|---|---|
| Kerr phase/material | `"Single-photon Kerr nonlinearities do not help quantum computation" pdf Shapiro`; `"maximum" "single photon" "Kerr" "bound" transparent`; `"Fundamental limits" "Kuzyk" "25" "1183"`; `"third-order" "sum rules" "rigorous" bulk bound susceptibility 2025 2026`; `"temporal trapping" "quantum" Yanagimoto arxiv` |
| Poling/NMR | `"sum rule" "frequency conversion" "inverse scattering"`; `"Zakharov" "minimum" "binary" pulse`; `"Design of grating-assisted codirectional couplers"`; `"Design of binary long-period fiber grating filters"`; `"Exact broadband excitation of two-level systems by mapping spins to springs" PMC`; `"Apodization of chirped quasi-phasematching" Phillips pdf` |
| Comb/PDE | `Kerr comb conversion efficiency "coupling" "squared" bound`; `"maximum" "conversion efficiency" "all" "Lugiato"`; `"microcomb" "universal" "efficiency" bound`; `"Global continua of solutions" "Lugiato" "two-mode" arxiv`; `"A continuum of bright and dark pulse states" efficiency limit` |
| Selectivity/operator | `"single-stage" "selectivity" "frequency conversion" bound 2024 2025 2026`; `"temporal-mode" "selectivity" "upper bound" proof`; `"single-stage" "selectivity" "Hankel"`; `"Time-frequency optical filtering" Raymer Banaszek arxiv`; `"Reddy" "NIST" "2017" "selectivity"`; thesis searches for `Hankel`, `Slepian`, `prolate`, `exhaustive` |
| Structural bounds | `"nonlinear overlap" "upper bound" cavity second harmonic`; `"fundamental limits" "second harmonic" 2025 2026 structural`; `"nonlinear overlap" "bound" "Maxwell" 2026`; `"Fundamental limits in photonics and electromagnetics: a tutorial"`; `"minimum mode volume" "bounds" dielectric resonators Wang 2020` |

The numerical work is limited to the registered trace-normalization and symbolic balance runs. No depleted-wave, few-photon, full Maxwell or LLE stationary-state simulation was performed. Source-reported experimental and numerical values were checked for meaning and provenance, not replicated. The open derivations, resource decisions and inaccessible proofs are assigned to T-20261013-gpt-b-02 through T-20261013-gpt-b-08.
