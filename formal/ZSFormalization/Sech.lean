module

public import ZSFormalization.SpectralBound

@[expose] public section

/-! # Exact sech moments and their source ceilings -/

open MeasureTheory Filter Set FourierTransform
open scoped Topology SchwartzMap

namespace ZS

noncomputable def sech (t : ℝ) : ℝ := (Real.cosh t)⁻¹

lemma sech_pos (t : ℝ) : 0 < sech t := inv_pos.mpr (Real.cosh_pos t)

lemma sech_continuous : Continuous sech := Real.continuous_cosh.inv₀ (fun t => (Real.cosh_pos t).ne')

lemma tanh_complement (t : ℝ) : 1 - Real.tanh t ^ 2 = sech t ^ 2 := by
  rw [Real.tanh_eq_sinh_div_cosh]
  unfold sech
  have hn := (Real.cosh_pos t).ne'
  field_simp
  nlinarith [Real.cosh_sq_sub_sinh_sq t]

lemma tanh_derivative (t : ℝ) : HasDerivAt Real.tanh (sech t ^ 2) t := by
  convert (Real.hasDerivAt_sinh t).div (Real.hasDerivAt_cosh t) (Real.cosh_pos t).ne' using 1
  · ext s; exact Real.tanh_eq_sinh_div_cosh s
  · unfold sech
    have hn := (Real.cosh_pos t).ne'
    field_simp
    nlinarith [Real.cosh_sq_sub_sinh_sq t]

lemma tanh_exp_neg (t : ℝ) :
    Real.tanh t = (1 - Real.exp (-t) ^ 2) / (1 + Real.exp (-t) ^ 2) := by
  rw [Real.tanh_eq, show Real.exp t = (Real.exp (-t))⁻¹ by rw [← Real.exp_neg, neg_neg]]
  have he := Real.exp_pos (-t)
  field_simp

lemma tanh_tendsto_atTop : Tendsto Real.tanh atTop (𝓝 1) := by
  have h := Real.tendsto_exp_neg_atTop_nhds_zero.pow 2
  have hh := ((tendsto_const_nhds (x := (1 : ℝ))).sub h).div
    ((tendsto_const_nhds (x := (1 : ℝ))).add h) (by norm_num : (1 : ℝ) + 0 ^ 2 ≠ 0)
  convert hh using 1
  · funext t; exact tanh_exp_neg t
  · norm_num

lemma tanh_tendsto_atBot : Tendsto Real.tanh atBot (𝓝 (-1)) := by
  have h := tanh_tendsto_atTop.neg.comp tendsto_neg_atBot_atTop
  simpa only [Function.comp_def, Real.tanh_neg, neg_neg] using h

lemma sech_moment_derivative (k : ℕ) (t : ℝ) :
    HasDerivAt (fun s => momentPrimitive k (Real.tanh s)) (sech t ^ (2 * k + 2)) t := by
  convert (momentPrimitive_derivative k (Real.tanh t)).comp t (tanh_derivative t) using 1
  · rfl
  · rw [tanh_complement, ← pow_mul, ← pow_add]

lemma sech_even_moment_integrable (k : ℕ) : Integrable (fun t => sech t ^ (2 * k + 2)) := by
  have hpc : Continuous (momentPrimitive k) :=
    continuous_iff_continuousAt.mpr (fun t => (momentPrimitive_derivative k t).continuousAt)
  have hi : IntegrableOn (fun t => sech t ^ (2 * k + 2)) (Ioi 0) :=
    integrableOn_Ioi_deriv_of_nonneg' (fun t _ => sech_moment_derivative k t)
      (fun t _ => (pow_pos (sech_pos t) _).le) (hpc.continuousAt.tendsto.comp tanh_tendsto_atTop)
  have hi' : IntegrableOn (fun t => sech t ^ (2 * k + 2)) (Ici 0) :=
    (integrableOn_Ici_iff_integrableOn_Ioi (μ := volume)).mpr hi
  have hj : IntegrableOn (fun t => sech t ^ (2 * k + 2)) (Iic 0) := by
    simpa only [sech, Real.cosh_neg, neg_zero] using
      (show IntegrableOn (fun t => sech t ^ (2 * k + 2)) (Ici (-(0 : ℝ))) by simpa using hi').comp_neg_Iic
  rw [← integrableOn_univ, ← Iic_union_Ioi (a := (0 : ℝ))]
  exact hj.union hi

/-- Exact sech even moments, without Gamma functions. -/
theorem sech_even_moment (k : ℕ) :
    (∫ t, sech t ^ (2 * k + 2)) = ∫ s in (-1 : ℝ)..1, (1 - s ^ 2) ^ k := by
  have hpc : Continuous (momentPrimitive k) :=
    continuous_iff_continuousAt.mpr (fun t => (momentPrimitive_derivative k t).continuousAt)
  rw [integral_of_hasDerivAt_of_tendsto (sech_moment_derivative k) (sech_even_moment_integrable k)
    (hpc.continuousAt.tendsto.comp tanh_tendsto_atBot)
    (hpc.continuousAt.tendsto.comp tanh_tendsto_atTop), momentPrimitive_jump]

lemma sech_moment_constant_pos (k : ℕ) :
    0 < ∫ s in (-1 : ℝ)..1, (1 - s ^ 2) ^ k := by
  rw [← sech_even_moment]
  exact integral_pos_of_integrable_nonneg_nonzero (sech_continuous.pow _) (sech_even_moment_integrable k)
    (fun t => (pow_pos (sech_pos t) _).le) (x := 0) (by simp [sech])

/-- A source is specified by its nonnegative Schwartz spectrum and exact TL
waveform. The explicit Fourier transform of sech is a separate identity. -/
def IsSechSource (N : ℝ) (g : 𝓢(ℝ, ℂ)) : Prop :=
  PositiveSpectrum g ∧ ∀ t, 𝓕⁻ g t = ((N * sech t : ℝ) : ℂ)

/-- The noninteger-sech ceiling in polynomial form (PDF page 61).
The parameter `N` need not be integral. -/
theorem sech_source_polynomial_ceiling (k : ℕ) {N : ℝ} (hN : 0 ≤ N)
    {f g : 𝓢(ℝ, ℂ)} (hs : IsSechSource N g) (m : ℝ → ℂ)
    (hm : ∀ ξ, ‖m ξ‖ ≤ 1) (hf : ∀ ξ, f ξ = m ξ * g ξ)
    {ζ : ℂ} (hz : IsEigenvalue (𝓕⁻ f : 𝓢(ℝ, ℂ)) ζ) :
    (2 * k + 2 : ℝ) ^ (2 * k + 2) * ζ.im ^ (2 * k + 1) ≤
      2 * (2 * k + 1 : ℝ) ^ (2 * k + 1) * N ^ (2 * k + 2) := by
  have h := passive_source_eigenvalue_bound k m hs.1 hm hf hz
  have hnorm : ∀ t, ‖𝓕⁻ g t‖ = N * sech t := by
    intro t
    rw [hs.2 t, Complex.norm_real, Real.norm_eq_abs, abs_of_nonneg (mul_nonneg hN (sech_pos t).le)]
  simp_rw [hnorm, mul_pow] at h
  rw [integral_const_mul, sech_even_moment] at h
  apply (mul_le_mul_iff_left₀ (sech_moment_constant_pos k)).mp
  nlinarith only [h]

lemma integer_sech_ceiling_algebra (k : ℕ) {η : ℝ} (hη : 0 ≤ η)
    (h : (2 * k + 2 : ℝ) ^ (2 * k + 2) * η ^ (2 * k + 1) ≤
      2 * (2 * k + 1 : ℝ) ^ (2 * k + 1) * (k + 1 : ℝ) ^ (2 * k + 2)) :
    η ≤ (k + 1 : ℝ) - 1 / 2 := by
  have hfactor : (2 * k + 2 : ℝ) ^ (2 * k + 2) * ((k + 1 : ℝ) - 1 / 2) ^ (2 * k + 1) =
      2 * (2 * k + 1 : ℝ) ^ (2 * k + 1) * (k + 1 : ℝ) ^ (2 * k + 2) := by
    rw [show (2 * k + 2 : ℝ) = 2 * (k + 1) by ring,
      show (k + 1 : ℝ) - 1 / 2 = (2 * k + 1) / 2 by ring,
      mul_pow, div_pow, pow_succ (2 : ℝ) (2 * k + 1)]
    field_simp
  rw [← hfactor] at h
  have hpow := (mul_le_mul_iff_right₀ (show (0 : ℝ) < (2 * k + 2 : ℝ) ^ (2 * k + 2) by positivity)).mp h
  exact (pow_le_pow_iff_left₀ hη (by have := Nat.cast_nonneg (α := ℝ) k; linarith)
    (by omega : 2 * k + 1 ≠ 0)).mp hpow

/-- Exact integer-order upper ceiling for every admissible mask of a source
whose TL waveform is `(k+1) sech`. Attainment is proved separately. -/
theorem integer_sech_source_ceiling (k : ℕ) {f g : 𝓢(ℝ, ℂ)}
    (hs : IsSechSource (k + 1 : ℝ) g) (m : ℝ → ℂ)
    (hm : ∀ ξ, ‖m ξ‖ ≤ 1) (hf : ∀ ξ, f ξ = m ξ * g ξ)
    {ζ : ℂ} (hz : IsEigenvalue (𝓕⁻ f : 𝓢(ℝ, ℂ)) ζ) :
    ζ.im ≤ (k + 1 : ℝ) - 1 / 2 :=
  integer_sech_ceiling_algebra k hz.1.le
    (sech_source_polynomial_ceiling k (by positivity) hs m hm hf hz)

end ZS
