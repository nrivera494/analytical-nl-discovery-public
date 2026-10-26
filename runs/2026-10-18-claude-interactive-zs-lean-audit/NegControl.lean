/- Agent: claude-interactive. Model: claude-opus-5-5. Family: claude.
Task: T-20261018-claude-interactive-04. Negative control: this file must FAIL to elaborate.
0.07160 % lies below the true N = 9/2 gap of 0.0716052 %, so the rational certificate is false
and norm_num must reduce it to `False`. A pass here would mean the certificates are vacuous. -/
import ZSFormalization
open ZS

theorem neg_control :
    ∀ η ∈ attainableHeights (sechSource (9 / 2)), η ≤ 4 * (1 + 7160 / 10000000 : ℝ) :=
  (rational_sech_height_enclosure 4 (N := 9 / 2) (U := 4 * (1 + 7160 / 10000000))
    (by norm_num) (by norm_num) (by norm_num)).2
