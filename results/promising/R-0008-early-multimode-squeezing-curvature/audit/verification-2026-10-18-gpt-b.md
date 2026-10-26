---
auditor: gpt-b
model: gpt-6-astra
family: gpt
date: 2026-10-18
verdict: pass-reduced-regime
report_type: cross-family verification, not a clean-context adversarial audit (gate G5 open)
---

# Cross-family verification of C-20261018-claude-interactive.7-01 (pointer)

The full report is [`claims/notes/audit-2026-10-18-gpt-b-C-20261018-claude-interactive.7-01.md`](../../../../claims/notes/audit-2026-10-18-gpt-b-C-20261018-claude-interactive.7-01.md). The PI summary is [`docs/summary-2026-10-18-gpt-b-C-20261018-claude-interactive.7-01.md`](../../../../docs/summary-2026-10-18-gpt-b-C-20261018-claude-interactive.7-01.md). Both are kept with the claim; this file records the verdict for result R-0008.

- **Verdict.** Pass with reduced regime, for the early quadrature prediction $\lambda_{\rm lin}=\sigma_{\max}^{-2}$ and its measured curvature correction $(0.0920\pm0.0039)\,\sigma_{\max}^6/n_0$ in the stated envelope. The proposer's family is claude (claude-interactive.7); the verifier's family is gpt.
- **Refuted or not signed off:**
  - the original exact-Gaussian premise, refuted by exact one-mode Kerr evolution;
  - curvature-free photon counting under multimode exchange, not established;
  - late counting accuracy, unresolved under step refinement.
- **Task.** The verify task T-20261018-claude-interactive.7-02.
- **Why it is a verification and not a G5 audit:**
  - gpt-b read the proposer's run config, meta and summary files as well as the cards and the evaluator;
  - no optimization-based counterexample search was run;
  - gpt-b kept blockers open in T-20261018-gpt-b-01 and did not mark the claim `audited`.

  gpt-b read no proposer scripts, notes, logs or PR descriptions.
- **What was done:**
  - exact one-mode Kerr moments and a Fock oracle;
  - independent 15-mode tangent and nonlinear Wigner ensembles with shared quenched disorder;
  - frozen held-out energies and occupations;
  - an exact three-mode exchange benchmark;
  - stochastic step refinement;
  - a second-solver check against the agents' solver at b9fa957;
  - loss and detection stress tests.
- **Runs.** `2026-10-18-gpt-b-grin-squeezing`, `2026-10-18-gpt-b-kerr-exact`, `2026-10-18-gpt-b-condensate-squeezing`.
