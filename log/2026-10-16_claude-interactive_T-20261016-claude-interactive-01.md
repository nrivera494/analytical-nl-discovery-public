---
date: 2026-10-16
agent: claude-interactive
model: claude-opus-5-5
family: claude
task: T-20261016-claude-interactive-01
duration_min: 75
---

## Did

On the PI's request, I drafted three candidate problem cards on supercontinuum bounds:
- dispersive-wave yield;
- the long-wavelength photon budget beyond a cutoff;
- the efficiency–shift frontier of Raman-soliton conversion.

Each card asks for a ceiling and for the headroom of input spectral shaping over three nested input classes: phase-only masks, passive amplitude-and-phase masks, and any input of the same energy and band.

Three Claude-family literature reviews ran in parallel, one per topic, by research subagents (about 25 minutes of web search each). Their sources and access levels are folded into the cards.

I ran a numerical check of the Zakharov–Shabat bound sketch, registered as run `2026-10-16-claude-interactive-zs-bound-check`.

## Found

- **No rigorous upper bound** on dispersive-wave yield, on photons beyond a long-wavelength cutoff, or on Raman-soliton efficiency was found in any of the three reviews.
- **No gradient or adjoint optimization** of input shaping for these targets was found.
- **Headroom measurements:**
  - The only measured dispersive-wave headroom is one chirp scan, about 40% → 55% (Petty, PhD thesis, 2024).
  - Shaping gains elsewhere are narrow-band spectral-density gains against weak baselines (Hary et al. 2023 and 2025; Wetzel et al. 2018).
- **Starting structures, unverified orchestrator sketches recorded on the cards:**
  1. $\mathrm{Im}\,\zeta\le\|q\|_\infty$ for Zakharov–Shabat bound states, so passive shaping cannot raise any soliton above the transform-limited peak. For a sech laser the leading soliton's energy fraction is then at most $2/N$, against $(2N-1)/N^2$ for the transform-limited launch.
  2. At fixed spectral amplitude, phase shaping moves the conserved quantities only through $\int|A|^4$, which the transform-limited pulse maximizes.
  3. The photon number, momentum and Hamiltonian, plus the sharp Gagliardo–Nirenberg inequality, define a convex program that bounds band yield. This develops a remark by the dispersive-wave literature subagent.
- **The run supports sketches 1 and 2 numerically,** on 40 random masks.

## Changed

- New cards, all `candidate`:
  - `problems/P-20261016-claude-interactive-01-dispersive-wave-yield-ceiling-and-shaping-headroom.md`
  - `problems/P-20261016-claude-interactive-02-long-wavelength-supercontinuum-budget.md`
  - `problems/P-20261016-claude-interactive-03-raman-soliton-efficiency-shift-frontier.md`
- New run `runs/2026-10-16-claude-interactive-zs-bound-check/` (config, meta, summary, script).
- New tasks -02 to -05.

## Not verified

- **Sketches 1–3** are derivations by the proposer only. Task -02 proves or refutes sketch 1; task -03 builds the program of sketch 3.
- **Literature access** is often abstract only, and several key full texts were not read:
  - Roy et al. 2009;
  - Dudley et al., RMP 2006;
  - Klaus & Shaw 2003;
  - Kodama & Hasegawa 1987;
  - Pant et al. 2010.

  Some efficiency figures are search snippets, marked as such on the cards.
- **Huang et al., arXiv:2607.05244** was located only at abstract level.

## Loose ends

- T-20261016-claude-interactive-02: Zakharov–Shabat bound and the Raman-soliton headroom.
- -03: the conservation-law convex program for dispersive-wave yield.
- -04: the reach-model ceiling and optimal length beyond $\lambda_c$.
- -05: second-family (GPT) literature review, needed before the cards can become `audited`.
- **Overlap.** P-20261016-claude-interactive-01 absorbs P-20261012-claude-interactive.4-01 (PR #41). The PI may keep both or mark .4-01 superseded. P-20261016-claude-interactive-02 overlaps P-20261012-claude-interactive.4-04 (blue band, Raman budget) and P-20261012-claude-interactive-01 (conservation-law ceilings), both in PR #41.
