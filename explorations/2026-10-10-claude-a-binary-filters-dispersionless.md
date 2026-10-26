---
agent: claude-a
model: claude-opus-5-5
family: claude
task: T-20261010-claude-interactive-04
date: 2026-10-10
problem: P-20261010-claude-interactive-01
runs: [2026-10-10-claude-a-dispersionless-fano]
---

# Binary spectral filters on a self-phase-modulated pulse (dispersionless Kerr): what limits them

## What was seen

**Setting.**
- Dispersionless scalar Kerr. A Gaussian pulse has its spectrum broadened by SPM, with peak phase $\Phi$.
- Binary filter on the unitary-DFT bins, then counting. All numbers are exact Fano factors of the stated filters, from run `2026-10-10-claude-a-dispersionless-fano`.

**Best binary filter found against $\Phi$.** Minimum over all search methods:

| $\Phi$ | 1 | 2 | 3 | 5 | 7 | 10 | 12.5 | 15 | 20 | 25 | 30 | 40 | 50 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| nested tabu (`scan_kerr_gaussian.json`, continuation) | 0.774 | 0.702 | 0.662 | 0.677 | 0.509 | 0.509 | 0.497 | 0.461 | 0.519 | 0.432 | 0.560 | — | — |
| box relaxation + dithering + tabu, best of two passes (`binary_relax_gaussian.json`, `binary_relax2_gaussian.json`) | 0.848 | 0.702 | 0.662 | 0.677 | 0.488 | 0.471 | 0.450 | 0.439 | 0.400 | 0.322 | 0.401 | 0.359 | 0.331 |
| parity bound $F_{\rm par}$, bins $\bar n\ge10^{-6}\bar n_{\max}$ (`parity_bound.json`), rigorous on that bin set | 0.484 | 0.286 | 0.184 | 0.308 | 0.076 | 0.156 | 0.106 | 0.129 | 0.152 | 0.081 | 0.121 | 0.061 | — |
| $\lambda_{\rm gen}$ (`scan_kerr_gaussian.json`, `parity_bound.json`) | 0.456 | 0.231 | 0.123 | 0.0446 | 0.0213 | 0.0115 | 0.0080 | 0.0055 | 0.0030 | 0.0021 | 0.0014 | 0.0008 | — |

**1. The apparent saturation was a search limit.**
- With the older search the optimum looked flat at about 0.43–0.56 for $\Phi\ge7$. The non-monotone tabu values were search failures.
- The better search shows a slow decrease. A fit to $\Phi\ge10$ gives $F_{\rm bin}\propto\Phi^{-0.21}$ (`summary.json`, `binary_exponent_Phi_ge_10`). The scatter is still about ±10%, so the search is not converged.
- The best binary is 16–28 dB above $\lambda_{\rm gen}$ for $\Phi\ge10$.
- **Bin width** ($\Phi=10$; padding 4, 8, 16; `binary_relax_pad*.json`): 0.478, 0.471, 0.470, converged.
- At $\Phi=20$: 0.436, 0.400, 0.391, still falling with finer bins.
- Padding 8 to 16 at $\Phi=30$: 0.401 to 0.375 (`binary_relax2_pad16.json`). At $\Phi=40$: 0.359 to 0.312 (`binary_relax2_pad16_phi40.json`).
- At padding 16 the best binary falls as about $\Phi^{-0.27}$ for $\Phi=10$–40.
- Convergence at $\Phi=20$: padding 4/8/16/32 gives 0.436/0.400/0.391/0.388, a geometric approach to about 0.386 (`binary_relax2_pad32_phi20.json`). The binary optimum is a well-defined continuum quantity, but at large $\Phi$ it needs bins well below the padding-8 grid.
- So at large $\Phi$ the optimum depends somewhat on spectral resolution. Finer bins dither better.
- **Physical units.** The window is $14T_0$. For $T_0=200$ fs, padding 4, 8 and 16 give bins of 89, 45 and 22 GHz (0.72, 0.36 and 0.18 nm at 1550 nm). Programmable pulse shapers resolve about 10–20 GHz, finer than the padding-16 grid, so lab optima at large $\Phi$ may lie somewhat below the padding-8 values quoted here. For $T_0=1$ ps, padding 8 is already 9 GHz.

**2. Dithering formula** (`dither_ramp.json`, $\Phi=10$, 22 shapes). A binary filter can realize any weight density $d(\omega)\in[0,1]$ by error-diffusion dithering over fine bins. The dither error is high-pass in $\omega$, so it lands at large delays where the field is dark and adds vacuum noise $d(1-d)$ per photon. Then
$$F_{\rm bin}\simeq1-(1-F_d)\frac{\langle d^2\rangle_{\bar n}}{\langle d\rangle_{\bar n}},$$
with $F_d$ the smooth-weight Fano factor. Predicted and measured values agree to about 1% for every shape tried.

**3. The binary objective's own box extension is reachable.** For binary $T$, $F[T]=1+T^{\mathsf T}(\Sigma-D)T/\bar n^{\mathsf T}T$, with $D=\mathrm{diag}\,\bar n$, because $T_i^2=T_i$. Its extension $J(d)$ to $d\in[0,1]^n$ is, by item 2, realized by dithering.
- So the binary problem is, to good accuracy, the continuous box problem $\min J$.
- Local minima of $J$ (L-BFGS-B), dithered and then tabu-polished, give the best filters above, in 4–30 s against minutes for tabu.
- The relaxed $J$ sits 0.5–3.5% below the dithered binary value.
- This is a search method. A global lower bound from $\min J$ would need a certificate, which is the lane of T-20261010-claude-interactive-03.

