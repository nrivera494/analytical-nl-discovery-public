---
date: 2026-10-19
agent: claude-interactive.13
model: claude-opus-5-5
family: claude
task: T-20261019-claude-interactive-03
duration_min: 115
---

## Did

Claude-family verification of C-20261019-pi-chatgpt-02 (proposer GPT 6 Pro, family gpt): the similariton matched-LO phase variance (i), the short-gain squeezing criterion with full ASE (ii), and the large-gain floor (iii). I followed the adapted clean-context protocol in the task:

1. I read only the claim card, C-20261008-claude-a-01/-02 (model and notation) and P-001. I derived (ii), including its second-order term at the boundary, and the reduced matched-LO covariance myself.
2. I wrote two codes:
   - `reduced.py`: leading-order Legendre $l=0,2$ hydrodynamic covariance with intensity-quadrature ASE, carrying the energy-locked phase analytically so that $1-r^2$ has no cancellation;
   - `fullfield.py`: linearized gain NLSE with both vacuum and both reservoir quadratures, exact discrete adjoint, commutator bookkeeping, checkpointed.
3. I ran (i)/(iii) at $\Gamma=\sqrt{18}$ and the held-out $\Gamma=1$ to $\tau=80$; (ii) slopes for smoothed parabolas and a Gaussian at $n_{sp}=1,2$; the explicit squeezed case; and full field against reduced at $\tau\le4$. I committed this attempt (4ff455f) before opening any of the proposer's material.
4. I wrote a truncated-Wigner (nonlinear) check of (ii), `twa.py`, and started it before reading. Then I read TECHNICAL_NOTES.md, report sections 4.1–4.4 and analysis_summary.json, and checked them. I reproduced the source's numbers on the source's launch with my code (`source_seed.py`).
5. Extra checks: $\Gamma=0.5$, 2, 10 in the reduced model; finite-length squeezing below the short-length threshold (closed-form slot model `slot_model.py`, full field `finite_length.py`); a truncated-Wigner mode-count test at small $N_0$.
6. Claim card, audit report, PI summary, figure, three loose-end tasks.

Run: `2026-10-19-claude-interactive.13-similariton-lo-verification`.

## Found

- **Verdict pass; status sim-verified.** (i), (ii) and (iii) hold in the stated regime. All five frozen predictions, including the held-out ones, are confirmed.
- **(i).** Fitted power of $\varepsilon_0^2C_{PP}$:
  - 2.33350 over 12–26 and 2.333333 over 26–40 ($\Gamma=\sqrt{18}$, asymptotic seed, $n_{sp}=1$; source 2.3335);
  - held-out $\Gamma=1$: 2.33175 over 12–26, 2.333314 over 26–40, 2.3333331–2.3333334 for equal-phase pairs over 40–80;
  - ratio $C_{PP}/[(32n_{sp}/9)G\Phi_{NL}^2]$: [0.9904, 1.0023] ($\Gamma=\sqrt{18}$) and [0.99981, 1.00130] ($\Gamma=1$) over 12–26, within $3\times10^{-7}$ of 1 over 40–80;
  - the error envelope falls as $G^{-0.334}$, against $-1/3$ from the $p_0$–$p_2$ cross-covariance (nonzero because the ASE metric couples $l=0$ and 2);
  - also verified at $\Gamma=0.5$, 2 and 10 with unchirped and chirped seeds (power 2.3309–2.3348 over 12–26);
  - the reduced code reproduces C-20261008-claude-a-02 table P4 to every digit.
- **(ii).** Full-field initial slope $=2n_{sp}g(1-R)$ to $7\times10^{-7}$; the root is within $3.3\times10^{-9}$ of $R=1$ for six shape/chirp/$n_{sp}$ cases.
  - Held-out $n_{sp}=2$ thresholds: Gaussian 2.828427; smoothed parabola 2.50699, 2.50030 and 2.500076 at $\delta=0.05$, 0.01, 0.005, converging to 5/2 as $\delta^{1.98}$.
  - The commutator is restored by the reservoir to $\le4\times10^{-13}$; without it, it would be $G$.
  - Source counterexample reproduced on the source's launch: 0.8964864646–53 against 0.8964864655.
- **Boundary correction to (ii).** At $R=1$ the slope vanishes and the $(gz)^2$ coefficient is $2\mathrm{Var}_P(\gamma P/g)-n_{sp}$ (dispersionless; the $-n_{sp}$ is the gain growth of the Kerr rate). It is negative for both shapes at $n_{sp}=1,2$ (full field $-0.85$, $-1.41$, $-0.69$, $-0.76$, matching the formula to four digits). So "if and only if" fails on the boundary; the card now reads "if $R>1$, not if $R<1$".
  - My first expectation ($+2\mathrm{Var}$) omitted the growth term. The full-field code was right, and an exact single-mode check located the error.
- **(iii).** $G^{-1/3}\lambda_{\min}\in[0.338,0.633]$ ($\Gamma=\sqrt{18}$) and [0.247, 0.797] ($\Gamma=1$) over 12–26, and the same over 26–80.
  - Source $\lambda_{\rm LO}(\tau=4)$ reproduced on its launch: 3.1592357 against 3.1592358, plus its $\varepsilon_0=0.1$ and 0.025 values to $1.2\times10^{-7}$.
  - The source's finite-volume and my Legendre reduced results agree to a few $10^{-6}$.
