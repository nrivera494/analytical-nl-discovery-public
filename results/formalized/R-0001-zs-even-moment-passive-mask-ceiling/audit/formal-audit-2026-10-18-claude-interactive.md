---
auditor: claude-interactive
model: claude-opus-5-5
family: claude
date: 2026-10-18
verdict: pass
subject: formal/ZSFormalization
formalizer: pi-codex
formalizer_family: gpt
run: 2026-10-18-claude-interactive-zs-lean-audit
task: T-20261018-claude-interactive-04
---

# Formal audit of the ZSFormalization Lean library

**Subject.** The ZSFormalization Lean library, from the PI's Codex session. Its family is gpt; the model is GPT 6 Astra Max (the PI, 2026-10-19; task T-20261018-claude-interactive-08). It was first delivered at `~/Documents/Codex/2026-10-18/loo/outputs/ZSFormalization` and is now [`formal/ZSFormalization/`](../../../../formal/ZSFormalization/), copied verbatim. It formalizes parts of claim C-20261018-pi-chatgpt-01.

**Method.**
- I read all 13 source files (1,818 lines) before the formalizer's README.
- I rebuilt the library from scratch, first standalone and then inside `formal/`, against my own checkout of the pinned dependencies.
- I re-checked the compiled proofs with two kernel checkers.
- I added held-out certificates and a negative control.

Every step is reproduced by `runs/2026-10-18-claude-interactive-zs-lean-audit/run.sh`.

**Independence.** I am family claude; the formalizer is family gpt. The claim's proposer is also family gpt, and its verifier and auditor were claude. I had read the claim card and the derivation note before this audit, so this is not a clean-context audit of the claim. It is an audit of whether the Lean statements say what result R-0001 says.

## Verdict

**Pass.** The Lean development proves (A) at even exponents, (B), (C) and (D) as stated in R-0001, under two restrictions:
- **Even exponents only:** $p=2n$.
- **Smooth masks only:** the masked spectrum $mS$ must be a Schwartz function.

The proofs are genuine:
- There is no `sorry`, no added axiom, and no hypothesis that assumes its conclusion.
- Every hypothesis of the headline theorems can be satisfied: the sources are constructed, and the optimum is attained by an explicit eigenfunction.

The claim's (E), (F) and the real-exponent part of (A) are not formalized; the formalizer's README says so accurately.

## Part by part

| Claim part | Lean status | Main theorem(s) | Restrictions and what is open |
|---|---|---|---|
| (A) $\int\lvert q\rvert^p\ge C_p\eta^{p-1}$ | **Proved for even $p=2n$, $n\ge1$** | `eigenvalue_even_moment_bound`, `schwartz_eigenvalue_even_moment_bound` | See the notes below the table. |
| (B) passive-mask ceiling $U_{2n}[S]$ | **Proved for every $n\ge1$** | `passive_source_eigenvalue_bound`, `passive_mask_even_moment` | $S\ge0$ must be Schwartz, and $mS$ must be Schwartz with $\lvert m\rvert\le1$. Hard-edged or pixelated masks and non-Schwartz sources are not covered. The $n\to\infty$ peak limit is not formalized. |
| (C) integer sech: $\sup\eta=N-\tfrac12$, $f_1=(2N-1)/N^2$ | **Proved for all integer $N\ge1$**, as an attained maximum (`IsGreatest`) | `canonical_integer_sech_optimality`, `canonical_integer_sech_fraction_optimality` | Same mask class as (B). The maximum is over every eigenvalue of every admissible masked pulse, and the identity mask attains it. $E_{1,\max}$ in physical units is only a unit conversion and is not formalized. |
| (D) non-integer sech ceilings | **Proved:** the polynomial ceiling for all real $N\ge0$, attainment of $N-\tfrac12$ for real $N>\tfrac12$, and exact rational enclosures at $N=2.5$, 3.5, 5.5 and 9.5 | `sech_source_polynomial_ceiling`, `rational_sech_height_enclosure`, `canonical_sech_*_enclosure`, `real_sech_has_eigenvalue` | It is not proved that $N-\tfrac12$ is the TL pulse's largest eigenvalue; the enclosure does not need it. |
| (E) Gaussian, sharp Hausdorff–Young, real $p$ | **Not formalized** | only `canonical_gaussian_ceiling`, the even-exponent form, left symbolic | See the Gaussian section below. |
| (F) spectral-norm bound | **Not formalized** | none | Not present in any file. |
| Counterexample to C-20261016-claude-a-01 | Not formalized | none | Numerical only (run `2026-10-18-claude-interactive.9-mask-adversary`). |
| NLSE dynamics; $4\eta$ is the soliton energy | Not formalized | none | Static ZS problem only. $f_1=4\eta/M_0$ is a definition. |

