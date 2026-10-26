module

public import Mathlib.Analysis.Fourier.Convolution
public import Mathlib.MeasureTheory.Function.L2Space
public import Mathlib.Tactic

@[expose] public section

/-! # Even-moment Fourier majorization for Schwartz spectra

Mathlib uses the character `exp (-2 * π * I * x * ξ)`. Both sides use the
same normalization, so no normalization constant occurs in the inequality.
-/

open MeasureTheory FourierTransform
open scoped SchwartzMap Convolution

namespace ZS

noncomputable def spectralConvolution (f g : 𝓢(ℝ, ℂ)) : 𝓢(ℝ, ℂ) :=
  SchwartzMap.convolution (ContinuousLinearMap.mul ℂ ℂ) f g

lemma spectralConvolution_apply (f g : 𝓢(ℝ, ℂ)) (x : ℝ) :
    spectralConvolution f g x = ∫ t, f t * g (x - t) := by
  simp [spectralConvolution, SchwartzMap.convolution_apply, convolution_def]

lemma convolution_integrand_integrable (f g : 𝓢(ℝ, ℂ)) (x : ℝ) :
    Integrable (fun t => f t * g (x - t)) := by
  apply (f.integrable.norm.mul_const (SchwartzMap.seminorm ℝ 0 0 g)).mono'
  · exact (f.continuous.mul (g.continuous.comp (continuous_const.sub continuous_id))).aestronglyMeasurable
  · filter_upwards with t
    rw [norm_mul]
    exact mul_le_mul_of_nonneg_left (SchwartzMap.norm_le_seminorm ℝ g (x - t)) (norm_nonneg _)

/-- Positivity of a spectrum, represented without a separate real-valued function. -/
def PositiveSpectrum (g : 𝓢(ℝ, ℂ)) : Prop := ∀ x, g x = (‖g x‖ : ℂ)

lemma spectralConvolution_positive {g h : 𝓢(ℝ, ℂ)}
    (hg : PositiveSpectrum g) (hh : PositiveSpectrum h) :
    PositiveSpectrum (spectralConvolution g h) := by
  intro x
  have heq : spectralConvolution g h x = (∫ t, ‖g t‖ * ‖h (x - t)‖ : ℝ) := by
    rw [spectralConvolution_apply]
    calc
      _ = ∫ t, ((‖g t‖ * ‖h (x - t)‖ : ℝ) : ℂ) := by
        congr 1; funext t; rw [Complex.ofReal_mul, ← hg t, ← hh (x - t)]
      _ = _ := integral_complex_ofReal
  rw [heq, Complex.norm_real, Real.norm_eq_abs, abs_of_nonneg (integral_nonneg (fun t => by positivity))]

lemma spectralConvolution_majorized {f₁ f₂ g₁ g₂ : 𝓢(ℝ, ℂ)}
    (hg₁ : PositiveSpectrum g₁) (hg₂ : PositiveSpectrum g₂)
    (h₁ : ∀ x, ‖f₁ x‖ ≤ ‖g₁ x‖) (h₂ : ∀ x, ‖f₂ x‖ ≤ ‖g₂ x‖) :
    ∀ x, ‖spectralConvolution f₁ f₂ x‖ ≤ ‖spectralConvolution g₁ g₂ x‖ := by
  intro x
  have heq : spectralConvolution g₁ g₂ x = (∫ t, ‖g₁ t‖ * ‖g₂ (x - t)‖ : ℝ) := by
    rw [spectralConvolution_apply]
    calc
      _ = ∫ t, ((‖g₁ t‖ * ‖g₂ (x - t)‖ : ℝ) : ℂ) := by
        congr 1; funext t; rw [Complex.ofReal_mul, ← hg₁ t, ← hg₂ (x - t)]
      _ = _ := integral_complex_ofReal
  rw [heq, Complex.norm_real, Real.norm_eq_abs,
    abs_of_nonneg (integral_nonneg (fun t => by positivity)), spectralConvolution_apply]
  apply (norm_integral_le_integral_norm _).trans
  apply integral_mono (convolution_integrand_integrable f₁ f₂ x).norm
  · simpa only [norm_mul] using (convolution_integrand_integrable g₁ g₂ x).norm
  · intro t
    simp only [norm_mul]
    exact mul_le_mul (h₁ t) (h₂ (x - t)) (norm_nonneg _) (norm_nonneg _)

noncomputable def convolutionPower (f : 𝓢(ℝ, ℂ)) : ℕ → 𝓢(ℝ, ℂ)
  | 0 => f
  | k + 1 => spectralConvolution (convolutionPower f k) f

