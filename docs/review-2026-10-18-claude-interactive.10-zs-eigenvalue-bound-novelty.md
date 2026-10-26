---
date: 2026-10-18
agent: claude-interactive.10
model: claude-opus-5-5
family: claude
task: T-20261018-claude-interactive-03
claim: C-20261018-pi-chatgpt-01
orchestrator: claude-interactive
base: "PR #63, task/T-20261018-claude-interactive-01"
run_ids: [2026-10-18-claude-interactive.10-zs-novelty-constants, 2026-10-18-claude-interactive.10-zs-modulus-comparison]
status: complete
---

# Novelty audit: the $L^p$ single-eigenvalue bound for Zakharov–Shabat and its passive-mask corollaries

This is the Claude-family novelty check of C-20261018-pi-chatgpt-01, a claim produced by GPT 6 Pro in the PI's ChatGPT session. The claim's derivation note was read, as the task allows for a literature audit. No proposer log or chat transcript was read. The verifier's task (T-20261018-claude-interactive-02) is separate. Nothing here checks the claim's proofs or numbers beyond the constant comparison described in Part (A).

## Summary

**Main finding.** The claimed sharp constant $C_p$ and the sech extremizer of (A) are already published for one special case: **real nonnegative potentials with purely imaginary eigenvalues**. They appear in Dirac-operator form in Dolbeault, Gontier, Pizzichillo and Van Den Bosch (DGPV), *Rev. Mat. Iberoam.* 40 (2024) 649–692, DOI 10.4171/RMI/1443, arXiv:2210.03091 (full text), Theorem 1.3 evaluated at $\lambda=0$.
- **How the two connect.** For real $q$ and $\zeta=i\eta$, the change of variables $(\phi,\chi)=(v_1-v_2,\,-(v_1+v_2))$ turns the ZS bound state into a zero-energy eigenfunction of the 1D massive Dirac operator $D_m-V$, with mass $m=\eta$ and electric potential $V=q$. That is the operator DGPV study.
- **Who states the connection.** Neither DGPV nor the claim does.
- **Run check.** At $\lambda=0$, DGPV's optimal potential is exactly the claim's $q_*$, and their optimal norm $\alpha_D(0,p)^p$ equals $C_p\eta^{p-1}$. Both agree to 40 digits for seven values of $p$ and two values of $\eta$ (run `2026-10-18-claude-interactive.10-zs-novelty-constants`).

**What was not found:** the sharp inequality for complex potentials and for eigenvalues off the imaginary axis, and the claim's weighted spinor-angle proof. Cuenin, Laptev and Tretter (2014) publish the same functional form for general complex (matrix) potentials, but with a weaker constant. The passive-mask corollaries (B)–(F) were not found. They need the complex case of (A), because masked pulses are complex.

**A possible shortcut, flagged for the verifier.** The complex case may follow from the published real case if $\eta(q)\le\eta_{\max}(\lvert q\rvert)$ for every eigenvalue. This held in all 55 test potentials of run `2026-10-18-claude-interactive.10-zs-modulus-comparison`. It is not proved here, and it was not found in the literature.

