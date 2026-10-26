module

public import ZSFormalization.SpectralBound

@[expose] public section

/-! # Gaussian ceilings at positive even exponents

This module does not assert the continuous-exponent Hausdorff--Young refinement.
-/

open MeasureTheory FourierTransform
open scoped SchwartzMap

namespace ZS

noncomputable def gaussianPulse (N t : ℝ) : ℝ := N * Real.exp (-t ^ 2 / 2)

def IsGaussianSource (N : ℝ) (g : 𝓢(ℝ, ℂ)) : Prop :=
  PositiveSpectrum g ∧ ∀ t, 𝓕⁻ g t = (gaussianPulse N t : ℂ)

lemma gaussian_even_moment (k : ℕ) (N : ℝ) :
    (∫ t, gaussianPulse N t ^ (2 * k + 2)) =
      N ^ (2 * k + 2) * Real.sqrt (Real.pi / (k + 1 : ℝ)) := by
  have he : ∀ t, gaussianPulse N t ^ (2 * k + 2) =
      N ^ (2 * k + 2) * Real.exp (-(k + 1 : ℝ) * t ^ 2) := by
    intro t
    unfold gaussianPulse
    rw [mul_pow, ← Real.exp_nat_mul]
    congr 2
    push_cast
    ring
  simp_rw [he]
  rw [integral_const_mul, integral_gaussian]

/-- An exact source-only Gaussian ceiling for each positive even exponent. -/
theorem gaussian_source_polynomial_ceiling (k : ℕ) {N : ℝ} (hN : 0 ≤ N)
    {f g : 𝓢(ℝ, ℂ)} (hs : IsGaussianSource N g) (m : ℝ → ℂ)
    (hm : ∀ ξ, ‖m ξ‖ ≤ 1) (hf : ∀ ξ, f ξ = m ξ * g ξ)
    {ζ : ℂ} (hz : IsEigenvalue (𝓕⁻ f : 𝓢(ℝ, ℂ)) ζ) :
    (2 * k + 2 : ℝ) ^ (2 * k + 2) * ζ.im ^ (2 * k + 1) *
        (∫ s in (-1 : ℝ)..1, (1 - s ^ 2) ^ k) ≤
      2 * (2 * k + 1 : ℝ) ^ (2 * k + 1) * N ^ (2 * k + 2) *
        Real.sqrt (Real.pi / (k + 1 : ℝ)) := by
  have h := passive_source_eigenvalue_bound k m hs.1 hm hf hz
  have hn : ∀ t, ‖𝓕⁻ g t‖ = gaussianPulse N t := by
    intro t
    rw [hs.2, Complex.norm_real, Real.norm_eq_abs, abs_of_nonneg]
    exact mul_nonneg hN (Real.exp_pos _).le
  simp_rw [hn] at h
  rw [gaussian_even_moment] at h
  simpa only [mul_assoc] using h

end ZS
