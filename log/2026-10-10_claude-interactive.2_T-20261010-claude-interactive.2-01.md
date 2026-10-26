---
date: 2026-10-10
agent: claude-interactive.2
model: claude-opus-5-5
family: claude
task: T-20261010-claude-interactive.2-01
duration_min: 185
---

## Did

The PI asked (2026-10-10) for a full-NLSE simulation test of the amplifier-similariton results R1-R10 that the orchestrator presented. I am a subagent of claude-interactive.

**Independence and prior reading.**
- I read only the claim cards of C-20261008-claude-a-01/-02 (branch `origin/task/T-20261008-claude-a-01`), the P-001 card (`origin/task/T-20261008-claude-interactive-01`), gpt-a's claim cards and gpt-b's review.
- I did not read claude-a's derivation note, run scripts or log.
- I froze the targets before any production run (`runs/2026-10-10-claude-interactive.2-simval-lib/targets.md`, commit 9b60c6e).

**Setup.**
- Solver: FastDifferentiableMMNLO, agents' copy b9fa957, unmodified.
- Self-steepening, which the solver always applies, was made negligible with a large carrier, $\omega/\omega_0\le10^{-5}$. The damping window was checked to be unreached.

**Run families.**
1. `2026-10-10-claude-interactive.2-gain-noise-mc`: Monte Carlo with the legacy stochastic backend (`ShotNoise` and `GainLangevin`, Kerr on). Cases: $n_s=0.5$ and 1, vacuum-only and ASE-only. `mc_adjoint.jl` repeats route (ii) on the same configuration.
2. `2026-10-10-claude-interactive.2-moment-noise`: discrete-RK4IP adjoint contraction of up to 10 output functionals.
   - Main, held-out and asymptotic seeds, $\varepsilon_0$ from 0.1 down to 0.0125 (noise runs at $gL$ = 2, 4 only; one attraction launch) and $gL\le8$.
   - The realistic seed of P8, with and without self-steepening and with $\gamma=0$.
   - A soft-edge variant, and a gain-bandwidth relaxed-assumption case.
3. `2026-10-10-claude-interactive.2-attraction`: deterministic parabolic launches for R1 (width ODE, Lyapunov function), R3 and R4 (paired energy-scaled runs).
4. `2026-10-10-claude-interactive.2-shape-modes`: paired $\pm\eta$ shape-mode launches for R2 and R5, read out with exact moment functionals. Includes an independent numpy split-step cross-check.

**Write-up.** `explorations/2026-10-10-claude-interactive.2-similariton-validation.md`, with the verdict table, figures and generated tables.

**Scheduling.** Jobs ran from a shared queue (`simval-lib/worker.sh`).
- During the session I added two backward-compatible options to `contract.jl`: the seed-edge softening mode and the gain bandwidth.
- I also fixed an indexing bug in `shapemodes.jl` before any of its results were used.
- Shape-mode runs with $\eta=10^{-3}$ showed a nonlinearity in the $l=0$ block and were repeated with $\eta=10^{-4}$. The $10^{-3}$ runs are kept as the linearity check.
- Under the two-process limit, and with other agents loading the machine, I dropped the most expensive $\varepsilon_0=0.0125$ jobs, the Kerr-off Monte Carlo cases and some redundant runs.

**Resource limit.** At 10:34 the orchestrator asked for at most two concurrent Julia processes. From about 11:00 the machine was heavily oversubscribed by other agents: load average 184 on 10 cores at 11:17. My jobs ran several times slower than in the morning, and the queue was cut to the runs needed for three-$\varepsilon_0$ coverage of each leading-order statement. I stopped two Monte Carlo chains early: kerr_vac at 734 trajectories, kerr_ase at 882, and the two Kerr-off cases not run. All later work used two processes.

## Found

All statements are Claude-family evidence. Full verdict table and numbers: the exploration note.

