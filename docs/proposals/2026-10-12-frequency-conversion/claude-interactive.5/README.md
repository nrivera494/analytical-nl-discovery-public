# Draft problem cards: limits to nonlinear frequency-conversion efficiency (lane: χ(2), resonant and structural bounds)

Proposer: claude-interactive.5 (claude; claude-fable-5-1). Task T-20261012-claude-interactive.5-01. Date 2026-10-12. These are drafts for the orchestrator's selection; none is in `problems/`.

Literature checks were done with four foreground subagents (claude-interactive.5.1: sum rules and quantum control; claude-interactive.5.2: Kerr combs; claude-interactive.5.3: nanophotonic bounds and quantum frequency conversion; claude-interactive.5.5: integrable three-wave conversion laws), one derivation-checking subagent (claude-interactive.5.4, card 02), and by the proposer. Access levels in the cards are those recorded by whoever opened the source.

## Scores (1 = low, 5 = high)

| Card | Target (one line) | Novelty | Impact | Analytic tractability | Oracle readiness |
|---|---|---|---|---|---|
| [01 Poling sum rule](P-20261012-claude-interactive.5-01-poling-sum-rule-efficiency-bandwidth.md) | Log-area bound $\int\ln[1/(1-\eta)]\,d\Delta k\le2\pi\kappa^2L$ on the efficiency–bandwidth trade-off of any poling design, and its fate under pump depletion, pulsed walk-off and loss | 4: the undepleted identity is an NMR theorem not yet written for frequency conversion; the depleted, pulsed and lossy extensions are open | 5: a hard minimum $\kappa^2L$ for any flat-top band, for QFC, adiabatic SFG and chirped OPA | 5: integrable structure, trace-formula hierarchy, Landau–Zener as the achievable point | 2: nothing in the repository, but a transfer-matrix code is minutes of work (scratch check done) |
| [02 Kerr comb bound](P-20261012-claude-interactive.5-02-kerr-comb-efficiency-bound-all-stationary-states.md) | $\eta\le\eta_c^2$ for every stationary LLE state from power balance; tightness over states, pulsed pumps, coupled rings | 4: no bound over states located; the inequality itself is three lines and may be folklore | 4: tells any single-ring microcomb lab its ceiling from the coupling ratio alone; explains the need for coupled rings | 5: the bound is immediate; tightness is a low-dimensional condition on the pump-mode projection | 2: needs an LLE integrator with continuation, a few hundred lines |
| [03 QFC selectivity](P-20261012-claude-interactive.5-03-qfc-single-stage-selectivity-bound.md) | A theorem for the single-stage temporal-mode selectivity ceiling (observed 0.8–0.85) and the purity–efficiency frontier | 4: stated as open in the literature since 2013; only numerics exist | 3: decides whether single-stage pulse gates can ever be good enough, for a specialised community | 3: exact Bessel kernel and Hankel/Slepian structure give a route, unproven | 2: linear coupled-wave PDE plus SVD, cheap to write |
| [04 Pulsed three-wave ceiling](P-20261012-claude-interactive.5-04-pulsed-three-wave-walkoff-conversion-bound.md) | Unconvertible energy fraction of pulsed SFG/SHG/OPA with walk-off and depletion, from the integrable limit, with dispersion and cascaded-phase corrections | 3: the structural law (only the pump's soliton content converts; soliton number = area/π) is published; the explicit energy law for sech or Gaussian inputs and the optimal-shape question are not | 4: direct design rule for thin-film lithium niobate and OPCPA | 3: inverse-scattering asymptotics are heavy; semiclassical soliton ensembles exist | 2: three-envelope split-step code, cheap to write |
| [05 Structural overlap bound](P-20261012-claude-interactive.5-05-structural-bound-cavity-chi2-overlap.md) | Upper bound on the normalized nonlinear overlap $\bar\beta$ of doubly resonant χ(2) cavities, hence a minimum critical power for complete SHG | 4: explicitly stated as unknown by the design literature; the only structural SHG bound is undepleted, 2D and loose | 3: nanophotonic cavity designers; little for fibre labs | 2: needs QCQP or sum-of-squares machinery for a trilinear objective | 1: needs a Maxwell solver and bound code; none in the repository |

## Top three

1. **Card 01, poling sum rule.** It is the only card with a rigorous closed-form bound, a named achievable point (linear chirp, which saturates it exactly in the Landau–Zener limit) and a conservation law for parametric gain that any design must obey, all verified in a scratch check this session. The open parts (pump depletion, pulsed walk-off, loss) are exactly the questions a thin-film lithium niobate designer asks, and the refutation engine is a few hundred lines with adjoint optimization over the poling profile.
2. **Card 02, Kerr comb bound.** The inequality $\eta\le\eta_c^2$ follows from power balance and the one-port input-output relation and is independent of dispersion, Raman and mode crossings, so it is robust; whether it is tight, and how the ceiling moves for pulsed pumps and coupled rings, are sharp, simulation-ready questions. It can be checked against published platicon and bidirectional results as soon as their coupling ratios are read.
3. **Card 03, QFC selectivity.** A decade-old numerical ceiling on an analytically known kernel, with the community itself calling the question open; a proof or a counterexample both matter for quantum pulse gates.

Cards 04 and 05 are in the PI's lane but carry more risk: 04 may be largely answered inside the integrable literature once read in full, and 05 needs tooling the repository does not have.

## Dropped ideas, and why

- **Undepleted efficiency–bandwidth area law** ($\int\eta\,d\Delta k\propto\kappa^2L$): solved by Parseval; stated for χ(2) tapers by Xiong et al., arXiv:1609.09221 (full text, subagent). Kept only as the linear limit of card 01.
- **CW resonator efficiencies** (singly and doubly resonant OPO, cavity SHG): solved classically, and for microresonator SHG by the nonlinear-critical-coupling results of Zhao, Jang, Okawachi & Gaeta, arXiv:2104.12905 (full text, subagent) and Wang et al., Sci. Adv. 2025, DOI 10.1126/sciadv.adu7605 (abstract only).
- **Single-soliton Kerr comb efficiency**: solved (Bao et al. 2014, DOI 10.1364/OL.39.006126; Jang et al. 2021, DOI 10.1364/OL.423654; Kondratiev et al. 2023, arXiv:2209.03707). Folded into card 02 as achievable points.
- **Cascaded (two-stage) QFC selectivity**: solved; temporal-mode interferometry reaches unit selectivity (Reddy, Raymer & McKinstrie, DOI 10.1364/OL.39.002924; Ansari et al., Optica 5, 534 (2018)). Only the single-stage ceiling remains (card 03).
- **OPCPA depletion limit for Gaussian pumps**: the mechanism (asynchronous local conversion cycles) is understood and idler absorption (quasi-parametric amplification, for example arXiv:2207.04147, not accessed) removes back-conversion in practice; the residual lossless-idler question is folded into card 04.
- **Material limits on χ(2)**: solved at the material level (Kuzyk, DOI 10.1103/PhysRevLett.85.1218; Bassani & Scandolo, DOI 10.1103/PhysRevB.44.8446); only the combination with structure is open (card 05, target 3).
- **Time-varying-media frequency conversion bounds**: an efficiency limit for upconversion in dynamic media exists (Qu et al., Phys. Rev. E 2018, located as a PDF, not read) and Hayran & Monticone (arXiv:2205.07142, abstract only) review which linear-time-invariant bounds time variation evades. No clearly open bound was identified in the time available; not proposed.
- **Pump-noise (SPDC and Raman) floors in QFC**: no universal bound, since pump wavelengths can be chosen to avoid in-band parametric noise; not proposed.

## What was not done

- Full texts of Epstein 2004, Kaup–Reiman–Bers 1979, Kaup 1978 (SHG), Bao 2014 and Jang 2021 were not read; each could narrow its card.
- The scratch check behind card 01 is not a registered run and must be repeated as one before any number from it is used.
- The $\eta\le\eta_c^2$ derivation in card 02 has been checked by nobody but the proposer.
