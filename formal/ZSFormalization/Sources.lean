module

public import ZSFormalization.Corollaries
public import ZSFormalization.Gaussian

@[expose] public section

/-! # Concrete Schwartz source constructions -/

open MeasureTheory Filter Set FourierTransform
open scoped Topology SchwartzMap Convolution

namespace ZS

noncomputable def sechDerivPoly : ℕ → Polynomial ℝ
  | 0 => 1
  | n + 1 => -Polynomial.X * sechDerivPoly n +
      (1 - Polynomial.X ^ 2) * (sechDerivPoly n).derivative

lemma sech_iteratedDeriv (n : ℕ) (t : ℝ) :
    iteratedDeriv n sech t = sech t * (sechDerivPoly n).eval (Real.tanh t) := by
  induction n generalizing t with
  | zero => simp [sechDerivPoly]
  | succ n ih =>
    rw [iteratedDeriv_succ]
    have heq : iteratedDeriv n sech =
        (fun t => sech t * (sechDerivPoly n).eval (Real.tanh t)) := funext ih
    rw [heq]
    have hd := ((sech_derivative t).mul
      (((sechDerivPoly n).hasDerivAt (Real.tanh t)).comp t (tanh_derivative t))).deriv
    change deriv (fun t => sech t * (sechDerivPoly n).eval (Real.tanh t)) t = _ at hd
    rw [hd]
    simp only [Function.comp_def, sechDerivPoly, Polynomial.eval_add, Polynomial.eval_mul, Polynomial.eval_neg,
      Polynomial.eval_X, Polynomial.eval_sub, Polynomial.eval_one, Polynomial.eval_pow]
    rw [tanh_complement]
    ring

lemma tanh_mem_Icc (t : ℝ) : Real.tanh t ∈ Icc (-1 : ℝ) 1 := by
  have h := tanh_complement t
  constructor <;> nlinarith [sq_nonneg (sech t), sq_nonneg (Real.tanh t + 1),
    sq_nonneg (Real.tanh t - 1)]

lemma sech_exp_bound (t : ℝ) : sech t ≤ 2 * Real.exp (-|t|) := by
  unfold sech
  rw [inv_eq_one_div, Real.exp_neg, ← div_eq_mul_inv]
  apply (div_le_div_iff₀ (Real.cosh_pos t) (Real.exp_pos |t|)).mpr
  rw [← Real.cosh_abs t, Real.cosh_eq]
  nlinarith [Real.exp_pos (-|t|)]

lemma sech_weight_bound (k : ℕ) (t : ℝ) :
    |t| ^ k * sech t ≤ 2 * (k.factorial : ℝ) := by
  have hp := Real.pow_div_factorial_le_exp |t| (abs_nonneg t) k
  have hf : (0 : ℝ) < k.factorial := by exact_mod_cast k.factorial_pos
  have hh : |t| ^ k ≤ (k.factorial : ℝ) * Real.exp |t| := by
    have := (div_le_iff₀ hf).mp hp
    nlinarith only [this]
  calc
    _ ≤ |t| ^ k * (2 * Real.exp (-|t|)) :=
      mul_le_mul_of_nonneg_left (sech_exp_bound t) (pow_nonneg (abs_nonneg t) _)
    _ ≤ ((k.factorial : ℝ) * Real.exp |t|) * (2 * Real.exp (-|t|)) := by gcongr
    _ = _ := by rw [Real.exp_neg]; field_simp

noncomputable def sechSchwartzReal : 𝓢(ℝ, ℝ) where
  toFun := sech
  smooth' := Real.contDiff_cosh.inv (fun t => (Real.cosh_pos t).ne')
  decay' k n := by
    obtain ⟨C, hC⟩ := (isCompact_Icc : IsCompact (Icc (-1 : ℝ) 1)).bddAbove_image
      ((sechDerivPoly n).continuous.abs.continuousOn)
    refine ⟨2 * (k.factorial : ℝ) * max C 0, fun t => ?_⟩
    rw [norm_iteratedFDeriv_eq_norm_iteratedDeriv, sech_iteratedDeriv, norm_mul,
      Real.norm_eq_abs, Real.norm_eq_abs, Real.norm_eq_abs, abs_of_pos (sech_pos t)]
    have hp : |(sechDerivPoly n).eval (Real.tanh t)| ≤ max C 0 :=
      (hC (mem_image_of_mem _ (tanh_mem_Icc t))).trans (le_max_left _ _)
    calc
      _ = (|t| ^ k * sech t) * |(sechDerivPoly n).eval (Real.tanh t)| := by ring
      _ ≤ (2 * (k.factorial : ℝ)) * max C 0 :=
        mul_le_mul (sech_weight_bound k t) hp (abs_nonneg _) (by positivity)

