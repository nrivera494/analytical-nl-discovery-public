---
agent: gpt-c
model: gpt-6-astra
family: gpt
run_id: 2026-10-17-gpt-c-raman-sharpening
---

# Numerical tables

All numerical entries are from run `2026-10-17-gpt-c-raman-sharpening`. Resolution intervals are numerical sensitivity estimates, not statistical confidence intervals. Peaks are bracketed local duration peaks at the stated output checkpoint.

## Blow–Wood, sech launch

| N | T0* (fs) | Neighbor bracket (fs) | a = f1* sqrt(N) ± resolution | f1* | y* | zN | Split |
|---|---|---|---|---|---|---|---|
| 3 | 123.33 | [113.29, 135.70] | 1.26654 ± 0.00197 | 0.731239 | 0.8903 | 8 | calibration |
| 4 | 197.94 | [180.55, 216.26] | 1.28833 ± 0.00030 | 0.644165 | 0.9862 | 4 | calibration |
| 5 | 286.88 | [259.17, 310.44] | 1.29465 ± 0.00088 | 0.578986 | 1.0632 | 4 | calibration |
| 6 | 387.09 | [348.23, 417.11] | 1.29409 ± 0.00067 | 0.528310 | 1.1346 | 4 | calibration |
| 7 | 496.22 | [447.01, 535.43] | 1.29035 ± 0.00040 | 0.487708 | 1.2047 | 2.5 | calibration |
| 8 | 616.29 | [554.97, 664.74] | 1.28429 ± 0.00043 | 0.454064 | 1.2669 | 2.5 | calibration |
| 9 | 747.47 | [704.85, 771.27] | 1.27716 ± 0.00046 | 0.425719 | 1.3221 | 2.5 | heldout |
| 10 | 881.89 | [796.64, 954.21] | 1.26967 ± 0.00036 | 0.401504 | 1.3834 | 1.75 | calibration |
| 11 | 1030.81 | [975.62, 1067.56] | 1.26168 ± 0.00034 | 0.380411 | 1.4321 | 1.75 | heldout |
| 12 | 1180.65 | [1070.37, 1282.09] | 1.25368 ± 0.00023 | 0.361906 | 1.4880 | 1.4 | calibration |
| 13 | 1346.14 | [1278.83, 1399.34] | 1.24560 ± 0.00028 | 0.345466 | 1.5316 | 1.4 | heldout |
| 14 | 1510.53 | [1374.00, 1645.79] | 1.23757 ± 0.00028 | 0.330755 | 1.5830 | 1.4 | calibration |
| 15 | 1691.75 | [1612.47, 1764.43] | 1.22970 ± 0.00026 | 0.317506 | 1.6226 | 1.4 | heldout |
| 16 | 1868.50 | [1705.83, 2043.24] | 1.22198 ± 0.00027 | 0.305496 | 1.6715 | 1.4 | calibration |

## Descriptive position fits by response and shape

T0* / tau_ref = A N^p, or y* = N^(2-p) / A. All fits here describe the completed data; only training_fit.json supplies the frozen predictive coefficients. Regression intervals use residuals; full-bracket intervals independently vary every peak over its complete neighboring-duration bracket. Neither is a material-parameter confidence interval or a physical asymptotic remainder. HC uses tau_ref = 12.2 fs.

| Response / shape | N values | A | A residual 95% interval | p | p residual 95% interval | p full-bracket sensitivity | y exponent 2-p | Constant y compatible with all brackets |
|---|---|---|---|---|---|---|---|---|
| bw / sech | 3,4,5,6,7,8,9,10,11,12,13,14,15,16 | 1.72072 | [1.69172, 1.75022] | 1.62232 | [1.61459, 1.63005] | [1.48516, 1.75714] | 0.37768 | False |
| hc / sech | 3,4,6,8,12,16 | 1.82005 | [1.80361, 1.83665] | 1.62477 | [1.62028, 1.62926] | [1.51277, 1.91841] | 0.37523 | False |
| as2s3 / sech | 3,4,6,8,12,16 | 1.82355 | [1.66503, 1.99717] | 1.53000 | [1.48502, 1.57498] | [1.28554, 1.74529] | 0.47000 | False |
| bw / gaussian | 3,4,6,8,12,16 | 1.62465 | [1.58692, 1.66328] | 1.62442 | [1.61280, 1.63605] | [1.40921, 1.83079] | 0.37558 | False |

## Response and launch-shape comparisons

