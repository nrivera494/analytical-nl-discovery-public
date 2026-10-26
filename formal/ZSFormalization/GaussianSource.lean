module

public import ZSFormalization.Sources

@[expose] public section

/-! # A concrete Gaussian source and its Fourier pair -/

open MeasureTheory Filter Set FourierTransform
open scoped Topology SchwartzMap ZeroAtInfty

namespace ZS

noncomputable def gaussianCore (t : ℝ) : ℝ := Real.exp (-(1 / 2 : ℝ) * t ^ 2)

lemma gaussianCore_derivative (t : ℝ) :
    HasDerivAt gaussianCore (-t * gaussianCore t) t := by
  convert (((hasDerivAt_id t).pow 2).const_mul (-(1 / 2 : ℝ))).exp using 1
  · rfl
  · simp only [Pi.pow_apply, id_eq, Nat.cast_ofNat, Nat.reduceSub, pow_one]
    unfold gaussianCore
    ring

noncomputable def gaussianDerivPoly : ℕ → Polynomial ℝ
  | 0 => 1
  | n + 1 => -Polynomial.X * gaussianDerivPoly n + (gaussianDerivPoly n).derivative

lemma gaussianCore_iteratedDeriv (n : ℕ) (t : ℝ) :
    iteratedDeriv n gaussianCore t = gaussianCore t * (gaussianDerivPoly n).eval t := by
  induction n generalizing t with
  | zero => simp [gaussianDerivPoly]
  | succ n ih =>
    rw [iteratedDeriv_succ, show iteratedDeriv n gaussianCore =
      (fun t => gaussianCore t * (gaussianDerivPoly n).eval t) from funext ih]
    have hd := ((gaussianCore_derivative t).mul ((gaussianDerivPoly n).hasDerivAt t)).deriv
    change deriv (fun t => gaussianCore t * (gaussianDerivPoly n).eval t) t = _ at hd
    rw [hd]
    simp only [gaussianDerivPoly, Polynomial.eval_add, Polynomial.eval_mul, Polynomial.eval_neg,
      Polynomial.eval_X]
    ring

lemma gaussianCore_monomial_tendsto (n : ℕ) :
    Tendsto (fun t : ℝ => t ^ n * gaussianCore t) (cocompact ℝ) (𝓝 0) := by
  apply (tendsto_zero_iff_norm_tendsto_zero).mpr
  have h := tendsto_rpow_abs_mul_exp_neg_mul_sq_cocompact
    (by norm_num : (0 : ℝ) < 1 / 2) (n : ℝ)
  simpa only [Real.rpow_natCast, norm_mul, norm_pow, Real.norm_eq_abs,
    gaussianCore, abs_of_pos (Real.exp_pos _)] using h

lemma gaussianCore_polynomial_tendsto (p : Polynomial ℝ) (k : ℕ) :
    Tendsto (fun t : ℝ => t ^ k * p.eval t * gaussianCore t) (cocompact ℝ) (𝓝 0) := by
  induction p using Polynomial.induction_on' with
  | add p q hp hq =>
    convert hp.add hq using 1
    · funext t; simp only [Polynomial.eval_add]; ring
    · norm_num
  | monomial n a =>
    convert (gaussianCore_monomial_tendsto (k + n)).const_mul a using 1
    · funext t
      simp only [Polynomial.eval_monomial, pow_add]
      ring
    · norm_num

