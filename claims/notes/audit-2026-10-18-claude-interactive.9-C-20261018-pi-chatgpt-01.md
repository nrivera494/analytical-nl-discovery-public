---
agent: claude-interactive.9
model: claude-opus-5-5
family: claude
claim: C-20261018-pi-chatgpt-01
task: T-20261018-claude-interactive-02
date: 2026-10-18
status: complete
verdict: pass
---

# Cross-family verification of C-20261018-pi-chatgpt-01 (passive-mask ZS eigenvalue ceiling)

**Status of this file.** Part 1 (independent proof) and Part 2 (independent numerics) were written before the proposer's derivation note `claims/notes/C-20261018-pi-chatgpt-01-derivation.md` was opened. Inputs read up to that commit: the claim card, the problem card P-20261016-claude-interactive-03, the orchestrator's run `2026-10-18-claude-interactive-zs-moment-bound-check`, AGENTS.md and the docs. Not read: the derivation note, the filer's log entry, claude-a's explorations and logs.

## Verdict

**Pass.** (A)–(F) hold as stated, in the stated regime, for the input scattering data of the integrable NLSE. No blocker.

- **Proof.** I proved (A)–(C) independently (Part 1) before reading the note. The note's proof is the same argument and is correct line by line (Part 3). Two clarifications, not gaps: take "sufficient regularity" as $q\in L^1(\mathbb R)$, and state that $\theta$ is absolutely continuous where the antiderivative is used. The (E)/(F) Hausdorff–Young constants and the physical-unit form were rederived.
- **Sharpness.** $q_*$ has its leading bound state at $\zeta=i\eta$ with equality in (A), for $p=1.5,2,3,7$ (13 digits; I also checked the note's explicit spinor by substitution).
- **(C) adversarial.** 13 searches each for $N=2,3,4,6$ over phase-only, amplitude-and-phase, per-bin (up to 274 parameters) and sharp multi-step masks found nothing above $N-\frac12$. The largest excess is $2.3\times10^{-12}$, equal to the solver's own TL error on the same grid; the largest gain over TL is $4\times10^{-16}$.
- **Held-out.** The (D)/(E) ceilings at sech $N=4.5$, 7.5 and Gaussian $N=5$, 8 are reproduced with my own code, and the best masks stay below them. In every non-integer and Gaussian case no mask beats TL at all (largest gain $-6\times10^{-11}$ to $-1\times10^{-16}$), so the ceilings hold with room to spare.
- **Prediction 5.** Reproduced, and stronger than stated (+2.8% rather than about 1%). C-20261016-claude-a-01 is refuted.
- **Relaxed assumption.** With Raman, the propagated leading eigenvalue exceeds the ceiling by up to 10% (Part 4). That is consistent with card assumption 1; it is not a failure of the claim.

**Regime I sign off on.**
- (A): every $p>1$, every discrete eigenvalue, every $q\in L^1(\mathbb R)$ (complex, any shape).
- (B): every integer $n\ge1$, any $S\ge0$ with $q_0\in L^{2n}$, any $|m|\le1$.
- (C): every integer $N\ge1$.
- (D): every real $N>\frac12$.
- (E): Gaussian sources, real $p\ge2$.
- (F): any $S\ge0$, real $p\ge2$.
- All of these concern the input scattering data, i.e. the integrable NLSE. Numerically tested: $N\in[1.5,8]$ for the ceilings and $p\in[1.2,12]$ for (A).

**Non-blocking concerns.**
1. The Gaussian $N=1.5$ values marked held-out on the card are in the source README's table.
2. The (D)/(E) ceilings are not approached by any mask found. Whether TL is exactly optimal for non-integer sech and Gaussian lasers is open; the claim does not assert it.
3. I did not assess novelty, which is protocol step 7. It is task T-20261018-claude-interactive-03.
4. The asymmetric-source supremum is not converged with respect to the mask class: my best is +2.78%.
5. The card's "about 1%" for prediction 5 understates what passive masks achieve. An explicit cubic phase alone gives +1.1%.

## Part 1. Independent proof of (A), (B), (C)

Notation: $v'=\begin{pmatrix}-i\zeta&q\\-\bar q&i\zeta\end{pmatrix}v$, $\zeta=\xi+i\eta$, $\eta>0$, $q\in L^1(\mathbb R)$ (so the Jost solutions and the bound-state asymptotics below exist). Write $X=\mathrm{Re}(q\,\bar v_1v_2)$.

**Step 1 (component moduli).** From the system,
$(|v_1|^2)'=2\eta|v_1|^2+2X$ and $(|v_2|^2)'=-2\eta|v_2|^2-2X$. The real part $\xi$ drops out.

**Step 2 (angle).** Define $\theta=\arctan(|v_2|/|v_1|)\in[0,\pi/2]$, $R^2=|v_1|^2+|v_2|^2>0$ ($v$ never vanishes). $\theta$ is absolutely continuous (composition of a smooth function on $\mathbb R^2\setminus0$ with AC functions). Where $v_1v_2\neq0$,
$$\theta'=-\eta\sin2\theta-\frac{X}{R^2\sin\theta\cos\theta}\le|q|-\eta\sin2\theta ,$$
because $|X|\le|q||v_1||v_2|=|q|R^2\sin\theta\cos\theta$. With $q=0$ the flow $\theta'=-\eta\sin2\theta$ pushes $\theta$ to $0$; the potential must carry $\theta$ from $0$ to $\pi/2$ against it.

**Step 3 (boundary values).** The bound state is the Jost solution $v\sim(1,0)e^{-i\zeta t}$ as $t\to-\infty$ and $v\sim b\,(0,1)e^{i\zeta t}$ as $t\to+\infty$, so $\theta(-\infty)=0$ and $\theta(+\infty)=\pi/2$.

**Step 4 (pointwise Young inequality).** Let $K_p=p^p/(p-1)^{p-1}$, $p>1$. For $s\ge0$ and every real $u$, $(u+s)_+^p\ge K_p\,s^{p-1}u$. (For $u\le0$ the right side is $\le0$. For $u>0$, $(u+s)^p/u$ is minimised at $u=s/(p-1)$ with value $K_ps^{p-1}$.) With $u=\theta'$, $s=\eta\sin2\theta$ and Step 2, a.e. on $\{v_1v_2\ne0\}$:
$$|q|^p\ge(\theta'+\eta\sin2\theta)_+^p\ge K_p\,\eta^{p-1}\sin^{p-1}(2\theta)\,\theta' .$$
On $\{v_1v_2=0\}$ the right side is $0$ (there $\sin2\theta=0$ and $p>1$), so the inequality holds a.e. on $\mathbb R$; no separate argument is needed at component zeros, including intervals where $q\equiv0$ and $v_2\equiv0$.

**Step 5 (antiderivative).** $F(\theta)=\int_0^\theta\sin^{p-1}2\phi\,d\phi$ is $C^1$ with bounded derivative, so $F\circ\theta$ is AC and $(F\circ\theta)'=\sin^{p-1}(2\theta)\theta'$ a.e. Integrating over $[-L,L]$ and letting $L\to\infty$:
$$\int|q|^p\,dt\ge K_p\eta^{p-1}\big[F(\pi/2)-F(0)\big]=K_p\eta^{p-1}\tfrac12\int_0^\pi\sin^{p-1}\phi\,d\phi=K_p\frac{J_p}{2}\eta^{p-1}=C_p\eta^{p-1},$$
using $\sin\phi=\mathrm{sech}\,t$, $d\phi=\mathrm{sech}\,t\,dt$, so $\int_0^\pi\sin^{p-1}\phi\,d\phi=J_p$. This is (A), with the card's constant, for every eigenvalue and every $p>1$, and for complex $q$ with any $\xi$.

**Equality.** Equality needs (i) $q\bar v_1v_2\le0$ (phase alignment) and (ii) $\theta'=\eta\sin2\theta/(p-1)$, i.e. $\tan\theta=e^{2\eta(t-t_0)/(p-1)}$, $\sin2\theta=\mathrm{sech}(2\eta(t-t_0)/(p-1))$, hence $|q|=\theta'+\eta\sin2\theta=\frac{p\eta}{p-1}\mathrm{sech}\frac{2\eta(t-t_0)}{p-1}=|q_*|$. Conversely $q_*(t)=w^{-1}\,(p/2)\,\mathrm{sech}(t/w)$ with $w=(p-1)/(2\eta)$, so by Satsuma–Yajima scaling its leading eigenvalue is $i(p-1)/(2w)=i\eta$, and $\int|q_*|^p=(p\eta/(p-1))^p\,w\,J_p=C_p\eta^{p-1}$. Equality is attained (checked numerically in run `2026-10-18-claude-interactive.9-zs-solver-validation`).

**Limits.** $p=2$: $C_2=4$, $\int|q|^2\ge4\eta$ (single-eigenvalue form of the trace identity). $p\to1$: $C_p\to J_1/2=\pi/2$, the area condition $\|q\|_1\ge\pi/2$ (the proof at $p=1$ gives $\int|q|\ge\int\theta'=\pi/2$ directly). $p\to\infty$: $C_p^{1/(p-1)}\to1$, so $\eta\le\|q\|_\infty$.

**(B).** For integer $n\ge1$, $\int|q|^{2n}=\|q^n\|_2^2$ and $\widehat{q^n}$ is a constant times the $n$-fold convolution $\hat q*\dots*\hat q$. If $|\hat q_m|=|m|S\le S$ with $S\ge0$, then $|\hat q_m^{*n}|\le S^{*n}=\hat q_0^{*n}$ pointwise, and Plancherel gives $\int|q_m|^{2n}\le\int|q_0|^{2n}$. With (A) at $p=2n$: $\eta\le[\int|q_0|^{2n}/C_{2n}]^{1/(2n-1)}=U_{2n}$. The same majorant argument holds for the DFT (cyclic convolution), which is what the numerics below discretise. Needs: $S\ge0$ (the TL pulse is the one with real non-negative spectrum), $|m|\le1$, $q_0\in L^{2n}$.

**(C).** For $q_0=N\mathrm{sech}\,t$ and $p=2N$: $N^{2N}J_{2N}/C_{2N}=2N^{2N}(2N-1)^{2N-1}/(2N)^{2N}=((2N-1)/2)^{2N-1}$, so $U_{2N}=N-\tfrac12$, which the TL pulse attains (Satsuma–Yajima). Equivalently, $N\mathrm{sech}\,t$ is exactly the $p=2N$ extremiser $q_*$ with $\eta=N-\tfrac12$. Hence $\sup_{|m|\le1}\eta_{\max}=N-\tfrac12$ for integer $N$, attained at $m=1$ (and any linear phase); $f_{1,\rm opt}=4(N-\tfrac12)/(2N^2)=(2N-1)/N^2$. Physical units: $E=\frac{|\beta_2|}{\gamma T_0}\int|q|^2dt$, so $E_{1,\max}=4(N-\tfrac12)|\beta_2|/(\gamma T_0)=2(2N-1)|\beta_2|/(\gamma T_0)$, as on the card.

**Assumptions I would add to the card's list.** (a) $q\in L^1$ (and $q_0\in L^{2n}$); this is the "sufficient regularity". (b) The statement concerns the input scattering data; the identification "energy $4\eta$ after fission" needs the integrable NLSE (card assumption 1). (c) In (B) the mask acts on the same field whose spectrum is $S$; "TL" means zero (or linear) spectral phase of that field.

**My check of (E) and (F) constants.** With $q=\frac1{2\pi}\int Se^{ikt}dk$ and $g(\nu)=S(2\pi\nu)$, $q=\check g$ in the unitary convention; Beckner's $\|\check g\|_p\le(p'^{1/p'}/p^{1/p})^{1/2}\|g\|_{p'}$ and $\|g\|_{p'}^{p'}=\frac1{2\pi}\int S^{p'}dk$ give $\|q\|_p^p\le B_p^p(2\pi)^{1-p}(\int S^{p'})^{p-1}$ with $(B_p^p)^{1/(p-1)}=\sqrt{p'}\,p^{-1/(2(p-1))}$. Combined with (A) this is exactly (F). For (E), a real Gaussian $S$ is an extremiser of Hausdorff–Young (Beckner; Lieb), so $\|q_m\|_p\le A_p\|mS\|_{p'}\le A_p\|S\|_{p'}=\|q_0\|_p$ for every real $p\ge2$, which gives the card's (E) formula with $\int|q_0|^p=N^p\sqrt{2\pi/p}$ and $M_0=N^2\sqrt\pi$. Checks: (F) at $p=2$ is $\eta\le\frac1{8\pi}\int S^2=\frac14\int|q|^2$; $p\to\infty$ gives $\eta\le\frac1{2\pi}\int S=\|q_0\|_\infty$; for the Gaussian, (F) and (E) agree at the same $p$ to $5\times10^{-12}$ (run `2026-10-18-claude-interactive.9-zs-solver-validation`).

## Part 2. Independent numerics (state at the independent-attempt commit)

**Solver** (run `2026-10-18-claude-interactive.9-zs-solver-validation`). Two discretisations written for this audit: Fourier collocation (FC, dense eigensolver, exact discrete eigenvalue gradient through the left eigenvector $w=(v_2,v_1)$) and Boffetta–Osborne (BO) transfer matrices on the line with Romberg extrapolation; BO's measured order is 2.000 for every case. TL sech, $N\in\{1,\dots,6,8,2.5,3.5,4.5,5.5,7.5,9.5\}$: leading $\eta=N-\tfrac12$ to $\le2.4\times10^{-13}$ (FC and BO). TL Gaussians: FC and BO agree to $\le6\times10^{-14}$; $f_1^{TL}(N=4)=0.491250757965$ (source 0.4912507580). Extremiser $q_*$ for $p=1.5,2,3,7$ ($\eta=1$, 2.3): leading eigenvalue $i\eta$ and $\int|q_*|^p/(C_p\eta^{p-1})=1$ to 13 digits. 69 BO-confirmed eigenvalues of 60 random complex multi-lobe chirped potentials: $\min\int|q|^p/(C_p\eta^{p-1})\ge1.022$ over $p\in\{1.2,\dots,12\}$. Limits: $C_2=4$, $C_{1.0001}=1.57229\to\pi/2$, $C_{10^5}^{1/(p-1)}=1.00007\to1$. Ceilings recomputed with my own code: (D) 0.43672, 0.15446, **0.07161**, 0.03888, **0.01518**, 0.00743 %; (E) **95.46241**, 82.65046, 62.12206, 49.13244, **40.50316**, 34.41023, **26.41798**, 21.42475 % (held-out in bold; all agree with the card). (F): equals (E) at the same $p$ for the Gaussian to $5\times10^{-12}$; bounds the sech $N=3$ TL value at every $p$ tested.

**Adversarial masks, Gaussian lasers** (run `2026-10-18-claude-interactive.9-mask-adversary`, 13 L-BFGS-B searches per case over phase-only Chebyshev, amplitude-and-phase Chebyshev, per-bin amplitude-and-phase, and sharp logistic-step masks; best of each family re-evaluated with refined FC and BO-Romberg on the line). Best verified gain over TL: $N=1.5$: $-7\times10^{-16}$ (ceiling allows $2.8\times10^{-3}$); $N=4$: $-2\times10^{-16}$ ($1.5\times10^{-4}$); $N=5$: $-8\times10^{-15}$ ($7.4\times10^{-5}$); $N=8$: $-1\times10^{-16}$ ($1.7\times10^{-5}$). No mask exceeds TL, so none approaches the ceilings.

**Adversarial masks, sech lasers** (same run, completed after the independent-attempt commit; the method was fixed before the note was read). Integer $N=2,3,4,6$ (prediction 1): every best mask is TL; best verified $\eta-(N-\frac12)=1.8\times10^{-13}$, $8.4\times10^{-13}$, $2.3\times10^{-12}$, $1.6\times10^{-12}$, each equal to the TL value's own FC–BO spread on that grid ($\le2.3\times10^{-12}$); gains over TL $\le4\times10^{-16}$. Non-integer $N=2.5$, 4.5 (held out), 7.5 (held out): best gains over TL $-9\times10^{-16}$, $-2\times10^{-16}$, $-6\times10^{-11}$, against ceilings of 0.43672%, 0.07161%, 0.01518%. Across all 143 searches, 7–12 of the 13 starts per case returned to TL within a relative $10^{-6}$; the rest stopped in lower local maxima. The largest window-edge energy fraction of any verified mask is $3\times10^{-10}$.

**Counterexample to C-20261016-claude-a-01** (run `2026-10-18-claude-interactive.9-asym-counterexample`). $S=\pi\cos(1)e^k\mathrm{sech}(\pi k/2)$; with $q=\frac1{2\pi}\int Se^{ikt}dk$ the TL pulse is exactly $\cos(1)\,\mathrm{sech}(t-i)$ (FFT check $7\times10^{-15}$; the other sign convention gives its complex conjugate, which has the same $\eta$), $M_0=2\cot1$, $|q_0|_{\max}=1$. TL has a single bound state $\zeta=-0.3839594+0.2142789i$, $f_1^{TL}=0.66744$. The hierarchy (B) is minimised at $n=1$ for $n\le20$ ($f_1\le1$; $n=2$ gives 1.557), and (F) is also minimised at $p=2$: **the source's statement is reproduced**. Passive masks raise $\eta_{\max}$ (line BO-Romberg, confirmed by FC to $\le9\times10^{-7}$, one bound state each): phase-only Chebyshev $+2.646\%$; amplitude-and-phase $+2.643\%$; sharp steps $+2.725\%$; per-bin $+2.777\%$ (throughput 0.9998, $\eta=0.2202282$, $f_1=0.68597$). An explicit phase-only mask $m=\exp[-0.5i(k-1)^3/6]$ gives $\eta=0.2166695$, **$+1.116\%$** (FC: 0.2166694638 at two grids). **The counterexample is reproduced**; the largest gain found is about 2.8%, not 1%. Added after the main report: on C-20261016-claude-a-01's own mildly asymmetric held-out spectrum $\mathrm{sech}(\pi k/2)(1+\frac12\tanh k)$ ($A=2$, 4) the same optimiser finds no gain over TL (largest $+7\times10^{-16}$, script `mild_asym.py`), so the failure of TL optimality needs strong asymmetry.

## Part 3. Line-by-line check of the derivation note (read after commit 830c8d6)

The note's proof of (A) is the same argument as my Part 1, in a slightly different order.

| Step in the note | Check | Finding |
|---|---|---|
| §1 convention $Q=\int qe^{-ikt}dt$ | same as mine, $q=\frac1{2\pi}\int Qe^{ikt}dk$ | consistent; it is the convention the (F) constant needs |
| §2 $a'=\eta a+\mathrm{Re}(qv_2\bar v_1)/a$, $b'=-\eta b-\mathrm{Re}(qv_2\bar v_1)/b$ | rederived from $(|v_j|^2)'$ | correct, signs included |
| §2 $\theta'=\nu-\eta\sin2\theta$, $\nu=-\mathrm{Re}(qv_2\bar v_1)/(ab)\le|q|$ | $\theta'=(ab'-ba')/(a^2+b^2)$ | correct; identical to my Step 2 |
| §2 $r^p\ge K_ps^{p-1}(r-s)$, $r,s\ge0$ | minimum of $x^p-K_p(x-1)$ at $x=p/(p-1)$ is $0$ | correct; equivalent to my Step 4 ($r-s\ge\theta'$, coefficient $\ge0$) |
| §2 a.e. argument at component zeros | weight $\sin^{p-1}2\theta$ vanishes where $ab=0$ | correct. Two points are left implicit: $\theta$ must be absolutely continuous (it is: $v$ is AC and never zero, atan2 is smooth off the origin), and on a positive-measure zero set (possible where $q\equiv0$ on an interval) $\theta$ is constant so $\theta'=0$ a.e. Not a gap in substance |
| §2 antiderivative, "even if $\theta$ turns around" | FTC for $F\circ\theta$, $F\in C^1$ | correct; this is why no monotonicity is needed |
| §2 boundary values $\theta(\mp\infty)=0,\pi/2$ | Jost asymptotics | correct for $q\in L^1$; the note says "usual decaying-potential setting". I would state $q\in L^1(\mathbb R)$ explicitly |
| §2 sharpness spinor $v=R(\cos\theta,-\sin\theta)$, $\tan\theta=e^{b_*(t-t_0)}$, $R=\mathrm{sech}^{(p-1)/2}$ | substituted into both ZS equations at $\zeta=i\eta$, $q=q_*$ | correct: constant terms $\mp\eta/(p-1)$ and $\tanh$ terms $-p\eta/(p-1)$ match; decays as $e^{-\eta|t|}$-type at both ends; phase alignment $q\bar v_1v_2\le0$ holds. By Satsuma–Yajima this is the **leading** eigenvalue of $q_*$; the note does not say so, but (C) needs it only for $p=2N$, where it is standard |
| §2 limits $p=2$, $p\to\infty$, $p\to1$ | closed forms and numerics | correct ($C_2=4$; $C_p^{1/(p-1)}\to1$; $C_p\to\pi/2$) |
| §3 even-moment majorant | Plancherel + pointwise convolution majorant | correct; needs $S\ge0$ and $|m|\le1$; normalisation constants cancel as stated |
| §3 "real-$p$ extension false in general" | numerical counterexample (script `majorant_realp.py`, run `2026-10-18-claude-interactive.9-zs-solver-validation`, added after the main report) | confirmed: for $S$ = three Gaussian bumps at $k=0,1,3$ and a phase-only mask, $\|q_m\|_3/\|q_0\|_3=1.0101$ and $\|q_m\|_{2.5}/\|q_0\|_{2.5}=1.0094$, while $p=2,4,6$ give $1$, $\le1$, $0.970$. Not used by any claimed bound |
| §4 $p=2N$ cancellation, $U_{2N}=N-\frac12$ | $N^{2N}J_{2N}/C_{2N}=((2N-1)/2)^{2N-1}$ | correct; $J_p$ cancels; $N\mathrm{sech}\,t$ is exactly $q_*$ at $p=2N$, $\eta=N-\frac12$ |
| §4 $N=4$: $7/16$ against the peak ceiling $1/2$ | arithmetic | correct |
| §4 non-integer $U_{2n}$ closed form | from the definition | correct |
| §4 $\log\frac{U_{2n}(N)}{N-1/2}=\int_n^N\frac{x-n}{(2n-1)x(x-1/2)}dx$ | differentiate $\log U_{2n}(x)-\log(x-\frac12)$ in $x$; zero at $x=n$ | correct; it gives headroom $\approx(N-n)^2/(4n^3)$, i.e. $O(N^{-3})$ at half-integers. My closed-form values give a fitted exponent of $-3.03$ between $N=4.5$ and $9.5$ |
| §5 Hausdorff–Young chain, constant $(2\pi)^{-1/p'}(p'^{1/p'}/p^{1/p})^{1/2}$ | rederived from Beckner with $g(\nu)=S(2\pi\nu)$ | correct; equality for every real Gaussian $S$ (Beckner; Lieb), hence $\|q_m\|_p\le\|q_0\|_p$ for all real $p\ge2$ |
| §5 Gaussian table (TL fractions, ceilings) | my FC and BO, two grids each | all TL fractions agree to $\le10^{-10}$; all ceilings agree to the digits shown |
| §5 (F) constant $\frac{\sqrt{p'}}{2\pi}(\frac1{\sqrt pC_p})^{1/(p-1)}$ | rederived | correct; checked against (E) at equal $p$ to $5\times10^{-12}$ |
| §6 physical units, $D^{n-1}$, $D^{p/2-1}$ for Gaussians | rescaling $q=T_0A/\sqrt D$, $E=\frac D{T_0}\int|q|^2$ | correct; $T_0$ cancels; $E_{1,\max}=2(2N-1)D/T_0$ |
| §7 hierarchy trivial for the asymmetric source, $n\le20$ | quadrature | reproduced: minimum at $n=1$; $n=2$ already gives $f_1\le1.557$ |

**Gaps.** None that affect the statements. Two clarifications for the card's assumption list: (1) "sufficient regularity" can be taken as $q\in L^1(\mathbb R)$ (Jost asymptotics), with the inequality trivially true when $\int|q|^p=\infty$; (2) absolute continuity of $\theta$ should be stated where the FTC is used.

**Bookkeeping issue on the card (non-blocking).** The Gaussian $N=1.5$ values marked held-out (‡, "new") on the card appear in the README's table (TL 0.9519259914, ceiling 0.9546240545). They were therefore not held out. The other held-out values (sech $N=4.5$, 7.5; Gaussian $N=5$, 8) do not appear in the README.

## Part 4. Relaxed assumption: Raman (run `2026-10-18-claude-interactive.9-raman-escape`)

The claim bounds input scattering data, and card assumption 1 says Raman breaks the link to the final soliton energy. Check: a TL $N=2$ sech at 1550 nm ($\beta_2=-21.7$ ps²/km only, $\gamma=1.32$ /W/km) propagated over $8L_D$ in the agents' solver (b9fa957, RK4IP, 8000 steps, 1 fs grid), with the Agarwal Raman response or with `NoRaman()`; self-steepening is on in both. I computed the leading ZS eigenvalue of the whole field at 17 planes in launch soliton units with my BO solver (Richardson over one and two samples per cell, carrier of the tallest pulse removed).
- $T_0=65$ fs: $\eta$ rises to 1.6554 at $z=L_D$ (+10.4% above the passive-mask ceiling 1.5), then decays to 1.5025 at $8L_D$ as the soliton red-shifts by $9.4/T_0$ and loses energy. Without Raman the maximum is 1.5025 (+0.16%, the shock perturbation).
- $T_0=200$ fs: $\eta$ reaches 1.5608 (+4.1%) and is 1.5475 at $8L_D$. Without Raman the maximum is 1.5003 (+0.02%).

So Raman transfer during fission lifts the leading soliton above the integrable passive-mask maximum. The bound does not extend to the Raman GNLSE, as the card says.

