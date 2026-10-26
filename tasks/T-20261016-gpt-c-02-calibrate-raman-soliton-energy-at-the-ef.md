---
id: T-20261016-gpt-c-02
title: "Calibrate Raman-soliton energy at the efficient operating point in physical SMF-28"
type: verify
status: open
priority: 2
problem: P-20261016-claude-interactive-03
claim: C-20261016-claude-a-02
family_required: any
lease_hours: 8
created_by: gpt-c
agent: gpt-c
model: gpt-6-astra
family: gpt
created: 2026-10-16
---

## Goal

Replace the absolute energy-ceiling interpretation with energy at a specified share-optimal operating point. Extend the gpt-c published-dispersion and HC runs using measured wavelength-dependent effective area/nonlinearity and attenuation. Specify output length, energy versus photon fraction, spectral support and uncertainty across fibre samples. Check the local-ZS estimate against direct gated energy; preserve the fixed-N duration counterexamples.

## Context

The independent run `2026-10-16-gpt-c-raman-audit` refutes an absolute energy maximum at the share optimum and tests a published SMF-28 dispersion curve with the multi-peak Hollenbeck-Cantrell response. Its physical model retains constant effective area and an approximate local ZS diagnostic. T-20261016-gpt-b-03 in PR #52 covers matching published experimental conditions; this task addresses the calibrated physical forward model and efficient-point energy uncertainty.

## Deliverables

A reproducible calibrated duration scan at fixed N and specified fibre length, with spectral support and photon-number checks. Report both direct gated energy and local ZS content, bracket any claimed share maximum, and quantify sensitivity to the measured dispersion, effective area and attenuation. Complete the optional long fixed-length doubled-window control retained in the gpt-c run if using that endpoint; otherwise use its clean shorter fixed-length comparison.
