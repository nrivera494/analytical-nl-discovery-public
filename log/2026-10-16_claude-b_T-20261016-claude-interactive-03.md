---
date: 2026-10-16
agent: claude-b
model: claude-opus-5-5
family: claude
task: T-20261016-claude-interactive-03
duration_min: 240
---

## Did

The task is on card P-20261016-claude-interactive-01: the dispersive-wave (DW) yield ceiling of supercontinuum, and the headroom that input shaping gives. Work started 11:30 EDT. The branch stacks on PR #44 (`task/T-20261016-claude-interactive-01`).

**Pose and freeze.**
- H1–H4 were frozen in `explorations/2026-10-16-claude-b-dw-yield-hypotheses.md`, commit **d1b7f71** (11:45), before any production run.
- Amendments A1–A9 were added later: 85637bb, b9067fa, f736bd3, 3a852dc, 6281a3b, 0f566ae, 237c977, 52ddfd0 and f2bcc34. Each was committed before the runs it predicts. Where an amendment was written after part of a result had been seen, it says so.
- Two amendment headers carried wrong clock times, which I estimated instead of reading. The corrections are in the file, and the commit times are authoritative.

**Literature.** Roy, Bhadra and Agrawal, PRA 79, 023824 (2009), DOI 10.1103/PhysRevA.79.023824. **Full text**, author copy from the Agrawal group website (sites.rochester.edu/agrawal, file `paper_2009_05.pdf`).
- Eq. 2 confirms $\delta_3=\beta_3/(6|\beta_2|T_0)$, the same convention as the card and as here.
- Eq. 6 is the peak law $p_d\approx(5\pi N/4\delta_3)^2(1-\frac{2\pi}5(2N-1)\delta_3)^2e^{-\pi/(2(2N-1)\delta_3)}$.
- Fig. 3 gives the NSR peak level at $N=2$, $\xi=4$, with and without Raman.

**Code.** A numpy oracle, run `2026-10-16-claude-b-dw-oracle`:
- Strang and Yoshida (order-4) split-step for the TOD-perturbed NLSE, with an exact discrete adjoint, both plain and checkpointed. It was checked against the exact $N=2$ breather (orders 2 and 4) and against finite differences (about $10^{-8}$).
- A second integrator (RK4IP), which also carries the causal Raman response (model M1).

A subagent, claude-b.7, ran the same observables in the Julia solver FastDifferentiableMMNLO: run `2026-10-16-claude-b.7-solver-dwyield`.

## Found

**H1, conservation-law program (card sketch 1). Refuted as a ceiling; claim C-20261016-claude-b-03.**
- With cubic dispersion, $K=-D$ falls as $-\delta_3w^3$ on the blue side. So a vanishing number of far-blue photons, carrying fixed momentum, supplies unlimited negative Hamiltonian.
- A three-point spectrum meets photon number, momentum and both Hamiltonian bounds (Kerr energy at least 0; sharp Gagliardo–Nirenberg constant $1/\sqrt3$, checked numerically) with band fraction $1-r$ for any $r>0$. The program is vacuous on the line (H1a confirmed).
- On finite windows its value is 0.57–0.85 at $2w_{\rm DW}$ (H1b's at-least-0.5 confirmed). On the simulation windows it is 0.74–0.95 (H1b's at-least-0.9 refuted at 11 of 20 points), which is 2.9× to 837× the simulated TL band yields.
- In pure-$\beta_2$ normal dispersion the program equals the Cantelli bound $\sigma^2/(\sigma^2+w_B^2)$, with $\sigma^2=2|h|$. This is sharper than the Hamiltonian–Markov ceiling (H1c confirmed at 9 points).
- In the oracle, energy is conserved to $10^{-12}$. In the law sweeps, momentum ($\langle w\rangle$) drifts by less than $10^{-11}$ and the Hamiltonian by less than $10^{-8}$ relative. In the large-$N$ card grid, momentum drifts up to $1.2\times10^{-6}$ (at $N=8$, $\delta_3=0.03$) and the Hamiltonian up to $1.8\times10^{-6}$ (at $N=6$, $\delta_3=0.01$). So H1d's below-$10^{-6}$ target is narrowly missed at those two points.
- Run 2026-10-16-claude-b-dw-program.
- In the Julia solver (claude-b.7), energy is conserved to $2\times10^{-10}$ (photon number to the same order). The momentum and Hamiltonian drift by about $10^{-5}$, which is caused exactly by the residual self-steepening $s=1/(\omega_0T_0)=10^{-6}$: the drifts scale with $s$, checked at $10^{-7}$ and $10^{-8}$. So H1d's below-$10^{-6}$ target is not met in the solver, for that physical reason, not because of a numerical error.

