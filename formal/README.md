---
agent: gpt-a
model: gpt-6-astra
family: gpt
task: T-20261012-gpt-a-02
---

> **Libraries in this project** (index added by claude-interactive, claude-opus-5-5, family claude, task T-20261018-claude-interactive-04; the rest of this file is gpt-a's):
>
> | Library | Content | Formalizer | Used by |
> |---|---|---|---|
> | `AnalyticalNL` | Finite parity and readout algebra, described below | gpt-a (gpt) | cross-family check of C-20261010-claude-a-03; not yet a result |
> | [`ZSFormalization`](ZSFormalization/README.md) | Sharp even-moment Zakharov–Shabat eigenvalue bound, passive-mask ceiling, and integer-sech optimality | the PI's Codex session (GPT 6 Astra Max, family gpt; see [provenance](ZSFormalization/PROVENANCE.md)) | [R-0001](../results/formalized/R-0001-zs-even-moment-passive-mask-ceiling/RESULT.md) |
>
> `lake build` builds both. Results built on these libraries are under `results/formalized/` (rules in `docs/PROMOTION.md`, gate G8).

# AnalyticalNL: finite mathematical checks in Lean

This project kernel-checks finite-dimensional implications used by
analytical-nl-discovery. The first module,
[`AnalyticalNL/Parity.lean`](AnalyticalNL/Parity.lean), checks the piecewise parity
floor, its physical attenuation and binary-mask consequences, and two exact
rational counterexamples to overbroad statements. It is a cross-family
mathematical check of Claude-family claim **C-20261010-claude-a-03**. It does not
change the claim's status or establish the optical model.

## Build

From the repository root, with the PI-provided elan installation:

```sh
export PATH=$HOME/.elan/bin:$PATH
cd formal
lake exe cache get
lake build
```

The cache was already present for this pilot, so the session ran `lake build`
without downloading it again. Do not run `lake update` or replace `.lake` to
reproduce this version. `.lake` is ignored and is never committed. The root
`AnalyticalNL.lean` publicly imports the parity module. No placeholder module
remains.

- Lean toolchain: `leanprover/lean4:v4.35.0-rc4`.
- Mathlib tag: `v4.35.0-rc4`.
- Mathlib commit: `1f414401f69059aa7eead47b53ee40bd38455eeb`.
- Dependency revisions: committed `lake-manifest.json`.

The toolchain file and manifest are unchanged from the supplied scaffold and
are adopted into this project by gpt-a (`gpt-6-astra`, family `gpt`). The Lake
options retain Mathlib's standard linters except its copyright/license-header
style check, whose template this repository does not adopt. This does not
disable kernel checking. Each main theorem has a `#print axioms` check; all
report only `propext`, `Classical.choice`, and `Quot.sound`.

## Definitions and physical boundary

For a finite type `ι`, `sqNorm x = ∑ i, (x i)^2` and
`qform A x = xᵀ A x`. `reflect r x i = x (r i)`, with an involutive permutation
`r`. The main hypothesis `hcomm` is equality of the two matrix-vector actions
`A R` and `R A`, for every vector. `A.IsSymm` is real matrix symmetry.
Sector lower bounds are hypotheses and need not be attained. The homogeneous
bound includes zero vectors and empty or trivial sectors; the Rayleigh
corollaries require nonzero vectors.

```text
parityFloor e o = min e ((e + o) / 2)
maskVector n T i = T i * sqrt (n i)
transmitted n T = sum_i T i * n i
physicalFano A n T = 1 + (qform A y - sqNorm y) / transmitted n T
```

The physical theorem uses division and explicitly assumes a positive
transmitted mean. `physicalFano_eq_identity_subtraction` proves equality to
`1 + qform (A - I) y / transmitted n T`. Binary masks prove equality of the
transmitted mean and squared norm before dividing. General electronic weights
use the Rayleigh quotient and have no upper bound of one.

The external modelling bridges in the map below are:

- **A:** canonical finite-bin coordinates and identification of the supplied
  matrix as the linearized amplitude covariance, in shot-noise units.
- **P:** actual optical dynamics and retained bins have exact parity symmetry.
  Lean assumes and uses an involution and exact `hcomm`; it does not derive them
  from Kerr propagation or accept a small numerical commutator as equality.
- **C:** linearized counting makes `y = T sqrt(n)` the relevant direction;
  quadratic count corrections and validity at faint bins remain outside.
- **V:** independent loss-port vacuum gives the stated `physicalFano` formula.
  Lean proves consequences of that definition, not the quantum attenuation law.

All four physical bridges remain outside the proof. The last column identifies
which ones are needed for the indicated use; purely algebraic rows do not
independently assert a physics result. No Gaussianity, purity, positivity of `A`,
symplectic structure, coherent input, or propagation equation is needed for the
core mathematical implication.

## Theorem-to-claim map

Every theorem below is in namespace `AnalyticalNL` in `Parity.lean`. The claim
target for the parity and readout rows is C-20261010-claude-a-03; the final rows
formalize the assessment's scope correction and the audit's attenuation
counterexample structure.

| Lean theorem | Mathematical statement / role in the physics claim | External bridge |
|---|---|---|
| `sqNorm_nonneg` | Nonnegative counting-direction energy. | A, C for interpretation |
| `sqNorm_reflect` | Reflection preserves squared norm. | A, P |
| `dotProduct_reflect` | Reflection preserves the real dot product. | A, P |
| `evenPart_even` | The even projection lies in the even sector. | P |
| `oddPart_odd` | The odd projection lies in the odd sector. | P |
| `evenPart_add_oddPart` | The projections reconstruct the original readout. | P, C |
| `even_odd_orthogonal` | Even and odd readouts are orthogonal. | A, P |
| `parity_energy_split` | Total energy is the sum of sector energies. | A, P, C |
| `parity_energy_difference` | Even minus odd energy equals the reflection overlap. | A, P, C |
| `odd_energy_le_even` | Nonnegative weights put at most half their energy in the odd sector. | A, P, C |
| `even_odd_covariance_zero` | Exact commutation eliminates the even–odd covariance term. | A, P |
| `parity_qform_split` | The total variance splits into sector variances. | A, P, C |
| `parity_lower_bound` | `min(e,(e+o)/2) * ‖y‖² ≤ yᵀAy` for `y ≥ 0`. | A, P, C |
| `sqNorm_eq_zero_iff` | Zero squared norm is exactly the zero vector. | A for norm interpretation |
| `sqNorm_pos` | A nonzero readout has a positive Rayleigh denominator. | A, C |
| `parity_rayleigh_lower_bound` | Nonnegative electronic weights obey the parity floor. | A, P, C |
| `maskVector_nonneg` | Nonnegative transmissions give a nonnegative counting direction. | A, C |
| `maskVector_sqNorm` | `‖T sqrt(n)‖² = ∑ T² n`. | A, C |
| `maskVector_sqNorm_le_transmitted` | `∑ T² n ≤ ∑ T n` for `0 ≤ T ≤ 1`. | A, C |
| `attenuation_lower_bound` | Any nonnegative-weight floor `B` gives physical floor `min(1,B)`. | A, C, V |
| `binary_sqNorm_eq_transmitted` | Binary masks equate the two denominators. | A, C |
| `binary_physicalFano_eq_rayleigh` | Binary physical Fano factor equals the Rayleigh quotient. | A, C, V |
| `binary_lower_bound` | Binary physical masks retain any nonnegative-weight floor `B`. | A, C, V |
| `parity_attenuation_lower_bound` | Arbitrary physical attenuation obeys `min(1,Bpar)`. | A, P, C, V |
| `parity_binary_lower_bound` | Binary physical masks obey `Bpar`, including when it exceeds one. | A, P, C, V |
| `physicalFano_eq_identity_subtraction` | The implemented formula is exactly `1 + yᵀ(A-I)y/D`. | A, C, V |
| `sector_lower_bound_of_rayleigh_minimum` | An assumed sector Rayleigh minimum supplies a sector lower bound. | A; existence of the minimum is a hypothesis |
| `parity_of_sector_rayleigh_minima` | The parity floor with `e,o` assumed to be sector Rayleigh minima. | A, P, C; minima are hypotheses |
| `twoBinReflection_involutive` | Swapping two bins is an involution. | Algebraic example only |
| `twoBinMatrix_symmetric` | `[[a,b],[b,a]]` is symmetric. | Algebraic example only |
| `twoBinMatrix_commutes` | This matrix commutes exactly with the bin swap. | Algebraic example only |
| `twoBin_even_qform` | Its even-sector quotient is `a+b`. | Algebraic example only |
| `twoBin_odd_qform` | Its odd-sector quotient is `a-b`. | Algebraic example only |
| `shortened_bound_counterexample` | `[[2,-1],[-1,2]]`, `e=1<3=o`, `y=[1,1]` refute the unqualified average floor. | Exact algebra; no particular fiber realization asserted |
| `partial_mask_counterexample` | `[[3,2],[2,3]]`, `n=[1,1]`, `T=[1/4,0]` give `Fphys=3/2 < Bpar=3`. | A, C, V for a physical reading; rational stand-in, not a certified Kerr covariance |

The variational corollary does not prove existence of sector minima or identify
them with Mathlib eigenvalues. In particular, `IsLeast` cannot hold for an empty
odd-sector Rayleigh set. The main lower-bound theorem needs no such existence
assumption. That spectral bridge is tracked separately.

See the [pilot note](../docs/lean/2026-10-13-gpt-a-parity-pilot.md) for the checked
build and axiom output, proposed card changes, source revisions, and follow-up
tasks. The proof does not certify simulated covariance entries, discretization,
approximate parity, continuum limits, empirical scaling laws, or laboratory
model validity.
