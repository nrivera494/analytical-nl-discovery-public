# Round 2 plan (2026-10-08)

Set by the PI in chat on 2026-10-08; recorded by claude-interactive. Four agents, about four hours each, started together.

| Agent | Model, effort | Problem | Task (created by the agent) | Question |
|---|---|---|---|---|
| claude-a | claude-opus-5-5, max | P-001 | `T-20261008-claude-a-01` | Noise channel of the amplifier similariton with spontaneous emission, and how attraction changes the noise |
| gpt-a | gpt-6-astra, max | P-001 | `T-20261008-gpt-a-01` | Prove or refute that the amplifier similariton is an attractor; state the basin |
| gpt-b | gpt-6-astra, max | P-20261004-claude-interactive-02 | `T-20261008-gpt-b-01` | Analytical Raman- and gain-driven covariance of a GRIN or step-index multimode soliton's collective coordinates, modal fractions and relative phases |
| claude-b | claude-opus-5-5, max | P-20261004-root-03 | `T-20261008-claude-b-01` | Prove or refute an inequality between filtered Manakov (LP01) and GRIN soliton noise, or whether GRIN can ever beat LP01 |

Each agent creates its own task with `scripts/task.py new` and claims it, because this plan's pull request may not be merged when the agents start.

## Rules for this round

- **Do not edit problem cards.** Two agents work on P-001, and round 1's card edits conflicted. Put proposed card changes in the log entry under "Proposed card changes"; the orchestrator applies them when integrating.
- **Independence.**
  - claude-a builds on the orchestrator's Claude-family sketch in P-001, so its claim must be verified by a non-Claude agent.
  - gpt-a checks that sketch independently as part of its task. That check counts as a cross-family check of the sketch, not of claude-a's claim.
  - Neither P-001 agent reads the other's branch until its own claim or exploration is committed.
- **Solver caveats** (see `docs/solver-upstream/` and the tasks named):
  - The default Raman Langevin spectrum halves the zero-point part; use `raman_langevin_spectrum_coth` (agents' solver branch `task/T-20261004-gpt-b-02`) or an equivalent explicit spectrum.
  - The sampled Raman kernel integrates to 0.904 at dt = 12.2 fs; use dt ≤ 3 fs or check convergence (T-20261006-claude-interactive-02).
  - The default continuous adjoint can be inaccurate for noise observables; use `adjoint_mode=:discrete_rk4ip` (T-20261006-claude-interactive-03).
  - The gain-noise normalization is unbenchmarked; check it against the analytic amplifier energy noise before relying on it.
- **Solver changes** go to the agents' copy only (AGENTS.md rule 14, `docs/SOLVER.md`), with a ledger row.
- **Budget.** About 240 minutes of wall-clock time each; reserve the last 15 for the log, validation, push and pull request.
