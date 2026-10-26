---
id: C-20261018-pi-chatgpt-01
problem: P-20261016-claude-interactive-03
title: "No passive spectral mask can raise any Zakharov–Shabat eigenvalue above [∫|q_TL|^(2n)/C_(2n)]^(1/(2n−1)); for integer-order sech lasers the transform-limited pulse is globally optimal (f1,opt = (2N−1)/N²), and Gaussian lasers have at most 0.015% relative headroom at N = 4"
type: bound
status: promoted
proposed_by: pi-chatgpt
proposer_model: gpt-6-pro
proposer_family: gpt
verified_by: claude-interactive.9
verifier_family: claude
audited_by: claude-interactive.9
auditor_family: claude
created: 2026-10-18
updated: 2026-10-18
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: [R-0001, R-0002]
---

> **Provenance.** This result was produced in the PI's own ChatGPT session with **GPT 6 Pro** (family gpt). The conversation is shared at https://chatgpt.com/s/t_6ad4b5574cc48191946a991871e10790; the orchestrator read the full text of its final answer on 2026-10-18. The PI also supplied a README, committed unchanged apart from LaTeX delimiters as [`notes/C-20261018-pi-chatgpt-01-derivation.md`](notes/C-20261018-pi-chatgpt-01-derivation.md). The orchestrator claude-interactive filed this card on the PI's instruction. The earlier turns of the conversation, and the reproduction scripts the README names, are not in the repository.

## Statement

**Setting.** Focusing NLSE $iq_z+\tfrac12q_{tt}+|q|^2q=0$ and the decaying-line Zakharov–Shabat (ZS) problem $v'=\begin{pmatrix}-i\zeta&q\\-\bar q&i\zeta\end{pmatrix}v$.
- A laser has upstream spectral amplitude $S(k)\ge0$. It passes a passive mask, $q_m=\mathcal F^{-1}(mS)$ with $|m(k)|\le1$; the transform-limited (TL) pulse is $q_0=\mathcal F^{-1}S$, and $M_0=\int|q_0|^2$ is the upstream laser energy.
- A discrete eigenvalue $\zeta=\xi+i\eta$, $\eta>0$, carries soliton energy $4\eta$. The leading fraction is $f_1=4\eta_{\max}/M_0$.

**(A) Sharp single-eigenvalue inequality.** For every potential in the decaying-line ZS class with sufficient regularity, every discrete eigenvalue satisfies
$$\int_{\mathbb R}|q(t)|^p\,dt\ \ge\ C_p\,\eta^{p-1}\quad(p>1),\qquad C_p=\frac{p^p}{(p-1)^{p-1}}\,\frac{J_p}{2},\qquad J_p=\int\mathrm{sech}^pt\,dt=\frac{\sqrt\pi\,\Gamma(p/2)}{\Gamma((p+1)/2)}.$$
Equality holds for $q_*(t)=\frac{p\eta}{p-1}\mathrm{sech}\big(\frac{2\eta(t-t_0)}{p-1}\big)$, a sech of soliton order $p/2$, up to constant phase and carrier.

> **Prior art for (A)** (novelty audit, claude-interactive.10, 2026-10-18).
> - **Real potentials.** For real $q\ge0$ and purely imaginary eigenvalues, (A) with the same sharp constant and sech extremizer is Theorem 1.3 at $\lambda=0$ of Dolbeault, Gontier, Pizzichillo & Van Den Bosch, Rev. Mat. Iberoam. 40 (2024) 649–692, DOI 10.4171/RMI/1443, arXiv:2210.03091. The link is the Dirac reformulation of the ZS problem at $\zeta=i\eta$.
> - **Complex potentials.** A weaker constant is in Cuenin, Laptev & Tretter (2014), DOI 10.1007/s00023-013-0259-3.
> - **New in this claim:** the sharp complex and off-axis case, with its angle-weighting proof, and the passive-mask consequences (B)–(F). These were not found in the literature (medium confidence).

**(B) Passive-mask ceiling for any source.** For every integer $n\ge1$ and every $|m|\le1$,
$$\eta_{\max}(q_m)\le U_{2n}[S]=\Big[\frac{\int|q_0|^{2n}dt}{C_{2n}}\Big]^{1/(2n-1)},\qquad f_{1,\rm opt}[S]\le\frac{4}{M_0}\inf_{n\ge1}U_{2n}[S].$$
The cases $n=1$ and $n\to\infty$ recover the energy bound $f_1\le1$ and the peak bound $\eta\le\|q_0\|_\infty$.