Each comparison optimizes duration in both models at equal peak-based N. Gaussian launch energy is sqrt(pi) N^2 in soliton units; sech launch energy is 2 N^2.

| Response / shape | N | Share change vs BW/sech | Resolution interval | Normalized leading-energy change | T0* ratio |
|---|---|---|---|---|---|
| as2s3 / sech | 12 | -5.842% | [-5.918%, -5.766%] | -5.842% | 1.0695 |
| as2s3 / sech | 16 | -6.416% | [-7.032%, -5.799%] | -6.416% | 1.0306 |
| as2s3 / sech | 3 | -3.530% | [-3.818%, -3.242%] | -3.530% | 1.1990 |
| as2s3 / sech | 4 | -3.973% | [-4.253%, -3.694%] | -3.973% | 1.1961 |
| as2s3 / sech | 6 | -4.410% | [-4.731%, -4.088%] | -4.410% | 1.1612 |
| as2s3 / sech | 8 | -4.817% | [-4.981%, -4.654%] | -4.817% | 1.1265 |
| bw / gaussian | 12 | +11.637% | [+11.469%, +11.804%] | -1.065% | 0.9503 |
| bw / gaussian | 16 | +12.108% | [+11.883%, +12.334%] | -0.647% | 0.9532 |
| bw / gaussian | 3 | +7.371% | [+6.946%, +7.798%] | -4.845% | 0.9514 |
| bw / gaussian | 4 | +8.720% | [+8.574%, +8.865%] | -3.650% | 0.9522 |
| bw / gaussian | 6 | +10.129% | [+9.966%, +10.293%] | -2.400% | 0.9464 |
| bw / gaussian | 8 | +10.835% | [+10.691%, +10.979%] | -1.775% | 0.9480 |
| hc / sech | 12 | -2.092% | [-2.328%, -1.856%] | -2.092% | 1.0643 |
| hc / sech | 16 | -2.285% | [-2.533%, -2.037%] | -2.285% | 1.0741 |
| hc / sech | 3 | -0.937% | [-1.346%, -0.526%] | -0.937% | 1.0717 |
| hc / sech | 4 | -1.201% | [-1.364%, -1.039%] | -1.201% | 1.0652 |
| hc / sech | 6 | -1.492% | [-1.694%, -1.290%] | -1.492% | 1.0580 |
| hc / sech | 8 | -1.734% | [-1.946%, -1.522%] | -1.734% | 1.0584 |

## Width-selection test

Widths are sech parameters, not intensity FWHM. Tfit comes from an intensity-profile fit; Tarea is inferred from the total-gamma area relation. Rmax is the independently bracketed overlap maximum.

