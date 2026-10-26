module

public import Mathlib.Analysis.MeanInequalities
public import Mathlib.Tactic

@[expose] public section

/-! # The sharp scalar inequality used in the ZS moment estimate -/

namespace ZS

/-- A denominator-free version of the sharp scalar inequality, for every integer
exponent `p = k + 2`. This is a proved inequality, not an analytical hypothesis. -/
theorem sharp_scalar (k : ℕ) {r s : ℝ} (hr : 0 ≤ r) (hs : 0 ≤ s) :
    (k + 2 : ℝ) ^ (k + 2) * s ^ (k + 1) * (r - s) ≤
      (k + 1 : ℝ) ^ (k + 1) * r ^ (k + 2) := by
  have h := pow_add_mul_le_add_pow
    (a := (k + 2 : ℝ) * s) (b := (k + 1 : ℝ) * r - (k + 2 : ℝ) * s)
    (by positivity)
    (by
      have : 0 ≤ (k + 2 : ℝ) * s + (k + 1 : ℝ) * r := by positivity
      linarith) (k + 2)
  have heq : (k + 2 : ℝ) * s + ((k + 1 : ℝ) * r - (k + 2 : ℝ) * s) =
      (k + 1 : ℝ) * r := by ring
  rw [heq] at h
  simp only [show k + 2 - 1 = k + 1 by omega, Nat.cast_add, Nat.cast_ofNat, mul_pow] at h
  have heq' : ((k + 2 : ℝ) ^ (k + 2) * s ^ (k + 2) +
      (k + 2 : ℝ) * ((k + 2 : ℝ) ^ (k + 1) * s ^ (k + 1)) *
        ((k + 1 : ℝ) * r - (k + 2 : ℝ) * s)) =
      (k + 1 : ℝ) * ((k + 2 : ℝ) ^ (k + 2) * s ^ (k + 1) * (r - s)) := by
    simp only [pow_succ]
    ring
  rw [heq'] at h
  apply (mul_le_mul_iff_right₀ (show (0 : ℝ) < k + 1 by positivity)).mp
  calc
    _ ≤ (k + 1 : ℝ) ^ (k + 2) * r ^ (k + 2) := h
    _ = _ := by rw [pow_succ]; ring

end ZS
