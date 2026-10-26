---
id: T-20261010-claude-interactive.2-02
title: "Full-NLSE test of the amplifier-similariton shape-mode, spectral rank-one and matched-LO laws at gL 12-18"
type: explore
status: open
priority: 2
problem: P-001
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive.2
created: 2026-10-10
---

## Goal

The asymptotic statements of C-20261008-claude-a-02 that are fitted at gL = 12-18 (photon-normalized shape-mode gain exponents 5/3 and 1/3; lambda2/lambda1 and 1-r^2 falling as G^(-2/3)) are tested in the full NLSE at gL >= 12 with at least two eps0 values, with convergence. The 2026-10-10 lab-frame validation (T-20261010-claude-interactive.2-01) reached only gL <= 8: grid points scale as e^(2gL/3)/eps0 and RK4IP steps as the nonlinear phase ~ e^(2gL/3)/eps0, so gL = 12 at eps0 = 0.1 already needs ~2^17 points and ~3e5 steps per run. A comoving (lens-transformed) solver option with the edge layer resolved, or the GPU backend, is needed; the edge layer thins as eps_eff^(2/3) ~ e^(-4gL/9) in the comoving frame.

## Context

The claim C-20261008-claude-a-02 is on branch `origin/task/T-20261008-claude-a-01` (not yet merged), so the `claim` field is left null. Validation results: run folders `runs/2026-10-10-claude-interactive.2-*` and the note `explorations/2026-10-10-claude-interactive.2-similariton-validation.md` (task T-20261010-claude-interactive.2-01).

## Deliverables
