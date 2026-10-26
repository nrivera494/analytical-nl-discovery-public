module

public import Mathlib

@[expose] public section

/-! # The actual Zakharov--Shabat bound-state problem

The spectral parameter is `ζ`; its imaginary part is the positive number η.
No spectral inequalities or endpoint asymptotics are built into this definition.
-/

open MeasureTheory Complex

namespace ZS

def SolvesZS (q : ℝ → ℂ) (ζ : ℂ) (v₁ v₂ : ℝ → ℂ) : Prop :=
  (∀ t, HasDerivAt v₁ (-I * ζ * v₁ t + q t * v₂ t) t) ∧
  (∀ t, HasDerivAt v₂ (-star (q t) * v₁ t + I * ζ * v₂ t) t)

/-- A discrete upper-half-plane eigenvalue is witnessed by an actual nonzero,
square-integrable solution of the ZS differential equation. -/
def IsEigenvalue (q : ℝ → ℂ) (ζ : ℂ) : Prop :=
  0 < ζ.im ∧ ∃ v₁ v₂ : ℝ → ℂ,
    SolvesZS q ζ v₁ v₂ ∧ MemLp v₁ 2 volume ∧ MemLp v₂ 2 volume ∧
    ∃ t, v₁ t ≠ 0 ∨ v₂ t ≠ 0

noncomputable def spinorMass (v₁ v₂ : ℝ → ℂ) (t : ℝ) : ℝ :=
  ‖v₁ t‖ ^ 2 + ‖v₂ t‖ ^ 2

noncomputable def polarization (v₁ v₂ : ℝ → ℂ) (t : ℝ) : ℝ :=
  (‖v₁ t‖ ^ 2 - ‖v₂ t‖ ^ 2) / spinorMass v₁ v₂ t

lemma component_one_derivative {q : ℝ → ℂ} {ζ : ℂ} {v₁ v₂ : ℝ → ℂ}
    (hv : SolvesZS q ζ v₁ v₂) (t : ℝ) :
    HasDerivAt (fun s => ‖v₁ s‖ ^ 2)
      (2 * ζ.im * ‖v₁ t‖ ^ 2 + 2 * (q t * v₂ t * star (v₁ t)).re) t := by
  convert (hv.1 t).norm_sq using 1
  simp [Complex.sq_norm, Complex.normSq_apply, real_inner_eq_re_inner, RCLike.inner_apply,
    Complex.mul_re, Complex.mul_im]
  ring

lemma component_two_derivative {q : ℝ → ℂ} {ζ : ℂ} {v₁ v₂ : ℝ → ℂ}
    (hv : SolvesZS q ζ v₁ v₂) (t : ℝ) :
    HasDerivAt (fun s => ‖v₂ s‖ ^ 2)
      (-2 * ζ.im * ‖v₂ t‖ ^ 2 - 2 * (q t * v₂ t * star (v₁ t)).re) t := by
  convert (hv.2 t).norm_sq using 1
  simp [Complex.sq_norm, Complex.normSq_apply, real_inner_eq_re_inner, RCLike.inner_apply,
    Complex.mul_re, Complex.mul_im]
  ring

lemma spinorMass_nonneg (v₁ v₂ : ℝ → ℂ) (t : ℝ) : 0 ≤ spinorMass v₁ v₂ t := by
  unfold spinorMass; positivity

lemma spinorMass_derivative {q : ℝ → ℂ} {ζ : ℂ} {v₁ v₂ : ℝ → ℂ}
    (hv : SolvesZS q ζ v₁ v₂) (t : ℝ) :
    HasDerivAt (spinorMass v₁ v₂) (2 * ζ.im * (‖v₁ t‖ ^ 2 - ‖v₂ t‖ ^ 2)) t := by
  convert (component_one_derivative hv t).add (component_two_derivative hv t) using 1
  · rfl
  · ring

lemma polarization_mem_Icc (v₁ v₂ : ℝ → ℂ) (t : ℝ)
    (h : 0 < spinorMass v₁ v₂ t) : polarization v₁ v₂ t ∈ Set.Icc (-1) 1 := by
  constructor
  · rw [polarization, le_div_iff₀ h]
    unfold spinorMass
    nlinarith [sq_nonneg ‖v₁ t‖]
  · rw [polarization, div_le_iff₀ h]
    unfold spinorMass
    nlinarith [sq_nonneg ‖v₂ t‖]

lemma polarization_derivative {q : ℝ → ℂ} {ζ : ℂ} {v₁ v₂ : ℝ → ℂ}
    (hv : SolvesZS q ζ v₁ v₂) (t : ℝ) (h : 0 < spinorMass v₁ v₂ t) :
    HasDerivAt (polarization v₁ v₂)
      (2 * ζ.im * (1 - polarization v₁ v₂ t ^ 2) +
        4 * (q t * v₂ t * star (v₁ t)).re / spinorMass v₁ v₂ t) t := by
  convert ((component_one_derivative hv t).sub (component_two_derivative hv t)).div
    (spinorMass_derivative hv t) (ne_of_gt h) using 1
  · rfl
  unfold polarization spinorMass
  have hn : ‖v₁ t‖ ^ 2 + ‖v₂ t‖ ^ 2 ≠ 0 := ne_of_gt h
  simp only [Pi.sub_apply]
  field_simp
  ring

