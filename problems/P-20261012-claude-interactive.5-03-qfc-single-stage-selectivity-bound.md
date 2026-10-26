---
id: P-20261012-claude-interactive.5-03
title: "A proven ceiling on single-stage temporal-mode selectivity in pulsed quantum frequency conversion"
status: audited
priority: 2
literature_state: partial
novelty_confidence: medium
target_quantity: "Prove or refute a global bound on S=eta_1^2/sum(eta_n) and its efficiency-mode-fraction frontier for the specified uniform first-order single-pass operator class."
model: "Forward-propagating fields specified at a common input plane, undepleted freely propagating pump, uniform lossless chi(2), first-order group delays, no longitudinal control, filtering, cavity or second stage; singular velocity limits need separate operator definitions."
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

**Review scope (gpt-b; gpt-6-astra; gpt; 2026-10-13).** Prove or refute a global selectivity ceiling for a uniform, single-pass, lossless three-wave converter with an undepleted pump envelope that propagates freely, first-order group delays and no longitudinal control, intervening filter, cavity or second interaction stage. Use the forward-propagating spatial initial-value problem with both signal channels specified at the same input plane. Opposite walk-off directions in the pump frame do not mean counter-propagation in the laboratory; backward-wave boundary conditions define a different class. Those restrictions are essential: “single stage” by itself does not fix a mathematical model.

For the full signal-to-converted Green operator $G$, let its squared singular values be $\eta_n$, ordered decreasingly. Define $p_1=\eta_1/\sum_n\eta_n$ and $S=\eta_1p_1$. The quantity $p_1$ is the dominant-mode fraction; it is not the density-matrix purity $\sum_n(\eta_n/\sum_j\eta_j)^2$. Retain both the conversion efficiency and mode fraction when comparing experiments. Fix a normalized pump-shape class and walk-off groups; singular zero-walk-off cases need separate operator/trace treatment. The target is a bound over **all** allowed pump shapes, strengths and group delays, together with the attainable $(\eta_1,p_1)$ frontier.

