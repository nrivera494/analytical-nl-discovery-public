# Frozen material prediction scores

Run `2026-10-17-gpt-c-zblan-transfer`; gpt-c / gpt-6-astra / gpt. All material points held out.
Intervals are numerical localization/resolution envelopes, not statistical or material confidence intervals.

| Model | N | Quantity | Frozen value (relative tolerance) | Measured [interval] | Central relative error | Verdict |
|---|---:|---|---:|---|---:|---|
| physical | 3 | f1 sqrt(N) | 1.29 (±10%) | 1.2048 [1.2023, 1.2072] | -6.61% | pass |
| physical | 3 | T0* (fs) | 93.037 (±30%) | 149.8 [144.67, 155.45] | +61.01% | fail |
| physical | 3 | E1* (nJ) | 1.2968 (±45%) | 0.75223 [0.72331, 0.78038] | -42.00% | pass |
| physical | 3 | T1 fit (fs) | 22.056 (±15%) | 39.281 [38.038, 40.595] | +78.10% | fail |
| physical | 3 | T1 area (fs) | 22.056 (±15%) | 34.641 [33.409, 35.977] | +57.06% | fail |
| physical | 4 | f1 sqrt(N) | 1.29 (±10%) | 1.184 [1.1817, 1.1864] | -8.21% | pass |
| physical | 4 | T0* (fs) | 148.27 (±30%) | 226.93 [210.34, 238.99] | +53.05% | fail |
| physical | 4 | E1* (nJ) | 1.2528 (±45%) | 0.75135 [0.71171, 0.81154] | -40.03% | pass |
| physical | 4 | T1 fit (fs) | 22.056 (±15%) | 43.502 [40.917, 45.488] | +97.24% | fail |
| physical | 4 | T1 area (fs) | 22.056 (±15%) | 39.747 [37.309, 41.617] | +80.21% | fail |
| physical | 5 | f1 sqrt(N) | 1.29 (±10%) | 1.1477 [1.1454, 1.15] | -11.03% | fail |
| physical | 5 | T0* (fs) | 212.84 (±30%) | 303.81 [285.55, 319.26] | +42.74% | fail |
| physical | 5 | E1* (nJ) | 1.2197 (±45%) | 0.76028 [0.72176, 0.81001] | -37.67% | pass |
| physical | 5 | T1 fit (fs) | 22.056 (±15%) | 47.686 [45.575, 49.552] | +116.20% | fail |
| physical | 5 | T1 area (fs) | 22.056 (±15%) | 44.161 [41.944, 46.105] | +100.22% | fail |
| physical | 6 | f1 sqrt(N) | 1.29 (±10%) | 1.1074 [1.1051, 1.1096] | -14.16% | fail |
| physical | 6 | T0* (fs) | 285.97 (±30%) | 380.07 [373.12, 394.53] | +32.91% | fail |
| physical | 6 | E1* (nJ) | 1.1933 (±45%) | 0.77076 [0.74084, 0.78664] | -35.41% | pass |
| physical | 6 | T1 fit (fs) | 22.056 (±15%) | 51.418 [50.36, 53.092] | +133.13% | fail |
| physical | 6 | T1 area (fs) | 22.056 (±15%) | 48.117 [47.065, 49.794] | +118.16% | fail |
| reference | 3 | f1 sqrt(N) | 1.29 (±10%) | 1.2848 [1.2823, 1.2874] | -0.40% | pass |
| reference | 3 | T0* (fs) | 93.037 (±30%) | 166.99 [166.67, 167.42] | +79.49% | fail |
| reference | 3 | E1* (nJ) | 1.2968 (±45%) | 0.71961 [0.71634, 0.72245] | -44.51% | pass |
| reference | 3 | T1 fit (fs) | 22.056 (±15%) | 29.136 [28.797, 29.491] | +32.10% | fail |
| reference | 3 | T1 area (fs) | 22.056 (±15%) | 25.014 [24.715, 25.328] | +13.41% | pass |
| reference | 4 | f1 sqrt(N) | 1.29 (±10%) | 1.3045 [1.3019, 1.3071] | +1.13% | pass |
| reference | 4 | T0* (fs) | 148.27 (±30%) | 277.31 [275.96, 280.97] | +87.03% | fail |
| reference | 4 | E1* (nJ) | 1.2528 (±45%) | 0.6774 [0.66723, 0.68207] | -45.93% | fail |
| reference | 4 | T1 fit (fs) | 22.056 (±15%) | 30.93 [30.495, 31.586] | +40.24% | fail |
| reference | 4 | T1 area (fs) | 22.056 (±15%) | 26.572 [26.179, 27.192] | +20.48% | fail |
| reference | 5 | f1 sqrt(N) | 1.29 (±10%) | 1.3097 [1.3071, 1.3123] | +1.53% | pass |
| reference | 5 | T0* (fs) | 212.84 (±30%) | 410.2 [396.14, 425.68] | +92.73% | fail |
| reference | 5 | E1* (nJ) | 1.2197 (±45%) | 0.64255 [0.61785, 0.6666] | -47.32% | fail |
| reference | 5 | T1 fit (fs) | 22.056 (±15%) | 32.348 [31.106, 33.707] | +46.66% | fail |
| reference | 5 | T1 area (fs) | 22.056 (±15%) | 28.014 [26.786, 29.366] | +27.01% | fail |
| reference | 6 | f1 sqrt(N) | 1.29 (±10%) | 1.3083 [1.3056, 1.3109] | +1.42% | pass |
| reference | 6 | T0* (fs) | 285.97 (±30%) | 561.99 [532.26, 616.51] | +96.52% | fail |
| reference | 6 | E1* (nJ) | 1.1933 (±45%) | 0.61583 [0.55954, 0.65125] | -48.39% | fail |
| reference | 6 | T1 fit (fs) | 22.056 (±15%) | 33.537 [31.719, 36.643] | +52.06% | fail |
| reference | 6 | T1 area (fs) | 22.056 (±15%) | 29.246 [27.418, 32.426] | +32.60% | fail |

## Physical operating points

Widths and photon/gated observables are interpolated within the final duration bracket. Length and launch energy follow the fitted duration exactly. The ZS and gate definitions are distinct. No energy maximization under an input constraint was performed for ZBLAN.

| N | T0* (fs) | f1 ZS | f1 gate | E launch (nJ) | E1 ZS (nJ) | E1 gate (nJ) | Photon fraction | L (m) | Centroid (nm) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 149.797 | 0.695568 | 0.700049 | 1.08147 | 0.752232 | 0.757094 | 0.746637 | 1.583 | 2068.58 |
| 4 | 226.925 | 0.592017 | 0.594236 | 1.26914 | 0.751353 | 0.754566 | 0.652321 | 2.7246 | 2129.15 |
| 5 | 303.806 | 0.513284 | 0.51486 | 1.48121 | 0.760282 | 0.762733 | 0.580919 | 3.90679 | 2188.49 |
| 6 | 380.073 | 0.452074 | 0.453206 | 1.70493 | 0.770757 | 0.772754 | 0.524447 | 5.09544 | 2244.55 |

## Controls and support

See `accuracy.json` for all control comparisons and measured numerical orders, `summary.json` for spectral-support and invariant bounds on each peak bracket, and `inventory.json` for every failed or unrun case.
The reference invariant is energy; the physical model invariant is loss-corrected photon number. The legacy forward field `photon_drift` stores the energy drift when shock is disabled; the analysis labels it explicitly.
