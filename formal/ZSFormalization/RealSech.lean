module

public import ZSFormalization.Sources

@[expose] public section

/-! # The explicit sech eigenvalue for every real order above one half -/

open MeasureTheory Filter Set FourierTransform
open scoped Topology SchwartzMap

namespace ZS

lemma sech_rpow_derivative (N t : ℝ) :
    HasDerivAt (fun t => sech t ^ N) (-N * Real.tanh t * sech t ^ N) t := by
  convert (sech_derivative t).rpow_const (p := N) (Or.inl (sech_pos t).ne') using 1
  rw [Real.rpow_sub_one (sech_pos t).ne']
  field_simp [(sech_pos t).ne']

lemma sech_rpow_integrable {r : ℝ} (hr : 0 < r) : Integrable (fun t => sech t ^ r) := by
  have hc : Continuous (fun t => sech t ^ r) :=
    continuous_iff_continuousAt.mpr (fun t => (sech_rpow_derivative r t).continuousAt)
  have hb (t : ℝ) : sech t ^ r ≤ (2 : ℝ) ^ r * Real.exp (-r * |t|) := by
    calc
      _ ≤ (2 * Real.exp (-|t|)) ^ r :=
        Real.rpow_le_rpow (sech_pos t).le (sech_exp_bound t) hr.le
      _ = _ := by
        rw [Real.mul_rpow (by norm_num) (Real.exp_pos _).le, ← Real.exp_mul]
        congr 2
        ring
  have hl : IntegrableOn (fun t => sech t ^ r) (Iic 0) := by
    apply ((integrableOn_exp_mul_Iic hr 0).const_mul ((2 : ℝ) ^ r)).mono' hc.aestronglyMeasurable
    filter_upwards [ae_restrict_mem measurableSet_Iic] with t ht
    change ‖sech t ^ r‖ ≤ (2 : ℝ) ^ r * Real.exp (r * t)
    rw [Real.norm_eq_abs, abs_of_pos (Real.rpow_pos_of_pos (sech_pos t) r)]
    simpa only [abs_of_nonpos ht, mul_neg, neg_mul, neg_neg] using hb t
  have ht : IntegrableOn (fun t => sech t ^ r) (Ioi 0) := by
    apply ((integrableOn_exp_mul_Ioi (neg_neg_of_pos hr) 0).const_mul ((2 : ℝ) ^ r)).mono' hc.aestronglyMeasurable
    filter_upwards [ae_restrict_mem measurableSet_Ioi] with t ht
    change ‖sech t ^ r‖ ≤ (2 : ℝ) ^ r * Real.exp (-r * t)
    rw [Real.norm_eq_abs, abs_of_pos (Real.rpow_pos_of_pos (sech_pos t) r)]
    simpa only [abs_of_pos ht] using hb t
  rw [← integrableOn_univ, ← Iic_union_Ioi (a := (0 : ℝ))]
  exact hl.union ht

noncomputable def realSechSpinorOne (N t : ℝ) : ℝ := Real.exp (-t / 2) * sech t ^ N
noncomputable def realSechSpinorTwo (N t : ℝ) : ℝ := -Real.exp (t / 2) * sech t ^ N

lemma realSechSpinorOne_derivative (N t : ℝ) :
    HasDerivAt (realSechSpinorOne N)
      ((-1 / 2 - N * Real.tanh t) * realSechSpinorOne N t) t := by
  convert ((((hasDerivAt_id t).neg).div_const (2 : ℝ)).exp).mul (sech_rpow_derivative N t) using 1
  · rfl
  · simp only [Pi.neg_apply, id_eq]
    unfold realSechSpinorOne
    ring

lemma realSechSpinorTwo_derivative (N t : ℝ) :
    HasDerivAt (realSechSpinorTwo N)
      ((1 / 2 - N * Real.tanh t) * realSechSpinorTwo N t) t := by
  convert ((((hasDerivAt_id t).div_const (2 : ℝ)).exp).neg).mul (sech_rpow_derivative N t) using 1
  · rfl
  · simp only [Pi.neg_apply, id_eq]
    unfold realSechSpinorTwo
    ring

lemma realSechSpinor_square_sum (N t : ℝ) :
    realSechSpinorOne N t ^ 2 + realSechSpinorTwo N t ^ 2 =
      2 * sech t ^ (2 * N - 1) := by
  have h₁ : Real.exp (-t / 2) ^ 2 = Real.exp (-t) := by
    rw [sq, ← Real.exp_add]; congr 1; ring
  have h₂ : Real.exp (t / 2) ^ 2 = Real.exp t := by
    rw [sq, ← Real.exp_add]; congr 1; ring
  have hp : (sech t ^ N) ^ (2 : ℕ) = sech t ^ (2 * N - 1) * sech t := by
    rw [← Real.rpow_natCast (sech t ^ N) 2, ← Real.rpow_mul (sech_pos t).le]
    norm_num only [Nat.cast_ofNat]
    rw [show N * (2 : ℝ) = (2 * N - 1) + 1 by ring, Real.rpow_add (sech_pos t), Real.rpow_one]
  unfold realSechSpinorOne realSechSpinorTwo
  simp only [mul_pow, neg_sq, h₁, h₂, hp]
  calc
    _ = (Real.exp t + Real.exp (-t)) * sech t * sech t ^ (2 * N - 1) := by ring
    _ = 2 * Real.cosh t * sech t * sech t ^ (2 * N - 1) := by rw [Real.cosh_eq]; ring
    _ = _ := by unfold sech; field_simp

lemma realSechSpinor_coupling_one (N t : ℝ) :
    sech t * realSechSpinorTwo N t = -(1 + Real.tanh t) * realSechSpinorOne N t := by
  have he : Real.exp t * Real.exp (-t / 2) = Real.exp (t / 2) := by
    rw [← Real.exp_add]; congr 1; ring
  have hh : sech t * Real.exp t = 1 + Real.tanh t := by
    rw [← Real.cosh_add_sinh, Real.tanh_eq_sinh_div_cosh]
    unfold sech
    field_simp
  unfold realSechSpinorOne realSechSpinorTwo
  rw [← he, ← hh]
  ring

lemma realSechSpinor_coupling_two (N t : ℝ) :
    sech t * realSechSpinorOne N t = -(1 - Real.tanh t) * realSechSpinorTwo N t := by
  have he : Real.exp (-t) * Real.exp (t / 2) = Real.exp (-t / 2) := by
    rw [← Real.exp_add]; congr 1; ring
  have hh : sech t * Real.exp (-t) = 1 - Real.tanh t := by
    rw [← Real.cosh_sub_sinh, Real.tanh_eq_sinh_div_cosh]
    unfold sech
    field_simp
  unfold realSechSpinorOne realSechSpinorTwo
  rw [← he, ← hh]
  ring

theorem realSechSpinor_solves (N : ℝ) :
    SolvesZS (fun t => ((N * sech t : ℝ) : ℂ)) (Complex.I * ((N - 1 / 2 : ℝ) : ℂ))
      (fun t => (realSechSpinorOne N t : ℂ)) (fun t => (realSechSpinorTwo N t : ℂ)) := by
  constructor
  · intro t
    convert (realSechSpinorOne_derivative N t).ofReal_comp using 1
    have h := congrArg (fun z : ℝ => N * z) (realSechSpinor_coupling_one N t)
    simp only [Real.tanh] at h
    apply Complex.ext <;> simp [Complex.mul_re, Complex.mul_im]
    nlinarith only [h]
  · intro t
    convert (realSechSpinorTwo_derivative N t).ofReal_comp using 1
    have h := congrArg (fun z : ℝ => N * z) (realSechSpinor_coupling_two N t)
    simp only [Real.tanh] at h
    apply Complex.ext <;> simp [Complex.mul_re, Complex.mul_im]
    nlinarith only [h]

theorem real_sech_has_eigenvalue {N : ℝ} (hN : 1 / 2 < N) :
    IsEigenvalue (fun t => ((N * sech t : ℝ) : ℂ)) (Complex.I * ((N - 1 / 2 : ℝ) : ℂ)) := by
  have hi := (sech_rpow_integrable (r := 2 * N - 1) (by linarith)).const_mul 2
  have hc₁ : Continuous (fun t => (realSechSpinorOne N t : ℂ)) :=
    continuous_iff_continuousAt.mpr (fun t => (realSechSpinorOne_derivative N t).ofReal_comp.continuousAt)
  have hc₂ : Continuous (fun t => (realSechSpinorTwo N t : ℂ)) :=
    continuous_iff_continuousAt.mpr (fun t => (realSechSpinorTwo_derivative N t).ofReal_comp.continuousAt)
  refine ⟨?_, _, _, realSechSpinor_solves N, ?_, ?_, ?_⟩
  · simpa using sub_pos.mpr hN
  · apply (memLp_two_iff_integrable_sq_norm hc₁.aestronglyMeasurable).mpr
    apply hi.mono' (hc₁.norm.pow 2).aestronglyMeasurable
    filter_upwards with t
    change ‖‖(realSechSpinorOne N t : ℂ)‖ ^ 2‖ ≤ 2 * sech t ^ (2 * N - 1)
    simp only [Complex.norm_real, Real.norm_eq_abs, sq_abs, abs_sq]
    nlinarith only [realSechSpinor_square_sum N t, sq_nonneg (realSechSpinorTwo N t)]
  · apply (memLp_two_iff_integrable_sq_norm hc₂.aestronglyMeasurable).mpr
    apply hi.mono' (hc₂.norm.pow 2).aestronglyMeasurable
    filter_upwards with t
    change ‖‖(realSechSpinorTwo N t : ℂ)‖ ^ 2‖ ≤ 2 * sech t ^ (2 * N - 1)
    simp only [Complex.norm_real, Real.norm_eq_abs, sq_abs, abs_sq]
    nlinarith only [realSechSpinor_square_sum N t, sq_nonneg (realSechSpinorOne N t)]
  · exact ⟨0, Or.inl (by simp [realSechSpinorOne, sech])⟩

theorem canonical_sech_baseline_attains {N : ℝ} (hN : 1 / 2 < N) :
    N - 1 / 2 ∈ attainableHeights (sechSource N) := by
  have hs := sechSource_spec (N := N) (by linarith)
  refine ⟨sechSource N, (fun _ => 1), Complex.I * ((N - 1 / 2 : ℝ) : ℂ),
    (by intro ξ; simp), (by intro ξ; simp), ?_, by simp⟩
  have hq : (⇑(𝓕⁻ (sechSource N) : 𝓢(ℝ, ℂ)) : ℝ → ℂ) =
      fun t => ((N * sech t : ℝ) : ℂ) := funext hs.2
  rw [hq]
  exact real_sech_has_eigenvalue hN

/-- The lower endpoint is actually attained, and the upper endpoint bounds every
admissible passive mask. The certificate itself is exact real/rational arithmetic. -/
theorem rational_sech_height_enclosure (k : ℕ) {N U : ℝ}
    (hN : 1 / 2 < N) (hU : 0 ≤ U)
    (hcert : 2 * (2 * k + 1 : ℝ) ^ (2 * k + 1) * N ^ (2 * k + 2) ≤
      (2 * k + 2 : ℝ) ^ (2 * k + 2) * U ^ (2 * k + 1)) :
    N - 1 / 2 ∈ attainableHeights (sechSource N) ∧
      ∀ η ∈ attainableHeights (sechSource N), η ≤ U := by
  refine ⟨canonical_sech_baseline_attains hN, ?_⟩
  rintro η ⟨f, m, ζ, hm, hf, hz, rfl⟩
  exact rational_sech_ceiling k (by linarith) hU hcert
    (sechSource_spec (by linarith)) m hm hf hz

theorem canonical_sech_five_halves_enclosure :
    (2 : ℝ) ∈ attainableHeights (sechSource (5 / 2)) ∧
      ∀ η ∈ attainableHeights (sechSource (5 / 2)),
        η ≤ 2 * (1 + 43672 / 10000000 : ℝ) := by
  convert rational_sech_height_enclosure 2 (N := 5 / 2)
    (U := 2 * (1 + 43672 / 10000000)) (by norm_num) (by norm_num) (by norm_num) using 1
  norm_num

theorem canonical_sech_seven_halves_enclosure :
    (3 : ℝ) ∈ attainableHeights (sechSource (7 / 2)) ∧
      ∀ η ∈ attainableHeights (sechSource (7 / 2)),
        η ≤ 3 * (1 + 15446 / 10000000 : ℝ) := by
  convert rational_sech_height_enclosure 3 (N := 7 / 2)
    (U := 3 * (1 + 15446 / 10000000)) (by norm_num) (by norm_num) (by norm_num) using 1
  norm_num

theorem canonical_sech_eleven_halves_enclosure :
    (5 : ℝ) ∈ attainableHeights (sechSource (11 / 2)) ∧
      ∀ η ∈ attainableHeights (sechSource (11 / 2)),
        η ≤ 5 * (1 + 3888 / 10000000 : ℝ) := by
  convert rational_sech_height_enclosure 5 (N := 11 / 2)
    (U := 5 * (1 + 3888 / 10000000)) (by norm_num) (by norm_num) (by norm_num) using 1
  norm_num

theorem canonical_sech_nineteen_halves_enclosure :
    (9 : ℝ) ∈ attainableHeights (sechSource (19 / 2)) ∧
      ∀ η ∈ attainableHeights (sechSource (19 / 2)),
        η ≤ 9 * (1 + 743 / 10000000 : ℝ) := by
  convert rational_sech_height_enclosure 9 (N := 19 / 2)
    (U := 9 * (1 + 743 / 10000000)) (by norm_num) (by norm_num) (by norm_num) using 1
  norm_num

end ZS