noncomputable def sechSchwartz (N : ℝ) : 𝓢(ℝ, ℂ) :=
  N • SchwartzMap.postcompCLM Complex.ofRealCLM sechSchwartzReal

@[simp] lemma sechSchwartz_apply (N t : ℝ) :
    sechSchwartz N t = ((N * sech t : ℝ) : ℂ) := by
  change N • (sech t : ℂ) = _
  simp [Complex.real_smul]

/- An autocorrelation representation proves spectral positivity without using
the contour-integral formula for the Fourier transform of sech. -/
noncomputable def sechFactor (t : ℝ) : ℝ := Real.exp (t - Real.exp (2 * t))

lemma sechFactor_pos (t : ℝ) : 0 < sechFactor t := Real.exp_pos _

lemma sechFactor_continuous : Continuous sechFactor := by unfold sechFactor; fun_prop

lemma sechFactor_le_exp (t : ℝ) : sechFactor t ≤ Real.exp t := by
  unfold sechFactor
  exact Real.exp_le_exp.mpr (by linarith [Real.exp_pos (2 * t)])

lemma sechFactor_le_exp_neg (t : ℝ) : sechFactor t ≤ Real.exp (-t) := by
  unfold sechFactor
  exact Real.exp_le_exp.mpr (by linarith [Real.add_one_le_exp (2 * t)])

lemma sechFactor_le_one (t : ℝ) : sechFactor t ≤ 1 := by
  rcases le_total t 0 with h | h
  · exact (sechFactor_le_exp t).trans (Real.exp_le_one_iff.mpr h)
  · exact (sechFactor_le_exp_neg t).trans (Real.exp_le_one_iff.mpr (by linarith))

lemma sechFactor_integrable : Integrable sechFactor := by
  have hl : IntegrableOn sechFactor (Iic 0) := by
    apply (integrableOn_exp_Iic 0).mono' sechFactor_continuous.aestronglyMeasurable
    filter_upwards with t
    rw [Real.norm_eq_abs, abs_of_pos (sechFactor_pos t)]
    exact sechFactor_le_exp t
  have hr : IntegrableOn sechFactor (Ioi 0) := by
    apply (integrableOn_exp_neg_Ioi 0).mono' sechFactor_continuous.aestronglyMeasurable
    filter_upwards with t
    rw [Real.norm_eq_abs, abs_of_pos (sechFactor_pos t)]
    exact sechFactor_le_exp_neg t
  rw [← integrableOn_univ, ← Iic_union_Ioi (a := (0 : ℝ))]
  exact hl.union hr

lemma sechFactor_product (s t : ℝ) :
    sechFactor s * sechFactor (s - t) =
      Real.exp (-t) * Real.exp (2 * s) *
        Real.exp (-(1 + Real.exp (-2 * t)) * Real.exp (2 * s)) := by
  unfold sechFactor
  rw [← Real.exp_add, ← Real.exp_add, ← Real.exp_add]
  congr 1
  rw [show 2 * (s - t) = 2 * s + -2 * t by ring, Real.exp_add]
  ring

lemma sechFactor_primitive_derivative (s t : ℝ) :
    HasDerivAt
      (fun s => -(Real.exp (-t) / (2 * (1 + Real.exp (-2 * t)))) *
        Real.exp (-(1 + Real.exp (-2 * t)) * Real.exp (2 * s)))
      (sechFactor s * sechFactor (s - t)) s := by
  have hd := (((((hasDerivAt_id s).const_mul 2).exp).const_mul
    (-(1 + Real.exp (-2 * t)))).exp).const_mul
      (-(Real.exp (-t) / (2 * (1 + Real.exp (-2 * t)))))
  convert hd using 1
  · rfl
  · rw [sechFactor_product]
    simp only [id_eq]
    have hA : 1 + Real.exp (-2 * t) ≠ 0 := by positivity
    field_simp

