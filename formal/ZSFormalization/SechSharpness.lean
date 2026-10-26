module

public import ZSFormalization.Sech

@[expose] public section

/-! # An explicit square-integrable sech bound state -/

open MeasureTheory Filter Complex Set FourierTransform
open scoped Topology SchwartzMap

namespace ZS

lemma sech_derivative (t : ℝ) : HasDerivAt sech (-sech t * Real.tanh t) t := by
  convert (Real.hasDerivAt_cosh t).inv (Real.cosh_pos t).ne' using 1
  · rfl
  · rw [Real.tanh_eq_sinh_div_cosh]
    unfold sech
    field_simp

lemma sech_le_one (t : ℝ) : sech t ≤ 1 := by
  exact inv_le_one_of_one_le₀ (Real.one_le_cosh t)

lemma arctan_exp_derivative (t : ℝ) :
    HasDerivAt (fun s => 2 * Real.arctan (Real.exp s)) (sech t) t := by
  convert ((Real.hasDerivAt_arctan (Real.exp t)).comp t (Real.hasDerivAt_exp t)).const_mul 2 using 1
  · rfl
  · unfold sech
    rw [Real.cosh_eq, Real.exp_neg]
    have he := Real.exp_pos t
    field_simp
    ring

lemma sech_integrable : Integrable sech := by
  have hlim : Tendsto (fun t => 2 * Real.arctan (Real.exp t)) atTop (𝓝 (2 * (Real.pi / 2))) :=
    ((Real.tendsto_arctan_atTop.mono_right nhdsWithin_le_nhds).comp Real.tendsto_exp_atTop).const_mul 2
  have hi : IntegrableOn sech (Ioi 0) :=
    integrableOn_Ioi_deriv_of_nonneg' (fun t _ => arctan_exp_derivative t)
      (fun t _ => (sech_pos t).le) hlim
  have hi' : IntegrableOn sech (Ici (-(0 : ℝ))) := by
    simpa only [neg_zero] using (integrableOn_Ici_iff_integrableOn_Ioi (μ := volume)).mpr hi
  have hj : IntegrableOn sech (Iic 0) := by
    have hh := hi'.comp_neg_Iic
    have heq : (fun x => sech (-x)) = sech := by funext x; simp [sech]
    rw [heq] at hh
    exact hh
  rw [← integrableOn_univ, ← Iic_union_Ioi (a := (0 : ℝ))]
  exact hj.union hi

lemma sech_power_integrable (k : ℕ) : Integrable (fun t => sech t ^ (k + 1)) := by
  apply sech_integrable.mono' (sech_continuous.pow _).aestronglyMeasurable
  filter_upwards with t
  simp only [Pi.pow_apply]
  rw [Real.norm_eq_abs, abs_of_nonneg (pow_nonneg (sech_pos t).le _), pow_succ]
  exact mul_le_of_le_one_left (sech_pos t).le (pow_le_one₀ (sech_pos t).le (sech_le_one t))

noncomputable def sechSpinorOne (k : ℕ) (t : ℝ) : ℝ :=
  Real.exp (-t / 2) * sech t ^ (k + 1)

noncomputable def sechSpinorTwo (k : ℕ) (t : ℝ) : ℝ :=
  -Real.exp (t / 2) * sech t ^ (k + 1)

lemma sechSpinorOne_derivative (k : ℕ) (t : ℝ) :
    HasDerivAt (sechSpinorOne k)
      ((-1 / 2 - (k + 1 : ℝ) * Real.tanh t) * sechSpinorOne k t) t := by
  have he := (((hasDerivAt_id t).neg).div_const (2 : ℝ)).exp
  convert he.mul ((sech_derivative t).pow (k + 1)) using 1
  · rfl
  · simp only [Nat.add_sub_cancel, Nat.cast_add, Nat.cast_one, Pi.pow_apply, Pi.neg_apply, id_eq]
    unfold sechSpinorOne
    rw [pow_succ]
    ring

