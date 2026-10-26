module

public import ZSFormalization.SechSharpness

@[expose] public section

/-! # Attained optimality and exact rational certificates -/

open MeasureTheory FourierTransform Set
open scoped SchwartzMap

namespace ZS

def attainableHeights (g : 𝓢(ℝ, ℂ)) : Set ℝ :=
  {η | ∃ (f : 𝓢(ℝ, ℂ)) (m : ℝ → ℂ) (ζ : ℂ),
    (∀ ξ, ‖m ξ‖ ≤ 1) ∧ (∀ ξ, f ξ = m ξ * g ξ) ∧
    IsEigenvalue (𝓕⁻ f : 𝓢(ℝ, ℂ)) ζ ∧ ζ.im = η}

/-- This is an attained optimum, not only an upper bound or a formal `sSup`. -/
theorem integer_sech_optimality (k : ℕ) {g : 𝓢(ℝ, ℂ)}
    (hs : IsSechSource (k + 1 : ℝ) g) :
    IsGreatest (attainableHeights g) ((k + 1 : ℝ) - 1 / 2) := by
  constructor
  · refine ⟨g, (fun _ => 1), Complex.I * (((k + 1 : ℝ) - 1 / 2 : ℝ) : ℂ), ?_, ?_,
      integer_sech_source_attains k hs, ?_⟩
    · intro ξ; simp
    · intro ξ; simp
    · simp
  · rintro η ⟨f, m, ζ, hm, hf, hz, rfl⟩
    exact integer_sech_source_ceiling k hs m hm hf hz

noncomputable def sourceEnergy (g : 𝓢(ℝ, ℂ)) : ℝ := ∫ t, ‖𝓕⁻ g t‖ ^ 2

theorem sech_source_energy {N : ℝ} (hN : 0 ≤ N) {g : 𝓢(ℝ, ℂ)}
    (hs : IsSechSource N g) : sourceEnergy g = 2 * N ^ 2 := by
  have hn : ∀ t, ‖𝓕⁻ g t‖ = N * sech t := by
    intro t
    rw [hs.2, Complex.norm_real, Real.norm_eq_abs, abs_of_nonneg (mul_nonneg hN (sech_pos t).le)]
  unfold sourceEnergy
  simp_rw [hn, mul_pow]
  rw [integral_const_mul]
  have hi := sech_even_moment 0
  norm_num at hi
  rw [hi]
  ring

def attainableFractions (g : 𝓢(ℝ, ℂ)) : Set ℝ :=
  {y | ∃ η ∈ attainableHeights g, y = 4 * η / sourceEnergy g}

theorem integer_sech_fraction_optimality (k : ℕ) {g : 𝓢(ℝ, ℂ)}
    (hs : IsSechSource (k + 1 : ℝ) g) :
    IsGreatest (attainableFractions g) ((2 * (k + 1 : ℝ) - 1) / (k + 1 : ℝ) ^ 2) := by
  have he := sech_source_energy (by positivity) hs
  have hpos : 0 < sourceEnergy g := by rw [he]; positivity
  have hmax := integer_sech_optimality k hs
  have heq : 4 * ((k + 1 : ℝ) - 1 / 2) / sourceEnergy g =
      (2 * (k + 1 : ℝ) - 1) / (k + 1 : ℝ) ^ 2 := by
    rw [he]
    have hk : (k + 1 : ℝ) ≠ 0 := by positivity
    field_simp
    ring
  constructor
  · exact ⟨_, hmax.1, heq.symm⟩
  · rintro y ⟨η, hη, rfl⟩
    rw [← heq]
    exact div_le_div_of_nonneg_right (mul_le_mul_of_nonneg_left (hmax.2 hη) (by norm_num)) hpos.le

theorem order_four_fraction_optimum {g : 𝓢(ℝ, ℂ)} (hs : IsSechSource 4 g) :
    IsGreatest (attainableFractions g) (7 / 16 : ℝ) := by
  have h := integer_sech_fraction_optimality 3 (g := g) (by norm_num; exact hs)
  norm_num at h
  exact h