| Part | Verdict | Confidence | Closest prior work (access) | What is not covered by it |
|---|---|---|---|---|
| (A) $\int\lvert q\rvert^p\ge C_p\eta^{p-1}$, sech extremizers | **Partly published** | High that the real-nonnegative, imaginary-eigenvalue case is published with the same constant and extremizer. Medium that the complex/off-axis sharp case is unpublished. | DGPV 2024, Thm 1.3 at $\lambda=0$ with Cor. 1.2, DOI 10.4171/RMI/1443 (**full text**). Cuenin–Laptev–Tretter 2014, Cor. 4.6, DOI 10.1007/s00023-013-0259-3, arXiv:1207.6584 (**full text**): same form for complex potentials, constant weaker by $pJ_p2^{p-2}$ (4 at $p=2$). Endpoints: Klaus–Shaw 2003, $\lVert q\rVert_1\ge\pi/2$, DOI 10.1137/S0036141002403067 (**abstract only**); trace identity, Yousefi–Kschischang Part I, §IV-D (**full text**). | Complex $q$, eigenvalues off the imaginary axis, sign-changing real $q$. The claim's proof: the modulus-angle inequality weighted by $\sin^{p-1}2\theta$. |
| (B) Passive-mask ceiling $U_{2n}[S]$ | **Not found** (both ingredients published) | Medium | Even-moment majorant: Lenzmann–Sok, arXiv:1805.06294, Lemma 5.1 (**full text**), classical after Hardy–Littlewood. Peak and $L^4$ cases for passive masks: earlier repository review, `docs/review-2026-10-16-gpt-b-supercontinuum-literature.md`. | The combination with a sharp eigenvalue inequality. It needs the complex case of (A). |
| (C) Integer-$N$ sech: TL globally optimal, $f_{1,\rm opt}=(2N-1)/N^2$ | **Not found** | Medium | TL eigenvalue $N-\tfrac12$: Satsuma–Yajima 1974 (stated in Biondini–Oregero–Tovbis, **full text**). Repository conjecture C-20261016-claude-a-01 (numerical). Closest optimization: Lazaridis–Debarge–Gallion 1995, DOI 10.1364/OL.20.001680 (**abstract only**), which optimizes power and width of a chirped sech² launch, a different input class. | Global optimality over passive masks at fixed upstream spectrum. |
| (D) Non-integer sech headroom ceilings | **Not found** | Medium | Corollary of (B) with closed-form sech moments | — |
| (E) Gaussian lasers via sharp Hausdorff–Young | **Not found** (ingredient published) | Medium | Beckner 1975, DOI 10.2307/1970980 (**not accessed**); PNAS announcement DOI 10.1073/pnas.72.2.638 (**abstract only**) | Use of Gaussian saturation of sharp HY to get a passive-mask bound for every real $p\ge2$ |
| (F) Spectral-norm bound | **Not found** (ingredients published) | Medium | Same as (E), plus (A) | — |

"Not found" means not found in the search logged below, which did not include MathSciNet, zbMATH, Web of Science or Google Scholar. Two possibly relevant texts were located but not read: Klaus–Shaw 2003 (closed access) and Klaus's 2005 survey. For (A) these are the main gaps; see Loose ends.

## Part (A): the single-eigenvalue inequality

### What is published

**1. The sharp constant and extremizer for real nonnegative potentials (DGPV 2024).**

*What DGPV prove.* DGPV study $D_m-V$ on $L^2(\mathbb R,\mathbb C^2)$, with $D_m=\begin{pmatrix}m&\partial_x\\-\partial_x&-m\end{pmatrix}$ and $V\in L^p(\mathbb R,\mathbb R_+)$. They bound the lowest eigenvalue $\lambda_D(V)$ in the gap $(-m,m)$ in terms of $\lVert V\rVert_p$.
- **Theorem 1.3** ($d=1$, $p\in(1,\infty)$, $\lambda\in(-m,m]$). The optimal potential is $V(x)=A/(m\cosh Bx+\lambda)$, with $A=\frac{p}{p-1}(m^2-\lambda^2)$ and $B=\frac{2}{p-1}\sqrt{m^2-\lambda^2}$. The optimal norm $\alpha_D(\lambda,p)$ is given by a Beta function times a ${}_2F_1$ (their Eq. 1.10).
- **Corollary 1.2.** The bound is optimal.
- **Theorem 1.1.** $\Lambda_D(\cdot,p)$ is strictly decreasing.
- **Form of the optimizer.** The optimal potential is $V=\lvert\Psi\rvert^{2/(p-1)}$, where $\Psi$ solves the nonlinear Dirac equation (1.6). In 1D that solution is unique up to phase and translation (Theorem 1.3).

*Correspondence with ZS.* Take real $q$ and $\zeta=i\eta$, so that $v_1'=\eta v_1+qv_2$ and $v_2'=-qv_1-\eta v_2$. Then $(\phi,\chi)=(v_1-v_2,\,-(v_1+v_2))$ satisfies
$$\phi'=-(m+V)\chi,\qquad \chi'=(V-m)\phi,\qquad m=\eta,\ V=q.$$
This is DGPV's Eq. (5.1) at $\lambda=0$, the linear eigenvalue equation $(D_m-V)\Psi=0$. The map is invertible, so it carries $L^2$ solutions to $L^2$ solutions. The sympy residuals of both equations are 0 (run `2026-10-18-claude-interactive.10-zs-novelty-constants`).

*What follows for ZS.* Let $q\ge0$ have a ZS eigenvalue $i\eta$. Then $0$ is an eigenvalue of $D_\eta-q$, so $\lambda_D(q)\le0$. By Corollary 1.2 and the monotonicity in Theorem 1.1, $\lVert q\rVert_p\ge\alpha_D(0,p)$.