**(C) Integer-order sech lasers: TL is globally optimal.** For $q_0=N\,\mathrm{sech}\,t$ with integer $N\ge1$, taking $n=N$ gives $U_{2N}=N-\tfrac12$, which the TL pulse attains. Hence
$$\sup_{|m|\le1}\eta_{\max}(q_m)=N-\tfrac12,\qquad f_{1,\rm opt}=\frac{2N-1}{N^2},\qquad E_{1,\max}=\frac{2(2N-1)|\beta_2|}{\gamma T_0}\ \text{(physical units)}.$$

**(D) Non-integer sech lasers.** For $N>\tfrac12$, $U_{2n}=\frac{2n-1}{2n}N\big(\frac Nn\big)^{1/(2n-1)}$ bounds the headroom over the exact TL value $N-\tfrac12$: at most 0.437%, 0.154%, 0.039% and 0.0074% at $N=2.5$, 3.5, 5.5 and 9.5.

**(E) Gaussian lasers.** For $q_0=Ne^{-t^2/2}$, sharp Hausdorff–Young (attained by Gaussians) gives $\|q_m\|_p\le\|q_0\|_p$ for every real $p\ge2$. Hence
$$f_{1,\rm opt}\le\frac{4}{\sqrt\pi N^2}\inf_{p\ge2}\Big[\frac{N^p\sqrt{2\pi/p}}{C_p}\Big]^{1/(p-1)}.$$
This leaves at most about 0.015% relative headroom over TL at $N=4$ (source table: TL 0.4912507580 against a ceiling of 0.4913243554).

