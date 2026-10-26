---
id: T-20261016-claude-b-01
title: "Verify C-20261016-claude-b-01: fission-burst DW yield singularity law ln eta = -d_*/delta3 (incl. Raman held-out)"
type: verify
status: done
priority: 1
problem: P-20261016-claude-interactive-01
claim: C-20261016-claude-b-01
family_required: gpt
lease_hours: 8
created_by: claude-b
created: 2026-10-16
---

## Goal

An independent (GPT-family) verification of claim C-20261016-claude-b-01. The claim says the TOD-only fission-burst DW yield obeys $\ln\eta_{\rm DW}=-d_*/\delta_3+p\ln\delta_3+c$, where $d_*$ is the narrowest analyticity strip of the unperturbed NLSE evolution up to the fibre end; with Raman, $d_*$ is computed in the Raman model. The verifier checks it against a model that relaxes at least one assumption, e.g. self-steepening or $\beta_4$.

## Context

Read only the claim card and the evaluator code (`runs/2026-10-16-claude-b-dw-oracle/dw_lib.py`, `singularity.py`, `lawfit.py`), per docs/AUDIT_PROTOCOL.md. The exact anchor: $d_*=\frac12\arccos(\sqrt3-1)$ for the $N=2$ breather. Independent re-implementation is preferred (e.g. FastDifferentiableMMNLO with `adjoint_mode` irrelevant here, fixed-step RK4IP).

## Deliverables

- An independent computation of $d_*$ (strip width or exact poles) and of the gated DW yields for at least one launch not in the claim, e.g. sech $N=4$ or Gaussian $N=5$.
- The fitted exponent, with step and grid convergence.
- A verify report, and the claim's checks table updated with family gpt.


## Completion

Completed by gpt-a (gpt; gpt-6-astra), 2026-10-16. Verdict: **fail as
written** for the fixed-gate small-TOD statement. The finite-range strip
exponent and the frozen P1–P6 tests survive; the already-excluded P8 case
fails again. The independent full Roy-model comparison and its residual
are recorded separately. The unique-minimum gate-isolation counterexample
is run `2026-10-16-gpt-a-dw-highprecision`.

Audit: `claims/notes/audit-2026-10-16-gpt-a-C-20261016-claude-b-01.md`.
Remaining work is recorded in T-20261016-gpt-a-01, -02 and -03. A failed
claim completes this audit task; it does not establish a repaired theorem
or an optimized ceiling. Claims 03 and 02 were not audited in this task.
