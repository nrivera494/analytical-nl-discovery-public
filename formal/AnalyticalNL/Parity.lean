module

public import Mathlib

/-!
# Finite-bin parity and attenuation bounds

Agent: gpt-a. Model: gpt-6-astra. Family: gpt.
Task: T-20261012-gpt-a-02.

The matrix is supplied as data. Its interpretation as a linearized amplitude
covariance, exact physical reflection symmetry, linearized counting, and the
loss-port vacuum model are not derived here.
-/

@[expose] public section

noncomputable section

namespace AnalyticalNL

open scoped BigOperators

variable {ι : Type*} [Fintype ι]

/-- Euclidean squared norm in canonical finite-bin coordinates. -/
def sqNorm (x : ι → ℝ) : ℝ := ∑ i, (x i) ^ 2

/-- The real quadratic form `xᵀ A x`. -/
def qform (A : Matrix ι ι ℝ) (x : ι → ℝ) : ℝ := x ⬝ᵥ A.mulVec x

/-- Reflection acts by permuting the vector coordinates. -/
def reflect (r : Equiv.Perm ι) (x : ι → ℝ) : ι → ℝ := fun i => x (r i)

def evenPart (r : Equiv.Perm ι) (x : ι → ℝ) : ι → ℝ :=
  fun i => (x i + x (r i)) / 2

def oddPart (r : Equiv.Perm ι) (x : ι → ℝ) : ι → ℝ :=
  fun i => (x i - x (r i)) / 2

/-- Both sector orderings are retained. -/
def parityFloor (e o : ℝ) : ℝ := min e ((e + o) / 2)

theorem sqNorm_nonneg (x : ι → ℝ) : 0 ≤ sqNorm x :=
  Finset.sum_nonneg fun i _ => sq_nonneg (x i)

theorem sqNorm_reflect (r : Equiv.Perm ι) (x : ι → ℝ) :
    sqNorm (reflect r x) = sqNorm x := Equiv.sum_comp r (fun i => (x i) ^ 2)

theorem dotProduct_reflect (r : Equiv.Perm ι) (x z : ι → ℝ) :
    reflect r x ⬝ᵥ reflect r z = x ⬝ᵥ z :=
  Equiv.sum_comp r (fun i => x i * z i)

omit [Fintype ι] in
theorem evenPart_even (r : Equiv.Perm ι) (hr : Function.Involutive r) (x : ι → ℝ) :
    reflect r (evenPart r x) = evenPart r x := by
  funext i
  simp only [reflect, evenPart, hr i]
  ring

omit [Fintype ι] in
theorem oddPart_odd (r : Equiv.Perm ι) (hr : Function.Involutive r) (x : ι → ℝ) :
    reflect r (oddPart r x) = -oddPart r x := by
  funext i
  simp only [reflect, oddPart, hr i, Pi.neg_apply]
  ring

omit [Fintype ι] in
theorem evenPart_add_oddPart (r : Equiv.Perm ι) (x : ι → ℝ) :
    evenPart r x + oddPart r x = x := by
  funext i
  simp only [evenPart, oddPart, Pi.add_apply]
  ring

theorem even_odd_orthogonal (r : Equiv.Perm ι) (x z : ι → ℝ)
    (hx : reflect r x = x) (hz : reflect r z = -z) : x ⬝ᵥ z = 0 := by
  have h := dotProduct_reflect r x z
  rw [hx, hz, dotProduct_neg] at h
  linarith

theorem parity_energy_split (r : Equiv.Perm ι) (x : ι → ℝ) :
    sqNorm (evenPart r x) + sqNorm (oddPart r x) = sqNorm x := by
  calc
    _ = ∑ i, ((evenPart r x i) ^ 2 + (oddPart r x i) ^ 2) :=
      Finset.sum_add_distrib.symm
    _ = ∑ i, ((x i) ^ 2 + (x (r i)) ^ 2) / 2 := by
      apply Finset.sum_congr rfl
      intro i _
      dsimp [evenPart, oddPart]
      ring
    _ = (sqNorm x + sqNorm (reflect r x)) / 2 := by
      simp only [sqNorm, reflect, ← Finset.sum_div, Finset.sum_add_distrib]
    _ = sqNorm x := by rw [sqNorm_reflect]; ring

