---
date: 2026-10-11
agent: claude-b
model: claude-opus-5-5
family: claude
task: T-20261010-claude-interactive-05
duration_min: 50
---

## Did

This is a continuation of yesterday's session (log `2026-10-10_claude-b_T-20261010-claude-interactive-05.md`) on the item left open there: the best binary filter for a Gaussian in normal dispersion at $N\gg1$. I worked on the same branch, and PR #31 was updated.

1. **Synced the solver submodule** to the agents' copy (FastDifferentiableMMNLO-agents, `b9fa957`, clean), per the updated AGENTS.md.
2. **Anatomy of the optimal weighted readouts** (run `2026-10-11-claude-b-nd-binary-theory`: `mode_anatomy.py`, `coarse_grain.py`, `fig_modes.py`). I examined the optimal even and odd modes of $V^{\rm amp}$, i.e. the readouts behind $\lambda_{\rm even}$, the parity bound and $\lambda_{\rm gen}$, and their dependence on spectral resolution.
3. **A discrete adjoint of the split-step map** for the spectral count covariance (`adjoint_cov.py`).
   - Validated against the finite-difference oracle at N10, $z/z_{\rm wb}=0.7$ to $2\times10^{-9}$, with identical $\lambda_{\rm gen}$ and binary $F$; 15 times faster.
   - Used it for N = 56, 80, 112 at $z/z_{\rm wb}=0.7$; N = 56, 80 at 1.0; N = 40, 56, 80 at 0.3; and N = 40, 56 at 1.5 (`big_points.py`).
   - A harder binary search (`big_search.py`) checked the binary values.
4. **Fits and figures** (`summarize.py`, `fig_scaling.png`, `summary.json`), and updates to C-20261010-claude-b-02 part (d), the exploration note (section 5.1b) and tasks T-20261010-claude-b-04 and -05.

## Found

**1. Three tiers of readout** (z/z_wb = 0.7, N = 20–112; `fig_scaling.png`)

| readout | slope in $N$ | value at $N=112$ |
|---|---|---|
| signed weights ($\lambda_{\rm gen}$, the odd centroid mode of C-20261010-claude-b-02) | $-1.97$ | $N^2\lambda_{\rm gen}$ = 3.554, 3.597, 3.638 at $N$ = 56, 80, 112, converging toward $1/(2K)=3.70$ |
| graded non-negative weights (heuristic optimum) | $-0.70$ overall, $-1.29$ between $N$ = 80 and 112 | 0.045 |
| $\lambda_{\rm even}$ | similar to non-negative weights | 0.060 |
| parity bound $\approx\lambda_{\rm even}/2$ | similar | 0.030 |
| best binary filter found | $-0.43$ ($F\approx1.24N^{-0.43}$) | 0.160 |

- **At $z/z_{\rm wb}=1.0$** ($N\le80$) the four slopes are $-1.96$, $-1.08$, $-0.92$ and $-0.62$.
- **Robustness.** A harder search moves the large-$N$ binary values by $\le1.2\%$. The centroid identity holds to $\le7\times10^{-5}$ at every large-$N$ point.

**2. Consequence for the card's goal** (a fast, tight lower bound on binary filters)
- The parity bound of C-20261010-claude-a-03 is tight to 2–6 dB at $N\le40$, but its bracket widens to 7.2 dB at $N=112$ ($z/z_{\rm wb}=0.7$).
- Binary filters fall 5.5 dB behind the graded non-negative optimum at $N=112$, against 3.6 dB at $N=40$.
- So at large $N$ the binary constraint itself, not only the sign constraint, sets the binary optimum. A tight binary bound must use binary-ness (task T-20261010-claude-b-04).
- **For the lab.** Multi-pixel detection with graded positive post-detection gains can exploit the fringe-locked even mode, which binary masks cannot. This is not the same as a partially transmitting mask, which adds partition noise.