- **R1 (width ODE, Lyapunov function, convergence of parabolic launches).** Confirmed in the full NLSE.
  - The deviation from the ODE falls with $\varepsilon_0$ (slopes 1.71 to 1.78 (median 1.75)).
  - $V$ is non-increasing for $\varepsilon_0\le0.05$.
  - All parabolic launches approach the asymptote.
- **R2 (linear spectrum).** Confirmed.
  - Decay $g/3$ and frequencies $\sqrt2g/3$, $\sqrt5g/3$, $g$ to $\le0.3\%$ at $\varepsilon_0=0.05$.
  - $l=0$ neutral; $l=1$ is the exact Ehrenfest double root.
  - The $l=3,4$ block maps carry finite-$\varepsilon$ errors that fall with $\varepsilon_0$. Their relative size fluctuates with the oscillation phase of the map.
- **R3.** Confirmed.
  - $\varepsilon_{\rm eff}$ from peak and width decays as $e^{-2\tau/3}$ (slope $-0.666$).
  - The transform-limited bandwidth share decays at $-1.10$ to $-1.14$ per unit $\tau$. Its excess over $\varepsilon_{\rm eff}^2\times$(edge logarithm) shrinks as $\varepsilon_0\to0$.
  - The edge-layer scaling $\propto\varepsilon_{\rm eff}^{2/3}$ (a frozen target of mine, not a claim statement) converges toward the prediction but misses the frozen 5% criterion: slopes -1.60 ($\varepsilon_0=0.1$), -1.07 ($\varepsilon_0=0.05$), -0.70 ($\varepsilon_0=0.025$), -0.52 ($\varepsilon_0=0.0125$) against $-4/9$.
- **R4.** Confirmed: extrapolated asymptotes $\varepsilon_0=0.1$: (0.332, 0.678, 0.339, 0.0066); $\varepsilon_0=0.05$: (0.333, 0.672, 0.335, 0.0024); $\varepsilon_0=0.025$: (0.333, 0.669, 0.334, 0.0009), against $(1/3,2/3,1/3,0)$.
- **R5.** Confirmed through $gL=6$: block structure, $\det M_l=1$ for $l\le2$, oscillatory scaled generator (envelopes $G^{1/3}$, $G^{5/3}$). The $gL=12$-24 exponents were not reached.
- **R6 (exact moment structure).** Confirmed.
  - Energy law and $n_{sp}=2n_s^2+\tfrac12$: exact.
  - Adjoint covariance equals the $W(z)$ moment formula to $2.3\times10^{-5}$.
  - Monte Carlo ASE scale factors 1.013 $\pm$ 0.024 ($T_c$), 0.993 $\pm$ 0.019 ($\Omega_c$).
- **R7 (closed forms and tables).**
  - Closed forms confirmed: ASE parts within 0.55% ($gL=2$, $\varepsilon_0=0.025$), 0.23% ($gL=4$, $\varepsilon_0=0.0125$), 0.58% ($gL=6$, $\varepsilon_0=0.025$).
  - P8 reproduced to all digits (ratio 3.5495).
  - P3/P5 ASE entries converge. The input-vacuum entries exceed the claimed 5% band at $\varepsilon_0=0.1$ (up to +313%), because of the seed's transform-limited bandwidth.
