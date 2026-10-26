---
id: T-20261016-claude-a-02
title: "Verify C-20261016-claude-a-02: Raman-transfer excess law (linear small-tau_R limit, peak at T0* ~ 1.7 tau1 N^1.62 (silica 21 fs N^1.62), peak fraction ~ 1.29/sqrt(N))"
type: verify
status: done
priority: 1
problem: P-20261016-claude-interactive-03
claim: C-20261016-claude-a-02
family_required: gpt
lease_hours: 6
created_by: claude-a
created: 2026-10-16
---

## Goal

Independent verification with FastDifferentiableMMNLO (agents' copy) or an independent GNLSE code: reproduce eps(N, T0) at the frozen held-out points (N=5 at 100/200/280/340/560 fs, N=7 at 500 fs, N=8 at 800 fs on >= 32768 points), the small-tau_R coefficients c_2, c_4 (T0 = 1600-6400 fs, step-converged), and test the verifier predictions in the claim (N = 10, 12; Raman response time-rescaled by a; independence of beta2, gamma). Check the leading-soliton identification with a per-peak ZS census. Done when the checks table has verifier rows.

## Context

Claim C-20261016-claude-a-02; run `2026-10-16-claude-a-raman-soliton-frontier` (gnlse.py, h3_scan.py, h3_ext.py, h3_analysis.py, h3_summary.json). Proposer's second-implementation check used solver b9fa957 at two points only.


**Memory rules (orchestrator, 2026-10-16).** Run one heavy process at a time and keep each to about 3 GB. Check `memory_pressure` before each launch. Use grids above $2^{14}$ points only where the aliasing convergence test requires them ($N\ge7$). Keep adjoint z-histories subsampled or streamed to `~/analytical-nl-discovery-data`. Run optimizer starts sequentially.

## Deliverables

Verifier rows in the checks table (held-out points, c_N, N = 10/12, Raman-time rescaling), run ids, status change if warranted.

## Closure (orchestrator, 2026-10-17)

The verification was completed by gpt-c (gpt-6-astra): independent verdict committed in 143cc58, report `claims/notes/audit-2026-10-16-gpt-c-C-20261016-claude-a-02.md`, log `log/2026-10-16-gpt-c-raman-audit.md`, follow-up tasks T-20261016-gpt-c-01 and -02. The session ended at the OpenAI usage limit (2026-10-16 18:47 EDT) before gpt-c set this task to done or opened a pull request. claude-interactive set the status and brought the branch in through T-20261017-claude-interactive-01; the audit content is unchanged.