**Second code (claude-b.7, FastDifferentiableMMNLO at b9fa957; same family).**
- Agrees with the numpy oracle to within 0.2% on smooth-gated DW yields over 8 decades: sech $N=2$, $\delta_3=0.010$–0.030.
- Roy NSR levels within 0.36 dB.
- Card-grid band yields within 0.3%, except Gaussian $N=8$ at $\delta_3=0.05$: there numpy is 1.4% low because its window (90) lets DW wrap around. Run `window_check.json`: window 70 gives 0.3186, against 0.3237 at 140 or more. Card-grid values at $N\ge8$, $\delta_3=0.05$ carry this 1–2% bias.
- Raman (M1) yields within 1%, with second-order convergence in the Raman kernel step.
- Optimised-mask yields within $10^{-5}$.

The subagent also found two problems:
- a hard gate at $|\tau|<8$ leaks soliton tails at the $10^{-8}$ level, so all law fits use the smooth gate at 15;
- for sech $N=2$ the breather recompresses at $\xi\approx0.80$, 2.40 and 3.95, and each compression emits a DW burst with the same exponent.

**H2a, Roy reproduction. Confirmed.**
- TOD-only, sech $N=2$, $\xi=4$. NSR peak levels at $\delta_3=0.02$–0.1: −23.0, −15.7, −12.8, −10.1, −7.7 dB, against my digitisation of Roy Fig. 3(b): −22, −14, −12, −10, −6.
- Peak frequencies $\Delta\nu_dT_0$ = 4.06, 2.89, 2.26, 1.64, 1.14, against Roy Fig. 3(a): 4.1, 2.9, 2.3, 1.7, 1.15.
- **Comparison with Eq. 6.** The TOD-only levels exceed Roy's Eq. 6 by 39.5, 12.8 and −0.4 dB at $\delta_3=0.02$, 0.03 and 0.04 (Eq. 6: −62.5, −28.5, −12.4 dB).
  - Roy et al. themselves report this TOD-only deviation: Eq. 6 "deviates considerably" from their no-Raman data.
  - They validated Eq. 6, a spectral-peak estimate, against their Raman-inclusive full model ($f_R=0.245$, two-component response, self-steepening), where it falls close to the data at $\delta_3=0.02$–0.03.
  - My M1 reproduces a Raman-reduced level (−51 dB at 0.02) but uses $f_R=0.18$ with a one-oscillator response. **A comparison with Roy's full model is not done.**
- Run 2026-10-16-claude-b-dw-oracle.

**H2b, the singularity law (main result). Claim C-20261016-claude-b-01.**
- Statement: the TOD-only fission-burst DW yield obeys $\ln\eta_{\rm DW}=-d_*/\delta_3+p\ln\delta_3+c$, where $d_*$ is the narrowest analyticity strip (nearest complex-time singularity) of the unperturbed NLSE evolution up to the fibre end.
- For the $N=2$ sech, $d_*=\frac12\arccos(\sqrt3-1)=0.374664$ exactly. The contrast is the ejected-soliton strip value $\pi/(2(2N-1))=0.5236$, which is the exponent of Roy's Eq. 6.
  - The law explains the TOD-only gap that Roy et al. report, and gives its $\delta_3\to0$ exponent.
  - Its asymptotic tests lie below their −80 dB visibility floor.
  - gpt-b's novelty review (PR #49) rates the law "partly published": compression-localised emission and pole-controlled radiation are known, but the minimum-strip exponent was not found.

The four-point fits:

