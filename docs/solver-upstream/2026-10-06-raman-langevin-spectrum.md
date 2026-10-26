# Raman Langevin spectrum with the symmetrized thermal factor

Status in the original: **not carried**. Prepared 2026-10-06 by claude-interactive (claude-opus-5-5) under T-20261004-gpt-b-02 and T-20261006-claude-interactive-01. Evidence: run `2026-10-05-claude-interactive-raman-stochastic` in this repository.

## Commits

| | Commit | Tree |
|---|---|---|
| Original, base | `9c1288712ea9cd7ef858d4e6dff9dea350e9291a` ("Link each figure caption to its generating example notebook", `main` on 2026-10-06) | `ce25a00760964a362767daf5799b6611904c1502` |
| Agents' copy, seed | `b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa` | `ce25a00760964a362767daf5799b6611904c1502` (identical) |
| Agents' copy, change | `d79f150c4dabac6f461f0302eb06b1ec7900bd4e` on `task/T-20261004-gpt-b-02`, [PR #1](https://github.com/nrivera494/FastDifferentiableMMNLO-agents/pull/1) | `ccc8227a27f7fca29031771d4ba65d80cf65eb9e` |
| Same change on the original's history (local only) | `2f632d9`, parent `9c12887`, branch `task/T-20261004-gpt-b-02-on-original-9c12887` in `~/agent-work/solver-raman` on the PI's laptop | `ccc8227a27f7fca29031771d4ba65d80cf65eb9e` (identical) |

`git diff b9fa957 d79f150` and `git diff 9c12887 2f632d9` are byte-identical (SHA-256 `6e005eeeb725ab5899de4670d67b5e6798aea766f8e4a50987540e9e6cb8c0d5`). The patch is 562 KB, almost all of it re-executed notebook outputs.

## Applying it in the original

In a clone of the original:

```sh
git checkout -b raman-langevin-coth 9c12887          # or main, if the five files are unchanged there
gh api repos/nrivera494/FastDifferentiableMMNLO-agents/commits/d79f150c4dabac6f461f0302eb06b1ec7900bd4e \
  -H "Accept: application/vnd.github.patch" > raman-langevin-coth.patch
git am -3 raman-langevin-coth.patch
git diff --stat 9c12887                               # 5 files, +445 −65
git rev-parse HEAD^{tree}                             # ccc8227a… if applied on 9c12887
```

On the laptop, the local commit can be cherry-picked directly, since its parent is `9c12887`:

```sh
git fetch ~/agent-work/solver-raman task/T-20261004-gpt-b-02-on-original-9c12887
git cherry-pick 2f632d9
```

The commit message ends with a `Co-Authored-By: Claude Opus 5.5` trailer; keep or edit it as you prefer.

## What it changes

| File | Change | Meant for the original? |
|---|---|---|
| `example_notebooks/raman_bath_spectrum.jl` | New. `raman_langevin_spectrum_coth(nt, dt, f0, gamma_eff; raman_fraction, tau1, tau2, temperature_K)`: same grid, ordering and prefactor as `PulsePropagation.raman_langevin_spectrum`; thermal factor $\coth(\hbar|\omega|/2k_BT)$; finite $\omega=0$ limit. `tau1`, `tau2` in ps as in `AgarwalRaman`. | Yes, unless the fix moves into `src/` (decision 1). |
| `example_notebooks/soliton_jitter.ipynb` | Cell 6 builds `Cω` from the helper and keeps `Cω_legacy`; cell 7 accumulates both; cell 8 plots both; new cells 9–10 print the comparison table. Re-executed. | Yes. |
| `example_notebooks/squeezing_spectral_filter.ipynb` | New markdown cell 33; cell 34 builds both spectra (passing `tau1`, `tau2`); cell 35 computes both Raman variances; cell 36 prints the three Fano factors. Re-executed. | Yes. |
| `example_notebooks/raman_stochastic_check.jl` | New. Monte Carlo with `stochastic_solve_raman` against the adjoint contraction, for both notebooks' setups. | Optional: a verification script. It needs about an hour of CPU for useful statistics and writes outside the repository. |
| `example_notebooks/raman_stochastic_summary.jl` | New. Summarizes the Monte Carlo output. | Optional, goes with the previous file. |

`src/` is unchanged. In particular, `PulsePropagation.raman_langevin_spectrum` still returns the legacy spectrum, and `stochastic_solve_raman` uses it whenever no `Cω` is passed. The public `RamanLangevin` stochastic path (`src/stochastic.jl`) never passes `Cω`, so stochastic Raman noise through the public interface still has half the zero-point part and no DC term.

## Why

