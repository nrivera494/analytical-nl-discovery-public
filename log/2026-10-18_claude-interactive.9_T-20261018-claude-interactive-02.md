---
date: 2026-10-18
agent: claude-interactive.9
model: claude-opus-5-5
family: claude
task: T-20261018-claude-interactive-02
duration_min: 90
---

## Did

Cross-family (Claude) verification and adversarial audit of C-20261018-pi-chatgpt-01, the PI's GPT 6 Pro passive-mask ceiling on Zakharov–Shabat eigenvalues, following the adapted clean-context protocol in the task:

1. Read only the claim card, the problem card and the orchestrator's run `2026-10-18-claude-interactive-zs-moment-bound-check`. Wrote my own proof of (A)–(C) and checked the (E)/(F) constants. Wrote an independent ZS solver (Fourier collocation with exact discrete eigenvalue gradients; Boffetta–Osborne transfer matrices with Romberg extrapolation). Ran the solver validation, the Gaussian adversarial mask searches and the asymmetric-source counterexample. Committed this as 830c8d6 before opening the derivation note.
2. Read `claims/notes/C-20261018-pi-chatgpt-01-derivation.md` and checked it line by line (audit report, Part 3).
3. Ran the sech adversarial searches ($N=2,3,4,6$, 2.5, 4.5, 7.5), the summary figure, and a Raman GNLSE check in the agents' solver (b9fa957).
4. Updated both claim cards, wrote the audit report and the PI summary.

Runs: `2026-10-18-claude-interactive.9-zs-solver-validation`, `2026-10-18-claude-interactive.9-mask-adversary`, `2026-10-18-claude-interactive.9-asym-counterexample`, `2026-10-18-claude-interactive.9-raman-escape`.

## Found

- **The claim holds; verdict pass, no blocker.** My independent proof of (A) uses $\theta=\arctan(|v_2|/|v_1|)$, $\theta'\le|q|-\eta\sin2\theta$, Young's inequality and an antiderivative. It is the same argument as the proposer's note, which is correct line by line. Clarifications, not gaps: $q\in L^1$, and absolute continuity of $\theta$. The (E)/(F) Hausdorff–Young constants and the physical units were rederived.
- **Solver.** TL sech $\eta=N-\frac12$ to $2\times10^{-13}$. The source's Gaussian TL fractions are reproduced to $10^{-10}$ (0.491250757965 at $N=4$). $q_*$ attains equality in (A) to 13 digits at $p=1.5,2,3,7$. (A) holds on 69 eigenvalues of random complex potentials (minimum ratio 1.022). Run `2026-10-18-claude-interactive.9-zs-solver-validation`.
- **(C) adversarial:** 13 searches each at $N=2,3,4,6$. Every optimum is TL; the excess over $N-\frac12$ is ≤ $2.3\times10^{-12}$, which is solver error.
- **Held-out (D)/(E):** sech $N=4.5$, 7.5 and Gaussian $N=5$, 8. The ceilings are reproduced, and no mask beats TL at all (also at sech $N=2.5$ and Gaussian $N=1.5$, 4). Run `2026-10-18-claude-interactive.9-mask-adversary`.
- **Counterexample to C-20261016-claude-a-01 reproduced.** $S=\pi\cos(1)e^k\mathrm{sech}(\pi k/2)$; TL $\eta=0.2142789$, one bound state. Passive masks give up to +2.78%, phase-only +2.65%, and the explicit cubic phase $e^{-0.5i(k-1)^3/6}$ +1.12%; FC and BO agree. The hierarchy gives only $f_1\le1$ for $n\le20$, as the source says. Run `2026-10-18-claude-interactive.9-asym-counterexample`.
- **Mild asymmetry is not enough.** On C-a-01's own held-out spectrum $\mathrm{sech}(\pi k/2)(1+\frac12\tanh k)$ ($A=2$, 4) no mask beats TL (≤ $7\times10^{-16}$; `mild_asym.py`), consistent with claude-a's H2b.
- **Raman.** The propagated leading eigenvalue of a TL $N=2$ sech exceeds the passive-mask ceiling by up to 10.4% at 65 fs and 4.1% at 200 fs; without Raman, ≤ 0.16%. Run `2026-10-18-claude-interactive.9-raman-escape`.
- **Real-$p$ majorant.** The card's remark that the majorant step fails for non-even $p$ is confirmed: a phase-only mask on a three-bump spectrum gives $\|q_m\|_3/\|q_0\|_3=1.0101$ (script `majorant_realp.py` in run `2026-10-18-claude-interactive.9-zs-solver-validation`).
- **Card bookkeeping.** The Gaussian $N=1.5$ "held-out" values are in the source README's table.
- **Practical.** With load average about 19 on this machine, scipy's LU was 15x slower than single-threaded. Set `OPENBLAS_NUM_THREADS=1` for dense linear algebra.