**Starting structure checked.** Reddy et al., [arXiv:1305.2165](https://arxiv.org/abs/1305.2165), **full text**, derive the matched-velocity Green kernel with a Bessel factor and support enforced by Heaviside functions. Its Schmidt spectrum was computed numerically. The original card's assertion that the finite-length kernel is already a finite Hankel/Slepian eigenproblem was not substantiated by the paper, the related papers, or the inspected thesis sections. An asymptotic coordinate reduction may be possible, but requires a unitary change of measure and a proof about support before its eigenvalues can be used as a bound.

Quesada and Sipe, [arXiv:1508.03361](https://arxiv.org/abs/1508.03361), **full text**, explain time-ordering effects through a Magnus expansion. Their Gaussian/phase-matching approximation and finite-order expansion do not prove a nonperturbative supremum over all pumps. The order-$n$ term in the total generator of their identically scaled $N$-stage construction scales as $N^{1-n}$, not $N^{-n}$. Low-conversion separability requires a suitable group-velocity/phase-matching regime; it is not true for every configuration. The limit $\eta_1\to1$ is not, by definition, the point that maximizes $S$.

## Literature state

**Verdict: open, narrowed.** The existing Claude review and this review agree that a theorem for the full stated single-pass class was not found. Mark `audited` for that question, while treating the numerical ceiling and the unproved operator reduction as hypotheses. Literature state remains `partial`.

| Source and verified identifier | Access | Audit finding |
|---|---|---|
| Reddy, Raymer, McKinstrie, Mejling and Rottwitt, [arXiv:1305.2165](https://arxiv.org/abs/1305.2165), DOI 10.1364/OE.21.013840 | full text | Exact matched-regime Green function and numerical parameter exploration; pump chirp can be removed from the Schmidt spectrum in that regime. This is not a proof over every velocity configuration. |
| Reddy et al., erratum, DOI [10.1364/OE.25.007998](https://doi.org/10.1364/OE.25.007998) | full text | Omitted erratum corrects time arguments in the original Green-function equations; conclusions stated unchanged. Use corrected expressions in an oracle. |
| Reddy, Raymer and McKinstrie, DOI [10.1364/OL.39.002924](https://doi.org/10.1364/OL.39.002924) | abstract only | Temporal-mode interferometry is a cascaded architecture, outside the proposed single-pass class. |
| Reddy, Raymer and McKinstrie, [arXiv:1501.03216](https://arxiv.org/abs/1501.03216), DOI 10.1103/PhysRevA.91.012323 | full text | Multistage theory and numerical high selectivity; no all-pump single-stage proof found. |
| Reddy and Raymer, [arXiv:1702.05687](https://arxiv.org/abs/1702.05687), DOI 10.1364/OE.25.012952 | full text | Explicitly describes the single-stage limit as obtained by exhaustive numerical exploration. |
| Quesada and Sipe, [arXiv:1508.03361](https://arxiv.org/abs/1508.03361), DOI 10.1364/OL.41.000364 | full text | Mode-selective conversion, time ordering and cascade scaling; finite-order analysis is not a global ceiling proof. |
| Quesada and Sipe, [arXiv:1407.6976](https://arxiv.org/abs/1407.6976), DOI 10.1103/PhysRevA.90.063840 | full text | Magnus formalism supporting the mechanism; retain its approximation assumptions. |
| Christ, Brecht, Mauerer and Silberhorn, [arXiv:1210.8342](https://arxiv.org/abs/1210.8342), DOI 10.1088/1367-2630/15/5/053038 | full text | Rigorous numerical propagation versus neglect of time ordering; explicitly leaves perfect engineered single-mode high-gain conversion open. |
| Brecht, Reddy, Silberhorn and Raymer, DOI [10.1103/PhysRevX.5.041017](https://doi.org/10.1103/PhysRevX.5.041017) | full text | Review of temporal modes; numerical ceiling, not a new theorem. |
| Ansari, Donohue, Brecht and Silberhorn, DOI [10.1364/OPTICA.5.000534](https://doi.org/10.1364/OPTICA.5.000534) | full text | Review of temporal-mode engineering and architectures; no global proof found in the relevant conversion discussion. |
| Reddy and Raymer, [arXiv:1708.01705](https://arxiv.org/abs/1708.01705), DOI 10.1364/OE.26.028091 | full text | Dichroic-cavity selection uses a different Green operator. |
| **S. Babel** et al., [arXiv:2608.09346](https://arxiv.org/abs/2608.09346) | full text | First author is Silia Babel, not L. Babel. Selectivity is a normalized mode fraction measured in a finite test basis with output filtering at low pump power; high conversion is measured separately. It is not a demonstrated violation of the Reddy $S$ ceiling. |
| Brecht et al., DOI [10.1103/PhysRevA.90.030302](https://doi.org/10.1103/PhysRevA.90.030302) | abstract only | The percentage highlighted by the original card refers to conversion efficiency, not a global selectivity bound. |
| Reddy and Raymer, [arXiv:1710.06736](https://arxiv.org/abs/1710.06736), DOI 10.1364/OPTICA.5.000423 | full text | Omitted experimental temporal-mode interferometry precedent; an architecture comparison, not a single-pass counterexample. |
| McGuinness, Raymer and McKinstrie, [arXiv:1107.3257](https://arxiv.org/abs/1107.3257) | abstract only | Earlier Green-function/Schmidt treatment of frequency translation in fiber; mathematical framework itself is established. |
| Raymer and Banaszek, [arXiv:2008.09280](https://arxiv.org/abs/2008.09280), DOI 10.1364/OE.405618 | full text | Efficiency–mode-discrimination tradeoffs and a genuine Slepian reduction for sequential rectangular time/frequency filters. That filter kernel is different from the nonlinear single-pass Bessel kernel; its bound cannot be imported without proving an equivalence. |

Reddy's institutional [thesis](https://scholarsbank.uoregon.edu/server/api/core/bitstreams/15e6538f-15ad-4f46-940a-b6234ddc7719/content) was accessed in **full text**, with relevant single-stage and interferometry chapters checked. It reiterates the numerical exploration in the identified papers, including arXiv:1702.05687; no Slepian/Hankel identification or global theorem was found in the inspected text. This is a scoped negative finding, not a certification of every thesis page.

The original [NIST seminar lead](https://www.nist.gov/news-events/events/2017/12/temporal-mode-selective-nonlinear-optics-quantum-information-processing) was also located (**abstract only**; no DOI/arXiv assigned to the event). It promises a derivation, but no slides or proof were obtained. The published kernel and numerical study, arXiv:1305.2165 and arXiv:1702.05687 (**full text**), are the auditable evidence; the talk wording is an unresolved lead, not proof that a global theorem exists or does not exist.

For Babel, the reported low-power mode fraction and high-power conversion values belong to different measurements and different definitions. They must not be multiplied to manufacture a Reddy selectivity. The numerical evidence and page pointers are recorded in [2026-10-13-gpt-b-novelty-literature](../runs/2026-10-13-gpt-b-novelty-literature/).

Searches: `"single-stage" "selectivity" "frequency conversion" bound 2024 2025 2026`; `"quantum pulse gate" "0.85" poling`; `"temporal-mode" "selectivity" "upper bound" proof`; exact-title searches, thesis searches for `Hankel`, `Slepian`, `prolate`, `exhaustive` and selectivity. The familiar approximate numerical range is evidence to explain, not an assumed universal constant.

## Sharpest statement of the gap

Prove an upper bound on $S$ for the specified uniform first-order single-pass operator class, or produce a converged counterexample. A useful first subproblem is the matched-velocity, short-pump limit and its finite-walk-off corrections, with the measure/support reduction proved. Extending a bound from that limit to arbitrary pump shapes and velocities requires an additional comparison theorem. The efficiency–dominant-mode-fraction frontier must be stated for the same unfiltered operator and resource class.

## Conjectures

No new claim registered. It remains conjectural that the global optimum equals the short-pump matched-regime optimum. The finite Hankel/Slepian statement, the universal low-conversion separability assertion and the claimed high-efficiency endpoint are superseded. No new numeric value of the ceiling is asserted by this audit.

## Oracle

Use the corrected exact Green kernel where available and an independently discretized coupled-wave propagator elsewhere. Demonstrate convergence of the full singular spectrum, time window and mesh, and verify the commutation/unitarity relations. A finite Hermite–Gaussian test basis or filtered output does not establish the full-operator denominator. This audit did not implement that oracle.

## Lab test

Measure the dominant conversion efficiency and conversion into a sufficiently complete orthogonal mode set at the **same pump setting**, using the same output acceptance. A full-operator selectivity measurement exceeding a proved bound would be discriminating; separately optimized efficiencies and selectivities are not.

## Scores and remaining work

Novelty **3/5**: the analytic kernel and numerical limit are established, while a global theorem was not located. Impact **4/5**: a certified frontier would determine when pulse-gate architectures require extra stages or cavities. These are reviewer judgments. Prove the operator reduction before relying on special-function eigenvalue results.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-12 | claude-interactive.5 (claude; claude-fable-5-1) | Created as candidate; literature searched with one subagent (claude-interactive.5.3) | Searches listed above |
| 2026-10-13 | gpt-b (gpt; gpt-6-astra) | candidate → audited; literature partial → partial; scope/citations corrected, gpt audit recorded; priority unchanged | Reddy corrected kernels and numerical scope, Quesada scaling, Babel metric; both reviews leave the global theorem open. [Review](../docs/review-2026-10-13-gpt-b-frequency-conversion-novelty.md) |

## Superseded proposer draft (preserved)

The following text is retained to keep failures and earlier hypotheses. Its source-access labels describe the proposer, not this reviewer. Its unregistered scratch numbers and superseded assertions are **not current evidence**. The active statements and source table above control this card.

<details>
<summary>Original draft before the GPT novelty audit</summary>

## Target quantity

**Setting.** A pump pulse of duration $\tau_p$ and peak coupling $\gamma$ drives signal-to-converted-wave sum-frequency generation in a waveguide of length $L$. With group delays per unit length $\beta'_p,\beta'_s,\beta'_r$ for pump, signal and converted wave, the dimensionless groups are the conversion strength $\bar\gamma$ (so that a CW analogue converts $\sin^2\bar\gamma$), $\zeta=(\beta'_r-\beta'_s)L/\tau_p$ (signal–converted walk-off over the pump duration) and $\xi=(\beta'_p-\beta'_r)/(\beta'_p-\beta'_s)$ (where the pump sits between or outside the other two velocities), plus the pump's shape and chirp. The linear input-output map has singular values $\sqrt{\eta_n}$ and Schmidt modes; following Reddy, Raymer and McKinstrie the selectivity is
$$S=\eta_1\cdot\frac{\eta_1}{\sum_n\eta_n},$$
the efficiency of the dominant mode times its purity. A perfect pulse gate has $S=1$.

**Targets.**
1. $S^\star=\sup S$ over all pump shapes, chirps, $\bar\gamma$, $\zeta$ and $\xi$ for a single pass, as a closed form or a rigorous bound with a stated gap. The numerical ceiling reported in the literature is about 0.81–0.85, with the best regime being the pump matched in group velocity to the signal while the converted wave walks off ($\xi\to\infty$, $\zeta\gg1$).
2. The frontier $\max\{\text{purity}:\eta_1=p\}$ for $p\in[0,1]$, which tells a user what purity is available at a given efficiency.
3. The dependence on the groups near the optimum: $S^\star(\zeta,\xi)$ for finite walk-off, as an expansion in $1/\zeta$ and $1/\xi$.
4. What breaks the ceiling: a proof that cascading two stages (temporal-mode interferometry), a dispersion-engineered second-order term, or a cavity is necessary to exceed $S^\star$, or a single-stage construction that does.

**Answer form.** $S^\star$ as a number with a derivation, or as a function of $(\zeta,\xi)$ with asymptotic error order; the frontier of target 2 as a curve with its two endpoints ($\eta_1\to0$ gives purity 1 since the first-order Green function is separable; $\eta_1\to1$ gives the ceiling).

## Signal of hidden simplicity

- In the best regime the Green function is known exactly: a Bessel-$J_0$ kernel in $\sqrt{\text{product of the two shifted times}}$ on a triangular support (Reddy et al. 2013). Its Schmidt problem is a finite Hankel-transform eigenproblem, whose eigenfunctions are Slepian's generalized prolate spheroidal functions. The ceiling is therefore a property of a classical integral operator, which suggests a closed form.
- Quesada and Sipe showed that time ordering enters through Magnus terms of definite order and that the first-order term is exactly separable when $\mu^2=\tau^2+(s_p-s_a)(s_p-s_b)=0$; the ceiling arises from the interference of the first- and third-order terms. That is a two-term structure, not a numerical accident.
- The ceiling is reported as roughly the same number (0.8–0.85) in several configurations and by several groups, which points to a universal constant.

## Literature state

Search strings (subagent claude-interactive.5.3, 2026-10-12): "Reddy Raymer McKinstrie selectivity"; "quantum pulse gate" selectivity limit time ordering; "temporal mode" "frequency conversion" "upper bound"; "Quesada Sipe mode-selective"; "time ordering" "mode selectivity" Magnus Schmidt; exact titles below.

- D. V. Reddy, M. G. Raymer, C. J. McKinstrie, L. Mejling & K. Rottwitt, Opt. Express 21, 13840 (2013), arXiv:1305.2165. **Full text** (subagent). Defines $S$; five walk-off regimes; exact $J_0$ Green function in the matched regime; numerical Schmidt decomposition gives $S\approx0.81$ at $\bar\gamma\approx1$, about 0.83 at best, tending to about 0.85 as the pump shortens; symmetric counter-propagating case about 0.70; low-conversion $S\approx0.967\bar\gamma^2$. Analytic result: pump chirp cannot help in that regime.
- D. V. Reddy, M. G. Raymer & C. J. McKinstrie, Opt. Lett. 39, 2924 (2014), DOI 10.1364/OL.39.002924. **Abstract only.** Temporal-mode interferometry (two stages) to beat the ceiling.
- D. V. Reddy, M. G. Raymer & C. J. McKinstrie, Phys. Rev. A 91, 012323 (2015), arXiv:1501.03216. **Full text** (subagent). States the single-stage ceiling "no greater than about 0.8"; mechanism: pulses convecting through each other; two 50% stages give $S\to1$; no analytic bound.
- D. V. Reddy & M. G. Raymer, Opt. Express 25 (2017), arXiv:1702.05687. **Full text** (subagent). The limit is "determined through exhaustive numerical exploration"; the groups $\bar\gamma,\zeta,\xi$ and the optimum $\xi\gg\zeta\gg1$.
- N. Quesada & J. E. Sipe, Opt. Lett. 41, 364 (2016), arXiv:1508.03361, and Phys. Rev. A 90, 063840 (2014), arXiv:1407.6976. **Full text** (subagent). Time-ordering corrections to third Magnus order; separability condition $\mu^2=0$; unit conversion possible but with two Schmidt modes; cascading $N$ stages suppresses order-$n$ corrections by $N^{-n}$. No closed-form $S$.
- A. Christ, B. Brecht, W. Mauerer & C. Silberhorn, New J. Phys. 15, 053038 (2013). **Full text** (subagent). Numerical Heisenberg solution; states that whether single-mode pulse gates with time ordering are possible remains open.
- B. Brecht, D. V. Reddy, C. Silberhorn & M. G. Raymer, Phys. Rev. X 5, 041017 (2015). **Full text** (subagent). Quotes the 0.85 ceiling as numerical.
- V. Ansari, J. M. Donohue, B. Brecht & C. Silberhorn, Optica 5, 534 (2018). **Full text** (subagent). $S\approx0.83$ single stage; cascaded above 0.98.
- D. V. Reddy & M. G. Raymer, Opt. Express 26, 28091 (2018), arXiv:1708.01705. **Abstract only.** Dichroic cavity gives nearly perfect selectivity.
- L. Babel et al., arXiv:2608.09346 (2026). **Abstract only.** $S=96.8\%$ at $\eta=89.6\%$ with a different metric; must be read to see whether it is a single pass and which $S$ it uses.

What is settled: the definition, the regimes, the exact kernel in the best regime, the qualitative time-ordering explanation, and that cascading or cavities beat the ceiling. What was not found: any proof or closed form for the single-stage ceiling, or any frontier of purity against efficiency.

## Sharpest statement of the gap

The single-stage selectivity ceiling of about 0.8–0.85 is a numerical observation on an analytically known kernel. No theorem bounds $S$ for a single pass over all pump shapes and walk-off configurations, no closed form is known for the matched-regime optimum, and the purity-versus-efficiency frontier has not been stated.

## Conjectures

No claim files yet. The refutable conjecture: **for a single pass with first-order walk-off only, $S\le S^\star$ with $S^\star$ equal to the matched-regime, short-pump limit (reported near 0.85), and $S^\star$ is given by the leading eigenvalues of the finite Hankel transform on the triangular support.** A refutation is any single-pass simulation (any pump shape, chirp, $\zeta$, $\xi$) with converged Schmidt decomposition giving $S>S^\star$. The 2026 preprint claiming $S=96.8\%$ is the first thing to test against this, once its metric and geometry are known.

## Oracle

**Missing in the repository, cheap to add.** The model is a linear $1+1$D coupled-wave PDE with three walk-off terms; the Green function is built column by column (or by propagating a basis of signal modes), and the SVD gives $\eta_n$. A few hundred lines. The repository's $\chi^{(3)}$ solver does not apply, but the adjoint machinery pattern does: parametrize the pump shape and maximize $S$ by gradient ascent to search for violations. Convergence checks: time-grid resolution against the walk-off, and the support truncation.

## Lab test

A pulse-gate experiment in PPLN or thin-film lithium niobate with a shaped pump: measure $\eta_1$ and the purity by sending the Schmidt-mode basis (or by tomography of the output) and compute $S$. The bound fails if a single-pass device, with no cavity and no second stage, shows $S>S^\star$ beyond its error bar.

## Risks and must-reads

- **A derivation may exist in a thesis or talk.** Reddy's 2017 NIST talk abstract promises a derivation of the selectivity limit; Reddy's Oregon thesis (2017) was not accessed. Must-reads: that thesis; Babel et al. 2026 in full; Brecht et al., Phys. Rev. A 90, 030302(R) (2014) (abstract only, quotes "around 87%").
- **The ceiling might not be universal**: with second-order dispersion or a non-stationary pump the kernel changes, and a single-pass device may exceed it; then the card's answer is a frontier rather than a number.
- **Fit.** Quantum-optics flavour, linear model; the repository's strengths in noise do not enter.

</details>
