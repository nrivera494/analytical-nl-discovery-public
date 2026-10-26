---
date: 2026-10-17
agent: claude-interactive.7
model: claude-opus-5-5
family: claude
task: T-20261017-claude-interactive.7-01
duration_min: 85
---

## Did

- **PI question (chat, 2026-10-17):** after equilibration to a condensed state at large $n$, can the condensate be squeezed by subsequent Kerr, or has it lost phase coherence or gained excess intensity noise?
- Created and claimed T-20261017-claude-interactive.7-01. The work was first committed on the branch of T-20261016-claude-interactive.7-01, after its PR (#51) had been merged; it was moved here, and that task's merged log was left unchanged.
- Run `2026-10-17-claude-interactive.7-condensate-kerr-squeezability`:
  - the condensate's reduced covariance in its own amplitude/phase frame along the GRIN trajectories of `…-grin-gaussian-state` (same launch and disorder seeds);
  - the Kerr phase needed for −3 and −10 dB after a subsequent single-mode stage;
  - the best squeezing including the crescent curvature;
  - an exact single-mode Kerr check of the curvature law;
  - a balanced-Sagnac check with a shot-to-shot pump spread;
  - the condensate's phase jitter from the shot-statistics ensembles.
- Wrote exploration note §6.8 and updated the card's current answer and Lab test. Completed the note's header list of run folders.
- **PI question:** how was the condensate's own squeezing (−5 to −8 dB) established? It came from the tangent-map covariance, and "from its own Kerr" was my interpretation. I checked both:
  - a step-size test;
  - an independent truncated-Wigner ensemble (768 trajectories, full nonlinear propagation, same fibre);
  - a self-phase-only reference (`own_squeezing_checks.py`).
  The task was broadened to cover the follow-up questions.
- **PI question:** is thermalization in the model from nonlinearity alone? Show it directly. Run `2026-10-17-claude-interactive.7-grin-thermalization-visual`: four single trajectories (two launches, Kerr only against Kerr plus weak linear intra-group coupling), figures, and note §6.9.

## Found

1. **Phase coherence and intensity noise survive equilibration before scrambling.** At $n=10^{10}$ the condensate's quantum phase variance is $10^{-8}$–$10^{-6}$ rad$^2$ for $z=10$–$150L_{\rm NL}$; Wigner ensemble and linearized $V_P/4\bar n_0$ agree within 16% for $z=5$–50. Its Fano factor is 1.0–2.5 for $z\le50$.
2. **What limits direct Kerr squeezing is the mixedness $\nu$**, i.e. entanglement with the cloud, seen as phase noise uncorrelated with the condensate's photon number. After a stage of nonlinear phase $\Phi$, $\lambda_{\min}\simeq\nu^2/(V_P+4\Phi C+4\Phi^2V_X)$, which tends to $V_{P|X}/4\Phi^2$. Excess amplitude noise alone does not hurt.
3. **Curvature law.** Exact single-mode Kerr of a coherent state: best variance $0.945\,\bar n^{-1/3}$ (slope $-0.337$, $\bar n=10^2$–$10^6$). For the condensate, $\lambda_{\rm best}\simeq0.945(\nu^4/\bar n_0)^{1/3}$. At $\bar n_0=10^{10}$ that is −11 to −22 dB for $z=10$–$50L_{\rm NL}$ (coherent state −34 dB), and none by about $200L_{\rm NL}$. −10 dB needs $\Phi=2$–22 rad for $z=10$–50 (coherent 1.4 rad).
4. **After scrambling**, or for a phase-randomized ensemble, the condensate is Fock-diagonal. Kerr leaves it unchanged, so no Kerr stage acting on the mode can squeeze it [exact].
5. **A balanced Sagnac squeezer** rejects the pump's noise to first order. Its floor is the pump's relative power spread squared: −26 dB for the Dirichlet condensate ($K=5$), −34 dB for 2% jitter. The Gaussian check agrees within 1%.
6. **Laser jitter forces self-referencing.** 1% amplitude jitter gives 0.19 rad RMS of condensate phase jitter at $10L_{\rm NL}$ and 0.94 rad at 50, through the fibre's own Kerr.
7. **The condensate's own squeezing is confirmed.** dz = 0.02 and 0.01 agree to 0.01 dB. The Wigner ensemble gives −5.1, −6.1, −6.0, −8.1, −5.7, −5.6, −1.0 dB (±0.2–0.25), against −4.9, −5.7, −5.7, −7.9, −5.8, −5.6, −1.4 dB from the tangent map, at $z=1$–100. The shear is 84–91% self-phase modulation, which alone would give −18 to −38 dB; the cloud's cross-phase noise sets the level, $\lambda\approx V_XV_{P|X}/V_P$.
8. **What drives thermalization in the model.** Kerr moves power between groups; the linear coupling cannot. RJ/Dirichlet is reached only with the weak linear intra-group coupling:
   - $E'=0.6$ launch: $\langle I_0\rangle$ 0.735 against 0.739; $g^{(2)}$ 1.862 against 1.867; ${\rm Var}\,I_0$ $1.45$ against $1.48\times10^{-3}$.
   - Kerr only, same launch: a generalized Gibbs state (groups off by up to 40%, $g^{(2)}$ 1.73).
   - An LP11-only launch never moves without noise. With a vacuum seed and the weak coupling it condenses to 0.564 (RJ 0.565) at $z\approx100$–150. With Kerr only it stays in LP11.

## Changed

- New: `runs/2026-10-17-claude-interactive.7-condensate-kerr-squeezability/` (with `own_squeezing_checks.*`), `runs/2026-10-17-claude-interactive.7-grin-thermalization-visual/` (trajectories in `~/analytical-nl-discovery-data/`); `tasks/T-20261017-claude-interactive.7-01-…` (done).
- Updated: exploration note (§6.8, §6.9, answer in brief, header run list); problem card (current answer item 6, Lab test, exact-GRIN paragraph); task scope and title.

## Not verified

- Linearized (pre-scrambling) GRIN model, 15 modes, one launch geometry.
- The subsequent stage is ideal: lossless, single-mode, no dispersion, Raman or GAWBS.
- The curvature term assumes a Gaussian phase spread. The Sagnac statement is first-order Gaussian algebra; second-order pump-noise coupling was not computed.
- Thermalization runs are single trajectories of the resonant model with exactly equidistant groups and Brownian disorder. The stability of the LP11 state under Kerr alone was observed for one phase draw and one seed, not analysed.
- Proposer-family work only; nothing here counts as verification.

## Loose ends

- A check beyond the linearized model, with loss, Raman and the stage's dispersion, belongs with T-20261016-claude-interactive.7-10 (photon-counting squeezing law) and -12 (realistic experiment model). No separate task was created.