- **R8.** Confirmed for energy, $\Omega_c$ and $T_{\rm comp}$. **Not confirmed** for the shape-mode intensity: its vacuum share oscillates (0.07-0.42 over $gL=2$-8 and $\varepsilon_0=0.025$-0.1) instead of tending to 1/4.
- **R9.** $\lambda_2/\lambda_1$ confirmed at $gL=4$ and 6; the individual $N_0\mathrm{Var}(s_l)$ entries are not ($gL=2$, $\varepsilon_0=0.0125$: $s_1$ ase +19%, $s_3$ in -16%, $s_4$ in -12%; $gL=4$, $\varepsilon_0=0.025$: $s_1$ ase +15%, $s_2$ in +15%; $gL=6$, $\varepsilon_0=0.05$: $s_1$ ase +14%, $s_2$ in +152%, $s_2$ ase +16%, $s_3$ in +32%). At $gL=2$ the main-case ratio converges slowly (-5.3% at $\varepsilon_0=0.0125$, slope 0.80) and the held-out ratio does not converge (-9.1%, -9.4%, -9.5%, -8.4% at $\varepsilon_0$ = 0.1, 0.05, 0.025, 0.0125); the claim's 10% criterion fails there. The rank-one trend is seen to $gL=8$; the $G^{-2/3}$ law at $gL=12$-18 was not tested.
- **R10.** $C_{AA}$ exact; $C_{PP}$ and $1-r^2$ tables confirmed; the $G^{-2/3}$ law was not tested.
- **Relaxed assumptions.**
  - Self-steepening at 1030 nm changes the realistic-seed results by $\le5\times10^{-4}$.
  - Gain bandwidth: at the claim's bound ($gL(\omega_{\rm edge}/\Omega_g)^2=0.05$, asymptotic seed, $\varepsilon_0=0.1$, $gL=6$), $\mathrm{Var}(\Omega_c)$ falls by 1.2% relative to flat gain (claim: roughly 10%; the claim's own drift formula gives about 0.9%).

## Proposed card changes

All rows below are **same-family (Claude) evidence**. Under AGENTS.md hard rule 1 they cannot move either claim to `sim-verified`. I did not edit any claim or problem card.

### C-20261008-claude-a-01 (collective noise)

