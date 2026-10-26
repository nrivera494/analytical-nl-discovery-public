---
date: 2026-10-17
agent: gpt-b
model: gpt-6-astra
family: gpt
task: T-20261016-claude-interactive.7-07
duration_min: 197
status: complete
---

## Did

Worked on the assigned task branch, stacked on the specified #56 branch.
Claimed verification tasks T-20261016-claude-interactive.7-07, -09 and -08;
all implementation and reports remain on the -07 branch. No subagents were
used. No other clone or conversation history was accessed.

Maintained clean context through the independent reports: cards, problem,
permitted cited-run metadata, evaluator and protocol/solver documentation only.
No proposer exploration, run script, log or PR description was read. Built an
independent exact-Hermite–Gauss resonant Hamiltonian, unitary intra-group
Brownian coupling, constrained-shell sampler and truncated-Wigner propagator.
Production predictions, numerical GGE references and follow-up plans were
committed before their respective runs; later diagnostics are labelled.

Ran serial simulations with a memory gate before numerical launches. Only
block statistics, final phase draws and sparse checkpoints were retained.
Raw arrays and progress logs are outside git at the paths in run metadata.
The pinned agents solver was read and used for a small full-tensor RK4IP
cross-check; neither solver repository was modified. No adjoint was used.

## Found

All numerical statements below trace to the named independent runs.

- `2026-10-17-gpt-b-dirichlet`: the scalar fixed-(N,E) condensed microcanonical
  identity is exact. Long-time weak-disorder moments agree, including held-out
  mode counts. The initial strong-disorder window and the original 200-phase
  test have recorded failures. Enlarging to 800 phases passes the same tests,
  with the original 200 trajectories reproduced exactly. The fresh energy
  holdout also passes every frozen moment and resolved-sign gate. Strong-disorder compatibility
  has broad uncertainty and does not establish a universal equilibration length.
- `2026-10-17-gpt-b-gge`: N, E, resonant H and angular momentum are conserved;
  Kohn/breathing identities are broken by the finite cutoff. Phase memory is
  reproduced. Including angular momentum improves several frozen endpoint
  predictions, but slow statistics, finite conditioning width and accessible
  sectors block a general GGE endpoint verification. The refined controlled
  aligned case misses its endpoint tolerance at the finer step. Strong disorder
  passes the prescribed condensate-fraction equivalence tolerance in the final
  longer windows at both steps, while retaining a nonzero paired residual.
  Stationarity is not mixing, and tolerance-level agreement is not zero memory.
- `2026-10-17-gpt-b-scrambling`: exact Kerr coherence has the expected
  square-root collapse law. Gaussianity can fail well before that collapse.
  GRIN TWA supports a logarithmic trend, but the coupled step refinement leaves
  its coefficient unverified. A post-report analysis correction distinguishes
  the normally ordered excess g2-1 from photon relative variance: the former
  was incorrectly labelled in the initial analysis. The all-mode clock is
  inconclusive on initial vacuum modes. The corrected occupied-mode diagnostic
  supports n-independence but is post hoc and precedes equilibrium. The Kerr
  limit is not an exact chaotic multimode verification.

The original bounded GGE follow-up is complete: narrower shell references were
committed before longer, finer-step trajectories and strong-disorder ensembles.
The phase-4103 narrow-shell sampler remains unresolved; the explicitly perturbed
aligned reference passes its sampler gates. The two 1200000-length phase-4103
trajectories remain too imprecise for the frozen endpoint requirement despite
small invariant drift. The long exact-sector discrepancy triggered one extra
half-step check, frozen at a97c5be before execution. That check also misses
its endpoint gate and remains imprecise; it does not establish a converged
infinite-time counterexample. All planned production is complete.

The primary-source review locates prior resonant invariants and invariant
Gibbs measures (arXiv:1501.03760 and 1502.05643, full text, relevant sections),
as well as optical GGE with angular momentum (DOI 10.1103/PhysRevLett.128.123901,
full text, theory). The bounded literature search does not certify novelty of
any complete fibre endpoint law. Search strings and access levels are in the
GGE run's literature file.

## Changed

Independent evaluator, three run directories with frozen predictions and
reproduction scripts, three clean-context audits, and one-page summaries
with a single figure per claim. The C02 card is refuted as written; C03
remains cheap-checks-passed with failed cross-family endpoint verification.
C01 is sim-verified for its narrowed scalar classical statement. Original proposer
statements are retained. No result folder, problem card or generated file
was edited by gpt-b; inherited #56 changes remain in the branch ancestry.

## Not verified

A calibrated physical fibre with polarization, finite disorder correlation,
inter-group leakage, dispersion/walk-off, gain/loss or Raman; a uniform
long-length error bound for beat averaging; universal ergodicity or mixing
lengths; exact chaotic many-mode quantum scaling; reduced-state Fock
invariance; the full Gaussian-lifetime/minimum-of-lengths claim; and the
multimode Hartree–Fock ballistic coefficient. Temporal window/aliasing and
≤3 fs Raman-grid tests do not apply to the monochromatic model.

## Loose ends

- T-20261017-gpt-b-01: physical-fibre and long-length errors in the scalar
  Dirichlet prediction, including realistic vector/colored/inter-group disorder.
- T-20261017-gpt-b-02: GGE sampling, slow mixing, step convergence, exact
  sectors and tighter strong-disorder residual-memory bounds.
- T-20261017-gpt-b-03: stochastic convergence of TWA slopes and a properly
  specified dephased relaxation observable with fresh holdouts.
- T-20261017-gpt-b-04: exact chaotic quantum tests, Gaussianity diagnostics
  and the multimode ballistic coefficient.

## Proposed card changes

For P-20261016-claude-interactive.7-01, keep the exact scalar classical
microcanonical statistics separate from quantum-state and dynamical-selection
claims. Do not infer Gaussianity from variance scaling or from coherence.
Replace a universal GGE endpoint statement with the stationary conditional
measure plus a clearly unresolved mixing requirement, and distinguish the
finite HG cutoff from the untruncated GRIN collective invariants. Retain phase
memory as an observed effect, with the actual conserved charges stated.

Disorder weak relative to group spacing may be strong relative to Kerr;
quote the noise convention and the two ratios separately. The current
strong-disorder tests do not establish a universal short relaxation length.
Any metre-scale extrapolation should carry the missing polarization,
correlation-length and long-time normal-form checks. The problem card was
left untouched as instructed.

## Final checks

All three assigned verification tasks are marked done with their actual outcomes;
remaining work is in the four follow-up tasks above. `scripts/validate.py` and
`scripts/check_generated.py origin/main` pass. Shared evaluator hashes match all
run metadata, all three run records are complete, JSON summaries are finite,
and each summary figure is below 250 KB. The final GGE figure was visually
checked. The solver is clean, original Statement sections are unchanged, and
there are no gpt-b changes to problem cards or protected generated files.
The work is submitted in PR #61 against main, stacked on #56; no merge is made.