lemma sech_autocorrelation (t : ℝ) :
    (∫ s, sechFactor s * sechFactor (s - t)) = sech t / 4 := by
  have hi : Integrable (fun s => sechFactor s * sechFactor (s - t)) := by
    apply sechFactor_integrable.mono'
      (sechFactor_continuous.mul (sechFactor_continuous.comp (continuous_id.sub continuous_const))).aestronglyMeasurable
    filter_upwards with s
    change ‖sechFactor s * sechFactor (s - t)‖ ≤ sechFactor s
    rw [Real.norm_eq_abs, abs_of_pos (mul_pos (sechFactor_pos _) (sechFactor_pos _))]
    exact mul_le_of_le_one_right (sechFactor_pos _).le (sechFactor_le_one _)
  have hA : 0 < 1 + Real.exp (-2 * t) := by positivity
  have ht : Tendsto (fun s : ℝ => Real.exp (-(1 + Real.exp (-2 * t)) * Real.exp (2 * s)))
      atTop (𝓝 0) := Real.tendsto_exp_atBot.comp
    ((Real.tendsto_exp_atTop.comp (tendsto_id.const_mul_atTop (by norm_num : (0 : ℝ) < 2))).const_mul_atTop_of_neg (neg_neg_of_pos hA))
  have hb : Tendsto (fun s : ℝ => Real.exp (-(1 + Real.exp (-2 * t)) * Real.exp (2 * s)))
      atBot (𝓝 1) := by
    have h := (Real.tendsto_exp_atBot.comp
      (tendsto_id.const_mul_atBot (by norm_num : (0 : ℝ) < 2))).const_mul (-(1 + Real.exp (-2 * t)))
    simpa only [Function.comp_def, id_eq, mul_zero, Real.exp_zero] using (Real.continuous_exp.tendsto _).comp h
  rw [integral_of_hasDerivAt_of_tendsto (fun s => sechFactor_primitive_derivative s t) hi
    (hb.const_mul (-(Real.exp (-t) / (2 * (1 + Real.exp (-2 * t))))))
    (ht.const_mul (-(Real.exp (-t) / (2 * (1 + Real.exp (-2 * t))))))]
  simp only [mul_zero, mul_one, sub_neg_eq_add, zero_add]
  unfold sech
  rw [Real.cosh_eq, show -2 * t = -t + -t by ring, Real.exp_add, Real.exp_neg]
  have he := Real.exp_pos t
  field_simp
  ring

lemma fourier_reflect_real (h : ℝ → ℝ) (ξ : ℝ) :
    𝓕 (fun t => (h (-t) : ℂ)) ξ = (starRingEnd ℂ) (𝓕 (fun t => (h t : ℂ)) ξ) := by
  simp only [Real.fourier_real_eq_integral_exp_smul, smul_eq_mul]
  rw [← integral_conj]
  conv_lhs => rw [← integral_neg_eq_self]
  apply integral_congr_ae
  filter_upwards with t
  simp only [neg_neg, map_mul, ← Complex.exp_conj, Complex.conj_ofReal, Complex.conj_I]
  congr 2
  push_cast
  ring