theorem parity_energy_difference (r : Equiv.Perm ι) (x : ι → ℝ) :
    sqNorm (evenPart r x) - sqNorm (oddPart r x) = x ⬝ᵥ reflect r x := by
  rw [sqNorm, sqNorm, ← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro i _
  dsimp [evenPart, oddPart, reflect]
  ring

theorem odd_energy_le_even (r : Equiv.Perm ι) (y : ι → ℝ) (hy : ∀ i, 0 ≤ y i) :
    sqNorm (oddPart r y) ≤ sqNorm (evenPart r y) := by
  have h : 0 ≤ y ⬝ᵥ reflect r y :=
    Finset.sum_nonneg fun i _ => mul_nonneg (hy i) (hy (r i))
  rw [← parity_energy_difference] at h
  linarith

theorem even_odd_covariance_zero (r : Equiv.Perm ι) (A : Matrix ι ι ℝ)
    (hcomm : ∀ x, A.mulVec (reflect r x) = reflect r (A.mulVec x))
    (x z : ι → ℝ) (hx : reflect r x = x) (hz : reflect r z = -z) :
    x ⬝ᵥ A.mulVec z = 0 := by
  apply even_odd_orthogonal r x (A.mulVec z) hx
  rw [← hcomm, hz, Matrix.mulVec_neg]

theorem parity_qform_split (r : Equiv.Perm ι) (hr : Function.Involutive r)
    (A : Matrix ι ι ℝ) (hA : A.IsSymm)
    (hcomm : ∀ x, A.mulVec (reflect r x) = reflect r (A.mulVec x))
    (y : ι → ℝ) :
    qform A y = qform A (evenPart r y) + qform A (oddPart r y) := by
  have hcross := even_odd_covariance_zero r A hcomm (evenPart r y) (oddPart r y)
    (evenPart_even r hr y) (oddPart_odd r hr y)
  have hcross' : oddPart r y ⬝ᵥ A.mulVec (evenPart r y) = 0 := by
    rw [hA.dotProduct_mulVec_comm, hcross]
  calc
    qform A y = qform A (evenPart r y + oddPart r y) := by
      rw [evenPart_add_oddPart]
    _ = _ := by
      simp [qform, Matrix.mulVec_add, add_dotProduct, dotProduct_add, hcross, hcross']

/-- The piecewise parity floor for every entrywise non-negative vector,
including zero. Sector bounds are hypotheses, not enumerated eigenvalues. -/
theorem parity_lower_bound
    (r : Equiv.Perm ι) (hr : Function.Involutive r)
    (A : Matrix ι ι ℝ) (hA : A.IsSymm)
    (hcomm : ∀ x, A.mulVec (reflect r x) = reflect r (A.mulVec x))
    (e o : ℝ)
    (he : ∀ x, reflect r x = x → e * sqNorm x ≤ qform A x)
    (ho : ∀ x, reflect r x = -x → o * sqNorm x ≤ qform A x)
    (y : ι → ℝ) (hy : ∀ i, 0 ≤ y i) :
    parityFloor e o * sqNorm y ≤ qform A y := by
  have he' := he (evenPart r y) (evenPart_even r hr y)
  have ho' := ho (oddPart r y) (oddPart_odd r hr y)
  have hs := parity_energy_split r y
  have hd := odd_energy_le_even r y hy
  have hn := sqNorm_nonneg (oddPart r y)
  have hb₁ : parityFloor e o ≤ e := min_le_left _ _
  have hb₂ : parityFloor e o ≤ (e + o) / 2 := min_le_right _ _
  have hp₁ := mul_nonneg (sub_nonneg.mpr hb₁) (sub_nonneg.mpr hd)
  have hp₂ := mul_nonneg (show 0 ≤ e + o - 2 * parityFloor e o by linarith) hn
  rw [parity_qform_split r hr A hA hcomm y, ← hs]
  nlinarith

theorem sqNorm_eq_zero_iff (x : ι → ℝ) : sqNorm x = 0 ↔ x = 0 := by
  constructor
  · intro h
    funext i
    have hi : (x i) ^ 2 ≤ sqNorm x :=
      Finset.single_le_sum (fun j _ => sq_nonneg (x j)) (Finset.mem_univ i)
    change x i = 0
    nlinarith [sq_nonneg (x i)]
  · intro h
    simp [sqNorm, h]

theorem sqNorm_pos (x : ι → ℝ) (hx : x ≠ 0) : 0 < sqNorm x := by
  exact lt_of_le_of_ne (sqNorm_nonneg x) (Ne.symm (mt (sqNorm_eq_zero_iff x).mp hx))

/-- The electronic-weight Rayleigh quotient; no upper bound on weights is needed. -/
theorem parity_rayleigh_lower_bound
    (r : Equiv.Perm ι) (hr : Function.Involutive r)
    (A : Matrix ι ι ℝ) (hA : A.IsSymm)
    (hcomm : ∀ x, A.mulVec (reflect r x) = reflect r (A.mulVec x))
    (e o : ℝ)
    (he : ∀ x, reflect r x = x → e * sqNorm x ≤ qform A x)
    (ho : ∀ x, reflect r x = -x → o * sqNorm x ≤ qform A x)
    (y : ι → ℝ) (hy : ∀ i, 0 ≤ y i) (hy0 : y ≠ 0) :
    parityFloor e o ≤ qform A y / sqNorm y := by
  exact (le_div_iff₀ (sqNorm_pos y hy0)).mpr
    (parity_lower_bound r hr A hA hcomm e o he ho y hy)

/-- Intensity transmission multiplies the amplitude-counting direction by `T`,
not by its square root. -/
def maskVector (n T : ι → ℝ) : ι → ℝ := fun i => T i * Real.sqrt (n i)

def transmitted (n T : ι → ℝ) : ℝ := ∑ i, T i * n i

/-- The linearized loss-port-vacuum formula, supplied as the physical model. -/
def physicalFano (A : Matrix ι ι ℝ) (n T : ι → ℝ) : ℝ :=
  1 + (qform A (maskVector n T) - sqNorm (maskVector n T)) / transmitted n T

omit [Fintype ι] in
theorem maskVector_nonneg (n T : ι → ℝ) (hT : ∀ i, 0 ≤ T i) :
    ∀ i, 0 ≤ maskVector n T i :=
  fun i => mul_nonneg (hT i) (Real.sqrt_nonneg _)

theorem maskVector_sqNorm (n T : ι → ℝ) (hn : ∀ i, 0 ≤ n i) :
    sqNorm (maskVector n T) = ∑ i, (T i) ^ 2 * n i := by
  unfold sqNorm maskVector
  apply Finset.sum_congr rfl
  intro i _
  rw [mul_pow, Real.sq_sqrt (hn i)]

theorem maskVector_sqNorm_le_transmitted (n T : ι → ℝ)
    (hn : ∀ i, 0 ≤ n i) (hT : ∀ i, 0 ≤ T i ∧ T i ≤ 1) :
    sqNorm (maskVector n T) ≤ transmitted n T := by
  rw [maskVector_sqNorm n T hn]
  apply Finset.sum_le_sum
  intro i _
  have ht : (T i) ^ 2 ≤ T i := by nlinarith [(hT i).1, (hT i).2]
  exact mul_le_mul_of_nonneg_right ht (hn i)

/-- Any floor on non-negative counting directions gives the vacuum-corrected
physical floor `min 1 B`. This theorem is independent of parity. -/
theorem attenuation_lower_bound
    (A : Matrix ι ι ℝ) (n T : ι → ℝ) (B : ℝ)
    (hn : ∀ i, 0 ≤ n i)
    (hT : ∀ i, 0 ≤ T i ∧ T i ≤ 1)
    (hden : 0 < transmitted n T)
    (hB : ∀ y : ι → ℝ, (∀ i, 0 ≤ y i) → B * sqNorm y ≤ qform A y) :
    min 1 B ≤ physicalFano A n T := by
  have hq := hB (maskVector n T) (maskVector_nonneg n T fun i => (hT i).1)
  have hs := sqNorm_nonneg (maskVector n T)
  have hsd := maskVector_sqNorm_le_transmitted n T hn hT
  have hb₁ : min 1 B ≤ 1 := min_le_left _ _
  have hb₂ : min 1 B ≤ B := min_le_right _ _
  have hp₁ := mul_nonneg (sub_nonneg.mpr hb₂) hs
  have hp₂ := mul_nonneg (sub_nonneg.mpr hb₁) (sub_nonneg.mpr hsd)
  unfold physicalFano
  rw [← sub_le_iff_le_add', le_div_iff₀ hden]
  nlinarith

theorem binary_sqNorm_eq_transmitted (n T : ι → ℝ)
    (hn : ∀ i, 0 ≤ n i) (hT : ∀ i, T i = 0 ∨ T i = 1) :
    sqNorm (maskVector n T) = transmitted n T := by
  rw [maskVector_sqNorm n T hn]
  apply Finset.sum_congr rfl
  intro i _
  rcases hT i with h | h <;> simp [h]

/-- Binary masks have the electronic-weight denominator exactly. -/
theorem binary_physicalFano_eq_rayleigh
    (A : Matrix ι ι ℝ) (n T : ι → ℝ)
    (hn : ∀ i, 0 ≤ n i) (hT : ∀ i, T i = 0 ∨ T i = 1)
    (hden : 0 < transmitted n T) :
    physicalFano A n T = qform A (maskVector n T) / sqNorm (maskVector n T) := by
  unfold physicalFano
  rw [binary_sqNorm_eq_transmitted n T hn hT]
  field_simp
  ring

/-- The stronger floor survives binary physical masks even when it exceeds one. -/
theorem binary_lower_bound
    (A : Matrix ι ι ℝ) (n T : ι → ℝ) (B : ℝ)
    (hn : ∀ i, 0 ≤ n i) (hT : ∀ i, T i = 0 ∨ T i = 1)
    (hden : 0 < transmitted n T)
    (hB : ∀ y : ι → ℝ, (∀ i, 0 ≤ y i) → B * sqNorm y ≤ qform A y) :
    B ≤ physicalFano A n T := by
  have hT0 : ∀ i, 0 ≤ T i := by intro i; rcases hT i with h | h <;> simp [h]
  have hs : 0 < sqNorm (maskVector n T) := by
    rw [binary_sqNorm_eq_transmitted n T hn hT]
    exact hden
  rw [binary_physicalFano_eq_rayleigh A n T hn hT hden, le_div_iff₀ hs]
  exact hB _ (maskVector_nonneg n T hT0)

/-- Parity specialized to physical partial attenuation. -/
theorem parity_attenuation_lower_bound
    (r : Equiv.Perm ι) (hr : Function.Involutive r)
    (A : Matrix ι ι ℝ) (hA : A.IsSymm)
    (hcomm : ∀ x, A.mulVec (reflect r x) = reflect r (A.mulVec x))
    (e o : ℝ)
    (he : ∀ x, reflect r x = x → e * sqNorm x ≤ qform A x)
    (ho : ∀ x, reflect r x = -x → o * sqNorm x ≤ qform A x)
    (n T : ι → ℝ) (hn : ∀ i, 0 ≤ n i)
    (hT : ∀ i, 0 ≤ T i ∧ T i ≤ 1) (hden : 0 < transmitted n T) :
    min 1 (parityFloor e o) ≤ physicalFano A n T :=
  attenuation_lower_bound A n T (parityFloor e o) hn hT hden
    (parity_lower_bound r hr A hA hcomm e o he ho)

/-- Parity specialized to binary physical attenuation. -/
theorem parity_binary_lower_bound
    (r : Equiv.Perm ι) (hr : Function.Involutive r)
    (A : Matrix ι ι ℝ) (hA : A.IsSymm)
    (hcomm : ∀ x, A.mulVec (reflect r x) = reflect r (A.mulVec x))
    (e o : ℝ)
    (he : ∀ x, reflect r x = x → e * sqNorm x ≤ qform A x)
    (ho : ∀ x, reflect r x = -x → o * sqNorm x ≤ qform A x)
    (n T : ι → ℝ) (hn : ∀ i, 0 ≤ n i)
    (hT : ∀ i, T i = 0 ∨ T i = 1) (hden : 0 < transmitted n T) :
    parityFloor e o ≤ physicalFano A n T :=
  binary_lower_bound A n T (parityFloor e o) hn hT hden
    (parity_lower_bound r hr A hA hcomm e o he ho)

/-- The definition really is `1 + yᵀ (A - I) y / D`. -/
theorem physicalFano_eq_identity_subtraction [DecidableEq ι]
    (A : Matrix ι ι ℝ) (n T : ι → ℝ) :
    physicalFano A n T =
      1 + qform (A - 1) (maskVector n T) / transmitted n T := by
  simp [physicalFano, qform, Matrix.sub_mulVec, sqNorm, dotProduct, pow_two,
    mul_sub, Finset.sum_sub_distrib]

/-- Rayleigh values on a sector specified by a predicate. Empty sectors have no
minimum; the `IsLeast` hypotheses below explicitly rule them out. -/
def sectorRayleighValues (A : Matrix ι ι ℝ) (sector : (ι → ℝ) → Prop) : Set ℝ :=
  {v | ∃ x, sector x ∧ x ≠ 0 ∧ qform A x / sqNorm x = v}

theorem sector_lower_bound_of_rayleigh_minimum
    (A : Matrix ι ι ℝ) (sector : (ι → ℝ) → Prop) (m : ℝ)
    (hm : IsLeast (sectorRayleighValues A sector) m) :
    ∀ x, sector x → m * sqNorm x ≤ qform A x := by
  intro x hx
  by_cases hx0 : x = 0
  · simp [hx0, sqNorm, qform]
  · exact (le_div_iff₀ (sqNorm_pos x hx0)).mp (hm.2 ⟨x, hx, hx0, rfl⟩)

/-- Variational sector-minimum corollary. It assumes minima of the sector
Rayleigh quotients; it does not construct or enumerate an eigensystem. -/
theorem parity_of_sector_rayleigh_minima
    (r : Equiv.Perm ι) (hr : Function.Involutive r)
    (A : Matrix ι ι ℝ) (hA : A.IsSymm)
    (hcomm : ∀ x, A.mulVec (reflect r x) = reflect r (A.mulVec x))
    (e o : ℝ)
    (he : IsLeast (sectorRayleighValues A (fun x => reflect r x = x)) e)
    (ho : IsLeast (sectorRayleighValues A (fun x => reflect r x = -x)) o)
    (y : ι → ℝ) (hy : ∀ i, 0 ≤ y i) (hy0 : y ≠ 0) :
    parityFloor e o ≤ qform A y / sqNorm y :=
  parity_rayleigh_lower_bound r hr A hA hcomm e o
    (sector_lower_bound_of_rayleigh_minimum A _ e he)
    (sector_lower_bound_of_rayleigh_minimum A _ o ho) y hy hy0

/-! ## Exact rational counterexamples in two bins -/

def twoBinReflection : Equiv.Perm (Fin 2) := Equiv.swap 0 1

def twoBinMatrix (a b : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![a, b; b, a]

theorem twoBinReflection_involutive : Function.Involutive twoBinReflection := by
  intro i
  fin_cases i <;> norm_num [twoBinReflection]

theorem twoBinMatrix_symmetric (a b : ℝ) : (twoBinMatrix a b).IsSymm := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

theorem twoBinMatrix_commutes (a b : ℝ) (x : Fin 2 → ℝ) :
    (twoBinMatrix a b).mulVec (reflect twoBinReflection x) =
      reflect twoBinReflection ((twoBinMatrix a b).mulVec x) := by
  ext i
  fin_cases i <;>
    simp [twoBinMatrix, twoBinReflection, reflect, Matrix.mulVec, dotProduct,
      Fin.sum_univ_two] <;> ring

theorem twoBin_even_qform (a b : ℝ) (x : Fin 2 → ℝ)
    (hx : reflect twoBinReflection x = x) :
    qform (twoBinMatrix a b) x = (a + b) * sqNorm x := by
  have h : x 1 = x 0 := by simpa [reflect, twoBinReflection] using congrFun hx 0
  simp [qform, sqNorm, twoBinMatrix, Matrix.mulVec, dotProduct, Fin.sum_univ_two, h]
  ring

theorem twoBin_odd_qform (a b : ℝ) (x : Fin 2 → ℝ)
    (hx : reflect twoBinReflection x = -x) :
    qform (twoBinMatrix a b) x = (a - b) * sqNorm x := by
  have h : x 1 = -x 0 := by simpa [reflect, twoBinReflection] using congrFun hx 0
  simp [qform, sqNorm, twoBinMatrix, Matrix.mulVec, dotProduct, Fin.sum_univ_two, h]
  ring

/-- For `A = [[2,-1],[-1,2]]`, `e = 1 < 3 = o` and `y = [1,1]`,
all parity hypotheses hold but the shortened average floor fails. -/
theorem shortened_bound_counterexample :
    let A := twoBinMatrix 2 (-1)
    let y : Fin 2 → ℝ := ![1, 1]
    Function.Involutive twoBinReflection ∧ A.IsSymm ∧
    (∀ x, A.mulVec (reflect twoBinReflection x) = reflect twoBinReflection (A.mulVec x)) ∧
    (∀ x, reflect twoBinReflection x = x → qform A x = 1 * sqNorm x) ∧
    (∀ x, reflect twoBinReflection x = -x → qform A x = 3 * sqNorm x) ∧
    (1 : ℝ) < 3 ∧ (∀ i, 0 ≤ y i) ∧ y ≠ 0 ∧
    qform A y < ((1 + 3 : ℝ) / 2) * sqNorm y := by
  dsimp only
  refine ⟨twoBinReflection_involutive, twoBinMatrix_symmetric _ _,
    twoBinMatrix_commutes _ _, ?_, ?_, by norm_num, ?_, ?_, ?_⟩
  · intro x hx
    have h := twoBin_even_qform 2 (-1) x hx
    norm_num at h ⊢
    exact h
  · intro x hx
    have h := twoBin_odd_qform 2 (-1) x hx
    norm_num at h ⊢
    exact h
  · intro i; fin_cases i <;> norm_num
  · intro h
    have := congrFun h 0
    norm_num at this
  · norm_num [qform, sqNorm, twoBinMatrix, Matrix.mulVec, dotProduct, Fin.sum_univ_two]

/-- Rational stand-in for the audit's partial-mask failure: `A = [[3,2],[2,3]]`,
`n = [1,1]`, `T = [1/4,0]`. The parity floor is three but the physical Fano
factor is `3/2`. No Kerr realization of this exact matrix is asserted. -/
theorem partial_mask_counterexample :
    let A := twoBinMatrix 3 2
    let n : Fin 2 → ℝ := ![1, 1]
    let T : Fin 2 → ℝ := ![1 / 4, 0]
    Function.Involutive twoBinReflection ∧ A.IsSymm ∧
    (∀ x, A.mulVec (reflect twoBinReflection x) = reflect twoBinReflection (A.mulVec x)) ∧
    (∀ x, reflect twoBinReflection x = x → qform A x = 5 * sqNorm x) ∧
    (∀ x, reflect twoBinReflection x = -x → qform A x = 1 * sqNorm x) ∧
    (∀ i, 0 ≤ n i) ∧ (∀ i, 0 ≤ T i ∧ T i ≤ 1) ∧
    0 < transmitted n T ∧ 1 < parityFloor 5 1 ∧
    physicalFano A n T = 3 / 2 ∧ physicalFano A n T < parityFloor 5 1 := by
  dsimp only
  refine ⟨twoBinReflection_involutive, twoBinMatrix_symmetric _ _,
    twoBinMatrix_commutes _ _, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro x hx
    have h := twoBin_even_qform 3 2 x hx
    norm_num at h ⊢
    exact h
  · intro x hx
    have h := twoBin_odd_qform 3 2 x hx
    norm_num at h ⊢
    exact h
  · intro i; fin_cases i <;> norm_num
  · intro i; fin_cases i <;> norm_num
  · norm_num [transmitted, Fin.sum_univ_two]
  · norm_num [parityFloor]
  · norm_num [physicalFano, qform, sqNorm, maskVector, transmitted, twoBinMatrix,
      Matrix.mulVec, dotProduct, Fin.sum_univ_two]
  · norm_num [physicalFano, qform, sqNorm, maskVector, transmitted, twoBinMatrix,
      Matrix.mulVec, dotProduct, Fin.sum_univ_two, parityFloor]

#print axioms parity_lower_bound
#print axioms parity_rayleigh_lower_bound
#print axioms parity_of_sector_rayleigh_minima
#print axioms attenuation_lower_bound
#print axioms binary_lower_bound
#print axioms binary_physicalFano_eq_rayleigh
#print axioms physicalFano_eq_identity_subtraction
#print axioms parity_attenuation_lower_bound
#print axioms parity_binary_lower_bound
#print axioms shortened_bound_counterexample
#print axioms partial_mask_counterexample

end AnalyticalNL
