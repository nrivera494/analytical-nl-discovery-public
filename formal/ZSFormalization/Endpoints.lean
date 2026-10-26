module

public import ZSFormalization.BoundState

@[expose] public section

/-! # Endpoint behavior derived from the L² bound state -/

open MeasureTheory Filter Complex Set
open scoped Topology

namespace ZS

lemma cross_abs_bound (q a b : ℂ) :
    |(q * b * star a).re| ≤ ‖q‖ * (‖a‖ ^ 2 + ‖b‖ ^ 2) / 2 := by
  have h := Complex.abs_re_le_norm (q * b * star a)
  simp only [norm_mul, norm_star] at h
  nlinarith [mul_nonneg (norm_nonneg q) (sq_nonneg (‖a‖ - ‖b‖))]

lemma cross_integrable {q : ℝ → ℂ} {ζ : ℂ} {v₁ v₂ : ℝ → ℂ}
    (hq : Continuous q) (hv : SolvesZS q ζ v₁ v₂)
    (h₁ : MemLp v₁ 2 volume) (h₂ : MemLp v₂ 2 volume)
    {Q : ℝ} (hQ : ∀ t, ‖q t‖ ≤ Q) :
    Integrable (fun t => (q t * v₂ t * star (v₁ t)).re) := by
  have hi₁ := (memLp_two_iff_integrable_sq_norm h₁.aestronglyMeasurable).mp h₁
  have hi₂ := (memLp_two_iff_integrable_sq_norm h₂.aestronglyMeasurable).mp h₂
  have hc₁ : Continuous v₁ := continuous_iff_continuousAt.mpr (fun t => (hv.1 t).continuousAt)
  have hc₂ : Continuous v₂ := continuous_iff_continuousAt.mpr (fun t => (hv.2 t).continuousAt)
  apply (((hi₁.add hi₂).const_mul Q).div_const 2).mono' (by fun_prop)
  filter_upwards with t
  rw [Real.norm_eq_abs]
  exact (cross_abs_bound (q t) (v₁ t) (v₂ t)).trans
    (div_le_div_of_nonneg_right (mul_le_mul_of_nonneg_right (hQ t) (by positivity)) (by norm_num))

lemma component_limits_atTop {q : ℝ → ℂ} {ζ : ℂ} {v₁ v₂ : ℝ → ℂ}
    (hq : Continuous q) (hv : SolvesZS q ζ v₁ v₂)
    (h₁ : MemLp v₁ 2 volume) (h₂ : MemLp v₂ 2 volume)
    {Q : ℝ} (hQ : ∀ t, ‖q t‖ ≤ Q) :
    Tendsto (fun t => ‖v₁ t‖ ^ 2) atTop (𝓝 0) ∧
      Tendsto (fun t => ‖v₂ t‖ ^ 2) atTop (𝓝 0) := by
  have hi₁ := (memLp_two_iff_integrable_sq_norm h₁.aestronglyMeasurable).mp h₁
  have hi₂ := (memLp_two_iff_integrable_sq_norm h₂.aestronglyMeasurable).mp h₂
  have hc := cross_integrable hq hv h₁ h₂ hQ
  constructor
  · exact tendsto_zero_of_hasDerivAt_of_integrableOn_Ioi (a := 0)
      (fun t _ => component_one_derivative hv t)
      (((hi₁.const_mul (2 * ζ.im)).add (hc.const_mul 2)).integrableOn) hi₁.integrableOn
  · exact tendsto_zero_of_hasDerivAt_of_integrableOn_Ioi (a := 0)
      (fun t _ => component_two_derivative hv t)
      (((hi₂.const_mul (-2 * ζ.im)).sub (hc.const_mul 2)).integrableOn) hi₂.integrableOn