lemma sech_autocorrelation_complex :
    ((fun t => (sechFactor t : ℂ)) ⋆[ContinuousLinearMap.mul ℂ ℂ]
      (fun t => (sechFactor (-t) : ℂ))) = fun t => ((sech t / 4 : ℝ) : ℂ) := by
  funext t
  simp only [convolution_def, ContinuousLinearMap.mul_apply', neg_sub]
  simp_rw [← Complex.ofReal_mul]
  rw [integral_complex_ofReal, sech_autocorrelation]

lemma fourier_sech_nonnegative (ξ : ℝ) :
    ∃ r : ℝ, 0 ≤ r ∧ 𝓕 (sechSchwartz 1) ξ = (r : ℂ) := by
  have hi : Integrable (fun t => (sechFactor t : ℂ)) := sechFactor_integrable.ofReal
  have hj : Integrable (fun t => (sechFactor (-t) : ℂ)) := hi.comp_neg
  have hc := Real.fourier_mul_convolution_eq hi hj ξ
  rw [sech_autocorrelation_complex, fourier_reflect_real] at hc
  have heq : (fun t => ((sech t / 4 : ℝ) : ℂ)) =
      (1 / 4 : ℂ) • (fun t => (sech t : ℂ)) := by ext t; simp; ring
  rw [heq, Real.fourier_real_eq_integral_exp_smul] at hc
  simp only [Pi.smul_apply, smul_eq_mul] at hc
  have hscale : (∫ t : ℝ, Complex.exp (↑(-2 * Real.pi * t * ξ) * Complex.I) *
      ((1 / 4 : ℂ) * (sech t : ℂ))) =
      (1 / 4 : ℂ) * 𝓕 (fun t => (sech t : ℂ)) ξ := by
    rw [Real.fourier_real_eq_integral_exp_smul, ← integral_const_mul]
    congr 1; funext t
    simp only [smul_eq_mul]
    ring
  rw [hscale] at hc
  refine ⟨4 * ‖𝓕 (fun t => (sechFactor t : ℂ)) ξ‖ ^ 2, by positivity, ?_⟩
  have hq : (⇑(sechSchwartz 1) : ℝ → ℂ) = fun t => (sech t : ℂ) := by ext t; simp
  rw [SchwartzMap.fourier_coe, hq]
  rw [Complex.mul_conj] at hc
  rw [Complex.normSq_eq_norm_sq] at hc
  push_cast at hc ⊢
  linear_combination 4 * hc

noncomputable def sechSource (N : ℝ) : 𝓢(ℝ, ℂ) := 𝓕 (sechSchwartz N)

theorem sechSource_spec {N : ℝ} (hN : 0 ≤ N) : IsSechSource N (sechSource N) := by
  constructor
  · intro ξ
    obtain ⟨r, hr, heq⟩ := fourier_sech_nonnegative ξ
    have hq : sechSchwartz N = N • sechSchwartz 1 := by ext t; simp [Complex.real_smul]
    have hv : sechSource N ξ = ((N * r : ℝ) : ℂ) := by
      unfold sechSource
      rw [hq, fourier_smul]
      simp only [smul_apply, heq, Complex.real_smul, Complex.ofReal_mul]
    rw [hv, Complex.norm_real, Real.norm_eq_abs, abs_of_nonneg (mul_nonneg hN hr)]
  · intro t
    simp only [sechSource, fourierInv_fourier_eq, sechSchwartz_apply]

/-- A completely instantiated sharp optimum for the canonical sech spectrum. -/
theorem canonical_integer_sech_optimality (k : ℕ) :
    IsGreatest (attainableHeights (sechSource (k + 1 : ℝ))) ((k + 1 : ℝ) - 1 / 2) :=
  integer_sech_optimality k (sechSource_spec (by positivity))

theorem canonical_order_four_fraction_optimum :
    IsGreatest (attainableFractions (sechSource 4)) (7 / 16 : ℝ) :=
  order_four_fraction_optimum (sechSource_spec (by norm_num))

theorem canonical_integer_sech_fraction_optimality (k : ℕ) :
    IsGreatest (attainableFractions (sechSource (k + 1 : ℝ)))
      ((2 * (k + 1 : ℝ) - 1) / (k + 1 : ℝ) ^ 2) :=
  integer_sech_fraction_optimality k (sechSource_spec (by positivity))

theorem canonical_sech_polynomial_ceiling (k : ℕ) {N : ℝ} (hN : 0 ≤ N)
    {f : 𝓢(ℝ, ℂ)} (m : ℝ → ℂ)
    (hm : ∀ ξ, ‖m ξ‖ ≤ 1) (hf : ∀ ξ, f ξ = m ξ * sechSource N ξ)
    {ζ : ℂ} (hz : IsEigenvalue (𝓕⁻ f : 𝓢(ℝ, ℂ)) ζ) :
    (2 * k + 2 : ℝ) ^ (2 * k + 2) * ζ.im ^ (2 * k + 1) ≤
      2 * (2 * k + 1 : ℝ) ^ (2 * k + 1) * N ^ (2 * k + 2) :=
  sech_source_polynomial_ceiling k hN (sechSource_spec hN) m hm hf hz

end ZS