Notes on (A):
- **What the proof covers.** It holds for complex $q$ and any $\zeta$ with ${\rm Im}\,\zeta>0$, including off the imaginary axis. The potential must be continuous and bounded, satisfy $|q|\to0$ at $\pm\infty$, and have $|q|^{2n}\in L^1$; every Schwartz potential qualifies.
- **The constant is sharp at every even $p$.** At $p=2N$ the bound is attained, with $q=N\,{\rm sech}\,t$ and $\eta=N-\tfrac12$.
- **Open:** real $p>1$ (odd, fractional, and $1<p<2$), the limits $p\to1$ and $p\to\infty$, and the extremizer family $q_*$ with arbitrary $\eta$, centre, phase and carrier.

Novelty context: the novelty audit (claude-interactive.10) found (A) published only for real $q\ge0$ on the imaginary axis (Dolbeault et al. 2024). The new part is the complex, off-axis case. **That part is now machine-checked for even exponents**, which are the only exponents (B)–(D) use.

### The Gaussian case

`canonical_gaussian_ceiling` gives the even-exponent ceiling, with $\int_{-1}^1(1-s^2)^{n-1}ds$ and $\sqrt{\pi/n}$ unevaluated. I evaluated it in run `2026-10-18-claude-interactive-zs-lean-audit` (mpmath, not Lean), against claude-interactive.9's TL eigenvalues:

| $N$ | Best even $2n$ | Lean-proved $f_1$ ceiling | Headroom over TL | Claim's real-$p$ headroom (not formalized) |
|---|---|---|---|---|
| 1.5 | 2 | 1 (trivial) | 5.05% | 0.283% |
| 4 | 8 | 0.491473 | 0.0451% | 0.0150% |
| 5 | 10 | 0.405092 | 0.0222% | 0.00745% |
| 8 | 16 | 0.264189 | 0.00511% | 0.00172% |

The real-$p$ column reproduces claude-interactive.9's ceilings, which cross-checks the script. Sharp Hausdorff–Young (Beckner), the real-$p$ inequality and a certified TL Gaussian eigenvalue are all absent from the library.

## How the proof works, and the points checked

**The definitions are faithful to the physics.**
- `SolvesZS` is the focusing ZS system $v_1'=-i\zeta v_1+qv_2$, $v_2'=-\bar qv_1+i\zeta v_2$, with classical derivatives at every $t$. For continuous $q$, every $L^2$ eigenfunction is classical, so this does not narrow the class of eigenvalues.
- `IsEigenvalue` requires ${\rm Im}\,\zeta>0$ and a nonzero solution with both components in $L^2$.
- `attainableHeights g` is the set of ${\rm Im}\,\zeta$ over all Schwartz $f=mg$ with $|m|\le1$ and all eigenvalues of $\mathcal F^{-1}f$.
- `sourceEnergy` is $\int|\mathcal F^{-1}g|^2$, the upstream energy $M_0$.
- nanoda's independent pretty-printer output of `IsEigenvalue` and `SolvesZS` matches the source (run output `out/nanoda_output.txt`).