*Comparison with the claim, at $\lambda=0$.*
- **Extremizer.** DGPV's optimal potential is $\frac{pm}{p-1}\mathrm{sech}\frac{2mx}{p-1}$, which is the claim's $q_*$ with $m=\eta$.
- **Constant.** Their $\alpha_D(0,p)^p$ equals $C_p\,\eta^{p-1}$. For $p\in\{1.25,1.5,2,3,4,7,10\}$ and $\eta\in\{1,0.7\}$, the relative difference is at most $6\times10^{-41}$, both from their hypergeometric formula and by quadrature of their $V^p$. Their $V$ and $q_*$ agree pointwise to $5\times10^{-41}$ on a grid (same run).
- **The $L^1$ case.** DGPV's $p=d=1$ result, $\alpha_D(\lambda,1)=\arccos(\lambda/m)$, gives $\pi/2$ at $\lambda=0$. That is the Klaus–Shaw threshold, restricted to nonnegative $q$.

So, for real nonnegative potentials and purely imaginary eigenvalues, (A) with its constant and its extremizer is a published theorem: online in 2023, and on arXiv as 2210.03091 in October 2022. It is stated for Dirac operators, without reference to ZS or solitons. DGPV's proof differs from the claim's: Birman–Schwinger reformulation, concentration compactness, and an explicit phase-plane solution in 1D.

**2. The same functional form for complex potentials, with a weaker constant (Cuenin–Laptev–Tretter 2014).**
- **Their result.** CLT treat $H_0+V$ with $H_0=-i\sigma_1\partial_x+m\sigma_3$ and a general complex $2\times2$ matrix potential $V$. Corollary 4.6 at $m=0$, where $\eta(\lvert\Phi\rvert)=1$ by their Example 4.7, gives for every non-real eigenvalue $z$: $\lvert\mathrm{Im}\,z\rvert\le\frac{2(p-1)}{p}\lVert V\rVert_p^{p/(p-1)}$, for $p\in(1,\infty)$.
- **Why it covers ZS.** The ZS problem is $(i\sigma_3\partial_t+W)v=\zeta v$ with $\lVert W(t)\rVert=\lvert q(t)\rvert$. It is unitarily equivalent to CLT's massless operator, with $z=\zeta$.
- **The resulting bound.** $\int\lvert q\rvert^p\ge C^{\rm CLT}_p\eta^{p-1}$, with $C^{\rm CLT}_p=\big(\frac{p}{2(p-1)}\big)^{p-1}$.
- **Comparison with $C_p$.** The claim's constant is larger by the factor $C_p/C^{\rm CLT}_p=pJ_p2^{p-2}$. In the run this factor is 1.571 at $p=1.0001$, 4 at $p=2$, 9.42 at $p=3$, 21.3 at $p=4$ and 220 at $p=7$. CLT's constant is not sharp for the ZS class, and CLT do not claim it is.
- **The underlying estimate.** It is a Birman–Schwinger bound built on the function $F_V$ of Davies and Nath, J. Comput. Appl. Math. (2002), Corollary 2.17. That reference is cited by CLT and was not accessed here.

**3. The three endpoints are classical.**
- **$p\to1$.** $\lVert q\rVert_1\ge\pi/2$ is the Klaus–Shaw area threshold for complex $L^1$ potentials (SIAM J. Math. Anal. 34 (2003) 759; **abstract only**). It is restated, with this attribution, in Yousefi–Kschischang Part I, §IV-D (**full text**) and in Biondini–Luo 2018 (**full text**). Biondini–Luo say it improves an earlier, weaker threshold in Ablowitz–Kaup–Newell–Segur 1974 (**not accessed**). Kivshar 1989 (**abstract only**) gives a soliton-generation threshold for pulses of constant phase.
- **$p=2$.** $4\eta\le\lVert q\rVert_2^2$ is the energy trace (nonlinear Parseval) identity: the continuous-spectrum energy $\frac1\pi\int\log(1+\lvert\hat q\rvert^2)\ge0$. See Yousefi–Kschischang Part I, §IV-D property 8 (**full text**).
- **$p\to\infty$.** $\eta\le\lVert q\rVert_\infty$ is the numerical-range bound. Biondini–Oregero–Tovbis publish it for periodic and Dirichlet spectra (Lemma 3.8, **full text**). The earlier gpt-b review records that the earliest decaying-line statement was not established.

