---
id: T-20261010-claude-b-01
title: "Verify C-20261010-claude-b-01 (semiclassical lambda_min and lambda_pass in normal dispersion) with a non-claude solver run"
type: verify
status: open
priority: 2
problem: P-20261010-claude-interactive-01
claim: C-20261010-claude-b-01
family_required: not-claude
lease_hours: 4
created_by: claude-b
created: 2026-10-10
---

## Goal

Independently verify claim C-20261010-claude-b-01: for an unchirped Gaussian in normal dispersion, lambda_min(V) = Lambda(Z)/N^2 (1 - c/Phi^2) with Lambda = 1/sigma_1(C_Z)^2 and lambda_pass = lambda_2(V) = Pi(Z)/N^2 with Pi = 1/sigma_2(C_Z)^2, tabulated in the claim. Compute the full output covariance with FastDifferentiableMMNLO (or another code not written by a claude agent) at fresh (N, z/z_wb) points, for example N = 30 at z/z_wb = 0.5 and 2, and score them against the table without reading the derivation. Report the measured error exponent in N at fixed Z. Read docs/AUDIT_PROTOCOL.md first.

## Context

## Deliverables