| Response / shape | N | Tfit (fs) | Tfit resolution interval (fs) | Tarea (fs) | FWHM / 1.762747 (fs) | Rmax width (fs) | Tfit / Rmax | Tarea / Rmax |
|---|---|---|---|---|---|---|---|---|
| as2s3 / sech | 12 | 26.634 | [23.421, 31.638] | 25.734 | 26.817 | 19.147 | 1.3911 | 1.3440 |
| as2s3 / sech | 16 | 27.317 | [25.025, 34.589] | 26.312 | 27.524 | 19.147 | 1.4267 | 1.3742 |
| as2s3 / sech | 3 | 24.428 | [23.243, 29.139] | 23.293 | 24.613 | 19.147 | 1.2758 | 1.2166 |
| as2s3 / sech | 4 | 25.000 | [23.180, 29.972] | 23.922 | 25.178 | 19.147 | 1.3057 | 1.2494 |
| as2s3 / sech | 6 | 25.731 | [21.367, 27.631] | 24.724 | 25.908 | 19.147 | 1.3439 | 1.2913 |
| as2s3 / sech | 8 | 26.083 | [22.264, 28.770] | 25.099 | 26.262 | 19.147 | 1.3623 | 1.3109 |
| bw / gaussian | 12 | 23.565 | [21.659, 27.719] | 21.761 | 23.719 | 15.558 | 1.5147 | 1.3988 |
| bw / gaussian | 16 | 24.618 | [22.694, 29.188] | 22.921 | 24.772 | 15.558 | 1.5824 | 1.4733 |
| bw / gaussian | 3 | 20.802 | [18.159, 25.612] | 18.738 | 20.933 | 15.558 | 1.3371 | 1.2044 |
| bw / gaussian | 4 | 21.096 | [19.413, 24.586] | 18.980 | 21.246 | 15.558 | 1.3560 | 1.2200 |
| bw / gaussian | 6 | 21.720 | [19.847, 25.343] | 19.736 | 21.874 | 15.558 | 1.3961 | 1.2686 |
| bw / gaussian | 8 | 22.388 | [20.489, 26.133] | 20.468 | 22.541 | 15.558 | 1.4391 | 1.3156 |
| bw / sech | 10 | 23.709 | [21.839, 25.407] | 21.965 | 23.904 | 15.558 | 1.5240 | 1.4118 |
| bw / sech | 11 | 24.091 | [23.011, 24.844] | 22.395 | 24.261 | 15.558 | 1.5485 | 1.4395 |
| bw / sech | 12 | 24.326 | [22.492, 26.148] | 22.655 | 24.489 | 15.558 | 1.5636 | 1.4562 |
| bw / sech | 13 | 24.681 | [23.646, 25.538] | 23.057 | 24.860 | 15.558 | 1.5864 | 1.4820 |
| bw / sech | 14 | 24.898 | [23.075, 26.875] | 23.301 | 25.065 | 15.558 | 1.6003 | 1.4977 |
| bw / sech | 15 | 25.237 | [24.241, 26.195] | 23.681 | 25.436 | 15.558 | 1.6222 | 1.5222 |
| bw / sech | 16 | 25.427 | [23.629, 27.554] | 23.892 | 25.589 | 15.558 | 1.6344 | 1.5357 |
| bw / sech | 3 | 20.811 | [18.663, 23.281] | 18.741 | 20.955 | 15.558 | 1.3377 | 1.2046 |
| bw / sech | 4 | 21.146 | [19.419, 22.999] | 19.205 | 21.287 | 15.558 | 1.3592 | 1.2345 |
| bw / sech | 5 | 21.779 | [19.975, 23.381] | 19.819 | 21.917 | 15.558 | 1.3999 | 1.2739 |
| bw / sech | 6 | 22.263 | [20.333, 23.839] | 20.353 | 22.411 | 15.558 | 1.4310 | 1.3082 |
| bw / sech | 7 | 22.635 | [20.805, 24.165] | 20.764 | 22.788 | 15.558 | 1.4549 | 1.3347 |
| bw / sech | 8 | 23.032 | [21.147, 24.612] | 21.207 | 23.176 | 15.558 | 1.4804 | 1.3631 |
| bw / sech | 9 | 23.450 | [22.316, 24.120] | 21.676 | 23.600 | 15.558 | 1.5073 | 1.3933 |
| hc / sech | 12 | 26.973 | [25.475, 32.517] | 24.626 | 27.126 | 17.709 | 1.5231 | 1.3906 |
| hc / sech | 16 | 28.504 | [26.863, 34.377] | 26.262 | 28.668 | 17.709 | 1.6096 | 1.4830 |
| hc / sech | 3 | 22.837 | [18.569, 24.918] | 20.275 | 22.984 | 17.709 | 1.2895 | 1.1449 |
| hc / sech | 4 | 23.226 | [19.490, 24.761] | 20.706 | 23.372 | 17.709 | 1.3115 | 1.1692 |
| hc / sech | 6 | 24.357 | [22.977, 29.049] | 21.859 | 24.509 | 17.709 | 1.3754 | 1.2343 |
| hc / sech | 8 | 25.287 | [23.859, 30.283] | 22.842 | 25.440 | 17.709 | 1.4279 | 1.2898 |

## Physical SMF-28 model at the ZS-share optimum

Published dispersion including beta3 and higher orders, HC response, shock, uniform 0.2 dB/km loss, gamma0 = 1.3 / (W km), carrier 1550 nm; zN = 4. Local-ZS soliton content and direct temporal-gate energy are distinct observables. Photon fractions use the full positive-frequency spectral integral and the launch denominator.

| N | Input T0* / FWHM (fs) | Launch E (nJ) | ZS / gated share | ZS / gated E1 (nJ) | Photon fraction | Length (m) | Centroid wavelength (nm) | Minimum global / leading support in bracket (1200–2300 nm) |
|---|---|---|---|---|---|---|---|---|
| 3 | 133.93 / 236.08 | 2.0780 | 0.70194 / 0.70378 | 1.4586 / 1.4625 | 0.73833 | 1.1899 | 1625.72 | 1.00000000 / 0.99999455 |
| 4 | 208.03 / 366.70 | 2.3783 | 0.60893 / 0.61045 | 1.4482 / 1.4518 | 0.65278 | 2.1531 | 1657.17 | 1.00000000 / 0.99999879 |
| 6 | 377.07 / 664.68 | 2.9522 | 0.48881 / 0.48928 | 1.4431 / 1.4445 | 0.54047 | 4.7160 | 1711.94 | 1.00000000 / 0.99999996 |

