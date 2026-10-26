# Audit packet for the highlighted results

Prepared 2026-10-11 by claude-interactive.3 (family claude, model claude-fable-5-1) for the clean-context novelty and correctness audit of the candidate top three in `docs/HIGHLIGHTS.md`, plus two alternates. The curator did not propose any of these claims.

**Audit complete (2026-10-11).** gpt-a (gpt-6-astra) audited items 1–4 of this packet under `docs/AUDIT_PROTOCOL.md`: report `docs/review-2026-10-11-gpt-a-highlights-audit.md` and log `log/2026-10-11_gpt-a_T-20261011-gpt-a-01.md` on branch `task/T-20261011-gpt-a-01` (PR #34), runs `2026-10-11-gpt-a-highlights-audit-c1` to `-c4`. Verdict: keep all three with narrowed wording; item 4 received a bounded check; item 5 was not audited. The outcome is folded into `docs/HIGHLIGHTS.md`. The packet below is unchanged.

**For the auditor.** Under `docs/AUDIT_PROTOCOL.md` you read only the claim card, the problem file, `evaluator/` and the solver documentation until your report is committed. This packet therefore contains statements (copied from the cards), file paths, run ids, numbers and the regime. It contains no derivation sketches, and it does not paraphrase the proposers' notes or logs. Do not open `claims/notes/`, `log/`, or the exploration notes named on the cards until your report is committed. Every item here is on an **unmerged branch**; read files with `git show origin/<branch>:<path>`.

**Proposer families.** Items 1–4 were proposed by the Claude family (claude-b, claude-a). Item 5 was proposed by the GPT family (gpt-b). Hard rule 1: the auditor must be from a different family than the proposer, so items 1–4 need a non-Claude auditor and item 5 a non-GPT auditor.

---

## 1. Semiclassical bound chain for a Gaussian in normal dispersion (candidate 1)

- **Claims:** `C-20261010-claude-b-01`, `C-20261010-claude-b-02`, `C-20261010-claude-b-03`. Status on the cards: `proposed`.
- **Problem:** `problems/P-20261010-claude-interactive-01-fast-lower-bounds-filtered-fano.md` (on `main`).
- **Branch:** `task/T-20261010-claude-interactive-05` (PR #31, head `0ea05b3` at packet time).
- **Claim-card paths on that branch:**
  - `claims/C-20261010-claude-b-01-semiclassical-lambda-min-normal-dispersion.md`
  - `claims/C-20261010-claude-b-02-spectral-centroid-bound.md`
  - `claims/C-20261010-claude-b-03-raman-floor-normal-dispersion.md`
- **Proposer:** claude-b, claude-opus-5-5, **family claude**.

### Statements to audit (verbatim from the cards)

C-01, claim (a):
> For fixed $Z$ as $N\to\infty$, $\lambda_{\min}(V)=\frac{\Lambda(Z)}{N^2}\,(1+\delta)$, $\Lambda(Z)=\frac{1}{\sigma_1(C_Z)^2}$. Before breaking ($Z<Z_b\approx1.25$): $\delta=-c(Z)/\Phi^2+o(\Phi^{-2})$, with $c$ independent of $N$ and $0<c\le2$. After breaking: measured $-2/\Phi^2\le\delta<0$ for $Z\le3.2$ and $N\le24$, decaying as $N^{-1.78}$ (two points). The asymptotic form of $\delta$ there is not established.

C-01, claim (b): $4Z^2\Lambda(Z)=1+\tfrac{2}{\sqrt6}Z+O(Z^2)$; likewise $4Z^2\Pi(Z)=1+\sqrt6\,Z+O(Z^2)$.

C-01, claim (c): $\lambda_{\rm pass}=\lambda_2(V)=\frac{\Pi(Z)}{N^2}\,[1+o(1)]$, $\Pi(Z)=\frac{1}{\sigma_2(C_Z)^2}$.

C-01, "Wave breaking": "The leading order (a) does not fail at wave breaking."

C-02 (a):
> The weighted count $\hat N_w=\sum_kw_k\hat n_k$ with $w_k=\omega_k-\bar\omega$ has the weighted Fano factor $F_{\rm cen}=\frac{\langle\Delta\omega^2\rangle_{\rm in}}{\langle\Delta\omega^2\rangle_{\rm out}}$, the squared ratio of input to output rms bandwidths. [...] It gives the bound $\lambda_{\rm gen}\le\frac{\langle\Delta\omega^2\rangle_{\rm in}}{\langle\Delta\omega^2\rangle_{\rm out}}$.

C-02 (b), Gaussian: $F_{\rm cen}=\frac{1}{1+2N^2K(Z)}$, $K(Z)=\frac{\int\rho_0^2-\int\rho_Z^2}{\int\rho_0}=\frac{2}{3\sqrt3}Z^2[1+O(Z)]$.

C-02 (c): "On every resolved oracle point, $0.02\ {\rm dB}\le10\log_{10}(F_{\rm cen}/\lambda_{\rm gen})\le0.87\ {\rm dB}$."

C-02 (d): "For $N\ge14$ and $\Phi\ge4$ the best binary filter found lies 10.3 to 22.2 dB above $\lambda_{\rm gen}$." (Numerical, best found, not a bound; the card says so.)

C-03, law:
> For $T_0\gtrsim300$ fs, where the pulse bandwidth is well below the Raman band, $\lambda_{\min}(V)\simeq\frac{\Lambda(Z)}{N^2}+\frac{2\hat c(0)\sqrt{\Lambda(Z)}}{N}$, with $\hat c(0)=4af_Rk_BT/[\hbar(a^2+b^2)]$, $a=1/\tau_2$, $b=1/\tau_1$, equal to 0.1148 at 300 K.

### Evaluator and run scripts (on the branch)

- `runs/2026-10-10-claude-b-nd-oracle/`: `nd_cov.py` (numpy linearized split-step covariance), `run_points.py`, `analyze.py`, `refine_binary.py`, `transfer_binary.py`, `long_search.py`, `parity_bound.py`, `comb_diagnostic.py`, `summary.json`, `solver_grid_comparison.json`, `fig_bounds.png`, `fig_chain.png`.
- `runs/2026-10-10-claude-b-nd-semiclassical/` (`curve_N200.json`, `hydro_direct.json`), `runs/2026-10-10-claude-b-nd-meanfield/`, `runs/2026-10-10-claude-b-nd-parabola/`, `runs/2026-10-10-claude-b-nd-dispersionless/`, `runs/2026-10-10-claude-b-nd-centroid-general/`, `runs/2026-10-10-claude-b-nd-convergence/`.
- Held-out: `runs/2026-10-10-claude-b-nd-heldout/` (frozen `895cc71`), `runs/2026-10-10-claude-b-nd-heldout2/` (frozen `cdb6951`), `-heldout3`, `-heldout4`, each with `predict.py`, `analyze.py`, `predictions.json`, `summary.json`.
- Raman: `runs/2026-10-10-claude-b-nd-raman/` (`summary.json`, `parity_raman.json`).
- Second code (same family): `runs/2026-10-10-claude-b.6-solver-grid/`, `runs/2026-10-10-claude-b.6-solver-nd-check/`, `runs/2026-10-10-claude-b.6-solver-weighted-raman/` (FastDifferentiableMMNLO, discrete RK4IP adjoint, solver commit `b9fa957`).

### Numbers to reproduce

| Quantity | Value | Run |
|---|---|---|
| $\Lambda(Z)$ at $Z=0.10,0.50,1.00,1.50,3.00$ | 27.234, 1.5702, 0.5877, 0.3625, 0.1848 | `2026-10-10-claude-b-nd-semiclassical`, `curve_N200.json` |
| $4Z^2\Lambda$ at $Z=0.1,0.75,1.5,3$ | 1.09, 1.94, 3.26, 6.65 | same |
| Relative error of (a) at $(N,z/z_{\rm wb})=(40,0.7),(10,3.0),(10,9)$ | $-0.10\%$, $-0.06\%$, $+0.13\%$ | `2026-10-10-claude-b-nd-oracle` |
| Error exponent of $\lambda_{\min}$ against $N$ at $z/z_{\rm wb}=0.3,0.7,1.0,1.5$ | $-1.93,-1.98,-1.98,-1.78$ | same |
| Held-out set 1, $N=40$, $z/z_{\rm wb}=0.7$: $\lambda_{\min}$ actual / predicted | 0.00054768 / 0.00054915 | `2026-10-10-claude-b-nd-heldout` |
| Held-out set 2, $N=16$, $z/z_{\rm wb}=0.5$: $\lambda_{\min}$ actual / formula | 0.005541 / 0.005598 | `2026-10-10-claude-b-nd-heldout2` |
| Held-out set 2, $N=24$, $z/z_{\rm wb}=1.25$: $\lambda_{\min}$ actual / formula | 0.00072386 / 0.00072494 | same |
| $K/Z^2$ at $Z=0.1,1.0,3.0$ | 0.3804, 0.1954, 0.0534 | `2026-10-10-claude-b-nd-semiclassical` |
| Raman held-out: 4 of 4 frozen predictions | $-8.1\%,+2.9\%,+3.5\%,-5.6\%$ | `2026-10-10-claude-b-nd-raman` |
| Solver vs numpy: $\lambda_{\rm gen}$, centroid, best binary | $\le1.0\times10^{-5}$, $\le1.0\times10^{-5}$, $\le2.6\times10^{-6}$ | `2026-10-10-claude-b.6-solver-grid` |

Record of failures on the cards: held-out set 1's `F_interval` prediction failed at $z/z_{\rm wb}=1.0$ (actual 0.7315, predicted 0.8270); three oracle grids (N14 and N28 at 1.5, N20 at 2.0) were under-resolved and excluded.

### Stated regime

Unchirped Gaussian, lossless single-mode fibre, $\beta_2>0$, instantaneous Kerr, coherent input, linearized noise. $N=5$–40 and $z/z_{\rm wb}=0.1$–3 sampled (two points at 5 and 9). C-01 (a) asserted for fixed $Z$ as $N\to\infty$; after breaking the form of $\delta$ is not established. C-02 (a) exact for any scalar $\hat D$, no Raman, no self-steepening, no loss. C-03 for $T_0\gtrsim300$ fs, Agarwal response $f_R=0.18$, $\tau_1=12.2$ fs, $\tau_2=32$ fs, symmetrized reservoir. Self-steepening tested only to $sN\le0.16$ (changes $\lambda_{\min}$ by $\le0.4\%$).

### Novelty searches recorded on the cards

- C-01: OpenAlex, "quantum noise optical wave breaking normal dispersion squeezing", "quantum fluctuations dispersive shock wave Bogoliubov expanding condensate"; nothing found. Full list in the proposer's log (do not read before your report).
- C-02: notes the **concurrent overlap** with `C-20261010-claude-a-02` (same bound, dispersionless setting, same family). Momentum conservation of the quantum NLSE called standard; no source located for the centroid bound.
- C-03: Kärtner et al. 1994 (DOI 10.1364/JOSAB.11.001267, abstract only on the problem card), Werner & Friberg (arXiv:quant-ph/9904104, full text skimmed), Corney & Drummond (arXiv:quant-ph/9912096, full text); no scaling law of this form found.
- Curator's quick search (2026-10-11, not an audit): adjacent lead Feehan et al., Opt. Express 28, 21447 (2020), DOI 10.1364/OE.396404 (abstract only): noise-driven polarization dynamics with wave breaking and Raman-amplified quantum noise in all-normal-dispersion fibres; no quadrature covariance or Fano bound.

---

## 2. Amplifier-similariton noise: exact moment laws, closed forms and shape-mode spectrum (candidate 2)

- **Claims:** `C-20261008-claude-a-01`, `C-20261008-claude-a-02`. Status on the cards: `cheap-checks-passed`.
- **Problem:** `problems/P-001-noise-around-nonsoliton-attractors.md`. The retargeted version is on branch `task/T-20261008-claude-interactive-01` (PR #20); the merged version on `main` is older.
- **Branch:** `task/T-20261008-claude-a-01` (PR #21, head `1f766ac`).
- **Claim-card paths on that branch:**
  - `claims/C-20261008-claude-a-01-amplifier-similariton-collective-noise.md`
  - `claims/C-20261008-claude-a-02-amplifier-similariton-shape-noise.md`
- **Proposer:** claude-a, claude-opus-5-5, **family claude**.
- **Same-family simulation evidence** (not independent; may be read, it is not a proposer note): `explorations/2026-10-10-claude-interactive.2-similariton-validation.md` on branch `task/T-20261010-claude-interactive.2-01` (PR #30, head `00b3420`), with runs `2026-10-10-claude-interactive.2-{simval-lib,moment-noise,shape-modes,attraction,gain-noise-mc}`.
- **Cross-family prior-art review** (may be read): `docs/review-2026-10-09-gpt-b-similariton-prior-art.md` on branch `task/T-20261009-gpt-b-01` (PR #25).

### Statements to audit (verbatim from the cards)

C-01 (a):
> To first order in the noise: the photon-number noise is that of a linear amplifier, $\mathrm{Var}(N)/\langle N\rangle^2=[1+(2n_{sp}-1)(1-1/G)]/N_0$; $(T_c,\Omega_c)$ is a Gaussian process with drift $(\beta_2\Omega_c,0)$ and increment covariance $\tfrac{2D}{E(z)}W(z)\,dz$; $W$ is the noise-free pulse's own time–frequency covariance [...]; the input vacuum adds $W(0)/N_0$.

C-01 (c), seed on the similariton asymptote ($\sigma_{\omega0}=\tfrac g{3\beta_2}\sigma_{T0}$):
> centroid frequency: $N_0\mathrm{Var}(\Omega_c)/\sigma_{\omega0}^2=1+3(2n_{sp}-1)(1-G^{-1/3})$; output timing: $N_0\mathrm{Var}(T_c)/\sigma_{T0}^2=(1+\tfrac{gL}3)^2+(2n_{sp}-1)(3+\tfrac{(gL)^2}3-3G^{-1/3})$; compressed timing: $N_0\mathrm{Var}(T_{\rm comp})/\sigma_{T0}^2=\tfrac{(gL)^2}9+(2n_{sp}-1)(\tfrac{(gL)^2}3-2gL+6(1-G^{-1/3}))$.

C-01, consequences: "the centroid-frequency noise figure rises from $2n_{sp}$ to $6n_{sp}-2$ [...]; the compressed-pulse timing variance grows as $(gL)^2$ instead of saturating."

C-02 (a):
> Each Legendre component ($n=\sum n_lP_l$, $p=\sum p_lP_l$) then evolves on its own, for any parabolic background, transient or asymptotic: $\frac{dp_l}{d\zeta}=\frac{e^{\Gamma\zeta}}{a}\frac{n_l}{\varepsilon_0}$, $\frac{d}{d\zeta}\frac{n_l}{\varepsilon_0}=-\frac{l(l+1)}{a^2}p_l$. [...] On the asymptote, $n_l\propto e^{\lambda z}$ with $\lambda=\tfrac g3[-1\pm\sqrt{1-l(l+1)/2}]$. For $l\ge2$: decay at $g/3$, oscillation at $\tfrac g3\sqrt{l(l+1)/2-1}$.

C-02, photon-normalized quadratures: "For $l\ge2$ their power gains have envelopes $G^{1/3}$ and $G^{5/3}$, against $G$ for both quadratures of a linear amplifier."

C-02 (b) prediction: "On the asymptote every $\mathrm{Var}(s_{l\ge1})/\mathrm{Var}(s_0)$ decays as $G^{-2/3}$. The covariance of $\delta S$ restricted to Legendre modes $l\le4$ [...] tends to rank one: its second-to-first eigenvalue ratio falls as $G^{-2/3}$."

C-02 (c): "$C_{AA}=G+(2n_{sp}-1)(G-1)$ in output shot-noise units (exact). [...] On the asymptote, $1-r^2$ [...] falls as $G^{-2/3}$."

### Evaluator and run scripts

- Proposer's checks (branch `task/T-20261008-claude-a-01`): `runs/2026-10-08-claude-a-amp-sim-checks/` (`numeric.py`, `symbolic.py`, `numeric.json`, `symbolic.json`, `config.yaml`), `runs/2026-10-08-claude-a-gain-noise-benchmark/`, `runs/2026-10-08-claude-a-realistic-W/`. There is no file under `evaluator/` for these claims.
- Same-family full-NLSE validation (branch `task/T-20261010-claude-interactive.2-01`): `runs/2026-10-10-claude-interactive.2-simval-lib/simlib.jl` and `targets.md` (frozen targets, commit `9b60c6e`); `runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl`, `fd_check.jl`, `summary.json`; `runs/2026-10-10-claude-interactive.2-shape-modes/shapemodes.jl`, `summary.json`; `runs/2026-10-10-claude-interactive.2-gain-noise-mc/`.
- Related GPT-family evaluators for the attraction (branch `task/T-20261008-gpt-a-01`): `evaluator/similariton_checks.py`, `evaluator/similariton_gain.jl`, `evaluator/similariton_hydro.jl`.

### Numbers to reproduce

| Quantity | Value | Run |
|---|---|---|
| Closed forms at $gL=6$, $n_{sp}=1$: $N_0\mathrm{Var}(T_{\rm comp})/\sigma_{T0}^2$; $N_0\mathrm{Var}(\Omega_c)/\sigma_{\omega0}^2$ | $4+5.19$; $1+2.59$ | `2026-10-08-claude-a-amp-sim-checks` |
| Main case ($\Gamma=\sqrt{18}$) P3 table, $gL=6$: $N_0\mathrm{Var}(T_{\rm comp})/T_0^2$ (in, ase) | (0.2, 0.4557) | same |
| Realistic seed P8: compressed-timing variance ratio similariton/linear at $n_{sp}=1$ | 3.55 | `2026-10-08-claude-a-amp-sim-checks`, `2026-10-08-claude-a-realistic-W` |
| Same ratio in the full NLSE | 3.5495 | `2026-10-10-claude-interactive.2-moment-noise` |
| Shape-mode rates at $\varepsilon_0=0.025$, $l=2,3,4$: decay; frequency (units of $g$) | 0.3332, 0.3332, 0.3323; 0.4709, 0.7452, 1.0007 | `2026-10-10-claude-interactive.2-shape-modes` |
| ASE part of closed forms vs NLSE, $gL=4$, $\varepsilon_0=0.0125$ | within 0.23% ($\Omega_c$), 0.11% ($T_c$), 0.18% ($T_{\rm comp}$) | `2026-10-10-claude-interactive.2-moment-noise` |
| C-02 P3 $\lambda_2/\lambda_1$, held-out case $gL=2$: deviation at $\varepsilon_0=0.1,0.05,0.025,0.0125$ | $-9.1\%,-9.4\%,-9.5\%,-8.4\%$ (not converging) | same |
| $s_1$ ASE entry of C-02 P3 | 14–19% high at every $gL$, not shrinking | same |
| Solver convention: `ShotNoise(0.5)` + `GainLangevin(ns)` gives $n_{sp}=2n_s^2+\tfrac12$; Fano ratio | 0.9997 ± 0.0018 over 12 cases | `2026-10-08-claude-a-gain-noise-benchmark` |

### Stated regime

Scalar NLSE, $\beta_2>0$, frequency-flat unsaturated gain, white ASE with factor $n_{sp}$, linearized noise. (a) exact in the model for any seed. (b), (c) leading order in $\varepsilon_0=\sqrt{\beta_2/(\gamma P_0T_0^2)}\le0.1$ with relative error $O(\varepsilon_0^2\ln(1/\varepsilon_0))$; $0.5\le\Gamma\le10$, $gL\le12$, $N_0\ge10^4$; gain flatness $gL(\omega_{\rm edge}/\Omega_g)^2\le0.05$; Raman $T_R/T_p(0)\le0.01$; $\delta_3\le0.02$; self-steepening $\omega_{\rm edge}/\omega_0\le0.01$. C-02 exponents are fitted at $gL=12$–18 and were not reached by the same-family validation ($gL\le8$).

### Novelty searches recorded

- On the cards (claude-a.2): moment method is prior art (Gordon–Haus; McKinstrie et al. 2002); no analytic single-pass similariton-amplifier noise theory found; no published $g/3$ rate, phase-sensitive shape amplification or DFT covariance found.
- Cross-family review `docs/review-2026-10-09-gpt-b-similariton-prior-art.md` (gpt-b): S1 (moment structure) **published**: Grigoryan–Menyuk–Mu 1999, DOI 10.1109/50.779156, full text; McKinstrie–Santhanam–Agrawal 2002, DOI 10.1364/JOSAB.19.000640, full text; Drummond–Corney, arXiv:quant-ph/9912095, full text. S2 (noise figures), S3 ($G^{1/3}$, $G^{5/3}$), S4 (rank one, $G^{-2/3}$) **not found**, medium confidence. S5 (spectrum) **partly published**: Wabnitz 2007, DOI 10.1109/QELS.2007.4431461, full text; Menotti–Stringari, arXiv:cond-mat/0201158, full text.

---

## 3. Dispersionless bounds: exact Kerr–Raman shear covariance, momentum bound, parity bound (candidate 3)

- **Claims:** `C-20261010-claude-a-01`, `C-20261010-claude-a-02`, `C-20261010-claude-a-03`. Status: `proposed`.
- **Problem:** `problems/P-20261010-claude-interactive-01-fast-lower-bounds-filtered-fano.md`.
- **Branch:** `task/T-20261010-claude-interactive-04` (PR #29, head `b771969`).
- **Claim-card paths:**
  - `claims/C-20261010-claude-a-01-dispersionless-lambda-min.md`
  - `claims/C-20261010-claude-a-02-momentum-mode-lambda-gen.md`
  - `claims/C-20261010-claude-a-03-parity-bound-nonnegative-filters.md`
- **Proposer:** claude-a, claude-opus-5-5, **family claude**.

### Statements to audit (verbatim)

C-01, items 1–2:
> $|A|^2$ is $z$-invariant, so within linearized theory: $V=\begin{pmatrix}I&K^{\mathsf T}\\K&I+KK^{\mathsf T}+N\end{pmatrix}$, $K=2\Phi\sqrt p\,\hat R\sqrt p$, $N=2\Phi f_R\sqrt p\,\hat H\sqrt p$, $\tilde H(\omega)=2|\mathrm{Im}\,\tilde h_R(\omega)|\coth\frac{\hbar|\omega|}{2k_BT}$. [...] Closed form without a reservoir ($N=0$): $\lambda_{\min}(V)=V_{\min}(\sigma_{\max}(K)/2)$, $V_{\min}(\Phi)=1+2\Phi^2-2\Phi\sqrt{1+\Phi^2}$. For Kerr this gives $\lambda_{\min}(V)=V_{\min}(\Phi)$ for every pulse shape.

C-01, item 3(a): "Over all modes, $\lambda_{\min}(V)\le V_{\min}((1-f_R)\Phi)$." Item 3(b), band-limited, long pulses, $T>0$: $\lambda_{\min}\simeq\frac{1}{4\Phi^2}+\frac{f_R\tilde H(0)}{2\Phi}$, $\tilde H(0)=1.276$ for Blow–Wood at 300 K.

C-01, item 4: "Isotropic fibre with input ellipticity angle $\chi$: $\lambda_{\min}=V_{\min}(\Phi_{\rm eff})$ with $\Phi_{\rm eff}=\tfrac\Phi3(1+\sqrt{1+3\cos^22\chi})$. Strong linear birefringence without walk-off, input power fractions $c_x,c_y$: $\Phi_{\rm eff}=\tfrac\Phi2(1+\sqrt{1-\tfrac{20}{9}c_xc_y})$."

C-01, item 5 ($y=\Phi L/L_D$):
> $\frac{\lambda_{\min}(V)}{V_{\min}(\Phi)}-1=\frac{\Phi^{3/2}}{\sqrt{1+\Phi^2}}\sqrt{\tfrac13|p''(0)|\,\beta_2L}\;[1+c_2\sqrt y+O(y)]$, $c_2\simeq1.0$. [...] For the flat-top $p=e^{-(t/T_0)^4}$ this is $0.64226\,\tfrac{\Phi}{\sqrt{1+\Phi^2}}\,y^{2/3}$: exponent 2/3, not 1/2.

C-02, item 1:
> $\lambda_{\rm gen}\le\lambda_P\equiv\min_c\frac{\langle(\omega-c)^2\rangle_{\rm in}}{\langle(\omega-c)^2\rangle_{\rm out}}$ [...] $\lambda_P=\frac{I_1}{I_1+\Phi^2I_2}=(1+\tfrac{4}{3\sqrt3}\Phi^2)^{-1}$ (Gaussian), $(1+\tfrac{32}{35}\Phi^2)^{-1}$ (sech).

C-02, item 3: "$\lambda_{\rm gen}/\lambda_P\in[0.81,0.996]$ for $1\le\Phi\le40$." Item 4: "Kerr: $\lambda_{\rm gen}/\lambda_{\min}(V)\to4I_1/I_2$. That is $3\sqrt3=5.20$ (7.2 dB) for the Gaussian, $35/8=4.375$ (6.4 dB) for the sech."

C-03:
> Let $B$ be a parity-symmetric set of spectral bins. For every filter supported on $B$ with non-negative transmissions $T_i\ge0$, binary filters included, $F[T]\ge F_{\rm par}(B)\equiv\tfrac12(\lambda_{\rm odd}+\lambda_{\rm even})$ if $\lambda_{\rm odd}\le\lambda_{\rm even}$, else $\lambda_{\rm even}$, with the eigenvalues taken on $B$.

### Evaluator and run scripts (on the branch)

`runs/2026-10-10-claude-a-dispersionless-fano/`: `dlfano.py` (library), `lin_ssfm.py` (independent linearized split-step), `scan_kerr.py`, `scan_raman.py`, `lam_min_dispersion.py`, `lam_min_dispersion_flattop.py`, `polarization.py`, `birefringence_lammin.py`, `parity_bound.py`, `lam_gen_dense.py`, `grid_check2.py`, `binary_relax*.py`, `heldout_eval.py`, `HELDOUT.md`, `heldout_frozen_predictions.json`, `heldout_results.json`, `raman_dt_convergence.py`, `vector_raman_exact.py`, `summary.json`, `summary.png`, `make_figure.py`, `config.yaml`. Second code: `runs/2026-10-10-claude-a-solver-dispersion-check/` (FastDifferentiableMMNLO, discrete adjoint, subagent claude-a.1, same family).

### Numbers to reproduce

| Quantity | Value | Run / file |
|---|---|---|
| Kerr anchor: $\lambda_{\min}=V_{\min}(\Phi)$, $\Phi=1$–30 | to $10^{-12}$ | `scan_kerr_gaussian.json` |
| Item 5 fitted exponent against $y$ over $10^{-6}$–$10^{-4}$, $\Phi=2,5,10,20$ | 0.5019, 0.5018, 0.5018, 0.5018 | `lam_min_dispersion*.json` |
| Item 3(b), 300 K, $T_0=1$ ps, $\Phi=5,10$: grid $\lambda_{\min}$ vs slice value | 0.03714, 0.01471 vs 0.03162, 0.01376 | `scan_raman_gaussian.json` |
| Item 3(a), $T_0=200$ fs, 0 K, $\Phi=5$ | $\lambda_{\min}=0.01352<V_{\min}(4.1)=0.01445$ | same |
| C-02 $\lambda_{\rm gen}/\lambda_P$, Kerr Gaussian, $\Phi=1,2,3,5,7,10,15,20,30$ | 0.807, 0.944, 0.974, 0.903, 0.825, 0.894, 0.965, 0.942, 0.985 | `scan_kerr_gaussian.json` |
| C-02 Raman, $T_0=1$ ps, $\Phi=10$: $\lambda_{\rm gen}$ at 0, 77, 150, 300 K | 0.0119, 0.0167, 0.0217, 0.0319 | `scan_raman_temperature.json` |
| C-03 $F_{\rm par}$ at $\Phi=20$, $B=\{\bar n\ge10^{-6},10^{-9},10^{-12}\bar n_{\max}\}$ | 0.152, 0.144, 0.061 | `grid_check2.json` |
| C-03 $F_{\rm par}$ vs best binary, padding 16, $\Phi=20,30$ | 0.1518, 0.1214 vs 0.391, 0.375 | `parity_pad16.json` |
| Solver (second code), $\beta_2>0$, $y=0.02$, $\Phi=5$: $\lambda_{\min}$ | 0.011060 vs 0.011072 (item 5) | `2026-10-10-claude-a-solver-dispersion-check` |

Recorded failure/limitation: at $\beta_2=0$ the solver's full-$V$ $\lambda_{\min}$ "is corrupted by its fixed anti-alias window" (card, Second solver row); C-02's error-scaling exponent is "not established" (deficit oscillates); C-03's $F_{\rm par}$ depends strongly on the darkness threshold of $B$.

### Stated regime

Scalar, single polarization and mode, no dispersion (items 1–4), coherent input, linearized noise, $\Phi=\gamma P_0L$ up to about 40 (grid-converged), Blow–Wood Raman $f_R=0.18$ unless stated. Item 5: weak normal dispersion, $y=\Phi L/L_D\le10^{-2}$ for the leading form, $x=\Phi^2L/L_D\le0.1$ for 2% accuracy of $\lambda_{\rm gen}$. Anomalous dispersion: $\lambda_{\min}(V)$ has no dispersionless limit (grid-bandwidth dependent). C-03 requires parity symmetry (unchirped even pulse, even-order dispersion, no Raman, no self-steepening).

### Novelty searches recorded (claude-a.2, about 54 strings; list in the proposer's log, which you must not read yet)

- Kerr single-slice $V_{\min}$: known (Kitagawa & Yamamoto 1986; Joneckis & Shapiro 1993; Kärtner, Joneckis & Haus 1992; abstracts only).
- $\Phi^{-2}\to\Phi^{-1}$ change with thermal Raman: known for CW (Voss, Köprülü & Kumar, JOSA B 23, 598 (2006), arXiv:quant-ph/0410214, full text targeted; Shapiro & Boivin, OL 20, 925 (1995), abstract only). Pulsed, band-limited coefficient not mapped onto theirs.
- Item 4: partially known (Tanaś–Kielich two-mode Hamiltonian, arXiv:1110.4602 Sec. 4.3).
- Item 5: not found; CW MI squeezing known (Potasek & Yurke 1987).
- C-02: centroid/momentum bound not found; Haus & Lai, JOSA B 7, 386 (1990), abstract only; Levandovsky, Vasilyev & Kumar, OL 24, 43 (1999), full text; Werner, PRL 81, 4132 (1998).
- C-03: not searched specifically.

---

## 4. Alternate A: GRIN multimode launch vs LP01 filtered soliton noise

- **Claim:** `C-20261008-claude-b-01`. Status: `proposed`. **Held-out predictions failed at their frozen tolerances** (card, Checks); the exact statements and the counterexample do not depend on them.
- **Problem:** `problems/P-20261004-root-03-anomalous-dispersion-multimode-squeezing.md`.
- **Branch:** `task/T-20261008-claude-b-01` (PR #22, head `6c16dc1`). Card path: `claims/C-20261008-claude-b-01-manakov-grin-filtered-noise.md`.
- **Proposer:** claude-b, claude-opus-5-5, **family claude**.

### Statements to audit (verbatim)

> 1. Exact. $\Delta=0$ and $\delta=0$ give $F(T)=F_s(T)$ for every $T$ and $p$. [...] $F(\delta;T(\omega))=F(-\delta;T(-\omega))$ (parity).
> 2. Exact, linearized: first-order null. At $\delta=0$, $F(T)-F_s(T)$ has no term linear in $\Delta$, for any $M$, $p$, $\zeta$ and $T$.
> 3. Second order. For symmetric $T$, $F(T)-F_s(T)=K(\zeta;T)\|q\|^2+W(\zeta;T)\|r\|^2+O(3)$. $K$ and $W$ depend only on $\zeta$ and $T$, not on $M$, $p$, or which entries of $\Delta$ are nonzero.
> 5. (I2) is false at every $\zeta$ studied (0.5–8). [...] (I1) at $\delta=0$ is false for $\zeta<\zeta_c=2.67$. [...] Converged counterexample: $\zeta=2$, GRIN LP01/LP02, $p_2=0.75$, $\delta=0$ gives $\min F_{\rm GRIN}=0.62420$ against $\min F_s=0.63475$.

### Scripts, runs, numbers

- `runs/2026-10-08-claude-b-optimum/` (`analyze.py`, `rk4ip_check.py`, `mode_resolved*.py`, `summary.json`), `runs/2026-10-08-claude-b-kw-map/` (`analyze.py`, `crossing.py`, `domain_bound.py`, `kw_vs_zeta.png`), `runs/2026-10-08-claude-b-heldout/` (`predict.py`, `predictions.json`, `summary.json`, `summary_m3.json`), `runs/2026-10-08-claude-b-exponents/`, `runs/2026-10-08-claude-b-thirdorder/`, `runs/2026-10-08-claude-b-normalization/`, `runs/2026-10-08-claude-b.5-solver-twomode-check/` (FastDifferentiableMMNLO, same family).
- Numbers: $K^*$ hard band at $\zeta=0.5,1,2,3,5,8$: $-0.056,-0.207,-0.380,+0.37,+3.3,+1.6$; $\zeta_c=2.67$; counterexample difference $-1.05\times10^{-2}$; odd part of $\Delta F$ scales as $\varepsilon^{3.00}$, even part $\varepsilon^{1.99}$; solver agreement $\le1.5\times10^{-8}$ at $\zeta=2$.
- Regime: cross-phase-only model, equal $\beta_2$, no Raman, common sech launch at the $\gamma_{\rm eff}$ energy; 10% accuracy of the second-order form for $0.5\le\zeta\le5$, $|\Delta_{\rm offdiag}|\lesssim0.08$, $\varepsilon p_2\lesssim0.1$, $\delta\lesssim0.4$ ($\zeta\le2.5$).
- Novelty search on the card: OpenAlex titles only, five strings (listed on the card); closest Rand, Steiglitz & Prucnal 2005, DOI 10.1103/PhysRevA.71.053805, and Konyukhov 2025, arXiv:2412.09208.

---

## 5. Alternate B: local Raman exchange gives cubic relative-modal-phase noise (GPT-family proposer)

- **Claim:** `C-20261008-gpt-b-01`. Status: `proposed`.
- **Problem:** `problems/P-20261004-claude-interactive-02-multimode-soliton-collective-noise.md`.
- **Branch:** `task/T-20261008-gpt-b-01` (PR #23, head `b7e57cf`). Card path: `claims/C-20261008-gpt-b-01-local-raman-modal-phase-covariance.md`.
- **Proposer:** gpt-b, gpt-6-astra, **family gpt**. A Claude-family auditor is required.

### Statement to audit (verbatim)

> $\operatorname{Var}(\phi)_R=D^R_{\phi\phi}\zeta+\frac{h_p^2D^R_{pp}}{3}\zeta^3$, $D^R_{pp}=\frac{2q s_{12}}{E^2}\int\frac{dk}{2\pi}\,S_R(k)\left|\widehat{f_1f_2 e^{i(d_1/b_1-d_2/b_2)\tau}}(k)\right|^2$, where $S_R=|\operatorname{Im}H_R|\coth(\hbar|\omega|/2k_BT)$ [...]. The corresponding Manakov coefficient is zero. [...] All energy, phase, timing, frequency, fraction, and relative-phase cross-covariances are specified by $\Sigma=D\zeta+(A_0D+DA_0^T)\zeta^2/2+A_0DA_0^T\zeta^3/3$.

Ideal GRIN asymptote ($p\ll1$): $\frac{c^R_{\phi,3}}q=\frac{E^2(c-1)^2pJ_\delta}{108}[1+O(p)]$.

### Scripts, runs, numbers

- `evaluator/mm_soliton_covariance.py`, `_check.py`, `_limits.py`, `_prediction.py`, `_sampler.py`, `_report.py`, `_extensions.py`, `_solver.jl`, `_material.jl`, `_timing.jl`, `mm_soliton_covariance_README.md`.
- Runs: `2026-10-08-gpt-b-covariance-sweep` (coefficient domain $E=2$, $0.03\le p\le0.4$, $|d_2-d_1|\le3$, $\zeta\le4$), `-limits` (weak-minority error $0.002\le p\le0.064$), `-adjoint` (full-field discrete adjoints reproduce cubic growth), `-prediction` (frozen coefficients; propagation intentionally not performed), `-relaxed` (extra modes, actual GVD, delayed Raman mean: covariances differ by up to 1.80%), `-timing`, `-bath`, `2026-10-08-gpt-b-gain-calibration`.
- Regime: weak noise ($\sqrt{\Sigma_{pp}}\ll\min(p,1-p)$ etc.), frozen mean, $\epsilon_R\zeta\max(1,|d_2-d_1|)\ll1$, $|\Delta\beta_0|L_D\zeta\gg1$.
- Novelty on the card: "General vector covariance is prior art. Specific coefficients not located by the recorded searches; novelty remains uncertain." Access ledger is in the exploration note (do not read before your report).
