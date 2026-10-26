# Run 2026-10-20-claude-interactive.21-regime-screen

Dimensionless groups for 50-µm, NA 0.2 parabolic GRIN silica (1030 and 1064 nm). They decide which collision null space applies to random-phase light of coherence time $t_c$, and how long the Raman processes take. The run serves the second-family review and the exploration note (§§2.2, 3.4, 4, 5). No propagation.

| Output key (`summary.json`) | Meaning |
|---|---|
| `W_t` | $t_c^2/(\lvert\beta_2\rvert L_{\rm NL})$, temporal weak-turbulence parameter |
| `R_ST` | $\kappa/(t_c^2\delta\beta)$, spatio-temporal resonance parameter; `Omega_ST_THz`, `dlam_ST_nm` |
| `R_d` | $\kappa/(t_c^2\Delta\beta)$, frequency resolution of the disorder-broadened resonance |
| `joint_window_tc_fs` | $[(T_R\lvert\beta_2\rvert L_{\rm NL})^{1/3},\sqrt{\lvert\beta_2\rvert L_{\rm NL}}]$ |
| `Lkin_disorder_over_LNL`, `Ld_over_LNL`, `LD_tc_over_Lkin` | Garnier 2019 kinetic-length scaling and its regime |
| `LR_spec_over_LNL` | in-band Raman spectral-drift length |
| `srs` | noise-seeded SRS threshold $L_{\rm th}$, pump–Stokes walk-off, $L_{\rm kin}/L_{\rm th}$ (added in a re-run) |
| `occupation`, `lattice_theta1_fs` | lead L5: photons per mode and frequency cell; lattice value of $\theta_1$ |

`grin_second_order.py` evaluates the second-order (Raman²) modal-drift formula on 55 Hermite–Gauss modes with RJ populations (`grin_second_order.json`).