lemma sechSpinorTwo_derivative (k : ℕ) (t : ℝ) :
    HasDerivAt (sechSpinorTwo k)
      ((1 / 2 - (k + 1 : ℝ) * Real.tanh t) * sechSpinorTwo k t) t := by
  have he := (((hasDerivAt_id t).div_const (2 : ℝ)).exp).neg
  convert he.mul ((sech_derivative t).pow (k + 1)) using 1
  · rfl
  · simp only [Nat.add_sub_cancel, Nat.cast_add, Nat.cast_one, Pi.pow_apply, Pi.neg_apply, id_eq]
    unfold sechSpinorTwo
    rw [pow_succ]
    ring

lemma sechSpinor_square_sum (k : ℕ) (t : ℝ) :
    sechSpinorOne k t ^ 2 + sechSpinorTwo k t ^ 2 = 2 * sech t ^ (2 * k + 1) := by
  have h₁ : Real.exp (-t / 2) ^ 2 = Real.exp (-t) := by
    rw [sq, ← Real.exp_add]; congr 1; ring
  have h₂ : Real.exp (t / 2) ^ 2 = Real.exp t := by
    rw [sq, ← Real.exp_add]; congr 1; ring
  unfold sechSpinorOne sechSpinorTwo
  simp only [mul_pow, neg_sq, h₁, h₂, ← pow_mul]
  rw [show (k + 1) * 2 = 2 * k + 2 by omega]
  calc
    _ = (Real.exp t + Real.exp (-t)) * sech t ^ (2 * k + 2) := by ring
    _ = 2 * Real.cosh t * sech t ^ (2 * k + 2) := by rw [Real.cosh_eq]; ring
    _ = _ := by rw [pow_succ]; unfold sech; field_simp

lemma sechSpinor_coupling_one (k : ℕ) (t : ℝ) :
    sech t * sechSpinorTwo k t = -(1 + Real.tanh t) * sechSpinorOne k t := by
  have he : Real.exp t * Real.exp (-t / 2) = Real.exp (t / 2) := by
    rw [← Real.exp_add]; congr 1; ring
  have hh : sech t * Real.exp t = 1 + Real.tanh t := by
    rw [← Real.cosh_add_sinh, Real.tanh_eq_sinh_div_cosh]
    unfold sech
    field_simp
  unfold sechSpinorOne sechSpinorTwo
  rw [← he, ← hh]
  ring

lemma sechSpinor_coupling_two (k : ℕ) (t : ℝ) :
    sech t * sechSpinorOne k t = -(1 - Real.tanh t) * sechSpinorTwo k t := by
  have he : Real.exp (-t) * Real.exp (t / 2) = Real.exp (-t / 2) := by
    rw [← Real.exp_add]; congr 1; ring
  have hh : sech t * Real.exp (-t) = 1 - Real.tanh t := by
    rw [← Real.cosh_sub_sinh, Real.tanh_eq_sinh_div_cosh]
    unfold sech
    field_simp
  unfold sechSpinorOne sechSpinorTwo
  rw [← he, ← hh]
  ring

theorem sechSpinor_solves (k : ℕ) :
    SolvesZS (fun t => (((k + 1 : ℝ) * sech t : ℝ) : ℂ))
      (Complex.I * (((k + 1 : ℝ) - 1 / 2 : ℝ) : ℂ))
      (fun t => (sechSpinorOne k t : ℂ)) (fun t => (sechSpinorTwo k t : ℂ)) := by
  constructor
  · intro t
    convert (sechSpinorOne_derivative k t).ofReal_comp using 1
    have h := congrArg (fun z : ℝ => (k + 1 : ℝ) * z) (sechSpinor_coupling_one k t)
    simp only [Real.tanh] at h
    apply Complex.ext <;> simp [Complex.mul_re, Complex.mul_im]
    nlinarith only [h]
  · intro t
    convert (sechSpinorTwo_derivative k t).ofReal_comp using 1
    have h := congrArg (fun z : ℝ => (k + 1 : ℝ) * z) (sechSpinor_coupling_two k t)
    simp only [Real.tanh] at h
    apply Complex.ext <;> simp [Complex.mul_re, Complex.mul_im]
    nlinarith only [h]

