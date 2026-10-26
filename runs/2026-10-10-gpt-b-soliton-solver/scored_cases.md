---
agent: gpt-b
model: gpt-6-astra
family: gpt
---

# Scored soliton cases

All eigenvalues are numerical approximations in their declared spaces. Coarse-cell Ritz minima are not lower enclosures for the whole field. Binary search is heuristic; every reported mask is achievable.

All four readout values and all gaps are in dB. Formula refers to the cutoff-source bound for Raman fundamentals and the exact Kerr restriction for the Kerr row. It has no asserted one-sided physical GNLSE remainder.

| Case | Field minimum | Passive | Amplitude | Best binary | Formula gap | Amplitude gap | Field gap | Run/source |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Kerr fundamental, z/LD=3pi/2 | -19.77281 | -10.85503 | -7.26388 | -6.59037 | 0.67351 | 0.67351 | 13.18244 | `2026-10-10-gpt-b-soliton-kerr`, `pilot/summary.json` |
| Raman fundamental, T0=0.25 ps, 300 K | -12.89104 | -6.81783 | -6.22289 | -5.67810 | 0.54837 | 0.54480 | 7.21294 | `2026-10-10-gpt-b-soliton-solver`, `pilot_finest/batch.json` |
| Held out: T0=0.35 ps, 77 K | -15.05102 | -7.45286 | -5.68745 | -5.21963 | 0.47111 | 0.46783 | 9.83140 | `2026-10-10-gpt-b-soliton-solver`, `held_out/batch.json` |
| Held out: T0=0.2 ps, 150 K | -14.39719 | -7.24542 | -6.22270 | -5.73750 | 0.48985 | 0.48520 | 8.65970 | `2026-10-10-gpt-b-soliton-solver`, `held_out_second/batch.json` |
| Held out: T0=0.4 ps, 225 K, refined source | -14.20018 | -7.16522 | -6.68200 | -5.91302 | 0.77011 | 0.76898 | 8.28716 | `2026-10-10-gpt-b-soliton-solver`, `held_out_third/batch.json` |
| Gaussian N=1.25, Kerr+shock, z/LD=3 | -21.29616 | -11.46415 | -7.62322 | -6.51586 | — | 1.10735 | 14.78030 | `2026-10-10-gpt-b-soliton-gaussian`, `gaussian_N1.25/batch.json` |
| Gaussian N=1.5, Kerr+shock, z/LD=4 | -27.16825 | -16.81616 | -8.80309 | -7.53570 | — | 1.26739 | 19.63255 | `2026-10-10-gpt-b-soliton-gaussian`, `gaussian_N1.5/batch.json` |
| Gaussian N=1.25, Raman, z/LD=3 | -13.76645 | -7.49861 | -6.77623 | -5.85799 | — | 0.91824 | 7.90846 | `2026-10-10-gpt-b-soliton-gaussian`, `gaussian_N1.25_Raman/batch.json` |
| Gaussian N=1.5, Kerr+shock, z/LD=8 | -27.48747 | -20.69734 | -13.36471 | -9.32417 | — | 4.04054 | 18.16330 | `2026-10-10-gpt-b-soliton-gaussian`, `gaussian_N1.5_late/batch.json` |
| Notebook N=1.969 sech, Raman | -14.04392 | -14.01986 | -11.19154 | -9.16002 | — | 2.03152 | 4.88390 | `2026-10-10-gpt-b-soliton-anchor`, `native_50ps/batch_cells03.json` |
| Gaussian N=2, Raman fission, coarse cells | -15.86219 | -15.59704 | -11.36288 | -10.58848 | — | 0.77439 | 5.27371 | `2026-10-10-gpt-b-soliton-gaussian`, `gaussian_N2_Raman_fission/batch_cells03.json` |
| Gaussian N=2, Raman fission, finer cells | -16.13381 | -15.87727 | -12.05782 | -11.00567 | — | 1.05214 | 5.12814 | `2026-10-10-gpt-b-soliton-gaussian`, `gaussian_N2_Raman_fission/batch_cells015.json` |

The notebook row uses 0.3-wide spectral cells, the fission rows use 0.3 and 0.15, and the late Gaussian row uses 0.08. Their quoted eigenvalue gaps are gaps in those restricted readout spaces. Native checks and finer temporal-grid values of their fixed masks are retained separately in the same runs. The third held-out formula uses the quadratic-coth source refinement; the first two use the original linear-coth cutoff.