noncomputable def gaussianSchwartzReal : 𝓢(ℝ, ℝ) where
  toFun := gaussianCore
  smooth' := by unfold gaussianCore; fun_prop
  decay' k n := by
    let f : C₀(ℝ, ℝ) := {
      toFun := fun t => t ^ k * (gaussianDerivPoly n).eval t * gaussianCore t
      continuous_toFun := by unfold gaussianCore; fun_prop
      zero_at_infty' := gaussianCore_polynomial_tendsto (gaussianDerivPoly n) k }
    obtain ⟨C, hC⟩ := isBounded_iff_forall_norm_le.mp f.isBounded_range
    refine ⟨C, fun t => ?_⟩
    have ht := hC (f t) (mem_range_self t)
    change ‖t ^ k * (gaussianDerivPoly n).eval t * gaussianCore t‖ ≤ C at ht
    rw [norm_iteratedFDeriv_eq_norm_iteratedDeriv, gaussianCore_iteratedDeriv]
    change ‖t‖ ^ k * ‖gaussianCore t * (gaussianDerivPoly n).eval t‖ ≤ C
    simpa only [norm_mul, norm_pow, mul_assoc, mul_left_comm, mul_comm] using ht

noncomputable def gaussianSchwartz (N : ℝ) : 𝓢(ℝ, ℂ) :=
  N • SchwartzMap.postcompCLM Complex.ofRealCLM gaussianSchwartzReal

@[simp] lemma gaussianSchwartz_apply (N t : ℝ) :
    gaussianSchwartz N t = (gaussianPulse N t : ℂ) := by
  change N • (gaussianCore t : ℂ) = _
  simp only [Complex.real_smul, gaussianCore, gaussianPulse, Complex.ofReal_mul]
  congr 2
  congr 1
  ring

lemma fourier_const_mul_complex (a : ℂ) (h : ℝ → ℂ) (ξ : ℝ) :
    𝓕 (fun t => a * h t) ξ = a * 𝓕 h ξ := by
  simp only [Real.fourier_real_eq_integral_exp_smul, smul_eq_mul]
  rw [← integral_const_mul]
  congr 1; funext t; ring

lemma gaussianCore_fourier (ξ : ℝ) :
    𝓕 (fun t => (gaussianCore t : ℂ)) ξ =
      ((Real.sqrt (2 * Real.pi) * Real.exp (-2 * Real.pi ^ 2 * ξ ^ 2) : ℝ) : ℂ) := by
  have h := fourierIntegral_gaussian (b := (1 / 2 : ℂ)) (by norm_num)
    (-2 * (Real.pi : ℂ) * (ξ : ℂ))
  have hl : 𝓕 (fun t => (gaussianCore t : ℂ)) ξ =
      ∫ t : ℝ, Complex.exp (Complex.I * (-2 * (Real.pi : ℂ) * (ξ : ℂ)) * (t : ℂ)) *
        Complex.exp (-(1 / 2 : ℂ) * (t : ℂ) ^ 2) := by
    rw [Real.fourier_real_eq_integral_exp_smul]
    congr 1; funext t
    simp only [smul_eq_mul, gaussianCore, Complex.ofReal_exp]
    congr 1 <;> congr 1 <;> push_cast <;> ring
  rw [hl, h]
  have hp : ((Real.pi : ℂ) / (1 / 2 : ℂ)) ^ (1 / 2 : ℂ) =
      (Real.sqrt (2 * Real.pi) : ℂ) := by
    rw [Real.sqrt_eq_rpow, Complex.ofReal_cpow (by positivity)]
    congr 1 <;> push_cast <;> ring
  rw [hp, Complex.ofReal_mul, Complex.ofReal_exp]
  congr 1
  congr 1
  push_cast
  ring

noncomputable def gaussianSource (N : ℝ) : 𝓢(ℝ, ℂ) := 𝓕 (gaussianSchwartz N)

theorem gaussianSource_apply (N ξ : ℝ) :
    gaussianSource N ξ =
      ((N * Real.sqrt (2 * Real.pi) * Real.exp (-2 * Real.pi ^ 2 * ξ ^ 2) : ℝ) : ℂ) := by
  have hq : (⇑(gaussianSchwartz N) : ℝ → ℂ) =
      fun t => (N : ℂ) * (gaussianCore t : ℂ) := by
    funext t
    change N • (gaussianCore t : ℂ) = _
    simp only [Complex.real_smul]
  unfold gaussianSource
  rw [SchwartzMap.fourier_coe, hq, fourier_const_mul_complex, gaussianCore_fourier]
  push_cast
  ring

theorem gaussianSource_spec {N : ℝ} (hN : 0 ≤ N) :
    IsGaussianSource N (gaussianSource N) := by
  constructor
  · intro ξ
    rw [gaussianSource_apply, Complex.norm_real, Real.norm_eq_abs,
      abs_of_nonneg (by positivity)]
  · intro t
    simp only [gaussianSource, fourierInv_fourier_eq, gaussianSchwartz_apply]

theorem canonical_gaussian_ceiling (k : ℕ) {N : ℝ} (hN : 0 ≤ N)
    {f : 𝓢(ℝ, ℂ)} (m : ℝ → ℂ)
    (hm : ∀ ξ, ‖m ξ‖ ≤ 1) (hf : ∀ ξ, f ξ = m ξ * gaussianSource N ξ)
    {ζ : ℂ} (hz : IsEigenvalue (𝓕⁻ f : 𝓢(ℝ, ℂ)) ζ) :
    (2 * k + 2 : ℝ) ^ (2 * k + 2) * ζ.im ^ (2 * k + 1) *
        (∫ s in (-1 : ℝ)..1, (1 - s ^ 2) ^ k) ≤
      2 * (2 * k + 1 : ℝ) ^ (2 * k + 1) * N ^ (2 * k + 2) *
        Real.sqrt (Real.pi / (k + 1 : ℝ)) :=
  gaussian_source_polynomial_ceiling k hN (gaussianSource_spec hN) m hm hf hz

end ZS