lemma sechSpinor_squares_integrable (k : ℕ) :
    Integrable (fun t => sechSpinorOne k t ^ 2) ∧ Integrable (fun t => sechSpinorTwo k t ^ 2) := by
  have hc₁ : Continuous (sechSpinorOne k) :=
    continuous_iff_continuousAt.mpr (fun t => (sechSpinorOne_derivative k t).continuousAt)
  have hc₂ : Continuous (sechSpinorTwo k) :=
    continuous_iff_continuousAt.mpr (fun t => (sechSpinorTwo_derivative k t).continuousAt)
  have hI := (sech_power_integrable (2 * k)).const_mul 2
  constructor
  · apply hI.mono' (hc₁.pow 2).aestronglyMeasurable
    filter_upwards with t
    simp only [Pi.pow_apply]
    rw [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg _)]
    nlinarith only [sechSpinor_square_sum k t, sq_nonneg (sechSpinorTwo k t)]
  · apply hI.mono' (hc₂.pow 2).aestronglyMeasurable
    filter_upwards with t
    simp only [Pi.pow_apply]
    rw [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg _)]
    nlinarith only [sechSpinor_square_sum k t, sq_nonneg (sechSpinorOne k t)]

/-- Sharpness is witnessed by the explicit L² spinor, not by imported scattering data. -/
theorem sech_has_top_eigenvalue (k : ℕ) :
    IsEigenvalue (fun t => (((k + 1 : ℝ) * sech t : ℝ) : ℂ))
      (Complex.I * (((k + 1 : ℝ) - 1 / 2 : ℝ) : ℂ)) := by
  refine ⟨?_, (fun t => (sechSpinorOne k t : ℂ)), (fun t => (sechSpinorTwo k t : ℂ)),
    sechSpinor_solves k, ?_, ?_, ?_⟩
  · simp only [Complex.mul_im, Complex.I_re, Complex.I_im, Complex.ofReal_re,
      Complex.ofReal_im, zero_mul, one_mul, zero_add]
    have := Nat.cast_nonneg (α := ℝ) k
    linarith
  · have hc : Continuous (fun t => (sechSpinorOne k t : ℂ)) :=
      continuous_iff_continuousAt.mpr (fun t => (sechSpinorOne_derivative k t).ofReal_comp.continuousAt)
    apply (memLp_two_iff_integrable_sq_norm hc.aestronglyMeasurable).mpr
    simpa only [Complex.norm_real, Real.norm_eq_abs, sq_abs] using (sechSpinor_squares_integrable k).1
  · have hc : Continuous (fun t => (sechSpinorTwo k t : ℂ)) :=
      continuous_iff_continuousAt.mpr (fun t => (sechSpinorTwo_derivative k t).ofReal_comp.continuousAt)
    apply (memLp_two_iff_integrable_sq_norm hc.aestronglyMeasurable).mpr
    simpa only [Complex.norm_real, Real.norm_eq_abs, sq_abs] using (sechSpinor_squares_integrable k).2
  · exact ⟨0, Or.inl (by simp [sechSpinorOne, sech])⟩

theorem integer_sech_source_attains (k : ℕ) {g : 𝓢(ℝ, ℂ)}
    (hs : IsSechSource (k + 1 : ℝ) g) :
    IsEigenvalue (𝓕⁻ g : 𝓢(ℝ, ℂ))
      (Complex.I * (((k + 1 : ℝ) - 1 / 2 : ℝ) : ℂ)) := by
  have heq : (⇑(𝓕⁻ g : 𝓢(ℝ, ℂ)) : ℝ → ℂ) = (fun t => (((k + 1 : ℝ) * sech t : ℝ) : ℂ)) := funext hs.2
  rw [heq]
  exact sech_has_top_eigenvalue k

end ZS