**3. The optimal even readout** (`fig_modes.png`)
- **Shape.** A broad positive weight with strong modulation locked to the interference fringes of the central spectrum.
- **Resolution.** It needs resolution well below the fringe spacing: making the weights constant over a third of a fringe raises $\lambda_{\rm even}$ by about 1.6 times. The smooth odd (centroid) mode barely changes.
- **Sign structure.** It is 92–99% non-negative by weight, but its small negative parts are essential: clipping them raises $F$ from 0.06–0.20 to 0.23–1.75.
- **What failed.** I guessed that the fringe part enters as an $O(\varepsilon)$ admixture. That is not borne out: the fringe-locked part carries 18–34% of the mode at every $N$.

**4. Non-monotonic $N$-dependence at small $Z$.** At $z/z_{\rm wb}=0.3$, $\lambda_{\rm even}$ (no search involved) and the best binary filter are not monotonic in $N$.

| N | $\lambda_{\rm even}$ | best binary |
|---|---|---|
| 40 | 0.152 | 0.352 |
| 56 | 0.247 | 0.400 |
| 80 | 0.132 | 0.278 |

Earlier there was also the N14 "outlier". The cause is presumably commensurability of the central fringe pattern with the line centre; not checked. A power-law fit at small $Z$ is therefore not meaningful.

**5. After breaking** (z/z_wb = 1.5; Nt = 2048 and 4096; 2309 bins at N = 56)
- $\lambda_{\rm even}$ = 0.0925, 0.060, 0.058 at $N$ = 20, 40, 56: it flattens.
- Best binary filter = 0.421, 0.334, 0.235, using wide filters (photon fraction 0.84 at $N=56$).
- The centroid check holds to $8\times10^{-5}$.

**6. Design rule across $Z$** (empirical, Kerr only)
- The best binary filter found is about $1.6/\sqrt N$, within a factor 1.6, for $z/z_{\rm wb}$ = 0.3–1.5 and $N$ = 20–112: about $-5$ to $-8$ dB.
- Fitted slopes: $-0.31$, $-0.43$, $-0.62$, $-0.53$ at $z/z_{\rm wb}$ = 0.3, 0.7, 1.0, 1.5.
- With the 300 K Raman reservoir adding about 0.03 (yesterday's run `2026-10-10-claude-b-nd-raman`), binary filtering of a normal-dispersion Gaussian stays near $-7$ dB at $N\approx100$. The best quadrature ($\lambda_{\min}$, C-20261010-claude-b-01 and -03) is much lower.

## Changed

- **New run** `runs/2026-10-11-claude-b-nd-binary-theory` with `meta.yaml`, `summary.json`, scripts and figures.
- **Updated** C-20261010-claude-b-02 part (d), the exploration note (section 5.1b) and tasks T-20261010-claude-b-04 and -05.
- **PR** #31 description updated.

## Not verified

- **Search.** All binary values are best found, not certified. The non-negative-weight values are heuristic too.
- **Fits.** The slopes are fits over finite ranges; at $z/z_{\rm wb}=0.7$ the even-sector slope is still steepening at $N=112$. There is no theory for the binary law $N^{-0.43}$ or for the even sector.
- **Independence.** Same family as the original claims; the adjoint tool was validated only against my own finite-difference oracle (both numpy), not against the solver.

## Loose ends

- T-20261010-claude-b-04 (updated): a binary-specific bound; the stored large-$N$ covariances are ready for it.
- T-20261010-claude-b-05 (updated): a theory of the fringe-locked readouts and of the binary law.
- **Not tasked.** The small-$Z$ commensurability oscillation of $\lambda_{\rm even}$ could be checked by scanning $N$ finely at fixed $Z$ (adjoint points take seconds there). It belongs with -05.
- **Leftover folder.** A test-output folder `~/analytical-nl-discovery-data/2026-10-11-claude-b-nd-binary-theory-test` could not be removed: a shell hook blocks recursive deletes in home paths. It holds one N20 check and can be deleted.