| N | T0* bracket (fs) | Efficient energy resolution interval (nJ) | Entire interval within frozen 1.35–1.55 nJ | tau_R | shock s | delta3 | alpha L |
|---|---|---|---|---|---|---|---|
| 3 | [128.250, 141.750] | [1.3779, 1.5235] | True | 0.0183978 | 0.00614417 | 0.00771899 | 5.47947e-05 |
| 4 | [199.500, 220.500] | [1.3661, 1.5104] | True | 0.0118443 | 0.00395557 | 0.00496942 | 9.91537e-05 |
| 6 | [356.250, 393.750] | [1.3817, 1.5277] | True | 0.00653446 | 0.00218227 | 0.00274161 | 0.00021718 |

These resolution intervals keep fibre parameters fixed; they do not include spool-to-spool parameter uncertainty.

| N | Launch peak power (kW) | Input photons | Leading photons |
|---|---|---|---|
| 3 | 7.7579 | 1.62145e+10 | 1.19717e+10 |
| 4 | 5.7163 | 1.85576e+10 | 1.21141e+10 |
| 6 | 3.9147 | 2.30358e+10 | 1.24502e+10 |

## Alternative: maximize the directly gated energy fraction

The temporal-gate energy fraction is maximized independently at the same zN = 4 prescription. Its optimum need not equal the local-ZS-content optimum above. No photon-fraction maximum at a grid edge is accepted.

| N | T0* (fs) | Neighbor bracket (fs) | Gated fraction | Gated energy (nJ) | Photon fraction | Length (m) |
|---|---|---|---|---|---|---|
| 3 | 131.035 | [121.500, 135.000] | 0.703866 | 1.49491 | 0.739076 | 1.1390 |
| 4 | 205.705 | [199.500, 220.500] | 0.610509 | 1.46837 | 0.653197 | 2.1053 |
| 6 | 376.759 | [356.250, 393.750] | 0.489307 | 1.44573 | 0.540510 | 4.7082 |

## Fixed launch constraint

Transform-limited sech launch, energy 3 nJ, physical length 2 m, peak power <= 10 kW, duration 150–500 fs. This is a finite scan; its largest accepted sample is not a certified continuous global maximum.

| T0 (fs) | N | ZS energy (nJ) | Gated energy (nJ) | ZS / gated share | Photon fraction |
|---|---|---|---|---|---|
| 150 | 3.81480 | 1.80782 | 1.81104 | 0.60261 / 0.60368 | 0.66863 |
| 160 | 3.93991 | 1.78762 | 1.79121 | 0.59587 / 0.59707 | 0.65958 |
| 175 | 4.12046 | 1.76078 | 1.76347 | 0.58693 / 0.58782 | 0.64700 |
| 200 | 4.40496 | 1.71869 | 1.72250 | 0.57290 / 0.57417 | 0.62829 |
| 250 | 4.92489 | 1.65060 | 1.65420 | 0.55020 / 0.55140 | 0.59699 |
| 300 | 5.39495 | 1.59516 | 1.59907 | 0.53172 / 0.53302 | 0.57141 |
| 400 | 6.22955 | 1.49985 | 1.53051 | 0.49995 / 0.51017 | 0.53613 |

## Frozen BW holdout scores

| N | Predicted / measured a | a error / tolerance | Predicted / measured T0* (fs) | Relative T error | Share / position pass |
|---|---|---|---|---|---|
| 9 | 1.275978 / 1.277158 | +0.001181 / 0.006 | 741.040 / 747.473 | +0.868% | True / True |
| 11 | 1.260470 / 1.261680 | +0.001210 / 0.006 | 1026.193 / 1030.814 | +0.450% | True / True |
| 13 | 1.245137 / 1.245596 | +0.000459 / 0.006 | 1345.646 / 1346.138 | +0.037% | True / True |
| 15 | 1.230527 / 1.229697 | -0.000829 / 0.006 | 1697.289 / 1691.748 | -0.326% | True / True |

The preceding pass flags score central estimates. The following flags additionally require the full numerical resolution envelope or duration bracket to lie within the frozen tolerance.

| N | Share: envelope inside 0.006 | Fitted position: full bracket inside 5% | Original position: full bracket inside 10% |
|---|---|---|---|
| 9 | True | True | True |
| 11 | True | True | True |
| 13 | True | True | True |
| 15 | True | True | True |