lemma zero_of_derivative_bound {f f' : ℝ → ℝ} {K a : ℝ}
    (hd : ∀ t, HasDerivAt f (f' t) t) (hb : ∀ t, ‖f' t‖ ≤ K * ‖f t‖)
    (ha : f a = 0) (t : ℝ) : f t = 0 := by
  have hc : Continuous f := continuous_iff_continuousAt.mpr (fun x => (hd x).continuousAt)
  by_cases h : a ≤ t
  · exact eq_zero_of_abs_deriv_le_mul_abs_self_of_eq_zero_right hc.continuousOn
      (fun x _ => (hd x).hasDerivWithinAt) ha (fun x _ => hb x) t ⟨h, le_rfl⟩
  · have hd' : ∀ x, HasDerivAt (fun s => f (-s)) (-f' (-x)) x := by
      intro x
      simpa only [Function.comp_def, mul_neg_one] using (hd (-x)).comp x (hasDerivAt_neg x)
    have hb' : ∀ x, ‖-f' (-x)‖ ≤ K * ‖f (-x)‖ := by simpa using fun x => hb (-x)
    have he := eq_zero_of_abs_deriv_le_mul_abs_self_of_eq_zero_right
      (hc.comp continuous_neg).continuousOn (fun x _ => (hd' x).hasDerivWithinAt)
      (show f (-(-a)) = 0 by simpa using ha) (fun x _ => hb' x) (-t)
      (show -t ∈ Set.Icc (-a) (-t) by constructor <;> linarith)
    simpa using he

/-- Nonvanishing follows from the ODE and nontriviality; it is not assumed. -/
theorem spinorMass_pos {q : ℝ → ℂ} {ζ : ℂ} {v₁ v₂ : ℝ → ℂ}
    (hv : SolvesZS q ζ v₁ v₂) (hne : ∃ t, v₁ t ≠ 0 ∨ v₂ t ≠ 0) (t : ℝ) :
    0 < spinorMass v₁ v₂ t := by
  apply lt_of_le_of_ne (spinorMass_nonneg v₁ v₂ t)
  intro hz
  have hb : ∀ s, ‖2 * ζ.im * (‖v₁ s‖ ^ 2 - ‖v₂ s‖ ^ 2)‖ ≤
      (2 * |ζ.im|) * ‖spinorMass v₁ v₂ s‖ := by
    intro s
    have hab : |‖v₁ s‖ ^ 2 - ‖v₂ s‖ ^ 2| ≤ ‖v₁ s‖ ^ 2 + ‖v₂ s‖ ^ 2 := by
      apply abs_le.mpr; constructor <;> nlinarith [sq_nonneg ‖v₁ s‖, sq_nonneg ‖v₂ s‖]
    simp only [Real.norm_eq_abs, abs_mul, abs_of_nonneg (by norm_num : (0 : ℝ) ≤ 2),
      abs_of_nonneg (spinorMass_nonneg v₁ v₂ s)]
    exact mul_le_mul_of_nonneg_left hab (by positivity)
  obtain ⟨s, hs⟩ := hne
  have hs0 := zero_of_derivative_bound (spinorMass_derivative hv) hb hz.symm s
  have h1 : v₁ s = 0 := by
    have : ‖v₁ s‖ = 0 := by unfold spinorMass at hs0; nlinarith [sq_nonneg ‖v₂ s‖]
    exact norm_eq_zero.mp this
  have h2 : v₂ s = 0 := by
    have : ‖v₂ s‖ = 0 := by unfold spinorMass at hs0; nlinarith [sq_nonneg ‖v₁ s‖]
    exact norm_eq_zero.mp this
  exact hs.elim (fun h => h h1) (fun h => h h2)

lemma polarization_sqrt (v₁ v₂ : ℝ → ℂ) (t : ℝ)
    (h : 0 < spinorMass v₁ v₂ t) :
    Real.sqrt (1 - polarization v₁ v₂ t ^ 2) =
      2 * ‖v₁ t‖ * ‖v₂ t‖ / spinorMass v₁ v₂ t := by
  have he : 1 - polarization v₁ v₂ t ^ 2 =
      (2 * ‖v₁ t‖ * ‖v₂ t‖ / spinorMass v₁ v₂ t) ^ 2 := by
    unfold polarization spinorMass
    have hn : ‖v₁ t‖ ^ 2 + ‖v₂ t‖ ^ 2 ≠ 0 := ne_of_gt h
    field_simp
    ring
  rw [he, Real.sqrt_sq (by positivity)]

/-- The differential inequality on PDF page 60, derived from the complex ZS
equations without dividing by an individual spinor component. -/
theorem polarization_differential_inequality {q : ℝ → ℂ} {ζ : ℂ} {v₁ v₂ : ℝ → ℂ}
    (hv : SolvesZS q ζ v₁ v₂) (hne : ∃ t, v₁ t ≠ 0 ∨ v₂ t ≠ 0) (t : ℝ) :
    2 * ζ.im * (1 - polarization v₁ v₂ t ^ 2) -
        2 * ‖q t‖ * Real.sqrt (1 - polarization v₁ v₂ t ^ 2) ≤
      deriv (polarization v₁ v₂) t := by
  have hp := spinorMass_pos hv hne t
  rw [(polarization_derivative hv t hp).deriv, polarization_sqrt v₁ v₂ t hp]
  have hc : -(‖q t‖ * ‖v₂ t‖ * ‖v₁ t‖) ≤ (q t * v₂ t * star (v₁ t)).re := by
    have := neg_le_of_abs_le (Complex.abs_re_le_norm (q t * v₂ t * star (v₁ t)))
    simpa only [norm_mul, norm_star] using this
  have hdiv := (div_le_div_iff_of_pos_right hp).mpr (mul_le_mul_of_nonneg_left hc (by norm_num : (0 : ℝ) ≤ 4))
  ring_nf at hdiv ⊢
  linarith only [hdiv]

end ZS
