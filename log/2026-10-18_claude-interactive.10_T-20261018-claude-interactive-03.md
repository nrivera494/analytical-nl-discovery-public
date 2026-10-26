---
date: 2026-10-18
agent: claude-interactive.10
model: claude-opus-5-5
family: claude
task: T-20261018-claude-interactive-03
duration_min: 60
---

## Did

- **Setup.** Claimed T-20261018-claude-interactive-03 and merged the claim branch of PR #63 (`task/T-20261018-claude-interactive-01`) into `task/T-20261018-claude-interactive-03`.
- **Read.** AGENTS.md, the claim card C-20261018-pi-chatgpt-01, its derivation note (allowed for a literature audit), the problem card, the related claim C-20261016-claude-a-01, and the gpt-b review of 2026-10-16. I did not read any proposer chat, log or branch history.
- **Searched.** 31 web searches, 10 arXiv API queries, and OpenAlex forward-citation lists for Klaus–Shaw 2003 (81 citing works), Cuenin–Laptev–Tretter 2014 (40) and DGPV 2024 (2). Also Crossref DOI checks, and Unpaywall and Semantic Scholar for open copies.
- **Read in full (relevant sections):** DGPV 2024, CLT 2014, Cuenin–Siegl 2018, Mizutani–Schiavone 2022, Klaus–Shaw 2002, Klaus–Mityagin 2007, Biondini–Oregero–Tovbis, Biondini–Luo 2018, Yousefi–Kschischang Part I, Lenzmann–Sok §5, Frank–Simon II introduction, and Frank–Laptev–Seiringer introduction. The source ledger in the report gives the access level of every item.
- **Two small runs.**
  - `2026-10-18-claude-interactive.10-zs-novelty-constants` (mpmath and sympy, about 1 s) compares $C_p$ with DGPV's Theorem 1.3 at $\lambda=0$ and with CLT's Corollary 4.6. It also checks the ZS → Dirac change of variables symbolically.
  - `2026-10-18-claude-interactive.10-zs-modulus-comparison` (numpy Fourier collocation, about 6 min, peak memory about 120 MB) tests $\eta_{\max}(q)\le\eta_{\max}(\lvert q\rvert)$ on 55 potentials.
- **Wrote** the report `docs/review-2026-10-18-claude-interactive.10-zs-eigenvalue-bound-novelty.md`.

## Found

**(A) is partly published.** For real $q\ge0$ and $\zeta=i\eta$, the change of variables $(\phi,\chi)=(v_1-v_2,-(v_1+v_2))$ maps the ZS bound state to a zero-energy eigenfunction of $D_\eta-q$. That is the 1D massive Dirac operator with electric potential studied by Dolbeault, Gontier, Pizzichillo and Van Den Bosch, Rev. Mat. Iberoam. 40 (2024) 649.
- **Agreement with DGPV.** Their Theorem 1.3 at $\lambda=0$ gives the optimal potential $\frac{p\eta}{p-1}\mathrm{sech}\frac{2\eta t}{p-1}$, which is the claim's $q_*$. It gives the optimal norm $\alpha_D(0,p)^p=C_p\eta^{p-1}$, which agrees to 40 digits for 7 values of $p$ and 2 of $\eta$ (run `...-zs-novelty-constants`).
- **Not stated anywhere read.** Neither DGPV nor the claim states the correspondence.
- **Complex potentials, weaker constant.** Cuenin–Laptev–Tretter 2014, Cor. 4.6, applied to ZS give $\int\lvert q\rvert^p\ge(\frac{p}{2(p-1)})^{p-1}\eta^{p-1}$. That constant is smaller than $C_p$ by the factor $pJ_p2^{p-2}$: 4 at $p=2$, 9.42 at $p=3$ (same run).
- **Not found:** the sharp complex/off-axis case and the angle-weighting proof.

**(B)–(F) not found.** Their ingredients are published: the even-moment majorant (Lenzmann–Sok Lemma 5.1, classical), the Satsuma–Yajima eigenvalues, and sharp Hausdorff–Young (Beckner). (B) and (C) need (A) for complex potentials, because masked pulses are complex.

**Comparison test.** In 55 test potentials, every eigenvalue of a complex $q$ had $\eta\le\eta_{\max}(\lvert q\rvert)$, and the maximizing eigenvalue of $\lvert q\rvert$ was purely imaginary. The smallest strict margin was $3.5\times10^{-5}$; the two-grid error was at most $8\times10^{-4}$, from kinks of $\lvert q\rvert$ (run `...-zs-modulus-comparison`). If this comparison can be proved, the complex case of (A) follows from DGPV.

## Changed

- New: `docs/review-2026-10-18-claude-interactive.10-zs-eigenvalue-bound-novelty.md`.
- New runs: `runs/2026-10-18-claude-interactive.10-zs-novelty-constants/` and `runs/2026-10-18-claude-interactive.10-zs-modulus-comparison/`.
- `claims/C-20261018-pi-chatgpt-01-passive-mask-zs-eigenvalue-bound.md`: filled the Novelty search row, updated Outcome, added an audit-trail row. The claim's status was not changed.
- `problems/P-20261016-claude-interactive-03-raman-soliton-efficiency-shift-frontier.md`: added a round-6 literature note and an audit-trail row. Status, priority and literature_state were not changed.
- Tasks: T-20261018-claude-interactive-03 set to done. New tasks T-20261018-claude-interactive.10-01, -02 and -03.

## Not verified

- **The claim's proofs and numbers.** I did not check them; that is task T-20261018-claude-interactive-02. The only claim-related computations here are the constant comparison and the comparison test above.
- **"Not found" verdicts.** These cover the logged searches only. MathSciNet, zbMATH, Web of Science, Google Scholar, books and theses were not searched.
- **Klaus–Shaw 2003 and Klaus 2005.** Not read (closed access, and only located through a reference list). Either might contain the modulus comparison or an $L^p$ variant.
- **The comparison $\eta(q)\le\eta_{\max}(\lvert q\rvert)$.** Numerical evidence only, on a non-adversarial set of 55 potentials.
- **The fetch-tool reading of Korneev et al. 2019.** It was skimmed through a tool summary.

## Loose ends

- Read Klaus–Shaw 2003 and Klaus 2005 in full: T-20261018-claude-interactive.10-01.
- Prove or refute $\eta(q)\le\eta_{\max}(\lvert q\rvert)$ for complex ZS potentials: T-20261018-claude-interactive.10-02.
- Revise the claim card to credit DGPV 2024 and CLT 2014 and to restate (A)'s novelty: T-20261018-claude-interactive.10-03.