Proposed check-table rows (all by claude, claude-interactive.2, **same family as the proposer**, 2026-10-10):

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Simulation, core regime | **P1 (energy).** Exact: adjoint input and ASE parts $(1,\,1-1/G)$ to $5\times10^{-4}$ in every run, Kerr on. **P2 (moment formula).** Adjoint contraction equals the $W(z)$ moment formula to $2.3\times10^{-5}$. Monte Carlo ASE scale factors 1.013 $\pm$ 0.024 ($T_c$), 0.993 $\pm$ 0.019 ($\Omega_c$). **P8.** Reproduced to all quoted digits; ratio 3.5495. | claude (claude-interactive.2), same family | 2026-10-10-claude-interactive.2-moment-noise; 2026-10-10-claude-interactive.2-gain-noise-mc | 2026-10-10 |
| Error-scaling exponent | **P3/P5 ASE entries.** Converge with slopes 0.98 to 3.11 (median 1.77) (main) and 1.40 to 3.49 (median 2.15) (held out). **Input entries.** Slopes 1.34 to 1.62 (median 1.45) (main) and 1.39 to 1.75 (median 1.70) (held out); at the smallest $\varepsilon_0$ run the main-case input entries are within 0.4% ($gL=2$, $\varepsilon_0=0.0125$), 0.6% ($gL=4$, $\varepsilon_0=0.0125$), 2.4% ($gL=6$, $\varepsilon_0=0.025$); a soft-edge $\varepsilon_0^{4/3}$ effect and the seed's transform-limited bandwidth ($\varepsilon_0^2\ln$) both contribute. **R7 closed forms (asymptotic seed).** ASE within 0.55% ($gL=2$, $\varepsilon_0=0.025$), 0.23% ($gL=4$, $\varepsilon_0=0.0125$), 0.58% ($gL=6$, $\varepsilon_0=0.025$). With seeds softened at $\delta=\tfrac12\varepsilon_0$ the ASE deviations fall with slopes 1.55 to 2.02 ($gL=2$ and 4), consistent with the stated $O(\varepsilon_0^2\ln)$ (effective slope 1.66 over 0.025-0.1). With $\delta\propto\varepsilon_0^{2/3}$ seeds the slopes are 0.26 to 1.31. | same | 2026-10-10-claude-interactive.2-moment-noise | 2026-10-10 |
| Held-out region | **P5.** ASE entries within 0.2% ($gL=2$, $\varepsilon_0=0.0125$), 0.4% ($gL=4$, $\varepsilon_0=0.025$), 0.2% ($gL=6$, $\varepsilon_0=0.025$). Input-vacuum $\mathrm{Var}(T_c)$ entries are +313% at $\varepsilon_0=0.1$, $gL=6$ and converge as the transform-limited term falls (input slopes 1.39 to 1.75 (median 1.70)), but at the smallest $\varepsilon_0$ run the input entries are still off by up to 1.2% ($gL=2$, $\varepsilon_0=0.0125$), 12.7% ($gL=4$, $\varepsilon_0=0.025$), 27.5% ($gL=6$, $\varepsilon_0=0.025$). | same | 2026-10-10-claude-interactive.2-moment-noise | 2026-10-10 |
| Convergence and artefacts | Main case, $\varepsilon_0=0.05$, $gL=4$, all functionals. Doubling the steps: 1.3e-05 (largest over the covariance entries, $\lambda_2/\lambda_1$ and $1-r^2$). Halving $dt$: 8.0e-08 (largest over the covariance entries, $\lambda_2/\lambda_1$ and $1-r^2$). Edge energy $\le1.4\times10^{-9}$ (time) and $\le5.1\times10^{-9}$ (spectrum). Energy balance $\le3.8\times10^{-5}$. | same | 2026-10-10-claude-interactive.2-moment-noise | 2026-10-10 |
| Second solver or relaxed assumption | **Self-steepening** at 1030 nm (P8): entries change by $\le5\times10^{-4}$. **Gain bandwidth:** Parabolic gain $g(1-\omega^2/\Omega_g^2)$ on the asymptotic seed ($\varepsilon_0=0.1$, $gL=6$, $n_{sp}=1$, noise weight $\lvert g(\omega)\rvert$), relative to flat gain: $gL(\omega_{\rm edge}/\Omega_g)^2=0.05$: $\mathrm{Var}(\Omega_c)$ ratio 0.9881, $\mathrm{Var}(T_{\rm comp})$ ratio 0.9968, $\lambda_2/\lambda_1$ ratio 0.996, $1-r^2$ ratio 1.015. C-01's regime statement says gain filtering at the bound 0.05 damps the centre-frequency noise by roughly 10%; the claim's own drift formula integrated on the asymptote gives about 0.9%. At the bound the full NLSE reduces $\mathrm{Var}(\Omega_c)$ by 1.2% (input part 0.9%, ASE part 1.3%); the output energy is 0.24% below the flat-gain value. This is the size of the drift estimate, about an order of magnitude below "roughly 10%"; the claim's gain-flatness bound is conservative. | same | 2026-10-10-claude-interactive.2-moment-noise | 2026-10-10 |

Proposed text changes:
- **P7.** The statement "below 5% at $\varepsilon_0\in\{0.1,0.05,0.025\}$ for every entry except the $\Omega_c$ input parts" fails for the input-vacuum entries of $\mathrm{Var}(T_c)$ and $\mathrm{Var}(T_{\rm comp})$.
  - Main case: +23% and +11% at $\varepsilon_0=0.1$, $gL=6$. Held out: up to +313%.
  - With the sharper seed family ($\delta=\tfrac12\varepsilon_0$) all main-case $gL=4$ entries fall with slopes 1.71 to 1.82, consistent with $\varepsilon_0^2\ln$, but the $\mathrm{Var}(T_c)$ input entry is still +11.3% at $\varepsilon_0=0.1$. The band fails at $\varepsilon_0=0.1$ for either seed softening.
  - The cause is the seed's transform-limited bandwidth carried through $\beta_2L+D_c$, i.e. the dropped $O(\varepsilon_0^2\ln)$ term with a large coefficient. That bandwidth is log-divergent for a sharp parabola and depends on how the seed edge is softened.
  - Suggested fix: keep the exact $W(0)$ of the actual seed in the input term (R6(b) does this exactly), and state the 5% criterion for the ASE parts only.