lemma convolutionPower_positive {g : 𝓢(ℝ, ℂ)} (hg : PositiveSpectrum g) (k : ℕ) :
    PositiveSpectrum (convolutionPower g k) := by
  induction k with
  | zero => exact hg
  | succ k ih => exact spectralConvolution_positive ih hg

lemma convolutionPower_majorized {f g : 𝓢(ℝ, ℂ)} (hg : PositiveSpectrum g)
    (h : ∀ x, ‖f x‖ ≤ ‖g x‖) (k : ℕ) :
    ∀ x, ‖convolutionPower f k x‖ ≤ ‖convolutionPower g k x‖ := by
  induction k with
  | zero => exact h
  | succ k ih => exact spectralConvolution_majorized (convolutionPower_positive hg k) hg ih h

lemma fourier_convolutionPower (f : 𝓢(ℝ, ℂ)) (k : ℕ) (x : ℝ) :
    𝓕 (convolutionPower f k) x = (𝓕 f x) ^ (k + 1) := by
  induction k with
  | zero => simp [convolutionPower]
  | succ k ih =>
    simp [convolutionPower, spectralConvolution, SchwartzMap.fourier_convolution,
      SchwartzMap.pairing_apply_apply, ih, pow_succ]

lemma norm_sq_integrable (f : 𝓢(ℝ, ℂ)) : Integrable (fun t => ‖f t‖ ^ 2) :=
  (memLp_two_iff_integrable_sq_norm f.continuous.aestronglyMeasurable).mp (f.memLp 2 volume)

lemma even_moment_eq_convolutionPower (f : 𝓢(ℝ, ℂ)) (k : ℕ) :
    (∫ t, ‖𝓕 f t‖ ^ (2 * (k + 1))) = ∫ t, ‖convolutionPower f k t‖ ^ 2 := by
  rw [← SchwartzMap.integral_norm_sq_fourier]
  congr 1; funext t
  rw [fourier_convolutionPower, norm_pow, ← pow_mul, Nat.mul_comm]

/-- The full even-exponent Fourier-majorant inequality for Schwartz spectra. -/
theorem fourier_even_majorant {f g : 𝓢(ℝ, ℂ)} (hg : PositiveSpectrum g)
    (h : ∀ x, ‖f x‖ ≤ ‖g x‖) (k : ℕ) :
    (∫ t, ‖𝓕 f t‖ ^ (2 * (k + 1))) ≤ ∫ t, ‖𝓕 g t‖ ^ (2 * (k + 1)) := by
  rw [even_moment_eq_convolutionPower, even_moment_eq_convolutionPower]
  apply integral_mono (norm_sq_integrable _) (norm_sq_integrable _)
  intro t
  exact pow_le_pow_left₀ (norm_nonneg _) (convolutionPower_majorized hg h k t) 2

/-- The same result for the inverse transform used to launch optical pulses. -/
theorem inverse_fourier_even_majorant {f g : 𝓢(ℝ, ℂ)} (hg : PositiveSpectrum g)
    (h : ∀ x, ‖f x‖ ≤ ‖g x‖) (k : ℕ) :
    (∫ t, ‖𝓕⁻ f t‖ ^ (2 * (k + 1))) ≤ ∫ t, ‖𝓕⁻ g t‖ ^ (2 * (k + 1)) := by
  change (∫ t, ‖𝓕 f (-t)‖ ^ (2 * (k + 1))) ≤ ∫ t, ‖𝓕 g (-t)‖ ^ (2 * (k + 1))
  rw [integral_neg_eq_self (fun t => ‖𝓕 f t‖ ^ (2 * (k + 1))),
    integral_neg_eq_self (fun t => ‖𝓕 g t‖ ^ (2 * (k + 1)))]
  exact fourier_even_majorant hg h k

/-- Passive masks, with the regularity condition stated explicitly: the masked
spectrum `f` and the unmasked spectrum `g` must both be Schwartz. -/
theorem passive_mask_even_moment {f g : 𝓢(ℝ, ℂ)} (m : ℝ → ℂ)
    (hg : PositiveSpectrum g) (hm : ∀ x, ‖m x‖ ≤ 1)
    (hf : ∀ x, f x = m x * g x) (k : ℕ) :
    (∫ t, ‖𝓕⁻ f t‖ ^ (2 * (k + 1))) ≤ ∫ t, ‖𝓕⁻ g t‖ ^ (2 * (k + 1)) := by
  apply inverse_fourier_even_majorant hg
  intro x
  rw [hf, norm_mul]
  exact mul_le_of_le_one_left (norm_nonneg _) (hm x)

end ZS
