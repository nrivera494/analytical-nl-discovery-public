module

public import ZSFormalization.Scalar
public import ZSFormalization.BoundState

@[expose] public section

/-! # The sharp even-moment estimate -/

open MeasureTheory Filter Set
open scoped Topology

namespace ZS

noncomputable def momentPrimitive (k : ℕ) (x : ℝ) : ℝ :=
  ∫ s in 0..x, (1 - s ^ 2) ^ k

lemma momentPrimitive_derivative (k : ℕ) (x : ℝ) :
    HasDerivAt (momentPrimitive k) ((1 - x ^ 2) ^ k) x := by
  have hc : Continuous (fun s : ℝ => (1 - s ^ 2) ^ k) := by fun_prop
  exact intervalIntegral.integral_hasDerivAt_right (hc.intervalIntegrable _ _)
    hc.aestronglyMeasurable.stronglyMeasurableAtFilter hc.continuousAt

lemma weighted_differential_estimate (k : ℕ) {η r x xp : ℝ}
    (hη : 0 ≤ η) (hr : 0 ≤ r) (hx : x ∈ Icc (-1) 1)
    (hd : 2 * η * (1 - x ^ 2) - 2 * r * Real.sqrt (1 - x ^ 2) ≤ xp) :
    -(2 * k + 2 : ℝ) ^ (2 * k + 2) * η ^ (2 * k + 1) * (1 - x ^ 2) ^ k * xp ≤
      2 * (2 * k + 1 : ℝ) ^ (2 * k + 1) * r ^ (2 * k + 2) := by
  have hw : 0 ≤ 1 - x ^ 2 := by nlinarith [hx.1, hx.2]
  let u := Real.sqrt (1 - x ^ 2)
  have hu : u ^ 2 = 1 - x ^ 2 := Real.sq_sqrt hw
  have hus : (η * u) ^ (2 * k + 1) = η ^ (2 * k + 1) * (1 - x ^ 2) ^ k * u := by
    rw [mul_pow, pow_succ u, pow_mul u 2 k, hu]
    ring
  have hs := sharp_scalar (2 * k) (s := η * u) hr (mul_nonneg hη (Real.sqrt_nonneg (1 - x ^ 2)))
  norm_num only [Nat.cast_mul, Nat.cast_ofNat] at hs
  change (2 * k + 2 : ℝ) ^ (2 * k + 2) * (η * u) ^ (2 * k + 1) * (r - η * u) ≤ _ at hs
  rw [hus] at hs
  have hmul := mul_le_mul_of_nonneg_left hd
    (show 0 ≤ (2 * k + 2 : ℝ) ^ (2 * k + 2) * η ^ (2 * k + 1) * (1 - x ^ 2) ^ k by positivity)
  change (2 * k + 2 : ℝ) ^ (2 * k + 2) * η ^ (2 * k + 1) * (1 - x ^ 2) ^ k *
    (2 * η * (1 - x ^ 2) - 2 * r * u) ≤ _ at hmul
  have heq : (2 * k + 2 : ℝ) ^ (2 * k + 2) * η ^ (2 * k + 1) * (1 - x ^ 2) ^ k *
      (2 * η * (1 - x ^ 2) - 2 * r * u) =
      -2 * ((2 * k + 2 : ℝ) ^ (2 * k + 2) * (η ^ (2 * k + 1) * (1 - x ^ 2) ^ k * u) * (r - η * u)) := by
    rw [← hu]
    ring
  rw [heq] at hmul
  nlinarith only [hs, hmul]

lemma momentPrimitive_jump (k : ℕ) :
    momentPrimitive k 1 - momentPrimitive k (-1) = ∫ s in (-1 : ℝ)..1, (1 - s ^ 2) ^ k := by
  have hc : Continuous (fun s : ℝ => (1 - s ^ 2) ^ k) := by fun_prop
  exact intervalIntegral.integral_interval_sub_left (hc.intervalIntegrable _ _) (hc.intervalIntegrable _ _)