- **Full field against reduced model** ($\tau\le4$): $\varepsilon_0^2C_{PP}/G$ within 0.2%; $\lambda_{\min}$ 4.1–4.2% above the reduced value at $\varepsilon_0=0.05$ and 1.3% at 0.025. The apparent rate with the source's smoothing is $\varepsilon_0^{1.6}$; not established.
- **Truncated Wigner.** At $N_0=10^6$ it reproduces the linearized $\lambda_{\rm LO}$ within $1\sigma$ ($0.4729\pm0.0013$; $0.7999\pm0.0024$ against 0.7978 at $n_{sp}=2$).
  - At $N_0=10^4$ and $10^3$ it gives less squeezing (by 0.015–0.019 and 0.16–0.21), growing with the number of grid modes. I did not separate a physical correction from the TWA validity limit.
  - Since $\Phi_{NL}^2/N_0\le3\times10^{-4}$ there, the card's brightness condition may be insufficient for strongly squeezed variances.
- **Beyond the claim.** In a closed-form dispersionless model, checked against the full field at $\varepsilon_0=0.005$ to $6\times10^{-6}$ and at $\varepsilon_0=0.05$, the matched mode is squeezed at some finite length for $R>R_{\min}$. At $n_{sp}=1$, $R_{\min}=0.781$ (parabola) and 0.902 (Gaussian); at $n_{sp}=2$, 0.956 and 0.991. $R>1$ is the short-length criterion only.
- **Bright field.** At $\varepsilon_0=0.05$, $\Phi_{NL}^2=0.009$ ($\tau=0.02$), $8.97\times10^3$ ($\tau=4$), $4.44\times10^8$ ($\tau=12$) and $5.68\times10^{16}$ ($\tau=26$). For the 500 pJ seed of C-20261008-claude-a-01 ($N_0=2.6\times10^9$), $\Phi_{NL}^2/N_0=3.4\times10^{-6}$, 0.17 and $2\times10^7$ at $\tau=4$, 12, 26. That seed has $\gamma P_0/g=3.1$, i.e. $R=2.5/n_{sp}$, and is predicted to be squeezed at short length.
- **C-20261008-claude-a-02.** No statement there changes because of this work. Its verified block ("squeezed at short gain when $\gamma P_0>5n_{sp}g/4$"; $1-r^2=\Theta(G^{-2/3})$, measured $-0.653$ here) is consistent with these results. Its unverified edge remainder is the subject of task T-20261019-claude-interactive.13-02.

## Changed

- `claims/C-20261019-pi-chatgpt-02-...md`:
  - cheap-checks-passed → sim-verified; verified_by claude-interactive.13 (claude), verifier_model; solver_commit names the independent codes;
  - "as verified" block added; "if and only if" in (ii) marked superseded; regime note for (i)/(iii) ($0.5\le\Gamma\le10$ verified);
  - Checks rows filled (core, error exponent, held-out, convergence, relaxed assumption); Outcome and audit trail.
- New:
  - `claims/notes/audit-2026-10-19-claude-interactive.13-C-20261019-pi-chatgpt-02.md` (Parts 1–2 committed before reading the proposer);
  - `docs/summary-2026-10-19-claude-interactive.13-C-20261019-pi-chatgpt-02.md`;
  - run folder `runs/2026-10-19-claude-interactive.13-similariton-lo-verification/` (raw arrays in `~/analytical-nl-discovery-data/` under the same name);
  - three tasks.
- T-20261019-claude-interactive-03 → done.
- Not edited: C-20261008-claude-a-01/-02, P-001.

**Memory incident.** `curve.py` used a first version of `fullfield.py` that stored the background at every step. Its $\varepsilon_0=0.025$, $\tau=4$ case reached about 5.2 GB, above the 3 GB guideline, and completed. The next run hit the same case and was stopped by the watchdog. I then checkpointed the code: peak 109 MB, same results to $10^{-13}$. The TWA job ran in the background after exceeding the 10-minute foreground limit. I stopped its fourth case ($\tau=1$) unrun so that only one heavy process ran at a time.

## Not verified

- The rate in $\varepsilon_0$ of the full field's approach to the reduced model. It needs $\varepsilon_0\le0.0125$ (lens coordinates); task T-20261019-claude-interactive.13-02.
- Whether the truncated-Wigner shift at $N_0\le10^4$ is physical. It needs a positive-P or exact few-mode calculation; noted in the audit task.
- Raman, finite gain bandwidth with colored ASE, gain saturation, detection loss: excluded by the card, not tested.
- The finite-length threshold $R_{\min}$ is my own result and has not been checked by another family; task T-20261019-claude-interactive.13-03.
- Novelty: not searched by me. The card's bounded search is the source's.

## Loose ends

- Clean-context adversarial audit of C-20261019-pi-chatgpt-02 for status audited (family not gpt): T-20261019-claude-interactive.13-01.
- $\varepsilon_0$-rate of the full-field approach to the reduced matched-LO covariance; bears on C-20261008-claude-a-02's unverified remainder: T-20261019-claude-interactive.13-02.
- Whether to file the finite-length threshold $R_{\min}$ as a claim: T-20261019-claude-interactive.13-03.
