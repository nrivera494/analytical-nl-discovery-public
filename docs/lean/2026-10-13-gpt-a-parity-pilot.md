---
date: 2026-10-13
agent: gpt-a
model: gpt-6-astra
family: gpt
task: T-20261012-gpt-a-02
problem: P-20261010-claude-interactive-01
---

# Parity pilot: compiled finite-bin bounds

The finite-bin parity inequality and the corrected physical attenuation bound
are proved in [`formal/AnalyticalNL/Parity.lean`](../../formal/AnalyticalNL/Parity.lean),
with no proof holes or new axioms. This is a GPT-family mathematical check of
Claude-family C-20261010-claude-a-03, not a new simulation, a clean-context audit,
or a promotion. Claim and problem cards were not edited.

## Results

- `parity_lower_bound` proves
  $y^TAy\ge\min(e,(e+o)/2)\|y\|^2$ for every nonnegative vector, including zero.
  The finite index type may have fixed reflection bins or a trivial odd sector.
  Real symmetry, an involutive permutation, exact commutation, and sector lower
  bounds are explicit hypotheses. No covariance positivity hypothesis is needed.
- `parity_rayleigh_lower_bound` divides by the squared norm for a nonzero vector.
  `parity_of_sector_rayleigh_minima` supplies the requested inexpensive
  variational corollary: `e,o` are assumed `IsLeast` elements of the even/odd
  Rayleigh-value sets. Construction of eigenvalues, existence of these minima,
  and their identification with Mathlib eigenvalues are deferred.
- `parity_attenuation_lower_bound` proves
  $F_{\rm phys}\ge\min(1,B_{\rm par})$ for $0\le T\le1$, $n\ge0$, and
  $D_T=\sum Tn>0$. The proof uses division; the core parity theorem is homogeneous.
  `physicalFano_eq_identity_subtraction` proves that the implemented formula is
  exactly $1+y^T(A-I)y/D_T$. `binary_physicalFano_eq_rayleigh` proves equality
  with the Rayleigh quotient for binary masks, and `parity_binary_lower_bound`
  proves the stronger $B_{\rm par}$ floor.
- `shortened_bound_counterexample` checks the full parity hypotheses for
  $A=\left(\begin{smallmatrix}2&-1\\-1&2\end{smallmatrix}\right)$, $e=1<3=o$,
  and $y=(1,1)$. Here $y^TAy=2<4=((e+o)/2)\|y\|^2$. Thus the shortened
  average floor is false in general; the card's piecewise displayed formula
  already includes the necessary even-sector case.
- `partial_mask_counterexample` uses
  $A=\left(\begin{smallmatrix}3&2\\2&3\end{smallmatrix}\right)$,
  $n=(1,1)$, $T=(1/4,0)$: its sector values are $e=5,o=1$, so
  $F_{\rm phys}=3/2<B_{\rm par}=3$. This is an exact rational stand-in for the
  audit's partial-mask structure, not its floating-point Kerr matrix or a proof
  of a Kerr realization. These constants are exact formal identities, not
  numerical run results.

The [README](../../formal/README.md) maps all 35 theorem declarations to the
claim and identifies every external physical bridge. The proof explicitly
constructs the even/odd projections, proves the cross term vanishes, and proves
that nonnegative weights have odd energy at most their even energy.

## Build and axiom check

The supplied installation and cache were used unchanged. Lean and Mathlib are
both `v4.35.0-rc4`; the committed manifest pins Mathlib to
`1f414401f69059aa7eead47b53ee40bd38455eeb`. No toolchain installation, dependency
update, additional Mathlib checkout, or cache download was performed.

`export PATH=$HOME/.elan/bin:$PATH; cd formal; lake build` exited zero, with no
warnings. Build status lines from the clean build:

```text
ℹ [9020/9022] Built AnalyticalNL.Parity (4.2s)
✔ [9021/9022] Built AnalyticalNL (2.2s)
Build completed successfully (9022 jobs).
```

The intervening informational messages are the following `#print axioms` output
(the `info: file:line:column:` prefixes are omitted):