- **Regime, gain flatness.** The claim's own drift $-2g\sigma_\omega^2\Omega_c/\Omega_g^2$, integrated on the asymptote at the bound $gL(\omega_{\rm edge}/\Omega_g)^2=0.05$, reduces $\mathrm{Var}(\Omega_c)$ by about 0.9% at $gL=6$, not "roughly 10%". The full NLSE with parabolic gain at that bound gives 1.2% (asymptotic seed, $\varepsilon_0=0.1$, $gL=6$; gain-bandwidth row above). Suggested text: "at the bound, gain filtering changes $\mathrm{Var}(\Omega_c)$ by about 1%".

### C-20261008-claude-a-02 (shape noise)

Proposed check-table rows (claude-interactive.2, **same family**, 2026-10-10):

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Simulation, core regime | **Block maps (asymptotic seed).** Agree with the reduced block ODE: $l\le2$ within 0.3% at $\varepsilon_0=0.05$; $l=3,4$ within the values of the note's table. **Rates** on $\tau\in[3,6]$: decay 0.3332, 0.3338, 0.3326 and frequency 0.4700, 0.7447, 1.0022 ($l=2,3,4$). **Mixing** residual 7.5% ($\varepsilon_0=0.1$), 3.3% ($\varepsilon_0=0.05$), 1.4% ($\varepsilon_0=0.025$). **C-02 P1** (main case): relative (Frobenius) deviation from the frozen matrices: $\varepsilon_0=0.1$: gL2 M0 0.4%, gL2 M2 4.3%, gL2 M3 4.5%, gL4 M0 0.6%, gL4 M2 1.8%, gL4 M3 20.1%, gL6 M0 1.1%, gL6 M2 4.8%, gL6 M3 5.3%; $\varepsilon_0=0.05$: gL2 M0 0.2%, gL2 M2 1.8%, gL2 M3 1.9%, gL4 M0 0.3%, gL4 M2 0.7%, gL4 M3 8.0%, gL6 M0 0.5%, gL6 M2 1.9%, gL6 M3 1.7%; slopes 1.13 to 1.69. **P3** $\lambda_2/\lambda_1$ at $gL=4,6$: 0.369, 0.109 (table 0.3735, 0.1095). **P4** $\varepsilon_0^2C_{PP}/G$ within 1%; $1-r^2$: $gL=2$, $\varepsilon_0=0.0125$: 0.07471 (table 0.07436, 0.5%); $gL=2$, $\varepsilon_0=0.025$: 0.07537 (table 0.07436, 1.4%); $gL=2$, $\varepsilon_0=0.05$: 0.07729 (table 0.07436, 3.9%); $gL=2$, $\varepsilon_0=0.1$: 0.08279 (table 0.07436, 11.3%); $gL=4$, $\varepsilon_0=0.025$: 0.01264 (table 0.01251, 1.0%); $gL=4$, $\varepsilon_0=0.05$: 0.01299 (table 0.01251, 3.8%); $gL=4$, $\varepsilon_0=0.1$: 0.01414 (table 0.01251, 13.1%); $gL=6$, $\varepsilon_0=0.05$: 0.004456 (table 0.004356, 2.3%); $gL=6$, $\varepsilon_0=0.1$: 0.004602 (table 0.004356, 5.7%). | claude (claude-interactive.2), same family | 2026-10-10-claude-interactive.2-shape-modes; 2026-10-10-claude-interactive.2-moment-noise | 2026-10-10 |
| Error-scaling exponent | Block-map error slopes ($\tau\le4$): $l=0$: 1.62 (errors 2.2e-03, 6.9e-04, 2.3e-04 at $\varepsilon_0$ = 0.1, 0.05, 0.025), $l=1$: 1.76 (errors 6.9e-03, 2.1e-03, 6.0e-04 at $\varepsilon_0$ = 0.1, 0.05, 0.025), $l=2$: 1.42 (errors 8.9e-03, 3.2e-03, 1.2e-03 at $\varepsilon_0$ = 0.1, 0.05, 0.025), $l=3$: 1.51 (errors 3.0e-02, 1.1e-02, 3.8e-03 at $\varepsilon_0$ = 0.1, 0.05, 0.025), $l=4$: 1.06 (errors 1.5e-01, 8.4e-02, 3.5e-02 at $\varepsilon_0$ = 0.1, 0.05, 0.025). | same | 2026-10-10-claude-interactive.2-shape-modes | 2026-10-10 |
| Held-out region | **P5** ($\Gamma=1$): $gL=2$, $\varepsilon_0=0.0125$: $\lambda_2/\lambda_1$ 0.390 (table 0.4257), $1-r^2$ 0.062 (table 0.06191), $s_0$ (0.439, 0.380) (table (0.4444, 0.3843)); $gL=2$, $\varepsilon_0=0.025$: $\lambda_2/\lambda_1$ 0.385 (table 0.4257), $1-r^2$ 0.06226 (table 0.06191), $s_0$ (0.437, 0.379) (table (0.4444, 0.3843)); $gL=2$, $\varepsilon_0=0.05$: $\lambda_2/\lambda_1$ 0.386 (table 0.4257), $1-r^2$ 0.0632 (table 0.06191), $s_0$ (0.434, 0.376) (table (0.4444, 0.3843)); $gL=2$, $\varepsilon_0=0.1$: $\lambda_2/\lambda_1$ 0.387 (table 0.4257), $1-r^2$ 0.06631 (table 0.06191), $s_0$ (0.429, 0.373) (table (0.4444, 0.3843)); $gL=4$, $\varepsilon_0=0.025$: $\lambda_2/\lambda_1$ 0.127 (table 0.1256), $1-r^2$ 0.02123 (table 0.0211), $s_0$ (0.441, 0.433) (table (0.4444, 0.4363)); $gL=4$, $\varepsilon_0=0.05$: $\lambda_2/\lambda_1$ 0.130 (table 0.1256), $1-r^2$ 0.02145 (table 0.0211), $s_0$ (0.440, 0.431) (table (0.4444, 0.4363)); $gL=4$, $\varepsilon_0=0.1$: $\lambda_2/\lambda_1$ 0.147 (table 0.1256), $1-r^2$ 0.0221 (table 0.0211), $s_0$ (0.438, 0.429) (table (0.4444, 0.4363)); $gL=6$, $\varepsilon_0=0.05$: $\lambda_2/\lambda_1$ 0.081 (table 0.0757), $1-r^2$ 0.007863 (table 0.007757), $s_0$ (0.442, 0.441) (table (0.4444, 0.4433)); $gL=6$, $\varepsilon_0=0.1$: $\lambda_2/\lambda_1$ 0.087 (table 0.0757), $1-r^2$ 0.008016 (table 0.007757), $s_0$ (0.441, 0.438) (table (0.4444, 0.4433)) | same | 2026-10-10-claude-interactive.2-moment-noise | 2026-10-10 |
| Convergence and artefacts | Shape modes: doubling the steps changes the block maps by at most 3.1e-05 (asymptotic seed, $\varepsilon_0=0.1$, $gL=6$). Linearity: $\eta=10^{-3}$ gives a 1.1% error in $M_0$ at $\varepsilon_0=0.05$, so $10^{-4}$ was used. | same | 2026-10-10-claude-interactive.2-shape-modes | 2026-10-10 |
| Second solver or relaxed assumption | Independent numpy split-step code: rms width, bandwidth and $T$-$\omega$ covariance at all 61 planes within 6.1e-06, 1.1e-05 and 4.3e-04, and the $l=2$ block map within 1.3e-05 (48000 steps). | same | 2026-10-10-claude-interactive.2-shape-modes | 2026-10-10 |

