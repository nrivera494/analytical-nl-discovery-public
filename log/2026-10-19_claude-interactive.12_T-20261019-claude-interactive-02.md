---
date: 2026-10-19
agent: claude-interactive.12
model: claude-opus-5-5
family: claude
task: T-20261019-claude-interactive-02
duration_min: 110
---

## Did

Claude-family verification of C-20261019-pi-chatgpt-01 (GPT 6 Pro's closed-form $c_2(\Phi)$ for the weak-normal-dispersion squeezing law). I followed the clean-context order the orchestrator set for a derivation claim: own derivation and own simulation first, committed and pushed (23111dd, eeb688e, e136364) before opening the proposer's files.

1. **Symbolic derivation** (`derive_c2.py`, SymPy):
   - local scaling $x=y^{1/4}q$;
   - mean field expanded to $O(y)$ in a frame rotating at the constant rate $\Phi$;
   - real tangent generator expanded to second order, with Duhamel time ordering;
   - quasi-degenerate perturbation theory on $M^{\mathsf T}M$ (harmonic-oscillator ground state, branch mixing);
   - exact polynomial-Gaussian algebra throughout.

   The proposer worked in the local mean-phase frame on the output covariance; this route uses a different frame and the other side.
2. **Full mean-plus-tangent propagation** (`lam_min.py`):
   - Fourier interaction picture, DOP853, input restricted to $|x|\le10\sigma$;
   - $\Phi=1$, 1.5, 3, 7 at 10 values of $y$ from $10^{-4}$ to $10^{-7}$, plus $5\times10^{-8}$ and $2\times10^{-8}$ at $\Phi=3$ and 7, and the source's $(\Phi,y)=(10,10^{-6})$;
   - convergence in grid, window, input support, tolerance and parity; an unrestricted-input run; a second integrator (RK4IP with Richardson).
3. **Extra tests.**
   - Sech pulse: $c_2$ predicted from the same derivation, then confirmed by propagation.
   - Small-$\Phi$ probe at $\Phi=0.5$ and 0.25.
   - Ablation of mean reshaping in the derivation.
4. **After my work was committed,** I read the proposer's derivation note (sections 5 and 7), `second_order_symbolic.py` and its output, and report sections 5.5 and 6.1, and compared them line by line.
5. **Wrote and updated:** the audit report, the summary, the claim card and four tasks.

## Found

- **Closed form.** Reproduced exactly. My $r$-form, $c_2=\sqrt6(4r^8+45r^6+102r^4+5r^2+24)/(60(1-r^2)^2(1+r^2)^2)$ with $r=S-\Phi$, equals the card's closed form (symbolic residual 0). It is also character for character the proposer's intermediate expression, which I saw only afterwards.
- **Held-out values.** All pass.

  | $\Phi$ | extrapolated $c_{\rm eff}(y\to0)$ | frozen $c_2$ | slope in $\sqrt y$ |
  |---|---|---|---|
  | 1 | 1.2174395 | 1.21744000 | −1.56 |
  | 1.5 | 1.0525472 | 1.05254743 | −0.79 |
  | 7 | 0.9809822 | 0.98098336 | −0.35 |
  | 3 (source table) | 0.9894640 | 0.98946456 | −0.44 |

  The remainder after the $c_2$ term scales as $y^{0.999\text{–}1.000}$.
- **Sizes of the terms.** At second order, $\langle W_2\rangle$ and the branch-mixing term are each about $4\Phi^2$ times larger than $c_2$, and they nearly cancel. Mean reshaping contributes exactly $1/\sqrt6$ at every $\Phi$.
- **Shape dependence.** For sech, $c_2^{\rm sech}=c_2-1/(8\sqrt6)$, confirmed to $4\times10^{-7}$ at $\Phi=1$ and 3. The closed form is specific to the Gaussian.
- **General shape.** For any smooth unchirped peak $p=1-x^2+\kappa_4x^4$, the second-order term is linear in $\kappa_4$, so $c_2(\Phi,\kappa_4)=c_2(\Phi)-\tfrac{\sqrt6}{8}(\kappa_4-\tfrac12)$. A third shape ($\kappa_4=0$, intensity $e^{-x^2-x^4/2}$) was predicted before computing (commit 76856b7). Symbolic: exact. Propagation: within $4\times10^{-7}$ at $\Phi=1$ and 3. Filed as claim C-20261019-claude-interactive.12-01 (cheap-checks-passed), with four frozen held-out cases for a verifier from another family.
- **Small $\Phi$.** The slope grows about as $\Phi^{-3.6}$. Extrapolation still recovers $c_2$: $3\times10^{-5}$ off at $\Phi=0.5$, 0.05% off at $\Phi=0.25$.
- **Source's single-point values.** 0.98943 and 0.97998 are off by $\sim10^{-4}$ and $2\times10^{-5}$ (relative $\lambda$ errors near $10^{-11}$, the scale of its finite-difference grid error). My values are 0.989325 and 0.980000.

## Changed

- `claims/C-20261019-pi-chatgpt-01-...md`:
  - status `cheap-checks-passed` → `sim-verified`; `verified_by: claude-interactive.12`, `verifier_family: claude`;
  - Checks rows filled;
  - prediction 3 and the regime annotated with the measured values (no narrowing);
  - outcome and audit-trail row added.
- New: `claims/notes/audit-2026-10-19-claude-interactive.12-C-20261019-pi-chatgpt-01.md` (verdict `pass`).
- New: `docs/summary-2026-10-19-claude-interactive.12-C-20261019-pi-chatgpt-01.md`.
- New run `runs/2026-10-19-claude-interactive.12-c2-weak-dispersion-verification/`:
  - code: `derive_c2.py`, `lam_min.py`, `sweep.py`, `analyse.py`;
  - records: `config.yaml`, `meta.yaml`, `summary.json`, `derive_c2*.json`, `fig_summary.png`;
  - raw JSONL in `~/analytical-nl-discovery-data/2026-10-19-claude-interactive.12-c2-weak-dispersion-verification/`.
- New claim `claims/C-20261019-claude-interactive.12-01-weak-dispersion-c2-peak-shape.md`, added to the problem card's `claims` list.
- New tasks T-20261019-claude-interactive.12-01 to -05. Task -04 (shape dependence) was done in this session and is set to `done`.
- Task T-20261019-claude-interactive-02 → `done`.

## Not verified

- **The general-shape claim C-20261019-claude-interactive.12-01.** It rests on my own derivation and simulations only (same family), so it is not verified. The affine dependence on $\kappa_4$ follows from linearity of the second-order term; a symbolic run with a free $\kappa_4$ took over 20 minutes and was stopped, so the formula was checked at three numeric $\kappa_4$ values rather than for general $\kappa_4$ (T-20261019-claude-interactive.12-05).
- **Exclusion of remote competitors.** Unrestricted input was checked only at $y=10^{-4}$ on a 1024-point grid; smaller $y$ used inputs within $10\sigma$ of the peak. No proof of the global bound (T-20261019-claude-interactive.12-01).
- **No physical relaxations** (Raman, $\beta_3$, self-steepening, loss, finite bandwidth), and the PI's Julia solver was not used (T-20261019-claude-interactive.12-02).
- **Not checked independently:** the proposer's hand-integrated $S_1^\dagger e$ and $V_1$. My calculation does not use them, and the final coefficients agree.
- **Wall time** in `meta.yaml` (1500 s) is an estimate summed from the sweep logs, not a measured total.

## Loose ends

- T-20261019-claude-interactive.12-01: prove the spectral-localization bound and a uniform remainder.
- T-20261019-claude-interactive.12-02: realistic-fibre corrections ($\beta_3$, Raman, bandwidth).
- T-20261019-claude-interactive.12-03: clean-context adversarial audit, non-gpt, for `audited`.
- T-20261019-claude-interactive.12-04: derive and test $c_2(\Phi,\kappa_4)$; done in this session.
- T-20261019-claude-interactive.12-05: verify C-20261019-claude-interactive.12-01 (another family).
