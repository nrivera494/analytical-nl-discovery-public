# Pre-registration: bandpass-filtered LP01 soliton point (case 3 of T-20261004-claude-interactive-06)

Written by claude-b.1 on 2026-10-04, before any propagation for this case was run. Committed before the run.

## Chosen point

The archive's deepest validated **output-bandpass** (direct-detection) point for an LP01 soliton-like pulse at 1550 nm, the "long-pulse" condition of the arbitrary-output-bandpass study:

- Archive study: `~/Desktop/fall2026_research/ai driven lab work/research_runs/2026-09-23_arbitrary_bandpass/` (`report.md`, `filter_common.jl`, `validate_selected.jl`).
- Fiber: GIF625 model (GRIN, core radius 31.25 um, NA 0.275), scalar LP01, 20 m, 1550 nm, 80 MHz. Mean model: dispersion beta_0..beta_5, Kerr n2 = 2.3e-20 m^2/W, self-steepening, causal Raman (archive `AnalyticRaman` wrapper, exact Fourier kernels). Noise: linearized input vacuum through the discrete adjoint, plus the scalar Raman reservoir (300 K, symmetric fluctuation-dissipation spectrum).
- Input: measured 100 mW source spectrum (`2026-09-23_squeezing/inputs/source_100mw.csv`), 3 nm FWHM Gaussian input prefilter, GDD -0.015 ps^2, 180 mW coupled-equivalent before the prefilter, so about 25.064 mW actually coupled; input intensity FWHM on the grid 1.23 ps.
- Readout: direct photon counting after a unity-peak output bandpass with 50 % points at **1546.5 nm and 1553.5 nm** and logistic power-transmission edges of 0.5 nm 10-90 % width ("edge 0.5"). Partition vacuum of the fractional edges is included. No detector loss.
- Grid: 8192 samples over 80 ps, propagation step 5 mm, Raman reservoir z spacing 2.5 cm (the archive's direct-validation grid).
- Raman model: **oscillator (archive name `AgarwalRaman`) is the primary comparison.** The anisotropic response is a secondary comparison, run only if time allows.

Why this point: the problem card's readout (a) is direct detection after a fixed bandpass, and this is the archive's deepest direct-validated output-bandpass point for an LP01 pulse in the soliton regime at 1550 nm (case 2 of this task covers readout (b)). It is cheap (archive adjoint time 28 s).

## Archive values to be compared (copied before running)

Source: `research_runs/2026-09-23_arbitrary_bandpass/results/final_long_agarwal_deepest_edge0.5.toml` (sha256 `b8d9603d4df21308d8d6d5c6cf24cac7456e3ce4a1fa6bc8d687b4494702b794`).

| Quantity | Archive value (oscillator Raman, edge 0.5) |
|---|---:|
| Coupled input power `pin_mw` | 25.0640130455853 mW |
| Fano factor after the band, `F_filter` (input vacuum + partition vacuum + Raman) | 0.369938248889808 |
| Raman reservoir contribution `raman_F_increment` | 0.05200907054764635 |
| F without reservoir | 0.3179291783421616 |
| Mean photons after the band | 2.0405493668111348e9 |
| Fraction of output energy inside the band `spectral_transmission` | 0.8347171161552088 |
| Optical power after the ideal band (`detected_power_mw/(0.95*0.87*10^-0.3)`) | 20.92105095259975 mW |
| Input FWHM on the grid | 1.23046875 ps |
| Input peak power | 238.25163497653577 W |

Secondary values from the same study (compared if run):

| Quantity | Archive value | Source file (sha256) |
|---|---:|---|
| F, anisotropic Raman, edge 0.5 | 0.41491050276503666 (Raman part 0.09903311057795168; band power 20.874621863978494 mW) | `final_long_anisotropic_deepest_edge0.5.toml` (`9f01344f...`) |
| F, oscillator, sharp edges (edge 0) on the same propagation | 0.3709511900936711 (Raman part 0.051029716155780926) | `final_long_agarwal_deepest_edge0.0.toml` (`693a40f1...`) |
| F, oscillator, edge 0.5, coarse grid 4096 / 40 ps / dz 0.01 m / Raman z spacing 0.05 m | 0.3699508168175295 (Raman part 0.05201353938842226) | `power_long_agarwal_deepest_scale1.0.toml` (`efc944d6...`) |

## What will be reported

The relative differences of F, its Raman part and the band power from the archive values. The solver source at the pinned commit is byte-identical to the archive's `dossier/FastDifferentiableMMNLO for agents/src` (checked with `diff -rq` on 2026-10-04), so agreement at the 1e-8 relative level or better is expected; any relative difference above 1e-6 in F will be reported as a discrepancy and investigated. Checks: total-photon readout (all wavelengths, T = 1) on the same propagation must give F = 1 with a negligible Raman part; a grid/step convergence run.
