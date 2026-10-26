---
auditor: gpt-b
model: gpt-6-astra
family: gpt
date: 2026-10-18
verdict: pass-reduced-regime
report_type: cross-family verification, not a clean-context adversarial audit (gate G5 open)
---

# Cross-family verification of C-20261018-claude-interactive.7-03 (pointer)

The full report is [`claims/notes/audit-2026-10-18-gpt-b-C-20261018-claude-interactive.7-03.md`](../../../../claims/notes/audit-2026-10-18-gpt-b-C-20261018-claude-interactive.7-03.md). The PI summary is [`docs/summary-2026-10-18-gpt-b-C-20261018-claude-interactive.7-03.md`](../../../../docs/summary-2026-10-18-gpt-b-C-20261018-claude-interactive.7-03.md). Both are kept with the claim; this file records the verdict for result R-0010.

- **Verdict.** Pass with reduced regime, for three statements:
  - the exact displaced-thermal asymptotics;
  - the Fock-diagonal no-go, which is conditional on phase invariance;
  - the small-jitter Sagnac term for a stated measurement.

  The proposer's family is claude (claude-interactive.7); the verifier's family is gpt.
- **Refuted as general statements:**
  - the original generic-Gaussian covariance sufficiency (oriented-Gaussian counterexample);
  - the implication from super-Poissonian statistics to a coherent-state mixture (two counterexamples);
  - the raw-normalization 1% bound (an interior failure at $\varepsilon=0.051$, $\Phi=3$).

  Automatic diagonality after scrambling is unproved.
- **Task.** The verify task T-20261018-claude-interactive.7-04.
- **Why it is a verification and not a G5 audit:**
  - gpt-b read the proposer's run config, meta and summary files as well as the cards and the evaluator;
  - no optimization-based counterexample search was run;
  - gpt-b kept the classification of the actual extracted state, realistic reference imperfections and mixed-law novelty open in T-20261018-gpt-b-03, and did not mark the claim `audited`.

  gpt-b read no proposer scripts, notes, logs or PR descriptions.
- **What was done:**
  - exact displaced-thermal moments at 60 digits, with a Fock oracle;
  - frozen held-out mixedness and occupations;
  - an analytic Wigner-flow oracle and Sobol TWA;
  - the counterexamples above;
  - two-arm exact, Fock and TWA Sagnac references for three readout definitions;
  - extracted-condensate inputs, with phase and direction cross-validated on separate batches;
  - a bounded literature check.
- **Runs.** `2026-10-18-gpt-b-kerr-exact` and `2026-10-18-gpt-b-condensate-squeezing` (`extracted_stage.json`).
