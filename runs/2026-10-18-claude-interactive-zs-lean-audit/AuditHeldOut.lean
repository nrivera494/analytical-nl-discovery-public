/- Agent: claude-interactive. Model: claude-opus-5-5. Family: claude.
Task: T-20261018-claude-interactive-04. Cross-family audit of the ZSFormalization library.

Held-out certificates that the formalizer did not prepare, instantiated from the library's
general theorems, plus printouts of the definitions and headline statements. -/
import ZSFormalization

open ZS

/-- Frozen before the formalization existed (run 2026-10-18-claude-interactive-zs-moment-bound-check):
the N = 9/2 passive-mask ceiling is 0.07161 % above the attained height 4. -/
theorem audit_sech_nine_halves :
    (4 : ℝ) ∈ attainableHeights (sechSource (9 / 2)) ∧
      ∀ η ∈ attainableHeights (sechSource (9 / 2)), η ≤ 4 * (1 + 7161 / 10000000 : ℝ) := by
  convert rational_sech_height_enclosure 4 (N := 9 / 2)
    (U := 4 * (1 + 7161 / 10000000)) (by norm_num) (by norm_num) (by norm_num) using 1
  norm_num

/-- Frozen held-out value: the N = 15/2 ceiling is 0.01518 % above the attained height 7. -/
theorem audit_sech_fifteen_halves :
    (7 : ℝ) ∈ attainableHeights (sechSource (15 / 2)) ∧
      ∀ η ∈ attainableHeights (sechSource (15 / 2)), η ≤ 7 * (1 + 1518 / 10000000 : ℝ) := by
  convert rational_sech_height_enclosure 7 (N := 15 / 2)
    (U := 7 * (1 + 1518 / 10000000)) (by norm_num) (by norm_num) (by norm_num) using 1
  norm_num

/-- Integer order N = 7 from the general theorem (k = 6): the optimal fraction is 13/49. -/
theorem audit_order_seven : IsGreatest (attainableFractions (sechSource 7)) (13 / 49 : ℝ) := by
  have h := canonical_integer_sech_fraction_optimality 6
  norm_num at h
  exact h

#print axioms audit_sech_nine_halves
#print axioms audit_sech_fifteen_halves
#print axioms audit_order_seven

#print SolvesZS
#print IsEigenvalue
#print PositiveSpectrum
#print IsSechSource
#print attainableHeights
#print sourceEnergy
#print attainableFractions
#check @eigenvalue_even_moment_bound
#check @schwartz_eigenvalue_even_moment_bound
#check @passive_source_eigenvalue_bound
#check @canonical_integer_sech_optimality
#check @canonical_integer_sech_fraction_optimality
#check @rational_sech_height_enclosure
#check @canonical_gaussian_ceiling