lemma weighted_density_eventually_nonpos {q : ℝ → ℂ} {ζ : ℂ} {v₁ v₂ : ℝ → ℂ}
    (hv : SolvesZS q ζ v₁ v₂) (hη : 0 < ζ.im)
    (hl₁ : Tendsto (fun t => ‖v₁ t‖ ^ 2) atTop (𝓝 0))
    (hl₂ : Tendsto (fun t => ‖v₂ t‖ ^ 2) atTop (𝓝 0))
    (hq0 : Tendsto (fun t => ‖q t‖) atTop (𝓝 0))
    {c : ℝ} (hc : 0 < c) (hc' : c ≤ 1 / 2) :
    ∀ᶠ t in atTop, ‖v₁ t‖ ^ 2 - c * spinorMass v₁ v₂ t ≤ 0 := by
  let w := fun t => ‖v₁ t‖ ^ 2 - c * spinorMass v₁ v₂ t
  let w' := fun t => 2 * ζ.im * ‖v₁ t‖ ^ 2 +
      2 * (q t * v₂ t * star (v₁ t)).re - c * (2 * ζ.im * (‖v₁ t‖ ^ 2 - ‖v₂ t‖ ^ 2))
  have hd : ∀ t, HasDerivAt w (w' t) t := fun t =>
    (component_one_derivative hv t).sub ((spinorMass_derivative hv t).const_mul c)
  have hwlim : Tendsto w atTop (𝓝 0) := by
    simpa only [w, spinorMass, sub_zero, mul_zero, add_zero] using hl₁.sub ((hl₁.add hl₂).const_mul c)
  obtain ⟨T, hT⟩ := eventually_atTop.mp (hq0.eventually (gt_mem_nhds (show (0 : ℝ) < 2 * ζ.im * c by positivity)))
  have hpos : ∀ t, T ≤ t → 0 ≤ w' t := by
    intro t ht
    have hcross := (abs_le.mp (cross_abs_bound (q t) (v₁ t) (v₂ t))).1
    have hqt := hT t ht
    have hprod := mul_nonneg (show 0 ≤ 2 * ζ.im * c - ‖q t‖ by linarith)
      (show 0 ≤ ‖v₁ t‖ ^ 2 + ‖v₂ t‖ ^ 2 by positivity)
    have hprod' := mul_nonneg (mul_nonneg (mul_nonneg (by norm_num : (0 : ℝ) ≤ 2) hη.le) (show 0 ≤ 1 - 2 * c by linarith))
      (sq_nonneg ‖v₁ t‖)
    dsimp only [w']
    nlinarith only [hcross, hprod, hprod']
  have hmono : MonotoneOn w (Ici T) := by
    apply monotoneOn_of_deriv_nonneg (convex_Ici T)
      (continuous_iff_continuousAt.mpr (fun t => (hd t).continuousAt)).continuousOn
      (fun t _ => (hd t).differentiableAt.differentiableWithinAt)
    intro t ht
    rw [(hd t).deriv]
    exact hpos t (interior_subset ht)
  filter_upwards [eventually_ge_atTop T] with t ht
  apply ge_of_tendsto hwlim
  filter_upwards [eventually_ge_atTop t] with s hs
  exact hmono ht (le_trans ht hs) hs

theorem polarization_tendsto_atTop {q : ℝ → ℂ} {ζ : ℂ} {v₁ v₂ : ℝ → ℂ}
    (hq : Continuous q) (hv : SolvesZS q ζ v₁ v₂) (hη : 0 < ζ.im)
    (h₁ : MemLp v₁ 2 volume) (h₂ : MemLp v₂ 2 volume)
    (hne : ∃ t, v₁ t ≠ 0 ∨ v₂ t ≠ 0)
    {Q : ℝ} (hQ : ∀ t, ‖q t‖ ≤ Q)
    (hq0 : Tendsto (fun t => ‖q t‖) atTop (𝓝 0)) :
    Tendsto (polarization v₁ v₂) atTop (𝓝 (-1)) := by
  obtain ⟨hl₁, hl₂⟩ := component_limits_atTop hq hv h₁ h₂ hQ
  apply tendsto_order.mpr
  constructor
  · intro a ha
    exact Filter.Eventually.of_forall (fun t => ha.trans_le (polarization_mem_Icc v₁ v₂ t (spinorMass_pos hv hne t)).1)
  · intro b hb
    let c := min ((b + 1) / 4) (1 / 4 : ℝ)
    have hc : 0 < c := lt_min (by linarith) (by norm_num)
    have hc' : c ≤ 1 / 2 := (min_le_right _ _).trans (by norm_num)
    filter_upwards [weighted_density_eventually_nonpos hv hη hl₁ hl₂ hq0 hc hc'] with t ht
    have hp := spinorMass_pos hv hne t
    rw [polarization, div_lt_iff₀ hp]
    have hcb : 2 * c < b + 1 := by have := min_le_left ((b + 1) / 4) (1 / 4 : ℝ); dsimp [c]; linarith
    have hpos := mul_pos (show 0 < b + 1 - 2 * c by linarith) hp
    unfold spinorMass at *
    nlinarith

lemma SolvesZS.reflect {q : ℝ → ℂ} {ζ : ℂ} {v₁ v₂ : ℝ → ℂ}
    (hv : SolvesZS q ζ v₁ v₂) :
    SolvesZS (fun t => star (q (-t))) ζ (fun t => v₂ (-t)) (fun t => v₁ (-t)) := by
  constructor
  · intro t
    convert (hv.2 (-t)).scomp t (hasDerivAt_neg t) using 1
    · rfl
    · simp only [neg_one_smul]
      ring
  · intro t
    convert (hv.1 (-t)).scomp t (hasDerivAt_neg t) using 1
    · rfl
    · simp only [star_star, neg_one_smul]
      ring

theorem polarization_tendsto_atBot {q : ℝ → ℂ} {ζ : ℂ} {v₁ v₂ : ℝ → ℂ}
    (hq : Continuous q) (hv : SolvesZS q ζ v₁ v₂) (hη : 0 < ζ.im)
    (h₁ : MemLp v₁ 2 volume) (h₂ : MemLp v₂ 2 volume)
    (hne : ∃ t, v₁ t ≠ 0 ∨ v₂ t ≠ 0)
    {Q : ℝ} (hQ : ∀ t, ‖q t‖ ≤ Q)
    (hq0 : Tendsto (fun t => ‖q t‖) atBot (𝓝 0)) :
    Tendsto (polarization v₁ v₂) atBot (𝓝 1) := by
  have hm₁ : MemLp (fun t => v₂ (-t)) 2 volume :=
    h₂.comp_measurePreserving (Measure.measurePreserving_neg volume)
  have hm₂ : MemLp (fun t => v₁ (-t)) 2 volume :=
    h₁.comp_measurePreserving (Measure.measurePreserving_neg volume)
  have hn : ∃ t, v₂ (-t) ≠ 0 ∨ v₁ (-t) ≠ 0 := by
    obtain ⟨t, ht⟩ := hne
    exact ⟨-t, by simpa only [neg_neg, or_comm] using ht⟩
  have hb : ∀ t, ‖star (q (-t))‖ ≤ Q := by simpa only [norm_star] using fun t => hQ (-t)
  have hlim : Tendsto (fun t => ‖star (q (-t))‖) atTop (𝓝 0) := by
    simpa only [norm_star, Function.comp_def] using hq0.comp tendsto_neg_atTop_atBot
  have hh := polarization_tendsto_atTop ((hq.comp continuous_neg).star) hv.reflect hη hm₁ hm₂ hn hb hlim
  have hh' := hh.neg.comp tendsto_neg_atBot_atTop
  convert hh' using 1
  · funext t
    simp only [Function.comp_def, polarization, spinorMass, neg_neg]
    ring
  · norm_num

end ZS