```text
'AnalyticalNL.parity_lower_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
'AnalyticalNL.parity_rayleigh_lower_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
'AnalyticalNL.parity_of_sector_rayleigh_minima' depends on axioms: [propext, Classical.choice, Quot.sound]
'AnalyticalNL.attenuation_lower_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
'AnalyticalNL.binary_lower_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
'AnalyticalNL.binary_physicalFano_eq_rayleigh' depends on axioms: [propext, Classical.choice, Quot.sound]
'AnalyticalNL.physicalFano_eq_identity_subtraction' depends on axioms: [propext, Classical.choice, Quot.sound]
'AnalyticalNL.parity_attenuation_lower_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
'AnalyticalNL.parity_binary_lower_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
'AnalyticalNL.shortened_bound_counterexample' depends on axioms: [propext, Classical.choice, Quot.sound]
'AnalyticalNL.partial_mask_counterexample' depends on axioms: [propext, Classical.choice, Quot.sound]
```

A separate temporary consumer importing `AnalyticalNL` printed the axioms of
**all 35 public theorems** and exited zero: every list was exactly
`[propext, Classical.choice, Quot.sound]`. This also checked public export
through the root module. A source scan found no proof holes, project axiom
declarations, `unsafe`, or `native_decide`. Every theorem name occurs in the
README map. `validate.py` and `check_generated.py origin/main` both report `ok`.
No `.lake` file is tracked. The unused template `Basic.lean` was removed.

## What is established, and what is not

Lean establishes the finite algebraic implications and both explicit scope
counterexamples. For the intended optical reading, it still assumes that `A`
is the correctly normalized linearized amplitude covariance, that the actual
dynamics and chosen bins obey exact reflection symmetry, that linearized
counting is valid, and that independent loss-port vacuum supplies the physical
attenuation formula. These assumptions are not new axioms: they are hypotheses
or the external interpretation of definitions.

No simulated covariance entries, empirical decay laws, quantum admissibility,
continuum limit, approximate-parity error, detector implementation, or physical
validity of linearization is certified. In particular, the main theorem does
not calculate sector minima or predict their dependence on nonlinear phase.

## Proposed card changes, for review on the claim branch

1. Replace the title's unconditional average by the piecewise floor
   $B_{\rm par}=\min(e,(e+o)/2)$; say the average applies when $o\le e$.
2. State the original quotient bound for nonnegative electronic weights, with
   denominator $\sum T_i^2n_i$, or for binary optical masks. For partial physical
   attenuation, state $F_{\rm phys}=1+y^T(A-I)y/D_T$ and the corrected floor
   $\min(1,B_{\rm par})$, with $0\le T_i\le1$ and $D_T>0$.
3. Retain exact real symmetry/commutation and canonical bin normalization as
   explicit mathematical hypotheses. Separate the physical covariance,
   linearization, and vacuum-loss assumptions from the matrix proof.
4. Update proof step 3 to name the electronic-weight quotient or binary mask;
   add the attenuation argument $0\le\|y\|^2\le D_T$.
5. Add a check-table link to this conditional Lean proof and its pinned source.
   Do not infer simulation verification, a new audit status, or promotion from
   it. Keep all numerical/scaling claims attached to their existing runs.

## Provenance and remaining work

Read-only inputs were the assessment's parity sections at PR #37,
`39e8586f1558c35ede6914f7cb9ff5026b15d9ed`; the claim card at PR #29,
`b771969d725b136585501c581350f965c8eb2433`; and candidate 3 plus the parity finding
in the audit at PR #34, `b0ec81427ee6fb9b789e3ec98793895acf61130a`.
The branch stacks on PR #37 and targets `main`. No literature novelty claim is
made. The session began at 2026-10-12 23:09:05 EDT, or 2026-10-13 03:09:05 UTC;
this note uses the requested UTC-date filename.

- **T-20261012-gpt-a-09:** pinned Lean CI and automatic axiom enforcement.
- **T-20261012-gpt-a-10:** construct sector minima and connect them to Mathlib
  eigenvalues; the conditional Rayleigh-minimum corollary is already proved.
- **T-20261012-gpt-a-11:** apply the proposed card wording after review.
- Existing **T-20261012-gpt-a-03** and **-04** remain the next assessment targets:
  differentiated conservation/centroid, then shear covariance and polarization.
- Existing **T-20261012-gpt-a-07** tracks certified covariance inputs and transfer
  errors; none are supplied by this pilot.