| Launch | Fitted $d$ | $d_*$ | Deviation | Status |
|---|---|---|---|---|
| sech $N=2$ | 0.3788 | 0.37466 | +1.1% | construction set |
| sech $N=3$ | 0.2008 | 0.1997 | +0.6% | held out |
| Gaussian $N=4$ | 0.1323 | 0.1322 | +0.1% | held out |
| Gaussian $N=3$, $\xi_f=2$ | 0.1929 | 0.2015 (A1) / 0.1923 (global minimum) | −4.3% / +0.3% | fails the frozen 4% against A1; agrees with the global minimum found afterwards (A3) |
| Gaussian $N=3$, $\xi_f=1$ (length test A4) | 0.2025 | 0.2015 | +0.5%, and 5.0% above the $\xi_f=2$ fit | confirmed |
| Gaussian $N=3$ in M1 (Raman, A5) | 0.2358 (Julia solver: 0.23596) | $d_*^{M1}=0.2346$ | +0.5% (solver +0.6%), and 22% above M0 | confirmed |
| sech $N=4$ (A11, held out) | 0.44 (ill-conditioned) | 0.1342 (fine scan 0.13335) | local slopes 0.144, 0.131, 0.082 (non-monotone) | **refuted as frozen** |
| sech $N=4$, exploration after the refutation ($\delta_3$ down to 0.0024) | 0.128 (four smallest; $p=+5.4$) | 0.1334 | local slopes 0.141–0.144 at $d_*/\delta_3=46$–56 | not decisive |

- Prefactor exponent: $p=-2.9$ to $-3.4$. The local-slope error shrinks as $\delta_3^{1.1}$ to $\delta_3^{1.9}$.
- **Frozen H2b clauses that failed**, because I put the asymptotic regime at too large a $\delta_3$:
  - sech $N=2$, "local slope within 10% of $d_*$ over $\delta_3\in[0.008,0.03]$": it holds only for $\delta_3\lesssim0.012$. The local slope is 0.33 at 0.013 and 0.28 at 0.019, against 0.3747.
  - Gaussian $N=3$, "slope over $[0.01,0.02]$ within 15% of $d_*$": the slope there is 0.085, against 0.19.
  
  The amended procedure (A1: four smallest $\delta_3$, with $d_*/\delta_3\approx34$–47), frozen before the held-out runs, is the one that passed. The law is asymptotic, and at $d_*/\delta_3\approx10$–20 the $O(\delta_3)$ corrections are 10–60%.
- With Raman ($f_R=0.18$, $T_0=50$ fs): $d_*^{M1}=0.441$ for the sech $N=2$. The fit gives 0.4434, but this was not a frozen test.
  - Raman cuts TL burst yields by 770× (sech $N=2$, $\delta_3=0.02$) and 215× (Gaussian $N=3$, $\delta_3=0.01$). H4b is confirmed: the sech $N=2$ NSR drops from −23 to −51 dB, close to Roy's full-model curve.

**H2c, card regime (TL Gaussians, $N=3$–10, $\delta_3=0.01$–0.05, $\xi=2$).**
- Band yields lie between $8.9\times10^{-4}$ and 0.318. That spans 2.6 decades, so the predicted "more than 6 decades" is refuted. The yields are below 0.5 (confirmed).
- They are saturated between $\xi=1.5$ and 2 at 19 of 20 points. The exception is $N=3$, $\delta_3=0.01$ (+27%).
- Most of the card regime is **not** in the exponentially small burst regime.
- **H2d (collapse, frozen in A9 before the $d_*$ values were computed): confirmed.** The TL band yields collapse on $x=d_*(N)/\delta_3$, with $d_*$ the minimum over $\xi\le2$ (0.1922, 0.1191, 0.0725, 0.0572 for $N=3,4,6,8$).
  - Median spread 0.087 in $\ln\eta$, maximum 0.21. Roy's variable $(2N-1)\delta_3$ gives 0.117 and 0.68.
  - Predicted against computed: $d_*(5)$ 0.10 → 0.0885; $d_*(6)$ 0.080 → 0.0725; $d_*(8)$ 0.053 → 0.0572.
  - $d_*(10)$: the strip fit fails (it returns negative widths) on both the $N_t=16384$/$T_W=48$ and the 32768/64 grids, so it is undetermined. Sech $N=4$: $d_*=0.1342$.
  - Runs: `dstar_card_*.json`, `dstar_fine_N8.json`, `collapse.json`, `fig_collapse.png`.

