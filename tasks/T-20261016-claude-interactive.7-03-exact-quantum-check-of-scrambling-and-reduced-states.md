---
id: T-20261016-claude-interactive.7-03
title: "Exact quantum check of the scrambling length and the reduced states of thermalized light (small M)"
type: explore
status: open
priority: 2
problem: P-20261016-claude-interactive.7-01
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive.7
created: 2026-10-16
---

## Goal

Exact quantum propagation of a few-mode Kerr system from (a) a coherent state and (b) a per-mode dephased coherent state, compared with truncated Wigner (TWA) and with the conjectures of the card:
- the mean-field collapse length z_E against ln(n) (predicted slope 1/(2 lambda_1), with lambda_1 the classical Lyapunov exponent), against the sqrt(n) law in a regular regime;
- the dephased input reaching phase-invariant thermal-like reduced states at the kinetic length, independent of n;
- the purity of one mode and the entanglement entropy against the thermal entropy of the reduced state;
- the few-excitation condensed regime, where TWA should fail (E' comparable to E'_vac).

## Context

Exploration note explorations/2026-10-16-claude-interactive.7-quantum-rj-state.md, Sections 3 and 5. Cosme & Fialko, PRA 90, 053602 (2014) did a related Bose-Hubbard check (M = 4, N = 40). Use M <= 6 and N <= 60, propagated sector by sector with sparse Krylov methods: no dense matrices above 4096^2, and keep within the memory rules.

## Deliverables

- A run folder and an exploration note. If a law survives, a claim.
