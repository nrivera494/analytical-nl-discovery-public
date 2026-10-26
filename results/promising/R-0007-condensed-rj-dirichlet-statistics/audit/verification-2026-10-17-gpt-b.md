---
auditor: gpt-b
model: gpt-6-astra
family: gpt
date: 2026-10-17
verdict: pass-reduced-regime
report_type: cross-family verification, not a clean-context adversarial audit (gate G5 open)
---

# Cross-family verification of C-20261016-claude-interactive.7-01 (pointer)

The full report is [`claims/notes/audit-2026-10-17-gpt-b-C-20261016-claude-interactive.7-01.md`](../../../../claims/notes/audit-2026-10-17-gpt-b-C-20261016-claude-interactive.7-01.md). The PI summary is [`docs/summary-2026-10-17-gpt-b-C-20261016-claude-interactive.7-01.md`](../../../../docs/summary-2026-10-17-gpt-b-C-20261016-claude-interactive.7-01.md). Both are kept with the claim so that existing links stay valid; this file records the verdict for result R-0007.

- **Verdict.** Pass with reduced regime: the exact scalar classical measure identity, and its low-order moments at the tested parameters. The proposer's family is claude (claude-interactive.7); the verifier's family is gpt.
- **Task.** The verify task T-20261016-claude-interactive.7-07.
- **Why it is a verification and not a G5 audit:**
  - its author calls it "simulation verification, not a completed promotion audit";
  - no optimization-based counterexample search was run;
  - besides the claim card, problem file and evaluator, gpt-b read the metadata of the proposer's cited runs. It read no proposer notes, logs, scripts or PR descriptions.
- **What was done:**
  - an independent proof;
  - direct sampling of the measure at $M=6$–36;
  - resonant Hermite–Gauss dynamics at $K=4$, 5, 6 with two disorder strengths;
  - a failed 200-phase holdout, its 800-phase enlargement, and a fresh 400-phase holdout;
  - the full non-resonant tensor;
  - non-condensed and two-ground-mode attacks;
  - step, quadrature and conservation checks;
  - a second-solver check against the agents' solver at b9fa957.
- **Run.** `2026-10-17-gpt-b-dirichlet`. Its prior-art check is in `2026-10-17-gpt-b-gge/literature.md`.
- **Excluded from the sign-off:**
  - the quantum reduced-state reading;
  - the vector and polarization corollaries;
  - automatic equilibration;
  - a uniform long-length full-fibre error.
- **Left open by gpt-b.** The calibrated physical-fibre adversarial search, task T-20261017-gpt-b-01.
