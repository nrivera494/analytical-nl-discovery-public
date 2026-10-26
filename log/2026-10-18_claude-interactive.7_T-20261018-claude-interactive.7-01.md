---
date: 2026-10-18
agent: claude-interactive.7
model: claude-opus-5-5
family: claude
task: T-20261018-claude-interactive.7-01
duration_min: 40
---

## Did

- **Request.** Orchestrator message (claude-interactive, on the PI's instruction): file the squeezing results of card P-20261016-claude-interactive.7-01 as formal claims for a GPT-family verifier, restated within the Gaussian (linearized) validity domain that gpt-b's review of C-20261016-claude-interactive.7-02 put in question (exact one-mode Kerr: det $V=2.51$ against $1/4$ at $n=4096$, $s=4$, coherence 0.996).
- Created and claimed T-20261018-claude-interactive.7-01. The branch merges task/T-20261017-claude-interactive.7-02 (PR #56, still open), so this PR is stacked on #56.
- **Pre-registration.** Froze criteria G1–G4 in `runs/2026-10-18-claude-interactive.7-gaussian-validity/predictions.md` (commit 363ab078) before any check ran.
- **Runs** (one light process, memory well above 35% free):
  - G1, single-mode Kerr on mixed condensate inputs: classical Wigner map, $2\times10^5$ samples, nine inputs taken from the reference and ensemble runs.
  - G2–G3, multimode check: 512 truncated-Wigner trajectories on the tangent map's own trajectory, $E'=0.6$, $\sigma=0.3$, $n=10^6$ and $10^{10}$, $z=5$–100.
  - G4, thresholds: the Gaussian-validity photon number for the own squeezing over the 12-realization ensemble.
- **Write-up.**
  - Claims C-20261018-claude-interactive.7-01, -02 and -03.
  - Verify tasks T-20261018-claude-interactive.7-02, -03 and -04, all with family_required gpt.
  - Note §6.11 (new) and a superseded mark in §6.5.
  - Card: claims list, superseded mark on the multimode squeezing number, photon-counting robustness note, audit trail.
  - Following the orchestrator's instruction, the three existing claim cards were not edited (PR #61 updates them).

## Found

1. **The curvature boundary.**
   - A phase-quadrature spread $V'$ on a crescent of radius $2\sqrt{\bar n}$ adds $V'^2/(8\bar n)$ to the narrow direction. For the multimode quadrature squeezing this gives the validity bound $\sigma_{\max}^6<0.8\bar n_0$.
   - Wigner check: within 0.4 dB of $1/\sigma_{\max}^2$ where the bound holds ($n=10^{10}$, $z\le20$, down to −30.1 dB), and 6–63 dB worse where $\sigma_{\max}^6>8\bar n_0$. G2a and G2b pass.
   - The card's "−55 to −100 dB at $400L_{\rm NL}$" is withdrawn.
2. **Photon-counting squeezing $\lambda_{\rm gen}$ is robust to the curvature.**
   - Within 0.5 dB of the linearized value at every $z\le100$, at both $n=10^{10}$ and $n=10^6$. At $n=10^6$ the estimate of $\lambda_{\rm gen}$ from linear amplitude quadratures fails by up to 29.5 dB.
   - Photon numbers are phase-insensitive. G3b, which predicted breakdown at $n=10^6$, $z=50$ and 100, failed in this favourable direction.
3. **The Kerr stage on the extracted condensate.**
   - Coherent: $0.945\,\bar n^{-1/3}$ within 0.02 dB (G1a pass).
   - Mixed inputs: within 0.7 dB of $0.945(\nu^4/\bar n_0)^{1/3}$ at $\bar n_0=10^{10}$ (9/9).
   - At $10^8$ the formula is pessimistic by 1.1–6.3 dB for 5 of 9 inputs, which are themselves outside their Gaussian regime. G1b and G1c fail at $10^8$.
4. **The condensate's own squeezing.**
   - Gaussian-valid at $\bar n_0\approx10^{10}$ for $z\le50$: the threshold median (maximum) is $5\times10^8$ ($3.1\times10^9$) at $z=50$. $z=100$ is marginal.
   - G4 (maximum below $10^9$ at $z\le50$) fails by the letter on the worst realization.

## Changed

- New run: `runs/2026-10-18-claude-interactive.7-gaussian-validity/` (scripts, config, meta, summary; no raw data).
- New claims: `claims/C-20261018-claude-interactive.7-01-prescrambling-multimode-squeezing-validity.md`, `-02-condensate-own-squeezing.md` and `-03-equilibrated-condensate-kerr-squeezability.md`, all status cheap-checks-passed.
- New tasks: T-20261018-claude-interactive.7-02, -03 and -04 (verify, gpt). T-20261018-claude-interactive.7-01 done.
- Updated: `problems/P-20261016-claude-interactive.7-01-quantum-state-of-rj-thermalized-light.md` and `explorations/2026-10-16-claude-interactive.7-quantum-rj-state.md` (§6.5 mark, §6.11).

## Not verified

- **Independence.** Everything is proposer-family work. The three verify tasks are for GPT-family agents.
- **Multimode curvature ceiling.** C-…-01 prediction 5 (above −35 dB at $n=10^{10}$) is a conjecture by analogy with one mode. I computed the Wigner variance only along the linearized squeezed direction, not the full minimum eigenvalue.
- **Photon counting beyond $z=100$.** Robustness of $\lambda_{\rm gen}$ is untested there (C-…-01 prediction 4). The previous "−20 to −27 dB at 400" is withdrawn rather than confirmed.
- **Truncated Wigner as the reference.** It is checked against exact dynamics only on four modes. For one mode, the classical Wigner map is compared with exact Fock evolution only for coherent inputs.
- **Model scope.** All squeezing numbers come from the scalar 15-mode resonant model at weak Brownian disorder ($\sigma=0.3$, which PR #56 found 30–500 times too weak), plus $\sigma=1$ and 3 for the own squeezing.

## Loose ends

- The three verify tasks above.
- The realistic-disorder vector model is T-20261017-claude-interactive.7-03, and the gap to metre-scale experiments is T-20261016-claude-interactive.7-04. Both already exist, so no new task.
