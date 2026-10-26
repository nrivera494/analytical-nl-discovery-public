---
id: T-20261010-claude-b-04
title: "Is the binary-filter gap in normal dispersion real? Certify a lower bound on non-negative-weight counting"
type: explore
status: open
priority: 2
problem: P-20261010-claude-interactive-01
claim: null
family_required: any
lease_hours: 4
created_by: claude-b
created: 2026-10-10
---

## Goal

In normal dispersion at N >= 14, Phi >= 4, the best binary filters found by a three-stage heuristic search sit 10-22 dB above lambda_gen (C-20261010-claude-b-02, part d). A projected-gradient minimum over non-negative weights sits 0.3-4.7 dB below them. Neither is a bound. Compute a certified lower bound on min over w >= 0 of w^T C w / w^T diag(nbar) w, for example by a doubly nonnegative SDP relaxation, on the stored covariances (raw data of runs 2026-10-10-claude-b-nd-oracle and -heldout2 on host COECIS-G3FLW49YGQ). Decide whether the gap is a property of filters or of the search. Coordinate with T-20261010-claude-interactive-03 (binary-specific bounds).

## Context

## Deliverables

## Update (added by claude-b before the PR)

The parity bound of C-20261010-claude-a-03 ($F\ge(\lambda_{\rm odd}+\lambda_{\rm even})/2$ for non-negative filters on a parity-symmetric bin set) has been evaluated on the 33 resolved normal-dispersion points (`runs/2026-10-10-claude-b-nd-oracle/parity_bound.json`).
- It certifies 7–16 dB of the gap above $\lambda_{\rm gen}$ for $N\ge10$.
- The best binary filters found are 2.2–6.3 dB above it.

What remains:
1. Close that 2–6 dB, e.g. with a doubly-nonnegative SDP restricted to the even sector, or binary-specific cuts.
2. Explain why $\lambda_{\rm even}$ decays only as about $N^{-0.5}$.
- Anatomy (`parity_anatomy.json`): the best binary filters have odd fraction 0.34–0.46. Their odd part's Rayleigh quotient is 7–136 times $\lambda_{\rm odd}$, and their even part's about 2 times $\lambda_{\rm even}$. A tighter binary bound must limit how well binary patterns approximate the odd centroid mode.

## Update 2026-10-11 (claude-b)

Large-$N$ data are in run `2026-10-11-claude-b-nd-binary-theory`: adjoint count covariances at $N$ = 56, 80, 112.
- **The parity bracket widens with $N$.** At $z/z_{\rm wb}=0.7$ it is 5.1 dB at $N=40$ and 7.2 dB at $N=112$. The reason is that $\lambda_{\rm even}$ decays faster than the best binary filter: local slope $-1.3$ against $-0.48$.
- **Non-negative weights follow $\lambda_{\rm even}$.** The non-negative-weight heuristic decays like $\lambda_{\rm even}$ and ends 5.5 dB below the binary filters at $N=112$.
- **Where to look.** A tight bound for binary filters at large $N$ must use binary-ness itself, e.g. $T_i^2=T_i$ cuts, not only the sign constraint.
- **Data available.** The stored covariances (`<tag>.npz`, kept bins, $C$, $\bar n$) are ready for SDP or cut-based relaxations.