For an observable linear in the phonon noise, the variance depends only on the symmetrized phonon correlator, $C(\omega)+C(-\omega)$, because the weight $|\hat B(\omega)|^2$ is even for real $B$. The thermal expectation values give $\tfrac12[C(\omega)+C(-\omega)] = (\hbar\omega_0/\gamma)\,|\mathrm{Im}\,h_R(|\omega|)|\,\coth(\hbar|\omega|/2k_BT)$. The legacy factor $2n_{th}+\Theta(\omega)$ sums to $4n_{th}+1$ per $\pm\omega$ pair instead of $4n_{th}+2$. The prefactor and the thermal part are right; the zero-point part is halved, and the $\omega=0$ bin, whose correct value is the finite limit $(\hbar\omega_0/\gamma)|\mathrm{Im}\,h_R'(0)|(2k_BT/\hbar)$, is set to zero. The same conclusion was reached independently by gpt-b from the Wigner representation (Drummond and Corney, arXiv:quant-ph/9912095), in T-20261004-gpt-b-02.

## Evidence (run `2026-10-05-claude-interactive-raman-stochastic`)

- **Contraction kernel.** A small kick $\delta A = i\gamma\varepsilon A(z_0,t)\cos(2\pi\Omega t+\varphi)$ at $z_0 = 3, 7$ m and $\Omega = 1, 5, 13.2, 30$ THz, propagated to the end: the finite-difference $\delta n$ equals the discrete-adjoint prediction $(\gamma/N_t)\sum_t B\,\eta$ to $10^{-6}$, and to $1.4\times10^{-4}$ at 30 THz.
- **Sampler covariance.** $E|\mathrm{FFT}\,\eta_k|^2 / (N_t^2\,\Delta z\,\Delta f\,C^{\rm sym}_k) = 1.0003 \pm 0.0002$ over 4000 draws.
- **Monte Carlo** (stopped early by a time limit: 189–192 seeds for jitter, 85–88 for squeezing). It agrees with the adjoint at the 1–2σ level.
  - Jitter: corrected/legacy paired ratio 1.0040–1.0048 (±0.0003) against 1.0043.
  - Squeezing: paired ratio 1.290 ± 0.010 against 1.317 from the discrete adjoint, an unresolved 2.7σ (task T-20261006-claude-interactive-06).

The stochastic check confirms the adjoint contraction for a given spectrum. Which spectrum is physical rests on the argument above.

## Checking it after applying

Run both notebooks top to bottom.

`soliton_jitter.ipynb`, last cell (300 K):

| $L/L_D$ | legacy (s²) | corrected (s²) | ratio |
|---|---|---|---|
| 0.10 | 1.044142e-36 | 1.048627e-36 | 1.00430 |
| 3.10 | 3.107510e-32 | 3.120853e-32 | 1.00429 |
| 7.10 | 3.728351e-31 | 3.744353e-31 | 1.00429 |

`squeezing_spectral_filter.ipynb`, last cell:

| | Fano | dB |
|---|---|---|
| without Raman | 0.215942 | −6.657 |
| with Raman, legacy | 0.267072 | −5.734 |
| with Raman, corrected | 0.282997 | −5.482 |

Raman term ratio corrected/legacy 1.31146.

## Decisions for the PI

1. **Where the fix belongs.** Here it is an example-level helper and `src/` is untouched, following the opt-in rule for agents' solver changes. In the original you may prefer to fix `raman_langevin_spectrum` in `src/backend/stochastic.jl` directly. That would also change `stochastic_solve_raman` without `Cω` and the public `RamanLangevin` path. T-20261004-gpt-b-02 asks for an opt-in `src` option with tests in the agents' copy; when that lands it gets its own ledger row.
2. **The legacy comparison** in both notebooks is there to show the size of the change. It can be dropped once the fix is in `src/`.
3. **Notebook outputs** were produced by a plain-Julia cell runner (Julia 1.12.5, PyPlot `savefig`, PNG outputs), because IJulia crashed on figure display on this laptop. You may want to re-execute in Jupyter before committing to the original.
4. **The squeezing number on the notebook grid is not converged.** The table above reproduces the notebook as it stands. The review found issues this change does not fix; each could become its own change to the original:
   - The default continuous adjoint is 5–14% off for this observable at dz = 1 mm; `adjoint_mode=:discrete_rk4ip` is exact (T-20261006-claude-interactive-03).
   - The sampled Raman kernel integrates to 0.904 instead of 1 at the notebook's dt = 12.2 fs (T-20261006-claude-interactive-02).
   - The self-steepening factor is missing on the Raman noise term (T-20261006-claude-interactive-04).
   - With the filter fixed, the squeezing level moves between −5.44 and −4.72 dB across grids. At $2^{15}$ points it is −5.32 dB (T-20261006-claude-interactive-05).
   - Several notebook cleanups (T-20261006-claude-interactive-07).