/-- Rational upper bounds can be certified by exact polynomial arithmetic. -/
theorem rational_sech_ceiling (k : ℕ) {N U : ℝ} (hN : 0 ≤ N) (hU : 0 ≤ U)
    (hcert : 2 * (2 * k + 1 : ℝ) ^ (2 * k + 1) * N ^ (2 * k + 2) ≤
      (2 * k + 2 : ℝ) ^ (2 * k + 2) * U ^ (2 * k + 1))
    {f g : 𝓢(ℝ, ℂ)} (hs : IsSechSource N g) (m : ℝ → ℂ)
    (hm : ∀ ξ, ‖m ξ‖ ≤ 1) (hf : ∀ ξ, f ξ = m ξ * g ξ)
    {ζ : ℂ} (hz : IsEigenvalue (𝓕⁻ f : 𝓢(ℝ, ℂ)) ζ) : ζ.im ≤ U := by
  have h := (sech_source_polynomial_ceiling k hN hs m hm hf hz).trans hcert
  have hp := (mul_le_mul_iff_right₀ (show (0 : ℝ) < (2 * k + 2 : ℝ) ^ (2 * k + 2) by positivity)).mp h
  exact (pow_le_pow_iff_left₀ hz.1.le hU (by omega : 2 * k + 1 ≠ 0)).mp hp

theorem sech_five_halves_certificate {f g : 𝓢(ℝ, ℂ)} (hs : IsSechSource (5 / 2) g)
    (m : ℝ → ℂ) (hm : ∀ ξ, ‖m ξ‖ ≤ 1) (hf : ∀ ξ, f ξ = m ξ * g ξ)
    {ζ : ℂ} (hz : IsEigenvalue (𝓕⁻ f : 𝓢(ℝ, ℂ)) ζ) : ζ.im ≤ 2 * (1 + 43672 / 10000000 : ℝ) :=
  rational_sech_ceiling 2 (by norm_num) (by norm_num) (by norm_num) hs m hm hf hz

theorem sech_seven_halves_certificate {f g : 𝓢(ℝ, ℂ)} (hs : IsSechSource (7 / 2) g)
    (m : ℝ → ℂ) (hm : ∀ ξ, ‖m ξ‖ ≤ 1) (hf : ∀ ξ, f ξ = m ξ * g ξ)
    {ζ : ℂ} (hz : IsEigenvalue (𝓕⁻ f : 𝓢(ℝ, ℂ)) ζ) : ζ.im ≤ 3 * (1 + 15446 / 10000000 : ℝ) :=
  rational_sech_ceiling 3 (by norm_num) (by norm_num) (by norm_num) hs m hm hf hz

theorem sech_eleven_halves_certificate {f g : 𝓢(ℝ, ℂ)} (hs : IsSechSource (11 / 2) g)
    (m : ℝ → ℂ) (hm : ∀ ξ, ‖m ξ‖ ≤ 1) (hf : ∀ ξ, f ξ = m ξ * g ξ)
    {ζ : ℂ} (hz : IsEigenvalue (𝓕⁻ f : 𝓢(ℝ, ℂ)) ζ) : ζ.im ≤ 5 * (1 + 3888 / 10000000 : ℝ) :=
  rational_sech_ceiling 5 (by norm_num) (by norm_num) (by norm_num) hs m hm hf hz

theorem sech_nineteen_halves_certificate {f g : 𝓢(ℝ, ℂ)} (hs : IsSechSource (19 / 2) g)
    (m : ℝ → ℂ) (hm : ∀ ξ, ‖m ξ‖ ≤ 1) (hf : ∀ ξ, f ξ = m ξ * g ξ)
    {ζ : ℂ} (hz : IsEigenvalue (𝓕⁻ f : 𝓢(ℝ, ℂ)) ζ) : ζ.im ≤ 9 * (1 + 743 / 10000000 : ℝ) :=
  rational_sech_ceiling 9 (by norm_num) (by norm_num) (by norm_num) hs m hm hf hz

end ZS