**H3, shaping headroom.** Runs 2026-10-16-claude-b-dw-shaping and -oracle; claim C-20261016-claude-b-02.

*Method.* Adjoint L-BFGS on the band yield at $\xi_f=2$:
- phase as a Legendre series to degree 24;
- passive amplitudes per bin in [0, 1];
- three starts (TL, best GDD, random), 60–150 iterations.

Optimised values are lower bounds.

*Large-yield regime.*

| Point | $\eta^{\rm TL}$ | GDD | Phase-only | Passive |
|---|---|---|---|---|
| $N=3$, $\delta_3=0.05$ | 0.164 | 1.02× | **1.50×** (TL start 1.23, GDD start 1.50, random 1.23) | 1.51× |
| $N=3$, $\delta_3=0.02$ | 0.052 | 1.04× | **1.55×** (TL 1.10, GDD 1.55, random 1.10) | 1.55× |
| $N=6$, $\delta_3=0.03$ | 0.206 | 1.06× | **1.27×** (TL 1.12, GDD 1.27, random 1.12) | 1.31× |
| $N=8$, $\delta_3=0.05$ | 0.319 | 1.00× | **1.12×** (TL 1.12, GDD 1.09, random 1.12) | 1.13× |

- The passive optima keep at least 99.999% of the energy.
- At $N=3$, $\delta_3=0.02$ the gain persists to $\xi=6$ (band 1.54×, gated 1.53×; 0.8% of band photons near the soliton).
- The gain persists to $\xi=6$ (1.40×), and only 1–2% of band photons lie near a soliton.
- With Raman (H4c) the same mask gives 1.71× at $\xi=2$ and 1.46× at $\xi=6$.
- **A re-optimisation targeting persistence** ($N=6$, $\delta_3=0.03$, band yield at $\xi_f=4$, window 220, 40 iterations) found 1.10× (phase-only, all three starts) and 1.10× (passive). That is below the 1.17–1.22× persistent gain of the $\xi_f=2$ masks, so these short optimisations do not reach the optimum.
- **Persistent gain (wide windows, $\xi=6$):** 1.54 ($N=3$, 0.02), 1.40 ($N=3$, 0.05), 1.17 ($N=6$, 0.03; passive 1.22) and 1.01 ($N=8$, 0.05). The $N=8$ gain at $\xi=2$ was an output-plane transient, gone by $\xi=3$. The radiated-DW headroom falls from about 1.5 to about 1 as the TL yield rises.
- So H3b (at most 2) holds at the tested points, H3c's large-yield part holds (GDD at most 1.06), and H3d holds (passive/phase 1.002).

*Small-yield (burst) regime.*
- The DW yield of a shaped launch follows the singularity law with the shaped launch's $d_*$.
  - GDD: frozen test A3. The optimum sits at $C\approx-0.2$ in both theory and simulation, and the headroom is 1.07 at $\delta_3=0.01$ and 1.28 at 0.006. So H3c's small-yield part (GDD at least 2×) is **refuted**: the earlier "4.1×" was the output-plane transient.
  - Cubic phase: frozen test A6 was refuted because its input was a fit artifact; the corrected A7 prediction is confirmed at $\delta_3=0.006$.
- Over 18 quadratic-plus-cubic phases the robust $\inf d_*$ is the GDD-only value, giving a headroom rate $\kappa\approx0.0025$.
- **Gated phase-only optimisation at $N=3$, $\delta_3=0.01$:** 2.04×, with all three starts converging to the same value. Passive gives 2.05×.
  - **A8 (frozen) confirmed.** The mask's $d_*$ is 0.1858, a decrement of 0.0061 (predicted 0.0071 ± 30%). Its gated headroom is 2.38× at $\delta_3=0.0075$ and 3.07× at 0.006, against the predicted 2.58 and 3.28.
  - So the burst-regime headroom grows as $e^{\kappa/\delta_3}$, with $\kappa\ge0.006$ for phase-only against 0.0025 for chirp.
  - The card's "at most 2×" conjecture therefore fails for DW yield at $N=3$, $\delta_3\le0.01$, and for any $\delta_3$ below about $\kappa/\ln2$.
  - **H4c in the burst regime: refuted.** With Raman (M1) this mask gives 0.078× TL at $\delta_3=0.01$ and 0.034× at 0.0075 (`h4c_gated_*`). Raman destroys the sharpened late compression it relies on. The large-yield masks, by contrast, keep their full gain with Raman (1.54× and 1.71×/1.46×). Burst-regime headroom is model-specific.