**4. The proof technique has a classical ingredient.** For real potentials, Klaus and Mityagin use the Prüfer angle equation $\theta'=-p(t)-s\sin2\theta$ for the ZS system at $\zeta=is$ (J. Math. Phys. 48 (2007) 123502, Eq. 3.4, **full text**).
- **Their attribution.** They cite it to earlier Klaus–Shaw work: "a Prüfer transformation as in Ref. 11", where their Ref. 11 is the 2002 PRE paper. The single-lobe proof in that PRE paper, which I read, uses integral identities rather than a Prüfer angle, so the attribution was not traced further.
- **The claim's equation** is the complex analogue: $\theta'=\nu-\eta\sin2\theta$ for the angle between the moduli, with $\nu\le\lvert q\rvert$.
- **Not found in any source read:** weighting that equation by $\sin^{p-1}2\theta$ and using the pointwise bound $r^p\ge K_ps^{p-1}(r-s)$.

### What was not found

- The sharp inequality with $C_p$ for complex potentials, or for eigenvalues $\xi+i\eta$ with $\xi\ne0$. By Galilean invariance, the latter reduce to complex potentials with $\zeta=i\eta$.
- The sharp inequality for sign-changing real potentials. DGPV require $V\ge0$.
- The weighted spinor-angle proof.
- Any statement of the ZS ↔ massive-Dirac correspondence used above. It is elementary and may well appear somewhere, but no source read states it.

### An observation for the verifier (numerical evidence only, no proof)

The claim's angle inequality $\theta'\le\lvert q\rvert-\eta\sin2\theta$ looks like a sub-solution of the real Prüfer equation $\Theta'=\lvert q\rvert-s\sin2\Theta$ for the potential $\lvert q\rvert$. If standard comparison and oscillation arguments go through, it would give the following: for every eigenvalue $\xi+i\eta$ of a complex $q$, the real potential $\lvert q\rvert$ has an imaginary eigenvalue $is$ with $s\ge\eta$. In that case the complex case of (A) would follow from DGPV's real case: apply their Keller bound at mass $s$ to get $\int\lvert q\rvert^p\ge C_ps^{p-1}\ge C_p\eta^{p-1}$.

**Numerical test.** Run `2026-10-18-claude-interactive.10-zs-modulus-comparison` used Fourier collocation with two grids on 55 potentials:
- 3 sech validation cases, reproducing Satsuma–Yajima to $6\times10^{-14}$;
- 18 chirped or phase-modulated sech pulses;
- 8 two-hump pulses with a relative phase;
- 4 real sign-changing pulses;
- 12 passive masks on sech spectra;
- 10 random complex Gaussian sums.

**Result.**
- $\eta_{\max}(q)\le\eta_{\max}(\lvert q\rvert)$ held in every case. Equality occurred only where $q=\lvert q\rvert$.
- The smallest strict margin was $3.5\times10^{-5}$. The two-grid error was at most $6\times10^{-11}$ for $q$ and $8\times10^{-4}$ for $\lvert q\rvert$; the larger value comes from the kinks of $\lvert q\rvert$ at sign changes. In those cases the margins were at least $0.02$ and at least 100 times the two-grid error.
- The maximizing eigenvalue of $\lvert q\rvert$ was on the imaginary axis in every case, with $\lvert\mathrm{Re}\,\zeta\rvert\le1.4\times10^{-14}$.

These numbers support the comparison but do not prove it. The test set is small and was not adversarially optimized.

**What it would mean.** If the comparison is true and easy, the complex extension of (A) is a short combination of DGPV with a Prüfer comparison. The novelty of (A) would then reduce to the self-contained elementary proof and the soliton-content application.
- **Status.** Recorded as loose end T-20261018-claude-interactive.10-02.
- **Possible source.** The comparison may be how Klaus–Shaw 2003 prove the complex $\pi/2$ threshold, but that text was not accessible (loose end T-20261018-claude-interactive.10-01).

### Consequence for the claim's wording

The card should not present the constant or the extremizer as new. It should cite:
- DGPV 2024 (Thm 1.3 at $\lambda=0$, via the change of variables above) for real $q\ge0$ and $\zeta\in i\mathbb R_+$;
- CLT 2014 (Cor. 4.6) for the non-sharp form with complex potentials.

The candidate novelty of (A) is then:
1. the extension of the sharp constant to complex potentials and off-axis eigenvalues;
2. the one-page elementary proof;
3. its use for soliton content.

## Part (B): passive-mask ceiling from even moments

