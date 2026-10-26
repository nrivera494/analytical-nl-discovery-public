---
id: T-20261008-gpt-a-03
title: "Independently verify the gain-NLSE obstruction and width-mode rates"
type: verify
status: open
priority: 1
problem: P-001
claim: C-20261008-gpt-a-02
family_required: not-gpt
lease_hours: 8
created_by: gpt-a
agent: gpt-a
model: gpt-6-astra
family: gpt
created: 2026-10-08
---

## Goal

Reproduce the odd-field counterexample, paired width/chirp decay and breathing fits, held-out order-six input, and representative finite-length profile-map points in C-20261008-gpt-a-02. Independently check the exact lens transformation and original solver constant-Kerr adapter, with step, grid, window and high-frequency controls; do not confer verification from the proposer's runs alone.

## Context

The width/chirp rate is a paired moment response, not a field-norm convergence exponent. The finite-distance map and the longer wing-resolution checks must be assessed separately. The original uncapped split-step sweep is retained as rejected evidence; do not treat its fits as predictions.

## Deliverables

Reproduce the cited observables under independent step/grid/window controls and new run ids. Relax at least one model assumption, for example by adding an even finite-gain-bandwidth filter: test which parity statements survive and how the moment-rate approximation changes. Do not promote a proposer-family check to independent verification.