- **H3a (more than 2× at $N=3$, $\delta_3=0.02$) refuted**: 1.55×. Its premise was wrong, since $\eta^{\rm TL}=0.052$ there and the point is not in the burst regime.
- **A10 (frozen): refuted.** The large-yield optimised masks do **not** act through $d_*$. Their $d_*$ is 0.1996 ($N=3$, $\delta_3=0.02$) and 0.2813 ($\delta_3=0.05$), larger than TL's 0.1922, whereas inverting the TL collapse predicted 0.153 and 0.095.
  - The masks are a strong positive chirp (equivalent to GDD $C\approx2.2$–3.1, stretching the launch 2–3×) plus a negative quartic phase. They delay the compression to $\xi\approx1$–1.5 and raise the yield 1.5× without sharpening it.
  - The mechanism is open (task T-20261016-claude-b-07).
  - Exploratory, not frozen (`overlap.json`): in the $\delta_3=0$ evolution the optimised launches also have *less* spectral content past the ZDW than TL.
    - Maximum over $\xi$ of the fraction at $w\ge w_z$: 0.88× and 0.67×.
    - At $w\ge0.8w_{\rm DW}$: 0.73× and 0.20×.
    - So the unperturbed compressed-spectrum overlap (card sketch 3) does not explain the gain either. The gain must come from the TOD-perturbed dynamics, for example recoil-limited emission or the phase-matching history.
- H3e: the optimised yields lie far below the program value. For example at $N=3$, $\delta_3=0.05$: 0.247 against 0.909. The "within a factor 3" conjecture fails there.

**H4, Raman.** Model M1: $f_R=0.18$, single damped oscillator 12.2/32 fs, $T_0=50$ fs, RK4IP with kernel step at most 2.9 fs; the Julia solver agrees within 1%.

| Part | Outcome |
|---|---|
| H4a | **Confirmed, trivially.** M1 yields stay far below the vacuous program values; Raman makes the momentum constraint one-sided, which only loosens the program. |
| H4b | **Confirmed.** Raman lowers TL burst yields by 770× and 215×, with NSR from −23 to −51 dB at sech $N=2$, $\delta_3=0.02$, against Roy's IPRS curve at about −55. At $\delta_3=0.02$ and 0.05 (Gaussian $N=3$) the reduction is only 3.1× and 1.6×. |
| H4c | **Mixed.** Large-yield masks optimised in M0 keep their full gain in M1. The burst-regime mask loses it (0.03–0.08×). |
| H4d (A5) | **Confirmed.** The singularity law holds in M1 with $d_*$ from the Raman-including TOD-free evolution: Gaussian $N=3$ gives +0.5% (numpy) and +0.6% (Julia). Raman widens the strip ($0.3747\to0.441$ for sech $N=2$; $0.192\to0.235$ for Gaussian $N=3$), which is why it suppresses the burst. |

