# Frequency-conversion problem cards: selection (2026-10-13)

**Request.** The PI asked on 2026-10-12 for 5–10 candidate problem cards on limits to nonlinear frequency-conversion efficiency. The PI also asked for one card in particular: the maximum single-photon nonlinear phase in a non-dissipative Kerr medium.

**Proposers:**
- claude-interactive (orchestrator);
- claude-interactive.4 (claude-fable-5-1, χ(3) fibre lane, PR #39);
- claude-interactive.5 (claude-fable-5-1, χ(2), resonant and structural lane, PR #40).

The drafts and the proposers' ranked memos are in those PRs under `docs/proposals/2026-10-12-frequency-conversion/<agent>/`.

**Selected** (registered in `problems/` as `candidate`):

| Card | Proposer | Proposer's scores (novelty, impact, tractability, oracle) | Why |
|---|---|---|---|
| P-20261012-claude-interactive.5-01: poling sum rule on the efficiency–bandwidth trade-off | .5 | 4, 5, 5, 2 | An exact Zakharov–Shabat trace-formula bound; the depleted, walk-off and loss versions are open |
| P-20261012-claude-interactive.4-01: maximum dispersive-wave yield from fission as a law in $N\delta_3$ | .4 | 3, 5, 3, 5 | Only scattered data and perturbative rates exist; solver and adjoint ready |
| P-20261012-claude-interactive.5-02: Kerr-comb efficiency bound over all stationary states | .5 | 4, 4, 5, 2 | An energy-balance bound; tightness, pulsed pumping and coupled rings open |
| P-20261012-claude-interactive-02: maximum single-photon nonlinear phase in a non-dissipative Kerr medium | orchestrator | not scored | Requested by the PI; combines material, structural and quantum-dynamical limits |
| P-20261012-claude-interactive-01: conservation-law ceilings on Kerr conversion into a band | orchestrator | not scored | A Hamiltonian ceiling in normal dispersion; solver and adjoint ready |
| P-20261012-claude-interactive.4-02: frequency-jitter floor of soliton self-frequency-shift conversion | .4 | 3, 3, 5, 4 | Two moments of one Raman kernel give a fluctuation–dissipation floor; fits the project's noise work |
| P-20261012-claude-interactive.4-04: Raman-budget bound on blue-band supercontinuum | .4 | 3, 3, 4, 5 | The anomalous-dispersion companion of -01 |
| P-20261012-claude-interactive.5-03: proven ceiling on single-stage temporal-mode selectivity | .5 | 4, 3, 3, 2 | A long-standing numerical ceiling; a proof or a refutation matters |
| P-20261012-claude-interactive.5-05: structural bound on doubly resonant χ(2) overlap | .5 | 4, 3, 2, 1 | The χ(2) companion of the single-photon card's concentration question |

**Not selected:**
- **Bragg-scattering noise–efficiency frontier** (.4-03). Low novelty: the Raman-limited noise figures are largely published (Voss & Kumar), per its proposer.
- **GRIN geometric-parametric-instability depletion ceiling** (.4-05). Novelty 1: Mei et al. 2026 give the fixed-mismatch ceiling.
- **Pulsed three-wave walk-off ceiling** (.5-04). Low novelty: its integrable limit is classical (Kaup–Reiman–Bers), and the remaining part is closer to device optimization.

**Next.** Cross-family (GPT-6 Astra) novelty audits:
- gpt-a: the χ(3) fibre cards (-01, .4-01, .4-02, .4-04);
- gpt-b: the χ(2), resonant, structural and quantum cards (-02, .5-01, .5-02, .5-03, .5-05).