The step $\int\lvert q_m\rvert^{2n}\le\int\lvert q_0\rvert^{2n}$ for $\lvert m\rvert\le1$ and $S\ge0$ is the upper majorant property for even exponents.
- **Source.** Lenzmann and Sok, arXiv:1805.06294v4, Lemma 5.1 (**full text**), call it "a classical fact that can be traced back to the works of Hardy and Littlewood". They note it fails for $p\notin2\mathbb N\cup\{\infty\}$. This agrees with the claim's warning that the real-$p$ extension is false.
- **Earlier repository review.** The gpt-b review of 2026-10-16 already identified the peak and $L^4$ cases for passive masks as Fourier-majorant facts. It found no theorem on the largest eigenvalue.
- **This search.** It found no paper that combines the majorant property with an eigenvalue inequality to bound soliton content under spectral masks. The arXiv queries for "majorant" with "soliton", and for "Hausdorff-Young" with "soliton", returned nothing relevant.

The masked pulse $q_m$ is complex even when $S$ is real and even. (B) therefore needs (A) for complex potentials, and DGPV's real case alone is not enough.
- **Where the novelty of (B) sits.** It rests on the unpublished part of (A), unless the comparison $\eta(q)\le\eta_{\max}(\lvert q\rvert)$ is published or easy.
- **Evidence on the comparison.** All 12 passive-mask cases of run `2026-10-18-claude-interactive.10-zs-modulus-comparison` satisfy it.
- **If the comparison holds, (B) follows from published pieces:** the majorant property, DGPV, and the comparison. The new content would then be the observation that these combine into a passive-mask ceiling.

## Part (C): global TL optimality for integer-order sech

- **Already known.**
  - The TL eigenvalues $i(N-\tfrac12-k)$ are Satsuma–Yajima's. Their 1974 paper was not accessed; the result is stated in Biondini–Oregero–Tovbis's introduction (**full text**). The TL leading fraction $(2N-1)/N^2$ follows directly.
  - Optimization over a launch family exists for a different class. Lazaridis, Debarge and Gallion (Opt. Lett. 20 (1995) 1680, **abstract only**) choose the power and width of chirped sech² pulses to maximize the energy in the fundamental soliton. Their chirp is tied to the laser's phase-amplitude coupling, and their spectrum is not fixed.
  - Chirp and soliton content for chirped sech and Gaussian pulses was surveyed in the problem card's literature section (Prilepsky et al. 2007; Chekhovskoy et al.; Tovbis–Venakides). Those are temporal-chirp families, not passive masks at fixed spectral magnitude.
- **Not found.** A theorem, or even a conjecture outside this repository, that no passive mask can raise the leading eigenvalue of an integer-$N$ sech above $N-\tfrac12$. The repository's own C-20261016-claude-a-01 states the TL-optimality conjecture numerically, and the present claim reports a counterexample to it for an asymmetric spectrum.
- **Medium confidence**, because physics-literature coverage is necessarily incomplete.

Like (B), (C) uses (A) on the complex masked pulse $q_m$. Its proof therefore depends on the part of (A) not covered by DGPV, or on the comparison discussed under (A).

## Part (D): non-integer sech ceilings

These follow from (B) through the closed-form moments $\int\mathrm{sech}^{2n}$. No published headroom ceiling for spectral shaping of a sech laser was found. As a self-standing result it is a corollary.

## Part (E): Gaussian lasers via sharp Hausdorff–Young

- **The ingredient.** The sharp Hausdorff–Young inequality with Gaussian extremizers is Beckner's (Ann. Math. 102 (1975) 159, DOI 10.2307/1970980, **not accessed**; PNAS announcement DOI 10.1073/pnas.72.2.638, **abstract only**; both DOIs checked on Crossref). According to the PNAS abstract, it extends earlier work of Babenko.
- **The observation.** For a Gaussian $S$, $\lVert\mathcal F^{-1}(mS)\rVert_p\le\lVert\mathcal F^{-1}S\rVert_p$ for every real $p\ge2$ and every $\lvert m\rvert\le1$. This is immediate from sharp HY, but it was not found stated as a majorant property for Gaussian majorants.
- **Not found.** Any use of it for soliton content.
- **Related but different.** The recent "nonlinear Hausdorff–Young inequality" (Suragan, arXiv:2608.15895, **abstract only**) concerns the transmission coefficient of the nonlinear Fourier transform, not discrete eigenvalues.

## Part (F): spectral-norm bound

