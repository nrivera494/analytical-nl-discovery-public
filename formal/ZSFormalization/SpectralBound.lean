module

public import ZSFormalization.Endpoints
public import ZSFormalization.Moment
public import ZSFormalization.FourierMajorant

@[expose] public section

/-! # Sharp bounds for actual ZS eigenvalues -/

open MeasureTheory Filter FourierTransform
open scoped Topology SchwartzMap

namespace ZS

/-- The sharp even-moment inequality for a genuine L² ZS eigenvalue.
The assumptions on `q` concern only decay, continuity, boundedness and integrability.
Both spinor endpoint limits are proved internally from its ODE and L² condition. -/
theorem eigenvalue_even_moment_bound (k : ℕ) {q : ℝ → ℂ} {ζ : ℂ}
    (hq : Continuous q) {Q : ℝ} (hQ : ∀ t, ‖q t‖ ≤ Q)
    (hleft : Tendsto (fun t => ‖q t‖) atBot (𝓝 0))
    (hright : Tendsto (fun t => ‖q t‖) atTop (𝓝 0))
    (hint : Integrable (fun t => ‖q t‖ ^ (2 * k + 2))) (hz : IsEigenvalue q ζ) :
    (2 * k + 2 : ℝ) ^ (2 * k + 2) * ζ.im ^ (2 * k + 1) *
        (∫ s in (-1 : ℝ)..1, (1 - s ^ 2) ^ k) ≤
      2 * (2 * k + 1 : ℝ) ^ (2 * k + 1) * ∫ t, ‖q t‖ ^ (2 * k + 2) := by
  obtain ⟨hη, v₁, v₂, hv, h₁, h₂, hne⟩ := hz
  let xp := fun t => 2 * ζ.im * (1 - polarization v₁ v₂ t ^ 2) +
    4 * (q t * v₂ t * star (v₁ t)).re / spinorMass v₁ v₂ t
  have hp := spinorMass_pos hv hne
  have hd : ∀ t, HasDerivAt (polarization v₁ v₂) (xp t) t :=
    fun t => polarization_derivative hv t (hp t)
  have hc₁ : Continuous v₁ := continuous_iff_continuousAt.mpr (fun t => (hv.1 t).continuousAt)
  have hc₂ : Continuous v₂ := continuous_iff_continuousAt.mpr (fun t => (hv.2 t).continuousAt)
  have hxc : Continuous (polarization v₁ v₂) :=
    continuous_iff_continuousAt.mpr (fun t => (hd t).continuousAt)
  have hmc : Continuous (spinorMass v₁ v₂) := (hc₁.norm.pow 2).add (hc₂.norm.pow 2)
  have hxpc : Continuous xp :=
    (continuous_const.mul (continuous_const.sub (hxc.pow 2))).add
      ((continuous_const.mul (Complex.continuous_re.comp ((hq.mul hc₂).mul hc₁.star))).div hmc (fun t => (hp t).ne'))
  apply moment_bound_of_differential_inequality k hη.le (fun t => norm_nonneg _) hq.norm
    hd hxpc (fun t => polarization_mem_Icc v₁ v₂ t (hp t))
  · intro t
    rw [← (hd t).deriv]
    exact polarization_differential_inequality hv hne t
  · exact polarization_tendsto_atBot hq hv hη h₁ h₂ hne hQ hleft
  · exact polarization_tendsto_atTop hq hv hη h₁ h₂ hne hQ hright
  · exact hint

/-- The entire sharp ZS estimate with the single regularity assumption `q ∈ 𝓢`. -/
theorem schwartz_eigenvalue_even_moment_bound (k : ℕ) (q : 𝓢(ℝ, ℂ)) {ζ : ℂ}
    (hz : IsEigenvalue q ζ) :
    (2 * k + 2 : ℝ) ^ (2 * k + 2) * ζ.im ^ (2 * k + 1) *
        (∫ s in (-1 : ℝ)..1, (1 - s ^ 2) ^ k) ≤
      2 * (2 * k + 1 : ℝ) ^ (2 * k + 1) * ∫ t, ‖q t‖ ^ (2 * k + 2) := by
  apply eigenvalue_even_moment_bound k q.continuous (SchwartzMap.norm_le_seminorm ℝ q)
  · simpa only [norm_zero] using (q.tendsto_cocompact.mono_left atBot_le_cocompact).norm
  · simpa only [norm_zero] using (q.tendsto_cocompact.mono_left atTop_le_cocompact).norm
  · exact (q.memLp (2 * k + 2 : ℕ) volume).integrable_norm_pow (by omega)
  · exact hz

/-- End-to-end source-only ceiling: every passive Schwartz mask and every genuine
upper-half-plane ZS eigenvalue satisfy the sharp even-moment source bound. -/
theorem passive_source_eigenvalue_bound (k : ℕ) {f g : 𝓢(ℝ, ℂ)} (m : ℝ → ℂ)
    (hg : PositiveSpectrum g) (hm : ∀ ξ, ‖m ξ‖ ≤ 1)
    (hf : ∀ ξ, f ξ = m ξ * g ξ) {ζ : ℂ} (hz : IsEigenvalue (𝓕⁻ f : 𝓢(ℝ, ℂ)) ζ) :
    (2 * k + 2 : ℝ) ^ (2 * k + 2) * ζ.im ^ (2 * k + 1) *
        (∫ s in (-1 : ℝ)..1, (1 - s ^ 2) ^ k) ≤
      2 * (2 * k + 1 : ℝ) ^ (2 * k + 1) * ∫ t, ‖𝓕⁻ g t‖ ^ (2 * k + 2) := by
  apply (schwartz_eigenvalue_even_moment_bound k (𝓕⁻ f) hz).trans
  apply mul_le_mul_of_nonneg_left _ (by positivity)
  simpa only [Nat.mul_add, Nat.mul_one] using passive_mask_even_moment m hg hm hf k

end ZS