/-- Integrating the pointwise estimate requires no monotonicity of `x`. -/
theorem moment_bound_of_differential_inequality (k : ℕ) {r x xp : ℝ → ℝ} {η : ℝ}
    (hη : 0 ≤ η) (hr : ∀ t, 0 ≤ r t) (hrc : Continuous r)
    (hd : ∀ t, HasDerivAt x (xp t) t) (hxp : Continuous xp)
    (hx : ∀ t, x t ∈ Icc (-1) 1)
    (hi : ∀ t, 2 * η * (1 - x t ^ 2) - 2 * r t * Real.sqrt (1 - x t ^ 2) ≤ xp t)
    (hleft : Tendsto x atBot (𝓝 1)) (hright : Tendsto x atTop (𝓝 (-1)))
    (hint : Integrable (fun t => r t ^ (2 * k + 2))) :
    (2 * k + 2 : ℝ) ^ (2 * k + 2) * η ^ (2 * k + 1) *
        (∫ s in (-1 : ℝ)..1, (1 - s ^ 2) ^ k) ≤
      2 * (2 * k + 1 : ℝ) ^ (2 * k + 1) * ∫ t, r t ^ (2 * k + 2) := by
  let A : ℝ := (2 * k + 2 : ℝ) ^ (2 * k + 2) * η ^ (2 * k + 1)
  let B : ℝ := 2 * (2 * k + 1 : ℝ) ^ (2 * k + 1)
  have hxc : Continuous x := continuous_iff_continuousAt.mpr (fun t => (hd t).continuousAt)
  have hpc : Continuous (momentPrimitive k) :=
    continuous_iff_continuousAt.mpr (fun t => (momentPrimitive_derivative k t).continuousAt)
  have hdc : Continuous (fun t => (1 - x t ^ 2) ^ k * xp t) := by fun_prop
  have hpd : ∀ t, HasDerivAt (fun s => momentPrimitive k (x s)) ((1 - x t ^ 2) ^ k * xp t) t := by
    intro t
    simpa only [Function.comp_def] using (momentPrimitive_derivative k (x t)).comp t (hd t)
  have hfin : ∀ a b : ℝ, a ≤ b →
      A * (momentPrimitive k (x a) - momentPrimitive k (x b)) ≤ B * ∫ t in a..b, r t ^ (2 * k + 2) := by
    intro a b hab
    have hpw : ∀ t, -A * ((1 - x t ^ 2) ^ k * xp t) ≤ B * r t ^ (2 * k + 2) := by
      intro t
      convert weighted_differential_estimate k hη (hr t) (hx t) (hi t) using 1
      dsimp [A, B]
      ring
    have hh := intervalIntegral.integral_mono_on (μ := volume) hab
      ((hdc.const_mul (-A)).intervalIntegrable a b)
      (((hrc.pow (2 * k + 2)).const_mul B).intervalIntegrable a b) (fun t _ => hpw t)
    rw [intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul,
      intervalIntegral.integral_eq_sub_of_hasDerivAt (fun t _ => hpd t) (hdc.intervalIntegrable a b)] at hh
    simp only [Pi.pow_apply] at hh
    nlinarith only [hh]
  have hlimL : Tendsto (fun T => A * (momentPrimitive k (x (-T)) - momentPrimitive k (x T)))
      atTop (𝓝 (A * (momentPrimitive k 1 - momentPrimitive k (-1)))) :=
    ((hpc.continuousAt.tendsto.comp (hleft.comp tendsto_neg_atTop_atBot)).sub
      (hpc.continuousAt.tendsto.comp hright)).const_mul A
  have hlimR : Tendsto (fun T => B * ∫ t in -T..T, r t ^ (2 * k + 2))
      atTop (𝓝 (B * ∫ t, r t ^ (2 * k + 2))) :=
    (intervalIntegral_tendsto_integral hint tendsto_neg_atTop_atBot tendsto_id).const_mul B
  have hh := le_of_tendsto_of_tendsto hlimL hlimR (by
    filter_upwards [eventually_ge_atTop (0 : ℝ)] with T hT
    exact hfin (-T) T (by linarith))
  rw [momentPrimitive_jump] at hh
  exact hh

end ZS
