---
id: T-20261006-claude-interactive-07
title: "Fix the remaining issues in squeezing_spectral_filter.ipynb"
type: loose-end
status: open
priority: 3
problem: null
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive
created: 2026-10-06
---

## Goal

The excess-noise cells state their noise model and print their result, the filter is mapped by frequency rather than by index, variables are no longer overwritten, labels are correct, and the vacuum-variance formula guards against non-binary filters.

## Context

Found in the 2026-10-05 review of squeezing_spectral_filter.ipynb (run `2026-10-05-claude-interactive-raman-stochastic`).
- Cells 27–30: the markdown claims about 1.5× more noise and about 5 dB with 10× excess pump noise, but `fano_with_noise` is never printed. The cell's model (independent excess noise per input bin) gives ×1.28 on the notebook grid and ×1.41 converged. A common-mode energy fluctuation with the same input Fano factor gives ×1.69.
- The vacuum-variance formula $\sum|\partial n/\partial\alpha|^2$ is complete only for a 0/1 filter; the stored filter is binary.
- `opt_filt[1196:2371] = reverse(csv)` ties the filter to $N_t = 2^{12}$ and the 50 ps window; the CSV path is relative to the working directory.
- Cell 28 overwrites `λ0` (metres) with 1550 (nanometres), and cell 32 overwrites `filtered_sensitivity` with power-unit values; re-running earlier cells afterwards gives wrong numbers silently.
- Labels: cells 20 and 26 both print "Fano factor of the Raman soliton"; cell 25's y-label; cell 16's "small window" is one 20 GHz bin; cell 14 uses `ifftshift` where `fftshift` is meant (equal for even $N_t$).

## Deliverables

- The notebook fixed in the agents' copy and re-executed, with a ledger row.
- The excess-noise cells print their result and state which noise model they use.