Proposed text changes:
- **P6** ("$\le10\%$ at $\varepsilon_0=0.05$") fails for P3 at $gL=2$: $\lambda_2/\lambda_1$ is 0.825 against 0.987, and the $s_3$, $s_4$ entries are off by 8-28%. It holds at $gL=4$ and 6.
  - The $gL=2$ entries do converge, slowly: $\lambda_2/\lambda_1$ deviates by -5.3%, -9.3%, -16.4%, -28.0% at $\varepsilon_0$ = 0.0125, 0.025, 0.05, 0.1 (slope 0.80). The 9 nonzero $N_0\mathrm{Var}(s_l)$ entries deviate by at most 19% at $\varepsilon_0=0.0125$ ($s_1$, ase), with slopes 0.11 to 0.82.
  - The likely cause is the phase-quadrature noise dropped by Assumption 5. Its weight $(l(l+1)\varepsilon_0/aa')^2$ is largest at $gL=2$.
  - Where the spectral core is cut is not the cause: cutting at the chirp edge instead of $\sqrt5\sigma_\omega$ gives heldout, $gL=2$, $\varepsilon_0=0.05$: 0.386 (rms-edge core 0.386); main, $gL=2$, $\varepsilon_0=0.05$: 0.833 (rms-edge core 0.825). Moving the cut changes the ratio by at most 1.0%, so the cut does not explain the gap.
  - Either restrict P3 to $gL\ge4$ or add that term.
- **P3 entries.** The individual $N_0\mathrm{Var}(s_l)$ entries are not all reproduced. Off by more than 10% at the smallest $\varepsilon_0$ run: $gL=2$, $\varepsilon_0=0.0125$: $s_1$ ase +19%, $s_3$ in -16%, $s_4$ in -12%; $gL=4$, $\varepsilon_0=0.025$: $s_1$ ase +15%, $s_2$ in +15%; $gL=6$, $\varepsilon_0=0.05$: $s_1$ ase +14%, $s_2$ in +152%, $s_2$ ase +16%, $s_3$ in +32%. The $s_1$ ASE entry stays 14-19% high at every $gL$ and does not shrink, although in the claim's leading order it is $\tfrac45$ of C-01's $\mathrm{Var}(\Omega_c)$ entry, which the centroid functional reproduces. Either the Legendre readout over the core picks up non-centroid (edge) noise that the leading order drops, or the claim defines $s_l$ differently; the card should state the readout exactly. $\lambda_2/\lambda_1$ at $gL=4,6$ is not affected at the 3% level.
- **P5 (held out), $gL=2$.** The held-out $\lambda_2/\lambda_1$ stays below the frozen 0.4257, and the deviation barely changes: -9.1%, -9.4%, -9.5%, -8.4% at $\varepsilon_0$ = 0.1, 0.05, 0.025, 0.0125 (effective exponent 0.04 over a factor 8 in $\varepsilon_0$). Under the claim's own P6 rule ("a deviation that does not shrink with $\varepsilon_0$ refutes the corresponding part"), this entry is refuted. The other held-out $gL=2$ entries ($s_0$, $s_2$, $1-r^2$) do converge. Whether the frozen 0.4257 itself is right was not checked (task T-20261010-claude-interactive.2-05).
- **P2 and the $G^{-2/3}$ laws.** No full-NLSE test exists at the stated $gL=12$-18 (T-20261010-claude-interactive.2-02). Up to $gL=8$ the local slopes are $-0.61$ ($\lambda_2/\lambda_1$) and about $-0.9$ ($1-r^2$).
- **Regime, error bound.** The block matrices' error is stated to fall at least as $\varepsilon_0^{4/3}$. For $l\le3$ the measured slopes over $\varepsilon_0=0.1$-0.025 are 1.42-1.76, which meets this. For $l=4$ the slope is 1.25 between $\varepsilon_0=0.05$ and 0.025, both inside the regime $l\varepsilon_0\le0.2$, slightly below $4/3$.

### P-001

- **Oracle section.** Replace "the gain-noise normalization has not been benchmarked" with: `ShotNoise(0.5)` with `GainLangevin(n_s)` is a symmetric-ordered amplifier with $n_{sp}=2n_s^2+\tfrac12$. It was checked with Kerr off (claude-a.1, 2026-10-08) and with Kerr on (run 2026-10-10-claude-interactive.2-gain-noise-mc).
- **Self-steepening.** The solver's Kerr prefactor always includes it. A large carrier, or a constant-Kerr override as in gpt-a's evaluator, is needed to test the pure NLSE.
- **Orchestrator R8.** The inference that the shape-mode intensity share tends to 1/4 is not supported up to $gL=8$: the share oscillates.

## Changed

- New: `runs/2026-10-10-claude-interactive.2-{simval-lib,gain-noise-mc,moment-noise,attraction,shape-modes}/`, each with config, meta.yaml (solver b9fa957, clean), summary.json, scripts and figures. Raw data is in `~/analytical-nl-discovery-data/<run-id>/` on the PI's laptop.
- New: `explorations/2026-10-10-claude-interactive.2-similariton-validation.md`.
- New tasks: T-20261010-claude-interactive.2-02 to -05 (see Loose ends).
- Task T-20261010-claude-interactive.2-01: status done.

## Not verified

- **$gL=12$-18 laws.** The shape-mode gain exponents (C-02 P2) and the $G^{-2/3}$ laws for $\lambda_2/\lambda_1$ and $1-r^2$ were not reached; the lab-frame runs stop at $gL=8$. To be checked by T-20261010-claude-interactive.2-02 (needs a comoving-frame solver option or the GPU backend).
- **Trend comparisons up to $gL=8$.** These cannot be compared entry by entry with the claim's reduced model until T-20261010-claude-interactive.2-03 tabulates it.
- **Monte Carlo coverage.** Route (i) was run at one configuration only. The spectral, matched-LO and shape-mode noise numbers rest on the adjoint contraction alone. That contraction is exact for linear functionals, and its central-difference gradient checks (`fd_check.json` in run 2026-10-10-claude-interactive.2-moment-noise) agree to 1.1e-06 or better (relative). Nothing beyond that was cross-checked.
- **Relaxed assumptions.** Raman, third-order dispersion and saturation were not tested.
- **Independence.** All of this is Claude-family work. A non-Claude verifier must repeat the core comparisons before either claim can move to `sim-verified`. claude-a's branch carries the verification tasks T-20261008-claude-a-02/-03 for this.

## Loose ends

- T-20261010-claude-interactive.2-02: full-NLSE test at $gL=12$-18 of the shape-mode exponents, spectral rank-one and matched-LO laws.
- T-20261010-claude-interactive.2-03: tabulate the claim's reduced-model spectral and matched-LO values for the asymptotic seed at $gL=2$-8, for entry-by-entry comparison with run 2026-10-10-claude-interactive.2-moment-noise.
- T-20261010-claude-interactive.2-04 (not-claude): Monte Carlo check of the spectral-covariance and matched-LO numbers, which so far rest on the adjoint only.
- T-20261010-claude-interactive.2-05: recompute the held-out $gL=2$ ratio $\lambda_2/\lambda_1=0.4257$ of C-02 P5 from the claim's formulas; the full NLSE stays 8.4-9.5% below it at every $\varepsilon_0$ run (0.1 to 0.0125).
- No separate task for cross-family verification: T-20261008-claude-a-02/-03 (verify C-20261008-claude-a-01/-02, non-Claude) exist on claude-a's branch and land with that PR.
