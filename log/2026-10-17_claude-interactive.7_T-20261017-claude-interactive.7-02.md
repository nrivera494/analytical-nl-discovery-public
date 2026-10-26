---
date: 2026-10-17
agent: claude-interactive.7
model: claude-opus-5-5
family: claude
task: T-20261017-claude-interactive.7-02
duration_min: 130
---

## Did

- **Request.** PI request relayed by the orchestrator (claude-interactive) with review notes on PR #55: "address multiple launches as appropriate and multiple disorder realizations, commenting on whether the original quenched disorder model is valid."
- Created and claimed T-20261017-claude-interactive.7-02 from main at 77e285c.
- **Literature** (orchestrator note 1).
  - Read the full text (HTML via ar5iv or arXiv, through a fetch tool's extraction) of Fusaro et al., PRL 122, 123902 (2019) (arXiv:2011.05111); Garnier et al., PRA 100, 053835 (2019) (arXiv:2011.03918); and Berti et al., PRL 129, 063901 (2022) (arXiv:2207.08680).
  - Abstracts only: Ferraro et al., arXiv:2505.11299 (review), and Torres et al., PRL 136, 173801 (2026) (arXiv:2512.17777).
  - Two further items found and not accessed (arXiv:2309.02215, 2601.16998).
  - Search strings: "Garnier Fusaro Picozzi Wave condensation with weak disorder versus beam self-cleaning in multimode fibers"; "Berti Baudin Fusaro Millot Picozzi Garnier strong disorder thermalization multimode optical fibers ..."; "Interplay of thermalization and strong disorder ... DOI arXiv".
- **Pre-registration.** Froze predictions for three run folders in commit 1e377a7 (T1–T5, D1–D5, Q1–Q6), before any run.
- **Runs, serially, one light process at a time** (memory 67–83% free throughout):
  - `2026-10-17-claude-interactive.7-ensemble-thermalization` (158 single trajectories);
  - `-disorder-model-scan` (84; white-noise strength 0.1–3 and piecewise-constant coupling with $l_c=0.1$–100 $L_{\rm NL}$);
  - `-ensemble-squeezing` (60 tangent-map runs);
  - a post-hoc step-size check of the strong-disorder result.
- **Mistake.** My queue waited on `pgrep -f <script>`, which matched its own command line, so the disorder scan was idle for a few minutes before I noticed and restarted it.
- **Write-up.** Exploration note §6.10 (new); superseded marks in §6.8; card (literature, current answer, Lab test, Risks, audit trail); claims C-01 and C-03 (ensemble records).

## Found

1. **Weak disorder ($\sigma=0.3$): the RJ/Dirichlet endpoint self-averages and does not depend on the launch.**
   - 12 disorder seeds / 12 launch draws per $E'$: $\langle I_0\rangle$ = 0.869 ± 0.003 / 0.871 ± 0.003, 0.740 ± 0.004 / 0.738 ± 0.005, 0.612 ± 0.007 / 0.610 ± 0.005, against 0.870, 0.739, 0.609.
   - $g^{(2)}$ 1.85–1.87; ${\rm Var}\,I_0$ / Dirichlet 0.96–1.01.
   - The spread is within twice the block error (T2 passes).
   - Post-hoc Dirichlet tail test: 0.0426–0.0440 against 0.0435.
2. **Kerr only: launch-specific endpoints.** 0.834 ± 0.021, 0.700 ± 0.038, 0.576 ± 0.041: below RJ by 0.03–0.04, with seven to eight times the spread and $g^{(2)}$ 1.71–1.78. An all-LP11 launch never leaves LP11 (12/12). The centre-focused C-03 values are reproduced (0.699, 0.581), and weak disorder erases them (12/12).
3. **All-LP11 launch with weak disorder:** condenses in 12/12 at $z_{\rm on}=106$–161 $L_{\rm NL}$, to 0.565 ± 0.006 against 0.566.
4. **Disorder strength.** Relaxation is fastest near $\sigma\approx0.3$ ($L_d\approx11L_{\rm NL}$).
   - Median $L_{\rm rel}$ is 126 $L_{\rm NL}$ at $\sigma=1$ and 753 at $\sigma=3$ ($L_d\approx0.1L_{\rm NL}$, the realistic range). The all-LP11 onset is about 3000 at $\sigma=3$.
   - This is the kinetic slowing of Fusaro and Garnier (rate $\propto\gamma^2/\Delta\beta$). D2 passes; D1 and D5 fail at $\sigma=3$.
   - Step-size check: the same piecewise realization gives 717 and 714 $L_{\rm NL}$.
5. **Correlation length.** At matched strength, $l_c=0.1$–10 $L_{\rm NL}$ behaves like white noise (RJ; relaxation within a factor 2–4, below the metric's resolution). At $l_c=100L_{\rm NL}$ the endpoint shifts 0.01–0.02 above RJ with suppressed fluctuations. Real $l_c\lesssim1.5L_{\rm NL}$.
6. **Squeezing.**
   - The condensate's own squeezing does not self-average at $\sigma=0.3$: −9.6 ± 2.9, −9.8 ± 3.0, −8.4 ± 3.9 dB at $z=10$, 20, 50 ($f_0\approx0.85$). The reference realization (−7.9, −5.8, −5.6) was on the weak side; Q1–Q3 fail toward more squeezing.
   - $\lambda_{\rm best}$ and $\nu$ self-average: −23.4 ± 1.9, −13.2 ± 2.5, −6.8 ± 2.3 dB at $z=10$, 50, 100. Q4 passes.
   - Strong disorder: similar levels with three to six times smaller spread, and squeezing that lasts longer. Q5 passes.
7. **Sagnac floor of a Dirichlet-thermalized condensate:** −25.9 dB on average (range −27.2 to −25.0; Dirichlet −25.7). Q6 fails narrowly on one realization.
8. **Verdict.**
   - The disorder model is the right class (weak, intra-group, $\beta_0l_c\gg1$). The white-noise idealization is fine for $l_c\lesssim10L_{\rm NL}$. The original strength is 30–500 times too weak in $L_d$.
   - Endpoint conclusions stand. Relaxation lengths and single-realization squeezing numbers are model-specific or atypical and are now marked superseded.
   - Open: at realistic strength, this 15-mode model needs about $10^3L_{\rm NL}$ to thermalize.

## Changed

- New runs: `runs/2026-10-17-claude-interactive.7-ensemble-thermalization/`, `-disorder-model-scan/`, `-ensemble-squeezing/`. Raw series are in `~/analytical-nl-discovery-data/`.
- Updated: `explorations/2026-10-16-claude-interactive.7-quantum-rj-state.md` (§6.10 new; §6.8 superseded marks; §6.9 limits; §7); the problem card (literature on disorder, items 4–6, Lab test, Risks, audit trail); claims C-01 and C-03 (ensemble records).
- Tasks: T-20261017-claude-interactive.7-02 done; new T-20261017-claude-interactive.7-03 (vector model with polarization disorder and inter-group coupling).

## Not verified

- **Model scope.** All runs use the scalar resonant model: 15 modes, exactly equidistant groups, intra-group disorder only. Polarization and inter-group coupling are absent (T-20261017-claude-interactive.7-03).
- **Window length.** The thermalization window $z\le4000L_{\rm NL}$ is too short to see the strong-disorder endpoint. That RJ is reached eventually at $\sigma=3$ is taken from the kinetic theory, not observed.
- **Relaxation metric.** The pre-registered metric $L_{\rm rel}$ cannot resolve relaxation faster than about 50 $L_{\rm NL}$. The 10-$L_{\rm NL}$ version is post hoc.
- **Literature access.** The literature was read through a fetch tool's extraction of the HTML full text, not line by line. Physical disorder values are their simulation estimates, not measurements.
- **Independence.** Proposer-family work only; nothing counts as verification. GPT-family agents are unavailable until 22 Oct, 06:43.

## Loose ends

- T-20261017-claude-interactive.7-03: vector GRIN model with polarization disorder (Fusaro–Garnier) and inter-group coupling (Berti), to test which scalar-model conclusions survive at realistic disorder.
- The gap between about $10^3L_{\rm NL}$ (this model at realistic disorder) and metre-scale experiments belongs with T-20261016-claude-interactive.7-04 (Lyapunov and thermalization in real fibres) and -03.
