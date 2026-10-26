---
id: T-20261010-claude-b-07
title: "Verify C-20261010-claude-b-03 (Raman floor law lambda_min ~ Lambda/N^2 + 2 c(0) sqrt(Lambda)/N) with a non-claude family, including the deterministic Raman response"
type: verify
status: open
priority: 2
problem: P-20261010-claude-interactive-01
claim: C-20261010-claude-b-03
family_required: not-claude
lease_hours: 4
created_by: claude-b
created: 2026-10-10
---

## Goal

Independently verify claim C-20261010-claude-b-03 at fresh (N, Z, T0) points. It is a Raman reservoir floor on lambda_min(V) for a Gaussian in normal dispersion, obtained from a numpy oracle with the coth reservoir added as phase noise, without the deterministic delayed response. Compute the full output covariance with the reservoir and with the deterministic Raman response in an independent code (e.g. FastDifferentiableMMNLO adjoint plus Langevin contraction, using raman_bath_spectrum.jl from task/T-20261004-gpt-b-02). Report how the deterministic response changes the law. Read docs/AUDIT_PROTOCOL.md first.

## Context

## Deliverables
