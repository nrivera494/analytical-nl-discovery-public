---
id: T-20261004-gpt-a-01
title: "Replace the analytic GIF625 surrogate with a measured index profile"
type: loose-end
status: open
priority: 3
problem: P-002
claim: null
family_required: any
lease_hours: 8
created_by: gpt-a
agent: gpt-a
model: gpt-6-astra
family: gpt
creator_model: gpt-6-astra
creator_family: gpt
created: 2026-10-04
---

## Goal

Acquire a traceable measured GIF625 refractive-index profile and independently recompute LP01/LP02/LP03 overlaps, modal dispersion and phase mismatch at 1550 nm. The archive setup tested in T-20261004-claude-interactive-02 uses ideal Laguerre-Gauss modes and therefore cannot test a profile-induced deviation of sigma from one. Record data provenance and propagate the uncertainty to the capture prediction.

## Context

Material run `2026-10-04-gpt-a-material`; frozen-capture exploration `explorations/2026-10-04-gpt-a-weak-admixture.md`. No measured index-profile file was supplied with the archive reference.

## Deliverables

A sourced profile, a reproducible mode calculation, registered run metadata and overlap/dispersion summaries, and a clear comparison with the ideal surrogate.