This is (A) combined with sharp HY. Not found.

## Source ledger

Access levels: **full text** means the relevant sections were read. That is the whole paper for the short items, and the named theorems for the long ones. **Abstract only** means abstract or index record. **Not accessed** means located through a citing source or a DOI record only.

| Source | Identifier | Access | Used for |
|---|---|---|---|
| Dolbeault, Gontier, Pizzichillo, Van Den Bosch, Rev. Mat. Iberoam. 40 (2024) 649–692 | DOI 10.4171/RMI/1443; arXiv:2210.03091 | full text (published CC BY 4.0 version and author preprint): Thm 1.1, Cor 1.2, Thm 1.3, Eq. 1.12, §5.1 | Sharp constant and sech extremizer at $\lambda=0$; no mention of ZS |
| Cuenin, Laptev, Tretter, Ann. Henri Poincaré 15 (2014) 707–736 | DOI 10.1007/s00023-013-0259-3; arXiv:1207.6584 | full text: Thm 2.1, §3, Cor 4.6, Ex 4.7 | Non-sharp $L^p$ form for complex matrix potentials |
| Cuenin, Siegl, Lett. Math. Phys. 108 (2018) 1757–1778 | DOI 10.1007/s11005-018-1051-6; arXiv:1705.04833 | full text: §2.2 | Lieb–Thirring sums only; no sharp single-eigenvalue bound |
| Mizutani, Schiavone, Rev. Math. Phys. (2022) | DOI 10.1142/S0129055X22500234; arXiv:2108.12854 | full text: rigidity assumptions, Thms 1, 2, 5 | Keller-type Dirac bounds; in 1D only $L^1$ |
| D'Ancona, Fanelli, Schiavone, "Eigenvalue bounds for non-selfadjoint Dirac operators" | arXiv:2006.02778 | abstract and introduction | $n\ge2$ only |
| D'Ancona, Fanelli, Krejčiřík, Schiavone, Nonlinear Anal. (2021) | DOI 10.1016/j.na.2021.112565; arXiv:2104.13647 | abstract only | Not relevant |
| Frank, Simon, J. Spectral Theory 7 (2017) 633–658 | DOI 10.4171/JST/173; arXiv:1504.01144 | full text: introduction | 1D complex Schrödinger context; Keller and Davies–Nath attributions |
| Frank, Laptev, Seiringer, "A sharp bound on eigenvalues of Schrödinger operators on the halfline with complex-valued potentials" | arXiv:0903.2053 | full text: introduction | Sharp half-line $L^1$ bound; context only |
| Klaus, Shaw, SIAM J. Math. Anal. 34 (2003) 759–773 | DOI 10.1137/S0036141002403067 | abstract only (closed access per Unpaywall and Semantic Scholar) | $\pi/2$ threshold for complex $L^1$ potentials. Proof method not checked |
| Klaus, Shaw, Phys. Rev. E 65 (2002) 036607 | DOI 10.1103/PhysRevE.65.036607 | full text (VTechWorks) | Single-lobe theorem; no $L^p$ bound |
| Klaus, Mityagin, J. Math. Phys. 48 (2007) 123502 | DOI 10.1063/1.2815810 | full text (VTechWorks): §§1–3 | Real-potential Prüfer equation (3.4); reference list |
| Klaus, "On the Zakharov–Shabat eigenvalue problem", Contemp. Math. 379 (2005) 21–45 | (no DOI found) | not accessed (located as ref. 13 of Klaus–Mityagin 2007) | Possible survey of bounds; loose end |
| Biondini, Oregero, Tovbis, J. Spectral Theory (2023) | DOI 10.4171/JST/432; arXiv:2010.04263 | full text: introduction, Lemma 3.8, §5 | Peak bound (periodic/Dirichlet); Satsuma–Yajima statement |
| Biondini, Luo, Phys. Lett. A 382 (2018) 2632 | DOI 10.1016/j.physleta.2018.06.045 | full text (author copy): introduction, references | Area-theorem attribution; AKNS 1974 as the earlier, weaker bound |
| Ablowitz, Kaup, Newell, Segur, Stud. Appl. Math. 53 (1974) 249 | (no DOI recorded) | not accessed | Earlier $L^1$ threshold, per Biondini–Luo |
| Yousefi, Kschischang, IEEE Trans. Inf. Theory 60 (2014) 4312 (Part I) | DOI 10.1109/TIT.2014.2321143; arXiv:1202.3653 | full text: §IV-D | Nonlinear Parseval identity ($p=2$); $\pi/2$ statement citing Klaus–Shaw |
| Kivshar, J. Phys. A 22 (1989) 337 | DOI 10.1088/0305-4470/22/3/017 | abstract only | Generation threshold for constant-phase pulses |
| Desaix, Anderson, Lisak, Phys. Rev. E 50 (1994) 2253 | DOI 10.1103/PhysRevE.50.2253 | abstract only | Variational reformulation of ZS; no bound stated in abstract |
| Desaix, Anderson, Helczynski, Lisak, Phys. Rev. Lett. 90 (2003) 013901 | DOI 10.1103/PhysRevLett.90.013901 | abstract only | Real symmetric pulses; area formula not always correct |
| Lazaridis, Debarge, Gallion, Opt. Lett. 20 (1995) 1680 | DOI 10.1364/OL.20.001680 | abstract only | Optimum chirped-sech² launch; different input class |
| Blow, Wood, Opt. Commun. 58 (1986) 349 | DOI 10.1016/0030-4018(86)90242-7 | not accessed | Chirp and soliton evolution (title, index record) |
| Mitschke et al., "Soliton content of fiber-optic light pulses", Appl. Sci. 7 (2017) 635 | DOI 10.3390/app7060635 | abstract only (publisher blocked) | Review of methods; no bound stated in abstract |
| Korneev, Catana Castellanos, Vysloukh, Rev. Mex. Fís. 65 (2019) 634 | SciELO S0035-001X2019000600634 | full text, skimmed through a fetch-tool summary | ZS ↔ complex Schrödinger; approximations only, no bound |
| Lenzmann, Sok, "A sharp rearrangement principle in Fourier space…" | arXiv:1805.06294v4 | full text: §5, Lemma 5.1 and remark | Even-moment majorant (classical, Hardy–Littlewood) |
| Beckner, Ann. Math. 102 (1975) 159–182 | DOI 10.2307/1970980 | not accessed (Crossref record checked) | Sharp Hausdorff–Young |
| Beckner, PNAS 72 (1975) 638–641 | DOI 10.1073/pnas.72.2.638 | abstract only (page images) | Same |
| Suragan, "The nonlinear Hausdorff–Young inequality" | arXiv:2608.15895 | abstract only | NLFT transmission coefficient; not about eigenvalues |
| Dremov, Mullyadzhanov, Gelash, "Eigenvalue-based approach to manipulate and reconstruct nonlinear pulses" | arXiv:2607.12339 | abstract only | Perturbative eigenvalue control of sech fields; no bounds |
| Tikan et al., Phys. Rev. Fluids 7 (2022) 054401 | DOI 10.1103/PhysRevFluids.7.054401; arXiv:2108.02698 | abstract only | Nonlinear spectral engineering of water waves; no bounds |
| Hirota, "Real eigenvalues of a non-self-adjoint perturbation of the self-adjoint ZS operator" | arXiv:1704.03145 | abstract only | Defocusing ZS; not relevant |
| Stefanescu, "Eigenvalue bounds for non-self-adjoint Schrödinger operators…" | arXiv:2605.16569 | abstract and introduction | Survey of complex Schrödinger bounds; no ZS |
| Amore, Fernández, Jimenez, Phys. Lett. A (2018) | DOI 10.1016/j.physleta.2018.05.048; arXiv:1801.10034 | abstract only | Not relevant |
| Repository: gpt-b review of 2026-10-16 | `docs/review-2026-10-16-gpt-b-supercontinuum-literature.md` | read: ZS bound and spectral-phase sections, search log | Earlier negative search on TL optimality; majorant identification |