## Changed

- `claims/C-20261018-pi-chatgpt-01-passive-mask-zs-eigenvalue-bound.md`: cheap-checks-passed → audited; verified_by and audited_by claude-interactive.9 (claude); solver_commit b9fa957 (the Raman check; the ZS checks use the independent solver); Checks rows filled except Novelty; assumption 6 added (regularity, $S\ge0$); Outcome and audit trail. Statement and regime unchanged.
- `claims/C-20261016-claude-a-01-tl-maximizes-leading-zs-eigenvalue.md`: proposed → refuted (counterexample reproduced, run `2026-10-18-claude-interactive.9-asym-counterexample`); Checks row, Outcome, audit trail.
- New: `claims/notes/audit-2026-10-18-claude-interactive.9-C-20261018-pi-chatgpt-01.md`, `docs/summary-2026-10-18-claude-interactive.9-C-20261018-pi-chatgpt-01.md`, four run folders.
- Task T-20261018-claude-interactive-02 → done.

**Proposed problem-card changes (P-20261016-claude-interactive-03; I did not edit it).**
- "Claims and current results" table: C-20261016-claude-a-01 → refuted (asymmetric-source counterexample, +2.8% for passive masks, +2.6% phase-only); add C-20261018-pi-chatgpt-01 → audited (novelty pending): TL is globally optimal for integer-order sech lasers, with explicit ceilings for non-integer sech and Gaussian lasers.
- Status-of-sketches note: "In every test the transform-limited launch also maximises the leading eigenvalue" is no longer true in general (asymmetric spectra); for integer-order sech it is now a theorem, so $H_{\mathcal S_{A\phi}}=1$ exactly there, not $\le2N/(2N-1)$.
- "Answer to the PI's question so far": "Spectral phase adds ... nothing in the integrable limit" holds for integer sech (theorem) and numerically for non-integer sech and Gaussian lasers, but not for asymmetric spectra (≥ 2.6% phase-only for the counterexample source).

## Not verified

- Novelty of (A) and of the passive-mask corollaries: not searched by me (task T-20261018-claude-interactive-03). Search terms worth trying: eigenvalue bounds for non-self-adjoint one-dimensional Dirac operators with $L^p$ potentials; single-eigenvalue Lieb–Thirring bounds for Zakharov–Shabat.
- The supremum over passive masks for the asymmetric source: my best is +2.78%; the searches are not converged with respect to the mask class, so the true headroom may be larger.
- Whether TL is exactly optimal for non-integer sech and Gaussian lasers: no mask beat TL (gains ≤ 1e-14), but this is a search, not a proof.

## Loose ends

- Exact TL optimality for non-integer sech and Gaussian lasers (no mask beat TL; the ceilings are not approached): T-20261018-claude-interactive.9-01.
- The converged passive-mask headroom for asymmetric spectra, and its mechanism (≥ 2.78% for the counterexample source): T-20261018-claude-interactive.9-02.
- Apply the proposed P-20261016-claude-interactive-03 card changes above: T-20261018-claude-interactive.9-03.
- Novelty of (A) and its corollaries: already T-20261018-claude-interactive-03 (another agent).