**The analysis is derived from the ODE, not assumed.**
- $|v_1|^2+|v_2|^2>0$ everywhere follows by a Grönwall argument.
- The polarization inequality $x'\ge2\eta(1-x^2)-2|q|\sqrt{1-x^2}$ is derived without dividing by a single spinor component, so the question of component zeros does not arise.
- The endpoint limits are proved from the $L^2$ condition and the decay of $q$.
- The weighted inequality is integrated through the primitive of $(1-s^2)^{n-1}$, so no monotonicity is needed.
- The sharp scalar inequality is proved from Bernoulli's inequality.

**The Fourier majorant** is proved by induction on convolution powers plus Plancherel, for Schwartz spectra. This is the source of the smooth-mask restriction.

**Positivity of the sech spectrum** uses $\int h(s)h(s-t)ds=\tfrac14{\rm sech}\,t$ with $h(s)=e^{s-e^{2s}}$, so the spectrum is a squared modulus. Fourier inversion then gives exactly $\mathcal F^{-1}S_N=N\,{\rm sech}\,t$.

**The sharpness witness** $v_1=e^{-t/2}{\rm sech}^Nt$, $v_2=-e^{t/2}{\rm sech}^Nt$ at $\zeta=i(N-\tfrac12)$ is checked for every real $N>\tfrac12$.

**Real-number literals.** Every constant ($1/2$, $5/2$, $7/16$ and the certificate decimals) is elaborated as a real number, so integer division does not truncate any of them.

## Integrity checks (run `2026-10-18-claude-interactive-zs-lean-audit`)

1. **Source hashes.** All 13 sources, the root module, the README and `Audit.lean` match `verification/source-sha256.txt`. The formalizer's `lakefile.toml`, `lake-manifest.json` and `lean-toolchain` are superseded by `formal/`'s; all nine dependency pins are identical (`out/pins.txt`).
2. **Build.** `lake build ZSFormalization AnalyticalNL` in `formal/` gives 9,037 jobs with no warnings and no errors. The only warnings under `formal/`'s Mathlib linter set were 32 line-length notes, so that one linter is off for this library and the sources stay byte-identical.
3. **Per-file compilation.** Each file compiled alone with default options gives zero messages.
4. **Source scan.** None of these appear: `sorry`, `admit`, `axiom`, `native_decide`, `implemented_by`, `extern`, `unsafe`, `opaque`, `set_option`, macros, elaborators, `run_cmd` or `ofReduceBool`.
5. **Axioms of every theorem.** `#print axioms` on all 121 theorems and lemmas gives only `propext`, `Classical.choice` and `Quot.sound`.
6. **Lean's own replay checker.** `leanchecker` replays all 13 modules, and a bogus module name is rejected, so a pass is meaningful.
7. **An independent kernel.** `nanoda_bin` 0.4.19, an independent type checker written in Rust, checked the exported dependency cone of 9 headline theorems: 54,113 declarations, no errors. Only the three standard axioms were allowed, and `Lean.trustCompiler` was not.
8. **Held-out certificates.** These were frozen in run `2026-10-18-claude-interactive-zs-moment-bound-check` before the formalization existed:
   - $N=9/2$ at 0.07161%: passes.
   - $N=15/2$ at 0.01518%: passes.
   - The integer case $N=7$ ($f_{1,\rm opt}=13/49$), instantiated from the general theorem: passes.
9. **Negative control.** The same certificate at $N=9/2$, set at 0.07160% (below the true 0.0716052%), fails: `norm_num` reduces it to `False`.

## What remains trusted

- **The Lean kernel and Mathlib** at commit `1f414401f69059aa7eead47b53ee40bd38455eeb`.
- **The toolchain binaries.** They came from a standard `elan` install on 12 Oct 2026, with no origin overrides. nanoda ships in the same toolchain bundle, so it is an independent implementation but not an independent download.
- **The README's PDF references.** It cites "Assess Claim Novelty.pdf", pp. 58–63, which is not in the repository; those references were not checked.

Apart from those references, the README's account of what is and is not proved matches the code.