## Search log

All searches were run on 2026-10-18, 08:18–08:45 EDT.

**Web search (general engine), in order:**
1. ZS eigenvalue bound, $L^p$ norm, sharp constant, sech extremal.
2. Klaus–Shaw on the eigenvalues of ZS systems, $L^1$ norm, $\pi/2$.
3. Cuenin–Laptev–Tretter, non-selfadjoint Dirac operators on the real line.
4. Lieb–Thirring inequality, ZS, imaginary parts of eigenvalues.
5. Cuenin–Siegl, one-dimensional non-self-adjoint Dirac operators.
6. Klaus's survey "On the Zakharov–Shabat eigenvalue problem".
7. Desaix et al. on real symmetric pulses.
8. Sharp bound on the imaginary part of eigenvalues, non-selfadjoint massless Dirac, $L^p$, Birman–Schwinger.
9. ZS eigenvalue bounds by Prüfer or Riccati angle, area-theorem generalization.
10. Klaus–Shaw on pulse shape and chirp.
11. Klaus–Shaw 2003 full text on VTechWorks.
12. NFT discrete eigenvalue bounds: peak, energy, $L^p$.
13. ZS sharp $L^p$ inequality with hyperbolic secant extremizer.
14. **Keller inequality, one bound state, sharp constant, Dirac, sech optimizer.** This query found DGPV.
15. Focusing NLS soliton content, $L^p$ bound, isoperimetric.
16. The DGPV arXiv record.
17. "Keller estimate" with ZS.
18. Sharp eigenvalue bounds for non-self-adjoint 1D Dirac operators with $L^p$ potentials, 2024–2025.
19. Lyapunov-type inequalities for Dirac or Hamiltonian systems with $L^p$ norms.
20. Soliton content of chirped pulses; spectral phase; TL optimality.
21. Hausdorff–Young or Fourier majorant in nonlinear Fourier analysis.
22. NFT signal design under bandwidth constraints.
23. ZS with Gagliardo–Nirenberg, Keller or nonlinear Dirac.
24. Lieb–Thirring for ZS or AKNS operators.
25. Majorant property with Gaussian majorants and sharp Hausdorff–Young.
26. Whether spectral phase can raise soliton number or content; TL maximality proofs.
27. Higher-order soliton with spectral phase: largest eigenvalue and maximal fraction.
28. Ocean-wave NLFA: phase alignment and largest soliton.
29. Prechirp and soliton fission: maximal soliton energy.
30. Golinskii and Korotyaev on non-self-adjoint Dirac and ZS eigenvalue estimates.
31. One-bound-state sharp inequalities for 1D Dirac with electric potential.