**4. What the optimal filters look like** (`binary_structure.json`; figure, panel b).
- **$\Phi=7$–30: one-sided combs.**
  - 19–59 selected blocks, with 87–94% of the selected photons on one side of the carrier. Some runs find the mirror image.
  - Odd-sector fraction $f_{\rm odd}=0.38$–0.45, close to the parity limit 1/2.
  - The even sector supplies 0.22–0.35 of $F$ and the odd sector 0.10–0.14.
  - Overlap² with the momentum mode is 0.25–0.36.
- **$\Phi=40$: a symmetric comb.** 158 blocks, $f_{\rm odd}=0.03$, $F=0.359$, almost entirely from the even sector. As $\lambda_{\rm even}$ drifts down with $\Phi$, a second family of filters that ignores the momentum mode takes over.
  - This is consistent with the argument of Levandovsky, Vasilyev & Kumar (OL 24, 43 (1999)) that the optimal passive soliton filter is even.

**5. Why the gap to $\lambda_{\rm gen}$.**
- Only weights $g\propto\omega$ (the momentum mode, which is odd in $\omega$) cancel the $O(\Phi)$ anti-squeezed noise. A kink at $\omega=0$, which maps onto the bright peak, costs $O(\Phi)$: $|\omega|$ gives 13.8 and $\omega\Theta(\omega)$ gives 6.9 at $\Phi=10$.
- A non-negative filter can put at most half its weight on odd vectors. The other half must sit in the even sector, whose lowest eigenvalue does not go to zero (0.12–0.30 for $\Phi=7$–40).
- This gives the rigorous parity bound (claim C-20261010-claude-a-03), on the stated bin set. The best binary sits 2.0–8.1 dB above it for $\Phi\le40$.
- $\lambda_{\rm even}$ drifts down roughly as $\Phi^{-1/2}$ (window averages 0.34 to 0.12 over $\Phi=2$–60), so the parity bound weakens slowly at large $\Phi$.
- Admitting ultra-dark bins with arbitrary weights lowers it further (claim -03, "Choice of $B$ matters").

**6. Sensitivity to dispersion** (`binary_vs_dispersion.json`, `scan_dispersion_phi20_rest.json`).
- The binary optimum moves at first order in $\beta_2$: normal dispersion lowers it, anomalous raises it.
- At $\Phi=20$: $-9\%$ and $+11\%$ at $x=\Phi^2L/L_D=0.1$. Normal dispersion gives 0.30 at $x=1$ and 0.28 at $x=3$.
- $\lambda_{\rm gen}$ changes by under 1% to $x=0.3$.
- So the dispersionless binary numbers apply only to $x\lesssim0.03$–0.1, a window that narrows with $\Phi$. Normal dispersion is where binary filters start to work well (T-20261010-claude-interactive-05).

**7. Breaking parity with $\beta_3$ helps binary filters** (`binary_vs_beta3.json`; Kerr + $\beta_3$ only, relaxation search, padding 4).
- $\Phi=10$: the best binary falls from 0.47 ($\delta_3=0$) to 0.31, 0.34 and 0.30 at $\delta_3=\beta_3L/T_0^3=0.03$, 0.1 and 0.2.
- $\Phi=20$: from 0.44 to 0.25 ($\delta_3=0.03$) and 0.19 ($\delta_3=0.1$), a gain of 3.6 dB.
- This fits the parity mechanism of C-20261010-claude-a-03. Without $\omega\to-\omega$ symmetry, a non-negative filter is no longer held to half of the momentum mode. It is not a test of the bound itself, which needs parity.
- The point $\Phi=20$, $\delta_3=0.2$ violates $\lambda_{\rm gen}\le\lambda_P$ on its grid, so it is unconverged and excluded.

## Simplicity signal

- **A reduced model.** "Binary ≈ continuous density with a vacuum penalty $d(1-d)$" replaces a combinatorial problem by a smooth one. It also fixes how bin resolution enters: the dither error must land in the dark part of the time window, so the bins must be narrower than the inverse of the dark-window width.
- **A symmetry obstruction.** The parity bound explains why non-negative readouts cannot follow $\lambda_{\rm gen}\propto\Phi^{-2}$.

## Artefact checks

- Every reported $F$ is recomputed exactly from the final $T$.
- Padding 4 against 8: binary values within the search spread.
- Parity commutator $\le3\times10^{-8}$.
- The dithering formula was checked only at $\Phi=10$; the run was stopped after that row.
- Bin-width convergence: done at $\Phi=10$ (converged), $\Phi=20$ (2.3% further drop from padding 8 to 16), $\Phi=30$ (6.3%) and $\Phi=40$ (13%). Finer bins at large $\Phi$ are a loose end (T-20261010-claude-a-04).

## Worth a problem file?

It belongs to P-20261010-claude-interactive-01. Target quantities, suggested:
1. the $\Phi\to\infty$ behaviour of $\min_TF$ for the dispersionless SPM pulse. The current estimate is a slow decay of about $\Phi^{-0.2}$, still search- and resolution-limited;
2. a formula for $\lambda_{\rm even}(\Phi)$;
3. whether the box relaxation $\min J$ admits a certificate that closes the 2–8 dB gap to the parity bound.
