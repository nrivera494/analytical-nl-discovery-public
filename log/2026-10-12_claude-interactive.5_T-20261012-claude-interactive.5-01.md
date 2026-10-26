---
date: 2026-10-12
agent: claude-interactive.5
model: claude-fable-5-1
family: claude
task: T-20261012-claude-interactive.5-01
duration_min: 90
---

## Did

- Created and claimed T-20261012-claude-interactive.5-01 (explore): draft problem cards on limits to nonlinear frequency-conversion efficiency in the lane "χ(2) and resonant conversion, structural and fundamental bounds", for the PI's 2026-10-12 request.
- Brainstormed about fifteen candidate bounds, then ran four foreground literature subagents and one derivation-checking subagent (claude-interactive.5.4, card 02) (claude-interactive.5.1: trace-formula and quantum-control sum rules; .5.2: Kerr-comb efficiency; .5.3: nanophotonic χ(2) bounds and quantum-frequency-conversion selectivity) plus my own searches on integrable three-wave mixing, OPCPA depletion and time-varying media.
- Wrote five draft cards and a ranked memo under `docs/proposals/2026-10-12-frequency-conversion/claude-interactive.5/`. They are not in `problems/`.
- Ran scratch numerical checks (transfer-matrix, Python, in the session scratchpad; not registered runs) of the anchor identity of card 01: the log-area $\int\ln[1/(1-\eta)]\,d\Delta k$ equals $2\pi\kappa^2L$ for uniform poling below $\kappa L=\pi/2$, drops beyond it by $8\pi$ times the sum of the bound-state eigenvalues, and is saturated by linear chirps whose in-band efficiency follows Landau–Zener.

## Found

- Card 01: the undepleted-pump efficiency–bandwidth sum rule is a transcription of the SU(2) trace formula published for NMR pulse design (Epstein 2004; Epstein & Magland, arXiv:0903.4363); the linear (Parseval) area law is in Xiong et al., arXiv:1609.09221. No statement for frequency conversion or parametric gain was found, and the depleted, pulsed-walk-off and lossy versions are open.
- Card 02: power balance plus the one-port input-output relation gives $\eta\le\eta_c^2$ for every stationary LLE state (derivation sketched in the card, checked by nobody else). No bound over all states was located; published formulas are state-specific and all carry the factor $\eta_c^2$.
- Card 03: the single-stage temporal-mode selectivity ceiling (0.8–0.85) is numerical; Christ et al. 2013 call the single-mode pulse gate question open; no theorem found.
- Card 04: integrable three-wave theory (Kaup 1976; Kaup–Reiman–Bers 1979; Ibragimov, Struthers & Kaup 1998) gives depletion by soliton transfer only, and Buckingham, Jenkins & Miller give the soliton count as area over π; a second search (subagent claude-interactive.5.5) found no explicit converted-energy law for sech or Gaussian inputs and no SHG walk-off ceiling. Novelty confidence low.
- Card 05: Lin et al. 2016 state explicitly that no upper bound on the cavity nonlinear overlap is known; the only structural SHG bound (Mohajan et al. 2023) is undepleted, 2D and loose.
- Dropped as solved: the undepleted area law, CW resonator efficiencies, single-soliton comb efficiency, cascaded QFC selectivity, OPCPA Gaussian-pump depletion (idler-loss schemes), material χ(2) limits, time-varying-media upconversion limits (no clearly open bound identified).

## Changed

- New: `tasks/T-20261012-claude-interactive.5-01-propose-problem-cards-limits-to-nonlinea.md` (status done in this PR).
- New: five cards and `README.md` under `docs/proposals/2026-10-12-frequency-conversion/claude-interactive.5/`.
- New: this log entry.
- No existing problem cards or claims edited. No generated files touched.

## Not verified

- The $\eta\le\eta_c^2$ bound of card 02: derived by the proposer and confirmed by derivation by a same-family subagent (claude-interactive.5.4), which also supplied the exact identity $\eta=\eta_c^2-|t-(1-\eta_c)|^2$ and corrected the Raman-plus-shock statement; not yet checked by another family, and a crude LLE scratch integration in the scratchpad did not reach converged stationary states for two of three cases (not a run). To be checked by an LLE run with Newton-converged soliton and dark-pulse states.
- The bound-state term of card 01's trace formula: its normalization ($8\pi\sum_k\mathrm{Im}\,\xi_k$ in $\Delta k$) was confirmed only by a scratch check on box potentials with one and two bound states; a derivation is still needed when the first claim is written.
- The scratch check of card 01 is not a registered run; it must be repeated under `runs/` before any number from it is cited.
- Access levels marked "(subagent)" are those reported by the subagents; I did not open those texts myself.
- Full texts not read that could narrow cards: Epstein 2004; Kaup, Reiman & Bers 1979; Bao et al. 2014; Jang et al. 2021; Reddy's 2017 thesis; Chao et al. 2022 review.

## Loose ends

- Selection of cards into `problems/` is the orchestrator's; no task created for that.
- Oracle code for cards 01–04 (χ(2) transfer-matrix and three-wave split-step, LLE with continuation, linear pulse-gate Green function): to be created as tasks only if a card is selected; none created now to avoid queue noise.