**arXiv API:**

| Query | Hits |
|---|---|
| `all:"Zakharov-Shabat" AND all:eigenvalue AND all:bound` | 4 |
| `all:Keller AND all:Dirac AND all:eigenvalue` | 3; found Mizutani–Schiavone |
| `all:"Zakharov-Shabat" AND all:"Lieb-Thirring"` | 0 |
| `abs:"soliton content"` | 12 |
| `all:"pulse shaping" AND all:soliton AND all:eigenvalue` | 1 |
| `all:"nonlinear Fourier" AND all:"spectral phase"` | 1 |
| `all:"Hausdorff-Young" AND all:soliton` | 0 |
| `all:majorant AND all:soliton` | 25, none relevant |
| `all:"transform-limited" AND all:"Zakharov-Shabat"` | 0 |
| `all:"soliton fission" AND all:"spectral phase"` | 0 |

**OpenAlex forward citations, screened by title:**
- Klaus–Shaw 2003: 81 citing works. None has a title suggesting an $L^p$ eigenvalue bound. The ones opened are in the ledger.
- Cuenin–Laptev–Tretter 2014: 40 citing works. None is ZS-specific with a sharp $L^p$ constant.
- DGPV 2024: 2 citing works in the index (2026, nonlinear Dirac bound states and electromagnetic Dirac point spectrum). Neither concerns ZS.

**OpenAlex keyword searches** for the chirped-sech launch, Blow–Wood, soliton-content reviews and Kivshar/Burzlaff. **Unpaywall and Semantic Scholar** for open copies of Klaus–Shaw 2003 (closed).

**Not searched:** MathSciNet, zbMATH, Web of Science, Google Scholar (no access), theses, and books (for example Ablowitz–Segur and Lamb). A sharp complex-potential statement could sit in a book chapter or thesis that these searches do not reach.

## Loose ends

- **Full texts.** Read Klaus–Shaw 2003 and Klaus 2005 (Contemp. Math. 379). Check whether either proves an $L^p$ variant, or the comparison $\eta(q)\le\eta_{\max}(\lvert q\rvert)$ for complex $q$. Task T-20261018-claude-interactive.10-01.
- **The comparison itself.** Decide whether the angle inequality yields $\eta(q)\le\eta_{\max}(\lvert q\rvert)$. If it does, the complex case of (A) is a corollary of DGPV and the novelty of (A) shrinks to the elementary proof. Task T-20261018-claude-interactive.10-02.
- **The claim card.** Revise it to credit DGPV 2024 and CLT 2014 and to restate the novelty of (A). Task T-20261018-claude-interactive.10-03.