**Observable pitfalls found here (relevant to the card's "fraction in band $B$ at the output").**
1. In the small-yield regime, a launch that happens to be mid-compression at the output plane has a transient spectrum spilling past the ZDW.
   - Gaussian $N=3$, $\delta_3=0.01$, GDD $C=-0.4$: the band count at $\xi=2$ is 4.1× TL, but 82% of it sits within 10 of the soliton, the peak power there is 5.9, and it is gone by $\xi=4$.
   - The cubic-phase launch at $\delta_3=0.006$: band count 314× TL, against a gated DW headroom of 0.70.
2. In the large-yield regime, a gate fixed at $\tau=0$ is wrong. The solitons recoil and drift (to $\tau\approx30$ by $\xi=6$ at $\delta_3=0.05$), while slow DW near $2w_z$ stays near $\tau=0$. There the ungated band yield is DW: only 1–2% of band photons lie near a soliton.

**Post-session corrections (orchestrator messages on the PI's instruction, 2026-10-16, after 14:56).**
- **Roy framing.** The framing of Roy et al. (2009) in C-20261016-claude-b-01, the derivation note, this log and the PR #45 description was corrected:
  - Eq. 6 is a spectral-peak estimate, validated against Raman-inclusive simulations;
  - Roy et al. themselves report the TOD-only deviation;
  - the gap depends on $\delta_3$;
  - the asymptotic regime lies below their visibility floor;
  - the comparison with Roy's full model is not done;
  - gpt-b's predecessors are added.
  No prediction, number, status or regime bound changed.
- **Memory rules acknowledged** for any further runs: one heavy process at a time, at most about 3 GB each, check `memory_pressure` first, time grids of $2^{14}$ or fewer unless convergence demands more, no full z-histories in memory, mask optimisation one start at a time.
  - None of my processes were running when the rules arrived.
  - Earlier in the session, before the rules, I ran up to 6 concurrent single-threaded Python processes and some grids of $2^{15}$–$2^{17}$ points (the sech $N=4$ and smallest-$\delta_3$ law runs). The plain adjoint stored forward states; the production optimisations used the checkpointed adjoint.

## Changed

- New: `explorations/2026-10-16-claude-b-dw-yield-hypotheses.md` (frozen hypotheses and amendments).
- New: `explorations/2026-10-16-claude-b-dw-singularity-law.md` (derivation note).
- New claims: `claims/C-20261016-claude-b-01-dw-burst-singularity-law.md`, `-02-...`, `-03-conservation-program-vacuous.md`.
- New runs: `runs/2026-10-16-claude-b-dw-program`, `runs/2026-10-16-claude-b-dw-oracle` (figures `fig_singularity_law.png`, `fig_collapse.png`), `runs/2026-10-16-claude-b-dw-shaping`, `runs/2026-10-16-claude-b.7-solver-dwyield`, `runs/2026-10-16-claude-b.7-solver-masks`, `runs/2026-10-16-claude-b.7-solver-m1gauss`.
- Task T-20261016-claude-interactive-03: status done in this PR. New tasks are listed under Loose ends.
- No card edited, no generated file edited, solver submodule untouched.

## Not verified

- The singularity law is supported numerically and by a leading-order heuristic (first-order perturbation plus Laplace's method). It is not proved, and its prefactor is not derived.
- Independence: every check in this PR is by the claude family. The Julia cross-check (claude-b.7) is a second code, not a second family. All three claims need GPT-family verification.
- Roy Fig. 3 values were digitised by eye from the PDF: ±2 dB, and ±0.1 in $\Delta\nu_dT_0$.
- The optimised headrooms are lower bounds from local optimisation with three starts and 60–150 iterations.
  - At $N=8$, $\delta_3=0.05$ the $\xi_f=2$ objective was gamed by an output-plane transient; the persistent gain is 1.01.
  - A persistent objective (yield at $\xi\ge4$, or a soliton-centred gate) should be used in future optimisations (task T-20261016-claude-b-07).
- Literature for the singularity law: a search for analyticity-strip and complex-singularity methods applied to fission DW was cursory. arXiv:2509.07397 (McCue et al., complex singularities and dispersive waves in KdV; **abstract only**) is the closest method found. Karpman, PRE 47, 2073 (1993), DOI 10.1103/PhysRevE.47.2073 (**abstract only**) treats stationary solitons. Pomeau–Ramani–Grammaticos (1988) and the wider exponential-asymptotics literature on Cherenkov radiation were **not accessed** (task T-20261016-claude-b-08).

## Proposed card changes

For P-20261016-claude-interactive-01 (not edited, per instructions):
1. **Sketch 1:** mark it refuted as a ceiling in anomalous dispersion with $\beta_3>0$ (C-20261016-claude-b-03). Replace "the useful improvement over the known Markov ceiling" with: the Gagliardo–Nirenberg control does not help, because $K\to-\infty$ on the band side. In normal dispersion with pure $\beta_2$ the program equals the Cantelli bound; with $\beta_3\ne0$ it is vacuous.
2. **Sketch 3:** replace "amplitude proportional to the soliton's spectral amplitude at resonance" with the singularity law (C-20261016-claude-b-01).
   - The burst yield is set by the narrowest analyticity strip of the unperturbed evolution up to the fibre end.
   - Roy's Eq. 6 is a spectral-peak estimate built on the ejected-soliton strip $\pi/(2(2N-1))$. Roy et al. validated it against Raman-inclusive simulations, and themselves reported that it deviates from TOD-only data.
   - The law accounts for that TOD-only gap and gives its $\delta_3\to0$ exponent, $[\pi/(2(2N-1))-d_*]/\delta_3$.
   - At $N=2$ the gap is 39.5, 12.8 and −0.4 dB at $\delta_3=0.02$, 0.03 and 0.04.
   - Cite the predecessors from gpt-b's review: Austin 2006, Demircan 2007, Driben–Yulin–Efimov 2015, Wai–Chen–Lee 1990, Karpman 1993.
   - With Raman, $d_*$ is computed in the Raman model.
3. **Literature:** upgrade Roy et al. 2009 to full text (claude-b, this session; Eq. 2 convention, Eq. 6, Fig. 3). Add arXiv:2509.07397 (abstract only) as the closest method.
4. **Target quantity:** distinguish (a) band photons at the output plane from (b) radiated DW photons, and state how (b) is measured. Two pitfalls were found:
   - transient compression at the output plane inflates (a) by up to 300×;
   - fixed gates misplace solitons and slow DW.
   Recommend persistence over length plus soliton-centred gating.
5. **Conjecture ("phase-only at most 2×; ceiling within 3×")**, from C-20261016-claude-b-02 and -03.
   - At large TL yields (0.05–0.32) the first part holds: the persistent gains found are 1.54, 1.40, 1.17 and 1.01, and GDD alone gives at most 1.06.
   - In the exponentially small regime it fails: 2.04× at $N=3$, $\delta_3=0.01$, rising as $e^{\kappa/\delta_3}$ to 3.07× at 0.006. That gain is lost with Raman at $T_0=50$ fs (0.03–0.08×).
   - The "within a factor 3" part fails, because the program is vacuous.
6. **Answer to the PI's question, as far as this model goes:**
   - TL Gaussians put 0.1–32% of photons past the ZDW at $\xi=2$ for $N=3$–10, $\delta_3=0.01$–0.05, organised by $d_*/\delta_3$.
   - Simple spectral shaping adds at most about 1.5× where the yield is already 5–16%, and about nothing at 30%.
   - Large relative gains exist only where the yield is tiny, and there they are fragile against Raman.

## Loose ends

- **T-20261016-claude-b-01** (verify, gpt): C-20261016-claude-b-01, the singularity law. Suggested held-out launch: sech $N=4$ or Gaussian $N=5$; relax with self-steepening or $\beta_4$.
- **T-20261016-claude-b-02** (verify, gpt): C-20261016-claude-b-02, shaping headroom. Re-optimise to beat the lower bounds; check persistence.
- **T-20261016-claude-b-03** (verify, gpt): C-20261016-claude-b-03, vacuity of the program and the Cantelli reduction.
- **T-20261016-claude-b-04** (derive): a rigorous lower bound on the analyticity-strip width, giving a provable DW band ceiling. This is the route to a real ceiling now that conservation laws are ruled out.
- **T-20261016-claude-b-05** (derive): closed form of $d_*(N)$ for integer-$N$ sech breathers; large-$N$ scaling.
- **T-20261016-claude-b-06** (explore): minimise $d_*$ over masks in the integrable NLSE. This gives the burst-regime headroom rate $\kappa_{\mathcal S}$ directly.
- **T-20261016-claude-b-07** (explore): large-yield headroom with Raman, self-steepening and length optimisation; Petty comparison.
- **T-20261016-claude-b-08** (literature, gpt): novelty search for C-01 (exponential asymptotics of Cherenkov radiation).
- **T-20261016-claude-b-09** (loose-end): apply the proposed card changes to P-20261016-claude-interactive-01.

Not made into tasks:
- The N = 1 Cherenkov-flux check (`n1_flux_*.json`) was inconclusive: local exponents 1.14–1.37 at $\delta_3=0.055$–0.08, against the asymptotic $\pi/2$, with unstable free fits. It is covered by T-20261016-claude-b-01's known-limit check.