**(F) Spectral-norm bound for any source** (sharp Hausdorff–Young, $p'=p/(p-1)$): $\eta\le\frac{\sqrt{p'}}{2\pi}\big(\frac1{\sqrt p\,C_p}\big)^{1/(p-1)}\int S^{p'}dk$ for $p\ge2$.

## Regime

- **(A):** any $p>1$; decaying-line ZS potentials with enough regularity (smooth, rapidly decaying pulses suffice). Complex fields, asymmetric and multimodal spectra are all allowed.
- **(B):** even exponents only, for a general spectrum. The real-$p$ extension is false in general.
- **(C):** integer $N\ge1$, exact.
- **(D):** $N>\tfrac12$.
- **(E):** Gaussian sources, real $p\ge2$.
- **Scope:** all statements concern the input scattering data, which the integrable NLSE preserves. No small parameter enters; (A)–(E) are claimed exact as inequalities. The numerical TL baselines quoted in (E) are convergence-checked, not interval-certified.

## Assumptions

1. **Integrable model.** The focusing NLSE in soliton units: scalar, with constant $\beta_2<0$ and $\gamma$, and no Raman, higher-order dispersion, loss or self-steepening. These break the inference from initial eigenvalues to final soliton energy. Raman transfer between pulses after launch (Kormokar et al. 2023) is **not** bounded.
2. **Energy assignment.** Discrete eigenvalues carry energy $4\eta$, the standard trace-identity assignment. "Leading" means the largest $\eta$, not the reddest pulse.
3. **Mask class.** Passive spectral masks $|m(k)|\le1$, normalized to the upstream energy $M_0$.
4. **Proof ingredients.** The even-moment Fourier majorant (Lenzmann–Sok Lemma 5.1) for (B), and sharp Hausdorff–Young (Beckner 1975) for (E) and (F).
5. **Not tight in general.** For asymmetric spectra the even-moment hierarchy can be trivial: for $S=\pi\cos(1)e^k\mathrm{sech}(\pi k/2)$, $n=1,\dots,20$ give only $f_1\le1$, according to the source.
6. **Added by the verifier (claude-interactive.9, 2026-10-18).** "Sufficient regularity" in (A) can be taken as $q\in L^1(\mathbb R)$: it gives the Jost asymptotics $\theta(-\infty)=0$, $\theta(+\infty)=\pi/2$, and the angle $\theta=\arctan(|v_2|/|v_1|)$ is then absolutely continuous, which the antiderivative step uses. If $\int|q|^p=\infty$ the inequality is trivial. (B) also needs $S\ge0$ (the TL field is the one with real non-negative spectrum) and $q_0\in L^{2n}$.

## Predictions

Frozen before verification. Values marked † are from the source; values marked ‡ were computed by the orchestrator in run `2026-10-18-claude-interactive-zs-moment-bound-check`, from the bound's closed forms only, and are new.

1. **(C) exactly.** No passive mask, including phase-only, amplitude-and-phase, multi-lobe or asymmetric masks, gives $\eta_{\max}>N-\tfrac12$ for $q_0=N\,\mathrm{sech}\,t$ with $N=2$, 3, 4 and 6, to numerical precision. An adversarial optimizer should find no excess beyond solver error.
2. **(A) sharpness.** $q_*$ has a bound state at $\zeta=i\eta$ with equality in (A), for $p=1.5$, 3 and 7.
3. **(D) ceilings:**
   - from the source† and reproduced: 0.43672% ($N=2.5$), 0.15446% (3.5), 0.03888% (5.5), 0.00743% (9.5);
   - held out‡: **0.07161% at $N=4.5$** and **0.01518% at $N=7.5$**.

   Any mask found for a non-integer-$N$ sech must stay below the ceiling for its $N$.
4. **(E) fraction ceilings:**
   - from the source† and reproduced: 82.65046%, 62.12206%, 49.13244%, 34.41023% and 21.42475% at $N=2$, 3, 4, 6 and 10;
   - held out‡: **95.46241% at $N=1.5$**, **40.50316% at $N=5$** and **26.41798% at $N=8$**.
   - The source's TL fractions (for example 0.4912507580 at $N=4$) should be reproduced by an independent ZS solver within about $10^{-9}$.
5. **Counterexample to C-20261016-claude-a-01.** For the asymmetric source $S=\pi\cos(1)e^k\mathrm{sech}(\pi k/2)$, a passive mask raises $\eta_{\max}$ above the TL value by about 1% (source; its details were not supplied). An independent reproduction, with a run id, is required. The hierarchy (B) should give only $f_1\le1$ there for $n\le20$.

## Derivation

See [`notes/C-20261018-pi-chatgpt-01-derivation.md`](notes/C-20261018-pi-chatgpt-01-derivation.md): the proofs of (A) via the spinor-angle inequality $\theta'\le|q|-\eta\sin2\theta$ and a sharp convexity inequality; (B) via the even-moment majorant; (C)–(F). Auditors do not read it until their report is committed.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Dimensionless ZS normalization; the physical-unit form (C) uses $D=|\beta_2|/\gamma$, and the normalization time cancels (source). **Rederived:** with $q=T_0A/\sqrt D$, $E=\frac D{T_0}\int|q|^2$, the bound becomes $E_1\le4[D^{n-1}C_{2n}^{-1}\int P_0^n dT]^{1/(2n-1)}$ ($D^{p/2-1}$ for real $p$), $T_0$ cancels, $E_{1,\max}=2(2N-1)D/T_0$ | claude-interactive.9 (claude) | — (algebra in the audit report) | 2026-10-18 |
| Known limits | $p=2$: $\eta\le\|q\|_2^2/4$; $p\to\infty$: peak bound; $p\to1$: the area condition $\|q\|_1\ge\pi/2$ (Klaus–Shaw). **Checked:** $C_2=4.000000000000001$; $C_p=1.57229$ at $p=1.0001$ ($\pi/2=1.570796$); $C_p^{1/(p-1)}=1.00007$ at $p=10^5$; the proof at $p=1$ gives $\int|q|\ge\pi/2$ directly. Sharpness: $q_*$ at $p=1.5,2,3,7$ ($\eta=1$, 2.3) has leading eigenvalue $i\eta$ (FC and BO) and $\int|q_*|^p/(C_p\eta^{p-1})=1$ to 13 digits | claude-interactive.9 (claude) | `2026-10-18-claude-interactive.9-zs-solver-validation` | 2026-10-18 |
| Symbolic residual | Closed-form evaluation only: (C) equals $N-\tfrac12$ to $4.4\times10^{-16}$ for $N=1$–8; the (D) and (E) values quoted in the source are reproduced to all quoted digits; held-out values frozen. No ZS eigenvalue was computed | claude-interactive (claude) | 2026-10-18-claude-interactive-zs-moment-bound-check | 2026-10-18 |
| Symbolic residual (verifier) | Independent proof of (A)–(C) and rederivation of the (E)/(F) Hausdorff–Young constants (audit report, Part 1); $p=2N$ cancellation $U_{2N}=N-\tfrac12$; closed forms (C)–(E) recomputed with independent code including direct quadrature (agreement $\le10^{-12}$); (F) equals (E) at equal $p$ for Gaussians to $5\times10^{-12}$ | claude-interactive.9 (claude) | `2026-10-18-claude-interactive.9-zs-solver-validation` | 2026-10-18 |
| Simulation, core regime | Independent ZS solver (Fourier collocation and Boffetta–Osborne). TL sech $N=1$–6, 8: $\eta_{\max}=N-\tfrac12$ to $5\times10^{-14}$ (FC), $2\times10^{-13}$ (BO). (A) on 69 BO-confirmed eigenvalues of 60 random complex multi-lobe chirped potentials: $\min\int|q|^p/(C_p\eta^{p-1})=1.022$ over $p\in[1.2,12]$. **(C), adversarial:** 13 L-BFGS-B searches per case (phase-only and amplitude-and-phase Chebyshev, per-bin amplitude and phase, sharp multi-step masks; asymmetric allowed; exact discrete gradients), $N=2,3,4,6$: every best mask is TL; largest gain over TL $+4\times10^{-16}$; largest excess over $N-\tfrac12$ $2.3\times10^{-12}$, equal to the solver's own TL error on the same grid (FC–BO spread $\le2.3\times10^{-12}$) | claude-interactive.9 (claude) | `2026-10-18-claude-interactive.9-zs-solver-validation`, `2026-10-18-claude-interactive.9-mask-adversary` | 2026-10-18 |
| Held-out region | Frozen ceilings recomputed with independent code: (D) 0.07161% at $N=4.5$, 0.01518% at 7.5; (E) 95.46241%, 40.50316%, 26.41798% at $N=1.5$, 5, 8 (fractions) — all match. Adversarial masks, best gain over TL: $N=2.5$: best gain $-9\times10^{-16}$ against a ceiling of 0.43672%; $N=4.5$ (held out): best gain $-2\times10^{-16}$ against a ceiling of 0.07161%; $N=7.5$ (held out): best gain $-6\times10^{-11}$ against a ceiling of 0.01518%. Gaussian: $N=1.5$ (marked held out, but in the README table): $-7\times10^{-16}$ against 0.28343%; $N=4$: $-2\times10^{-16}$ against 0.01498%; $N=5$ (held out): $-8\times10^{-15}$ against 0.00745%; $N=8$ (held out): $-1\times10^{-16}$ against 0.00172%. No mask beats TL in any of these cases | claude-interactive.9 (claude) | `2026-10-18-claude-interactive.9-zs-solver-validation`, `2026-10-18-claude-interactive.9-mask-adversary` | 2026-10-18 |
| Convergence and artefacts | BO measured order 2.000 (three cell widths), Romberg to $\le2.4\times10^{-13}$ on TL sech; FC at two grids; Gaussian TL FC–BO $\le6\times10^{-14}$; the source's TL fractions reproduced to $\le10^{-10}$ (0.491250757965 at $N=4$). Every optimised mask re-evaluated on a 2x finer time grid, on the line by BO-Romberg, and (smooth masks) on a 2x window: spreads $\le2.3\times10^{-12}$ (sech), $\le8\times10^{-12}$ (Gaussian); window-edge energy fraction $\le3\times10^{-10}$ | claude-interactive.9 (claude) | `2026-10-18-claude-interactive.9-zs-solver-validation`, `2026-10-18-claude-interactive.9-mask-adversary` | 2026-10-18 |
| Second solver or relaxed assumption | Two independent discretisations agree (FC and BO, above). **Relaxed (Raman GNLSE, agents' solver b9fa957):** TL $N=2$ sech at 1550 nm, $\beta_2$ only, Agarwal response, self-steepening on; whole-field ZS eigenvalue against the integrable ceiling $N-\tfrac12=1.5$. $T_0=65$ fs: max over $z\le8L_D$ of the leading eigenvalue 1.6554 (+10.4%), control without Raman 1.5025 (+0.16%); $T_0=200$ fs: max over $z\le8L_D$ of the leading eigenvalue 1.5608 (+4.1%), control without Raman 1.5003 (+0.02%). Raman transfer after launch lifts the leading soliton above the passive-mask ceiling, so the bound holds for the input scattering data only (card assumption 1) | claude-interactive.9 (claude) | `2026-10-18-claude-interactive.9-zs-solver-validation`, `2026-10-18-claude-interactive.9-raman-escape` | 2026-10-18 |
| Adversarial audit | **Pass.** Independent proof of (A)–(C) written before reading the derivation note (commit 830c8d6); line-by-line check of the note: no gap in substance (state $q\in L^1$ and the absolute continuity of $\theta$). Prediction 5 reproduced: asymmetric source, TL $\eta=0.2142789$, hierarchy minimised at $n=1$ for $n\le20$; passive masks raise $\eta_{\max}$ by up to $+2.78\%$ (explicit cubic phase $+1.12\%$). Report: `notes/audit-2026-10-18-claude-interactive.9-C-20261018-pi-chatgpt-01.md` | claude-interactive.9 (claude) | `2026-10-18-claude-interactive.9-zs-solver-validation`, `2026-10-18-claude-interactive.9-mask-adversary`, `2026-10-18-claude-interactive.9-asym-counterexample` | 2026-10-18 |
| Novelty search | **(A) partly published.** The sharp $C_p$ and the sech extremizer are published for real $q\ge0$ with purely imaginary eigenvalues, as a Keller estimate for the 1D Dirac operator $D_\eta-q$ at energy 0: Dolbeault–Gontier–Pizzichillo–Van Den Bosch, Rev. Mat. Iberoam. 40 (2024) 649, DOI 10.4171/RMI/1443, Thm 1.3 at $\lambda=0$ (full text). The map is $(\phi,\chi)=(v_1-v_2,-(v_1+v_2))$, which neither source states. The same form with a weaker constant, for complex potentials, is in Cuenin–Laptev–Tretter 2014, Cor. 4.6 (full text). The sharp complex/off-axis case and the angle-weighting proof were not found. **(B)–(F) not found**; their ingredients (even-moment majorant, Satsuma–Yajima, sharp Hausdorff–Young) are published. Report: [`docs/review-2026-10-18-claude-interactive.10-zs-eigenvalue-bound-novelty.md`](../docs/review-2026-10-18-claude-interactive.10-zs-eigenvalue-bound-novelty.md) | claude-interactive.10 (claude) | 2026-10-18-claude-interactive.10-zs-novelty-constants; 2026-10-18-claude-interactive.10-zs-modulus-comparison | 2026-10-18 |
| Formal verification (Lean) | **(A) at even exponents, (B), (C) and (D) are kernel-checked theorems** in [`formal/ZSFormalization/`](../formal/ZSFormalization/) (formalizer: the PI's Codex session, family gpt, model GPT 6 Astra Max per the PI). Restrictions: exponents $p=2n$ only; masks with a Schwartz output spectrum $mS$ and Schwartz $S\ge0$. (C) is proved as an attained maximum for every integer $N$; (D) as an enclosure with exact rational certificates. Not formalized: (A) at real $p$, rough masks, (E), (F). Cross-family formal audit: rebuilt from the committed pins (9,037 jobs, no warnings), all 121 theorems use only the three standard axioms, leanchecker and nanoda (54,113 declarations) pass, held-out certificates $N=9/2$ (0.07161%), $15/2$ (0.01518%) and $N=7$ ($13/49$) pass, a negative control fails as required. Even exponents give a Gaussian ceiling of 0.045% at $N=4$ (numerical, not Lean). Report: [`results/formalized/R-0001-zs-even-moment-passive-mask-ceiling/audit/formal-audit-2026-10-18-claude-interactive.md`](../results/formalized/R-0001-zs-even-moment-passive-mask-ceiling/audit/formal-audit-2026-10-18-claude-interactive.md) | claude-interactive (claude) | `2026-10-18-claude-interactive-zs-lean-audit` | 2026-10-18 |

## Outcome

**Verified (PI instruction, 2026-10-18): audited by claude-interactive.9 (claude), with the Claude-family novelty audit by claude-interactive.10 complete.** The PI instructed that the claim move to verified once both were complete; its status is `audited`, the strongest status before promotion. Verdict **pass** for (A)–(F) as stated, in the stated regime. Audit report: [`notes/audit-2026-10-18-claude-interactive.9-C-20261018-pi-chatgpt-01.md`](notes/audit-2026-10-18-claude-interactive.9-C-20261018-pi-chatgpt-01.md).
- (A) was proved independently (the same angle argument, written before the derivation note was read); the note's proof has no gap in substance. Equality at $q_*$ and the limits $p=2$, $p\to1$, $p\to\infty$ check.
- (B)–(F) follow from (A) and the Fourier majorant / sharp Hausdorff–Young inequalities; the constants were rederived.
- (C) is exact. Adversarial searches over phase-only, amplitude-and-phase, per-bin and sharp multi-step masks found nothing above $N-\tfrac12$ beyond solver error at $N=2,3,4,6$.
- (D), (E): the frozen and held-out ceilings are reproduced. In every non-integer-sech and Gaussian case tested, no mask beats TL at all (gains $\le10^{-14}$), so these ceilings are valid but are not approached by any mask found.
- Prediction 5 is reproduced, more strongly than stated: passive masks raise $\eta_{\max}$ of the asymmetric source by up to 2.8% (an explicit cubic phase gives 1.1%), while the hierarchy gives only $f_1\le1$. C-20261016-claude-a-01 is refuted.
- Scope: the statements bound the input scattering data of the integrable NLSE. With Raman the propagated leading soliton can exceed the ceiling: for a TL $N=2$ sech in the agents' solver the leading eigenvalue reaches 1.655 (+10.4%) at $T_0=65$ fs and 1.561 (+4.1%) at 200 fs, against $\le0.16\%$ without Raman (run `2026-10-18-claude-interactive.9-raman-escape`), as card assumption 1 says.
- Bookkeeping: the Gaussian $N=1.5$ values marked held-out (‡) appear in the README's table, so they were not held out; the other held-out values (sech $N=4.5$, 7.5; Gaussian $N=5$, 8) were.
- **Novelty audit (T-20261018-claude-interactive-03): complete.** (A) is partly published. The sharp constant and the sech extremizer are already known for real nonnegative potentials with purely imaginary eigenvalues, in Dirac-operator form (DGPV 2024). A non-sharp form for complex potentials is in Cuenin–Laptev–Tretter 2014. (B)–(F) were not found. See the Novelty search row.
- **Wording:** prior art is now credited in the Statement under (A), which closes task T-20261018-claude-interactive.10-03.

**Promoted (PI instruction, 2026-10-18), as two results.**
- [R-0001](../results/formalized/R-0001-zs-even-moment-passive-mask-ceiling/RESULT.md) (formalized): (A) at even exponents, and (B)–(D) for Schwartz masks, as kernel-checked Lean theorems.
- [R-0002](../results/promising/R-0002-zs-real-exponent-and-gaussian-ceilings/RESULT.md) (promising): (A) at real exponents, (B)–(D) for arbitrary masks, (E) and (F), which are verified but not formalized.
- Both leave gate G6 open, because only one family has searched the literature (task T-20261018-claude-interactive-05).

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-18 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Filed from the PI's GPT 6 Pro session (proposer family gpt) with status cheap-checks-passed; closed-form values checked | Shared chat (full text of the final answer read); PI-supplied README; run `2026-10-18-claude-interactive-zs-moment-bound-check` |
| 2026-10-18 | claude-interactive.9 (claude; claude-opus-5-5) | Cross-family verification and adversarial audit (task T-20261018-claude-interactive-02): status cheap-checks-passed → audited; verified_by and audited_by set; Checks rows filled (Novelty search left to T-20261018-claude-interactive-03); assumption 6 added; statement and regime unchanged | Runs `2026-10-18-claude-interactive.9-zs-solver-validation`, `2026-10-18-claude-interactive.9-mask-adversary`, `2026-10-18-claude-interactive.9-asym-counterexample`, `2026-10-18-claude-interactive.9-raman-escape`; audit report `notes/audit-2026-10-18-claude-interactive.9-C-20261018-pi-chatgpt-01.md` |
| 2026-10-18 | claude-interactive.10 (claude; claude-opus-5-5) | Claude-family novelty search (task T-20261018-claude-interactive-03). (A) partly published: DGPV 2024 has the sharp constant and extremizer for real $q\ge0$ and imaginary eigenvalues; CLT 2014 has a non-sharp complex form. (B)–(F) not found. Status unchanged. Wording changes requested in T-20261018-claude-interactive.10-03 | [novelty report](../docs/review-2026-10-18-claude-interactive.10-zs-eigenvalue-bound-novelty.md); runs `2026-10-18-claude-interactive.10-zs-novelty-constants`, `2026-10-18-claude-interactive.10-zs-modulus-comparison` |
| 2026-10-18 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Merged the verification (PR #65) and novelty (PR #64) records and resolved their conflict on this card. Added the prior-art credit under (A). With both checks complete, the claim stands as verified per the PI (status audited) | PRs #64, #65 |
| 2026-10-18 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Filed the Lean formalization (formal/ZSFormalization, from the PI's Codex session) and its cross-family audit; added the Formal verification row; status audited → promoted, result [R-0001, R-0002] (formalized and promising tiers) | Run `2026-10-18-claude-interactive-zs-lean-audit`; task T-20261018-claude-interactive-04 |
