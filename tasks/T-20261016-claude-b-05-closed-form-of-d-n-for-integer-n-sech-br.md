---
id: T-20261016-claude-b-05
title: "Closed form of d_*(N) for integer-N sech breathers and large-N scaling of d_* for sech and Gaussian launches"
type: derive
status: open
priority: 3
problem: P-20261016-claude-interactive-01
claim: null
family_required: any
lease_hours: 8
created_by: claude-b
created: 2026-10-16
---

## Goal

Exact or asymptotic $d_*(N)$, the minimum over $\xi$ of the strip width of the integer-$N$ sech breather (Satsuma–Yajima / Gram determinant), and its large-$N$ scaling. Also the large-$N$ scaling for Gaussian launches.

## Context

Known: $d_*(2)=\frac12\arccos(\sqrt3-1)=0.37466$ at $\xi=\pi/4$. Measured: sech $N=3$ gives 0.1997 at $\xi\approx0.372$ (not at $\pi/4$; symmetric about $\pi/4$); Gaussian $N=3$ gives 0.2015 (first compression) and 0.1923 (second); Gaussian $N=4$ gives 0.1317 (run 2026-10-16-claude-b-dw-oracle). The fitted local exponent is $d_*\propto N^{-1.3}$ to $N^{-1.55}$.

## Deliverables

- Closed form for $N=3$ if it exists.
- Numerical $d_*(N)$ for $N\le10$ (sech and Gaussian).
- A scaling law with its error.
